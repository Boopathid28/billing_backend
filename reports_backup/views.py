from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.response import Response
import customer
from order_management.models import OrderDetails, OrderItemDetails
from order_management.serializer import OrderDetailsSerializer
from settings.models import IncentivePercent
from .models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes, authentication_classes
from django.utils import timezone
from django.db.models import ProtectedError
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from django.core.paginator import Paginator
from app_lib.response_messages import ResponseMessages
from .serializer import *
from books.models import *
from books.serializer import *
import random
from django.conf import settings
from django.core.paginator import Paginator
from billing.models import *
from billing.serializer import *
from tagging.models import *
from tagging.serializer import *
from organizations.models import *
from organizations.serializer import *
from product.serializer import *
from billing.serializer import EstimateDetailsSerializer
from billing_backup.models import *
from billing_backup.serializer import *
from customer.serializer import *
from datetime import date, timedelta
from django.db.models import Sum
from purchase.models import *
from purchase.serializers import *
from repair_management.models import *
from repair_management.serializer import *
from stock.models import *
from stock.serializer import *
from payment_management.models import *
from payment_management.serializer import *
from masters.serializer import *

res_msg = ResponseMessages()

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class EstimationReportListView(APIView):
    def post(self,request):
        
        request_data=request.data
        
        search=request_data.get('search') if request_data.get('search') else ''
        from_date = request_data.get('from_date') if request_data.get('from_date') != None else None
        to_date = request_data.get('to_date') if request_data.get('to_date') != None else None
        metal_type = request_data.get('metal_type') if request_data.get('metal_type') != None else None
        page = request_data.get('page') if request_data.get('page') else 1
        branch = request_data.get('branch') if request_data.get('branch') else None
        try:
            items_per_page = int(request_data.get('items_per_page', EstimateDetails.objects.all().count()))
            if items_per_page == 0:
                items_per_page = 10 
        except Exception as err:
            items_per_page = 10 
        
        filter_condition={}

        if request.user.role.is_admin == True:
            if branch != None :
                filter_condition['branch'] = branch
        else:
            filter_condition['branch'] = request.user.branch.pk
        
    
        if search != "" :
            filter_condition['estimate_no__icontains'] = search

        if metal_type != None:
            filter_condition['metal'] = metal_type

        if from_date != None and to_date != None :
            date_range=(from_date,to_date)
            filter_condition['created_at__range'] = date_range
        
        if len(filter_condition) != 0:

            queryset=EstimateDetails.objects.filter(**filter_condition).order_by('-id')
            
        else:

            queryset=EstimateDetails.objects.all().order_by('-id')

        paginated_data = Paginator(queryset, items_per_page)
        serializer = EstimateDetailsSerializer(paginated_data.get_page(page), many=True)

        response_data=[]
        total_total_amount = 0
        total_gst_amount = 0
        total_advance_amount = 0
        total_discount_amount = 0
        total_chit_amount = 0
        total_exchange_amount = 0
        total_return_amount = 0
        total_cash_amount = 0
        total_card_amount = 0
        total_account_transfer_amount = 0
        total_upi_amount = 0
        total_bill_total = 0
        total_paid_amount = 0
        for i in range(0, len(serializer.data)):
            dict_data=serializer.data[i]
            
            dict_data['customer_name']=queryset[i].customer_details.customer_name
            dict_data['customer_mobile']=queryset[i].customer_details.phone
            dict_data['door_no']=queryset[i].customer_details.door_no
            dict_data['street_name']=queryset[i].customer_details.street_name
            dict_data['area']=queryset[i].customer_details.area
            dict_data['district']=queryset[i].customer_details.district
            dict_data['state_name']=queryset[i].customer_details.state
            dict_data['country']=queryset[i].customer_details.country
            dict_data['pincode']=queryset[i].customer_details.pincode
            try:
                estimation_item_queryset = list(EstimationTagItems.objects.filter(estimation_details = queryset[i].pk))
                total_weight = 0
                total_amount = 0
                wastage_percentage = 0
                flat_wastage = 0
                making_charge = 0
                flat_making_charge = 0
                for item in estimation_item_queryset:
                    total_weight += item.gross_weight
                    total_amount += item.total_rate
                    wastage_percentage += int(item.wastage_percentage) if (item, 'wastage_percentage') != None else "---"
                    flat_wastage += float(item.flat_wastage) if (item, 'flat_wastage') != None else "---"
                    making_charge += float(item.making_charge) if (item, 'making_charge') != None else "---"
                    flat_making_charge += float(item.flat_making_charge) if (item, 'flat_making_charge') != None else "---"

                    dict_data['item_name']=item.item_details.item_name
                    dict_data['weight'] = total_weight
                    dict_data['amount'] = total_amount
                    dict_data['wastage_percentage'] = wastage_percentage
                    dict_data['flat_wastage'] = flat_wastage
                    dict_data['making_charge'] = making_charge
                    dict_data['flat_making_charge'] = flat_making_charge
            except Exception as err:
                dict_data['item_name']= "--"
                dict_data['weight'] = 0
                dict_data['amount'] = 0
            total_total_amount += queryset[i].total_amount
            total_exchange_amount += queryset[i].exchange_amount
            total_advance_amount += queryset[i].advance_amount
            total_gst_amount += queryset[i].gst_amount
            total_discount_amount += queryset[i].discount_amount
            total_bill_total += queryset[i].payable_amount
            total_chit_amount += queryset[i].chit_amount
            total_cash_amount += queryset[i].cash_amount
            total_account_transfer_amount += queryset[i].account_transfer_amount
            total_card_amount += queryset[i].card_amount
            total_upi_amount += queryset[i].upi_amount
            total_paid_amount +=queryset[i].paid_amount
            dict_data['branch_name']=queryset[i].branch.branch_name
            
            try:
                
                dict_data['sales_person']=queryset[i].created_by.get_username()
                dict_data['billing_person']=queryset[i].created_by.get_username()
            except Exception as err:
                dict_data['sales_person'] = "---"
                dict_data['billing_person'] = "---"

            response_data.append(dict_data)
        
        return Response(
        {
            "data":{
                "list":response_data,
                "total_pages": paginated_data.num_pages,
                "current_page": page,
                "total_items": len(queryset),
                "current_items": len(serializer.data),
                "total_total_amount " : total_total_amount,
                "total_gst_amount " : total_gst_amount,
                "total_advance_amount " : total_advance_amount,
                "total_discount_amount " : total_discount_amount,
                "total_chit_amount " : total_chit_amount,
                "total_exchange_amount " : total_exchange_amount,
                "total_return_amount " : total_return_amount,
                "total_cash_amount " : total_cash_amount,
                "total_card_amount " : total_card_amount,
                "total_account_transfer_amount " : total_account_transfer_amount,
                "total_upi_amount " : total_upi_amount,
                "total_bill_total " : total_bill_total,
                "total_paid_amount " : total_paid_amount,
            },
            "message":res_msg.retrieve("Estimation Sale List"),
            "status":status.HTTP_200_OK
        },status=status.HTTP_200_OK
        )
        
        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class TagItemListView(APIView):
        
    def post(self,request):

        request_data=request.data
        
        search=request_data.get('search') if request_data.get('search') else ''
        from_date = request_data.get('from_date') if request_data.get('from_date') != None else None
        to_date = request_data.get('to_date') if request_data.get('to_date') != None else None
        metal_type = request_data.get('metal_type') if request_data.get('metal_type') != None else None
        page = request_data.get('page') if request_data.get('page') else 1
        branch = request.data.get('branch') if request.data.get('branch') else None
        try:
            items_per_page = int(request.data.get('items_per_page', TaggedItems.objects.all().count()))
            if items_per_page == 0:
                items_per_page = 10 
        except Exception as err:
            items_per_page = 10 

        filter_condition={}

        if request.user.role.is_admin == True :
            if branch != None:            
                filter_condition['branch'] = branch
        else:
            filter_condition['branch'] = request.user.branch.pk
        
        if search != "" :
            filter_condition['tag_number__icontains'] = search

        if metal_type != None:
            filter_condition['sub_item_details__metal'] = metal_type

        if from_date != None and to_date != None :
            date_range=(from_date,to_date)
            filter_condition['created_at__range'] = date_range
        
        if len(filter_condition) != 0:

            queryset=TaggedItems.objects.filter(**filter_condition)

        else:

            queryset=TaggedItems.objects.all()
        
        paginated_data = Paginator(queryset, items_per_page)
        serializer = TaggedItemsSerializer(paginated_data.get_page(page), many=True)

        response_data=[]
        for i in range(0, len(serializer.data)):
            dict_data=serializer.data[i]
            dict_data['item_name'] = queryset[i].item_details.item_details.item_name
            dict_data['subitem_name'] = queryset[i].sub_item_details.sub_item_name
            dict_data['metal_name'] = queryset[i].sub_item_details.metal.metal_name
            dict_data['tag_type_name'] = queryset[i].tag_type.tag_name
            dict_data['calculation_type_name'] = queryset[i].calculation_type.calculation_name


            response_data.append(dict_data)

        return Response(
        {
            "data":{
                "list":response_data,
                "total_pages": paginated_data.num_pages,
                "current_page": page,
                "total_items": len(queryset),
                "current_items": len(serializer.data)
            },
            "message":res_msg.retrieve("Estimation List"),
            "status":status.HTTP_200_OK
        },status=status.HTTP_200_OK
        )
    
       
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class TaggedItemWiseListView(APIView):
    def post(self,request):
 
        request_data=request.data
       
        search=request_data.get('search') if request_data.get('search') else ''
        from_date = request_data.get('from_date') if request_data.get('from_date') != None else None
        to_date = request_data.get('to_date') if request_data.get('to_date') != None else None
        metal_type = request_data.get('metal_type') if request_data.get('metal_type') != None else None
        page = request_data.get('page') if request_data.get('page') else 1
        branch = request.data.get('branch') if request.data.get('branch') else None
       
        filter_condition={}
        try:
            items_per_page = int(request.data.get('items_per_page', TaggedItems.objects.all().count()))
            if items_per_page == 0:
                items_per_page = 10
        except Exception as err:
            items_per_page = 10
 
        if search != "" :
            filter_condition['item_name__icontains'] = search
 
        if metal_type != None:
            filter_condition['metal'] = metal_type
 
        if from_date != None and to_date != None :
            date_range=(from_date,to_date)
            filter_condition['created_at__range'] = date_range
       
        if len(filter_condition) != 0:
 
            queryset= Item.objects.filter(**filter_condition).order_by('id')
           
        else:
 
            queryset=Item.objects.all()
     
        paginated_data = Paginator(queryset, items_per_page)
        serializer = ItemSerializer(paginated_data.get_page(page), many=True)
 
        response_data=[]
        filter_dict = {}
        total_pieces = 0
        total_gross_weight = 0
        total_net_weight = 0
        for i in range(0, len(serializer.data)):
            dict_data=serializer.data[i]
            dict_data['metal_name'] = queryset[i].metal.metal_name
 
            try:
                if request.user.role.is_admin ==True:
                    if branch != None:
                        filter_dict['branch'] = branch      
                else:
                    filter_dict['branch'] = request.user.branch.pk
 
                tagitem_queryset = TaggedItems.objects.filter(item_details=queryset[i].pk,**filter_dict)
               
                if len(tagitem_queryset) > 0:
                    for item in tagitem_queryset:
                        total_pieces += item.tag_count
                        total_gross_weight += item.gross_weight
                        total_net_weight += item.net_weight
                       
                        dict_data['tag_count'] = total_pieces
                        dict_data['gross_weight'] = total_gross_weight
                        dict_data['net_weight'] = total_net_weight
                else:
                    dict_data['tag_count'] = 0
                    dict_data['gross_weight'] = 0
                    dict_data['net_weight'] = 0
           
            except Exception as err:
                pass
            response_data.append(dict_data)
 
        return Response(
        {
            "data":{
                "list":response_data,
                "total_pages": paginated_data.num_pages,
                "current_page": page,
                "total_items": len(queryset),
                "current_items": len(serializer.data)
            },
            "message":res_msg.retrieve("Estimation List"),
            "status":status.HTTP_200_OK
        },status=status.HTTP_200_OK
        )
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class EstimationGSTReportView(APIView):

    def post(self,request):

        request_data = request.data

        from_date = request_data.get('from_date') if request_data.get('from_date') else None
        to_date = request_data.get('to_date') if request_data.get('to_date') else None
        search = request_data.get('search') if request_data.get('search') else None
        branch = request_data.get('branch') if request_data.get('branch') else None
        page = request_data.get('page') if request_data.get('page') else None
        try:
            items_per_page = int(request.data.get('items_per_page', TaggedItems.objects.all().count()))
            if items_per_page == 0:
                items_per_page = 10 
        except Exception as err:
            items_per_page = 10 

        filter_condition = {}

        if request.user.role.is_admin == True:
            if branch !=None :
                filter_condition['branch'] = branch

        else:
            filter_condition['branch'] = request.user.branch.pk

        if from_date != None and to_date != None :
            date_range = (from_date,to_date)
            filter_condition['created_at__range']=date_range

        if search != None:
            filter_condition['estimate_no__icontains'] = search

        if len(filter_condition) != 0:

            queryset= EstimateDetails.objects.filter(**filter_condition).order_by('id')
            
        else:

            queryset=EstimateDetails.objects.all().order_by('id')

        paginated_data = Paginator(queryset, items_per_page)
        serializer = EstimateDetailsSerializer(paginated_data.get_page(page), many=True)

        response_data=[]
        total_gst_value = 0

        for i in serializer.data:
            res_data={}
            data_queryset = EstimateDetails.objects.get(id=i['id'])
            res_data['id'] = data_queryset.pk
            res_data['estimation_number'] = data_queryset.estimate_no
            res_data['branch'] = data_queryset.branch.branch_name
            res_data['created_at'] = data_queryset.created_at

            res_data['gst_percent'] = '3.0%'

            res_data['gst_value'] = data_queryset.gst_amount
            total_gst_value += data_queryset.gst_amount
            response_data.append(res_data)

        return Response(
        {
            "data":{
                "list":response_data,
                "total_pages": paginated_data.num_pages,
                "current_page": page,
                "total_items": len(queryset),
                "current_items": len(serializer.data),
                "total_gst_value":total_gst_value
            },
            "message":res_msg.retrieve("Estimation Gst List"),
            "status":status.HTTP_200_OK
        },status=status.HTTP_200_OK
        )
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class BillingGSTReportView(APIView):

    def post(self,request):

        request_data = request.data

        from_date = request_data.get('from_date') if request_data.get('from_date') else None
        to_date = request_data.get('to_date') if request_data.get('to_date') else None
        search = request_data.get('search') if request_data.get('search') else None
        branch = request_data.get('branch') if request_data.get('branch') else None
        page = request_data.get('page') if request_data.get('page') else None
        try:
            items_per_page = int(request.data.get('items_per_page', TaggedItems.objects.all().count()))
            if items_per_page == 0:
                items_per_page = 10 
        except Exception as err:
            items_per_page = 10 

        filter_condition = {}

        if request.user.role.is_admin == True:
            if branch !=None :
                filter_condition['branch'] = branch

        else:
            filter_condition['branch'] = request.user.branch.pk

        if from_date != None and to_date != None :
            date_range = (from_date,to_date)
            filter_condition['created_at__range']=date_range

        if search != None:
            filter_condition['bill_no__icontains'] = search

        if len(filter_condition) != 0:

            queryset= BillingDetails.objects.filter(**filter_condition).order_by('id')
            
        else:

            queryset=BillingDetails.objects.all().order_by('id')

        paginated_data = Paginator(queryset, items_per_page)
        serializer = BillingDetailsSerializer(paginated_data.get_page(page), many=True)

        response_data=[]
        total_gst_value = 0

        for i in serializer.data:
            res_data={}
            data_queryset = BillingDetails.objects.get(id=i['id'])
            res_data['id'] = data_queryset.pk
            res_data['bill_no'] = data_queryset.bill_no
            res_data['branch'] = data_queryset.branch.branch_name
            res_data['created_at'] = data_queryset.created_at

            res_data['gst_percent'] = '3.0%'

            res_data['gst_value'] = data_queryset.gst_amount
            total_gst_value += data_queryset.gst_amount
            response_data.append(res_data)

        return Response(
        {
            "data":{
                "list":response_data,
                "total_pages": paginated_data.num_pages,
                "current_page": page,
                "total_items": len(queryset),
                "current_items": len(serializer.data),
                "total_gst_value":total_gst_value
            },
            "message":res_msg.retrieve("Billing Gst List"),
            "status":status.HTTP_200_OK
        },status=status.HTTP_200_OK
        )
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class BillingReportListView(APIView):
    def post(self,request):
        
        request_data=request.data
        
        search=request_data.get('search') if request_data.get('search') else ''
        from_date = request_data.get('from_date') if request_data.get('from_date') != None else None
        to_date = request_data.get('to_date') if request_data.get('to_date') != None else None
        metal_type = request_data.get('metal_type') if request_data.get('metal_type') != None else None
        customer_details = request_data.get('customer_details') if request_data.get('customer_details') != None else None
        page = request_data.get('page') if request_data.get('page') else 1
        branch = request_data.get('branch') if request_data.get('branch') else None
        try:
            items_per_page = int(request_data.get('items_per_page', BillingDetails.objects.all().count()))
            if items_per_page == 0:
                items_per_page = 10 
        except Exception as err:
            items_per_page = 10 
        
        filter_condition={}

        if request.user.role.is_admin == True:
            if branch != None :
                filter_condition['branch'] = branch
        else:
            filter_condition['branch'] = request.user.branch.pk
        
        if search != "" :
            filter_condition['bill_no__icontains'] = search

        if metal_type != None:
            filter_condition['bill_type'] = metal_type

        if customer_details != None:
            filter_condition['customer_details'] = customer_details

        if from_date != None and to_date != None :
            date_range=(from_date,to_date)
            filter_condition['created_at__range'] = date_range
        
        if len(filter_condition) != 0:

            queryset=BillingDetails.objects.filter(**filter_condition).order_by('-id')
            
        else:

            queryset=BillingDetails.objects.all().order_by('-id')

        paginated_data = Paginator(queryset, items_per_page)
        serializer = BillingDetailsSerializer(paginated_data.get_page(page), many=True)

        response_data=[]
        total_total_amount = 0
        total_gst_amount = 0
        total_advance_amount = 0
        total_discount_amount = 0
        total_chit_amount = 0
        total_exchange_amount = 0
        total_return_amount = 0
        total_cash_amount = 0
        total_card_amount = 0
        total_account_transfer_amount = 0
        total_upi_amount = 0
        total_bill_total = 0
        total_paid_amount = 0
        for i in range(0, len(serializer.data)):
            dict_data=serializer.data[i]
            
            dict_data['customer_name']=queryset[i].customer_details.customer_name
            dict_data['customer_mobile']=queryset[i].customer_details.phone
            dict_data['door_no']=queryset[i].customer_details.door_no
            dict_data['street_name']=queryset[i].customer_details.street_name
            dict_data['area']=queryset[i].customer_details.area
            dict_data['district']=queryset[i].customer_details.district
            dict_data['state_name']=queryset[i].customer_details.state
            dict_data['country']=queryset[i].customer_details.country
            dict_data['pincode']=queryset[i].customer_details.pincode
            try:
                estimation_item_queryset = list(BillingTagItems.objects.filter(billing_details = queryset[i].pk))
                total_weight = 0
                total_amount = 0
                wastage_percentage = 0
                flat_wastage = 0
                making_charge = 0
                flat_making_charge = 0
                for item in estimation_item_queryset:
                    total_weight += item.gross_weight
                    total_amount += item.total_rate
                    wastage_percentage += int(item.wastage_percentage) if (item, 'wastage_percentage') != None else "---"
                    flat_wastage += float(item.flat_wastage) if (item, 'flat_wastage') != None else "---"
                    making_charge += float(item.making_charge) if (item, 'making_charge') != None else "---"
                    flat_making_charge += float(item.flat_making_charge) if (item, 'flat_making_charge') != None else "---"

                    dict_data['item_name']=item.item_details.item_name
                    dict_data['metal_type']=item.metal.metal_name
                    dict_data['weight'] = total_weight
                    dict_data['amount'] = total_amount
                    dict_data['wastage_percentage'] = wastage_percentage
                    dict_data['flat_wastage'] = flat_wastage
                    dict_data['making_charge'] = making_charge
                    dict_data['flat_making_charge'] = flat_making_charge
                    
                    taggedd_item_queryset = TaggedItems.objects.get(tag_number=item.tag_number)
                    dict_data['vendor_name'] = taggedd_item_queryset.tag_entry_details.lot_details.designer_name.account_head_name
                    
            except Exception as err:
                dict_data['item_name']= "--"
                dict_data['weight'] = 0
                dict_data['amount'] = 0
                dict_data['vendor_name'] = "---"

            try:
                common_payment_queryset = CommonPaymentDetails.objects.filter(refference_number=queryset[i].bill_no)
                common_payment_serializer = CommonPaymentSerializer(common_payment_queryset,many=True)
                for j in range(0,len(common_payment_serializer.data)):
                    common_payment_data = common_payment_serializer.data[j]
                    dict_data['advance_amount'] = common_payment_queryset[j].advance_amount
                    dict_data['discount_amount'] = common_payment_queryset[j].discount_amount
                    dict_data['bill_total'] = common_payment_queryset[j].payable_amount
                    dict_data['total_exchange_amount'] += common_payment_queryset[j].exchange_amount
                    dict_data['total_advance_amount'] += common_payment_queryset[j].advance_amount
                    dict_data['total_discount_amount'] += common_payment_queryset[j].discount_amount
                    dict_data['total_bill_total'] += common_payment_queryset[j].payable_amount
            except:
                dict_data['total_exchange_amount'] = 0
                dict_data['total_advance_amount'] = 0
                dict_data['total_discount_amount'] = 0
                dict_data['total_bill_total'] = 0

            try:
                payment_queryset = CustomerPaymentTabel.objects.filter(refference_number=queryset[i].bill_no)
                payment_serializer = CustomerPaymentTabelSerializer(payment_queryset,many=True)
                for data in range(0,len(payment_serializer.data)):
                    payment_data = payment_serializer.data[data]
                    if payment_queryset[data].payment_method == settings.CASH:
                        dict_data['total_cash_amount'] += payment_queryset[data].paid_amount
                    else:
                        dict_data['total_cash_amount'] = 0

                    if payment_queryset[data].payment_method == settings.SCHEME:
                        dict_data['total_chit_amount'] += payment_queryset[data].paid_amount
                    else:
                        dict_data['total_chit_amount'] = 0

                    if payment_queryset[data].payment_method == settings.BANK:
                        dict_data['total_account_transfer_amount'] += payment_queryset[data].paid_amount
                    else:
                        dict_data['total_account_transfer_amount'] = 0

                    if payment_queryset[data].payment_method == settings.CARD:
                        dict_data['total_card_amount'] += payment_queryset[data].paid_amount
                    else:
                        dict_data['total_card_amount'] = 0

                    if payment_queryset[data].payment_method == settings.UPI:
                        dict_data['total_upi_amount'] += payment_queryset[data].paid_amount
                    else:
                        dict_data['total_upi_amount'] = 0

                    total_paid_amount +=payment_queryset[data].paid_amount
            except:
                dict_data['total_cash_amount'] = 0
                dict_data['total_chit_amount'] = 0
                dict_data['total_account_transfer_amount'] = 0
                dict_data['total_card_amount'] = 0
                dict_data['total_upi_amount'] = 0


            dict_data['branch_name']=queryset[i].branch.branch_name
            
            try:
                
                dict_data['sales_person']=queryset[i].created_by.get_username()
                dict_data['billing_person']=queryset[i].created_by.get_username()
            except Exception as err:
                dict_data['sales_person'] = "---"
                dict_data['billing_person'] = "---"

            response_data.append(dict_data)
        
        return Response(
        {
            "data":{
                "list":response_data,
                "total_pages": paginated_data.num_pages,
                "current_page": page,
                "total_items": len(queryset),
                "current_items": len(serializer.data),
                # "total_total_amount " : total_total_amount,
                # "total_gst_amount " : total_gst_amount,
                # "total_advance_amount " : total_advance_amount,
                # "total_discount_amount " : total_discount_amount,
                # "total_chit_amount " : total_chit_amount,
                # "total_exchange_amount " : total_exchange_amount,
                # "total_return_amount " : total_return_amount,
                # "total_cash_amount " : total_cash_amount,
                # "total_card_amount " : total_card_amount,
                # "total_account_transfer_amount " : total_account_transfer_amount,
                # "total_upi_amount " : total_upi_amount,
                # "total_bill_total " : total_bill_total,
                # "total_paid_amount " : total_paid_amount
            },
            "message":res_msg.retrieve("Estimation Sale List"),
            "status":status.HTTP_200_OK
        },status=status.HTTP_200_OK
        )
        

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class BillingBackupReportListView(APIView):
    def post(self,request):
        
        request_data=request.data
        
        search=request_data.get('search') if request_data.get('search') else ''
        from_date = request_data.get('from_date') if request_data.get('from_date') != None else None
        to_date = request_data.get('to_date') if request_data.get('to_date') != None else None
        metal_type = request_data.get('metal_type') if request_data.get('metal_type') != None else None
        page = request_data.get('page') if request_data.get('page') else 1
        branch = request_data.get('branch') if request_data.get('branch') else None
        try:
            items_per_page = int(request_data.get('items_per_page', BillingBackupDetails.objects.all().count()))
            if items_per_page == 0:
                items_per_page = 10 
        except Exception as err:
            items_per_page = 10 
        
        filter_condition={}

        if request.user.role.is_admin == True:
            if branch != None :
                filter_condition['branch'] = branch
        else:
            filter_condition['branch'] = request.user.branch.pk
        
    
        if search != "" :
            filter_condition['bill_no__icontains'] = search

        if metal_type != None:
            filter_condition['metal'] = metal_type

        if from_date != None and to_date != None :
            date_range=(from_date,to_date)
            filter_condition['created_at__range'] = date_range
        
        if len(filter_condition) != 0:

            queryset=BillingBackupDetails.objects.filter(**filter_condition).order_by('-id')
            
        else:

            queryset=BillingBackupDetails.objects.all().order_by('-id')

        paginated_data = Paginator(queryset, items_per_page)
        serializer = BillingBackupDetailsSerializer(paginated_data.get_page(page), many=True)

        response_data=[]
        total_total_amount = 0
        total_gst_amount = 0
        total_advance_amount = 0
        total_discount_amount = 0
        total_chit_amount = 0
        total_exchange_amount = 0
        total_return_amount = 0
        total_cash_amount = 0
        total_card_amount = 0
        total_account_transfer_amount = 0
        total_upi_amount = 0
        total_bill_total = 0
        total_paid_amount = 0
        for i in range(0, len(serializer.data)):
            dict_data=serializer.data[i]
            
            dict_data['customer_name']=queryset[i].customer_details.customer_name
            dict_data['customer_mobile']=queryset[i].customer_details.phone
            dict_data['door_no']=queryset[i].customer_details.door_no
            dict_data['street_name']=queryset[i].customer_details.street_name
            dict_data['area']=queryset[i].customer_details.area
            dict_data['district']=queryset[i].customer_details.district
            dict_data['state_name']=queryset[i].customer_details.state
            dict_data['country']=queryset[i].customer_details.country
            dict_data['pincode']=queryset[i].customer_details.pincode
            try:
                estimation_item_queryset = list(BillingBackupTagItems.objects.filter(billing_details = queryset[i].pk))
                total_weight = 0
                total_amount = 0
                wastage_percentage = 0
                flat_wastage = 0
                making_charge = 0
                flat_making_charge = 0
                for item in estimation_item_queryset:
                    total_weight += item.gross_weight
                    total_amount += item.total_rate
                    wastage_percentage += int(item.wastage_percentage) if (item, 'wastage_percentage') != None else "---"
                    flat_wastage += float(item.flat_wastage) if (item, 'flat_wastage') != None else "---"
                    making_charge += float(item.making_charge) if (item, 'making_charge') != None else "---"
                    flat_making_charge += float(item.flat_making_charge) if (item, 'flat_making_charge') != None else "---"

                    dict_data['item_name']=item.item_details.item_name
                    dict_data['weight'] = total_weight
                    dict_data['amount'] = total_amount
                    dict_data['wastage_percentage'] = wastage_percentage
                    dict_data['flat_wastage'] = flat_wastage
                    dict_data['making_charge'] = making_charge
                    dict_data['flat_making_charge'] = flat_making_charge
            except Exception as err:
                dict_data['item_name']= "--"
                dict_data['weight'] = 0
                dict_data['amount'] = 0
            total_total_amount += queryset[i].total_amount
            total_exchange_amount += queryset[i].exchange_amount
            total_advance_amount += queryset[i].advance_amount
            total_gst_amount += queryset[i].gst_amount
            total_discount_amount += queryset[i].discount_amount
            total_bill_total += queryset[i].payable_amount
            total_chit_amount += queryset[i].chit_amount
            total_cash_amount += queryset[i].cash_amount
            total_account_transfer_amount += queryset[i].account_transfer_amount
            total_card_amount += queryset[i].card_amount
            total_upi_amount += queryset[i].upi_amount
            total_paid_amount +=queryset[i].paid_amount
            dict_data['branch_name']=queryset[i].branch.branch_name
            
            try:
                
                dict_data['sales_person']=queryset[i].created_by.get_username()
                dict_data['billing_person']=queryset[i].created_by.get_username()
            except Exception as err:
                dict_data['sales_person'] = "---"
                dict_data['billing_person'] = "---"

            response_data.append(dict_data)
        
        return Response(
        {
            "data":{
                "list":response_data,
                "total_pages": paginated_data.num_pages,
                "current_page": page,
                "total_items": len(queryset),
                "current_items": len(serializer.data),
                "total_total_amount " : total_total_amount,
                "total_gst_amount " : total_gst_amount,
                "total_advance_amount " : total_advance_amount,
                "total_discount_amount " : total_discount_amount,
                "total_chit_amount " : total_chit_amount,
                "total_exchange_amount " : total_exchange_amount,
                "total_return_amount " : total_return_amount,
                "total_cash_amount " : total_cash_amount,
                "total_card_amount " : total_card_amount,
                "total_account_transfer_amount " : total_account_transfer_amount,
                "total_upi_amount " : total_upi_amount,
                "total_bill_total " : total_bill_total,
                "total_paid_amount " : total_paid_amount
            },
            "message":res_msg.retrieve("Billing Backup List"),
            "status":status.HTTP_200_OK
        },status=status.HTTP_200_OK
        )
        

