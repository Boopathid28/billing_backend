from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from billing.models import BillingExchangeDetails
from app_lib.response_messages import ResponseMessages
from rest_framework import status, viewsets
from accounts.models import User
from .models import BagID,BagNumber
from django.conf import settings
from django.utils import timezone
from .serializer import *
from django.core.paginator import Paginator
from django.db.models import ProtectedError
from organizations.models import Staff
from vendor_management.models import VendorLedger
from vendor_management.serializer import VendorLedgerSerializer
from django.db.models import Q
from django.db import transaction
from old_gold_ledger.serializer import OldGoldLedgerSerializer
from old_gold_management.models import *


res_msg = ResponseMessages()

# Create your views here.
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class OldMetalCategoryListView(APIView):
    def get(self,request):
        
        queryset = list(OldMetalCategory.objects.all().values('id','category_name').order_by('id'))
        
        return Response(
            {
                "data":{
                    "list":queryset
                },
                "message":res_msg.retrieve("Old Metal Category"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class TransferCreationTypeListView(APIView):
    
    def get(self,request):
        
        queryset = TransferCreationType.objects.all().values('id','type_name').order_by('id')
        
        return Response(
            {
                "data":{
                    "list":queryset
                },
                "message":res_msg.retrieve("Transfer Creation Type List"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class AllOldGoldList(APIView):
    def post(self,request):
        
        request_data = request.data
        
        metal = request_data.get('metal') if request_data.get('metal') != None else None
        branch = request_data.get('branch') if request_data.get('branch') != None else None
        from_date = request_data.get('from_date') if request_data.get('from_date') != None else None
        to_date = request_data.get('to_date') if request_data.get('to_date') != None else None
        
        filter_condition = {}
        
        if request.user.role.is_admin == True:
            if branch != None:
                filter_condition['old_bill_details__branch'] = branch
        else:
            filter_condition['old_bill_details__branch'] = request.user.branch.pk
            
        if metal != None:
            filter_condition['old_metal'] = metal
            
        if from_date != None and to_date != None:
            date_range = (from_date,to_date)
            
            filter_condition['old_bill_details__created_at__range'] = date_range
            
        filter_condition['is_transffered'] = False
        filter_condition['old_bill_details__is_canceled'] = False
        
        response_data = []
        
        total_gross_weight = 0
        total_net_weight = 0
        total_dust_weight = 0
        
        if len(filter_condition) != 0:
            queryset = OldGoldItemDetails.objects.filter(**filter_condition).order_by('-id')
            
        else:
            queryset = OldGoldItemDetails.objects.all().order_by('-id')
        
        for data in queryset:
            
            res_data={
                "id":data.pk,
                "refference_number":data.old_bill_details.old_gold_bill_number,
                "old_metal":data.old_metal.pk,
                "old_metal_name":data.old_metal.metal_name,
                "old_gross_weight":data.old_gross_weight,
                "old_net_weight":data.old_net_weight,
                "dust_weight":data.old_dust_weight,
                "recieved_date":data.old_bill_details.created_at,
                "customer_name":data.old_bill_details.customer_details.customer_name
            }
            
            response_data.append(res_data)
            
            total_gross_weight += data.old_gross_weight
            total_net_weight += data.old_net_weight
            total_dust_weight += data.old_dust_weight
            
        if len(response_data) != 0:
            return Response(
                {
                    "data":{
                        "list" : response_data,
                        "total_gross_weight" : total_gross_weight,
                        "total_net_weight" : total_net_weight,
                        "total_dust_weight" : total_dust_weight
                    },
                    "message":res_msg.retrieve("Old Metal List"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
            
        else:
            return Response(
                {
                    "message":"No Data Found",
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
            
        
        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class BagnumberView(APIView):  
    def get(self, request):  
        try:
            
            user_id = request.user.id
            user_instance = User.object.get(id=user_id)
            try:
                bag_number = BagNumber.objects.get(user=user_instance)
                return Response(
                    {
                        "data": bag_number.bag_number,
                        "message": "Bag Number found",
                        "status": status.HTTP_200_OK
                    },
                    status=status.HTTP_200_OK
                )
            except BagNumber.DoesNotExist:
                next_bag_number = self.generatebagnumber()
                
                BagNumber.objects.create(user=user_instance, bag_number=next_bag_number)

                return Response(
                    {
                        "data": next_bag_number,
                        "message": "New Bag Number generated",
                        "status": status.HTTP_200_OK
                    },
                    status=status.HTTP_200_OK
                )

        except Exception as err:
            return Response(
                {
                    "data": str(err),
                    "message": res_msg.something_else(),
                    "status": status.HTTP_204_NO_CONTENT
                },
                status=status.HTTP_200_OK
            )
            
    def generatebagnumber(self):
        try:
            bag_queryset = BagID.objects.all().order_by('-id').first()
            
            if bag_queryset:
                number = int(bag_queryset.pk) + 1
            else:
                number = 1
            prefix = 'BAG-00'
            bag_number = f'{prefix}{number}'
            pbag_number = BagID.objects.create(bag_id=bag_number)
            return bag_number
        except Exception as err:
            pbag_number = BagID.objects.create(bag_id='BAG-001')
            return 'BAG-001'
        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class TransferCreationView(viewsets.ViewSet):
    
    def create(self,request):
        
        try:
        
            request_data = request.data
            
            transfer_creation_details = request_data
            
            if request.user.role.is_admin == False:
                transfer_creation_details['branch'] = request.user.branch.pk
            
            transfer_creation_details['created_by'] = request.user.id
            transfer_creation_details['created_at'] = timezone.now()
            
            transfer_creation_serialier = TransferCreationSerializer(data=transfer_creation_details)
            
            if transfer_creation_serialier.is_valid():
                transfer_creation_serialier.save()
                response_data=transfer_creation_serialier.data
            
                transfer_creation_item_details = transfer_creation_details.get('item_details')
            
                item_details = []
                
                for old_item in transfer_creation_item_details:
                    old_gold_id = old_item['old_gold_id']

                    old_item['transfet_creation_details'] = transfer_creation_serialier.data['id']
                    old_item['old_item_details'] = old_item.get('old_gold_id')
                    old_item['old_metal'] = old_item.get('old_metal')
                    old_item['old_gold_number'] = old_item.get('refference_number')
                    old_item['received_date'] = old_item.get('received_date')
                    old_item['transfered_date'] = old_item.get('transfered_date')
                    old_item['gross_weight'] = old_item.get('gross_weight')
                    old_item['net_weight'] = old_item.get('net_weight')
                    old_item['dust_weight'] = old_item.get('dust_weight')
                    old_item['transfered_date'] = timezone.now().date()
                    
                    old_item_serializer = TransferCreationItemsSerializer(data=old_item)
                    
                    if old_item_serializer.is_valid():
                        old_item_serializer.save()
                        item_details.append(old_item_serializer.data)
                        
                        old_item_queryset = OldGoldItemDetails.objects.get(id=old_item_serializer.data['old_item_details'])
                    
                        old_item_queryset.is_transffered = True
                        
                        old_item_queryset.save()
                    else:
                        raise Exception(old_item_serializer.errors)
                    
                if transfer_creation_details['transfer_type'] == settings.BAG_TRANSFER:
                    queryset = BagNumber.objects.get(user=request.user.id)
                    queryset.delete()
                    
                response_data['item_details'] = item_details
                
                return Response(
                    {
                        "data":response_data,
                        "message":res_msg.create("Transfer Creation"),
                        "status":status.HTTP_200_OK
                    },status=status.HTTP_200_OK
                )
                    
            else:
                raise Exception(transfer_creation_serialier.errors)
            
        except Exception as err:
            try:
                DeleteTransferCreation(transfer_creation_serialier.data['id'])
                
            except :
                pass
            
            return Response(
                {
                    "data":str(err),
                    "message":res_msg.something_else(),
                    "status":status.HTTP_204_NO_CONTENT
                },status=status.HTTP_200_OK
            )
            
        
def DeleteTransferCreation(pk):
    try:
        queryset = TransferCreation.objects.get(id=pk)
        queryset.delete()
        
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
class TransferCreationList(APIView):
    
    def get(self,request):
        
        if request.user.role.is_admin == False:
            
            queryset = TransferCreation.objects.filter(branch=request.user.branch.pk,transfer_type=settings.BAG_TRANSFER)
            
        else:   
            
            queryset = TransferCreation.objects.filter(transfer_type=settings.BAG_TRANSFER)
            
        response_data = []
        
        for data in queryset:
            
            res_data = {}
            res_data['id'] = data.pk
            res_data['refference_number'] = data.refference_number
            res_data['smith'] = data.smith.pk
            res_data['smith_name'] = data.smith.account_head_name
            res_data['metal'] = data.metal.pk
            res_data['metal_name'] = data.metal.metal_name
            res_data['total_gross_weight'] = data.total_gross_weight
            res_data['total_net_weight'] = data.total_net_weight
            res_data['total_dust_weight'] = data.total_dust_weight
            
            response_data.append(res_data)
            
        return Response(
            {
                "data":{
                    "list":response_data
                },
                "message":res_msg.retrieve("Transfer Creation List"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
        
    def post(self,request):
        
        request_data = request.data
        
        smith = request_data.get('smith') if request_data.get('smith') else None
        transfer_type = request_data.get('transfer_type') if request_data.get('transfer_type') else None
        branch = request_data.get('branch') if request_data.get('branch') else None
        metal = request_data.get('metal') if request_data.get('metal') else None
        from_date = request_data.get('from_date') if request_data.get('from_date') else None
        to_date = request_data.get('to_date') if request_data.get('to_date') else None
        search = request_data.get('search') if request_data.get('search') else None
        page = request.data.get('page') if request.data.get('page') else None
        items_per_page = request.data.get('items_per_page') if request.data.get('items_per_page') else None
        
        filter_condition = {}
        
        if request.user.role.is_admin == False:
            filter_condition['branch'] = request.user.branch.pk
            
        else:
            if branch != None:
                filter_condition['branch'] = branch
                
        if smith != None:
            
            filter_condition['smith'] = smith
            
        if transfer_type != None:
            
            filter_condition['transfer_type'] = transfer_type
            
        if metal != None:
            
            filter_condition['metal'] = metal
            
        if from_date != None and to_date != None: 
            date_range = (from_date,to_date)
            
            filter_condition['created_at__range'] = date_range
            
        if search != None:
            filter_condition['refference_number__icontains'] = search
            
        if len(filter_condition) != 0:
            
            queryset = TransferCreation.objects.filter(**filter_condition).order_by('id')
        
        else:
            
            queryset = TransferCreation.objects.all().order_by('id')
            
        if items_per_page != None:
            paginated_data = Paginator(queryset, items_per_page)
            serializer = TransferCreationSerializer(paginated_data.get_page(page), many=True)
            total_pages = paginated_data.num_pages
            current_page=page
            
        else:
            serializer = TransferCreationSerializer(queryset, many=True)
            total_pages=1
            current_page=1
            
        response_data=[]
        
        for i in serializer.data:
            
            res_data=i
            
            details_queryset = TransferCreation.objects.get(id=i['id'])
            
            res_data['transfer_type_name'] = details_queryset.transfer_type.type_name
            res_data['smith_name'] = details_queryset.smith.account_head_name
            res_data['metal_name'] = details_queryset.metal.metal_name
            res_data['branch_name'] = details_queryset.branch.branch_name
            res_data['transfer_category_name'] = details_queryset.transfer_category.category_name
            
            response_data.append(res_data)
            
        return Response(
            {
                "data":{
                    "list":response_data,
                    "total_pages": total_pages,
                    "current_page": current_page,
                    "total_items": len(queryset),
                    "current_items": len(serializer.data)
                },
                "message":res_msg.retrieve("Transfer Creation"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
        
        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class MeltingIssueView(viewsets.ViewSet):
    @transaction.atomic
    def create(self,request):
        
        request_data = request.data
        
        if request.user.role.is_admin == False:
            
            request_data['branch'] = request.user.branch.pk
            
        request_data['is_issued'] = True
        request_data['issued_by'] = request.user.id
        request_data['issued_at'] = timezone.now()
        
        request_data['melting_status'] = settings.MELTING_ISSUED
        
        serializer = MeltingIssueSerializer(data=request_data)
        
        if serializer.is_valid():
            serializer.save()
            
            try:
                print(request_data['transfer_creation_details'])
                transfer_creation_queryset = TransferCreation.objects.get(id=request_data['transfer_creation_details'])
                
            except TransferCreation.DoesNotExist:
                
                return Response(
                    {
                        "message":res_msg.not_exists("Bag Details"),
                        "status":status.HTTP_404_NOT_FOUND
                    },status=status.HTTP_200_OK
                )
            transfer_creation_queryset.is_issued = True
            transfer_creation_queryset.save()

            melting_issue_number = MeltingIssueNumber.objects.get(user = request.user.pk)
            melting_issue_number.delete()
            
            return Response(
                {
                    "data":serializer.data,
                    "message":res_msg.create("Melting Issue"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
            
        else:
            
            return Response(
                {
                    "data":serializer.errors,
                    "message":res_msg.not_create("Melting Issue"),
                    "status":status.HTTP_400_BAD_REQUEST
                },status=status.HTTP_200_OK
            )
            
    def retrieve(self,request,pk):
        
        try:
            
            queryset = MeltingIssue.objects.get(id=pk)
            
            serializer = MeltingIssueSerializer(queryset)
            
            res_data = serializer.data
            
            res_data['metal'] = queryset.transfer_creation_details.metal.pk
            res_data['smith'] = queryset.transfer_creation_details.smith.pk
            
            
            return Response(
                {
                    "data":res_data,
                    "message":res_msg.retrieve("Melting Issue"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
            
        except MeltingIssue.DoesNotExist:
            
            return Response(
                {
                    "message":res_msg.not_exists("Melting Issue"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
            
    def update(self,request,pk):
        
        try:
            
            queryset = MeltingIssue.objects.get(id=pk)
            
            request_data = request.data
            
            serializer = MeltingIssueSerializer(queryset,data=request_data,partial=True)
            
            if serializer.is_valid():
                serializer.save()
                
                return Response(
                    {
                        "data":serializer.data,
                        "message":res_msg.update("Melting Issue"),
                        "status":status.HTTP_200_OK
                    },status=status.HTTP_200_OK
                )
                
            else:
                
                return Response(
                    {
                        "data":serializer.errors,
                        "message":res_msg.not_update("Melting Issue"),
                        "status":status.HTTP_400_BAD_REQUEST
                    },status=status.HTTP_200_OK
                )
            
        except MeltingIssue.DoesNotExist:
            
            return Response(
                {
                    "message":res_msg.not_exists("Melting Issue"),
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
    def delete(self,request,pk):
        
        try:
            
            queryset = MeltingIssue.objects.get(id=pk)
            
            if queryset.is_cancelled == True:
                
                return Response(
                    {
                        "message":"Melting Already Cancelled",
                        "stauts":status.HTTP_204_NO_CONTENT
                    },status=status.HTTP_200_OK
                )
            
            if queryset.is_received == True:
                    
                return Response(
                    {
                        "message":"Melting Already Received",
                        "stauts":status.HTTP_204_NO_CONTENT
                    },status=status.HTTP_200_OK
                )
            
            try:
                
                transfer_creation_queryset = TransferCreation.objects.get(id=queryset.transfer_creation_details.pk)
                transfer_creation_queryset.is_issued = False
                
                transfer_creation_queryset.save()
                
            except TransferCreation.DoesNotExist:
                
                return Response(
                    {
                        "message":res_msg.not_exists("Transfer Creation Details"),
                        "status":status.HTTP_404_NOT_FOUND
                    },status=status.HTTP_200_OK
                )
                
            except Exception as err:
                transaction.set_rollback(True)
                return Response(
                    {
                        "data":str(err),
                        "message":res_msg.something_else(),
                        "status":status.HTTP_204_NO_CONTENT
                    },status=status.HTTP_200_OK
                )
                
            queryset.is_cancelled = True
            queryset.save()
            
            return Response(
                {
                    "message":res_msg.delete("Melting Issue"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
            
        except MeltingIssue.DoesNotExist:
            
            return Response(
                {
                    "message":res_msg.not_exists("Melting issue"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
            
        except ProtectedError:
            
            return Response(
                {
                    "message":res_msg.related_item("Please Delete"),
                    "status":status.HTTP_204_NO_CONTENT
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
class MeltingIssueList(APIView):
    
    def get(self,request):
        
        if request.user.role.is_admin == False:
            
            queryset =list(MeltingIssue.objects.filter(branch = request.user.branch.pk).exclude(melting_status=settings.MELTING_RECEIVED).order_by('id'))
            
        else:
            
            queryset = list(MeltingIssue.objects.all().exclude(melting_status=settings.MELTING_RECEIVED).order_by('id'))
            
        response_data = []
        
        for data in queryset :
            
            
            res_data = {}
            res_data['id'] = data.pk
            res_data['melting_issue_id'] = data.melting_issue_id
            res_data['bag_number'] = data.transfer_creation_details.refference_number
            res_data['smith_name'] = data.transfer_creation_details.smith.account_head_name
            res_data['metal_name'] = data.transfer_creation_details.metal.metal_name
            res_data['issued_category_name'] = data.issued_category.category_name
            res_data['issued_date'] = data.issued_date
            res_data['return_date'] = data.return_date
            res_data['bullion_rate'] = data.bullion_rate
            res_data['stone_weight'] = data.stone_weight
            res_data['gross_weight'] = data.gross_weight
            res_data['net_weight'] = data.net_weight
            res_data['notes'] = data.notes
            
            response_data.append(res_data)
            
        return Response(
            {
                "data":{
                    "list":response_data
                },
                "message":res_msg.retrieve("Melting Issue List"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
    
    def post(self,request):
        
        issue_from_date = request.data.get('from_date') if request.data.get('from_date') else None
        issue_to_date = request.data.get('to_date') if request.data.get('to_date') else None
        vendor = request.data.get('vendor') if request.data.get('vendor') else None
        search = request.data.get('search') if request.data.get('search') else ""
        branch = request.data.get('branch') if request.data.get('branch') else None
        page = request.data.get('page') if request.data.get('page') else None
        items_per_page = request.data.get('items_per_page') if request.data.get('items_per_page') else None
        
        filter_condition = {}
        
        if request.user.role.is_admin == False:
            
            filter_condition['branch'] = request.user.branch.pk
            
        else:
            if branch!= None:
                filter_condition['branch'] = branch
                
        if vendor != None:
            
            filter_condition['transfer_creation_details__smith'] = vendor
            
        if issue_from_date != None and issue_to_date != None:
            
            date_range = (issue_from_date,issue_to_date)
            
            filter_condition['issued_date__range'] = date_range
            
        if len(filter_condition) != 0 :
            
            queryset = MeltingIssue.objects.filter(Q(transfer_creation_details__refference_number__icontains=search) |Q(melting_issue_id__icontains=search),**filter_condition).order_by('id')
            
        else:
            queryset = MeltingIssue.objects.filter(Q(transfer_creation_details__refference_number__icontains=search) |Q(melting_issue_id__icontains=search)).order_by('id')
            
        if items_per_page != None:
            paginated_data = Paginator(queryset, items_per_page)
            serializer = MeltingIssueSerializer(paginated_data.get_page(page), many=True)
            total_pages = paginated_data.num_pages
            current_page=page
            
        else:
            serializer = MeltingIssueSerializer(queryset, many=True)
            total_pages=1
            current_page=1
            
        response_data=[]
        
        for i in serializer.data:
            
            res_data=i
            
            details_queryset = MeltingIssue.objects.get(id=i['id'])
            
            res_data['bag_number'] = details_queryset.transfer_creation_details.refference_number
            res_data['smith_name'] = details_queryset.transfer_creation_details.smith.account_head_name
            res_data['melting_status_name'] = details_queryset.melting_status.status_name
            res_data['melting_status_colour'] = details_queryset.melting_status.color
            res_data['branch_name'] = details_queryset.branch.branch_name
            res_data['issued_category_name'] = details_queryset.issued_category.category_name
            
            try:
                staff = Staff.objects.get(user = details_queryset.issued_by.pk)
                username = staff.first_name

            except:
                username = '-'
                
            res_data['issued_by_name'] = username
            
            response_data.append(res_data)
            
        return Response(
            {
                "data":{
                    "list":response_data,
                    "total_pages": total_pages,
                    "current_page": current_page,
                    "total_items": len(queryset),
                    "current_items": len(serializer.data)
                },
                "message":res_msg.retrieve("Melting Issue"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class MeltingIssueNumberView(APIView):
    def get(self, request):  
        try:
            
            user_id = request.user.id
            user_instance = User.object.get(id=user_id)
            try:
                melting_issue_number = MeltingIssueNumber.objects.get(user=user_instance)
                return Response(
                    {
                        "data": melting_issue_number.melting_issue_number,
                        "message": "Melting Issue Number found",
                        "status": status.HTTP_200_OK
                    },
                    status=status.HTTP_200_OK
                )
            except MeltingIssueNumber.DoesNotExist:
                next_melting_issue_number = self.generatemeltingissuenumber()
                
                MeltingIssueNumber.objects.create(user=user_instance, melting_issue_number=next_melting_issue_number)

                return Response(
                    {
                        "data": next_melting_issue_number,
                        "message": "New Melting Issue Number generated",
                        "status": status.HTTP_200_OK
                    },
                    status=status.HTTP_200_OK
                )

        except Exception as err:
            return Response(
                {
                    "data": str(err),
                    "message": res_msg.something_else(),
                    "status": status.HTTP_204_NO_CONTENT
                },
                status=status.HTTP_200_OK
            )
            
        
    def generatemeltingissuenumber(self):
        try:
            melting_issue_queryset = MeltingIssueID.objects.all().order_by('-id').first()
            
            if melting_issue_queryset:
                number = int(melting_issue_queryset.pk) + 1
            else:
                number = 1
            prefix = 'MELT-ISSUE-00'
            melting_issue_number = f'{prefix}{number}'
            pmelting_issue_number = MeltingIssueID.objects.create(melting_issue_id=melting_issue_number)
            return melting_issue_number
        except Exception as err:
            pmelting_issue_number = MeltingIssueID.objects.create(melting_issue_id='MELT-ISSUE-001')
            return 'MELT-ISSUE-001'
        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class MeltingReciptNumberView(APIView):
    def get(self, request):  
        try:
            
            user_id = request.user.id
            user_instance = User.object.get(id=user_id)
            try:
                melting_recipt_number = MeltingReciptNumber.objects.get(user=user_instance)
                return Response(
                    {
                        "data": melting_recipt_number.melting_recipt_number,
                        "message": "Melting Recipt Number found",
                        "status": status.HTTP_200_OK
                    },
                    status=status.HTTP_200_OK
                )
            except MeltingReciptNumber.DoesNotExist:
                next_melting_recipt_number = self.generatemeltingReciptnumber()
                
                MeltingReciptNumber.objects.create(user=user_instance, melting_recipt_number=next_melting_recipt_number)

                return Response(
                    {
                        "data": next_melting_recipt_number,
                        "message": "New Melting Recipt Number generated",
                        "status": status.HTTP_200_OK
                    },
                    status=status.HTTP_200_OK
                )

        except Exception as err:
            return Response(
                {
                    "data": str(err),
                    "message": res_msg.something_else(),
                    "status": status.HTTP_204_NO_CONTENT
                },
                status=status.HTTP_200_OK
            )
            
        
    def generatemeltingReciptnumber(self):
        try:
            melting_recipt_queryset = MeltingReciptID.objects.all().order_by('-id').first()
            
            if melting_recipt_queryset:
                number = int(melting_recipt_queryset.pk) + 1
            else:
                number = 1
            prefix = 'MELT-RCPT-00'
            melting_recipt_number = f'{prefix}{number}'
            pmelting_Recipt_number = MeltingReciptID.objects.create(melting_recipt_id=melting_recipt_number)
            return melting_recipt_number
        except Exception as err:
            pmelting_Recipt_number = MeltingReciptID.objects.create(melting_recipt_id='MELT-RCPT-001')
            return 'MELT-RCPT-001'
        

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class MeltingReciptView(viewsets.ViewSet):
    
    def create(self,request):
        
        request_data = request.data
        
        if request.user.role.is_admin == False:
            branch = request.user.branch.pk
        else:
            branch = request_data.get('branch')

        vendor_queryset = MeltingIssue.objects.get(id = request_data.get('melting_issue_details'))
        
        request_data['branch'] = branch
        request_data['vendor_details'] = vendor_queryset.vendor_details.pk

        melting_charges = float(request_data.get('melting_charges'))
        amount_paid = float(request_data.get('amount_paid'))
        
        if amount_paid == 0:
            request_data['payment_status'] = settings.PAYMENT_PENDING
        elif 0 < amount_paid < melting_charges :
            request_data['payment_status'] = settings.PARTIALLY_PAID
        elif amount_paid == melting_charges :
            request_data['payment_status'] = settings.PAID
        elif amount_paid > melting_charges :
            
            return Response(
                {
                    "message":"The Paid Amount is more than Melting Charges",
                    "status":status.HTTP_204_NO_CONTENT
                },status=status.HTTP_200_OK
            )
        
        request_data['received_by'] = request.user.pk
        request_data['received_at'] = timezone.now()
        request_data['melting_status'] = int(settings.MELTING_RECEIVED)
        
        serializer = MeltingReciptSerializer(data=request_data)
        
        if serializer.is_valid():
            serializer.save()

            try:
                melting_issue_queryset = MeltingIssue.objects.get(id=request_data['melting_issue_details'])

                melting_issue_queryset.is_received = True
                melting_issue_queryset.save()

            except MeltingIssue.DoesNotExist:
                transaction.set_rollback(True)
                return Response(
                    {
                        "message":res_msg.not_exists("Melting Issue"),
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

            ledger_data = {}

            ledger_data['vendor_details'] = vendor_queryset.vendor_details.pk
            ledger_data['transaction_date'] = timezone.now()
            ledger_data['refference_number'] = serializer.data['melting_recipt_id']
            ledger_data['transaction_type'] = settings.MELTING_VENDOR_LEDGER
            ledger_data['transaction_weight'] = 0.0
            ledger_data['transaction_amount'] = serializer.data['melting_charges']
            ledger_data['branch'] = serializer.data['branch']
            
            ledger_serializer = VendorLedgerSerializer(data=ledger_data)
            
            if ledger_serializer.is_valid():
                ledger_serializer.save()
            else:
                transaction.set_rollback(True)
                return Response(
                    {
                        "data":ledger_serializer.errors,
                        "message":res_msg.not_create("Melting Recipt"),
                        "status":status.HTTP_400_BAD_REQUEST
                    },status=status.HTTP_200_OK
                )
            
                
            recipt_number_queryset = MeltingReciptNumber.objects.get(user = request.user.pk)
            recipt_number_queryset.delete()
            
            res_data = serializer.data
            
            status_queryset = StatusTable.objects.get(id=int(settings.MELTING_RECEIVED))
            
            melting_issue_queryset = MeltingIssue.objects.get(id=res_data['melting_issue_details'])
            
            melting_issue_queryset.melting_status = status_queryset
            
            melting_issue_queryset.save()
            
            return Response(
                {
                    "data":res_data,
                    "message":res_msg.create("Melting Recipt"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
            
        else:
            
            return Response(
                {
                    "data":serializer.errors,
                    "message":res_msg.not_create("Melting Recipt"),
                    "status":status.HTTP_400_BAD_REQUEST
                },status=status.HTTP_200_OK
            )
            
    def retrieve(self,request,pk):
        
        try:
            
            queryset = MeltingRecipt.objects.get(id=pk)
            
            serializer = MeltingReciptSerializer(queryset)
            
            res_data = serializer.data
            
            res_data['melting_issue_id'] = queryset.melting_issue_details.melting_issue_id
            res_data['bag_number'] = queryset.melting_issue_details.transfer_creation_details.refference_number
            res_data['smith_name'] = queryset.melting_issue_details.transfer_creation_details.smith.account_head_name
            res_data['metal_name'] = queryset.melting_issue_details.transfer_creation_details.metal.metal_name
            res_data['issued_category_name'] = queryset.melting_issue_details.issued_category.category_name
            res_data['issued_date'] = queryset.melting_issue_details.issued_date
            res_data['return_date'] = queryset.melting_issue_details.return_date
            res_data['bullion_rate'] = queryset.melting_issue_details.bullion_rate
            res_data['issued_stone_weight'] = queryset.melting_issue_details.stone_weight
            res_data['issued_gross_weight'] = queryset.melting_issue_details.gross_weight
            res_data['issued_net_weight'] = queryset.melting_issue_details.net_weight
            res_data['notes'] = queryset.melting_issue_details.notes
            
            return Response(
                {
                    "data":res_data,
                    "message":res_msg.retrieve("Melting Recipt"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
            
        except MeltingRecipt.DoesNotExist:
            
            return Response(
                {
                    "message":res_msg.not_exists("Melting Recipt"),
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
            
            
    def update(self,request,pk):
        
        try:
            
            queryset = MeltingRecipt.objects.get(id=pk)
            
            request_data = request.data

            vendor_queryset = MeltingIssue.objects.get(id = queryset.melting_issue_details)
        
            request_data['vendor_details'] = vendor_queryset.vendor_details.pk
            
            melting_charges = queryset.melting_charges
            amount_paid = float(request_data.get('amount_paid'))
        
            if amount_paid == 0:
                request_data['payment_status'] = settings.PAYMENT_PENDING
            elif 0 < amount_paid < melting_charges :
                request_data['payment_status'] = settings.PARTIALLY_PAID
            elif amount_paid == melting_charges :
                request_data['payment_status'] = settings.PAID
            elif amount_paid > melting_charges :
            
                return Response(
                    {
                        "message":"The Paid Amount is more than Melting Charges",
                        "status":status.HTTP_204_NO_CONTENT
                    },status=status.HTTP_200_OK
                )
                
            serializer = MeltingReciptSerializer(queryset,data=request_data,partial=True)
            
            if serializer.is_valid():
                serializer.save()
                
                return Response(
                    {
                        "data":serializer.data,
                        "message":res_msg.update("Melting Recipt"),
                        "status":status.HTTP_200_OK
                    },status=status.HTTP_200_OK
                )
                
            else:
                
                return Response(
                    {
                        "data":serializer.errors,
                        "message":res_msg.not_update("Melting Recipt"),
                        "status":status.HTTP_400_BAD_REQUEST
                    },status=status.HTTP_200_OK
                )
                
        except MeltingRecipt.DoesNotExist:
            
            return Response(
                {
                    "message":res_msg.not_exists("Melting Recipt"),
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
            
            queryset = MeltingRecipt.objects.get(id=pk)
            
            if queryset.is_cancelled == True:
                
                return Response(
                    {
                        "data" : "Melting Receipt Already Cancelled",
                        "message":"Melting Receipt Already Cancelled",
                        "stauts":status.HTTP_200_OK
                    },status=status.HTTP_200_OK
                )
            
            melting_issue_queryset = MeltingIssue.objects.get(id=queryset.melting_issue_details.pk)

            if melting_issue_queryset.is_received == True:
                
                return Response(
                    {
                        "data" : "Melting Received Already, So didn't Cancelled the Receipt",
                        "message":"Melting Received Already, So didn't Cancelled the Receipt",
                        "stauts":status.HTTP_200_OK
                    },status=status.HTTP_200_OK
                )
            
            
            melting_issue_queryset.is_cancelled == True
                
            melting_issue_queryset.save()
           
            try:
                
                ledger_queryset = VendorLedger.objects.get(vendor_details=queryset.vendor_details.pk,refference_number=queryset.melting_recipt_id,transaction_type=settings.MELTING_VENDOR_LEDGER)
                
                ledger_queryset.is_canceled = True
                
                ledger_queryset.save()
                
            except VendorLedger.DoesNotExist:
                
                transaction.set_rollback(True)
                return Response(
                    {
                        "message":res_msg.not_exists("Ledger Details"),
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
                
            queryset.is_cancelled = True
            queryset.save()

            return Response(
                {
                    "message":res_msg.delete("Melting Recipt"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
            
        except MeltingRecipt.DoesNotExist:
            
            return Response(
                {
                    "message":res_msg.not_exists("Melting Recipt"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
            
        except ProtectedError:
            
            return Response(
                {
                    "message":res_msg.related_item("Please Delete"),
                    "status":status.HTTP_400_BAD_REQUEST
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
class MeltingReciptListView(APIView):
    
    def get(self,request):
        
        if request.user.role.is_admin == False:
            
            queryset = list(MeltingRecipt.objects.filter(branch=request.user.branch.pk).order_by('id'))
            
        else:
            queryset = list(MeltingRecipt.objects.all().order_by('id'))
            
        response_data = []

        for data in queryset :
            
            res_data = {}
            res_data['id']=data.pk
            res_data['melting_recipt_id']=data.melting_recipt_id
            res_data['transfer_creation']=data.melting_issue_details.transfer_creation_details.pk
            res_data['bag_number']=data.melting_issue_details.transfer_creation_details.refference_number
            res_data['bag_weight']=data.melting_issue_details.transfer_creation_details.total_net_weight
            res_data['recipt_net_weight']=data.recipt_net_weight
            
            response_data.append(res_data)
            
        return Response(
            {
                "data":{
                    "list":response_data
                },
                "message":res_msg.retrieve("Melting Recipt"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
        
    def post(self,request):
        
        request_data = request.data
        
        search = request_data.get('search') if request_data.get('search') else ''
        from_date = request_data.get('from_date') if request_data.get('from_date') else None
        to_date = request_data.get('to_date') if request_data.get('to_date') else None
        payment_status = request_data.get('payment_status') if request_data.get('payment_status') else None
        branch = request_data.get('branch') if request_data.get('branch') else None
        page = request.data.get('page') if request.data.get('page') else None
        items_per_page = request.data.get('items_per_page') if request.data.get('items_per_page') else None
        
        filter_condition = {}
        
        if request.user.role.is_admin == False:
            filter_condition['branch'] = request.user.branch.pk
        else:
            if branch != None:
                filter_condition['branch'] = branch
                
        if payment_status != None: 
            filter_condition['payment_status'] = payment_status
            
        if from_date != None and to_date != None: 
            date_range = (from_date,to_date)
            filter_condition['received_date__range'] = date_range
            
        if len(filter_condition) != 0:
            
            queryset = MeltingRecipt.objects.filter(Q(melting_recipt_id__icontains=search)|Q(melting_issue_details__melting_issue_id__icontains=search),**filter_condition).order_by('id')
            
        else:
            queryset = MeltingRecipt.objects.filter(Q(melting_recipt_id__icontains=search)|Q(melting_issue_details__melting_issue_id__icontains=search)).order_by('id')
            
        
        if items_per_page != None:
            paginated_data = Paginator(queryset, items_per_page)
            serializer = MeltingReciptSerializer(paginated_data.get_page(page), many=True)
            total_pages = paginated_data.num_pages
            current_page=page
            
        else:
            serializer = MeltingReciptSerializer(queryset, many=True)
            total_pages=1
            current_page=1
            
        response_data=[]
        
        for i in serializer.data:
            
            res_data=i
            
            details_queryset = MeltingRecipt.objects.get(id=i['id'])
            
            res_data['bag_number'] = details_queryset.melting_issue_details.transfer_creation_details.refference_number
            res_data['melting_issue_id'] = details_queryset.melting_issue_details.melting_issue_id
            res_data['issued_net_weight'] = details_queryset.melting_issue_details.net_weight
            res_data['melting_status_name'] = details_queryset.melting_status.status_name
            res_data['melting_status_color'] = details_queryset.melting_status.color
            
            res_data['branch_name'] = details_queryset.branch.branch_name
            res_data['received_category_name'] = details_queryset.received_category.category_name
            res_data['payment_status_name'] = details_queryset.payment_status.status_name
            res_data['payment_status_color'] = details_queryset.payment_status.color
            
            try:
                staff = Staff.objects.get(user = details_queryset.received_by.pk)
                username = staff.first_name

            except:
                username = '-'
                
            res_data['received_by_name'] = username
            
            response_data.append(res_data)
            
        return Response(
            {
                "data":{
                    "list":response_data,
                    "total_pages": total_pages,
                    "current_page": current_page,
                    "total_items": len(queryset),
                    "current_items": len(serializer.data)
                },
                "message":res_msg.retrieve("Melting Recipt"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class PurificationIssueNumberView(APIView):
    def get(self, request):  
        try:
            
            user_id = request.user.id
            user_instance = User.object.get(id=user_id)
            try:
                purification_issue_number = PurificationIssueNumber.objects.get(user=user_instance)
                return Response(
                    {
                        "data": purification_issue_number.purification_issue_number,
                        "message": "Purification Issue Number found",
                        "status": status.HTTP_200_OK
                    },
                    status=status.HTTP_200_OK
                )
            except PurificationIssueNumber.DoesNotExist:
                next_purification_issue_number = self.generatepurificationissuenumber()
                
                PurificationIssueNumber.objects.create(user=user_instance, purification_issue_number=next_purification_issue_number)

                return Response(
                    {
                        "data": next_purification_issue_number,
                        "message": "New Purification Issue Number generated",
                        "status": status.HTTP_200_OK
                    },
                    status=status.HTTP_200_OK
                )

        except Exception as err:
            return Response(
                {
                    "data": str(err),
                    "message": res_msg.something_else(),
                    "status": status.HTTP_204_NO_CONTENT
                },
                status=status.HTTP_200_OK
            )
            
        
    def generatepurificationissuenumber(self):
        try:
            purification_issue_queryset = PurificationIssueID.objects.all().order_by('-id').first()
            
            if purification_issue_queryset:
                number = int(purification_issue_queryset.pk) + 1
            else:
                number = 1
            prefix = 'PUR-ISSUE-00'
            purification_issue_number = f'{prefix}{number}'
            ppurification_issue_number = PurificationIssueID.objects.create(purification_issue_id=purification_issue_number)
            return purification_issue_number
        except Exception as err:
            ppurification_issue_number = PurificationIssueID.objects.create(purification_issue_id='PUR-ISSUE-001')
            return 'PUR-ISSUE-001'
        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class PurificationIssueView(viewsets.ViewSet):
    
    def create(self,request):
        
        request_data = request.data
        
        if request.user.role.is_admin == False:
            
            request_data['branch'] = request.user.branch.pk
            
        
        request_data['issued_by'] = request.user.id
        request_data['issued_at'] = timezone.now()
        
        request_data['purification_status'] = settings.PURIFICATION_ISSUED
        
        serializer = PurificationIssueSerializer(data=request_data)
        
        if serializer.is_valid():
            serializer.save()
            
            purification_issue_number = PurificationIssueNumber.objects.get(user = request.user.pk)
            purification_issue_number.delete()
            
            
            return Response(
                {
                    "data":serializer.data,
                    "message":res_msg.create("Purification Issue"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
            
        else:
            
            return Response(
                {
                    "data":serializer.errors,
                    "message":res_msg.not_create("Melting Issue"),
                    "status":status.HTTP_400_BAD_REQUEST
                },status=status.HTTP_200_OK
            )
            
    def retrieve(self,request,pk):
        
        try:
            
            queryset = PurificationIssue.objects.get(id=pk)
            
            serializer = PurificationIssueSerializer(queryset)
            
            res_data = serializer.data
            
            res_data['transfer_creation_details'] = queryset.melting_recipt_details.melting_issue_details.transfer_creation_details.pk
            
            
            return Response(
                {
                    "data":res_data,
                    "message":res_msg.retrieve("Purification Issue"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
            
        except PurificationIssue.DoesNotExist:
            
            return Response(
                {
                    "message":res_msg.not_exists("Purification Issue"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
            
    def update(self,request,pk):
        
        try:
            
            queryset = PurificationIssue.objects.get(id=pk)
            
            request_data = request.data
            
            serializer = PurificationIssueSerializer(queryset,data=request_data,partial=True)
            
            if serializer.is_valid():
                serializer.save()
                
                return Response(
                    {
                        "data":serializer.data,
                        "message":res_msg.update("Purification Issue"),
                        "status":status.HTTP_200_OK
                    },status=status.HTTP_200_OK
                )
                
            else:
                
                return Response(
                    {
                        "data":serializer.errors,
                        "message":res_msg.not_update("Purification Issue"),
                        "status":status.HTTP_400_BAD_REQUEST
                    },status=status.HTTP_200_OK
                )
            
        except PurificationIssue.DoesNotExist:
            
            return Response(
                {
                    "message":res_msg.not_exists("Purification Issue"),
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
            
            queryset = PurificationIssue.objects.get(id=pk)
            
            if queryset.is_cancelled == True:
                
                return Response(
                    {
                        "message":"Melting Already Cancelled",
                        "stauts":status.HTTP_204_NO_CONTENT
                    },status=status.HTTP_200_OK
                )
            
            if queryset.is_received == True:
                    
                return Response(
                    {
                        "message":"Purification Already Received",
                        "stauts":status.HTTP_204_NO_CONTENT
                    },status=status.HTTP_200_OK
                )
                
            queryset.is_cancelled = True
            queryset.save()
           
            return Response(
                {
                    "message":res_msg.delete("Purification Issue"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
            
        except PurificationIssue.DoesNotExist:
            
            return Response(
                {
                    "message":res_msg.not_exists("Purification issue"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
            
        except ProtectedError:
            
            return Response(
                {
                    "message":res_msg.related_item("Please Delete"),
                    "status":status.HTTP_204_NO_CONTENT
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
class PurificationIssueListView(APIView):
    
    def get(self,request):
        
        if request.user.role.is_admin == True:
            
            queryset = list(PurificationIssue.objects.all().exclude(purification_status=settings.PURIFICATION_RECEIVED).order_by('id'))
            
        else:
            
            queryset = list(PurificationIssue.objects.filter(branch=request.user.branch.pk).exclude(purification_status=settings.PURIFICATION_RECEIVED).order_by('id'))
            
        response_data = []
        
        for data in queryset:
            
            res_data = {}
            res_data['id'] = data.pk
            res_data['purification_issue_id'] = data.purification_issue_id
            res_data['bag_number'] = data.melting_recipt_details.melting_issue_details.transfer_creation_details.refference_number
            res_data['smith_name'] = data.smith.account_head_name
            res_data['category_name'] = data.issued_category.category_name
            res_data['issued_date'] = data.issued_date
            res_data['return_date'] = data.return_date
            res_data['notes'] = data.notes
            res_data['metal'] = data.metal_details.pk
            res_data['issued_pure_weight'] = data.issued_pure_weight
            res_data['issued_category_name'] = data.issued_category.category_name
            res_data['bag_weight'] = data.bag_weight
            res_data['recipt_metal_weight'] = data.recipt_metal_weight
            
            response_data.append(res_data)
            
            
        return Response(
            {
                "data":{
                    "list":response_data
                },
                "message":res_msg.retrieve("Purification Issue List"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
        
    def post(self,request):
        
        from_date = request.data.get('from_date') if request.data.get('from_date') else None
        to_date = request.data.get('to_date') if request.data.get('to_date') else None
        vendor = request.data.get('vendor') if request.data.get('vendor') else None
        search = request.data.get('search') if request.data.get('search') else ""
        branch = request.data.get('branch') if request.data.get('branch') else None
        page = request.data.get('page') if request.data.get('page') else None
        items_per_page = request.data.get('items_per_page') if request.data.get('items_per_page') else None
        
        filter_condition = {}
        
        if request.user.role.is_admin == False:
            
            filter_condition['branch'] = request.user.branch.pk
            
        else:
            if branch != None:
                filter_condition['branch'] = branch
                
        if from_date != None and to_date != None:
            date_range=(from_date,to_date)
            filter_condition['issued_date__range'] = date_range
            
        if vendor != None:
            filter_condition['smith'] = vendor
            
        
        if len(filter_condition) != 0:
            
            queryset = PurificationIssue.objects.filter(Q(melting_recipt_details__melting_issue_details__transfer_creation_details__refference_number__icontains=search)|Q(purification_issue_id__icontains=search),**filter_condition).order_by('id')
            
        else:
            queryset = PurificationIssue.objects.filter(Q(melting_recipt_details__melting_issue_details__transfer_creation_details__refference_number__icontains=search)|Q(purification_issue_id__icontains=search)).order_by('id')
            
        
        if items_per_page != None:
            paginated_data = Paginator(queryset, items_per_page)
            serializer = PurificationIssueSerializer(paginated_data.get_page(page), many=True)
            total_pages = paginated_data.num_pages
            current_page=page
            
        else:
            serializer = PurificationIssueSerializer(queryset, many=True)
            total_pages=1
            current_page=1
            
        response_data=[]
        
        for i in serializer.data:
            
            res_data=i
            
            details_queryset = PurificationIssue.objects.get(id=i['id'])
            
            res_data['issued_category_name'] = details_queryset.issued_category.category_name
            res_data['bag_number'] = details_queryset.melting_recipt_details.melting_issue_details.transfer_creation_details.refference_number
            res_data['smith_name'] = details_queryset.melting_recipt_details.melting_issue_details.transfer_creation_details.smith.account_head_name
            res_data['purification_status_name'] = details_queryset.purification_status.status_name
            res_data['purification_status_color'] = details_queryset.purification_status.color
            res_data['branch_name'] = details_queryset.branch.branch_name
            res_data['bag_weight'] = details_queryset.melting_recipt_details.melting_issue_details.transfer_creation_details.total_gross_weight
            res_data['melting_net_weight'] = details_queryset.melting_recipt_details.recipt_net_weight
            
            try:
                staff = Staff.objects.get(user = details_queryset.issued_by.pk)
                username = staff.first_name

            except:
                username = '-'
                
            res_data['issued_by_name'] = username
            
            response_data.append(res_data)
            
        return Response(
            {
                "data":{
                    "list":response_data,
                    "total_pages": total_pages,
                    "current_page": current_page,
                    "total_items": len(queryset),
                    "current_items": len(serializer.data)
                },
                "message":res_msg.retrieve("Purification Issue"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class PurificationReciptNumberView(APIView):
    def get(self, request):  
        try:
            
            user_id = request.user.id
            user_instance = User.object.get(id=user_id)
            try:
                purification_recipt_number = PurificationReciptNumber.objects.get(user=user_instance)
                return Response(
                    {
                        "data": purification_recipt_number.purification_recipt_number,
                        "message": "Purification Recipt Number found",
                        "status": status.HTTP_200_OK
                    },
                    status=status.HTTP_200_OK
                )
            except PurificationReciptNumber.DoesNotExist:
                next_purification_recipt_number = self.generatepurificationreciptnumber()
                
                PurificationReciptNumber.objects.create(user=user_instance, purification_recipt_number=next_purification_recipt_number)

                return Response(
                    {
                        "data": next_purification_recipt_number,
                        "message": "New Purification Recipt Number generated",
                        "status": status.HTTP_200_OK
                    },
                    status=status.HTTP_200_OK
                )

        except Exception as err:
            return Response(
                {
                    "data": str(err),
                    "message": res_msg.something_else(),
                    "status": status.HTTP_204_NO_CONTENT
                },
                status=status.HTTP_200_OK
            ) 
            
    def generatepurificationreciptnumber(self):
        try:
            purification_recipt_queryset = PurificationReciptID.objects.all().order_by('-id').first()
            
            if purification_recipt_queryset:
                number = int(purification_recipt_queryset.pk) + 1
            else:
                number = 1
            prefix = 'PUR-RCPT-00'
            purification_recipt_number = f'{prefix}{number}'
            ppurification_recipt_number = PurificationReciptID.objects.create(purification_recipt_id=purification_recipt_number)
            return purification_recipt_number
        except Exception as err:
            ppurification_recipt_number = PurificationReciptID.objects.create(purification_recipt_id='PUR-RCPT-001')
    
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class PurificationReciptView(viewsets.ViewSet):
    
    def create(self,request):
        
        request_data = request.data
        
        if request.user.role.is_admin == False:
            branch = request.user.branch.pk
        else:
            branch = request_data.get('branch')

        request_data['branch'] = branch
        
        vendor_queryset = PurificationIssue.objects.get(id = request_data.get('purification_issue_details'))
        
        request_data['branch'] = branch
        request_data['vendor_details'] = vendor_queryset.smith.pk

        purification_charges = float(request_data.get('purification_charges'))
        amount_paid = float(request_data.get('amount_paid'))
        
        if amount_paid == 0:
            request_data['payment_status'] = settings.PAYMENT_PENDING
        elif 0 < amount_paid < purification_charges :
            request_data['payment_status'] = settings.PARTIALLY_PAID
        elif amount_paid == purification_charges :
            request_data['payment_status'] = settings.PAID
        elif amount_paid > purification_charges :
            
            return Response(
                {
                    "message":"The Paid Amount is more than Purification Charges",
                    "status":status.HTTP_400_BAD_REQUEST
                },status=status.HTTP_200_OK
            )
        
        request_data['received_by'] = request.user.pk
        request_data['received_at'] = timezone.now()
        request_data['purification_status'] = settings.PURIFICATION_RECEIVED
        
        serializer = PurificationReciptSerializer(data=request_data)
        
        if serializer.is_valid():
            serializer.save()

            purification_issue_queryset = PurificationIssue.objects.get(id=request_data['purification_issue_details'])

            purification_issue_queryset.is_received = True
            purification_issue_queryset.save()

            ledger_data = {}
            
            ledger_data['vendor_details'] = vendor_queryset.smith.pk
            ledger_data['transaction_date'] = timezone.now()
            ledger_data['refference_number'] = serializer.data['putification_recipt_id']
            ledger_data['transaction_type'] = settings.PURIFICATION_VENDOR_LEDGER
            ledger_data['transaction_weight'] = 0.0
            ledger_data['transaction_amount'] = serializer.data['purification_charges']
            ledger_data['branch'] = serializer.data['branch']
            
            ledger_serializer = VendorLedgerSerializer(data=ledger_data)
            
            if ledger_serializer.is_valid():
                
                ledger_serializer.save()
                
            else:
                transaction.set_rollback(True)
                return Response(
                    {
                        "data":ledger_serializer.errors,
                        "message":res_msg.not_create("Purification Recipt"),
                        "status":status.HTTP_400_BAD_REQUEST
                    },status=status.HTTP_200_OK
                )
                
            old_leger_data = {}
            
            old_leger_data['vendor_details'] = vendor_queryset.smith.pk
            old_leger_data['entry_date'] = timezone.now()
            old_leger_data['metal_details'] = serializer.data['metal_details']
            old_leger_data['old_ledger_entry_type'] = settings.OLD_IN
            old_leger_data['touch'] = serializer.data['touch']
            old_leger_data['weight'] = serializer.data['received_pure_weight']
            old_leger_data['refference_number'] = serializer.data['putification_recipt_id']
            old_leger_data['branch'] = serializer.data['branch']
            old_leger_data['created_by'] = request.user.id
                
            old_leger_serializer = OldGoldLedgerSerializer(data=old_leger_data)
            
            if old_leger_serializer.is_valid():
                
                old_leger_serializer.save()
                
            else:
                transaction.set_rollback(True)
                return Response(
                    {
                        "data":old_leger_serializer.errors,
                        "message":res_msg.not_create("Purification Recipt"),
                        "status":status.HTTP_400_BAD_REQUEST
                    },status=status.HTTP_200_OK
                )
            
            recipt_number_queryset = PurificationReciptNumber.objects.get(user = request.user.pk)
            recipt_number_queryset.delete()
            
            res_data = serializer.data
            
            status_queryset = StatusTable.objects.get(id=settings.PURIFICATION_RECEIVED)
            
            purification_issue_queryset = PurificationIssue.objects.get(id=res_data['purification_issue_details'])
            
            purification_issue_queryset.purification_status = status_queryset
            
            purification_issue_queryset.save()
            
            return Response(
                {
                    "data":res_data,
                    "message":res_msg.create("Purification Recipt"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
            
        else:
            
            return Response(
                {
                    "data":serializer.errors,
                    "message":res_msg.not_create("Purification Recipt"),
                    "status":status.HTTP_400_BAD_REQUEST
                },status=status.HTTP_200_OK
            )
            
    def retrieve(self,request,pk):
        
        try:
            
            queryset = PurificationRecipt.objects.get(id=pk)
            
            serializer = PurificationReciptSerializer(queryset)
            
            res_data = serializer.data
            
            res_data['purification_issue_id'] = queryset.purification_issue_details.purification_issue_id
            res_data['bag_number'] = queryset.purification_issue_details.melting_recipt_details.melting_issue_details.transfer_creation_details.refference_number
            res_data['smith_name'] = queryset.purification_issue_details.smith.account_head_name
            res_data['category_name'] = queryset.purification_issue_details.issued_category.category_name 
            res_data['melting_bullion_rate'] = queryset.melting_bullion_rate
            res_data['touch'] = queryset.touch
            res_data['issued_date'] = queryset.purification_issue_details.issued_date
            res_data['return_date'] = queryset.purification_issue_details.return_date
            res_data['notes'] = queryset.purification_issue_details.notes
            res_data['received_pure_weight'] = queryset.received_pure_weight
            res_data['issued_category_name'] = queryset.purification_issue_details.issued_category.category_name
            res_data['bag_weight'] = queryset.purification_issue_details.bag_weight
            res_data['recipt_metal_weight'] = queryset.purification_issue_details.recipt_metal_weight
            
            return Response(
                {
                    "data":res_data,
                    "message":res_msg.retrieve("Purification Recipt"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
            
        except PurificationRecipt.DoesNotExist:
            
            return Response(
                {
                    "message":res_msg.not_exists("Purification Recipt"),
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
            
            
    def update(self,request,pk):
        
        try:
            
            queryset = PurificationRecipt.objects.get(id=pk)
            
            request_data = request.data
            
            purification_charges = queryset.purification_charges
            amount_paid = float(request_data.get('amount_paid'))
        
            if amount_paid == 0:
                request_data['payment_status'] = settings.PAYMENT_PENDING
            elif 0 < amount_paid < purification_charges :
                request_data['payment_status'] = settings.PARTIALLY_PAID
            elif amount_paid == purification_charges :
                request_data['payment_status'] = settings.PAID
            elif amount_paid > purification_charges :
            
                return Response(
                    {
                        "message":"The Paid Amount is more than Purification Charges",
                        "status":status.HTTP_400_BAD_REQUEST
                    },status=status.HTTP_200_OK
                )
                
            serializer = PurificationReciptSerializer(queryset,data=request_data,partial=True)
            
            if serializer.is_valid():
                serializer.save()
                
                return Response(
                    {
                        "data":serializer.data,
                        "message":res_msg.update("Purification Recipt"),
                        "status":status.HTTP_200_OK
                    },status=status.HTTP_200_OK
                )
                
            else:
                
                return Response(
                    {
                        "data":serializer.errors,
                        "message":res_msg.not_update("Purification Recipt"),
                        "status":status.HTTP_400_BAD_REQUEST
                    },status=status.HTTP_200_OK
                )
                
        except PurificationRecipt.DoesNotExist:
            
            return Response(
                {
                    "message":res_msg.not_exists("Purification Recipt"),
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
            
            queryset = PurificationRecipt.objects.get(id=pk)
            
            if queryset.is_cancelled == True:
                
                return Response(
                    {
                        "message":"Melting Receipt Already Cancelled",
                        "stauts":status.HTTP_204_NO_CONTENT
                    },status=status.HTTP_200_OK
                )

            melting_issue_queryset = PurificationIssue.objects.get(id=queryset.purification_issue_details.pk)
        
            melting_issue_queryset.is_cancelled == True
                
            melting_issue_queryset.save()
            
            try:
                
                ledger_queryset = VendorLedger.objects.get(vendor_details=queryset.vendor_details.pk,refference_number=queryset.putification_recipt_id,transaction_type=settings.PURIFICATION_VENDOR_LEDGER)
                
                ledger_queryset.is_canceled = True
                
                ledger_queryset.save()
                
            except VendorLedger.DoesNotExist:
                
                transaction.set_rollback(True)
                return Response(
                    {
                        "message":res_msg.not_exists("Ledger Details"),
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
                
            queryset.is_cancelled = True
            queryset.save()
            
            return Response(
                {
                    "message":res_msg.delete("Purification Recipt"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
            
        except MeltingRecipt.DoesNotExist:
            
            return Response(
                {
                    "message":res_msg.not_exists("Purification Recipt"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
            
        except ProtectedError:
            
            return Response(
                {
                    "message":res_msg.related_item("Please Delete"),
                    "status":status.HTTP_400_BAD_REQUEST
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
class PurificationReciptListView(APIView):
    
    def get(self,request):
        
        if request.user.role.is_admin == False:
            
            queryset = list(PurificationRecipt.objects.filter(branch=request.user.branch.pk).values('id','putification_recipt_id').order_by('id'))
            
        else:
            
            queryset = list(PurificationRecipt.objects.all().values('id','putification_recipt_id').order_by('id'))
            
        
        return Response(
            {
                "data":{
                    "list":queryset
                },
                "message":res_msg.retrieve("Purification Recipt"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
        
    def post(self,request):
        
        from_date = request.data.get('from_date') if request.data.get('from_date') else None
        to_date = request.data.get('to_date') if request.data.get('to_date') else None
        vendor = request.data.get('vendor') if request.data.get('vendor') else None
        payment_status = request.data.get('payment_status') if request.data.get('payment_status') else None
        search = request.data.get('search') if request.data.get('search') else ""
        branch = request.data.get('branch') if request.data.get('branch') else None
        page = request.data.get('page') if request.data.get('page') else None
        items_per_page = request.data.get('items_per_page') if request.data.get('items_per_page') else None
        
        filter_condition = {}
        
        if request.user.role.is_admin == False:
            
            filter_condition['branch'] = request.user.branch.pk
            
        else:
            
            if branch != None:
                
                filter_condition['branch'] = branch
                
        if from_date != None and to_date != None:
            
            date_range = (from_date,to_date)
            
            filter_condition['received_date__range'] = date_range
            
        if vendor != None:
            
            filter_condition['purification_issue_details__smith'] = vendor
            
        if payment_status != None:
            
            filter_condition['payment_status'] = payment_status
            
        if len(filter_condition) != 0:
            
            queryset = PurificationRecipt.objects.filter(Q(putification_recipt_id__icontains = search)|Q(purification_issue_details__melting_recipt_details__melting_issue_details__transfer_creation_details__refference_number=search),**filter_condition).order_by('id')
            
        else:
            
            queryset = PurificationRecipt.objects.filter(Q(putification_recipt_id__icontains = search)|Q(purification_issue_details__melting_recipt_details__melting_issue_details__transfer_creation_details__refference_number=search)).order_by('id')
            
        
        if items_per_page != None:
            paginated_data = Paginator(queryset, items_per_page)
            serializer = PurificationReciptSerializer(paginated_data.get_page(page), many=True)
            total_pages = paginated_data.num_pages
            current_page=page
            
        else:
            serializer = PurificationReciptSerializer(queryset, many=True)
            total_pages=1
            current_page=1
            
        response_data=[]
        
        for i in serializer.data:
            
            res_data=i
            
            details_queryset = PurificationRecipt.objects.get(id=i['id'])
            
            res_data['received_category_name'] = details_queryset.received_category.category_name
            res_data['bag_number'] = details_queryset.purification_issue_details.melting_recipt_details.melting_issue_details.transfer_creation_details.refference_number
            res_data['smith_name'] = details_queryset.purification_issue_details.melting_recipt_details.melting_issue_details.transfer_creation_details.smith.account_head_name
            res_data['purification_status_name'] = details_queryset.purification_status.status_name
            res_data['purification_status_color'] = details_queryset.purification_status.color
            res_data['payment_status_name'] = details_queryset.payment_status.status_name
            res_data['payment_status_color'] = details_queryset.payment_status.color
            res_data['branch_name'] = details_queryset.branch.branch_name
            res_data['bag_weight'] = details_queryset.purification_issue_details.melting_recipt_details.melting_issue_details.transfer_creation_details.total_gross_weight
            res_data['melting_net_weight'] = details_queryset.purification_issue_details.melting_recipt_details.recipt_net_weight
            res_data['purification_issue_id'] = details_queryset.purification_issue_details.purification_issue_id
            
            try:
                staff = Staff.objects.get(user = details_queryset.received_by.pk)
                username = staff.first_name

            except:
                username = '-'
                
            res_data['issued_by_name'] = username
            
            response_data.append(res_data)
            
        return Response(
            {
                "data":{
                    "list":response_data,
                    "total_pages": total_pages,
                    "current_page": current_page,
                    "total_items": len(queryset),
                    "current_items": len(serializer.data)
                },
                "message":res_msg.retrieve("Purification Recipt"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
            
        
            
        
            
        
            
            
        
        
            
            
            
        
        
        
        
            
        
                
            
        
        
        
        
        
        
                    
            
            
            
        
            
        
            
        
        
        
        
        

            
        
                
            
        
        
            
            
            
            
            
    
            
    
            
    
            

            
        
        
                
            
        
            
            

            
        