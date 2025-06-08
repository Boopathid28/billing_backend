from django.shortcuts import render

from purchase.models import PurchaseEntry
from tagging.models import Lot
from .models import *
from rest_framework.views import APIView
from rest_framework import status,viewsets
from django.utils import timezone
from app_lib.response_messages import ResponseMessages
# from .serializer import *
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.db.models import ProtectedError
from masters.models import StoneDetails
from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework import filters
from books.models import *
import random
from django.conf import settings
from masters.models import MetalRate
from billing.models import *
from dateutil.relativedelta import relativedelta
from product.models import *
from value_addition.models import *
from organizations.models import *
from accounts.models import *
from django.db import transaction
import calendar
from django.db.models import Sum
from datetime import datetime,timedelta
from django.db.models import Count
from django.db.models.functions import ExtractMonth

res_msg = ResponseMessages()



@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class DashboardCountView(APIView):
    def post(self,request):

        filter_condition = {}

        if request.user.role.is_admin == False:
            filter_condition['branch'] = request.user.branch.pk

        else:
            if request.data.get('branch') != None:
                filter_condition['branch'] =  request.data.get('branch')

        from_date = request.data.get('from_date') if request.data.get('from_date') != None else None
        to_date = request.data.get('to_date') if request.data.get('to_date') != None else None        
        

        if from_date != None and to_date!= None:
            # fdate =from_date+'T00:00:00.899010+05:30'
            # tdate =to_date+'T23:59:59.899010+05:30'
            date_range=(from_date,to_date)
            filter_condition['created_at__range']=date_range

        # res_data = []
        count = {}
        if len(filter_condition) != 0:
            billing_queryset = BillingDetails.objects.filter(**filter_condition).count()
            count['billing'] = billing_queryset

            estimation_queryset = EstimateDetails.objects.filter(**filter_condition).count()
            count['estimation'] = estimation_queryset

            tag_queryset = TaggedItems.objects.filter(**filter_condition).count()
            count['tag_entry'] = tag_queryset

            purchase_queryset = PurchaseEntry.objects.filter(**filter_condition).count()
            count['purchase'] = purchase_queryset
           
        else:
            
            billing_queryset = BillingDetails.objects.all().count()
            count['billing'] = billing_queryset

            estimation_queryset = EstimateDetails.objects.all().count()
            count['estimation'] = estimation_queryset

            tag_queryset = TaggedItems.objects.all().count()
            count['tag_entry'] = tag_queryset

            purchase_queryset = PurchaseEntry.objects.all().count()
            count['purchase'] = purchase_queryset

        # itemfilter_condition = {}
        # if from_date != None and to_date!= None:          
        #     date_range=(from_date,to_date)
        #     itemfilter_condition['created_at__range']=date_range

        # item_queryset = Item.objects.filter(**itemfilter_condition).count()
        # count['item'] = item_queryset

        

        # res_data.append(count)

        return Response(
            {
                "data":{
                    "list":count
                },
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class TotalPaymentView(APIView):
    def post(self,request):
        filter_condition = {}

        if request.user.role.is_admin == False:
            filter_condition['branch'] = request.user.branch.pk

        else:
            if request.data.get('branch') != None:
                filter_condition['branch'] =  request.data.get('branch')

        current_date = datetime.now()
        year = current_date.year
        month = current_date.month
        _, num_days = calendar.monthrange(year, month)

        start_date = datetime(year, month, 1)
        end_date = datetime(year, month, num_days)
        end_date += timedelta(days=1)

        year_start_date = datetime(year, 1, 1).date()
        year_end_date = datetime(year, 12, 31).date()
        year_end_date += timedelta(days=1)

        if len(filter_condition) != 0:
            today_queryset = list(BillingDetails.objects.filter(bill_date__icontains = current_date.date(),**filter_condition))
            today_amount = sum(data.paid_amount for data in today_queryset)

            monthly_queryset = list(BillingDetails.objects.filter(bill_date__range = (start_date.date(),end_date.date()),**filter_condition))
            monthly_amount = sum(data.paid_amount for data in monthly_queryset)

            year_queryset = list(BillingDetails.objects.filter(bill_date__range = (year_start_date,year_end_date),**filter_condition))
            yearwise_paid_amount = sum(data.paid_amount for data in year_queryset)
        else:
            today_queryset = list(BillingDetails.objects.filter(bill_date__icontains = current_date.date()))
            today_amount = sum(data.paid_amount for data in today_queryset)

            monthly_queryset = list(BillingDetails.objects.filter(bill_date__range = (start_date.date(),end_date.date())))
            monthly_amount = sum(data.paid_amount for data in monthly_queryset)

            year_queryset = list(BillingDetails.objects.filter(bill_date__range = (year_start_date,year_end_date)))
            yearwise_paid_amount = sum(data.paid_amount for data in year_queryset)

        
        res_data = {
            
                'today_amount': today_amount,           
                'monthly_amount': monthly_amount,  
                'yearwise_amount': yearwise_paid_amount
            
        }
        
        return Response(
            {
                "data":{
                    "list":res_data
                },
                "message" : res_msg.retrieve("payment count"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class MetalWiseSalesView(APIView):
    def post(self,request):

        from_date = request.data.get('from_date') if request.data.get('from_date') != None else None
        to_date = request.data.get('to_date') if request.data.get('to_date') != None else None
        # if to_date != None:
            # to_date += timedelta(days=1)

        res_data = []
       
        gold_weight = 0
        silver_weight =0 
        filter_condition = {}

        if request.user.role.is_admin == False:
            filter_condition['branch'] = request.user.branch.pk
        else:
            if request.data.get('branch') != None:
                filter_condition['branch'] =  request.data.get('branch')

        if from_date != None and to_date != None:
            filter_condition['bill_date__range'] = (from_date,to_date)

        if len(filter_condition) != 0:
            bill_queryset = list(BillingDetails.objects.filter(**filter_condition).order_by('-id'))
        else:
            bill_queryset = list(BillingDetails.objects.all().order_by('-id'))

        
        for data in bill_queryset:
            tag_item_queryset = list(BillingTagItems.objects.filter(billing_details = data.pk).order_by('-id'))
            
            for i in tag_item_queryset:
                if i.metal.pk == 1:
                    gold_weight += i.gross_weight
                elif i.metal.pk == 2:
                    silver_weight += i.gross_weight
        
        res_data ={
                'gold_weight': gold_weight,            
                'silver_weight': silver_weight
            }
        
        
        return Response(
            {
                "data":{
                    "list":res_data
                },
                "message" : res_msg.retrieve("Metal Wise Sales"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
    
    

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ItemWiseStockListView(APIView):
    def post(self,request):

        from_date = request.data.get('from_date') if request.data.get('from_date') != None else None
        to_date = request.data.get('to_date') if request.data.get('to_date') != None else None
        # if to_date != None:
            # to_date += timedelta(days=1)

        res_data = []

        filter_condition = {}    

        if from_date != None and to_date != None:
            filter_condition['created_at__range'] = (from_date,to_date)
        
        item_weights = {}
        if len(filter_condition) != 0:
            item_queryset = Item.objects.filter(**filter_condition).order_by('-id')
        else:
            item_queryset = Item.objects.all().order_by('-id')

        for item in item_queryset:
            item_name = item.item_name
            
            if item_name not in item_weights:
                item_weights[item_name] = {
                    'total_weight': 0,
                    'total_stock': 0
                }

            tagfilter_condition ={}
            if request.user.role.is_admin == False:
                tagfilter_condition['branch'] = request.user.branch.pk
            else:
                if request.data.get('branch') != None:
              
                    tagfilter_condition['branch'] =  request.data.get('branch')

            if len(tagfilter_condition) != 0:
                tag_item_queryset = TaggedItems.objects.filter(item_details__item_details__id=item.pk,**tagfilter_condition).order_by('-id')
            else:
                tag_item_queryset = TaggedItems.objects.all().order_by('-id')

            item_weight = sum(tag_item.gross_weight for tag_item in tag_item_queryset)

            total_stock = tag_item_queryset.count()
            
            item_weights[item_name]['total_weight'] += item_weight
            item_weights[item_name]['total_stock'] += total_stock
            item_weights[item_name]['id'] = item.pk
       
        for item_name, data in item_weights.items():
            res_data.append({
                'id':data['id'],
                'item_name': item_name,
                'weight': data['total_weight'],
                'total_stock': data['total_stock']
            })
        return Response(
            {
                "data":{
                    "list":res_data
                },
                "message" : res_msg.retrieve("Metal Wise Sales"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
    


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class BillingListView(APIView):
    def post(self,request):

        from_date = request.data.get('from_date') if request.data.get('from_date') != None else None
        to_date = request.data.get('to_date') if request.data.get('to_date') != None else None
        # if to_date != None:
            # to_date += timedelta(days=1)

        res_data = []
        filter_condition = {}

        if request.user.role.is_admin == False:
            filter_condition['branch'] = request.user.branch.pk
        else:
            if request.data.get('branch') != None:
                filter_condition['branch'] =  request.data.get('branch')

        if from_date != None and to_date != None:
            filter_condition['created_at__range'] = (from_date,to_date)

        
        if len(filter_condition) != 0:
            billing_queryset = BillingDetails.objects.filter(**filter_condition).order_by('-id')
        else:
            billing_queryset = BillingDetails.objects.all().order_by('-id')

     
        for i in billing_queryset:  
            data={
                'id':i.pk,
                'bill_no': i.bill_no,
                'customer_name':i.customer_details.customer_name,
                'total_amount':i.total_amount
            }  
            res_data.append(data)    
        return Response(
            {
                "data":{
                    "list":res_data
                },
                "message" : res_msg.retrieve("Recent sales"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class PurchaseListView(APIView):
    def post(self,request):

        from_date = request.data.get('from_date') if request.data.get('from_date') != None else None
        to_date = request.data.get('to_date') if request.data.get('to_date') != None else None
        # if to_date != None:
            # to_date += timedelta(days=1)
        
        res_data = []
        filter_condition = {}
       
        if request.user.role.is_admin == False:
            filter_condition['branch'] = request.user.branch.pk
            
        else:
            if request.data.get('branch') != None:
                filter_condition['branch'] =  request.data.get('branch')

        if from_date != None and to_date != None:
            filter_condition['created_at__range'] = (from_date,to_date)
        
        if len(filter_condition) != 0:
            billing_queryset = PurchaseEntry.objects.filter(**filter_condition).order_by('-id')
        else:
            billing_queryset = PurchaseEntry.objects.all().order_by('-id')

     
        for i in billing_queryset:  
            person = Customer.objects.get(id =i.person_id)   #Old purchase so data should come from customer          
            person_name = person.customer_name
            data={
                'id':i.pk,
                'bill_no': i.bill_no,
                'customer_name':person_name,
                'total_amount':i.total_amount,                
                'type':'Old'
            }  
            res_data.append(data)    
        return Response(
            {
                "data":{
                    "list":res_data
                },
                "message" : res_msg.retrieve("Purchase entry"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class SalesandPurchaseListView(APIView):
        def post(self, request):
            filter_condition = {}

            if request.user.role.is_admin == False:
                filter_condition['branch'] = request.user.branch.pk

            else:
                if request.data.get('branch') != None:
                    filter_condition['branch'] =  request.data.get('branch')
           

            current_year = timezone.now().year         
            sales_data = []
            purchase_data = []

            for month in range(1, 13):            
                month_str = str(month).zfill(2)
                prefix = f'{current_year}-{month_str}'
                if len(filter_condition) != 0:
                    # Fetch sales data
                    sales_items = BillingDetails.objects.filter(created_at__icontains=prefix, **filter_condition)
                    sales_count = sales_items.count()
                    sales_data.append(sales_count)

                    # Fetch purchase data
                    purchase_items = PurchaseEntry.objects.filter(created_at__icontains=prefix, **filter_condition)
                    purchase_count = purchase_items.count()
                    purchase_data.append(purchase_count)
                else:
                    # Fetch sales data
                    sales_items = BillingDetails.objects.filter(created_at__icontains=prefix)
                    sales_count = sales_items.count()
                    sales_data.append(sales_count)

                    # Fetch purchase data
                    purchase_items = PurchaseEntry.objects.filter(created_at__icontains=prefix)
                    purchase_count = purchase_items.count()
                    purchase_data.append(purchase_count)


            response_data = [
                {
                    "name": "Sales",
                    "data": sales_data
                },
                {
                    "name": "Purchase",
                    "data": purchase_data
                }
            ]

            return Response(
                {
                    "data": {
                        'list':response_data
                    },
                    "message": "Sales and Purchase retrieved successfully!",
                    "status": status.HTTP_200_OK
                },
                status=status.HTTP_200_OK
            )
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class VendorListView(APIView):
    def post(self, request):
        filter_condition = {}

        if request.user.role.is_admin == False:
            filter_condition['branch'] = request.user.branch.pk

        else:
            if request.data.get('branch') != None:
                filter_condition['branch'] =  request.data.get('branch')



        current_year = timezone.now().year 
        customer_ids = AccountHeadDetails.objects.filter(is_active=True)  # Assuming vendor is your accounthead model
        response_data = []

        for customer_id in customer_ids:
            # vendor_data = {'name': customer_id.account_head_name, 'total_pieces': [],'total_grossweight':[],'total_netweight':[]}
            vendor_data = {'name': customer_id.account_head_name, 'data': []}

            for month in range(1, 13):
                month_str = str(month).zfill(2)
                prefix = f'{current_year}-{month_str}'
                if len(filter_condition) != 0:
                    total_pieces = Lot.objects.filter(created_at__icontains=prefix, designer_name=customer_id, **filter_condition).aggregate(total_pieces=Sum('total_pieces'))['total_pieces'] or 0
                    # total_grossweight = Lot.objects.filter(created_at__icontains=prefix, designer_name=customer_id, **filter_condition).aggregate(total_grossweight=Sum('total_grossweight'))['total_grossweight'] or 0
                    # total_netweight = Lot.objects.filter(created_at__icontains=prefix, designer_name=customer_id, **filter_condition).aggregate(total_netweight=Sum('total_netweight'))['total_netweight'] or 0

                    vendor_data['data'].append(total_pieces)
                    # vendor_data['total_grossweight'].append(total_grossweight)
                    # vendor_data['total_netweight'].append(total_netweight)
                else:
                    total_pieces = Lot.objects.filter(created_at__icontains=prefix, designer_name=customer_id).aggregate(total_pieces=Sum('total_pieces'))['total_pieces'] or 0
                    # total_grossweight = Lot.objects.filter(created_at__icontains=prefix, designer_name=customer_id, **filter_condition).aggregate(total_grossweight=Sum('total_grossweight'))['total_grossweight'] or 0
                    # total_netweight = Lot.objects.filter(created_at__icontains=prefix, designer_name=customer_id, **filter_condition).aggregate(total_netweight=Sum('total_netweight'))['total_netweight'] or 0

                    vendor_data['data'].append(total_pieces)
                    # vendor_data['total_grossweight'].append(total_grossweight)
                    # vendor_data['total_netweight'].append(total_netweight)
            
            response_data.append(vendor_data)

        return Response(
        {
            "data": {
                'list':response_data
            },
            "message": "Vendor wise sales retrieved successfully!",
            "status": status.HTTP_200_OK
        },
        status=status.HTTP_200_OK
    )