# CUSTOMER WISE SALE REPORT #
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class CustomerWiseSaleReport(APIView):
    def post(self,request):
        
        request_data=request.data

        search=request_data.get('search') if request_data.get('search') else ''
        from_date = request_data.get('from_date') if request_data.get('from_date') != None else None
        to_date = request_data.get('to_date') if request_data.get('to_date') != None else None
        metal_type = request_data.get('metal_type') if request_data.get('metal_type') != None else None
        customer_details = request_data.get('customer_details') if request_data.get('customer_details') != None else None
        page = request_data.get('page') if request_data.get('page') else 1
        branch = request_data.get('branch') if request_data.get('branch') else None
        try:
            items_per_page = int(request_data.get('items_per_page', BillingDetails.objects.all().count()))
            if items_per_page == 0:
                items_per_page = 10 
        except Exception as err:
            items_per_page = 10 
        
        filter_condition={}

        if request.user.role.is_admin == True:
            if branch != None :
                filter_condition['branch'] = branch
        else:
            filter_condition['branch'] = request.user.branch.pk
        
        if search != "":
            filter_condition['bill_no'] = search

        if from_date != None and to_date != None :
            date_range=(from_date,to_date)
            filter_condition['created_at__range'] = date_range

        if customer_details != None :
            customer_queryset = Customer.objects.filter(id=customer_details).order_by('-id')
        else:
            customer_queryset = Customer.objects.all().order_by('-id')
        customer_serializer = CustomerSerializer(customer_queryset,many=True)

        for j in range(0,len(customer_serializer.data)):
            dict_data = {}
            dict_data['customer_name'] = customer_queryset[j].customer_name
            dict_data['customer_mobile'] = customer_queryset[j].phone
            if len(filter_condition) != 0:

                queryset=BillingDetails.objects.filter(**filter_condition,customer_details=customer_queryset[j].pk).order_by('-id')
                
            else:

                queryset=BillingDetails.objects.filter(customer_details=customer_queryset[j].pk).order_by('-id')

            paginated_data = Paginator(queryset, items_per_page)
            serializer = BillingDetailsSerializer(paginated_data.get_page(page), many=True)
            
            response_data = []
            bill_list = []
            total_data = {}
            total_gross_weight = 0
            total_net_weight = 0
            total_making_charge = 0
            total_net_amount = 0
            total_advance_amount = 0
            totalamount = 0
            for i in range(0, len(serializer.data)):
                bill_data = {}
                bill_data['bill_no']=queryset[i].bill_no
                bill_data['bill_date']=queryset[i].bill_date
                bill_data['branch_name']=queryset[i].branch.branch_name
                try:
                    
                    bill_data['sales_person']=queryset[i].created_by.get_username()
                    bill_data['billing_person']=queryset[i].created_by.get_username()
                except Exception as err:
                    bill_data['sales_person'] = "---"
                    bill_data['billing_person'] = "---"

                try:
                    payment_queryset = CommonPaymentDetails.objects.filter(refference_number=queryset[i].bill_no).order_by('-id').first()
                    bill_data['total_amount'] = payment_queryset.total_amount
                    bill_data['advance_amount'] = payment_queryset.advance_amount
                    bill_data['payable_amount'] = payment_queryset.payable_amount
                except: 
                    bill_data['total_amount'] = 0
                    bill_data['advance_amount'] = 0
                    bill_data['payable_amount'] = 0

                try:
                    if metal_type != None:
                        estimation_item_queryset = list(BillingTagItems.objects.filter(billing_details = queryset[i].pk,metal=metal_type))
                    else:
                        estimation_item_queryset = list(BillingTagItems.objects.filter(billing_details = queryset[i].pk))
                    
                    wastage_percentage = 0
                    flat_wastage = 0
                    making_charge = 0
                    flat_making_charge = 0
                    
                    for item in estimation_item_queryset:
                        total_gross_weight += item.gross_weight
                        total_net_weight += item.net_weight
                        total_net_amount += item.total_rate
                        total_making_charge += item.making_charge
                        wastage_percentage += int(item.wastage_percentage) if (item, 'wastage_percentage') != None else "---"
                        flat_wastage += float(item.flat_wastage) if (item, 'flat_wastage') != None else "---"
                        making_charge += float(item.making_charge) if (item, 'making_charge') != None else "---"
                        
                        flat_making_charge += float(item.flat_making_charge) if (item, 'flat_making_charge') != None else "---"
                        
                        bill_data['item_name']=item.item_details.item_name
                        bill_data['subitem_name']=item.sub_item_details.sub_item_name
                        bill_data['pieces'] = item.pieces
                        bill_data['gross_weight'] = item.gross_weight
                        bill_data['net_weight'] = item.net_weight
                        bill_data['net_amount'] = item.total_rate
                        bill_data['tag_number'] = item.tag_number
                        bill_data['metal_type'] = item.metal.metal_name
                        bill_data['wastage_percentage'] = wastage_percentage
                        bill_data['flat_wastage'] = flat_wastage
                        bill_data['making_charge'] = making_charge
                        bill_data['flat_making_charge'] = flat_making_charge
                        
                        taggedd_item_queryset = TaggedItems.objects.get(tag_number=item.tag_number)
                        bill_data['vendor_name'] = taggedd_item_queryset.tag_entry_details.lot_details.designer_name.account_head_name
                        bill_list.append(bill_data)
                    
                except Exception as err:
                    bill_data['item_name']= "--"
                    bill_data['subitem_name']="--"
                    bill_data['pieces'] = 0
                    bill_data['gross_weight'] = 0
                    bill_data['net_weight'] = 0
                    bill_data['net_amount'] = 0
                    bill_data['tag_number'] = "--"
                    bill_data['weight'] = 0
                    bill_data['amount'] = 0
                    bill_data['metal_type'] = "---"
                    bill_data['vendor_name'] = "---"
                    bill_list.append(bill_data)
                # total_advance_amount += queryset[i].advance_amount
                # totalamount += queryset[i].total_amount
            total_data['total_gross_weight'] = total_gross_weight
            total_data['total_net_weight'] = total_net_weight
            total_data['total_making_charge'] = total_making_charge
            total_data['total_net_amount'] = total_net_amount
            total_data['totalamount'] = totalamount
            total_data['total_advance_amount'] = total_advance_amount
            dict_data['billing_details'] = bill_list
            dict_data['total_data'] = total_data
            response_data.append(dict_data)
        return Response(
        {
            "data":{
                "list":response_data,
                "total_pages": paginated_data.num_pages,
                "current_page": page,
                "total_items": len(queryset),
                "current_items": len(serializer.data)
            },
            "message":res_msg.retrieve("Estimation Sale List"),
            "status":status.HTTP_200_OK
        },status=status.HTTP_200_OK
        )
    

