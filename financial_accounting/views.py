from django.shortcuts import render
from .models import *
from rest_framework.views import APIView
from rest_framework import status,viewsets
from django.utils import timezone
from app_lib.response_messages import ResponseMessages
from .serializer import *
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.db.models import ProtectedError
from django.db.models import Q
from rest_framework import filters
import random
from django.conf import settings
from django.core.paginator import Paginator
from datetime import datetime
from billing.models import *
from billing.serializer import *
from order_management.models import *
from order_management.serializer import *
from repair_management.models import *
from repair_management.serializer import *
from purchase.models import *
from purchase.serializers import *
from payment_management.models import *
from payment_management.serializer import *
from customer.serializer import *
from django.db.models import Sum

# Create your views here.
res_msg = ResponseMessages()

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class LedgerListView(APIView):
    def post(self, request):
        
        fromdate = request.data.get('from_date') if request.data.get('from_date') != None else None
        todate = request.data.get('to_date') if request.data.get('to_date') != None else None
        customer = request.data.get('customer') if request.data.get('customer') != None else None
        type = request.data.get('type') if request.data.get('type') != None else None
        page = request.data.get('page') if request.data.get('page') else 1
        items_per_page = int(request.data.get('items_per_page')) if request.data.get('items_per_page') else 10
            
        combined_data = []
        from_date = datetime.strptime(fromdate, '%Y-%m-%d') if fromdate else None
        to_date = datetime.strptime(todate, '%Y-%m-%d') if todate else None
        
        if type != None:
            if int(type) == settings.BILLING_PAYMENT:
                if from_date != None and to_date!= None:
                    if customer != None:
                        sales_queryset = BillingDetails.objects.filter(created_at__range=(from_date,to_date),customer_details=customer).order_by('-id')
                    else:
                        sales_queryset = BillingDetails.objects.filter(created_at__range=(from_date,to_date)).order_by('-id')
                else:
                    if customer != None:
                        sales_queryset = BillingDetails.objects.filter(customer_details=customer).order_by('-id')
                    else:
                        sales_queryset = BillingDetails.objects.all().order_by('-id')

                paginated_data = Paginator(sales_queryset, items_per_page)
                sales_serializer = BillingDetailsSerializer(paginated_data.get_page(page), many=True)

                for i in range(len(sales_serializer.data)):
                    dict_data = sales_serializer.data[i]
                    dict_data['date'] = sales_queryset[i].bill_date
                    dict_data['order_no'] = sales_queryset[i].bill_no
                    dict_data['type_name'] = "Sales"
                    dict_data['type'] = 3
                    dict_data['customer_name'] = sales_queryset[i].customer_details.customer_name
                    dict_data['customer_mobile'] = sales_queryset[i].customer_details.phone
                    dict_data['payment_status_name'] = sales_queryset[i].payment_status.status_name
                    
                    try:
                        payment_queryset = CommonPaymentDetails.objects.get(refference_number=sales_queryset[i].bill_no)
                        dict_data['amount'] = payment_queryset.payable_amount
                    except:
                        dict_data['amount'] = 0

                    paid_amount = CustomerPaymentTabel.objects.filter(refference_number=sales_queryset[i].bill_no).aggregate(total_paid=Sum('paid_amount'))
                    try:
                        last_paid_date = CustomerPaymentTabel.objects.filter(refference_number=sales_queryset[i].bill_no).order_by('-id').first()
                        dict_data['last_paid_date'] = last_paid_date.payment_date
                    except: 
                        dict_data['last_paid_date'] = None
                    
                    dict_data['paid_amount'] = paid_amount['total_paid'] if paid_amount['total_paid'] else 0
                    dict_data['balance'] = dict_data['amount'] - dict_data['paid_amount']
                    dict_data['cr_dr'] = "CR"
                    
                    if dict_data['amount'] > 0 and dict_data['paid_amount'] > 0 and dict_data['amount'] == dict_data['paid_amount']:
                        dict_data['pay_status'] = "Done"
                    elif dict_data['balance'] > 0 and dict_data['balance'] < dict_data['amount']:
                        dict_data['pay_status'] = "Pay now"
                    else:
                        dict_data['pay_status'] = "Pay now"

                    combined_data.append(dict_data)
                
            elif int(type) == settings.ORDER_PAYMENT:
                
                if from_date != None and to_date!= None:
                    if customer != None:
                        sales_order_queryset = OrderDetails.objects.filter(created_at__range=(from_date,to_date),customer=customer).order_by('-id')
                    else:
                        sales_order_queryset = OrderDetails.objects.filter(created_at__range=(from_date,to_date)).order_by('-id')
                else:
                    if customer != None:
                        sales_order_queryset = OrderDetails.objects.filter(customer=customer).order_by('-id')
                    else:
                        sales_order_queryset = OrderDetails.objects.all().order_by('-id')
                
                paginated_data = Paginator(sales_order_queryset, items_per_page)
                sales_order_serializer = OrderDetailsSerializer(paginated_data.get_page(page), many=True)

                for i in range(len(sales_order_serializer.data)):
                    
                    dict_data = sales_order_serializer.data[i]
                    dict_data['date'] = sales_order_queryset[i].order_date
                    dict_data['order_no'] = sales_order_queryset[i].order_id.order_id
                    dict_data['type_name'] = "Order"
                    dict_data['type'] = 1
                    dict_data['customer_name'] = sales_order_queryset[i].customer.customer_name
                    dict_data['customer_details'] = sales_order_queryset[i].customer.pk
                    dict_data['customer_mobile'] = sales_order_queryset[i].customer.phone
                    dict_data['payment_status_name'] = sales_order_queryset[i].payment_status.status_name
                    try:
                        payment_queryset = CommonPaymentDetails.objects.get(refference_number=sales_order_queryset[i].order_id.order_id)
                        dict_data['amount'] = payment_queryset.payable_amount
                        dict_data['balance'] = payment_queryset.balance_amount
                    except:
                        dict_data['amount'] = 0
                        dict_data['balance'] = 0

                    paid_amount = CustomerPaymentTabel.objects.filter(refference_number=sales_order_queryset[i].order_id.order_id).aggregate(total_paid=Sum('paid_amount'))
                    try:
                        last_paid_date = CustomerPaymentTabel.objects.filter(refference_number=sales_order_queryset[i].order_id.order_id).order_by('-id').first()
                        dict_data['last_paid_date'] = last_paid_date.payment_date
                    except: 
                        dict_data['last_paid_date'] = None
                    dict_data['paid_amount'] = paid_amount['total_paid'] if paid_amount['total_paid'] else 0
                    dict_data['balance'] = dict_data['amount'] - dict_data['paid_amount']
                    dict_data['cr_dr'] = "CR"

                    if dict_data['amount'] > 0 and dict_data['paid_amount'] > 0 and dict_data['amount'] == dict_data['paid_amount']  :
                        dict_data['pay_status'] = "Done"
                    elif dict_data['balance'] > 0 and dict_data['balance'] < dict_data['amount']:
                        dict_data['pay_status'] = "Pay now"
                    else:
                        dict_data['pay_status'] = "Pay now"

                    combined_data.append(dict_data)
                
            elif int(type) == settings.REPAIR_PAYMENT:
                
                if from_date != None and to_date!= None:
                    if customer != None:
                        repair_queryset = RepairDetails.objects.filter(created_at__range=(from_date,to_date),customer_details=customer).order_by('-id')
                    else:
                        repair_queryset = RepairDetails.objects.filter(created_at__range=(from_date,to_date)).order_by('-id')
                else:
                    if customer != None:
                        repair_queryset = RepairDetails.objects.filter(customer_details=customer).order_by('-id')
                    else:
                        repair_queryset = RepairDetails.objects.all().order_by('-id')

                paginated_data = Paginator(repair_queryset, items_per_page)
                repair_serializer = RepairDetailsSerializer(paginated_data.get_page(page), many=True)

                for i in range(len(repair_serializer.data)):
                    dict_data = repair_serializer.data[i]
                    dict_data['date'] = repair_queryset[i].repair_recived_date
                    dict_data['order_no'] = repair_queryset[i].repair_number
                    dict_data['type_name'] = "Repair"
                    dict_data['type'] = 2
                    dict_data['customer_name'] = repair_queryset[i].customer_details.customer_name
                    dict_data['customer_details'] = repair_queryset[i].customer_details.pk
                    dict_data['customer_mobile'] = repair_queryset[i].customer_details.phone
                    dict_data['payment_status_name'] = repair_queryset[i].payment_status.status_name
                    
                    try:
                        payment_queryset = CommonPaymentDetails.objects.get(refference_number=repair_queryset[i].repair_number)
                        dict_data['amount'] = payment_queryset.payable_amount
                        dict_data['balance'] = payment_queryset.balance_amount
                    except:
                        dict_data['amount'] = 0
                        dict_data['balance'] = 0

                    paid_amount = CustomerPaymentTabel.objects.filter(refference_number=repair_queryset[i].repair_number).aggregate(total_paid=Sum('paid_amount'))
                    try:
                        last_paid_date = CustomerPaymentTabel.objects.filter(refference_number=repair_queryset[i].repair_number).order_by('-id').first()
                        dict_data['last_paid_date'] = last_paid_date.payment_date
                    except: 
                        dict_data['last_paid_date'] = None
                    dict_data['paid_amount'] = paid_amount['total_paid'] if paid_amount['total_paid'] else 0
                    dict_data['balance'] = dict_data['amount'] - dict_data['paid_amount']
                    dict_data['cr_dr'] = "CR"

                    if dict_data['amount'] > 0 and dict_data['paid_amount'] > 0 and dict_data['amount'] == dict_data['paid_amount']  :
                        dict_data['pay_status'] = "Done"
                    elif dict_data['balance'] > 0 and dict_data['balance'] < dict_data['amount']:
                        dict_data['pay_status'] = "Pay now"
                    else:
                        dict_data['pay_status'] = "Pay now"

                    combined_data.append(dict_data)
            
        else:
            if from_date != None and to_date!= None:
                if customer != None:
                    sales_queryset = BillingDetails.objects.filter(created_at__range=(from_date,to_date),customer_details=customer).order_by('-id')
                    sales_order_queryset = OrderDetails.objects.filter(created_at__range=(from_date,to_date),customer=customer).order_by('-id')
                    repair_queryset = RepairDetails.objects.filter(created_at__range=(from_date,to_date),customer_details=customer).order_by('-id')
                else:
                    sales_queryset = BillingDetails.objects.filter(created_at__range=(from_date,to_date)).order_by('-id')
                    sales_order_queryset = OrderDetails.objects.filter(created_at__range=(from_date,to_date)).order_by('-id')
                    repair_queryset = RepairDetails.objects.filter(created_at__range=(from_date,to_date)).order_by('-id')

            else:
                if customer != None:
                    sales_queryset = BillingDetails.objects.filter(customer_details=customer).order_by('-id')
                    sales_order_queryset = OrderDetails.objects.filter(customer=customer).order_by('-id')
                    repair_queryset = RepairDetails.objects.filter(customer_details=customer).order_by('-id')
                   
                else:
                    sales_queryset = BillingDetails.objects.all().order_by('-id')
                    sales_order_queryset = OrderDetails.objects.all().order_by('-id')
                    repair_queryset = RepairDetails.objects.all().order_by('-id')

            sales_serializer = BillingDetailsSerializer(sales_queryset, many=True)
            sales_order_serializer = OrderDetailsSerializer(sales_order_queryset, many=True)
            repair_serializer = RepairDetailsSerializer(repair_queryset, many=True)
        
            for i in range(len(sales_serializer.data)):
                dict_data = sales_serializer.data[i]
                dict_data['date'] = sales_queryset[i].bill_date
                dict_data['order_no'] = sales_queryset[i].bill_no
                dict_data['type_name'] = "Sales"
                dict_data['type'] = 3
                dict_data['customer_name'] = sales_queryset[i].customer_details.customer_name
                dict_data['payment_status_name'] = sales_queryset[i].payment_status.status_name
                try:
                    payment_queryset = CommonPaymentDetails.objects.get(refference_number=sales_queryset[i].bill_no)
                    dict_data['amount'] = payment_queryset.payable_amount
                    dict_data['balance'] = payment_queryset.balance_amount
                except:
                    dict_data['amount'] = 0
                    dict_data['balance'] = 0

                paid_amount = CustomerPaymentTabel.objects.filter(refference_number=sales_queryset[i].bill_no).aggregate(total_paid=Sum('paid_amount'))
                try:
                    last_paid_date = CustomerPaymentTabel.objects.filter(refference_number=sales_queryset[i].bill_no).order_by('-id').first()
                    dict_data['last_paid_date'] = last_paid_date.payment_date
                except: 
                    dict_data['last_paid_date'] = None

                dict_data['paid_amount'] = paid_amount['total_paid'] if paid_amount['total_paid'] else 0
                dict_data['balance'] = dict_data['amount'] - dict_data['paid_amount']
                dict_data['cr_dr'] = "CR"

                if dict_data['amount'] > 0 and dict_data['paid_amount'] > 0 and dict_data['amount'] == dict_data['paid_amount']:
                    dict_data['pay_status'] = "Done"
                elif dict_data['balance'] > 0 and dict_data['balance'] < dict_data['amount']:
                    dict_data['pay_status'] = "Pay now"
                else:
                    dict_data['pay_status'] = "Pay now"

                combined_data.append(dict_data)
                
            for i in range(len(sales_order_serializer.data)):
                dict_data = sales_order_serializer.data[i]
                dict_data['date'] = sales_order_queryset[i].order_date
                dict_data['order_no'] = sales_order_queryset[i].order_id.order_id
                dict_data['type_name'] = "Order"
                dict_data['type'] = 1
                dict_data['customer_name'] = sales_order_queryset[i].customer.customer_name
                dict_data['customer_details'] = sales_order_queryset[i].customer.pk
                dict_data['customer_mobile'] = sales_order_queryset[i].customer.phone
                dict_data['payment_status_name'] = sales_order_queryset[i].payment_status.status_name
                try:
                    payment_queryset = CommonPaymentDetails.objects.get(refference_number=sales_order_queryset[i].order_id.order_id)
                    dict_data['amount'] = payment_queryset.payable_amount
                    dict_data['balance'] = payment_queryset.balance_amount
                except:
                    dict_data['amount'] = 0
                    dict_data['balance'] = 0

                paid_amount = CustomerPaymentTabel.objects.filter(refference_number=sales_order_queryset[i].order_id.order_id).aggregate(total_paid=Sum('paid_amount'))
                
                try:
                    last_paid_date = CustomerPaymentTabel.objects.filter(refference_number=sales_order_queryset[i].order_id.order_id).order_by('-id').first()
                    dict_data['last_paid_date'] = last_paid_date.payment_date
                except: 
                    dict_data['last_paid_date'] = None

                dict_data['paid_amount'] = paid_amount['total_paid'] if paid_amount['total_paid'] else 0
                dict_data['balance'] = dict_data['amount'] - dict_data['paid_amount']
                dict_data['cr_dr'] = "CR"

                if dict_data['amount'] > 0 and dict_data['paid_amount'] > 0 and dict_data['amount'] == dict_data['paid_amount']:
                    dict_data['pay_status'] = "Done"
                elif dict_data['balance'] > 0 and dict_data['balance'] < dict_data['amount']:
                    dict_data['pay_status'] = "Pay now"
                else:
                    dict_data['pay_status'] = "Pay now"

                combined_data.append(dict_data)
           
            for i in range(len(repair_serializer.data)):
                dict_data = repair_serializer.data[i]
                dict_data['date'] = repair_queryset[i].repair_recived_date
                dict_data['order_no'] = repair_queryset[i].repair_number
                dict_data['type_name'] = "Repair"
                dict_data['type'] = 2
                dict_data['customer_name'] = repair_queryset[i].customer_details.customer_name
                dict_data['customer_details'] = repair_queryset[i].customer_details.pk
                dict_data['customer_mobile'] = repair_queryset[i].customer_details.phone
                dict_data['payment_status_name'] = repair_queryset[i].payment_status.status_name
                try:
                    payment_queryset = CommonPaymentDetails.objects.get(refference_number=repair_queryset[i].repair_number)
                    dict_data['amount'] = payment_queryset.payable_amount
                    dict_data['balance'] = payment_queryset.balance_amount
                except:
                    dict_data['amount'] = 0
                    dict_data['balance'] = 0

                paid_amount = CustomerPaymentTabel.objects.filter(refference_number=repair_queryset[i].repair_number).aggregate(total_paid=Sum('paid_amount'))
                try:
                    last_paid_date = CustomerPaymentTabel.objects.filter(refference_number=repair_queryset[i].repair_number).order_by('-id').first()
                    dict_data['last_paid_date'] = last_paid_date.payment_date
                except: 
                    dict_data['last_paid_date'] = None

                dict_data['paid_amount'] = paid_amount['total_paid'] if paid_amount['total_paid'] else 0
                dict_data['balance'] = dict_data['amount'] - dict_data['paid_amount']
                dict_data['cr_dr'] = "CR"

                if dict_data['amount'] > 0 and dict_data['paid_amount'] > 0 and dict_data['amount'] == dict_data['paid_amount']:
                    dict_data['pay_status'] = "Done"
                elif dict_data['balance'] > 0 and dict_data['balance'] < dict_data['amount']:
                    dict_data['pay_status'] = "Pay now"
                else:
                    dict_data['pay_status'] = "Pay now"

                combined_data.append(dict_data)
            
        paginator = Paginator(combined_data, items_per_page)
        
        paginated_data = paginator.page(page)
        paginated_items = list(paginated_data)
        return Response({
            "data": {
                "list": paginated_items,
            },
            'total_pages': paginator.num_pages,
            'current_page': paginated_data.number,
            'total_items': paginator.count,
            'current_items': len(paginated_items),
            "message": res_msg.retrieve('Ledger Details'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class CustomerPaymentListView(APIView):
    def get(self, request, customer, type):

        combined_data = []
        customer_list = []
        credit_balance = []
        customer_queryset = Customer.objects.get(id=customer)
        customer_data = {}
        customer_data['id'] = customer_queryset.pk
        customer_data['customer_name'] = customer_queryset.customer_name
        customer_data['customer_mobile'] = customer_queryset.phone
        customer_data['district'] = customer_queryset.district
        customer_data['pincode'] = customer_queryset.pincode
        customer_data['state'] = customer_queryset.state
        customer_data['country'] = customer_queryset.country
        if type != None:
            if int(type) == settings.BILLING_PAYMENT:
                sales_queryset = BillingDetails.objects.filter(customer_details=customer).order_by('-id')
                sales_serializer = BillingDetailsSerializer(sales_queryset, many=True)
                total_credit_balance = 0
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
                        dict_data['payable_amount'] = payment_queryset.payable_amount
                        dict_data['advance_amount'] = payment_queryset.advance_amount
                    except:
                        dict_data['total_amount'] = 0
                        dict_data['payable_amount'] = 0
                        dict_data['advance_amount'] = 0

                    paid_amount = CustomerPaymentTabel.objects.filter(refference_number=sales_queryset[i].bill_no).aggregate(total_paid=Sum('paid_amount'))
                    dict_data['paid_amount'] = paid_amount['total_paid'] if paid_amount['total_paid'] else 0
                    dict_data['balance_amount'] = dict_data['total_amount'] - dict_data['paid_amount']
                    total_credit_balance += dict_data['paid_amount']

                    if dict_data['total_amount'] == dict_data['paid_amount'] and dict_data['total_amount'] > 0 and dict_data['paid_amount'] > 0:
                        dict_data['pay_status'] = "Done"
                    elif dict_data['balance_amount'] > 0 and dict_data['balance_amount'] < dict_data['total_amount']:
                        dict_data['pay_status'] = "Pay now"
                    else:
                        dict_data['pay_status'] = "Pay now"

                    combined_data.append(dict_data)

            elif int(type) == settings.ORDER_PAYMENT:
                
                sales_order_queryset = OrderDetails.objects.filter(customer=customer).order_by('-id')
                sales_order_serializer = OrderDetailsSerializer(sales_order_queryset, many=True)
                total_credit_balance = 0
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
                        dict_data['payable_amount'] = payment_queryset.payable_amount
                        dict_data['advance_amount'] = payment_queryset.advance_amount
                    except:
                        dict_data['total_amount'] = 0
                        dict_data['payable_amount'] = 0
                        dict_data['advance_amount'] = 0

                    paid_amount = CustomerPaymentTabel.objects.filter(refference_number=sales_order_queryset[i].order_id.order_id).aggregate(total_paid=Sum('paid_amount'))
                    dict_data['paid_amount'] = paid_amount['total_paid'] if paid_amount['total_paid'] else 0
                    dict_data['balance_amount'] = dict_data['total_amount'] - dict_data['paid_amount']
                    total_credit_balance += dict_data['paid_amount']

                    if dict_data['total_amount'] == dict_data['paid_amount'] and dict_data['total_amount'] > 0 and dict_data['paid_amount'] > 0:
                        dict_data['pay_status'] = "Done"
                    elif dict_data['balance_amount'] > 0 and dict_data['balance_amount'] < dict_data['total_amount']:
                        dict_data['pay_status'] = "Pay now"
                    else:
                        dict_data['pay_status'] = "Pay now"
                    combined_data.append(dict_data)
            
                
            elif int(type) == settings.REPAIR_PAYMENT:
                repair_queryset = RepairDetails.objects.filter(customer_details=customer).order_by('-id')
                
                repair_serializer = RepairDetailsSerializer(repair_queryset, many=True)
                total_credit_balance = 0
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
                        dict_data['payable_amount'] = payment_queryset.payable_amount
                        dict_data['advance_amount'] = payment_queryset.advance_amount
                    except:
                        dict_data['total_amount'] = 0
                        dict_data['payable_amount'] = 0
                        dict_data['advance_amount'] = 0

                    paid_amount = CustomerPaymentTabel.objects.filter(refference_number=repair_queryset[i].repair_number).aggregate(total_paid=Sum('paid_amount'))
                    dict_data['paid_amount'] = paid_amount['total_paid'] if paid_amount['total_paid'] else 0
                    dict_data['balance_amount'] = dict_data['total_amount'] - dict_data['paid_amount']
                    total_credit_balance += dict_data['paid_amount']

                    if dict_data['total_amount'] == dict_data['paid_amount'] and dict_data['total_amount'] > 0 and dict_data['paid_amount'] > 0:
                        dict_data['pay_status'] = "Done"
                    elif dict_data['balance_amount'] > 0 and dict_data['balance_amount'] < dict_data['total_amount']:
                        dict_data['pay_status'] = "Pay now"
                    else:
                        dict_data['pay_status'] = "Pay now"
                    combined_data.append(dict_data)
                    
        customer_data['total_credit_balance'] = total_credit_balance
        customer_list.append(customer_data)
        return Response({
            "data": {
                "customer_list" : customer_list,
                "list": combined_data,
            },
            "message": res_msg.retrieve('Customer Payment List'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
    


