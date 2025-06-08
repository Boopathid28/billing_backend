from rest_framework.views import APIView
from rest_framework import status, viewsets, generics, mixins
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .models import *
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework.decorators import permission_classes, authentication_classes
import phonenumbers
from app_lib.utility import Email
from django.utils import timezone
from django.db.models import ProtectedError
from django.core.paginator import Paginator
from app_lib.response_messages import ResponseMessages
from accounts.serializer import UserRoleSerializer
from accounts.models import *
from .serializer import *
from repair_management.serializer import *
from repair_management.models import *
from order_management.serializer import *
from order_management.models import *
from datetime import date
import requests
from django.db.models import Sum
import json
from django.db.models import Q
from django.conf import settings
from billing.serializer import *
from billing.models import *

res_msg = ResponseMessages()

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class PaymentMethodList(APIView):

    def get(self, request):

        queryset = list(PaymentMenthod.objects.all().order_by('id'))
        serializer = PaymentMenthodSerializer(queryset, many=True)

        return Response({
            "data": {
                "list": serializer.data,
            },
            "message": res_msg.retrieve('Payment Method Details'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)

    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class PaymentProviderList(APIView):

    def get(self, request,pk=None):
        if pk != None:
            queryset = list(PaymentProviders.objects.filter(payment_method=pk).order_by('id'))
        else:
            queryset = list(PaymentProviders.objects.all().order_by('id'))

        serializer = PaymentProvidersSerializer(queryset, many=True)

        return Response({
            "data": {
                "list": serializer.data,
            },
            "message": res_msg.retrieve('Payment Provider Details'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
    

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class PaymentView(APIView):

    def post(self, request):
        request_data = request.data
        
        try:
            is_reference_valid = check_and_process_reference_number(request_data.get('refference_number'))

            is_issued = request_data.get('is_issued',None)

            if is_reference_valid == True:
                request_data['refference_number'] = request_data.get('refference_number')
                request_data['total_amount'] = float(request_data.get('total_amount')) if request_data.get('total_amount') !=None else 0
                request_data['discount_percentage'] = request_data.get('discount_percentage') if request_data.get('discount_percentage') != None else 0
                request_data['discount_amount'] = float(request_data.get('discount_amount')) if request_data.get('discount_amount') !=None else 0
                request_data['gst_type'] = request_data.get('gst_type') 
                request_data['igst_percentage'] = request_data.get('igst_percentage')
                request_data['igst_amount'] = request_data.get('igst_amount')
                request_data['sgst_percentage'] = request_data.get('sgst_percentage')  
                request_data['sgst_amount'] = request_data.get('sgst_amount')  
                request_data['cgst_percentage'] = request_data.get('cgst_percentage')
                request_data['cgst_amount'] = request_data.get('cgst_amount')
                request_data['others'] = request_data.get('others')
                request_data['round_off_total'] = request_data.get('round_off')
                request_data['hall_mark_charges'] = request_data.get('hall_mark_charges')
                request_data['stone_amount'] = request_data.get('stone_amount')
                request_data['diamond_amount'] = request_data.get('diamond_amount')
                request_data['making_charge_per_gram'] = request_data.get('making_charge_per_gram')
                request_data['flat_making_charge'] = request_data.get('flat_making_charge')
                request_data['salereturn_amount'] = request_data.get('salereturn_amount')
                request_data['exchange_amount'] = request_data.get('exchange_amount')
                request_data['payable_amount'] = request_data.get('payable_amount')
                request_data['advance_amount'] = request_data.get('advance_amount')
                request_data['balance_amount'] = request_data.get('balance_amount')
                request_data['amount_received'] = request_data.get('amount_received')
                request_data['created_at']=timezone.now()
                request_data['created_by']=request.user.id
                try:
                    payment_queryset = CommonPaymentDetails.objects.get(refference_number = request_data.get('refference_number'))
                
                    payment_serializer=CommonPaymentSerializer(payment_queryset,data=request_data,partial=True)
                except CommonPaymentDetails.DoesNotExist:
                    payment_serializer=CommonPaymentSerializer(data=request_data)
                except Exception as err:
                    raise Exception(err)
                    
                if payment_serializer.is_valid():
                    payment_serializer.save()
                    
                    oldgold_details=request_data.get('oldgold_particulars') if request_data.get('oldgold_particulars') else {}
                    if len(oldgold_details) != 0:
                        for data in oldgold_details:
                            try:
                                oldgold_id = data.get('id') if data.get('id') else 0
                                oldgold_queryset = RepairOrderOldGold.objects.get(id=oldgold_id)
                                oldgold_data = {}
                                oldgold_data = {
                                    'refference_number' : request_data.get('refference_number'),
                                    'old_gold_no' : data.get('old_gold_no'),
                                    'metal' : data.get('metal'),
                                    'gross_weight': 0 if data.get('gross_weight') is None else float(data.get('gross_weight')),
                                    'net_weight': 0 if data.get('net_weight') is None else float(data.get('net_weight')),
                                    'dust_weight': 0 if data.get('dust_weight') is None else float(data.get('dust_weight')),
                                    'metal_rate': 0 if data.get('metal_rate') is None else float(data.get('metal_rate')),
                                    'today_metal_rate': 0 if data.get('today_metal_rate') is None else float(data.get('today_metal_rate')),
                                    'purity': data.get('purity'),
                                    'total_amount': 0 if data.get('total_amount') is None else float(data.get('total_amount')),
                                    'old_rate' : 0 if data.get('old_rate') is None else float(data.get('old_rate')),
                                    'employee_id' : data.get('employee_id'),
                                    'created_at' : timezone.now(),
                                    'created_by' : request.user.id
                                }
                                
                                repair_order_oldgold_serializer=RepairOrderOldGoldSerializer(oldgold_queryset,data=oldgold_data,partial=True)

                                if repair_order_oldgold_serializer.is_valid():
                                    repair_order_oldgold_serializer.save()
                                else:
                                    raise Exception(repair_order_oldgold_serializer.errors)
                            
                            except RepairOrderOldGold.DoesNotExist:
                                oldgold_data = {
                                    'refference_number' : request_data.get('refference_number'),
                                    'old_gold_no' : data.get('old_gold_no'),
                                    'metal' : data.get('metal'),
                                    'gross_weight': 0 if data.get('gross_weight') is None else float(data.get('gross_weight')),
                                    'net_weight': 0 if data.get('net_weight') is None else float(data.get('net_weight')),
                                    'dust_weight': 0 if data.get('dust_weight') is None else float(data.get('dust_weight')),
                                    'metal_rate': 0 if data.get('metal_rate') is None else float(data.get('metal_rate')),
                                    'today_metal_rate': 0 if data.get('today_metal_rate') is None else float(data.get('today_metal_rate')),
                                    'purity': data.get('purity'),
                                    'total_amount': 0 if data.get('total_amount') is None else float(data.get('total_amount')),
                                    'old_rate' : 0 if data.get('old_rate') is None else float(data.get('old_rate')),
                                    'employee_id' : data.get('employee_id'),
                                    'modified_at' : timezone.now(),
                                    'modified_by' : request.user.id
                                }
                                
                                repair_order_oldgold_serializer=RepairOrderOldGoldSerializer(data=oldgold_data)

                                if repair_order_oldgold_serializer.is_valid():
                                    repair_order_oldgold_serializer.save()
                                else:
                                    raise Exception(repair_order_oldgold_serializer.errors)
                                
                            except Exception as err:
                                raise Exception(err)
                            

                    sale_return_details = request.data.get('sale_return_details') if request.data.get('sale_return_details') else []
                    if len(sale_return_details) != 0:
                        # if return_items.get('type') == settings.AUTOMATIC:
                            for return_items in sale_return_details:
                                try:
                                    bill_item_queryset = BillingTagItems.objects.get(id=return_items.get('id'))
                                    
                                    estimation_return_data={
                                        'billing_details': return_items.get('billing_details'),
                                        'return_bill_details' : bill_item_queryset.billing_details.pk,
                                        'return_items' : bill_item_queryset.pk,
                                        'tag_number' : bill_item_queryset.tag_number,
                                        'item_details': bill_item_queryset.item_details.pk,
                                        'sub_item_details': bill_item_queryset.sub_item_details.pk,
                                        'metal': bill_item_queryset.metal.pk,
                                        'net_weight':bill_item_queryset.net_weight,
                                        'gross_weight':bill_item_queryset.gross_weight,
                                        'tag_weight':bill_item_queryset.tag_weight,
                                        'cover_weight':bill_item_queryset.cover_weight,
                                        'loop_weight':bill_item_queryset.loop_weight,
                                        'other_weight':bill_item_queryset.other_weight,
                                        'pieces':bill_item_queryset.pieces,
                                        'total_pieces':bill_item_queryset.total_pieces,
                                        'rate' : bill_item_queryset.rate,
                                        'stone_rate' : bill_item_queryset.stone_rate,
                                        'diamond_rate' : bill_item_queryset.diamond_rate,
                                        'stock_type' : bill_item_queryset.stock_type.pk,
                                        'calculation_type' : bill_item_queryset.calculation_type.pk,
                                        'tax_percent' : bill_item_queryset.tax_percent,
                                        'additional_charges' : bill_item_queryset.additional_charges,
                                        'total_stone_weight' : bill_item_queryset.total_stone_weight,
                                        'total_diamond_weight' : bill_item_queryset.total_diamond_weight,
                                        'per_gram_weight_type' : bill_item_queryset.per_gram_weight_type.pk if bill_item_queryset.per_gram_weight_type else None,
                                        'wastage_percentage' : bill_item_queryset.wastage_percentage,
                                        'flat_wastage' : bill_item_queryset.flat_wastage,
                                        'making_charge' : bill_item_queryset.making_charge,
                                        'flat_making_charge' : bill_item_queryset.flat_making_charge,
                                        'wastage_calculation_type': bill_item_queryset.wastage_calculation_type.pk if bill_item_queryset.wastage_calculation_type else None,
                                        'making_charge_calculation_type': bill_item_queryset.making_charge_calculation_type.pk if bill_item_queryset.making_charge_calculation_type else None,
                                        'gst' : bill_item_queryset.gst,
                                        'total_rate' : bill_item_queryset.total_rate,
                                        'without_gst_rate' : bill_item_queryset.without_gst_rate,
                                        'huid_rate':bill_item_queryset.huid_rate
                                    }   
                                    
                                    return_serializer=BillingSaleReturnItemsSerializer(data=estimation_return_data)

                                    if return_serializer.is_valid():
                                        return_serializer.save()
                                        
                                        try:

                                            return_stone_queryset = BillingStoneDetails.objects.filter(billing_details=bill_item_queryset.billing_details.pk,billing_item_details=bill_item_queryset.pk)
                                            
                                            if len(return_stone_queryset) != 0:
                                                for return_stone in return_stone_queryset:

                                                    stone_dict={}

                                                    stone_dict['billing_details'] = return_items.get('billing_details')
                                                    stone_dict['billing_return_item'] = return_serializer.data['id']
                                                    stone_dict['stone_name']=return_stone.stone_name.pk
                                                    stone_dict['stone_pieces']=return_stone.stone_pieces
                                                    stone_dict['stone_weight']=return_stone.stone_weight
                                                    stone_dict['stone_weight_type']=return_stone.stone_weight_type.pk
                                                    stone_dict['stone_rate']=return_stone.stone_rate
                                                    stone_dict['stone_rate_type']=return_stone.stone_rate_type.pk
                                                    stone_dict['include_stone_weight']=return_stone.include_stone_weight
                                                    stone_dict['total_stone_value']=return_stone.total_stone_value

                                                    billing_return_stone_serializer=BillingReturnStoneDetailsSerializer(data=stone_dict)
                                                    if billing_return_stone_serializer.is_valid():
                                                        billing_return_stone_serializer.save()
                                                    else:
                                                        raise Exception (billing_return_stone_serializer.errors)
                                                
                                        except Exception as err: 
                                            raise Exception(err)

                                        try:
                                            
                                            return_diamond_queryset = BillingDiamondDetails.objects.filter(billing_details=bill_item_queryset.billing_details.pk,billing_item_details=bill_item_queryset.pk)
                                        
                                            if len(return_diamond_queryset) != 0:
                                                for return_diamond in return_diamond_queryset:

                                                    diamond_dict={}

                                                    diamond_dict['billing_details'] = return_items.get('billing_details')
                                                    diamond_dict['billing_return_item'] = return_serializer.data['id']
                                                    diamond_dict['diamond_name'] = return_diamond.diamond_name.pk
                                                    diamond_dict['diamond_pieces'] = return_diamond.diamond_pieces
                                                    diamond_dict['diamond_weight'] = return_diamond.diamond_weight
                                                    diamond_dict['diamond_weight_type'] = return_diamond.diamond_weight_type.pk
                                                    diamond_dict['diamond_rate'] = return_diamond.diamond_rate
                                                    diamond_dict['diamond_rate_type'] = return_diamond.diamond_rate_type.pk
                                                    diamond_dict['include_diamond_weight'] = return_diamond.include_diamond_weight

                                                    billing_return_diamond_serializer=BillingReturnDiamondDetailsSerializer(data=diamond_dict)
                                                    if billing_return_diamond_serializer.is_valid():
                                                        billing_return_diamond_serializer.save()
                                                    else:
                                                        raise Exception (billing_return_diamond_serializer.errors)
                                                
                                        except Exception as err:
                                            raise Exception(err)
                                        
                                    else:
                                        raise Exception (return_serializer.errors)
                                    
                                except Exception as err:
                                    raise Exception (err)
                                
                        # elif return_items.get('type') == settings.AUTOMATIC:
                        #     for return_items in sale_return_details:
                        #         try:
                        #             estimation_return_data={
                        #                 'billing_details': return_items.get('billing_details'),
                        #                 'return_bill_details' : bill_item_queryset.billing_details.pk,
                        #                 'return_items' : bill_item_queryset.pk,
                        #                 'tag_number' : bill_item_queryset.tag_number,
                        #                 'item_details': bill_item_queryset.item_details.pk,
                        #                 'sub_item_details': bill_item_queryset.sub_item_details.pk,
                        #                 'metal': bill_item_queryset.metal.pk,
                        #                 'net_weight':bill_item_queryset.net_weight,
                        #                 'gross_weight':bill_item_queryset.gross_weight,
                        #                 'tag_weight':bill_item_queryset.tag_weight,
                        #                 'cover_weight':bill_item_queryset.cover_weight,
                        #                 'loop_weight':bill_item_queryset.loop_weight,
                        #                 'other_weight':bill_item_queryset.other_weight,
                        #                 'pieces':bill_item_queryset.pieces,
                        #                 'total_pieces':bill_item_queryset.total_pieces,
                        #                 'rate' : bill_item_queryset.rate,
                        #                 'stone_rate' : bill_item_queryset.stone_rate,
                        #                 'diamond_rate' : bill_item_queryset.diamond_rate,
                        #                 'stock_type' : bill_item_queryset.stock_type.pk,
                        #                 'calculation_type' : bill_item_queryset.calculation_type.pk,
                        #                 'tax_percent' : bill_item_queryset.tax_percent,
                        #                 'additional_charges' : bill_item_queryset.additional_charges,
                        #                 'total_stone_weight' : bill_item_queryset.total_stone_weight,
                        #                 'total_diamond_weight' : bill_item_queryset.total_diamond_weight,
                        #                 'per_gram_weight_type' : bill_item_queryset.per_gram_weight_type.pk if bill_item_queryset.per_gram_weight_type else None,
                        #                 'wastage_percentage' : bill_item_queryset.wastage_percentage,
                        #                 'flat_wastage' : bill_item_queryset.flat_wastage,
                        #                 'making_charge' : bill_item_queryset.making_charge,
                        #                 'flat_making_charge' : bill_item_queryset.flat_making_charge,
                        #                 'wastage_calculation_type': bill_item_queryset.wastage_calculation_type.pk if bill_item_queryset.wastage_calculation_type else None,
                        #                 'making_charge_calculation_type': bill_item_queryset.making_charge_calculation_type.pk if bill_item_queryset.making_charge_calculation_type else None,
                        #                 'gst' : bill_item_queryset.gst,
                        #                 'total_rate' : bill_item_queryset.total_rate,
                        #                 'without_gst_rate' : bill_item_queryset.without_gst_rate,
                        #                 'huid_rate':bill_item_queryset.huid_rate
                        #             }   
                                    
                        #             return_serializer=BillingSaleReturnItemsSerializer(data=estimation_return_data)

                        #             if return_serializer.is_valid():
                        #                 return_serializer.save()
                        #             else:
                        #                 raise Exception (return_serializer.errors)
                                    
                                # except Exception as err:
                                #     raise Exception (err)
                                

                    payment_details=request_data.get('payment_particulars') if request_data.get('payment_particulars') else {}
                    today = date.today()
                    if len(payment_details) != 0:
                        for data in payment_details:
                            payment_data = {}
                            payment_data = {
                                'customer_details': data.get('customer_details'),
                                'payment_date': timezone.now(),
                                'payment_method' : data.get('payment_method'),
                                'payment_provider' : data.get('payment_provider') if data.get('payment_provider') != None else None,
                                'payment_module': data.get('payment_module'),
                                'refference_number': data.get('refference_number'),
                                'paid_amount': 0 if data.get('paid_amount') is None else float(data.get('paid_amount')),
                                'payment_refference_number' : data.get('payment_refference_number'),
                                'created_at' : timezone.now(),
                                'created_by' : request.user.id
                            }
                            
                            payment_table_serializer=CustomerPaymentTabelSerializer(data=payment_data)

                            if payment_table_serializer.is_valid():
                                payment_table_serializer.save()
                                
                                payment_queryset = CustomerPaymentTabel.objects.filter(refference_number=payment_table_serializer.data['refference_number']).aggregate(total_paid=Sum('paid_amount'))
                                paid_amount = payment_queryset['total_paid'] if payment_queryset['total_paid'] else 0
                                
                                if paid_amount == payment_serializer.data['payable_amount']:
                                    payment_status = settings.PAID
                                elif paid_amount > 0 and paid_amount < payment_serializer.data['payable_amount']:
                                    payment_status = settings.PARTIALLY_PAID
                                elif paid_amount == 0:
                                    payment_status = settings.PAYMENT_PENDING
                                print(payment_status)
                                
                                update_data = {}
                                if request_data.get('payment_module') == 3:
                                    update_data = {
                                        'payment_status' : payment_status,
                                        'is_issued' : is_issued if is_issued != None else None,
                                        'modified_at' : timezone.now(),
                                        'modified_by' : request.user.id
                                    }
                                else:
                                    update_data = {
                                        'payment_status' : payment_status,
                                        'modified_at' : timezone.now(),
                                        'modified_by' : request.user.id
                                    }
                                
                                if request_data.get('payment_module') == 1:
                                    queryset = OrderDetails.objects.get(order_id__order_id=data.get('refference_number'))
                                    serializer = OrderDetailsSerializer(queryset,data=update_data,partial=True)
                                    if serializer.is_valid():
                                        serializer.save()
                                    else:
                                        raise Exception(serializer.errors)
                                    
                                elif request_data.get('payment_module') == 2:
                                    queryset = RepairDetails.objects.get(repair_number=data.get('refference_number'))
                                    serializer = RepairDetailsSerializer(queryset,data=update_data,partial=True)
                                    if serializer.is_valid():
                                        serializer.save()
                                    else:
                                        raise Exception(serializer.errors)
                                
                                elif request_data.get('payment_module') == 3:
                                    queryset = BillingDetails.objects.get(bill_no=data.get('refference_number'))
                                    serializer = BillingDetailsSerializer(queryset,data=update_data,partial=True)
                                    if serializer.is_valid():
                                        serializer.save()
                                    else:
                                        raise Exception(serializer.errors)
                                    
                            else:
                                raise Exception(payment_table_serializer.errors)
                    return Response(
                        {
                            "message":res_msg.create('Payment Details'),
                            "status":status.HTTP_201_CREATED    
                        },status=status.HTTP_200_OK
                    )
                else:
                    raise Exception(payment_serializer.errors)
            else:
                return Response(
                    {
                        "data" : "Given reference number not exists please check!",
                        "message":res_msg.something_else(),
                        "status":status.HTTP_400_BAD_REQUEST    
                    },status=status.HTTP_200_OK
                )
        except Exception as err:
            return Response(
                {
                    "data" : str(err),
                    "message":res_msg.something_else(),
                    "status":status.HTTP_400_BAD_REQUEST    
                },status=status.HTTP_200_OK
            )
        
def check_and_process_reference_number(reference_number):
    try:
        
        if OrderDetails.objects.filter(order_id__order_id=reference_number).exists():
            return True
        elif RepairDetails.objects.filter(repair_number=reference_number).exists():
            return True
        elif BillingDetails.objects.filter(bill_no=reference_number).exists():
            return True
        else:
            return False
    except Exception as err:
        raise Exception(f"An error occurred while checking the reference number: {err}")
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class PaymentModuleListView(APIView):

    def get(self,request):

        queryset = PaymentModule.objects.all()
        serializer = PaymentModuleSerializer(queryset,many=True)
        
        return Response(
            {
                "data":{
                    "list":serializer.data
                },
                "message":res_msg.retrieve('Payment Module Details List'),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