# SALE ITEM COUNT AND WEIGHT REPORT
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ItemWiseSaleReport(APIView):
    def post(self,request):
        
        request_data=request.data
        
        from_date = request_data.get('from_date') if request_data.get('from_date') != None else None
        to_date = request_data.get('to_date') if request_data.get('to_date') != None else None
        item_name = request_data.get('item_name') if request_data.get('item_name') != None else None
        page = request_data.get('page') if request_data.get('page') else 1
        branch = request_data.get('branch') if request_data.get('branch') else None
        try:
            items_per_page = int(request_data.get('items_per_page', BillingTagItems.objects.all().count()))
            if items_per_page == 0:
                items_per_page = 10 
        except Exception as err:
            items_per_page = 10 
        
        filter_condition={}

        if request.user.role.is_admin == True:
            if branch != None :
                filter_condition['billing_details__branch'] = branch
        else:
            filter_condition['billing_details__branch'] = request.user.branch.pk

        if from_date != None and to_date != None :
            date_range=(from_date,to_date)
            filter_condition['created_at__range'] = date_range

        if item_name != None: 
            item_queryset = Item.objects.filter(id=item_name).order_by('-id')
        else:
            item_queryset = Item.objects.all().order_by('-id')
        
        paginated_data = Paginator(item_queryset, items_per_page)
        item_serializer = ItemSerializer(paginated_data.get_page(page), many=True)
        response_data=[]
        dict_data={}
        for i in range(0,len(item_serializer.data)):
            
            if len(filter_condition) != 0:
                queryset=BillingTagItems.objects.filter(**filter_condition,item_details=item_queryset[i].pk).order_by('-id')
                
            else:
                queryset=BillingTagItems.objects.filter(item_details=item_queryset[i].pk).order_by('-id')
            
            serializer = BillingTagItemsSerializer(queryset, many=True)
            qty = 0
            total_weight = 0
            for j in range(0,len(serializer.data)):
                dict_data = serializer.data[j]
                dict_data['metal_name'] = item_queryset[i].metal.metal_name
                dict_data['item_name'] = item_queryset[i].item_name
                qty += queryset[j].pieces
                total_weight += queryset[j].gross_weight

            dict_data['pieces']=qty
            dict_data['total_weight']=total_weight
            
            response_data.append(dict_data)
        
        return Response(
        {
            "data":{
                "list":response_data,
                "total_pages": paginated_data.num_pages,
                "current_page": page,
                "total_items": len(queryset),
                "current_items": len(queryset),
            },
            "message":res_msg.retrieve("Item Wise Sale Report"),
            "status":status.HTTP_200_OK
        },status=status.HTTP_200_OK
        )


# SALES DETAILS REPORT #
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class SalesDetailsReport(APIView):
    def post(self,request):
        
        request_data=request.data

        search=request_data.get('search') if request_data.get('search') else ''
        from_date = request_data.get('from_date') if request_data.get('from_date') != None else None
        to_date = request_data.get('to_date') if request_data.get('to_date') != None else None
        metal_type = request_data.get('metal_type') if request_data.get('metal_type') != None else None
        item_name = request_data.get('item_name') if request_data.get('item_name') != None else None
        page = request_data.get('page') if request_data.get('page') else 1
        branch = request_data.get('branch') if request_data.get('branch') else None
        items_per_page = request_data.get('items_per_page') if request_data.get('items_per_page') else 10
        
        filter_condition={}

        if request.user.role.is_admin == True:
            if branch != None :
                filter_condition['billing_details__branch'] = branch
        else:
            filter_condition['billing_details__branch'] = request.user.branch.pk
        
        if search != "":
            filter_condition['billing_details__bill_no'] = search

        if metal_type != None:
            filter_condition['metal'] = metal_type

        if from_date != None and to_date != None :
            date_range=(from_date,to_date)
            filter_condition['created_at__range'] = date_range

        item_queryset = Item.objects.all().order_by('-id')
        item_serializer = ItemSerializer(item_queryset,many=True)
        response_data = []
        
        for j in range(0,len(item_serializer.data)):
            dict_data = item_serializer.data[j]

            if item_name != None :
                item_details = item_name
            else:
                item_details = item_queryset[j].pk

            if len(filter_condition) != 0:

                queryset=BillingTagItems.objects.filter(**filter_condition,item_details=item_details).order_by('-id')
                
            else:

                queryset=BillingTagItems.objects.filter(item_details=item_details).order_by('-id')

            serializer = BillingTagItemsSerializer(queryset, many=True)
            
            bill_list = []
            wastage_percentage = 0
            flat_wastage = 0
            making_charge = 0
            flat_making_charge = 0
            
            total_gross_weight = 0
            total_net_weight = 0
            total_making_charge = 0
            total_net_amount = 0
            total_pieces = 0
            total_advance_amount = 0
            totalamount = 0
            total_data = {}
            for i in range(0, len(serializer.data)):
                bill_item_data = serializer.data[i]
                bill_item_data['bill_no']=queryset[i].billing_details.bill_no
                bill_item_data['bill_date']=queryset[i].billing_details.bill_date
                bill_item_data['total_amount']=queryset[i].billing_details.total_amount
                bill_item_data['tag_number']=queryset[i].billing_tag_item.tag_number
                bill_item_data['advance_amount']=queryset[i].billing_details.advance_amount
                bill_item_data['paid_amount']=queryset[i].billing_details.paid_amount
                bill_item_data['branch_name']=queryset[i].billing_details.branch.branch_name

                total_gross_weight += queryset[i].gross_weight
                total_net_weight += queryset[i].net_weight
                total_net_amount += queryset[i].total_rate
                total_pieces += queryset[i].pieces
                total_making_charge += queryset[i].making_charge
                wastage_percentage += int(queryset[i].wastage_percentage) if (queryset[i], 'wastage_percentage') != None else "---"
                flat_wastage += float(queryset[i].flat_wastage) if (queryset[i], 'flat_wastage') != None else "---"
                making_charge += float(queryset[i].making_charge) if (queryset[i], 'making_charge') != None else "---"
                flat_making_charge += float(queryset[i].flat_making_charge) if (queryset[i], 'flat_making_charge') != None else "---"
                
                # bill_item_data['total_weight'] = total_weight
                # bill_item_data['total_amount'] = total_amount
                bill_item_data['metal_type'] = queryset[i].metal.metal_name
                bill_item_data['wastage_percentage'] = wastage_percentage
                bill_item_data['flat_wastage'] = flat_wastage
                bill_item_data['making_charge'] = making_charge
                bill_item_data['flat_making_charge'] = flat_making_charge
                
                taggedd_item_queryset = TaggedItems.objects.get(tag_number=queryset[i].tag_number)
                bill_item_data['vendor_name'] = taggedd_item_queryset.tag_entry_details.lot_details.designer_name.account_head_name
                
                try:
                    
                    bill_item_data['sales_person']=queryset[i].billing_details.created_by.get_username()
                    bill_item_data['billing_person']=queryset[i].billing_details.created_by.get_username()
                except Exception as err:
                    bill_item_data['sales_person'] = "---"
                    bill_item_data['billing_person'] = "---"

                bill_list.append(bill_item_data)
                total_advance_amount += queryset[i].billing_details.advance_amount
                totalamount += queryset[i].billing_details.total_amount
            total_data['total_gross_weight'] = total_gross_weight
            total_data['total_net_weight'] = total_net_weight
            total_data['total_making_charge'] = total_making_charge
            total_data['total_net_amount'] = total_net_amount
            total_data['total_pieces'] = total_pieces
            # total_data['totalamount'] = totalamount
            # total_data['total_advance_amount'] = total_advance_amount
            
            dict_data['bill_details'] = bill_list
            dict_data['total_data'] = total_data
            response_data.append(dict_data)
        return Response(
        {
            "data":{
                "list":response_data,
                # "total_pages": paginated_data.num_pages,
                # "current_page": page,
                # "total_items": len(queryset),
                # "current_items": len(serializer.data)
            },
            "message":res_msg.retrieve("Sale Detail Report List"),
            "status":status.HTTP_200_OK
        },status=status.HTTP_200_OK
        )


