import random
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
from customer.serializer import CustomerLedgerSerializer
from customer.models import CustomerLedger

res_msg = ResponseMessages()


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class SuspenseNumberView(APIView):
    def get(self,request):
            
        random_number = random.randint(100, 9999999)
        
        generated_number = "SUS"+str(random_number)
        
        suspense_id = generated_number

        return Response(
            {
                "data":suspense_id,
                "message":res_msg.create("Suspense Number"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
            

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class SuspenseView(viewsets.ViewSet):

    @transaction.atomic()
    def create(self,request):

        request_data = request.data
        
        if request.user.role.is_admin == True:
            if request_data.get('branch') != None:            
                branch = request_data.get('branch')
        else:
            branch = request.user.branch_id
        
        request_data['branch'] = branch
        serializer = SuspenseDetailsSerializer(data=request_data)
        
        if serializer.is_valid():
            
            serializer.save()
            
            item_details = request.data.get('item_details',[])
            
            total_amount = 0
            
            for item in item_details:
                
                item['suspense_details'] = serializer.data['id']
                
                item_serializer = SuspenseItemDetailsSerializer(data=item)
                
                if item_serializer.is_valid():
                    
                    item_serializer.save()
                    
                    total_amount += item_serializer.data['total_amount']
                    
                else:
                    transaction.set_rollback(True)
                    return Response(
                        {
                            "data":item_serializer.errors,
                            "message":res_msg.not_create("Suspense"),
                            "status":status.HTTP_400_BAD_REQUEST
                        },status=status.HTTP_200_OK
                    )
                    
            ledger_data = {}
            
            ledger_data['customer_details'] = serializer.data['customer_details']
            ledger_data['entry_date'] = timezone.now()
            ledger_data['entry_type'] = settings.SUSPENSE_ENTRY
            ledger_data['transaction_type'] = settings.DEBIT_ENTRY
            ledger_data['invoice_number'] = None
            ledger_data['reffrence_number'] = serializer.data['suspense_id']
            ledger_data['transaction_amount'] = total_amount
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
                        "message":res_msg.not_create("Suspense"),
                        "status":status.HTTP_400_BAD_REQUEST
                    },status=status.HTTP_200_OK
                )
            
            ledger_repayment_data = {}
            
            ledger_repayment_data['customer_details'] = serializer.data['customer_details']
            ledger_repayment_data['entry_date'] = timezone.now()
            ledger_repayment_data['entry_type'] = settings.SUSPENSE_REPAYMENT_ENTRY
            ledger_repayment_data['transaction_type'] = settings.CREDIT_ENTRY
            ledger_repayment_data['invoice_number'] = None
            ledger_repayment_data['reffrence_number'] = serializer.data['suspense_id']
            ledger_repayment_data['transaction_amount'] = total_amount
            ledger_repayment_data['transaction_weight'] = 0.0
            ledger_repayment_data['branch'] = branch
                    
            ledger_repayment_serializer = CustomerLedgerSerializer(data=ledger_repayment_data)
            
            if ledger_repayment_serializer.is_valid():
                
                ledger_repayment_serializer.save()
                
            else:
                transaction.set_rollback(True)
                return Response(
                    {
                        "data":ledger_repayment_serializer.errors,
                        "message":res_msg.not_create("Suspense"),
                        "status":status.HTTP_400_BAD_REQUEST
                    },status=status.HTTP_200_OK
                )    
            return Response(
                {
                    "data":serializer.data,
                    "message":res_msg.create("Suspense"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
            
        else:
            return Response(
                {
                    "data":serializer.errors,
                    "message":res_msg.not_create("Suspense"),
                    "stauts":status.HTTP_400_BAD_REQUEST
                },status=status.HTTP_200_OK
            )
            
    def retrieve(self,request,pk):
        
        try:
            
            if pk == None:
                return Response(
                    {
                        "message":res_msg.missing_fields("ID"),
                        "status":status.HTTP_204_NO_CONTENT
                    },status=status.HTTP_200_OK
                )
                
            queryset = SuspenseDetails.objects.get(id=pk)
            
            serializer = SuspenseDetailsSerializer(queryset)
            
            res_data = serializer.data 
            
            res_data['customer_details_name'] = queryset.customer_details.customer_name
            
            item_details = []
            
            item_queryset = SuspenseItemDetails.objects.filter(suspense_details=queryset.pk)
            
            total_amount = 0.0
            total_weight = 0.0
            
            for item in item_queryset:
                
                item_serializer = SuspenseItemDetailsSerializer(item)
                
                item_data = item_serializer.data
                
                total_amount += item.total_amount
                total_weight += item.metal_weight
                
                item_data['metal_details_name'] = item.metal_details.metal_name
                
                item_details.append(item_data)
                
            res_data['suspense_amount'] = total_amount
            res_data['suspense_weight'] = total_weight
            res_data['item_details'] = item_details
            
            payment_details = []
            
            payment_queryset = SuspensePaymentDetails.objects.filter(suspense_details=queryset.pk)
            
            paid_amount = 0.0
            
            for payment in payment_queryset:
                
                payment_serializer = SuspensePaymentDetailsSerializer(payment)
                
                payment_data = payment_serializer.data
                
                total_paid_amount = 0.0
                
                denomination_queryset = SuspensePaymentDenominations.objects.filter(payment_details=payment.pk)
                
                for denomination in denomination_queryset:
                    
                    total_paid_amount += denomination.paid_amount
                    
                payment_data['paid_amount'] = total_paid_amount
                
                paid_amount += total_paid_amount
                
                payment_details.append(payment_data)
                
            res_data['total_paid_amount'] = paid_amount
            res_data['payment_details'] = payment_details
            res_data['remaining_amount'] = total_amount - paid_amount
            
            return Response(
                {
                    "data":res_data,
                    "message":res_msg.retrieve("Suspense Details"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
            
        except SuspenseDetails.DoesNotExist:
            return Response(
                {
                    "message":res_msg.not_exists('Suspense'),
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
            
            if pk == None:
                
                return Response(
                    {
                        "message":res_msg.missing_fields("ID"),
                        "status":status.HTTP_204_NO_CONTENT
                    },status=status.HTTP_200_OK
                )
                
            queryset = SuspenseDetails.objects.get(id=pk)
            
            if queryset.is_cancelled == True:
                return Response(
                    {
                        "message":"The Suspense is already cancelled",
                        "stauts":status.HTTP_204_NO_CONTENT
                    },status=status.HTTP_200_OK
                )
                
            if queryset.is_redeemed == True:
                return Response(
                    {
                        "message":"Cannot cancel the suspense after redeem",
                        "status":status.HTTP_204_NO_CONTENT
                    },status=status.HTTP_200_OK
                )
                
            payment_queryset = SuspensePaymentDetails.objects.filter(suspense_details=queryset.pk)
            
            if len(payment_queryset) != 0:
                
                return Response(
                    {
                        "message":"Cannot Cancel the suspense after receiving payment",
                        "status":status.HTTP_204_NO_CONTENT
                    },status=status.HTTP_200_OK
                )
                
            leger_queryset = CustomerLedger.objects.get(customer_details=queryset.customer_details.pk,entry_type=settings.SUSPENSE_ENTRY,transaction_type=settings.CREDIT_ENTRY,reffrence_number=queryset.suspense_id,is_cancelled=False)
            
            leger_queryset.is_cancelled = True
            
            leger_queryset.save()
            
            queryset.is_cancelled = True
            
            queryset.save()
            
            
            return Response(
                {
                    "message":"Suspense Cancelled Sucessfully",
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
            
        except SuspenseDetails.DoesNotExist:
            
            return Response(
                {
                    "message":res_msg.not_exists("Suspense Details"),
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
        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class SuspensePaymentIdGenerateView(APIView):
    def get(self, request):
         
        random_number = random.randint(100, 9999999)
                
        generated_number = "SUSPMT"+str(random_number)
        
        try:
            supense_number_queryset = SuspensePaymentDetails.objects.get(payment_id=generated_number)
            return Response(
                {
                    "data":"Payment ID Already Exists",
                    "message":res_msg.something_else(),
                    "status":status.HTTP_204_NO_CONTENT
                },status=status.HTTP_200_OK
            )
        
        except SuspensePaymentDetails.DoesNotExist:
            payment_id = generated_number
            return Response(
                {
                    "data":payment_id,
                    "message":res_msg.something_else(),
                    "status":status.HTTP_204_NO_CONTENT
                },status=status.HTTP_200_OK
            )
            
        except Exception  as err:
            return Response(
                {
                    "data":str(err),
                    "message":res_msg.something_else(),
                    "status":status.HTTP_204_NO_CONTENT
                },status=status.HTTP_200_OK
            )
            
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class SuspensePaymentView(APIView):
    
    @transaction.atomic
    def post(self,request):
        
        try:
            
            pk = request.data.get('id',None)
            
            if pk == None:
                
                return Response(
                    {
                        "message":res_msg.missing_fields("Id"),
                        "status":status.HTTP_204_NO_CONTENT
                    },status=status.HTTP_200_OK
                )
                
            request_data = request.data
            
            if request.user.role.is_admin == False:
                branch = request.user.branch.pk
            else:
                branch = request_data.get('branch')
        
            request_data['branch'] = branch
            request_data['payment_date'] = timezone.now()
            request_data['created_by'] = request.user.id

            suspense_queryset = SuspenseDetails.objects.get(id=pk)
            
            request_data['suspense_details'] = suspense_queryset.pk

            pmt_id = True
        
            while pmt_id ==True:
                
                random_number = random.randint(100, 9999999)
                
                generated_number = "SUSPMT"+str(random_number)
                
                try:
                    supense_number_queryset = SuspensePaymentDetails.objects.get(payment_id=generated_number)
                    pmt_id = True
                except SuspensePaymentDetails.DoesNotExist:
                    request_data['payment_id'] = generated_number
                    pmt_id=False
                    
                except Exception  as err:
                    return Response(
                        {
                            "data":str(err),
                            "message":res_msg.something_else(),
                            "status":status.HTTP_204_NO_CONTENT
                        },status=status.HTTP_200_OK
                    )
           
            serializer = SuspensePaymentDetailsSerializer(data=request_data)
            
            if serializer.is_valid():
                
                serializer.save()
                
                denomination_details = request_data.get('denomination_details',[])
                
                paid_amount = 0.0
                
                for denomination in denomination_details :
                    
                    denomination['payment_details'] = serializer.data['id']
                    
                    denomination_serializer = SuspensePaymentDenominationsSerializer(data=denomination)
                    
                    if denomination_serializer.is_valid():
                        
                        denomination_serializer.save()
                        
                        paid_amount += denomination_serializer.data['paid_amount']
                        
                    else:
                        
                        transaction.set_rollback(True)
                        
                        return Response(
                            {
                                "data":denomination_serializer.errors,
                                "message":res_msg.not_create("Suspense Payment"),
                                "status":status.HTTP_400_BAD_REQUEST
                            },status=status.HTTP_200_OK
                        )
                        
                ledger_data = {}
                
                ledger_data['customer_details'] = suspense_queryset.customer_details.pk
                ledger_data['entry_date'] = timezone.now()
                ledger_data['entry_type'] = settings.SUSPENSE_REPAYMENT_ENTRY
                ledger_data['transaction_type'] = settings.DEBIT_ENTRY
                ledger_data['invoice_number'] = suspense_queryset.suspense_id
                ledger_data['reffrence_number'] = serializer.data['payment_id']
                ledger_data['transaction_amount'] = paid_amount
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
                            "message":res_msg.not_create("Suspense Payment"),
                            "status":status.HTTP_400_BAD_REQUEST
                        },status=status.HTTP_200_OK
                    )
                    
                suspense_payment_queryset = SuspensePaymentDenominations.objects.filter(payment_details__suspense_details=suspense_queryset.pk)
                
                total_paid_amount = 0.0
                
                for payment in suspense_payment_queryset:
                    
                    total_paid_amount += payment.paid_amount
                    
                suspense_item_details = SuspenseItemDetails.objects.filter(suspense_details=suspense_queryset.pk)
                
                total_amount = 0.0
                
                for items in suspense_item_details:
                    
                    total_amount += items.total_amount
                    
                if total_paid_amount == total_amount:
                    
                    suspense_queryset.is_closed = True
                    suspense_queryset.closed_date = timezone.now()
                    suspense_queryset.closed_by = request.user.id
                    suspense_queryset.save()
                    
                if total_paid_amount > total_amount:
                    transaction.set_rollback(True)
                    
                    return Response(
                        {
                            "message":"Paid Amount is greater that total amount",
                            "status":status.HTTP_204_NO_CONTENT
                        },status=status.HTTP_200_OK
                    )
                
                return Response(
                    {
                        "data":serializer.data,
                        "message":res_msg.create("Suspense payment"),
                        "status":status.HTTP_200_OK
                    },status=status.HTTP_200_OK
                )
                
            else:
                
                return Response(
                    {
                        "data":serializer.errors,
                        "message":res_msg.not_create("Suspense Payment"),
                        "status":status.HTTP_400_BAD_REQUEST
                    },status=status.HTTP_200_OK
                )
                    
            
        except SuspenseDetails.DoesNotExist:
            
            return Response(
                {
                    "message":res_msg.not_exists("Suspense"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
            
        except Exception as err:
            
            return Response(
                {
                    "message":res_msg.something_else(),
                    "status":status.HTTP_204_NO_CONTENT
                },status=status.HTTP_200_OK
            )
            
            
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class SuspenseListView(APIView):
    
    def post(self,request):
        
        
        filter_condition = {}
        
        if request.user.role.is_admin == False:
            branch = request.user.branch.pk
        else:
            branch = request.data.get('branch')
                
        customer_details = request.data.get('customer_details',None)
        from_date = request.data.get('from_date',None)
        to_date = request.data.get('to_date',None)
        redeeme_status = request.data.get('redeeme_status',None)
        cancel_status = request.data.get('cancel_status',None)
        search = request.data.get('search',"")
        page = request.data.get('page',1)
        items_per_page = request.data.get('items_per_page',10)
        
        if customer_details != None:
            
            filter_condition['customer_details'] = customer_details
        
        if from_date != None and to_date != None:
            
            date_range = (from_date,to_date)
            
            filter_condition['created_at__range'] = date_range
            
        if redeeme_status != None:
            
            filter_condition['is_redeemed'] = redeeme_status
        
            
        if cancel_status != None:
            
            filter_condition['is_cancelled'] = cancel_status
        
        combined_conditions = Q()
        
        if search != "":
            or_conditions = []
            or_conditions.append(Q(suspense_id__icontains=search))
            or_conditions.append(Q(bill_number__icontains=search))

            for condition in or_conditions:
                combined_conditions |= condition
                
                
        if len(filter_condition) != 0 :
            
            queryset = SuspenseDetails.objects.filter(combined_conditions,**filter_condition).order_by('-id')
            
        else:
            
            queryset = SuspenseDetails.objects.filter(combined_conditions).order_by('-id')
        
        paginated_data = Paginator(queryset, int(items_per_page))
        serializer = SuspenseDetailsSerializer(paginated_data.get_page(int(page)), many=True)
        total_items = len(queryset)
        
        response_data = []
        
        for data in serializer.data:
            
            res_data = data
            
            suspense_queryset = SuspenseDetails.objects.get(id=data['id'])
            
            res_data['customer_details_name'] = suspense_queryset.customer_details.customer_name
            
            total_amount = 0
            
            suspense_item_queryset = SuspenseItemDetails.objects.filter(suspense_details=suspense_queryset.pk)
            
            for item in suspense_item_queryset:
                
                total_amount += item.total_amount
                
            total_payment = 0
            
            suspense_payment_queryset  = SuspensePaymentDenominations.objects.filter(payment_details__suspense_details=suspense_queryset.pk)
            
            for payment in suspense_payment_queryset:
                
                total_payment += payment.paid_amount
                
            res_data['total_amount'] = total_amount
            res_data['total_payment'] = total_payment
            res_data['reamining_amount'] = total_amount-total_payment
            
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
                "message":res_msg.retrieve("Suspense Table List"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class SuspenseNumberSearch(APIView):
    
    def get(self,request,pk):
        
        try:
            
            if pk == None:
                
                return Response(
                    {
                        "message":res_msg.missing_fields("ID"),
                        "status":status.HTTP_204_NO_CONTENT
                    },status=status.HTTP_200_OK
                )
            
            queryset = SuspenseDetails.objects.get(suspense_id=pk)
            
            serializer = SuspenseDetailsSerializer(queryset)
            
            res_data = serializer.data 
            
            res_data['customer_details_name'] = queryset.customer_details.customer_name
            
            item_details = []
            
            item_queryset = SuspenseItemDetails.objects.filter(suspense_details=queryset.pk)
            
            total_amount = 0.0
            total_weight = 0.0
            
            for item in item_queryset:
                
                item_serializer = SuspenseItemDetailsSerializer(item)
                
                item_data = item_serializer.data
                
                total_amount += item.total_amount
                total_weight += item.metal_weight
                
                item_data['metal_details_name'] = item.metal_details.metal_name
                
                item_details.append(item_data)
                
            res_data['suspense_amount'] = total_amount
            res_data['suspense_weight'] = total_weight
            res_data['item_details'] = item_details
            
            payment_details = []
            
            payment_queryset = SuspensePaymentDetails.objects.filter(suspense_details=queryset.pk)
            
            paid_amount = 0.0
            
            for payment in payment_queryset:
                
                payment_serializer = SuspensePaymentDetailsSerializer(payment)
                
                payment_data = payment_serializer.data
                
                total_paid_amount = 0.0
                
                denomination_queryset = SuspensePaymentDenominations.objects.filter(payment_details=payment.pk)
                
                for denomination in denomination_queryset:
                    
                    total_paid_amount += denomination.paid_amount
                    
                payment_data['paid_amount'] = total_paid_amount
                
                paid_amount += total_paid_amount
                
                payment_details.append(payment_data)
                
            res_data['total_paid_amount'] = paid_amount
            res_data['payment_details'] = payment_details
            res_data['remaining_amount'] = total_amount - paid_amount
            
            return Response(
                {
                    "data":res_data,
                    "message":res_msg.retrieve("Suspense Details"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
            
        except SuspenseDetails.DoesNotExist:
            
            return Response(
                {
                    "message":res_msg.not_exists('Suspense'),
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
        
        
            
        