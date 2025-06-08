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
from customer.serializer import CustomerLedgerSerializer
from customer.models import CustomerLedger
from refinery_management.models import TransferCreationItems

res_msg = ResponseMessages()

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class OldGoldBillingView(viewsets.ViewSet):
    
    @transaction.atomic
    def create(self,request):

        request_data = request.data
        
        request_data['created_at'] = timezone.now()
        request_data['created_by'] = request.user.pk
        
        if request.user.role.is_admin == True:
            if request_data.get('branch') != None:
                branch = request_data.get('branch')
            else:
                branch = None
        else:
            branch = request.user.branch.pk

        request_data['branch'] = branch

        serializer = OldGoldBillDetailsSerializer(data=request_data)
        
        if serializer.is_valid():
            serializer.save()
            
            old_item_details = request.data.get('old_item_details',[])
            
            for old_item in old_item_details:
                
                old_item['old_bill_details'] = serializer.data['id']
                
                old_item_serializer = OldGoldItemDetailsSerializer(data=old_item)
                
                if old_item_serializer.is_valid():
                    
                    old_item_serializer.save()
                    
                else:
                    
                    transaction.rollback(True)
                    
                    return Response(
                        {
                            "data":old_item_serializer.errors,
                            "message":res_msg.not_create("Old Bill"),
                            "status":status.HTTP_400_BAD_REQUEST
                        },status=status.HTTP_200_OK
                    )
                    
            old_bill_update_queryset = OldGoldBillDetails.objects.get(id=serializer.data['id'])
            
            old_gold_weight = 0
            old_gold_pieces = 0
            gst_amount = 0
            old_gold_amount = 0
            
            old_item_queryset = OldGoldItemDetails.objects.filter(old_bill_details=serializer.data['id'])
            
            for item in old_item_queryset:
                
                old_gold_weight += item.old_gross_weight
                old_gold_pieces += 1
                old_gold_amount += item.total_amount
                gst_amount += item.gst_amount
                
            old_bill_update_dict = {
                "old_gold_weight":old_gold_weight,
                "old_gold_pieces" :old_gold_pieces,
                "old_gold_amount":old_gold_amount,
                "total_gst_amount":gst_amount
            }
                
            old_bill_update_serializer = OldGoldBillDetailsSerializer(old_bill_update_queryset,data=old_bill_update_dict,partial=True)
            
            if old_bill_update_serializer.is_valid():
                old_bill_update_serializer.save()
                
                ledger_data = {}
                
                ledger_data['customer_details'] = old_bill_update_serializer.data['customer_details']
                ledger_data['entry_date'] = timezone.now()
                ledger_data['entry_type'] = settings.OLD_PURCHASE_ENTRY
                ledger_data['transaction_type'] = settings.DEBIT_ENTRY
                ledger_data['invoice_number'] = None
                ledger_data['reffrence_number'] = old_bill_update_serializer.data['old_gold_bill_number']
                ledger_data['transaction_amount'] = old_bill_update_serializer.data['old_gold_amount']
                ledger_data['transaction_weight'] = 0.0
                ledger_data['branch'] = branch
                
                ledger_serializer = CustomerLedgerSerializer(data=ledger_data)
                
                if ledger_serializer.is_valid():
                    
                    ledger_serializer.save()
                    
                else:
                    transaction.set_rollback(True)
                    return Response(
                        {
                            "data":ledger_serializer.errors,
                            "message":res_msg.not_create("Old Gold Purchase"),
                            "status":status.HTTP_400_BAD_REQUEST
                        },status=status.HTTP_200_OK
                    )
            else:
                transaction.rollback(True)
                return Response(
                    {
                        "data":old_bill_update_serializer.errors,
                        "message":res_msg.not_create("Old Gold Bill"),
                        "status":status.HTTP_400_BAD_REQUEST
                    },status=status.HTTP_200_OK
                )
            
            return Response(
                {
                    "data":serializer.data,
                    "message":res_msg.create("Old Gold Bill"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
                
        else:
            return Response(
                {
                    "data":serializer.errors,
                    "message":res_msg.not_create("Old Gold Bill"),
                    "status":status.HTTP_400_BAD_REQUEST
                },status=status.HTTP_200_OK
            )
            
    def retrieve(self,request,pk):
        
        try:
           
            queryset = OldGoldBillDetails.objects.get(id=pk)
            
            serializer = OldGoldBillDetailsSerializer(queryset)
            
            res_data = serializer.data
            
            res_data['customer_details_name'] = queryset.customer_details.customer_name
            res_data['customer_details_mobile'] = queryset.customer_details.phone
            res_data['customer_details_gst'] = queryset.customer_details.gst_no
            
            old_item_queryset = OldGoldItemDetails.objects.filter(old_bill_details=serializer.data['id'])
            
            old_item_serializer = OldGoldItemDetailsSerializer(old_item_queryset,many=True)
            
            response_data = []
            
            for data in old_item_serializer.data:
                item_data = data
                
                item_queryset = OldGoldItemDetails.objects.get(id=data['id'])
                
                item_data['old_metal_name'] = item_queryset.old_metal.metal_name
                
                response_data.append(item_data)
                
            res_data['old_item_details_list'] = response_data
                
            return Response(
                {
                    "data":res_data,
                    "message":res_msg.retrieve("Old Gold Bill Details"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
            
        except OldGoldBillDetails.DoesNotExist:
            
            return Response(
                {
                    "message":res_msg.not_exists("Old GOld Bill"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
                
        except Exception as err:
            
            return Response(
                {
                    "data":str(err),
                    "message":res_msg.something_else(),
                    "status":status.HTTP_204_NO_CONTENT
                },status=status.HTTP_200_OK
            )

    @transaction.atomic
    def update(self,request,pk):
        
        try:
            
            if pk == None :
                return Response(
                    {
                        "message":res_msg.missing_fields("ID"),
                        "status":status.HTTP_204_NO_CONTENT
                    },status=status.HTTP_200_OK
                )

            request_data = request.data

            if request.user.role.id == False:
                branch = request.user.branch.id
            else:
                branch = request_data.get('branch')
            
            request_data['modified_at'] = timezone.now()
            request_data['modified_by'] = request.user.id
            request_data['branch'] = branch

            queryset = OldGoldBillDetails.objects.get(id=pk)
            
            serializer = OldGoldBillDetailsSerializer(queryset,data=request_data,partial=True)
            
            if serializer.is_valid():
                
                serializer.save()
                
                old_item_details = request_data.get('old_item_details',[])
                
                for old_item in old_item_details:

                    old_item_id = old_item.get('id') if old_item.get('id') else 0

                    if old_item_id != 0:
                        
                        old_item_queryset = OldGoldItemDetails.objects.get(id=old_item_id)
                        
                        old_item['old_bill_details'] = queryset.pk
                        
                        old_item_serializer = OldGoldItemDetailsSerializer(old_item_queryset,data=old_item,partial=True)
                        
                        if old_item_serializer.is_valid():
                            old_item_serializer.save()
                            
                        else:
                            
                            transaction.set_rollback(True)
                            return Response(
                                {
                                    "data":old_item_serializer.errors,
                                    "message":res_msg.not_update("Value Addition"),
                                    "status":status.HTTP_400_BAD_REQUEST
                                },status=status.HTTP_200_OK
                            )
                        
                    else:
                        
                        old_item['old_bill_details'] = queryset.pk
                        
                        old_item_serializer = OldGoldItemDetailsSerializer(data=old_item)
                        
                        if old_item_serializer.is_valid():
                            
                            old_item_serializer.save()
                            
                        else:
                            
                            transaction.set_rollback(True)
                            return Response(
                                {
                                    "data":old_item_serializer.errors,
                                    "message":res_msg.not_update("Value Addition"),
                                    "status":status.HTTP_400_BAD_REQUEST
                                },status=status.HTTP_200_OK
                            )
                            
                old_gold_bill_queryset = OldGoldBillDetails.objects.get(id=serializer.data['id'])
                
                old_gold_weight = 0
                old_gold_pieces = 0
                old_gold_amount = 0
                
                old_item_queryset = OldGoldItemDetails.objects.filter(old_bill_details=old_gold_bill_queryset.pk)
            
                for item in old_item_queryset:
                    
                    old_gold_weight += item.old_gross_weight
                    old_gold_pieces += 1
                    old_gold_amount += item.total_amount
                    
                old_bill_update_dict = {
                    "old_gold_weight":old_gold_weight,
                    "old_gold_pieces" :old_gold_pieces,
                    "old_gold_amount":old_gold_amount
                }
                
                old_gold_bill_serializer = OldGoldBillDetailsSerializer(old_gold_bill_queryset,data=old_bill_update_dict,partial=True)
                
                if old_gold_bill_serializer.is_valid():
                    old_gold_bill_serializer.save()
                    
                else:
                    
                    transaction.set_rollback(True)
                    return Response(
                        {
                            "data":old_gold_bill_serializer.errors,
                            "message":res_msg.not_update("Old Gold Bill"),
                            "status":status.HTTP_400_BAD_REQUEST
                        },status=status.HTTP_200_OK
                    )
                            
                return Response(
                    {
                        "data":serializer.data,
                        "message":res_msg.update("Old Bill"),
                        "status":status.HTTP_200_OK
                    },status=status.HTTP_200_OK
                )
                            
            else:
                
                return Response(
                    {
                        "data":serializer.errors,
                        "message":res_msg.not_update("Old Gold Bill"),
                        "status":status.HTTP_400_BAD_REQUEST
                    },status=status.HTTP_200_OK
                )
                
        except OldGoldBillDetails.DoesNotExist:
            
            return Response(
                {
                    "message":res_msg.not_exists("Old GOld Bill"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
            
        except Exception as err:
            
            return Response(
                {
                    "data":str(err),
                    "message":res_msg.something_else(),
                    "status":status.HTTP_204_NO_CONTENT
                },status=status.HTTP_200_OK
            )
            
    def destroy(self,request,pk):
        
        try:
            
            queryset = OldGoldBillDetails.objects.get(id=pk)
            
            if queryset.is_canceled == True:
                
                return Response(
                    {
                        "message":"The Bill is already cancelled",
                        "status":status.HTTP_204_NO_CONTENT
                    },status=status.HTTP_200_OK
                )
                
            if queryset.is_billed == True:
                
                return Response(
                    {
                        "message":"The Bill is already used",
                        "status":status.HTTP_204_NO_CONTENT
                    },status=status.HTTP_200_OK
                )
                
            transfer_creation_item_queryset = TransferCreationItems.objects.filter(old_item_details__old_bill_details=queryset.pk)
            
            if len(transfer_creation_item_queryset) != 0 :
                
                return Response(
                    {
                        "message":"Cannot Cancel the Bill after Transfer Creation",
                        "status":status.HTTP_204_NO_CONTENT
                    },status=status.HTTP_200_OK
                )
                
            try:
                
                ledger_queryset = CustomerLedger.objects.get(customer_details=queryset.customer_details.pk,entry_type=settings.OLD_PURCHASE_ENTRY,transaction_type=settings.DEBIT_ENTRY,reffrence_number=queryset.old_gold_bill_number)
                
                ledger_queryset.is_cancelled = True
                
                ledger_queryset.save()
                
            except Exception as err:
                
                pass
            
            queryset.is_canceled = True
            queryset.save()
            
            return Response(
                {
                    "message":"Bill cancelled sucessfully",
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
            
        except ProtectedError:
            
            return Response(
                {
                    "message":res_msg.related_item("Please Delete"),
                    "status":status.HTTP_204_NO_CONTENT
                },status=status.HTTP_200_OK
            )
            
        except OldGoldBillDetails.DoesNotExist:
            
            return Response(
                {
                    "message":res_msg.not_exists("Old GOld Bill"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
                
        except Exception as err:
            
            return Response(
                {
                    "data":str(err),
                    "message":res_msg.something_else(),
                    "status":status.HTTP_204_NO_CONTENT
                },status=status.HTTP_200_OK
            )
            
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class OldGoldBillListView(APIView):
    
    def post(self,request):
        
        request_data = request.data 

        search = request.data.get('search') if request.data.get('search') else ''
        from_date = request.data.get('from_date') if request.data.get('from_date') else None
        to_date = request.data.get('to_date') if request.data.get('to_date') else None
        bill_status = request.data.get('status') if request.data.get('status') else None
        customer = request.data.get('customer') if request.data.get('customer') else None
        page = request.data.get('page',1)
        items_per_page = request.data.get('items_per_page',10)
        
        filter_condition = {}
        combined_conditions=Q()

        if request.user.role.is_admin == True:
            if request_data.get('branch') != None:
                branch = request_data.get('branch')
            else:
                branch = None
        else:
            branch = request.user.branch.pk

        if branch != None:
            filter_condition['branch'] = branch
                
        if bill_status != None:
            filter_condition['is_canceled'] = bill_status
        
        if customer != None:
            filter_condition['customer_details'] = customer
            
        if from_date != None and to_date != None:
            date_range = (from_date,to_date)
            filter_condition['created_at__range'] = date_range
        
        if search != "":
            or_conditions = []
            or_conditions.append(Q(old_gold_bill_number__icontains=search))
        
            for condition in or_conditions:
                combined_conditions |= condition
        
        if len(filter_condition) != 0:
            queryset = OldGoldBillDetails.objects.filter(combined_conditions,**filter_condition).order_by('-id')
        else:
            queryset = OldGoldBillDetails.objects.filter(combined_conditions).order_by('-id')
        
        paginated_data = Paginator(queryset, items_per_page)
        serializer = OldGoldBillDetailsSerializer(paginated_data.get_page(page), many=True)
        total_items = len(queryset)
        
        response_data = []
        
        for data in serializer.data:
            
            old_gold_bill_queryset = OldGoldBillDetails.objects.get(id=data['id'])
            
            res_data = data
            
            res_data['customer_details_name'] = old_gold_bill_queryset.customer_details.customer_name
            
            response_data.append(res_data)
            
        return Response(
            {
                "data":{
                    "list":response_data,
                    "total_pages": paginated_data.num_pages,
                    "current_page": page,
                    "total_items": total_items,
                    "current_items": len(serializer.data)
                },
                "message":res_msg.retrieve("Old Gold Bill Table List"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated]) 
class OldGoldSerachView(APIView):
    
    def get(self,request,pk):
        
        try:
            
            queryset = OldGoldBillDetails.objects.get(old_gold_bill_number=pk)
            
            if queryset.is_billed == True:
                
                return Response(
                    {
                        "message":"Already Billed",
                        "status":status.HTTP_204_NO_CONTENT
                    },status=status.HTTP_200_OK
                )
            
            if queryset.is_canceled == True:
                
                return Response(
                    {
                        "message":"Old Gold Bill is cancelled",
                        "status":status.HTTP_204_NO_CONTENT
                    },status=status.HTTP_200_OK
                )
            
            serializer = OldGoldBillDetailsSerializer(queryset)
            
            res_data = serializer.data
            
            res_data['customer_details_name'] = queryset.customer_details.customer_name
            res_data['customer_details_mobile'] = queryset.customer_details.phone
            
            old_item_queryset = OldGoldItemDetails.objects.filter(old_bill_details=serializer.data['id'])
            
            old_item_serializer = OldGoldItemDetailsSerializer(old_item_queryset,many=True)
            
            response_data = []
            
            for data in old_item_serializer.data:
                item_data = data
                
                item_queryset = OldGoldItemDetails.objects.get(id=data['id'])
                
                item_data['old_metal_name'] = item_queryset.old_metal.metal_name
                
                response_data.append(item_data)
                
            res_data['old_item_details_list'] = response_data
                
            return Response(
                {
                    "data":res_data,
                    "message":res_msg.retrieve("Old Gold Bill Details"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
            
        except OldGoldBillDetails.DoesNotExist:
            
            return Response(
                {
                    "message":res_msg.not_exists("Old GOld Bill"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
                
        except Exception as err:
            
            return Response(
                {
                    "data":str(err),
                    "message":res_msg.something_else(),
                    "status":status.HTTP_204_NO_CONTENT
                },status=status.HTTP_200_OK
            )
            
        

# Generate Estimate Number
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class OldgoldNumberGenerateAPIView(APIView):
    def get(self,request):
        prefix = 'OG'  # Prefix for the estimate number
        random_number = random.randint(1000000, 9999999)
        oldgold_number = f'{prefix}-{random_number}'

        return Response(
            {
                "data": oldgold_number,
                "message" : res_msg.create("Old Gold Number"),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK
        ) 
        
        
            

            