# SALES RETURN REPORT #
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class SaleReturnReport(APIView):
    def post(self,request):
        
        request_data=request.data

        search=request_data.get('search') if request_data.get('search') else ''
        from_date = request_data.get('from_date') if request_data.get('from_date') != None else None
        to_date = request_data.get('to_date') if request_data.get('to_date') != None else None
        metal_type = request_data.get('metal_type') if request_data.get('metal_type') != None else None
        item_name = request_data.get('item_name') if request_data.get('item_name') != None else None
        page = request_data.get('page') if request_data.get('page') else 1
        branch = request_data.get('branch') if request_data.get('branch') else None
        items_per_page = request_data.get('items_per_page') if request_data.get('items_per_page') else 10
        
        filter_condition={}

        if request.user.role.is_admin == True:
            if branch != None :
                filter_condition['billing_details__branch'] = branch
        else:
            filter_condition['billing_details__branch'] = request.user.branch.pk
        
        if metal_type != None:
            filter_condition['metal'] = metal_type

        if item_name != None:
            filter_condition['item_details'] = item_name

        if from_date != None and to_date != None :
            date_range=(from_date,to_date)
            filter_condition['created_at__range'] = date_range

        response_data = []
        total_gross_weight = 0
        total_net_weight = 0
        total_net_amount = 0
        total_pieces = 0
        total_data = {}

        if len(filter_condition) != 0:
            queryset=BillingSaleReturnItems.objects.filter(**filter_condition).order_by('-id')
            
        else:
            queryset=BillingSaleReturnItems.objects.all().order_by('-id')

        paginated_data = Paginator(queryset, items_per_page)
        serializer = BillingSaleReturnItemsSerializer(paginated_data.get_page(page), many=True)
        
        bill_list = []
        dict_data = {}
        for i in range(0, len(serializer.data)):
            dict_data = serializer.data[i]
            bill_item_data = serializer.data[i]
            bill_item_data['bill_no']=queryset[i].billing_details.bill_no
            bill_item_data['bill_date']=queryset[i].billing_details.bill_date
            bill_item_data['branch_name']=queryset[i].billing_details.branch.branch_name
            bill_item_data['metal_type'] = queryset[i].metal.metal_name
            bill_item_data['item_name'] = queryset[i].item_details.item_name
            bill_item_data['customer_name'] = queryset[i].billing_details.customer_details.customer_name

            total_gross_weight += queryset[i].gross_weight
            total_net_weight += queryset[i].net_weight
            total_net_amount += queryset[i].total_rate
            total_pieces += queryset[i].pieces

            bill_list.append(bill_item_data)

        total_data['total_gross_weight'] = total_gross_weight
        total_data['total_net_weight'] = total_net_weight
        total_data['total_net_amount'] = total_net_amount
        total_data['total_pieces'] = total_pieces
        
        dict_data['bill_details'] = bill_list
        dict_data['total_data'] = total_data
        response_data.append(dict_data)
        return Response(
        {
            "data":{
                "list":response_data,
                "total_pages": paginated_data.num_pages,
                "current_page": page,
                "total_items": len(queryset),
                "current_items": len(serializer.data)
            },
            "message":res_msg.retrieve("Sale Return Report List"),
            "status":status.HTTP_200_OK
        },status=status.HTTP_200_OK
        )

# STOCK SUMMARY REPORT #
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class StockSummaryReport(APIView):
    def post(self,request):
        
        request_data=request.data

        search=request_data.get('search') if request_data.get('search') else ''
        from_date = request_data.get('from_date') if request_data.get('from_date') != None else None
        to_date = request_data.get('to_date') if request_data.get('to_date') != None else None
        metal_type = request_data.get('metal_type') if request_data.get('metal_type') != None else None
        item_name = request_data.get('item_name') if request_data.get('item_name') != None else None
        location = request_data.get('location') if request_data.get('location') != None else None
        page = request_data.get('page') if request_data.get('page') else 1
        branch = request_data.get('branch') if request_data.get('branch') else None
        try:
            items_per_page = int(request_data.get('items_per_page', TaggedItems.objects.all().count()))
            if items_per_page == 0:
                items_per_page = 10 
        except Exception as err:
            items_per_page = 10 
        
        filter_condition={}

        if request.user.role.is_admin == True:
            if branch != None :
                filter_condition['branch'] = branch
        else:
            filter_condition['branch'] = request.user.branch.pk

        if item_name != None :
            filter_condition['item_details'] = item_name

        if metal_type != None:
            filter_condition['metal'] = metal_type

        if location != None:
            filter_condition['sub_item_counter'] = location

        if from_date != None and to_date != None :
            date_range=(from_date,to_date)
            filter_condition['created_at__range'] = date_range

        if len(filter_condition) != 0:
            subitem_queryset = SubItem.objects.filter(**filter_condition).order_by('-id')
        else:
            subitem_queryset = SubItem.objects.all().order_by('-id')

        paginated_data = Paginator(subitem_queryset, items_per_page)
        serializer = SubItemSerializer(paginated_data.get_page(page), many=True)
        response_data = []
        for i in range(0, len(serializer.data)):
            dict_data = serializer.data[i]
            
            queryset=TaggedItems.objects.filter(sub_item_details=subitem_queryset[i].pk).order_by('-id')
                
            tagged_items_serializer = TaggedItemsSerializer(queryset, many=True)
            serialized_tagged_items = tagged_items_serializer.data

            dict_data['total_weight'] = queryset.aggregate(total_weight=Sum('gross_weight'))['total_weight'] or 0
            dict_data['counter'] = subitem_queryset[i].sub_item_counter.pk
            dict_data['floor'] = subitem_queryset[i].sub_item_counter.floor.floor_name
            dict_data['item_name'] = subitem_queryset[i].item_details.item_name
            dict_data['metal_name'] = subitem_queryset[i].metal.metal_name
            dict_data['total_stock'] = queryset.count()
            # in_stock
            in_stock = queryset.filter(is_billed=False)
            dict_data['in_stock'] = in_stock.count()

            response_data.append(dict_data)
        return Response(
        {
            "data":{
                "list":response_data,
                "total_pages": paginated_data.num_pages,
                "current_page": page,
                "total_items": len(subitem_queryset),
                "current_items": len(serializer.data)
            },
            "message":res_msg.retrieve("Stock Summary Report"),
            "status":status.HTTP_200_OK
        },status=status.HTTP_200_OK
        )
    

# STOCK SUMMARY REPORT #
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class TagWiseStockReport(APIView):
    def post(self,request):
        
        request_data=request.data

        search=request_data.get('search') if request_data.get('search') else None
        from_date = request_data.get('from_date') if request_data.get('from_date') != None else None
        to_date = request_data.get('to_date') if request_data.get('to_date') != None else None
        metal_type = request_data.get('metal_type') if request_data.get('metal_type') != None else None
        location = request_data.get('location') if request_data.get('location') != None else None
        page = request_data.get('page') if request_data.get('page') else 1
        branch = request_data.get('branch') if request_data.get('branch') else None
        try:
            items_per_page = int(request_data.get('items_per_page', TaggedItems.objects.all().count()))
            if items_per_page == 0:
                items_per_page = 10 
        except Exception as err:
            items_per_page = 10 
        
        filter_condition={}

        if request.user.role.is_admin == True:
            if branch != None :

                filter_condition['branch'] = branch
        else:
            filter_condition['branch'] = request.user.branch.pk

        if search != None:
            filter_condition['tag_number'] = search

        if metal_type != None:
            filter_condition['sub_item_details__metal'] = metal_type

        if location != None:
            filter_condition['sub_item_details__sub_item_counter'] = location

        if from_date != None and to_date != None :
            date_range=(from_date,to_date)
            filter_condition['created_at__range'] = date_range
        
        response_data = []
        
        if len(filter_condition) != 0:
            queryset=TaggedItems.objects.filter(**filter_condition).order_by('-id')
        
        else:
            queryset=TaggedItems.objects.all().order_by('-id')
        
        paginated_data = Paginator(queryset, items_per_page)
        serializer = TaggedItemsSerializer(paginated_data.get_page(page), many=True)
        
        for i in range(0, len(serializer.data)):
            dict_data = serializer.data[i]
            dict_data['item_name'] = queryset[i].item_details.item_details.item_name
            dict_data['subitem_name'] = queryset[i].sub_item_details.sub_item_name
            dict_data['metal_type'] = queryset[i].sub_item_details.metal.metal_name
            dict_data['counter'] = queryset[i].sub_item_details.sub_item_counter.pk

            response_data.append(dict_data)
        return Response(
        {
            "data":{
                "list":response_data,
                "total_pages": paginated_data.num_pages,
                "current_page": page,
                "total_items": len(queryset),
                "current_items": len(serializer.data)
            },
            "message":res_msg.retrieve("Tagwise Stock Report"),
            "status":status.HTTP_200_OK
        },status=status.HTTP_200_OK
        )
    

# LOT REPORT #
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class LotReport(APIView):
    def post(self,request):
        
        request_data=request.data

        search=request_data.get('search') if request_data.get('search') else ''
        from_date = request_data.get('from_date') if request_data.get('from_date') != None else None
        to_date = request_data.get('to_date') if request_data.get('to_date') != None else None
        vendor = request_data.get('vendor') if request_data.get('vendor') != None else None
        item_name = request_data.get('item_name') if request_data.get('item_name') != None else None
        page = request_data.get('page') if request_data.get('page') else 1
        branch = request_data.get('branch') if request_data.get('branch') else None
        try:
            items_per_page = int(request_data.get('items_per_page', LotItem.objects.all().count()))
            if items_per_page == 0:
                items_per_page = 10 
        except Exception as err:
            items_per_page = 10 
        
        filter_condition={}

        if request.user.role.is_admin == True:
            if branch != None :
                filter_condition['branch'] = branch
        else:
            filter_condition['branch'] = request.user.branch.pk

        if vendor != None:
            filter_condition['designer_name'] = vendor

        if item_name != None:
            filter_condition['item_name'] = item_name

        if from_date != None and to_date != None :
            date_range=(from_date,to_date)
            filter_condition['created_at__range'] = date_range
        
        response_data = []

        if len(filter_condition) != 0:
            queryset=Lot.objects.filter(**filter_condition).order_by('-id')
        
        else:
            queryset=Lot.objects.all().order_by('-id')
            
        paginated_data = Paginator(queryset, items_per_page)
        serializer = LotSerializer(paginated_data.get_page(page), many=True)

        for i in range(0, len(serializer.data)):
            dict_data = serializer.data[i]
            dict_data['vendor_name'] = queryset[i].designer_name.account_head_name

            response_data.append(dict_data)
        return Response(
        {
            "data":{
                "list":response_data,
                "total_pages": paginated_data.num_pages,
                "current_page": page,
                "total_items": len(queryset),
                "current_items": len(serializer.data)
            },
            "message":res_msg.retrieve("Tagwise Stock Report"),
            "status":status.HTTP_200_OK
        },status=status.HTTP_200_OK
        )
    

# PURCHASE REPORT #
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class PurchaseReport(APIView):
    def post(self,request):
        
        request_data=request.data

        search=request_data.get('search') if request_data.get('search') else ''
        from_date = request_data.get('from_date') if request_data.get('from_date') != None else None
        to_date = request_data.get('to_date') if request_data.get('to_date') != None else None
        vendor = request_data.get('vendor') if request_data.get('vendor') != None else None
        metal_type = request_data.get('metal_type') if request_data.get('metal_type') != None else None
        page = request_data.get('page') if request_data.get('page') else 1
        branch = request_data.get('branch') if request_data.get('branch') else None
        try:
            items_per_page = int(request_data.get('items_per_page', NewPurchaseItemdetail.objects.all().count()))
            if items_per_page == 0:
                items_per_page = 10 
        except Exception as err:
            items_per_page = 10 
        
        filter_condition={}

        if request.user.role.is_admin == True:
            if branch != None :
                filter_condition['purchase_order__branch'] = branch
        else:
            filter_condition['purchase_order__branch'] = request.user.branch.pk

        if vendor != None:
            filter_condition['purchase_order__designer_name'] = vendor

        if metal_type != None:
            filter_condition['metal'] = metal_type

        if from_date != None and to_date != None :
            date_range=(from_date,to_date)
            filter_condition['purchase_order__order_date__range'] = date_range
        
        response_data = []

        if len(filter_condition) != 0:
            queryset=NewPurchaseItemdetail.objects.filter(**filter_condition).order_by('-id')
        
        else:
            queryset=NewPurchaseItemdetail.objects.all().order_by('-id')
            
        paginated_data = Paginator(queryset, items_per_page)
        serializer = NewPurchaseItemdetailSerializer(paginated_data.get_page(page), many=True)

        for i in range(0, len(serializer.data)):
            dict_data = serializer.data[i]
            dict_data['purchase_order'] = queryset[i].purchase_order.purchase_order_id
            dict_data['date'] = queryset[i].purchase_order.order_date
            dict_data['vendor_name'] = queryset[i].purchase_order.designer_name.account_head_name
            dict_data['item_name'] = queryset[i].item.item_name

            response_data.append(dict_data)
        return Response(
        {
            "data":{
                "list":response_data,
                "total_pages": paginated_data.num_pages,
                "current_page": page,
                "total_items": len(queryset),
                "current_items": len(serializer.data)
            },
            "message":res_msg.retrieve("Purchase Report"),
            "status":status.HTTP_200_OK
        },status=status.HTTP_200_OK
        )
    

# VENDOR WISE PURCHASE REPORT #
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class VendorWisePurchaseReport(APIView):
    def post(self,request):
        
        request_data=request.data

        search=request_data.get('search') if request_data.get('search') else ''
        from_date = request_data.get('from_date') if request_data.get('from_date') != None else None
        to_date = request_data.get('to_date') if request_data.get('to_date') != None else None
        vendor = request_data.get('vendor') if request_data.get('vendor') != None else None
        page = request_data.get('page') if request_data.get('page') else 1
        branch = request_data.get('branch') if request_data.get('branch') else None
        try:
            items_per_page = int(request_data.get('items_per_page', AccountHeadDetails.objects.all().count()))
            if items_per_page == 0:
                items_per_page = 10 
        except Exception as err:
            items_per_page = 10 
        
        filter_condition={}

        if request.user.role.is_admin == True:
            if branch != None :
                filter_condition['branch'] = branch
        else:
            filter_condition['branch'] = request.user.branch.pk

        if vendor != None:
            filter_condition['purchase_order__designer_name'] = vendor

        if from_date != None and to_date != None :
            date_range=(from_date,to_date)
            filter_condition['purchase_order__order_date__range'] = date_range
        
        response_data = []

        vendor_queryset = AccountHeadDetails.objects.all().order_by('-id')
        vendor_serializer = AccountHeadDetailsSerailizer(vendor_queryset,many=True)

        for i in range(0,len(vendor_serializer.data)):
            vendor_data = vendor_serializer.data[i]
            newpurchase_queryset = NewPurchase.objects.filter(designer_name=vendor_queryset[i].pk)
            paginated_data = Paginator(newpurchase_queryset, items_per_page)
            newpurchase_serializer = NewPurchaseSerializer(paginated_data.get_page(page),many=True)

            for j in range(0,len(newpurchase_serializer.data)):
                dict_data = newpurchase_serializer.data[j]
                dict_data['vendor_name'] = newpurchase_queryset[j].designer_name.account_head_name
                if len(filter_condition) != 0:
                    queryset=NewPurchaseItemdetail.objects.filter(**filter_condition,purchase_order=newpurchase_queryset[j].pk).order_by('-id')
                
                else:
                    queryset=NewPurchaseItemdetail.objects.filter(purchase_order=newpurchase_queryset[j].pk).order_by('-id')
                    
                serializer = NewPurchaseItemdetailSerializer(queryset, many=True)

                item_list = []
                for i in range(0, len(serializer.data)):
                    item_data = serializer.data[i]
                    item_data['item_name'] = queryset[i].item.item_name
                    item_data['metal_name'] = queryset[i].metal.metal_name
                    item_data['purity'] = queryset[i].item.purity.pk
                    
                    item_list.append(item_data)
                dict_data['item_list'] = item_list

            response_data.append(dict_data)
        return Response(
        {
            "data":{
                "list":response_data,
                "total_pages": paginated_data.num_pages,
                "current_page": page,
                "total_items": len(queryset),
                "current_items": len(serializer.data)
            },
            "message":res_msg.retrieve("Purchase Report"),
            "status":status.HTTP_200_OK
        },status=status.HTTP_200_OK
        )
    

