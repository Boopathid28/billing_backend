from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.response import Response
import random
from organizations.models import Staff
from .models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes, authentication_classes
from django.utils import timezone
from django.db.models import ProtectedError
from django.db.models import Q
from django.db import transaction
from django.core.paginator import Paginator
from app_lib.response_messages import ResponseMessages
from .serializer import *
from datetime import datetime
from django.conf import settings
from customer.serializer import CustomerLedgerSerializer
from customer.models import CustomerLedger
from masters.models import MetalRate

res_msg = ResponseMessages()

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class AdvancePurposeView(APIView):
    def get(self,request):

        queryset=list(AdvancePurpose.objects.filter(is_active=True).order_by('id').values('id','purpose_name'))

        return Response(
            {
                "data":{
                    "list":queryset
                },
                "message":res_msg.retrieve("Advance Purpose"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
    

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class AdvancePaymentViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk):

        try:
            queryset = AdvanceDetails.objects.get(id=pk)
       
            serializer = AdvanceDetailsSerializer(queryset)

            res_data = serializer.data
            res_data['customer_name'] = queryset.customer_details.customer_name
                
            if queryset.advance_weight_purity != None:
                res_data['purity_name'] = queryset.advance_weight_purity.purity_name
                
            else:
                res_data['purity_name'] =None

            res_data['advance_purpose_name'] = queryset.advance_purpose.purpose_name

            redeem_amount = 0
            redeem_weight = 0
                
            log_queryset = AdvanceLogs.objects.filter(advance_details=queryset.pk,is_cancelled=False)
            
            for logs in log_queryset:
                
                redeem_amount  += logs.redeem_amount
                redeem_weight  += logs.redeem_weight
                
            remaining_amount = queryset.total_advance_amount - redeem_amount
            remaining_weight = queryset.total_advance_weight - redeem_weight
            
            res_data['redeem_amount'] = redeem_amount
            res_data['redeem_weight'] = redeem_weight
            res_data['remaining_amount'] = remaining_amount
            res_data['remaining_weight'] = remaining_weight
            
            ledger_queryset = CustomerLedger.objects.filter(reffrence_number=queryset.advance_id)
            
            ledger_serializer = CustomerLedgerSerializer(ledger_queryset,many=True)
            
            res_data['ledger_data'] = ledger_serializer.data

            return Response({
                "data": res_data,
                "message": res_msg.retrieve('Advance Details'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        
        except AdvanceDetails.DoesNotExist:
            return Response(
                {
                    "message":res_msg.not_exists("Advance"),
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
    def create(self, request):
        data = request.data

        if request.user.role.is_admin == True:
            if data.get('branch') != None:
                branch = data.get('branch')
            else:
                branch = None
        else:
            branch = request.user.branch.pk

        data['created_at'] = timezone.now()
        data['created_by'] = request.user.id

        serializer = AdvanceDetailsSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            ledger_data = {}
            
            ledger_data['customer_details'] = serializer.data['customer_details']
            ledger_data['entry_date'] = timezone.now()
            ledger_data['entry_type'] = settings.ADVANCE_ENTRY
            ledger_data['transaction_type'] = settings.DEBIT_ENTRY
            ledger_data['invoice_number'] = None
            ledger_data['reffrence_number'] = serializer.data['advance_id']
            ledger_data['transaction_amount'] = serializer.data['total_advance_amount']
            ledger_data['transaction_weight'] = serializer.data['total_advance_weight']
            ledger_data['branch'] = branch
            
            ledger_serializer = CustomerLedgerSerializer(data=ledger_data)
            
            if ledger_serializer.is_valid():
                ledger_serializer.save()
                
            else:
                transaction.set_rollback(True)
                return Response(
                    {
                        "data":ledger_serializer.errors,
                        "message":res_msg.not_create('Advance'),
                        "status":status.HTTP_400_BAD_REQUEST
                    },status=status.HTTP_200_OK
                )
         
            return Response({
                "data": serializer.data,
                "message": res_msg.create('Advance Details'),
                "status": status.HTTP_201_CREATED
            }, status=status.HTTP_200_OK)
        
        else:
            return Response({
                "data": serializer.errors,
                "message": res_msg.in_valid_fields(),
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_200_OK)

        
    def update(self, request, pk):
        try:
            queryset = AdvanceDetails.objects.get(id=pk)
        except Exception as err:
            return Response({
                "message": res_msg.not_exists('Advance Details'),
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_200_OK)
        
        data = request.data

        if request.user.role.is_admin == False :
            branch = request.user.branch.pk
        else:
            if data.get('branch') != None:
                branch = data.get('branch')
            else:
                branch = None

        data['modified_at'] = timezone.now()
        data['modified_by'] = request.user.id
        serializer = AdvanceDetailsSerializer(queryset, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": res_msg.update('Advance Payment Details'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        
        return Response({
                "data": serializer.errors,
                "message": res_msg.in_valid_fields(),
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_200_OK)
    

    def destroy(self, request, pk):
        try:
           
            queryset = AdvanceDetails.objects.get(id=pk)

            if queryset.is_cancelled == True:
                return Response({
                   "message":"Advance is Already Cancelled",
                    "status":status.HTTP_204_NO_CONTENT
                }, status=status.HTTP_200_OK)
            
            advance_log_queryset = AdvanceLogs.objects.filter(advance_details=queryset.pk)

            if len(advance_log_queryset) != 0:
                return Response(
                    {
                        "message":"Cannot Cancel After Redeem",
                        "status":status.HTTP_204_NO_CONTENT
                    },status=status.HTTP_200_OK
                )
            
            try:
                
                ledger_queryset = CustomerLedger.objects.get(customer_details=queryset.customer_details,entry_type=settings.ADVANCE_ENTRY,transaction_type=settings.DEBIT_ENTRY,reffrence_number=queryset.advance_id,is_cancelled=False)
                
                ledger_queryset.is_cancelled = True
                
                ledger_queryset.save()
                
            except CustomerLedger.DoesNotExist:
                pass
                
            except Exception as err:
                transaction.set_rollback(True)
                return Response(
                    {
                        "data":str(err),
                        "message":res_msg.something_else(),
                        "status":status.HTTP_204_NO_CONTENT
                    },status=status.HTTP_200_OK
                )
                
            log_queryset = AdvanceLogs.objects.filter(advance_details=queryset.pk,is_cancelled=False)
            
            for logs in log_queryset:
                
                logs.is_cancelled = True
                
                logs.save()
            
            queryset.is_cancelled = True
            
            queryset.save()
            
            return Response(
                {
                    "message":"Advance Cancelled Sucessfully",
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
            
        except AdvanceDetails.DoesNotExist:
            
            return Response(
                {
                    "message":res_msg.not_exists("Advance"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
            
        except Exception as err:
            transaction.set_rollback(True)
            return Response(
                {
                    "data":str(err),
                    "message":res_msg.something_else(),
                    "stauts":status.HTTP_204_NO_CONTENT
                },status=status.HTTP_200_OK
            )
        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class AdvancePaymentList(APIView):

    def get(self, request,branch=None):

        if request.user.role.is_admin == False :
            branch = None
        else:
            branch = request.user.branch.pk

        if branch == None : 
            queryset = list(AdvanceDetails.objects.all().order_by('id'))
        else:
            queryset = list(AdvanceDetails.objects.filter(branch=branch).order_by('id'))

        serializer = AdvanceDetailsSerializer(queryset, many=True)

        return Response({
            "data": {
                "list": serializer.data,
            },
            "message": res_msg.retrieve('Advance Payment Details'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
    

    def post(self, request):

        if request.user.role.is_admin == False :
            branch = request.user.branch.pk
        else:
            branch = None

        search = request.data.get('search') if request.data.get('search') else ''
        from_date = request.data.get('from_date') if request.data.get('from_date') else None
        to_date = request.data.get('to_date') if request.data.get('to_date') else None
        cancel_status = request.data.get('cancel_status') if request.data.get('cancel_status') else None
        redeem_status = request.data.get('redeem_status') if request.data.get('redeem_status') else None
        customer_details = request.data.get('customer_details') if request.data.get('customer_details') else None
        branch = request.data.get('branch') if request.data.get('branch') else None
        page = request.data.get('page') if request.data.get('page') else 1
        try:
            items_per_page = int(request.data.get('items_per_page', AdvanceDetails.objects.all().count()))
            if items_per_page == 0:
                items_per_page = 10 
        except Exception as err:
            items_per_page = 10 
        
        filter_condition={}

        if branch != None :
            filter_condition['branch'] = branch

        if customer_details != None :
            filter_condition['customer_details'] = customer_details
    
        if cancel_status != None:
           filter_condition['is_cancelled'] = cancel_status 

        if redeem_status != None:
           filter_condition['is_redeemed'] = redeem_status 

        if from_date != None and to_date!= None:
           fdate =from_date
           tdate =to_date
           date_range=(fdate,tdate)
           filter_condition['created_at__range']=date_range

        if len(filter_condition) != 0:
                queryset = list(AdvanceDetails.objects.filter(Q(customer_details__customer_name__icontains=search) | Q(advance_purpose__purpose_name__icontains=search),**filter_condition).order_by('id'))
        elif search != '':
                queryset = list(AdvanceDetails.objects.filter(Q(customer_details__customer_name__icontains=search) | Q(advance_purpose__purpose_name__icontains=search)).order_by('id'))
        else:
            queryset = list(AdvanceDetails.objects.all().order_by('id'))

        paginated_data = Paginator(queryset, items_per_page)
        serializer = AdvanceDetailsSerializer(paginated_data.get_page(page), many=True)

        res_data = []
        
        for i in range(len(serializer.data)):
            try :
                staff = Staff.objects.get(user =queryset[i].created_by)
                username = staff.first_name
            except:
                username = "-"   

            dict_data = serializer.data[i]
            dict_data['customer_name'] = queryset[i].customer_details.customer_name
            dict_data['advance_purpose_name'] = queryset[i].advance_purpose.purpose_name
            if queryset[i].advance_weight_purity != None:
                dict_data['advance_purity_name'] = queryset[i].advance_weight_purity.purity_name
            else:
                dict_data['advance_purity_name'] = "---"
            dict_data['created_by'] = username
            dict_data['branch_name'] = queryset[i].branch.branch_name
            res_data.append(dict_data)

        return Response({
            "data": {
                "list": res_data,
                "total_pages": paginated_data.num_pages,
                "current_page": page,
                "total_items": len(queryset),
                "current_items": len(serializer.data)
            },
            "message": res_msg.retrieve('Advance Payment Details'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class AdvanceNumberAutoGenerate(APIView):
    def get(self,request):
        prefix = 'ADV'  
        random_number = random.randint(100, 9999999)  
        advance_number = f'{prefix}-{random_number}'

        return Response(
            {
                "data": advance_number,
                "message" : res_msg.create("Advance Number"),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK
        )  
    

# ADVANCE NUMBER DETAILS FETCH
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class AdvanceSearchView(APIView):
    
    def get(self,request,pk):
        try:
            
            queryset = AdvanceDetails.objects.get(advance_id=pk)
            
            if queryset.is_redeemed == True:
                return Response(
                    {
                        "message":"Advance is already used",
                        "status":status.HTTP_204_NO_CONTENT
                    },status=status.HTTP_200_OK
                )
                
            if queryset.is_cancelled == True:
                return Response(
                    {
                        "message":"Advance is cancelled",
                        "status":status.HTTP_204_NO_CONTENT
                    },status=status.HTTP_200_OK
                )
            
            serializer = AdvanceDetailsSerializer(queryset)
            
            res_data = serializer.data
            
            res_data['customer_details_name'] = queryset.customer_details.customer_name
            
            if queryset.advance_weight_purity != None:
                
                res_data['purity_name'] = queryset.advance_weight_purity.purity_name
                
                try:
                    
                    metal_rate_queryset = MetalRate.objects.filter(purity=queryset.advance_weight_purity.pk).last()
                    
                    if metal_rate_queryset != None:
                    
                        res_data['metal_rate'] = metal_rate_queryset.rate
                        
                    else:
                        
                        res_data['metal_rate'] = 0
                        
                except MetalRate.DoesNotExist:
                    
                    res_data['metal_rate'] = 0
                    
                except Exception as err:
                    
                    res_data['metal_rate'] = 0
                
            else:
                
                res_data['purity_name'] =None
                
            redeem_amount = 0
            redeem_weight = 0
                
            log_queryset = AdvanceLogs.objects.filter(advance_details=queryset.pk,is_cancelled=False)
            
            for logs in log_queryset:
                
                redeem_amount  += logs.redeem_amount
                redeem_weight  += logs.redeem_weight
                
            remaining_amount = queryset.total_advance_amount - redeem_amount
            remaining_weight = queryset.total_advance_weight - redeem_weight
            
            res_data['redeem_amount'] = redeem_amount
            res_data['redeem_weight'] = redeem_weight
            res_data['remaining_amount'] = remaining_amount
            res_data['remaining_weight'] = remaining_weight
            
            return Response(
                {
                    "data":res_data,
                    "message":res_msg.retrieve("Advance"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
            
        except AdvanceDetails.DoesNotExist:
            return Response(
                {
                    "message":res_msg.not_exists("Advance"),
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
    