from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes, authentication_classes
from django.utils import timezone
from django.core.paginator import Paginator
from app_lib.response_messages import ResponseMessages
from django.conf import settings
from .serializer import *
from .models import *
from django.db import transaction
from django.db.models import Q
from django.db.models import ProtectedError
import random

res_msg = ResponseMessages()

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class OldGoldLedgerTouchList(APIView):
    
    def get(self,request,metal=None):
        
        filter_condition = {}

        metal = request.data.get('metal')

        if request.user.role.is_admin == False:
            branch = request.user.branch.pk
        else:
            branch = request.data.get('branch')

        filter_condition['branch'] = branch
                
        filter_condition['is_cancelled'] = False
        
        if metal != None:
            
            distinct_queryset = OldGoldLedger.objects.filter(metal_details=metal).values('touch').distinct().order_by('-touch')
            
        else:
            
            distinct_queryset = OldGoldLedger.objects.values('touch').distinct().order_by('-touch')
        
        
        response_data = []
        
        for touch in distinct_queryset:
            
            res_data = {}
            
            in_weight = 0.0
            out_weight = 0.0
            
            queryset = OldGoldLedger.objects.filter(touch=touch['touch'],**filter_condition)
            
            for data in queryset:
                
                if data.old_ledger_entry_type == settings.OLD_IN:
                    
                    in_weight += data.weight
                    
                else:
                    
                    out_weight += data.weight
                    
            remaining_weight = in_weight-out_weight
            
            res_data['touch'] = touch['touch']
            res_data['in_weight'] = in_weight
            res_data['out_weight'] = out_weight
            res_data['remaining_weight'] = remaining_weight
            
            response_data.append(res_data)
            
        return Response(
            {
                "data":{
                    "list":response_data
                },
                "message":res_msg.retrieve("Old Ledger Touch List"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class OldGoldLedgerListView(APIView):
    
    def post(self,request):
        
        permission = persmission_check( request=request,permission_type=settings.MODULE)
            
        if permission['error'] == True:
        
            if permission['error_status'] == 401 :
                
                return Response(
                    {
                        "message":permission['error_message'],
                        "status":status.HTTP_401_UNAUTHORIZED
                    },status=status.HTTP_401_UNAUTHORIZED
                )
                
            else:
                
                return Response(
                    {
                        "message":permission['error_message'],
                        "status":status.HTTP_204_NO_CONTENT
                    },status=status.HTTP_200_OK
                )
                
        filter_condition = {}
        
        if permission['branch_permission'] == True:
            
            if permission['branch'] != None:
                
                filter_condition['branch'] = permission['branch']
                
        vendor = request.data.get('vendor',None)
        old_ledger_entry_type = request.data.get('old_ledger_entry_type',None)
        metal = request.data.get('metal',None)
        touch = request.data.get('touch',None)
        cancel_status = request.data.get('cancel_status',None)
        from_date = request.data.get('from_date',None)
        to_date = request.data.get('to_date',None)
        search = request.data.get('search',"")
        page = request.data.get('page',1)
        items_per_page = request.data.get('items_per_page',10)
        
        if vendor != None:
            
            filter_condition['vendor_details'] = vendor
            
        if old_ledger_entry_type != None:
            
            filter_condition['old_ledger_entry_type'] = old_ledger_entry_type
            
        if metal != None:
            
            filter_condition['metal_details'] = metal
            
        if from_date != None and to_date!= None:
            
            date_range = (from_date,to_date)
            
            filter_condition['entry_date__range'] = date_range
            
        if touch != None:
            
            filter_condition['touch']=touch
            
        if len(filter_condition) != 0:
            
            calculation_queryset = OldGoldLedger.objects.filter(**filter_condition,is_cancelled=False).order_by('-id')
            
        else:
            calculation_queryset = OldGoldLedger.objects.filter(is_cancelled=False).order_by('-id')
            
        in_weight = 0.0
        out_weight = 0.0
        
        for calculations in calculation_queryset:
            
            if calculations.old_ledger_entry_type == settings.OLD_IN:
                
                in_weight += calculations.weight
            else:
                
                out_weight += calculations.weight
                
        remaining_weight = in_weight-out_weight
                
        if cancel_status != None:
            
            filter_condition['is_cancelled'] = cancel_status
            
        if search != "":
            
            filter_condition['refference_number__icontains'] = search
            
        if len(filter_condition) != 0:
            
            queryset = OldGoldLedger.objects.filter(**filter_condition).order_by('-id')
            
        else:
            
            queryset = OldGoldLedger.objects.all().order_by('-id')
            
        paginated_data = Paginator(queryset, items_per_page)
        serializer = OldGoldLedgerSerializer(paginated_data.get_page(page), many=True)
        total_items = len(queryset)
        
        response_data = []
        
        for data in serializer.data:
            
            res_data = data
            
            ledger_queryset = OldGoldLedger.objects.get(id=data['id'])
            
            res_data['metal_details_name'] = ledger_queryset.metal_details.metal_name
            
            if ledger_queryset.vendor_details != None:
                
                res_data['vendor_details_name'] = ledger_queryset.vendor_details.designer_name
                
            else:
                
                res_data['vendor_details_name'] = "-"
                
            response_data.append(res_data)
            
        for i in range(len(response_data)):
            
            response_data[i]['s_no'] = i+1
            
        return Response(
                {
                    "data":{
                        "list":response_data,
                        "total_ic_weight":in_weight,
                        "total_out_weight":out_weight,
                        "total_remaining_weight":remaining_weight,
                        "total_pages": paginated_data.num_pages,
                        "current_page": page,
                        "total_items": total_items,
                        "current_items": len(serializer.data)
                    },
                    "message":res_msg.retrieve("Metal Ledger Table List"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        
        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class MetalEntriesView(APIView):
    
    @transaction.atomic
    def post(self,request):
        
        permission = persmission_check( request=request,permission_type=settings.ADD)
            
        if permission['error'] == True:
        
            if permission['error_status'] == 401 :
                
                return Response(
                    {
                        "message":permission['error_message'],
                        "status":status.HTTP_401_UNAUTHORIZED
                    },status=status.HTTP_401_UNAUTHORIZED
                )
                
            else:
                
                return Response(
                    {
                        "message":permission['error_message'],
                        "status":status.HTTP_204_NO_CONTENT
                    },status=status.HTTP_200_OK
                )
                
        request_data = request.data 
        request_data['created_at'] = permission['time']
        request_data['created_by'] = permission['username']
        
        if permission['branch_permission'] == True:
            
            if permission['branch'] != None:
                
                request_data['branch'] = permission['branch']
                request_data['branch_name'] = permission['branch_name']
                
        try:
            
            entries_id_queryset = MetalEntries.objects.all().last()
            
            if entries_id_queryset:
                old_entry_id = entries_id_queryset.entry_id.split('-')
                
                new_entry_id = int(old_entry_id[1])+1
                
            else:
                new_entry_id=1
            
            new_entry_number = "MTL-"+str(new_entry_id)
            
        except MetalEntries.DoesNotExist :
            new_entry_number = "MTL-1"
            
        except Exception as err:
            return Response(
                {
                    "data":str(err),
                    "message":res_msg.something_else(),
                    "status":status.HTTP_204_NO_CONTENT
                },status=status.HTTP_200_OK
            )
            
        request_data['entry_id'] = new_entry_number
                
        serializer = MetalEntriesSerializer(data=request_data)
        
        if serializer.is_valid():
            
            serializer.save()
            
            old_leger_data = {}
                
            old_leger_data['entry_date'] = permission['time']
            old_leger_data['metal_details'] = serializer.data['metal_details']
            old_leger_data['old_ledger_entry_type'] = settings.OLD_IN
            old_leger_data['touch'] = serializer.data['touch']
            old_leger_data['weight'] = serializer.data['weight']
            old_leger_data['refference_number'] = serializer.data['entry_id']
            old_leger_data['created_by'] = permission['username']
            
            if permission['branch_permission'] == True:
                
                old_leger_data['branch'] = serializer.data['branch']
                old_leger_data['branch_name'] = serializer.data['branch_name']
                
            old_leger_serializer = OldGoldLedgerSerializer(data=old_leger_data)
            
            if old_leger_serializer.is_valid():
                
                old_leger_serializer.save()
                
            else:
                
                transaction.set_rollback(True)
                
                return Response(
                    {
                        "data":old_leger_serializer.errors,
                        "message":res_msg.not_create("Metal Entries"),
                        "status":status.HTTP_400_BAD_REQUEST
                    },status=status.HTTP_200_OK
                )
                
            return Response(
                {
                    "data":serializer.data,
                    "message":res_msg.create("Metal Entries"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
            
        else:
            
            return Response(
                {
                    "data":serializer.errors,
                    "message":res_msg.not_create("Metal Entries"),
                    "status":status.HTTP_400_BAD_REQUEST
                },status=status.HTTP_200_OK
            )
            
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class MetalEntriesListView(APIView):
    
    def post(self,request):
        
        permission = persmission_check( request=request,permission_type=settings.MODULE)
            
        if permission['error'] == True:
        
            if permission['error_status'] == 401 :
                
                return Response(
                    {
                        "message":permission['error_message'],
                        "status":status.HTTP_401_UNAUTHORIZED
                    },status=status.HTTP_401_UNAUTHORIZED
                )
                
            else:
                
                return Response(
                    {
                        "message":permission['error_message'],
                        "status":status.HTTP_204_NO_CONTENT
                    },status=status.HTTP_200_OK
                )
                
        filter_condition = {}
        
        if permission['branch_permission'] == True:
            
            if permission['branch'] != None:
                
                filter_condition['branch'] = permission['branch']
                
        metal = request.data.get('metal',None)
        search = request.data.get('search',"")
        page = request.data.get('page',1)
        items_per_page = request.data.get('items_per_page',10)
        
        if metal != None:
            
            filter_condition['metal_details'] = metal
            
        if search != "":
            
            filter_condition['entry_id__icontains'] = search
            
            
        if len(filter_condition) != 0:
            
            queryset = MetalEntries.objects.filter(**filter_condition).order_by('-id')
            
        else:
            
            queryset = MetalEntries.objects.all().order_by('-id')
            
        paginated_data = Paginator(queryset, items_per_page)
        serializer = MetalEntriesSerializer(paginated_data.get_page(page), many=True)
        total_items = len(queryset)
        
        response_data = []
        
        for data in serializer.data:
            
            entry_queryset = MetalEntries.objects.get(id=data['id'])
            
            res_data = data
            
            res_data['metal_details_name'] = entry_queryset.metal_details.metal_name
            
            response_data.append(res_data)
            
        for i in range(len(response_data)):
            
            response_data[i]['s_no'] = i+1
            
        return Response(
            {
                "data":{
                    "list":response_data,
                    "total_pages": paginated_data.num_pages,
                    "current_page": page,
                    "total_items": total_items,
                    "current_items": len(serializer.data)
                },
                "message":res_msg.retrieve("Metal Entries Table List"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
                
        
        
        
        
        