# VENDOR WISE PURCHASE REPORT #
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ItemWisePurchaseReport(APIView):
    def post(self,request):
        
        request_data=request.data

        search=request_data.get('search') if request_data.get('search') else ''
        from_date = request_data.get('from_date') if request_data.get('from_date') != None else None
        to_date = request_data.get('to_date') if request_data.get('to_date') != None else None
        item_name = request_data.get('item_name') if request_data.get('item_name') != None else None
        metal_type = request_data.get('metal_type') if request_data.get('metal_type') != None else None
        page = request_data.get('page') if request_data.get('page') else 1
        branch = request_data.get('branch') if request_data.get('branch') else None
        try:
            items_per_page = int(request_data.get('items_per_page', Item.objects.all().count()))
            if items_per_page == 0:
                items_per_page = 10 
        except Exception as err:
            items_per_page = 10 
        
        filter_condition={}

        if request.user.role.is_admin == True:
            if branch != None :
                filter_condition['purchase_order__branch'] = branch
        else:
            filter_condition['purchase_order__branch'] = request.user.branch.pk

        if from_date != None and to_date != None :
            date_range=(from_date,to_date)
            filter_condition['purchase_order__order_date__range'] = date_range

        item_filter_condition = {}
        if metal_type != None:
            item_filter_condition['metal'] = metal_type

        if item_name != None:
            item_filter_condition['id'] = item_name

        response_data = []
        total_pieces = 0
        total_weight = 0
        total_amount = 0
        if len(item_filter_condition) > 0:
            item_queryset = Item.objects.filter(**item_filter_condition).order_by('-id')
        else:
            item_queryset = Item.objects.all().order_by('-id')
        
        paginated_data = Paginator(item_queryset, items_per_page)
        item_serializer = ItemSerializer(paginated_data.get_page(page),many=True)

        for i in range(0,len(item_serializer.data)):
            dict_data = item_serializer.data[i]
            dict_data['metal_name'] = item_queryset[i].metal.metal_name
            
            if len(filter_condition) != 0:
                queryset=NewPurchaseItemdetail.objects.filter(**filter_condition,item=item_queryset[i].pk).order_by('-id')
            else:
                queryset=NewPurchaseItemdetail.objects.filter(item=item_queryset[i].pk).order_by('-id')

            serializer = NewPurchaseItemdetailSerializer(queryset,many=True)
            pieces = 0
            weight = 0
            for obj in range(0,len(serializer.data)):

                pieces +=  queryset[obj].pieces
                weight +=  queryset[obj].gross_weight

            dict_data['pieces'] = pieces
            dict_data['weight'] = weight

            total_pieces += dict_data['pieces']
            total_weight += dict_data['weight']
            
            response_data.append(dict_data)

        result_data = {}
        result_data['total_pieces'] = total_pieces
        result_data['total_weight'] = total_weight

        return Response(
        {
            "data":{
                "list":response_data,
                "total" : result_data,
                "total_pages": paginated_data.num_pages,
                "current_page": page,
                "total_items": len(item_queryset),
                "current_items": len(item_serializer.data)
            },
            "message":res_msg.retrieve("Item Wise Purchase Report"),
            "status":status.HTTP_200_OK
        },status=status.HTTP_200_OK
        )
    

# OLD PURCHASE REPORT #
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class OldPurchaseReport(APIView):
    def post(self,request):
        
        request_data=request.data

        search=request_data.get('search') if request_data.get('search') else ''
        from_date = request_data.get('from_date') if request_data.get('from_date') != None else None
        to_date = request_data.get('to_date') if request_data.get('to_date') != None else None
        item_name = request_data.get('item_name') if request_data.get('item_name') != None else None
        page = request_data.get('page') if request_data.get('page') else 1
        branch = request_data.get('branch') if request_data.get('branch') else None
        try:
            items_per_page = int(request_data.get('items_per_page', PurchaseEntry.objects.all().count()))
            if items_per_page == 0:
                items_per_page = 10 
        except Exception as err:
            items_per_page = 10 
        
        filter_condition={}

        if request.user.role.is_admin == True:
            if branch != None :
                filter_condition['branch'] = branch
        else:
            filter_condition['branch'] = request.user.branch.pk

        if from_date != None and to_date != None :
            date_range=(from_date,to_date)
            filter_condition['created_at__range'] = date_range
        
        response_data = []
        
        if len(filter_condition) != 0:
            queryset=PurchaseEntry.objects.filter(**filter_condition).order_by('-id')
        else:
            queryset=PurchaseEntry.objects.all().order_by('-id')
            
        paginated_data = Paginator(queryset, items_per_page)
        serializer = PurchaseEntrySerializer(paginated_data.get_page(page),many=True)

        for i in range(0, len(serializer.data)):
            dict_data = serializer.data[i]
            
            item_queryset=list(PurchaseItemDetail.objects.filter(purchaseentry=queryset[i].pk).order_by('-id'))
            item_serializer = PurchaseItemDetailSerializer(item_queryset,many=True)

            gold_weight = 0
            silver_weight = 0
            total_amount = 0
            gold_pieces = 0
            silver_pieces = 0
            for j in range(0,len(item_serializer.data)):
                item_data = item_serializer.data[j]
                
                if item_queryset[j].purchase_metal.pk == int(settings.GOLD):
                    gold_weight += item_queryset[j].gross_weight
                    gold_pieces += int(item_queryset[j].pieces)
                
                if item_queryset[j].purchase_metal.pk == int(settings.SILVER):
                    silver_weight += item_queryset[j].gross_weight
                    silver_pieces += int(item_queryset[j].pieces)
               
                total_amount += item_queryset[j].total_amount

                dict_data['silver_weight'] = silver_weight
                dict_data['gold_weight'] = gold_weight
                dict_data['gold_pieces'] = gold_pieces
                dict_data['silver_pieces'] = silver_pieces
                dict_data['totalamount'] = total_amount

            response_data.append(dict_data)

        return Response(
        {
            "data":{
                "list":response_data,
                "total_pages": paginated_data.num_pages,
                "current_page": page,
                "total_items": len(queryset),
                "current_items": len(serializer.data)
            },
            "message":res_msg.retrieve("Old Purchase Report"),
            "status":status.HTTP_200_OK
        },status=status.HTTP_200_OK
        )
    

# LOT REPORT #
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class VendorWiseLotReport(APIView):
    def post(self,request):
        
        request_data=request.data

        search=request_data.get('search') if request_data.get('search') else ''
        from_date = request_data.get('from_date') if request_data.get('from_date') != None else None
        to_date = request_data.get('to_date') if request_data.get('to_date') != None else None
        vendor = request_data.get('vendor') if request_data.get('vendor') != None else None
        item_name = request_data.get('item_name') if request_data.get('item_name') != None else None
        metal_type = request_data.get('metal_type') if request_data.get('metal_type') != None else None
        page = request_data.get('page') if request_data.get('page') else 1
        branch = request_data.get('branch') if request_data.get('branch') else None
        try:
            items_per_page = int(request_data.get('items_per_page', LotItem.objects.all().count()))
            if items_per_page == 0:
                items_per_page = 10 
        except Exception as err:
            items_per_page = 10 
        
        filter_condition={}

        if request.user.role.is_admin == True:
            if branch != None :
                filter_condition['branch'] = branch
        else:
            filter_condition['branch'] = request.user.branch.pk

        if vendor != None:
            filter_condition['designer_name'] = vendor

        if item_name != None:
            filter_condition['item_name'] = item_name

        if from_date != None and to_date != None :
            date_range=(from_date,to_date)
            filter_condition['created_at__range'] = date_range
        
        response_data = []

        vendor_queryset = AccountHeadDetails.objects.all().order_by('-id')
        vendor_serializer = AccountHeadDetailsSerailizer(vendor_queryset,many=True)

        for i in range(0,len(vendor_serializer.data)):
            dict_data = vendor_serializer.data[i]

            if len(filter_condition) != 0:
                queryset=LotItem.objects.filter(**filter_condition).order_by('-id')
            
            else:
                queryset=LotItem.objects.all().order_by('-id')
                
            paginated_data = Paginator(queryset, items_per_page)
            serializer = LotItemSerializer(paginated_data.get_page(page), many=True)
            
            gold_weight = 0
            gold_pieces = 0
            silver_weight = 0
            silver_pieces = 0
            item_list = []
            for j in range(0, len(serializer.data)):
                item_data = serializer.data[i]
                if queryset[j].item_details.metal.pk == int(settings.GOLD):
                    gold_weight += queryset[j].gross_weight
                    gold_pieces += int(queryset[j].pieces)
                
                if queryset[j].item_details.metal.pk == int(settings.SILVER):
                    silver_weight += queryset[j].gross_weight
                    silver_pieces += int(queryset[j].pieces)

                item_data['silver_weight'] = silver_weight
                item_data['gold_weight'] = gold_weight
                item_data['gold_pieces'] = gold_pieces
                item_data['silver_pieces'] = silver_pieces
                item_data['invoice'] = queryset[j].lot_details.invoice_number
                item_data['date'] = queryset[j].lot_details.entry_date
                item_data['lot_number'] = queryset[j].lot_details.lot_number

                item_list.append(item_data)
            dict_data['item_data'] = item_list
            response_data.append(dict_data)
        return Response(
        {
            "data":{
                "list":response_data,
                "total_pages": paginated_data.num_pages,
                "current_page": page,
                "total_items": len(queryset),
                "current_items": len(serializer.data)
            },
            "message":res_msg.retrieve("Tagwise Stock Report"),
            "status":status.HTTP_200_OK
        },status=status.HTTP_200_OK
        )
    

# CUSTOMER WISE REPAIR REPORT #
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class CustomerRepairIssueReport(APIView):
    def post(self,request):
        
        request_data=request.data

        search=request_data.get('search') if request_data.get('search') else ''
        from_date = request_data.get('from_date') if request_data.get('from_date') != None else None
        to_date = request_data.get('to_date') if request_data.get('to_date') != None else None
        metal_type = request_data.get('metal_type') if request_data.get('metal_type') != None else None
        customer_details = request_data.get('customer_details') if request_data.get('customer_details') != None else None
        page = request_data.get('page') if request_data.get('page') else 1
        branch = request_data.get('branch') if request_data.get('branch') else None
        items_per_page = request_data.get('items_per_page') if request_data.get('items_per_page') else 10
        
        filter_condition={}

        if request.user.role.is_admin == True:
            if branch != None :
                filter_condition['repair_details__branch'] = branch
        else:
            filter_condition['repair_details__branch'] = request.user.branch.pk

        if from_date != None and to_date != None :
            date_range=(from_date,to_date)
            filter_condition['created_at__range'] = date_range

        if customer_details != None :
            customer_queryset = Customer.objects.filter(id=customer_details).order_by('-id')
        else: 
            customer_queryset = Customer.objects.all().order_by('-id')
        paginated_data = Paginator(customer_queryset, items_per_page)
        customer_serializer = CustomerSerializer(paginated_data.get_page(page), many=True)

        response_data = []
        for j in customer_queryset:
            dict_data = {}
            dict_data['customer_name'] = j.customer_name

            if len(filter_condition) != 0:
                repair_issue_queryset=RepairOrderIssued.objects.filter(**filter_condition,repair_details__customer_details=j.pk).order_by('-id')
            else:
                repair_issue_queryset=RepairOrderIssued.objects.filter(repair_details__customer_details=j.pk).order_by('-id')

            issue_data = []
            repair_issue = {}
            for i in repair_issue_queryset:
                repair_issue['vendor_name'] = i.vendor_name.account_head_name
                repair_issue['repair_number'] = i.repair_details.repair_number
                repair_issue['repair_date'] = i.repair_details.repair_recived_date
                repair_issue['description'] = i.repair_details.description
                
                if metal_type != None:
                    queryset=RepairItemDetails.objects.filter(metal_details=metal_type).order_by('-id')

                else:
                    queryset=RepairItemDetails.objects.all().order_by('-id')

                for data in queryset:
                    repair_issue['metal_name'] = data.metal_details.metal_name
                    repair_issue['item_name'] = data.item_details.item_name
                    repair_issue['gross_weight'] = data.issued_gross_weight
                    repair_issue['net_weight'] = data.issued_net_weight
                    repair_issue['pieces'] = data.total_pieces
                    repair_issue['stone_count'] = data.old_stone
                    repair_issue['diamond_count'] = data.old_diamond

                    issue_data.append(repair_issue)

            dict_data['repair_data'] = issue_data

            response_data.append(dict_data)
        
        return Response(
        {
            "data":{
                "list":response_data,
                "total_pages": paginated_data.num_pages,
                "current_page": page,
                "total_items": len(customer_queryset),
                "current_items": len(customer_serializer.data)
            },
            "message":res_msg.retrieve("Customer wise Repair Issue Report"),
            "status":status.HTTP_200_OK
        },status=status.HTTP_200_OK
        )


# VENDOR WISE REPAIR REPORT #
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class VendorRepairIssueReport(APIView):
    def post(self,request):
        
        request_data=request.data

        search=request_data.get('search') if request_data.get('search') else ''
        from_date = request_data.get('from_date') if request_data.get('from_date') != None else None
        to_date = request_data.get('to_date') if request_data.get('to_date') != None else None
        metal_type = request_data.get('metal_type') if request_data.get('metal_type') != None else None
        vendor_details = request_data.get('vendor_details') if request_data.get('vendor_details') != None else None
        page = request_data.get('page') if request_data.get('page') else 1
        branch = request_data.get('branch') if request_data.get('branch') else None
        items_per_page = request_data.get('items_per_page') if request_data.get('items_per_page') else 10
        
        filter_condition={}

        if request.user.role.is_admin == True:
            if branch != None :
                filter_condition['repair_details__branch'] = branch
        else:
            filter_condition['repair_details__branch'] = request.user.branch.pk

        if from_date != None and to_date != None :
            date_range=(from_date,to_date)
            filter_condition['created_at__range'] = date_range

        if vendor_details != None :
            vendor_queryset = AccountHeadDetails.objects.filter(id=vendor_details).order_by('-id')
        else: 
            vendor_queryset = AccountHeadDetails.objects.all().order_by('-id')
        paginated_data = Paginator(vendor_queryset, items_per_page)
        vendor_serializer = AccountHeadDetailsSerailizer(paginated_data.get_page(page), many=True)

        response_data = []
        for j in vendor_queryset:
            dict_data = {}
            dict_data['vendor_name'] = j.account_head_name

            if len(filter_condition) != 0:
                repair_issue_queryset=RepairOrderIssued.objects.filter(**filter_condition,vendor_name=j.pk).order_by('-id')
            else:
                repair_issue_queryset=RepairOrderIssued.objects.filter(vendor_name=j.pk).order_by('-id')

            issue_data = []
            repair_issue = {}
            for i in repair_issue_queryset:
                repair_issue['repair_number'] = i.repair_details.repair_number
                repair_issue['issue_date'] = i.issue_date
                repair_issue['description'] = i.repair_details.description
                
                if metal_type != None:
                    queryset=RepairItemDetails.objects.filter(metal_details=metal_type).order_by('-id')

                else:
                    queryset=RepairItemDetails.objects.all().order_by('-id')

                for data in queryset:
                    repair_issue['metal_name'] = data.metal_details.metal_name
                    repair_issue['item_name'] = data.item_details.item_name
                    repair_issue['gross_weight'] = data.issued_gross_weight
                    repair_issue['net_weight'] = data.issued_net_weight
                    repair_issue['pieces'] = data.total_pieces
                    repair_issue['stone_count'] = data.old_stone
                    repair_issue['diamond_count'] = data.old_diamond

                    issue_data.append(repair_issue)

            dict_data['repair_data'] = issue_data

            response_data.append(dict_data)
        
        return Response(
        {
            "data":{
                "list":response_data,
                "total_pages": paginated_data.num_pages,
                "current_page": page,
                "total_items": len(vendor_queryset),
                "current_items": len(vendor_serializer.data)
            },
            "message":res_msg.retrieve("Vendor wise Repair Issue Report"),
            "status":status.HTTP_200_OK
        },status=status.HTTP_200_OK
        )


