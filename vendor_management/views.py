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
import pandas as pd
from books.models import *

res_msg = ResponseMessages()

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class VendorDiscountView(viewsets.ViewSet):
    @transaction.atomic
    def create(self,request):
        
        data = request.data
        
        dis_id = True
        
        while dis_id ==True:
            
            random_number = random.randint(100, 9999999)
            
            generated_number = "DIS"+str(random_number)
            
            try:
            
                vendor_discount_queryset = VendorDiscount.objects.get(discount_id=generated_number)
                dis_id = True
            except VendorDiscount.DoesNotExist:
                data['discount_id'] = generated_number
                dis_id=False
                
            except Exception  as err:
                
                return Response(
                    {
                        "data":str(err),
                        "message":res_msg.something_else(),
                        "status":status.HTTP_204_NO_CONTENT
                    },status=status.HTTP_200_OK
                )
        
        if request.user.role.is_admin == True:
            branch = request.data.get('branch')
        else:
            branch = request.user.branch.pk
        
        data['discount_date'] = timezone.now()
        data['created_by'] = request.user.id

        if branch != None:
                
            data['branch'] = branch
        
        serializer = VendorDiscountSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            
            ledger_data = {}
            
            ledger_data['vendor_details'] = serializer.data['vendor_details']
            ledger_data['transaction_date'] = serializer.data['discount_date']
            ledger_data['transaction_type'] = settings.DISCOUNT_VENDOR_LEDGER
            ledger_data['refference_number'] = serializer.data['discount_id']
            ledger_data['transaction_weight'] = serializer.data['discount_weight']
            ledger_data['transaction_amount'] = serializer.data['discount_amount']
            ledger_data['branch'] = branch

            ledger_serializer = VendorLedgerSerializer(data=ledger_data)
            
            if ledger_serializer.is_valid():
                ledger_serializer.save()
                
            else:
                transaction.set_rollback(True)
                return Response(
                    {
                        "data":ledger_serializer.errors,
                        "message":res_msg.not_create("Vendor Discount"),
                        "status":status.HTTP_400_BAD_REQUEST
                    },status=status.HTTP_200_OK
                )
                
            return Response(
                {
                    "data":serializer.data,
                    "message":res_msg.create("vendor Discount"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        else:
            return Response(
                    {
                        "data":serializer.errors,
                        "message":res_msg.not_create("Vendor Discount"),
                        "status":status.HTTP_400_BAD_REQUEST
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
                
            queryset = VendorDiscount.objects.get(id=pk)
            
            serializer = VendorDiscountSerializer(queryset)
            
            res_data = serializer.data
            
            res_data['vendor_name'] = queryset.vendor_details.account_head_name
            
            return Response(
                {
                    "data":res_data,
                    "message":res_msg.retrieve("vendor Discount"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
            
        except VendorDiscount.DoesNotExist:
            
            return Response(
                {
                    "message":res_msg.not_exists("Vendor Discount"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
            
        except Exception as err:
            
            return Response(
                {
                    "data":str(err),
                    "message":res_msg.something_else(),
                    "status":status.HTTP_204_NO_CONTENT
                }
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
                
            queryset = VendorDiscount.objects.get(id=pk)
            
            if queryset.is_canceled == True:
                
                return  Response(
                    {
                        "message":"Vendor Discount Already Cancelled",
                        "status":status.HTTP_204_NO_CONTENT
                    },status=status.HTTP_200_OK
                )
            
            queryset.is_canceled = True
            
            queryset.save()
            
            ledger_queryset = VendorLedger.objects.get(vendor_details=queryset.vendor_details.pk,refference_number=queryset.discount_id,transaction_type=settings.DISCOUNT_VENDOR_LEDGER)
            
            ledger_queryset.is_canceled = True
            
            ledger_queryset.save()
            
            return Response(
                {
                    "message":"Vendor Discount Cancelled Sucessfully",
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
            
        except VendorDiscount.DoesNotExist:
            
            return Response(
                {
                    "message":res_msg.not_exists("Vendor Discount"),
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
class VendorDiscountList(APIView):
    
    def post(self,request):
                
        vendor = request.data.get('vendor',None)
        from_date = request.data.get('from_date',None)
        to_date = request.data.get('to_date',None)
        search = request.data.get('search',"")
        cancel_status = request.data.get('status',None)
        page = request.data.get('page') if request.data.get('page') else 1
        items_per_page = request.data.get('items_per_page') if request.data.get('items_per_page') else 10
        
        combined_conditions=Q()
        
        filter_condition = {}
        
        if request.user.role.is_admin == False:
            branch = request.user.branch.pk
        else:
            branch = request.data.get('branch')

        if branch != None:
            
            filter_condition['branch'] = branch
        
        if search != "":
            or_conditions = []
            or_conditions.append(Q(discount_id__icontains=search))

            for condition in or_conditions:
                combined_conditions |= condition
        
        if vendor != None:
            
            filter_condition['vendor_details'] = vendor
            
        if from_date != None and to_date != None:
            
            data_range = (from_date,to_date)
            
            filter_condition['discount_date__range'] =  data_range
            
        if cancel_status != None:

            filter_condition['is_canceled'] = cancel_status

            
        if len(filter_condition) != 0 :
            
            queryset = VendorDiscount.objects.filter(combined_conditions,**filter_condition).order_by('-id')
            
        else:
            
            queryset = VendorDiscount.objects.filter(combined_conditions).order_by('-id')
            
        paginated_data = Paginator(queryset, items_per_page)
        serializer = VendorDiscountSerializer(paginated_data.get_page(page), many=True)
        total_items = len(queryset)
        
        response_data = []
        
        for data in serializer.data:
            
            res_data = data
            
            discount_queryset = VendorDiscount.objects.get(id=data['id'])
            
            res_data['vendor_details_name'] = discount_queryset.vendor_details.account_head_name
            res_data['branch_name'] = discount_queryset.branch.branch_name
            
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
                "message":res_msg.retrieve("Vendor Discount Table List"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
        
        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class VendorPaymentView(viewsets.ViewSet):
    @transaction.atomic
    def create(self,request):
        
        if request.user.role.is_admin == False:
            branch = request.user.branch.pk
        else:
            branch = request.data.get('branch')

        request_data = request.data 
        
        request_data['payment_date'] = timezone.now()
        request_data['created_by'] = request.user.id
        request_data['branch'] = branch
        
        pay_id = True
        
        while pay_id ==True:
            
            random_number = random.randint(100, 9999999)
            
            generated_number = "PMT"+str(random_number)
            
            try:
            
                vendor_payment_queryset = VendorPayment.objects.get(payment_id=generated_number)
                pay_id = True
            except VendorPayment.DoesNotExist:
                request_data['payment_id'] = generated_number
                pay_id=False
                
            except Exception  as err:
                
                return Response(
                    {
                        "data":str(err),
                        "message":res_msg.something_else(),
                        "status":status.HTTP_204_NO_CONTENT
                    },status=status.HTTP_200_OK
                )
                
        serializer = VendorPaymentSerializer(data=request_data) 
        
        if serializer.is_valid():
            
            serializer.save()
            
            payment_details = request_data.get('payment_details',[])
            
            for payment in payment_details:
                
                payment_data = payment
                
                payment_data['payment_details'] = serializer.data['id']
                
                payment_serializer = VendorAmountPaymentDenominationsSerializer(data=payment_data)
                
                if payment_serializer.is_valid():
                    
                    payment_serializer.save()
                    
                else:
                    transaction.set_rollback(True)
                    return Response(
                        {
                            "data":payment_serializer.errors,
                            "message":res_msg.not_create("Vendor Payment"),
                            "status":status.HTTP_400_BAD_REQUEST
                        },status=status.HTTP_200_OK
                    )
                    
            weight_details = request_data.get('weight_details',[])
            
            for weight in weight_details:
                
                weight_data = weight
                
                weight_data['payment_details'] = serializer.data['id']
                
                weight_serializer = VendorWeightPaymentDenominationsSerializer(data=weight_data)
                
                if weight_serializer.is_valid():
                    
                    weight_serializer.save()
                    
                else:
                    transaction.set_rollback(True)
                    return Response(
                        {
                            "data":weight_serializer.errors,
                            "message":res_msg.not_create("Vendor Payment"),
                            "status":status.HTTP_400_BAD_REQUEST
                        },status=status.HTTP_200_OK
                    )
            
            ledger_data = {}
            
            ledger_data['vendor_details'] = serializer.data['vendor_details']
            ledger_data['transaction_date'] = serializer.data['payment_date']
            ledger_data['transaction_type'] = settings.PAYMENT_VENDOR_LEDGER
            ledger_data['refference_number'] = serializer.data['payment_id']
            ledger_data['transaction_weight'] = serializer.data['payment_weight']
            ledger_data['transaction_amount'] = serializer.data['payment_amount']
            ledger_data['branch'] = branch
            
            ledger_serializer = VendorLedgerSerializer(data=ledger_data)
            
            if ledger_serializer.is_valid():
                ledger_serializer.save()
                
            else:
                transaction.set_rollback(True)
                return Response(
                    {
                        "data":ledger_serializer.errors,
                        "message":res_msg.not_create("Vendor Payment"),
                        "status":status.HTTP_400_BAD_REQUEST
                    },status=status.HTTP_200_OK
                )
                
            return Response(
                {
                    "data":serializer.data,
                    "message":res_msg.create("vendor Payment"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
            
        else:
            return Response(
                {
                    "data":serializer.errors,
                    "message":res_msg.not_create("Vendor Payment"),
                    "status":status.HTTP_400_BAD_REQUEST
                },status=status.HTTP_200_OK
            )
            
    def retrieve(self,request,pk):
        
        try:
            
            if pk == None:
                
                return Response(
                    {
                        "data":res_msg.missing_fields("ID"),
                        "status":status.HTTP_204_NO_CONTENT
                    },status=status.HTTP_200_OK
                )
                    
            queryset = VendorPayment.objects.get(id=pk)
            
            serializer = VendorPaymentSerializer(queryset)
            
            res_data = serializer.data
            
            res_data['vendor_details_name'] = queryset.vendor_details.account_head_name
            
            denomination_queryset = VendorAmountPaymentDenominations.objects.filter(payment_details=queryset.pk)
            
            denomination_serializer = VendorAmountPaymentDenominationsSerializer(denomination_queryset,many=True)
            
            res_data['payment_details'] = denomination_serializer.data
            
            weight_queryset = VendorWeightPaymentDenominations.objects.filter(payment_details=queryset.pk)
            
            weight_serializer = VendorWeightPaymentDenominationsSerializer(weight_queryset,many=True)
            
            res_data['weight_details'] = weight_serializer.data
            
            return Response(
                {
                    "data":res_data,
                    "message":res_msg.retrieve("Vendor Payment"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
            
        except VendorPayment.DoesNotExist:
            
            return Response(
                {
                    "message":res_msg.not_exists("Vendor Payment"),
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
                        "data":res_msg.missing_fields("ID"),
                        "status":status.HTTP_204_NO_CONTENT
                    },status=status.HTTP_200_OK
                )
            
            queryset = VendorPayment.objects.get(id=pk)
            
            if queryset.is_canceled == True:
                
                return Response(
                    {
                        "message":"Vendor Payment is already canceled",
                        "status":status.HTTP_204_NO_CONTENT
                    },status=status.HTTP_200_OK
                )
                
            queryset.is_canceled = True
            
            queryset.save()
            
            ledger_queryset = VendorLedger.objects.get(vendor_details=queryset.vendor_details.pk,refference_number=queryset.payment_id,transaction_type=settings.PAYMENT_VENDOR_LEDGER)
            
            ledger_queryset.is_canceled = True
            
            ledger_queryset.save()
            
            return Response(
                {
                    "message":"Vendor Payment Cancelled Sucessfully",
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
            
        except VendorPayment.DoesNotExist:
            
            return Response(
                {
                    "message":res_msg.not_exists("Vendor Payment"),
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
class VendorPaymentListView(APIView):
    
    def post(self,request):
        
        if request.user.role.is_admin == False:
            branch = request.user.branch.pk
        else:
            branch = request.data.get('branch')

        vendor = request.data.get('vendor',None)
        from_date = request.data.get('from_date',None)
        to_date = request.data.get('to_date',None)
        search = request.data.get('search',"")
        cancel_status = request.data.get('status',None)
        page = request.data.get('page',1)
        items_per_page = request.data.get('items_per_page') if request.data.get('items_per_page') else 10
        
        combined_conditions=Q()
        
        filter_condition = {}
        
        if branch != None:
            
            filter_condition['branch'] = branch
        
        if search != "":
            or_conditions = []
            or_conditions.append(Q(payment_id__icontains=search))

            for condition in or_conditions:
                combined_conditions |= condition
        
        if vendor != None:
            
            filter_condition['vendor_details'] = vendor
            
        if from_date != None and to_date != None:
            
            data_range = (from_date,to_date)
            
            filter_condition['payment_date__range'] =  data_range
        
        if cancel_status != None:
            filter_condition['is_canceled'] = cancel_status
            
        if len(filter_condition) != 0 :
            
            queryset = VendorPayment.objects.filter(combined_conditions,**filter_condition).order_by('-id')
            
        else:
            
            queryset = VendorPayment.objects.filter(combined_conditions).order_by('-id')
            
        paginated_data = Paginator(queryset, items_per_page)
        serializer = VendorPaymentSerializer(paginated_data.get_page(page), many=True)
        total_items = len(queryset)

        response_data = []
        
        for data in serializer.data:
            
            res_data = data
            
            payment_queryset = VendorPayment.objects.get(id=data['id'])
            
            res_data['vendor_details_name'] = payment_queryset.vendor_details.account_head_name
            
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
                "message":res_msg.retrieve("Vendor Payment Table List"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class VendorLedgerListView(APIView):
    
    def post(self,request):

        if request.user.role.is_admin == False:
            branch = request.user.branch.pk
        else:
            branch = request.data.get('branch')
                
        vendor = request.data.get('vendor',None)
        from_date = request.data.get('from_date',None)
        to_date = request.data.get('to_date',None)
        search = request.data.get('search',"")
        transaction_type = request.data.get('transaction_type',None)
        cancel_status = request.data.get('status',None)
        page = request.data.get('page',1)
        items_per_page = request.data.get('items_per_page') if request.data.get('items_per_page') else 10
        
        combined_conditions=Q()
        
        filter_condition = {}
        
        if search != "":
            or_conditions = []
            or_conditions.append(Q(refference_number__icontains=search))

            for condition in or_conditions:
                combined_conditions |= condition
        
        if vendor != None:
            
            filter_condition['vendor_details'] = vendor

            
        if from_date != None and to_date != None:
            
            date_range = (from_date,to_date)
            
            filter_condition['transaction_date__range'] = date_range
            
        
            
        total_weight = 0
        total_amount = 0
        
        disc_weight = 0
        disc_amount = 0
        
        paid_weight = 0
        paid_amount = 0
        
        
        if len(filter_condition) != 0 :
            
            calc_queryset = VendorLedger.objects.filter(**filter_condition,is_canceled = False)
            
        else:
            
            calc_queryset = VendorLedger.objects.filter(is_canceled = False)
            
        for data in calc_queryset : 
            
            if data.transaction_type.pk == settings.PAYMENT_VENDOR_LEDGER:
                
                paid_weight += data.transaction_weight
                paid_amount += data.transaction_amount
                
            elif data.transaction_type.pk == settings.DISCOUNT_VENDOR_LEDGER:
                
                disc_weight += data.transaction_weight
                disc_amount += data.transaction_amount
                
            else:
                total_weight += data.transaction_weight           
                total_amount += data.transaction_amount
                
        balance_weight = total_weight-(disc_weight+paid_weight)  
        balance_amount = total_amount-(disc_amount+paid_amount)
        
        
        if branch != None:
            
            filter_condition['branch'] = branch

        if transaction_type != None:
            
            filter_condition['transaction_type'] = transaction_type
            
        if cancel_status != None:
            
            filter_condition['is_canceled'] = cancel_status
            
        if len(filter_condition) != 0 :
            
            queryset = VendorLedger.objects.filter(combined_conditions,**filter_condition).order_by('-id')
            
        else:
            
            queryset = VendorLedger.objects.filter(combined_conditions).order_by('-id')
            
        paginated_data = Paginator(queryset, items_per_page)
        serializer = VendorLedgerSerializer(paginated_data.get_page(page), many=True)
        total_items = len(queryset)

        response_data = []
        
        for data in serializer.data:
            
            res_data = data
            
            ledger_queryset = VendorLedger.objects.get(id=data['id'])
            
            res_data['vendor_details_name'] = ledger_queryset.vendor_details.account_head_name
            res_data['branch_name'] = ledger_queryset.branch.branch_name
            res_data['transaction_type_name'] = ledger_queryset.transaction_type.vendor_ledger_type
            
            response_data.append(res_data)
            
        for i in range(len(response_data)):
            
            response_data[i]['s_no'] = i+1

        return Response(
            {
                "data":{
                    "list":response_data,
                    "total_weight":total_weight,
                    "total_amount":total_amount,
                    "disc_weight":disc_weight,
                    "disc_amount":disc_amount,
                    "paid_weight":paid_weight,
                    "paid_amount":paid_amount,
                    "balance_weight":balance_weight,
                    "balance_amount":balance_amount,
                    "total_pages": paginated_data.num_pages,
                    "current_page": page,
                    "total_items": total_items,
                    "current_items": len(serializer.data)
                },
                "message":res_msg.retrieve("Vendor Ledger Table List"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class VendorPaymentDetailsView(APIView):
    
    def get(self,request,vendor):
        
        if vendor == None:
            
            return Response(
                {
                    "message":res_msg.missing_fields("Vendor"),
                    "status":status.HTTP_204_NO_CONTENT
                },status=status.HTTP_200_OK
            )
            
        total_weight = 0.0
        total_amount = 0.0
        
        disc_weight = 0.0
        disc_amount = 0.0
        
        paid_weight = 0.0
        paid_amount = 0.0
            
        queryset = VendorLedger.objects.filter(vendor_details=vendor).order_by('-id')
        
        serializer = VendorLedgerSerializer(queryset,many=True)
        
        for data in queryset : 
            
            if data.is_canceled == False:
                if data.transaction_type.pk == settings.PAYMENT_VENDOR_LEDGER:
                    
                    paid_weight += data.transaction_weight
                    paid_amount += data.transaction_amount
                    
                elif data.transaction_type.pk == settings.DISCOUNT_VENDOR_LEDGER:
                    
                    disc_weight += data.transaction_weight
                    disc_amount += data.transaction_amount
                    
                else:
                    total_weight += data.transaction_weight           
                    total_amount += data.transaction_amount
                
        balance_weight = total_weight-(disc_weight+paid_weight)  
        balance_amount = total_amount-(disc_amount+paid_amount)
        
        res_data = {}
        
        try:
            
            vendor_queryset = AccountHeadDetails.objects.get(id=vendor)
            res_data['vendor_name'] = vendor_queryset.account_head_name

            try:
                vendor_contact_queryset = AccountHeadContact.objects.get(account_head=vendor)
                res_data['vendor_phone'] = vendor_contact_queryset.mobile_number
            except AccountHeadContact.DoesNotExist:
                res_data['vendor_phone'] = None

            try:
                vendor_address_queryset = AccountHeadAddress.objects.get(account_head=vendor)
                res_data['door_no'] = vendor_address_queryset.door_no
                res_data['area'] = vendor_address_queryset.area
                res_data['street_name'] = vendor_address_queryset.street_name
                res_data['district'] = vendor_address_queryset.district
                res_data['state'] = vendor_address_queryset.state
                res_data['country'] = vendor_address_queryset.country
                res_data['pin_code'] = vendor_address_queryset.pin_code
            except AccountHeadAddress.DoesNotExist:
                res_data['door_no'] = None
                res_data['area'] = None
                res_data['street_name'] = None
                res_data['district'] = None
                res_data['state'] = None
                res_data['country'] = None
                res_data['pin_code'] = None

        except:
            
            res_data['vendor_name'] = None
            res_data['vendor_phone'] = None
            res_data['door_no'] = None
            res_data['area'] = None
            res_data['street_name'] = None
            res_data['district'] = None
            res_data['state'] = None
            res_data['country'] = None
            res_data['pin_code'] = None
        
        res_data['total_weight'] = total_weight
        res_data['total_amount'] = total_amount
        res_data['disc_weight'] = disc_weight
        res_data['disc_amount'] = disc_amount
        res_data['paid_weight'] = paid_weight
        res_data['paid_amount'] = paid_amount
        res_data['balance_weight'] = balance_weight
        res_data['balance_amount'] = balance_amount
        res_data['ledger_list'] = serializer.data
        
        return Response(
            {
                "data":res_data,
                "message":res_msg.retrieve("vendor Payment Details"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
        
        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class VendorLedgerListExcelView(APIView):
    
    def post(self,request):
                
        vendor = request.data.get('vendor',None)
        from_date = request.data.get('from_date',None)
        to_date = request.data.get('to_date',None)
        search = request.data.get('search',"")
        transaction_type = request.data.get('transaction_type',None)
        cancel_status = request.data.get('status',None)
        
        combined_conditions=Q()
        
        filter_condition = {}
        
        if search != "":
            or_conditions = []
            or_conditions.append(Q(refference_number__icontains=search))

            for condition in or_conditions:
                combined_conditions |= condition
        
        if vendor != None:
            
            filter_condition['vendor_details'] = vendor

            
        if from_date != None and to_date != None:
            
            date_range = (from_date,to_date)
            
            filter_condition['transaction_date__range'] = date_range
            
        if request.user.role.is_admin == True:
            branch = request.data.get('branch')
        else:
             branch = request.user.branch.pk
        
        
        if branch != None:
            
            filter_condition['branch'] = branch

        if transaction_type != None:
            
            filter_condition['transaction_type'] = transaction_type
            
            
        if cancel_status != None:
            
            filter_condition['is_canceled'] = cancel_status
            
        if len(filter_condition) != 0 :
            
            queryset = VendorLedger.objects.filter(combined_conditions,**filter_condition).order_by('-id')
            
        else:
            
            queryset = VendorLedger.objects.filter(combined_conditions).order_by('-id')
            
        serializer = VendorLedgerSerializer(queryset, many=True)

        response_data = []
        
        for data in serializer.data:
            
            res_data = data
            
            ledger_queryset = VendorLedger.objects.get(id=data['id'])
            
            res_data['vendor_details_name'] = ledger_queryset.vendor_details.account_head_name
            
            response_data.append(res_data)
            
        df = pd.DataFrame(response_data)
    
        df.to_excel(settings.EXPORT_URL, index=False)
        
        res_data={}
        
        res_data['path']=settings.EXPORT_URL
        
        return Response(
            {
                "data":res_data,
                "message":res_msg.create("Excel"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
            
        
            
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class VendorPaymentListExcelView(APIView):
    
    def post(self,request):
        
        if request.user.role.is_admin == True:
            branch = request.data.get('branch')
        else:
            branch = request.user.branch.pk

        vendor = request.data.get('vendor',None)
        from_date = request.data.get('from_date',None)
        to_date = request.data.get('to_date',None)
        search = request.data.get('search',"")
        cancel_status = request.data.get('status',None)
        
        combined_conditions=Q()
        
        filter_condition = {}
        
        if branch != None:
            
            filter_condition['branch'] = branch
        
        if search != "":
            or_conditions = []
            or_conditions.append(Q(payment_id__icontains=search))

            for condition in or_conditions:
                combined_conditions |= condition
        
        if vendor != None:
            
            filter_condition['vendor_details'] = vendor
            
        if from_date != None and to_date != None:
            
            data_range = (from_date,to_date)
            
            filter_condition['payment_date__range'] =  data_range
        
        if cancel_status != None:
            filter_condition['is_canceled'] = cancel_status

            
        if len(filter_condition) != 0 :
            
            queryset = VendorPayment.objects.filter(combined_conditions,**filter_condition).order_by('-id')
            
        else:
            
            queryset = VendorPayment.objects.filter(combined_conditions).order_by('-id')
            
        serializer = VendorPaymentSerializer(queryset, many=True)

        response_data = []
        
        for data in serializer.data:
            
            res_data = data
            
            payment_queryset = VendorPayment.objects.get(id=data['id'])
            
            res_data['vendor_details_name'] = payment_queryset.vendor_details.account_head_name
            
            response_data.append(res_data)
            
        df = pd.DataFrame(response_data)
    
        df.to_excel(settings.EXPORT_URL, index=False)
        
        res_data={}
        
        res_data['path']=settings.EXPORT_URL
        
        return Response(
            {
                "data":res_data,
                "message":res_msg.create("Excel"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
            
        
        
        
        
        
        
        
        
            

        
        
        
    
    