# MISC ISSUE DETAILS REPORT #
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class MiscDetailsReport(APIView):
    def post(self,request):
        
        request_data=request.data

        search=request_data.get('search') if request_data.get('search') else ''
        from_date = request_data.get('from_date') if request_data.get('from_date') != None else None
        to_date = request_data.get('to_date') if request_data.get('to_date') != None else None
        metal_type = request_data.get('metal_type') if request_data.get('metal_type') != None else None
        branch = request_data.get('branch') if request_data.get('branch') else None
        page = request_data.get('page') if request_data.get('page') else 1
        items_per_page = request_data.get('items_per_page') if request_data.get('items_per_page') else 10
        
        filter_condition={}

        if request.user.role.is_admin == True:
            if branch != None :
                filter_condition['misc_issue_details__branch'] = branch
        else:
            filter_condition['misc_issue_details__branch'] = request.user.branch.pk

        if from_date != None and to_date != None :
            date_range=(from_date,to_date)
            filter_condition['misc_issue_details__created_at__range'] = date_range

        if metal_type != None :
            filter_condition['tag_number__item_details__metal'] = metal_type

        if len(filter_condition) != 0:
            miscbilling_queryset = MiscParticulars.objects.filter(**filter_condition).order_by('-id')
        else:
            miscbilling_queryset = MiscParticulars.objects.all().order_by('-id')

        paginated_data = Paginator(miscbilling_queryset, items_per_page)
        serializer = MiscParticularsSerializer(paginated_data.get_page(page), many=True)

        response_data = []
        for i in range(0, len(serializer.data)):
            dict_data = serializer.data[i]
            dict_data['misc_issue_id'] = miscbilling_queryset[i].misc_issue_details.misc_issue_id.misc_issue_id
            dict_data['customer_name'] = miscbilling_queryset[i].misc_issue_details.customer.customer_name
            dict_data['issue_date'] = miscbilling_queryset[i].misc_issue_details.issue_date
            dict_data['branch_name'] = miscbilling_queryset[i].misc_issue_details.branch.branch_name
            dict_data['giver_name'] = miscbilling_queryset[i].misc_issue_details.giver_name
            dict_data['total_gross_weight'] = miscbilling_queryset[i].misc_issue_details.total_gross_weight
            dict_data['total_net_weight'] = miscbilling_queryset[i].misc_issue_details.total_net_weight
            dict_data['total_pieces'] = miscbilling_queryset[i].misc_issue_details.total_pieces
            dict_data['total_amount'] = miscbilling_queryset[i].misc_issue_details.total_amount
            dict_data['bill_amount'] = miscbilling_queryset[i].misc_issue_details.bill_amount   
            dict_data['net_amount'] = miscbilling_queryset[i].misc_issue_details.net_amount
            response_data.append(dict_data)
        
        return Response(
        {
            "data":{
                "list":response_data,
                "total_pages": paginated_data.num_pages,
                "current_page": page,
                "total_items": len(miscbilling_queryset),
                "current_items": len(serializer.data)
            },
            "message":res_msg.retrieve("Misc Billing Report"),
            "status":status.HTTP_200_OK
        },status=status.HTTP_200_OK
        )


# MISC ISSUE DETAILS REPORT #
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class MiscDetailsReport(APIView):
    def post(self,request):
        
        request_data=request.data

        search=request_data.get('search') if request_data.get('search') else ''
        from_date = request_data.get('from_date') if request_data.get('from_date') != None else None
        to_date = request_data.get('to_date') if request_data.get('to_date') != None else None
        metal_type = request_data.get('metal_type') if request_data.get('metal_type') != None else None
        branch = request_data.get('branch') if request_data.get('branch') else None
        page = request_data.get('page') if request_data.get('page') else 1
        items_per_page = request_data.get('items_per_page') if request_data.get('items_per_page') else 10
        
        filter_condition={}

        if request.user.role.is_admin == True:
            if branch != None :
                filter_condition['misc_issue_details__branch'] = branch
        else:
            filter_condition['misc_issue_details__branch'] = request.user.branch.pk

        if from_date != None and to_date != None :
            date_range=(from_date,to_date)
            filter_condition['misc_issue_details__created_at__range'] = date_range

        if metal_type != None :
            filter_condition['tag_number__item_details__metal'] = metal_type

        if len(filter_condition) != 0:
            miscbilling_queryset = MiscParticulars.objects.filter(**filter_condition).order_by('-id')
        else:
            miscbilling_queryset = MiscParticulars.objects.all().order_by('-id')

        paginated_data = Paginator(miscbilling_queryset, items_per_page)
        serializer = MiscParticularsSerializer(paginated_data.get_page(page), many=True)

        response_data = []
        for i in range(0, len(serializer.data)):
            dict_data = serializer.data[i]
            dict_data['misc_issue_id'] = miscbilling_queryset[i].misc_issue_details.misc_issue_id.misc_issue_id
            dict_data['customer_name'] = miscbilling_queryset[i].misc_issue_details.customer.customer_name
            dict_data['issue_date'] = miscbilling_queryset[i].misc_issue_details.issue_date
            dict_data['branch_name'] = miscbilling_queryset[i].misc_issue_details.branch.branch_name
            dict_data['giver_name'] = miscbilling_queryset[i].misc_issue_details.giver_name
            dict_data['total_gross_weight'] = miscbilling_queryset[i].misc_issue_details.total_gross_weight
            dict_data['total_net_weight'] = miscbilling_queryset[i].misc_issue_details.total_net_weight
            dict_data['total_pieces'] = miscbilling_queryset[i].misc_issue_details.total_pieces
            dict_data['total_amount'] = miscbilling_queryset[i].misc_issue_details.total_amount
            dict_data['bill_amount'] = miscbilling_queryset[i].misc_issue_details.bill_amount   
            dict_data['net_amount'] = miscbilling_queryset[i].misc_issue_details.net_amount
            response_data.append(dict_data)
        
        return Response(
        {
            "data":{
                "list":response_data,
                "total_pages": paginated_data.num_pages,
                "current_page": page,
                "total_items": len(miscbilling_queryset),
                "current_items": len(serializer.data)
            },
            "message":res_msg.retrieve("Misc Billing Report"),
            "status":status.HTTP_200_OK
        },status=status.HTTP_200_OK
        )


# MISC ISSUE DETAILS REPORT #
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ApprovalIssueReport(APIView):
    def post(self,request):
        
        request_data=request.data

        search=request_data.get('search') if request_data.get('search') else ''
        from_date = request_data.get('from_date') if request_data.get('from_date') != None else None
        to_date = request_data.get('to_date') if request_data.get('to_date') != None else None
        metal_type = request_data.get('metal_type') if request_data.get('metal_type') != None else None
        branch = request_data.get('branch') if request_data.get('branch') else None
        page = request_data.get('page') if request_data.get('page') else 1
        items_per_page = request_data.get('items_per_page') if request_data.get('items_per_page') else 10
        
        filter_condition={}

        if request.user.role.is_admin == True:
            if branch != None :
                filter_condition['approval_issue_details__branch'] = branch
        else:
            filter_condition['approval_issue_details__branch'] = request.user.branch.pk

        if from_date != None and to_date != None :
            date_range=(from_date,to_date)
            filter_condition['approval_issue_details__created_at__range'] = date_range

        if metal_type != None :
            filter_condition['tag_details__item_details__metal'] = metal_type

        if len(filter_condition) != 0:
            approval_issue_queryset = ApprovalIssueTagItems.objects.filter(**filter_condition).order_by('-id')
        else:
            approval_issue_queryset = ApprovalIssueTagItems.objects.all().order_by('-id')

        paginated_data = Paginator(approval_issue_queryset, items_per_page)
        serializer = ApprovalIssueTagItemsSerializer(paginated_data.get_page(page), many=True)

        response_data = []
        for i in range(0, len(serializer.data)):
            dict_data = serializer.data[i]
            dict_data['approval_issue_id'] = approval_issue_queryset[i].approval_issue_details.approval_issue_id
            dict_data['bill_type'] = approval_issue_queryset[i].approval_issue_details.bill_type.bill_type_name
            dict_data['issue_date'] = approval_issue_queryset[i].approval_issue_details.issue_date
            dict_data['branch_name'] = approval_issue_queryset[i].approval_issue_details.branch.branch_name
            dict_data['shop_name'] = approval_issue_queryset[i].approval_issue_details.shop_name.customer_name
            dict_data['receiver_name'] = approval_issue_queryset[i].approval_issue_details.receiver_name
            dict_data['issued_gross_weight'] = approval_issue_queryset[i].approval_issue_details.issued_gross_weight
            dict_data['issued_net_weight'] = approval_issue_queryset[i].approval_issue_details.issued_net_weight
            dict_data['recieved_date'] = approval_issue_queryset[i].approval_issue_details.recieved_date
            dict_data['received_by'] = approval_issue_queryset[i].approval_issue_details.received_by   
            dict_data['net_amount'] = approval_issue_queryset[i].approval_issue_details.received_gross_weight
            dict_data['received_gross_weight'] = approval_issue_queryset[i].approval_issue_details.received_net_weight   
            dict_data['received_net_weight'] = approval_issue_queryset[i].approval_issue_details.sold_gross_weight   
            dict_data['sold_net_weight'] = approval_issue_queryset[i].approval_issue_details.sold_net_weight   
            dict_data['status'] = approval_issue_queryset[i].approval_issue_details.status.status_name   

            response_data.append(dict_data)
        
        return Response(
        {
            "data":{
                "list":response_data,
                "total_pages": paginated_data.num_pages,
                "current_page": page,
                "total_items": len(approval_issue_queryset),
                "current_items": len(serializer.data)
            },
            "message":res_msg.retrieve("Approval Issue Report"),
            "status":status.HTTP_200_OK
        },status=status.HTTP_200_OK
        )


# MISC ISSUE DETAILS REPORT #
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ItemWiseMonthlySalesReport(APIView):
    def post(self,request):
        
        request_data=request.data

        search=request_data.get('search') if request_data.get('search') else ''
        from_yeaar = request_data.get('from_yeaar') if request_data.get('from_yeaar') != None else None
        to_year = request_data.get('to_year') if request_data.get('to_year') != None else None
        metal_type = request_data.get('metal_type') if request_data.get('metal_type') != None else None
        item = request_data.get('item') if request_data.get('item') else None
        branch = request_data.get('branch') if request_data.get('branch') else None
        page = request_data.get('page') if request_data.get('page') else 1
        items_per_page = request_data.get('items_per_page') if request_data.get('items_per_page') else 10
        
        filter_condition={}

        if request.user.role.is_admin == True:
            if branch != None :
                filter_condition['billing_details__branch'] = branch
        else:
            filter_condition['billing_details__branch'] = request.user.branch.pk

        if from_yeaar != None and to_year != None :
            date_range=(from_yeaar,to_year)
            filter_condition['billing_details__bill_date__year__gte'] = from_yeaar
            filter_condition['billing_details__bill_date__year__lte'] = to_year

        if metal_type != None :
            filter_condition['metal'] = metal_type

        item_queryset = Item.objects.all().order_by('-id')

        paginated_data = Paginator(item_queryset, items_per_page)
        item_serializer = ItemSerializer(paginated_data.get_page(page), many=True)

        for data in range(0, len(item_serializer.data)):

            if item != None :
                filter_condition['item_details'] = item
            else:
                filter_condition['item_details'] = item_queryset[data].pk

            if len(filter_condition) != 0:
                billing_queryset = BillingTagItems.objects.filter(**filter_condition).annotate(month=TruncMonth('billing_details__bill_date')).values('month').annotate(total_gross_weight=Count('gross_weight'), toal_amount=Sum('billing_details__paid_amount')).order_by('-id')

            else:
                billing_queryset = BillingTagItems.objects.all().order_by('-id').annotate(month=TruncMonth('billing_details__bill_date')).values('month').annotate(total_gross_weight=Count('gross_weight'), toal_amount=Sum('billing_details__paid_amount')).order_by('-id')

            response_data = []
            for entry in billing_queryset:
                dict_data = []
                dict_data['month'] = entry['month']
                dict_data['total_gross_weight'] = entry['total_gross_weight']
                dict_data['toal_amount'] = entry['toal_amount']
                
                response_data.append(dict_data)
            
        return Response(
        {
            "data":{
                "list":response_data,
                "total_pages": paginated_data.num_pages,
                "current_page": page,
                "total_items": len(item_queryset),
                "current_items": len(item_serializer.data)
            },
            "message":res_msg.retrieve("Item Wise Monthly Sale Report"),
            "status":status.HTTP_200_OK
        },status=status.HTTP_200_OK
        )
    


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class PaymentListView(APIView):
    def post(self, request):

        combined_data = []
        
        if type != None:
            if int(type) == settings.BILLING_PAYMENT:
                sales_queryset = BillingDetails.objects.all().order_by('-id')
                sales_serializer = BillingDetailsSerializer(sales_queryset, many=True)

                for i in range(len(sales_serializer.data)):
                    dict_data = sales_serializer.data[i]
                    dict_data['date'] = sales_queryset[i].bill_date
                    dict_data['order_no'] = sales_queryset[i].bill_no
                    dict_data['type'] = 3
                    try:
                        bill_item_queryset = BillingTagItems.objects.get(billing_details=sales_queryset[i].pk)
                        dict_data['item_name'] = bill_item_queryset.item_details.item_name
                        dict_data['gross_weight'] = bill_item_queryset.gross_weight
                        dict_data['net_weight'] = bill_item_queryset.net_weight
                    except:
                        dict_data['item_name'] = "---"
                        dict_data['gross_weight'] = 0
                        dict_data['net_weight'] = 0

                    try:
                        payment_queryset = CommonPaymentDetails.objects.get(refference_number=sales_queryset[i].bill_no)
                        dict_data['total_amount'] = payment_queryset.payable_amount
                        dict_data['balance_amount'] = payment_queryset.balance_amount
                    except:
                        dict_data['total_amount'] = 0
                        dict_data['balance_amount'] = 0

                    paid_amount = CustomerPaymentTabel.objects.filter(refference_number=sales_queryset[i].bill_no).aggregate(total_paid=Sum('paid_amount'))
                    dict_data['paid_amount'] = paid_amount['total_paid'] if paid_amount['total_paid'] else 0
                    
                    if dict_data['total_amount'] == dict_data['paid_amount'] and dict_data['total_amount'] > 0 and dict_data['paid_amount'] > 0:
                        dict_data['pay_status'] = "Done"
                    elif dict_data['balance_amount'] > 0:
                        dict_data['pay_status'] = "Pay now"
                    
                    combined_data.append(dict_data)
                
            elif int(type) == settings.ORDER_PAYMENT:
                
                sales_order_queryset = OrderDetails.objects.filter(customer=customer).order_by('-id')
                sales_order_serializer = OrderDetailsSerializer(sales_order_queryset, many=True)

                for i in range(len(sales_order_serializer.data)):
                    dict_data = sales_order_serializer.data[i]
                    dict_data['date'] = sales_order_queryset[i].order_date
                    dict_data['order_no'] = sales_order_queryset[i].order_id.order_id
                    dict_data['type'] = 1
                    try:
                        order_item_queryset = OrderItemDetails.objects.get(order_id=sales_order_queryset[i].pk)
                        dict_data['item_name'] = order_item_queryset.item.item_name
                        dict_data['gross_weight'] = order_item_queryset.gross_weight
                        dict_data['net_weight'] = order_item_queryset.net_weight
                        
                    except:
                        dict_data['item_name'] = "---"
                        dict_data['gross_weight'] = "---"
                        dict_data['net_weight'] = "---"

                    try:
                        payment_queryset = CommonPaymentDetails.objects.get(refference_number=sales_order_queryset[i].order_id.order_id)
                        dict_data['total_amount'] = payment_queryset.payable_amount
                        dict_data['balance_amount'] = payment_queryset.balance_amount
                    except:
                        dict_data['total_amount'] = 0
                        dict_data['balance_amount'] = 0

                    paid_amount = CustomerPaymentTabel.objects.filter(refference_number=sales_order_queryset[i].order_id.order_id).aggregate(total_paid=Sum('paid_amount'))
                    dict_data['paid_amount'] = paid_amount['total_paid'] if paid_amount['total_paid'] else 0

                    if dict_data['total_amount'] == dict_data['paid_amount'] and dict_data['total_amount'] > 0 and dict_data['paid_amount'] > 0:
                        dict_data['pay_status'] = "Done"
                    elif dict_data['balance_amount'] > 0:
                        dict_data['pay_status'] = "Pay now"

                    combined_data.append(dict_data)
            
                
            elif int(type) == settings.REPAIR_PAYMENT:
                repair_queryset = RepairDetails.objects.filter(customer_details=customer).order_by('-id')
                
                repair_serializer = RepairDetailsSerializer(repair_queryset, many=True)
                
                for i in range(len(repair_serializer.data)):
                    dict_data = repair_serializer.data[i]
                    dict_data['date'] = repair_queryset[i].repair_recived_date
                    dict_data['order_no'] = repair_queryset[i].repair_number
                    dict_data['type'] = 2
                    try:
                        repair_item_queryset = RepairItemDetails.objects.get(repair_order_details=repair_queryset[i].pk)
                        dict_data['item_name'] = repair_item_queryset.item_details.item_name
                        dict_data['gross_weight'] = repair_item_queryset.issued_gross_weight
                        dict_data['net_weight'] = repair_item_queryset.issued_net_weight
                        
                    except:
                        dict_data['item_name'] = "---"
                        dict_data['gross_weight'] = "---"
                        dict_data['net_weight'] = "---"
                        
                    try:
                        payment_queryset = CommonPaymentDetails.objects.get(refference_number=repair_queryset[i].repair_number)
                        dict_data['total_amount'] = payment_queryset.payable_amount
                        dict_data['balance_amount'] = payment_queryset.balance_amount
                    except:
                        dict_data['total_amount'] = 0
                        dict_data['balance_amount'] = 0

                    paid_amount = CustomerPaymentTabel.objects.filter(refference_number=repair_queryset[i].repair_number).aggregate(total_paid=Sum('paid_amount'))
                    dict_data['paid_amount'] = paid_amount['total_paid'] if paid_amount['total_paid'] else 0
                    
                    if dict_data['total_amount'] == dict_data['paid_amount'] and dict_data['total_amount'] > 0 and dict_data['paid_amount'] > 0:
                        dict_data['pay_status'] = "Done"
                    elif dict_data['balance_amount'] > 0:
                        dict_data['pay_status'] = "Pay now"

                    combined_data.append(dict_data)

        customer_list.append(customer_data) # type: ignore
        return Response({
            "data": {
                "customer_list" : customer_list, # type: ignore
                "list": combined_data,
            },
            "message": res_msg.retrieve('Customer Payment List'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
    

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class CommonPaymentReportListView(APIView):    

    def post(self, request):
        
        from_date = request.data.get('from_date') if request.data.get('from_date') else None
        to_date = request.data.get('to_date') if request.data.get('to_date') else None
        customer = request.data.get('customer') if request.data.get('customer') else None
        branch = request.data.get('branch') if request.data.get('branch') else None
        page= request.data.get('page') if request.data.get('page') else 1
        items_per_page = request.data.get('items_per_page') if request.data.get('items_per_page') else 10
        type = request.data.get('type') if request.data.get('type') else None

        # from_date = datetime.strptime(fromdate, '%Y-%m-%d') if fromdate else None
        # to_date = datetime.strptime(todate, '%Y-%m-%d') if todate else None

        filter_condition={}
        bill_customer_filter ={}
        order_customer_filter={}
        if customer != None:
            bill_customer_filter['customer_details'] = customer
            order_customer_filter['customer'] = customer
        if from_date and to_date != None:
            date_range = (from_date,to_date)
            filter_condition['created_at__range'] = date_range
        
        if request.user.role.is_admin == True:
            if branch != None :
                filter_condition['branch'] = branch
        else:
            filter_condition['branch'] = request.user.branch.pk

        
        combined_data = []
        if type != None:
            if int(type) == settings.BILLING_PAYMENT:
               
                if len(filter_condition)!= 0:                    
                    queryset = BillingDetails.objects.filter(**filter_condition,**bill_customer_filter).order_by('-id')
                else:
                    queryset = BillingDetails.objects.all().order_by('-id')

                paginated_data = Paginator(queryset, items_per_page)                
                serializer = BillingDetailsSerializer(paginated_data.get_page(page), many=True)
                for i in range(len(serializer.data)):
                    dict_data = serializer.data[i]
                    sales_queryset = BillingDetails.objects.get(id=dict_data['id'])
                    dict_data['date'] = sales_queryset.bill_date
                    dict_data['order_no'] = sales_queryset.bill_no
                    dict_data['type_name'] = "Sales"
                    dict_data['type'] = 3
                    dict_data['customer_name'] = sales_queryset.customer_details.customer_name
                    dict_data['customer_mobile'] = sales_queryset.customer_details.phone
                    dict_data['payment_status_name'] = sales_queryset.payment_status.status_name
                    
                    try:
                        payment_queryset = CommonPaymentDetails.objects.get(refference_number=sales_queryset.bill_no)
                        dict_data['amount'] = payment_queryset.payable_amount
                        dict_data['balance'] = payment_queryset.balance_amount
                    except:
                        dict_data['amount'] = 0
                        dict_data['balance'] = 0

                    paid_amount = CustomerPaymentTabel.objects.filter(refference_number=sales_queryset.bill_no).aggregate(total_paid=Sum('paid_amount'))
                    try:
                        last_paid_date = CustomerPaymentTabel.objects.filter(refference_number=sales_queryset.bill_no).order_by('-id').first()
                        dict_data['last_paid_date'] = last_paid_date.payment_date
                    except: 
                        dict_data['last_paid_date'] = None
                    dict_data['paid_amount'] = paid_amount['total_paid'] if paid_amount['total_paid'] else 0
                    dict_data['cr_dr'] = "CR"

                    if dict_data['amount'] == dict_data['paid_amount'] and dict_data['amount'] > 0 and dict_data['paid_amount'] > 0:
                        dict_data['pay_status'] = "Received"
                    elif dict_data['balance'] > 0:
                        dict_data['pay_status'] = "Pending"
                    combined_data.append(dict_data)
                
            elif int(type) == settings.ORDER_PAYMENT:
                
                if len(filter_condition)!= 0:  
                    queryset = OrderDetails.objects.filter(**filter_condition,**order_customer_filter).order_by('-id')
                else:
                    queryset = OrderDetails.objects.all().order_by('-id')
               

                paginated_data = Paginator(queryset, items_per_page)                
                serializer = OrderDetailsSerializer(paginated_data.get_page(page), many=True)

                for i in range(len(serializer.data)):
                    
                    dict_data = serializer.data[i]                    
                    sales_order_queryset = OrderDetails.objects.get(id=dict_data['id'])
                    dict_data['date'] = sales_order_queryset.order_date
                    dict_data['order_no'] = sales_order_queryset.order_id.order_id
                    dict_data['type_name'] = "Order"
                    dict_data['type'] = 1
                    dict_data['customer_name'] = sales_order_queryset.customer.customer_name
                    dict_data['customer_details'] = sales_order_queryset.customer.pk
                    dict_data['customer_mobile'] = sales_order_queryset.customer.phone
                    dict_data['payment_status_name'] = sales_order_queryset.payment_status.status_name
                    try:
                        payment_queryset = CommonPaymentDetails.objects.get(refference_number=sales_order_queryset.order_id.order_id)
                        dict_data['amount'] = payment_queryset.payable_amount
                        dict_data['balance'] = payment_queryset.balance_amount
                    except:
                        dict_data['amount'] = 0
                        dict_data['balance'] = 0

                    paid_amount = CustomerPaymentTabel.objects.filter(refference_number=sales_order_queryset.order_id.order_id).aggregate(total_paid=Sum('paid_amount'))
                    try:
                        last_paid_date = CustomerPaymentTabel.objects.filter(refference_number=sales_order_queryset.order_id.order_id).order_by('-id').first()
                        dict_data['last_paid_date'] = last_paid_date.payment_date
                    except: 
                        dict_data['last_paid_date'] = None
                    dict_data['paid_amount'] = paid_amount['total_paid'] if paid_amount['total_paid'] else 0
                    dict_data['cr_dr'] = "CR"

                    if dict_data['amount'] == dict_data['paid_amount'] and dict_data['amount'] > 0 and dict_data['paid_amount'] > 0:
                        dict_data['pay_status'] = "Received"
                    elif dict_data['balance'] > 0:
                        dict_data['pay_status'] = "Pending"

                    combined_data.append(dict_data)
                    
                
            elif int(type) == settings.REPAIR_PAYMENT:
                
                if len(filter_condition)!= 0:      
                
                    queryset = RepairDetails.objects.filter(**filter_condition,**bill_customer_filter).order_by('-id')
                else:
                    queryset = RepairDetails.objects.all().order_by('-id')
                

                paginated_data = Paginator(queryset, items_per_page)                
                serializer = RepairDetailsSerializer(paginated_data.get_page(page), many=True)
                
                for i in range(len(serializer.data)):
                    dict_data = serializer.data[i]
                    repair_queryset = RepairDetails.objects.get(id=dict_data['id'])
                    dict_data['date'] = repair_queryset.repair_recived_date
                    dict_data['order_no'] = repair_queryset.repair_number
                    dict_data['type_name'] = "Repair"
                    dict_data['type'] = 2
                    dict_data['customer_name'] = repair_queryset.customer_details.customer_name
                    dict_data['customer_mobile'] = repair_queryset.customer_details.phone
                    dict_data['payment_status_name'] = repair_queryset.payment_status.status_name
                    
                    try:
                        payment_queryset = CommonPaymentDetails.objects.get(refference_number=repair_queryset.repair_number)
                        dict_data['amount'] = payment_queryset.payable_amount
                        dict_data['balance'] = payment_queryset.balance_amount
                    except:
                        dict_data['amount'] = 0
                        dict_data['balance'] = 0

                    paid_amount = CustomerPaymentTabel.objects.filter(refference_number=repair_queryset.repair_number).aggregate(total_paid=Sum('paid_amount'))
                    try:
                        last_paid_date = CustomerPaymentTabel.objects.filter(refference_number=repair_queryset.repair_number).order_by('-id').first()
                        dict_data['last_paid_date'] = last_paid_date.payment_date
                    except: 
                        dict_data['last_paid_date'] = None
                    dict_data['paid_amount'] = paid_amount['total_paid'] if paid_amount['total_paid'] else 0
                    dict_data['cr_dr'] = "CR"

                    if dict_data['amount'] == dict_data['paid_amount'] and dict_data['amount'] > 0 and dict_data['paid_amount'] > 0:
                        dict_data['pay_status'] = "Received"
                    elif dict_data['balance'] > 0:
                        dict_data['pay_status'] = "Pending"
                    combined_data.append(dict_data)
            
        else:
            queryset = CommonPaymentDetails.objects.all().order_by('-id')
            paginated_data = Paginator(queryset, items_per_page)                
            serializer = CommonPaymentSerializer(paginated_data.get_page(page), many=True)
                     
            
            for i in range(len(serializer.data)):
                pay=serializer.data[i]
                sales_queryset = BillingDetails.objects.filter(bill_no=pay['refference_number'],**filter_condition,**bill_customer_filter).order_by('-id')
                sales_order_queryset = OrderDetails.objects.filter(order_id__order_id =pay['refference_number'],**filter_condition,**order_customer_filter).order_by('-id')
                repair_queryset = RepairDetails.objects.filter(repair_number=pay['refference_number'],**filter_condition,**bill_customer_filter).order_by('-id')
           
            
                if sales_queryset:
                    sales_serializer = BillingDetailsSerializer(sales_queryset, many=True)
                    for i in range(len(sales_serializer.data)):
                        dict_data = sales_serializer.data[i]
                        detail_queryset = BillingDetails.objects.get(id=dict_data['id'])
                        dict_data['date'] = detail_queryset.bill_date
                        dict_data['order_no'] = detail_queryset.bill_no
                        dict_data['type_name'] = "Sales"
                        dict_data['type'] = 3
                        dict_data['customer_name'] = detail_queryset.customer_details.customer_name
                        dict_data['payment_status_name'] = detail_queryset.payment_status.status_name
                        try:
                            payment_queryset = CommonPaymentDetails.objects.get(refference_number=detail_queryset.bill_no)
                            dict_data['amount'] = payment_queryset.payable_amount
                            dict_data['balance'] = payment_queryset.balance_amount
                        except:
                            dict_data['amount'] = 0
                            dict_data['balance'] = 0

                        paid_amount = CustomerPaymentTabel.objects.filter(refference_number=detail_queryset.bill_no).aggregate(total_paid=Sum('paid_amount'))
                        try:
                            last_paid_date = CustomerPaymentTabel.objects.filter(refference_number=detail_queryset.bill_no).order_by('-id').first()
                            dict_data['last_paid_date'] = last_paid_date.payment_date
                        except: 
                            dict_data['last_paid_date'] = None

                        dict_data['paid_amount'] = paid_amount['total_paid'] if paid_amount['total_paid'] else 0
                        dict_data['cr_dr'] = "CR"

                        if dict_data['amount'] == dict_data['paid_amount'] and dict_data['amount'] > 0 and dict_data['paid_amount'] > 0:
                            dict_data['pay_status'] = "Received"
                        elif dict_data['balance'] > 0:
                            dict_data['pay_status'] = "Pending"
                        combined_data.append(dict_data)
                if sales_order_queryset:
                    sales_order_serializer = OrderDetailsSerializer(sales_order_queryset, many=True)
                    for i in range(len(sales_order_serializer.data)):
                        dict_data = sales_order_serializer.data[i]
                        detail_queryset = OrderDetails.objects.get(id=dict_data['id'])
                        dict_data['date'] = detail_queryset.order_date
                        dict_data['order_no'] = detail_queryset.order_id.order_id
                        dict_data['type_name'] = "Order"
                        dict_data['type'] = 1
                        dict_data['customer_name'] = detail_queryset.customer.customer_name
                        dict_data['customer_details'] = detail_queryset.customer.pk
                        dict_data['payment_status_name'] = detail_queryset.payment_status.status_name
                        try:
                            payment_queryset = CommonPaymentDetails.objects.get(refference_number=detail_queryset.order_id.order_id)
                            dict_data['amount'] = payment_queryset.payable_amount
                            dict_data['balance'] = payment_queryset.balance_amount
                        except:
                            dict_data['amount'] = 0
                            dict_data['balance'] = 0

                        paid_amount = CustomerPaymentTabel.objects.filter(refference_number=detail_queryset.order_id.order_id).aggregate(total_paid=Sum('paid_amount'))
                        
                        try:
                            last_paid_date = CustomerPaymentTabel.objects.filter(refference_number=detail_queryset.order_id.order_id).order_by('-id').first()
                            dict_data['last_paid_date'] = last_paid_date.payment_date
                        except: 
                            dict_data['last_paid_date'] = None

                        dict_data['paid_amount'] = paid_amount['total_paid'] if paid_amount['total_paid'] else 0
                        dict_data['cr_dr'] = "CR"

                        if dict_data['amount'] == dict_data['paid_amount'] and dict_data['amount'] > 0 and dict_data['paid_amount'] > 0:
                            dict_data['pay_status'] = "Received"
                        elif dict_data['balance'] > 0:
                            dict_data['pay_status'] = "Pending"
                        combined_data.append(dict_data)
                        
                if repair_queryset:
                    repair_serializer = RepairDetailsSerializer(repair_queryset, many=True)

                    for i in range(len(repair_serializer.data)):
                        dict_data = repair_serializer.data[i]
                        detail_queryset = RepairDetails.objects.get(id=dict_data['id'])
                        dict_data['date'] = detail_queryset.repair_recived_date
                        dict_data['order_no'] = detail_queryset.repair_number
                        dict_data['type_name'] = "Repair"
                        dict_data['type'] = 2
                        dict_data['customer_name'] = detail_queryset.customer_details.customer_name
                        dict_data['payment_status_name'] = detail_queryset.payment_status.status_name
                        try:
                            payment_queryset = CommonPaymentDetails.objects.get(refference_number=detail_queryset.repair_number)
                            dict_data['amount'] = payment_queryset.payable_amount
                            dict_data['balance'] = payment_queryset.balance_amount
                        except:
                            dict_data['amount'] = 0
                            dict_data['balance'] = 0

                        paid_amount = CustomerPaymentTabel.objects.filter(refference_number=detail_queryset.repair_number).aggregate(total_paid=Sum('paid_amount'))
                        try:
                            last_paid_date = CustomerPaymentTabel.objects.filter(refference_number=detail_queryset.repair_number).order_by('-id').first()
                            dict_data['last_paid_date'] = last_paid_date.payment_date
                        except: 
                            dict_data['last_paid_date'] = None

                        dict_data['paid_amount'] = paid_amount['total_paid'] if paid_amount['total_paid'] else 0
                        dict_data['cr_dr'] = "CR"

                        if dict_data['amount'] == dict_data['paid_amount'] and dict_data['amount'] > 0 and dict_data['paid_amount'] > 0:
                            dict_data['pay_status'] = "Received"
                        elif dict_data['balance'] > 0:
                            dict_data['pay_status'] = "Pending"

                        combined_data.append(dict_data)

        return Response({
                "data": {
                    "list": combined_data,
                    "total_pages": paginated_data.num_pages,
                    "current_page": page,
                    "total_items": len(queryset),
                    "current_items": len(serializer.data)
                },
                "message": res_msg.retrieve('Common payment Details'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)


# #Sales incentive function
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# class SalesIncentivePercentReportView(APIView):
#     def post(self,request):
        
#         request_data=request.data        
#         search=request_data.get('search') if request_data.get('search') else ''
#         from_date = request_data.get('from_date') if request_data.get('from_date') != None else None
#         to_date = request_data.get('to_date') if request_data.get('to_date') != None else None
#         page = request_data.get('page') if request_data.get('page') else 1
#         branch = request_data.get('branch') if request_data.get('branch') else None
#         try:
#             items_per_page = int(request_data.get('items_per_page', BillingDetails.objects.all().count()))
#             if items_per_page == 0:
#                 items_per_page = 10 
#         except Exception as err:
#             items_per_page = 10 
        
#         filter_condition={}

#         if request.user.role.is_admin == True:
#             if branch != None :
#                 filter_condition['branch'] = branch
#         else:
#             filter_condition['branch'] = request.user.branch.pk
        
#         if search != "" :
#             filter_condition['bill_no__icontains'] = search

#         if from_date != None and to_date != None :
#             date_range=(from_date,to_date)
#             filter_condition['created_at__range'] = date_range
        
#         if len(filter_condition) != 0:
#             queryset=BillingDetails.objects.filter(**filter_condition).order_by('-id')            
#         else:
#             queryset=BillingDetails.objects.all().order_by('-id')

#         paginated_data = Paginator(queryset, items_per_page)
#         serializer = BillingDetailsSerializer(paginated_data.get_page(page), many=True)

#         dict_data=[]
#         for i in range(0, len(serializer.data)):
#             data = serializer.data[i]

#             payment = CommonPaymentDetails.objects.filter(refference_number=data['bill_no'])
#             try:
#                 staff = Staff.objects.get(user=data['created_by'])                         
#                 name= f"{staff.first_name} {staff.last_name}"
#             except:
#                 user=User.object.get(id=data['created_by'])
#                 name=user.email

#             amount = payment.values('created_by').aggregate(Sum('payable_amount'))
#             total_amount =amount['payable_amount__sum'] 
#             incentive = IncentivePercent.objects.all().order_by('-id')

#             for percentage in incentive:                
#                 if total_amount >= percentage.from_amount and total_amount <= percentage.to_amount:
#                     percent = percentage.incentive_percent
#                     incentive_amount = total_amount*(percent/100)                    
#                 else:
#                     percent=0
#                     incentive_amount=0
                
#                 res_data={
#                     'name':name,
#                     'total_amount':total_amount,
#                     'percent':percent,
#                     'incentive_amount':incentive_amount
#                 } 
#                 dict_data.append(res_data) 

#         return Response(
#         {
#             "data":{
#                 "list":dict_data,
#                 "total_pages": paginated_data.num_pages,
#                 "current_page": page,
#                 "total_items": len(queryset),
#                 "current_items": len(serializer.data),                
#             },
#             "message":res_msg.retrieve("Sales Incentive Percent Report"),
#             "status":status.HTTP_200_OK
#         },status=status.HTTP_200_OK
#         )


#Sales incentive function
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class SalesIncentiveAmountReportView(APIView):
    
    def post(self,request):
        request_data=request.data        
        search=request_data.get('search') if request_data.get('search') else ''
        from_date = request_data.get('from_date') if request_data.get('from_date') != None else None
        to_date = request_data.get('to_date') if request_data.get('to_date') != None else None
        page = request_data.get('page') if request_data.get('page') else 1
        branch = request_data.get('branch') if request_data.get('branch') else None
        try:
            items_per_page = int(request_data.get('items_per_page', BillingDetails.objects.all().count()))
            if items_per_page == 0:
                items_per_page = 10 
        except Exception as err:
            items_per_page = 10 
        
        filter_condition={}

        if request.user.role.is_admin == True:
            if branch != None :
                filter_condition['branch'] = branch
        else:
            filter_condition['branch'] = request.user.branch.pk
        
        if search != "" :
            filter_condition['bill_no__icontains'] = search

        if from_date != None and to_date != None :
            date_range=(from_date,to_date)
            filter_condition['created_at__range'] = date_range
        
        if len(filter_condition) != 0:
            queryset=BillingDetails.objects.filter(**filter_condition).order_by('-id')            
        else:
            queryset=BillingDetails.objects.all().order_by('-id')

        
        created_by_ids = queryset.values_list('created_by', flat=True).distinct()
        dict_data = {}
        paginator = Paginator(created_by_ids, items_per_page)
        paginated_data = paginator.get_page(page)
        for created_by_id in created_by_ids:
            total_amount = 0

            # Calculate total_amount for the current user
            created_by_data = queryset.filter(created_by=created_by_id)
            for bill_data in created_by_data:
                payment = CommonPaymentDetails.objects.filter(refference_number=bill_data.bill_no)
                amount = payment.aggregate(Sum('payable_amount'))
                total_amount += amount['payable_amount__sum'] or 0

            # Find the correct incentive percentage
            incentive_amount = 0
            for percentage in IncentivePercent.objects.all().order_by('-id'):
                if percentage.from_amount <= total_amount <= percentage.to_amount:
                    incentive_amount = percentage.incentive_amount
                    break

            # Retrieve user details
            try:
                staff = Staff.objects.get(user=created_by_id)
                name = f"{staff.first_name} {staff.last_name}"
            except Staff.DoesNotExist:
                user = User.object.get(id=created_by_id)
                name = user.email

            # Only add the user data to the dictionary if it doesn't already exist
            if created_by_id not in dict_data:
                dict_data[created_by_id] = {
                    'created_by': created_by_id,
                    'name': name,
                    'total_amount': total_amount,
                    'incentive_amount': incentive_amount
                }

        dict_data = list(dict_data.values())

       

        return Response(
            {
                "data": {
                    "list": dict_data,
                    "total_pages": paginator.num_pages,
                    "current_page":paginated_data.number,
                    "total_items": paginator.count,
                    "current_items":items_per_page,
                },
                "message": "Sales Incentive Percent Report retrieved successfully!",
                "status": status.HTTP_200_OK
            }
        )
       


#Sales incentive function
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class SalesIncentivePercentReportView(APIView):
    
    def post(self,request):
        request_data=request.data        
        search=request_data.get('search') if request_data.get('search') else ''
        from_date = request_data.get('from_date') if request_data.get('from_date') != None else None
        to_date = request_data.get('to_date') if request_data.get('to_date') != None else None
        page = request_data.get('page') if request_data.get('page') else 1
        branch = request_data.get('branch') if request_data.get('branch') else None
        try:
            items_per_page = int(request_data.get('items_per_page', BillingDetails.objects.all().count()))
            if items_per_page == 0:
                items_per_page = 10 
        except Exception as err:
            items_per_page = 10 
        
        filter_condition={}

        if request.user.role.is_admin == True:
            if branch != None :
                filter_condition['branch'] = branch
        else:
            filter_condition['branch'] = request.user.branch.pk
        
        if search != "" :
            filter_condition['bill_no__icontains'] = search

        if from_date != None and to_date != None :
            date_range=(from_date,to_date)
            filter_condition['created_at__range'] = date_range
        
        if len(filter_condition) != 0:
            queryset=BillingDetails.objects.filter(**filter_condition).order_by('-id')            
        else:
            queryset=BillingDetails.objects.all().order_by('-id')

        
        created_by_ids = queryset.values_list('created_by', flat=True).distinct()
        dict_data = {}
        paginator = Paginator(created_by_ids, items_per_page)
        paginated_data = paginator.get_page(page)
        for created_by_id in created_by_ids:
            total_amount = 0

            # Calculate total_amount for the current user
            created_by_data = queryset.filter(created_by=created_by_id)
            for bill_data in created_by_data:
                payment = CommonPaymentDetails.objects.filter(refference_number=bill_data.bill_no)
                amount = payment.aggregate(Sum('payable_amount'))
                total_amount += amount['payable_amount__sum'] or 0

            # Find the correct incentive percentage
            incentive_amount = 0
            percent = 0
            for percentage in IncentivePercent.objects.all().order_by('-id'):
                if percentage.from_amount <= total_amount <= percentage.to_amount:
                    percent = percentage.incentive_percent
                    incentive_amount = total_amount*(percent/100) 
                    break

            # Retrieve user details
            try:
                staff = Staff.objects.get(user=created_by_id)
                name = f"{staff.first_name} {staff.last_name}"
            except Staff.DoesNotExist:
                user = User.object.get(id=created_by_id)
                name = user.email

            # Only add the user data to the dictionary if it doesn't already exist
            if created_by_id not in dict_data:
                dict_data[created_by_id] = {
                    'created_by': created_by_id,
                    'name': name,
                    'total_amount': total_amount,
                    'percent':percent,
                    'incentive_amount': incentive_amount
                }

        dict_data = list(dict_data.values())

       

        return Response(
            {
                "data": {
                    "list": dict_data,
                    "total_pages": paginator.num_pages,
                    "current_page":paginated_data.number,
                    "total_items": paginator.count,
                    "current_items":items_per_page,
                },
                "message": "Sales Incentive Percent Report retrieved successfully!",
                "status": status.HTTP_200_OK
            }
        )
       


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class CashCounterReport(APIView):
    def post(self, request):
        from_date = request.data.get('from_date') if request.data.get('from_date') else None
        to_date = request.data.get('to_date') if request.data.get('to_date') else None
        page = request.data.get('page') if request.data.get('page') else 1
        try:
            items_per_page = int(request.data.get('items_per_page', CashCounter.objects.all().count()))
            if items_per_page == 0:
                items_per_page = 10 
        except Exception as err:
            items_per_page = 10 
        
        filter_condition={}

        if from_date != None and to_date!= None:
           date_range=(from_date,to_date)
           filter_condition['created_at__range']=date_range

        res_data = []
        

        cash_counter_queryset = CashCounter.objects.all().order_by('id')

        paginated_data = Paginator(cash_counter_queryset, items_per_page)
        cash_counter_serializer = CashCounterSerializer(paginated_data.get_page(page), many=True)

        for item in range(0, len(cash_counter_serializer.data)):
            dict_data = cash_counter_serializer.data[item]

            if len(filter_condition) != 0:
                queryset = list(BillingDetails.objects.filter(**filter_condition,cash_counter=cash_counter_queryset[item].pk).order_by('-id'))
            else:
                queryset = list(BillingDetails.objects.filter(cash_counter=cash_counter_queryset[item].pk).order_by('-id'))

            serializer = BillingDetailsSerializer(queryset, many=True)
            payment_list = []
            payment_data_dict = {}
            for i in range(len(serializer.data)):
                dict_data['customer_name'] = queryset[i].customer_details.customer_name
                try:
                    payment_queryset = CustomerPaymentTabel.objects.filter(refference_number__icontains=queryset[i].bill_no).values('payment_method__payment_method_name').annotate(total_amount=Sum('paid_amount'))
                    print(payment_queryset)
                    
                    for data in payment_queryset:
                        payment_data = {}
                        payment_method = data['payment_method__payment_method_name']
                        total_amount = data['total_amount']

                        dict_data[payment_method] = total_amount
                    # dict_data['payment_list'] = payment_list
                except:
                    pass
            # dict_data['payment_data'] = payment_data_dict 
            res_data.append(dict_data)

        return Response({
            "data": {
                "list": res_data,
                "total_pages": paginated_data.num_pages,
                "current_page": page,
                "total_items": len(queryset),
                "current_items": len(serializer.data)
            },
            "message": res_msg.retrieve('Billing Payment Details'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)