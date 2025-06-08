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
from django.db.models import ProtectedError, Sum
from django.db.models import Q
from rest_framework import filters
from books.models import *
import random
from django.conf import settings
from django.core.paginator import Paginator
from tagging .models import *
from tagging.serializer import *
from product.models import *
from product.serializer import *
from advance_payment.models import *
from advance_payment.serializer import *
from customer.serializer import *
from masters.serializer import *
from datetime import datetime
from approval.models import *
from approval.serializer import *
from accounts.models import *
from settings.models import *
from organizations.serializer import *
import requests
from django.db import transaction
from payment_management.models import *
from payment_management.serializer import *
from repair_management.models import *
from stock.serializer import StockLedgerSerializer
from old_gold_management.serializer import OldGoldBillDetailsSerializer
from customer.serializer import CustomerLedgerSerializer
from advance_payment.serializer import AdvanceDetailsSerializer, AdvanceLogsSerializer
from advance_payment.models import AdvanceLogs
from suspense_management.serializer import SuspenseDetailsSerializer
from suspense_management.models import SuspenseItemDetails


# Create your views here.
res_msg = ResponseMessages()

# Generate Estimate Number
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class EstimationNumberGenerateAPIView(APIView):
    def get(self,request):
        prefix = 'EST'  # Prefix for the estimate number
        # timestamp = datetime.now().strftime('%Y%m%d%H%M%S')  # Current date and time
        random_number = random.randint(1000000, 9999999)
        estimate_number = f'{prefix}-{random_number}'

        return Response(
            {
                "data": estimate_number,
                "message" : res_msg.create("Estimation Number"),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK
        )  

def DeleteEstimation(pk):
    
    try:

        queryset=EstimateDetails.objects.get(id=pk)
        queryset.delete()

    except Exception as err:
        pass

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class EstimationAPIView(APIView):
    def get(self,request,pk):
        if pk != None:
            estimation_details = {}
            try:
                    
                filter_dict={}
                filter_dict['id'] = pk
                
                try:
                    queryset = EstimateDetails.objects.get(**filter_dict)
                    serializer = EstimateDetailsSerializer(queryset)
                    estimation_details.update(serializer.data)
                except EstimateDetails.DoesNotExist:
                    return Response(
                    {
                        "message" : res_msg.not_exists('Estimate Details'),
                        "status": status.HTTP_204_NO_CONTENT,                        
                    }, status=status.HTTP_200_OK
                )  

                customer_details = []
                try:
                    customer_queryset = Customer.objects.get(id=queryset.customer_details.pk,is_active=True)
                    customer_serializer = CustomerSerializer(customer_queryset)
                    customer_details = customer_serializer.data
                except Exception as err:
                    return Response(
                        {
                            "message" : res_msg.not_exists('Customer'),
                            "status": status.HTTP_204_NO_CONTENT
                        }, status=status.HTTP_200_OK
                    )
                
                particulars = []
                estimate_tag_item_queryset = EstimationTagItems.objects.filter(estimation_details=pk)
                
                for item in estimate_tag_item_queryset:
                    
                    tag_details={
                        'id':item.pk,
                        'flat_making_charge':item.flat_making_charge,
                        'flat_wastage':item.flat_wastage,
                        'gross_weight':item.gross_weight,
                        'gst':item.gst,
                        'item_details':item.item_details.pk,
                        'item':item.item_details.item_name,
                        'jewel_type':item.metal.metal_name,
                        'making_charge':item.making_charge,
                        'metal':item.metal.pk,
                        'metal_rate':item.rate,
                        'net_weight':item.net_weight,
                        'pieces':item.pieces,
                        'rate':item.total_amount,
                        'stock_type':item.stock_type.pk,
                        'stock_type_name':item.stock_type.stock_type_name,
                        'calculation_type':item.calculation_type.pk,
                        'calculation_type_name':item.calculation_type.calculation_name,
                        'stone_rate':item.stone_rate,
                        'diamond_rate':item.diamond_rate,
                        'sub_item_details':item.sub_item_details.pk,
                        'sub_item_name':item.sub_item_details.sub_item_name,
                        'tag_item_id':item.estimation_tag_item.pk,
                        'tag_number':item.estimation_tag_item.tag_number,
                        'gst_percent':item.gst_percent,
                        'total_diamond_weight':item.total_diamond_weight,
                        'total_pieces':item.total_pieces,
                        'total_stone_weight':item.total_stone_weight,
                        'wastage_percent':item.wastage_percentage,
                        "item_huid_rate":item.huid_rate,
                        "with_gst_rate":item.with_gst_total_rate,
                        "employee_id":item.employee_id.pk,
                        "employee_name":item.employee_id.staff_id,
                    }

                    if str(item.calculation_type.pk) == settings.FIXEDRATE:
                        tag_details['min_metal_rate'] = item.estimation_tag_item.min_fixed_rate
                        tag_details['max_metal_rate'] = item.estimation_tag_item.max_fixed_rate

                    elif str(item.calculation_type.pk) == settings.WEIGHTCALCULATION:

                        subitem_weight_queryset=SubItemWeightCalculation.objects.get(sub_item_details=item.estimation_tag_item.sub_item_details.pk)
                        
                        tag_details['wastage_calculation_type'] = subitem_weight_queryset.wastage_calculation.pk
                        tag_details['wastage_calculation_name'] = subitem_weight_queryset.wastage_calculation.weight_name
                        
                        tag_details['making_charge_calculation_type'] = subitem_weight_queryset.making_charge_calculation.pk
                        tag_details['making_charge_calculation_name'] = subitem_weight_queryset.making_charge_calculation.weight_name

                        tag_details['min_wastage_percent'] = item.estimation_tag_item.min_wastage_percent
                        tag_details['min_wastage_percent'] = item.estimation_tag_item.min_wastage_percent
                        tag_details['min_flat_wastage'] = item.estimation_tag_item.min_flat_wastage
                        tag_details['max_wastage_percent'] = item.estimation_tag_item.max_wastage_percent
                        tag_details['max_flat_wastage'] = item.estimation_tag_item.max_flat_wastage
                        tag_details['min_making_charge'] = item.estimation_tag_item.min_making_charge_gram
                        tag_details['min_flat_making_charge'] = item.estimation_tag_item.min_flat_making_charge
                        tag_details['max_making_charge'] = item.estimation_tag_item.max_making_charge_gram
                        tag_details['max_flat_making_charge'] = item.estimation_tag_item.max_flat_making_charge

                    elif str(item.calculation_type.pk) == settings.PERGRAMRATE:

                        tag_details['min_metal_rate'] = item.estimation_tag_item.min_pergram_rate
                        tag_details['max_metal_rate'] = item.estimation_tag_item.max_pergram_rate
                        tag_details['per_gram_weight_type'] = item.estimation_tag_item.per_gram_weight_type.pk
                        tag_details['per_gram_weight_type_name'] = item.estimation_tag_item.per_gram_weight_type.weight_name

                    elif str(item.calculation_type.pk) == settings.PERPIECERATE:
                        # subitem_piece_queryset=SubItemPerPiece.objects.get(sub_item_details=item.estimation_tag_item.sub_item_details.pk)
                        tag_details['min_per_piece_rate'] = item.estimation_tag_item.min_per_piece_rate
                        tag_details['per_piece_rate'] = item.estimation_tag_item.per_piece_rate

                    try:
                        tax_queryset = TaxDetailsAudit.objects.filter(metal=item.metal.pk).order_by('-id').first()
                        if tax_queryset:
                            tax_percent_queryset = SalesTaxDetails.objects.get(tax_details=tax_queryset.tax_details)
                            tag_details['sales_tax_igst']=tax_percent_queryset.sales_tax_igst
                            tag_details['sales_tax_cgst']=tax_percent_queryset.sales_tax_cgst
                            tag_details['sales_tax_sgst']=tax_percent_queryset.sales_tax_sgst
                            tag_details['sales_surcharge_percent']=tax_percent_queryset.sales_surcharge_percent
                            tag_details['sales_additional_charges'] = tax_percent_queryset.sales_additional_charges
                    except Exception as err:
                        tag_details['sales_tax_igst']=0
                        tag_details['sales_tax_cgst']=0
                        tag_details['sales_tax_sgst']=0
                        tag_details['sales_surcharge_percent']=0
                        tag_details['sales_additional_charges'] = 0
                    # if item.per_gram_weight_type != None:
                    #     tag_details['per_gram_weight_type']=item.estimation_tag_item.per_gram_weight_type.pk if item.estimation_tag_item.per_gram_weight_type.pk is not None else None,
                    #     tag_details['per_gram_weight_type_name'] = item.estimation_tag_item.per_gram_weight_type.weight_name if item.estimation_tag_item.per_gram_weight_type.weight_name is not None else None
                    
                    stone_queryset=EstimationStoneDetails.objects.filter(estimation_details=pk,estimation_item_details=item.pk)
                    stone_details=[]
                    
                    for stone in stone_queryset:
                        stone_data={
                            'id' : stone.pk,
                            'stone_name':stone.stone_name.pk,
                            'stone_pieces':stone.stone_pieces,
                            'stone_weight':stone.stone_weight,
                            'stone_weight_type':stone.stone_weight_type.pk,
                            'stone_weight_type_name':stone.stone_weight_type.weight_name,
                            'stone_rate':stone.stone_rate,
                            'stone_rate_type':stone.stone_rate_type.pk,
                            'stone_rate_type_name':stone.stone_rate_type.type_name,
                            'include_stone_weight':stone.include_stone_weight
                        }

                        if str(stone.stone_weight_type.pk) == settings.CARAT:
                            stone_data['stone_weight'] = float(stone.stone_weight)*5

                        else:
                            stone_data['stone_weight'] = float(stone.stone_weight)

                        if str(stone.stone_rate_type.pk) == settings.PERCARAT:
                            stone_data['stone_rate'] = float(stone.stone_rate)/5

                        elif str(stone.stone_rate_type.pk) == settings.PERPIECE:
                            stone_data['stone_rate'] = float(stone.stone_rate)
                        else:
                            stone_data['stone_rate'] = float(stone.stone_rate)

                        stone_details.append(stone_data)
                    tag_details['stone_details']=stone_details
                    
                    diamond_queryset=EstimationDiamondDetails.objects.filter(estimation_details=pk,estimation_item_details=item.pk)
                    diamond_details=[]
                    
                    for diamond in diamond_queryset:
                        diamond_data={
                            'id' : diamond.pk,
                            'diamond_name':diamond.diamond_name.pk,
                            'diamond_pieces':diamond.diamond_pieces,
                            'diamond_weight':diamond.diamond_weight,
                            'diamond_weight_type':diamond.diamond_weight_type.pk,
                            'diamond_weight_type_name':diamond.diamond_weight_type.weight_name,
                            'diamond_rate':diamond.diamond_rate,
                            'diamond_rate_type':diamond.diamond_rate_type.pk,
                            'diamond_rate_type_name':diamond.diamond_rate_type.type_name,
                            'include_diamond_weight':diamond.include_diamond_weight
                        }

                        if str(diamond.diamond_weight_type.pk) == settings.CARAT:
                            diamond_data['diamond_weight'] = float(diamond.diamond_weight)*5

                        else:
                            diamond_data['diamond_weight'] = float(diamond.diamond_weight)

                        if str(diamond.diamond_rate_type.pk) == settings.PERCARAT:
                            diamond_data['diamond_rate'] = float(diamond.diamond_rate)/5

                        else:
                            diamond_data['diamond_rate'] = float(diamond.diamond_rate)

                        diamond_details.append(diamond_data)


                    tag_details['diamond_details']=diamond_details
                    
                    particulars.append(tag_details)
                    
                estimation_details['tag_item_details']=particulars
                
                old_gold_details=[]
                old_gold_queryset = EstimationOldGold.objects.filter(estimation_details=pk)
                
                for old_gold in old_gold_queryset:
                    old_details={
                        'id':old_gold.pk,
                        'old_gold_no':old_gold.old_gold_no,
                        'old_dust_weight':old_gold.old_dust_weight,
                        'old_gross_weight':old_gold.old_gross_weight,
                        'old_metal':old_gold.old_metal.pk,
                        'metal_name':old_gold.old_metal.metal_name,
                        'old_touch':old_gold.old_touch,
                        'old_net_weight':old_gold.old_net_weight,
                        'old_rate':old_gold.old_rate,
                        'old_amount':old_gold.old_amount,
                        'total_amount':old_gold.total_amount,
                        'employee_id':old_gold.employee_id.pk,
                        'employee_name':old_gold.employee_id.staff_id
                    }
                   
                    old_gold_details.append(old_details)
                    
                estimation_details["old_item_details"] = old_gold_details

                estimation_return_details = []

                estimation_return_queryset = EstimationSaleReturnItems.objects.filter(estimation_details=pk)
                
                for return_item in estimation_return_queryset:

                    return_details={
                        'id':return_item.pk,
                        'estimation_details': return_item.estimation_details.pk,
                        'bill_details' : return_item.bill_details.pk if return_item.bill_details is not None else None,
                        'return_items' : return_item.return_items.pk if return_item.return_items is not None else None,
                        'tag_number' : return_item.tag_number if return_item.tag_number is not None else None,
                        'item_details': return_item.item_details.pk,
                        'item_details_name': return_item.item_details.item_name,
                        'sub_item_details': return_item.sub_item_details.pk,
                        'sub_item_details_name': return_item.sub_item_details.sub_item_name,
                        'metal': return_item.metal.pk,
                        'metal_name': return_item.metal.metal_name,
                        'net_weight':return_item.net_weight,
                        'gross_weight':return_item.gross_weight,
                        'tag_weight':return_item.tag_weight,
                        'cover_weight':return_item.cover_weight,
                        'loop_weight':return_item.loop_weight,
                        'other_weight':return_item.other_weight,
                        'pieces':return_item.pieces,
                        'total_pieces':return_item.total_pieces,
                        'metal_rate' : return_item.rate,
                        'rate':return_item.without_gst_rate,
                        'stone_rate' : return_item.stone_rate,
                        'diamond_rate' : return_item.diamond_rate,
                        'stock_type' : return_item.stock_type.pk,
                        'calculation_type' : return_item.calculation_type.pk,
                        'tax_percent' : return_item.tax_percent,
                        'additional_charges' : return_item.additional_charges,
                        'total_stone_weight' : return_item.total_stone_weight,
                        'total_diamond_weight' : return_item.total_diamond_weight,
                        'per_gram_weight_type' : return_item.per_gram_weight_type.pk if return_item.per_gram_weight_type is not None else None,
                        'per_gram_weight_type_name' : return_item.per_gram_weight_type.weight_name if return_item.per_gram_weight_type is not None else None,
                        'wastage_percentage' : return_item.wastage_percentage,
                        'flat_wastage' : return_item.flat_wastage,
                        'making_charge' : return_item.making_charge,
                        'flat_making_charge' : return_item.flat_making_charge,
                        'wastage_calculation_type': return_item.wastage_calculation_type.pk,
                        'wastage_calculation_type_name': return_item.wastage_calculation_type.weight_name,
                        'making_charge_calculation_type': return_item.making_charge_calculation_type.pk,
                        'making_charge_calculation_type_name': return_item.making_charge_calculation_type.weight_name,
                        'gst' : return_item.gst,
                        'without_gst_rate' : return_item.without_gst_rate,
                        'total_rate' : return_item.total_rate,
                        'huid_rate':return_item.huid_rate,
                    }

                    stone_return_details=[]

                    return_stone_queryset = EstimationReturnStoneDetails.objects.filter(estimation_details=pk,estimation_return_item=return_item.pk)

                    for return_stone in return_stone_queryset:

                        stone_details_return={
                            "id":return_stone.pk,
                            "estimation_details":return_stone.estimation_details.pk,
                            "estimation_return_item":return_stone.estimation_return_item.pk,
                            "stone":return_stone.stone_name.pk,
                            "stone_name":return_stone.stone_name.stone_name,
                            "stone_pieces":return_stone.stone_pieces,
                            "stone_weight":return_stone.stone_weight,
                            "stone_weight_type":return_stone.stone_weight_type.pk,
                            "stone_weight_type_name":return_stone.stone_weight_type.weight_name,
                            "stone_rate":return_stone.stone_rate,
                            "stone_rate_type":return_stone.stone_rate_type.pk,
                            "stone_rate_type_name":return_stone.stone_rate_type.type_name,
                            "include_stone_weight":return_stone.include_stone_weight,
                            "total_stone_value":return_stone.total_stone_value
                        }

                        stone_return_details.append(stone_details_return)

                    return_details['stone_details'] = stone_return_details

                    diamond_return_details=[]

                    return_diamond_queryset = EstimationReturnDiamondDetails.objects.filter(estimation_details=pk,estimation_return_item=return_item.pk)

                    for return_diamond in return_diamond_queryset:

                        diamond_details_return={

                            "id":return_diamond.pk,
                            "estimation_details":return_diamond.estimation_details.pk,
                            "estimation_return_item":return_diamond.estimation_return_item.pk,
                            "diamond":return_diamond.diamond_name.pk,
                            "diamond_name":return_diamond.diamond_name.stone_name,
                            "diamond_pieces":return_diamond.diamond_pieces,
                            "diamond_weight":return_diamond.diamond_weight,
                            "diamond_weight_type":return_diamond.diamond_weight_type.pk,
                            "diamond_weight_type_name":return_diamond.diamond_weight_type.weight_name,
                            "diamond_rate":return_diamond.diamond_rate,
                            "diamond_rate_type":return_diamond.diamond_rate_type.pk,
                            "diamond_rate_type_name":return_diamond.diamond_rate_type.type_name,
                            "include_diamond_weight":return_diamond.include_diamond_weight,
                            "total_diamond_value":return_diamond.total_diamond_value
                        }

                        diamond_return_details.append(diamond_details_return)

                    return_details['diamond_details'] = diamond_return_details

                    estimation_return_details.append(return_details)
                    print(estimation_return_details)
                estimation_details['estimation_return_details'] = estimation_return_details


                old_purchase_queryset = EstimationOldPurchaseDetails.objects.filter(estimation_details=queryset.pk)
                
                old_purchase_details = []
                
                for old_purchase in old_purchase_queryset:
                    
                    old_purchase_serializer = EstimationOldPurchaseDetailsSerializer(old_purchase)
                    
                    old_purchase_data = old_purchase_serializer.data
                    
                    old_purchase_data['old_bill_number'] = old_purchase.old_purchase_details.old_gold_bill_number
                    
                    old_purchase_details.append(old_purchase_data)
                    
                estimation_details['old_purchase_details'] = old_purchase_details

                
                advance_queryset = EstimationAdvanceDetails.objects.filter(estimation_details=queryset.pk)
                
                advance_details = []
                
                for advance in advance_queryset:
                    
                    advance_serializer = EstimationAdvanceDetailsSerializer(advance)
                    
                    advance_data = advance_serializer.data
                    
                    advance_data['advance_id'] = advance.advance_details.advance_id
                    
                    advance_details.append(advance_data)
                    
                estimation_details['advance_details'] = advance_details


                chit_queryset = EstimationChitDetails.objects.filter(estimation_details=queryset.pk)
                
                chit_serializer = EstimationChitDetailsSerializer(chit_queryset,many=True)
                
                estimation_details['chit_details'] = chit_serializer.data
                
            except Exception as err:

                return Response(
                    {
                        "data":str(err),
                        "message" : res_msg.something_else(),
                        "status": status.HTTP_204_NO_CONTENT,                        
                    }, status=status.HTTP_200_OK
            )  

            return Response(
                {
                    "data":{
                        "customer_details" : customer_details,
                        "estimation_details": estimation_details,
                    },
                    "message" : res_msg.retrieve("Estimate details"),
                    "status": status.HTTP_200_OK
                }, status=status.HTTP_200_OK
            )  
        else:
            return Response(
                {
                    "message" : "Invalid Estimate Number",
                    "status": status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_200_OK
            )  
        
    @transaction.atomic   
    def post(self,request):
        try:
            data = request.data

            if request.user.role.is_admin == True:
                branch = data.get('branch')
                
            else:
                branch = request.user.branch.pk

            res_data={
                'branch':branch,
                'estimate_no':data.get('estimation_no'),
                'bill_type':data.get('bill_type'),
                'estimation_date':data.get('estimation_date'),
                'customer_details':data.get('customer_details'),
                # 'estimation_status' : estimation_status,
                'total_amount':data.get('total_amount'),
                'discount_percentage':data.get('discount_percentage'),
                'discount_amount':data.get('discount_amount'),
                'stone_amount':data.get('stone_amount'),
                'diamond_amount':data.get('diamond_amount'),
                'chit_amount':data.get('chit_amount'),
                'salereturn_amount':data.get('salereturn_amount'),
                'exchange_amount':data.get('exchange_amount'),
                'gst_percentage':data.get('gst_percentage'),
                'gst_amount':data.get('gst_amount'),
                'gst_type':data.get('gst_type'),
                'payable_amount':data.get('payable_amount'),
                'advance_amount':data.get('advance_amount'),
                'balance_amount':data.get('balance_amount'),
            }
            
            res_data['created_at'] = timezone.now()
            res_data['created_by'] = request.user.id

            serializer = EstimateDetailsSerializer(data=res_data)
            if serializer.is_valid():
                
                serializer.save()
                estimation_details = serializer.data

                if int(res_data['bill_type']) == 1:
                    estimation_id_dict={}
                    estimation_id_dict['gold_estimation_id']=serializer.data['estimate_no']
                    estimation_number_serializer = GoldEstimationIDSerializer(data=estimation_id_dict)

                    if estimation_number_serializer.is_valid():
                        estimation_number_serializer.save()
                elif int(res_data['bill_type']) == 2:

                    estimation_id_dict={}
                    estimation_id_dict['silver_estimation_id']=serializer.data['id']
                    estimation_number_serializer = SilverEstimationIDSerializer(data=estimation_id_dict)

                    if estimation_number_serializer.is_valid():
                        estimation_number_serializer.save()
                
                else:
                    pass

                oldgold_details = request.data.get('old_gold_particulars', {})
                new_oldgold_data = {}
                new_oldgold_data['old_gold_no']=request.data.get('old_gold_no')
                if len(oldgold_details) != 0:
                    for oldgold in oldgold_details:
                        try:
                            new_oldgold_data['old_metal']=oldgold['metal']
                            new_oldgold_data['metal_rate']=oldgold['metal_rate']
                            new_oldgold_data['old_gross_weight']=oldgold['gross_weight']
                            new_oldgold_data['old_net_weight']=oldgold['net_weight']
                            new_oldgold_data['dust_weight']=oldgold['dust_weight']
                            new_oldgold_data['estimation_details']=serializer.data['id']
                            # new_oldgold_data['old_metal_rate']=oldgold['old_rate']
                            # new_oldgold_data['today_metal_rate']=oldgold['today_rate']
                            new_oldgold_data['total_old_gold_value']=oldgold['total']
                            # new_oldgold_data['purity']=oldgold['purity']
                            new_oldgold_data['employee_id']=oldgold['employee_id']

                            oldgold_serializer = EstimationOldGoldSerializer(data=new_oldgold_data)
                            if oldgold_serializer.is_valid():
                                oldgold_serializer.save()
                            else:
                                raise Exception(oldgold_serializer.errors)
                            
                        except Exception as error:
                            raise Exception(error)
                        
                estimation_item_details = request.data.get('particulars', [])
                
                if len(estimation_item_details) != 0:
                    for item in estimation_item_details:
                        try:

                            tag_number=item.get('tag_number')

                            tag_queryset=TaggedItems.objects.get(tag_number=tag_number)
                            estimation_tag_data = {
                                'estimation_details': estimation_details['id'],
                                'estimation_tag_item': tag_queryset.pk,
                                'tag_number': item.get('tag_number'),
                                'item_details': item.get('item_details'),
                                'sub_item_details': item.get('sub_item_details'),
                                'metal': item.get('metal'),
                                'net_weight': item.get('net_weight'),
                                'gross_weight' : item.get('gross_weight'),
                                'tag_weight' : item.get('tag_weight'),
                                'cover_weight' : item.get('cover_weight'),
                                'loop_weight' : item.get('loop_weight'),
                                'other_weight' : item.get('other_weight'),
                                'pieces' : item.get('pieces'),
                                'total_pieces' : item.get('total_pieces'),
                                'rate' : item.get('metal_rate'),
                                'stone_rate' : item.get('stone_rate'),
                                'diamond_rate' : item.get('diamond_rate'),
                                'stock_type' : item.get('stock_type'),
                                'calculation_type' : item.get('calculation_type'),
                                'tax_percent' : item.get('tax_percent'),
                                'additional_charges' : item.get('additional_charges'),
                                'total_stone_weight' : item.get('total_stone_weight'),
                                'total_diamond_weight' : item.get('total_diamond_weight'),
                                'per_gram_weight_type' : item.get('per_gram_weight_type',None),
                                'wastage_percentage' : item.get('wastage_percent', None),
                                'flat_wastage' : item.get('flat_wastage', None),
                                'making_charge' : item.get('making_charge', None),
                                'flat_making_charge' : item.get('flat_making_charge', None),
                                'wastage_calculation_type': item.get('wastage_calculation_type', None),
                                'making_charge_calculation_type': item.get('making_charge_calculation_type', None),
                                'gst' : item.get('gst'),
                                'total_rate' : item.get('with_gst_rate'),
                                'without_gst_rate':item.get('rate'),
                                'huid_rate':item.get('item_huid_rate')
                            }
                            
                            estimation_taggeditem_serializer = EstimationTagItemsSerializer(data=estimation_tag_data)
                            if estimation_taggeditem_serializer.is_valid():
                                estimation_taggeditem_serializer.save()

                                stone_details=item.get('stone_details') if item.get('stone_details') else []

                                for stone in stone_details:
                                    stone['estimation_details'] = estimation_details['id']
                                    stone['estimation_item_details'] = estimation_taggeditem_serializer.data['id']
                                    stone['stone_name']=float(stone['stone_name'])
                                    stone['stone_pieces']=float(stone['stone_pieces'])
                                    stone['stone_weight']=float(stone['stone_weight'])
                                    stone['stone_weight_type']=int(stone['stone_weight_type'])
                                    stone['stone_rate']=float(stone['stone_rate'])
                                    stone['stone_rate_type']=int(stone['stone_rate_type'])
                                    stone['include_stone_weight']=stone['include_stone_weight']

                                    if int(stone['stone_weight_type']) == int(settings.CARAT):
                                        stone['stone_weight']=(float(stone['stone_weight'])/5)

                                    if int(stone['stone_rate_type']) == int(settings.PERGRAM):
                                        total_stone_value=float(stone['stone_rate']*stone['stone_weight'])
                                        stone['total_stone_value']=total_stone_value
                                    
                                    if int(stone['stone_rate_type']) == int(settings.PERCARAT):
                                        stone_rate = float(stone['stone_rate'])*5
                                        stone['stone_rate'] = stone_rate
                                        total_stone_value=float(stone['stone_rate']*stone['stone_weight'])
                                        stone['total_stone_value']=total_stone_value

                                    if int(stone['stone_rate_type']) == int(settings.PERPIECE):
                                        total_stone_value=float(stone['stone_rate']*stone['stone_pieces'])
                                        stone['total_stone_value']=total_stone_value

                                    estimation_stone_serializer=EstimationStoneDetailsSerializer(data=stone)
                                    if estimation_stone_serializer.is_valid():
                                        estimation_stone_serializer.save()
                                    else:
                                        raise Exception (estimation_stone_serializer.errors)

                                diamond_details=item.get('diamond_details') if item.get('diamond_details') else []

                                for diamond in diamond_details :

                                    diamond['estimation_details'] = estimation_details['id']
                                    diamond['estimation_item_details'] = estimation_taggeditem_serializer.data['id']
                                    diamond['diamond_name'] = float(diamond['diamond_name'])
                                    diamond['diamond_pieces'] = float(diamond['diamond_pieces'])
                                    diamond['diamond_weight'] = float(diamond['diamond_weight'])
                                    diamond['diamond_weight_type'] = int(diamond['diamond_weight_type'])
                                    diamond['diamond_rate'] = float(diamond['diamond_rate'])
                                    diamond['diamond_rate_type'] = int(diamond['diamond_rate_type'])
                                    diamond['include_diamond_weight'] = diamond['include_diamond_weight']

                                    if int(diamond['diamond_weight_type']) == settings.CARAT :
                                        diamond_weight=float(diamond['diamond_weight'])/5
                                        diamond['diamond_weight']=diamond_weight

                                    if int(diamond['diamond_rate_type']) ==settings.PERGRAM:
                                        total_diamond_value=float(diamond['diamond_rate']*diamond['diamond_weight'])
                                        diamond['total_diamond_value'] = total_diamond_value

                                    if int(diamond['diamond_rate_type']) == settings.PERCARAT:
                                        diamond_rate=float(diamond['diamond_rate'])*5
                                        diamond['diamond_rate']=diamond_rate
                                        total_diamond_value=float(diamond['diamond_rate']*diamond['diamond_weight'])
                                        diamond['total_diamond_value'] = total_diamond_value

                                    if int(diamond['diamond_rate_type']) ==settings.PERPIECE:
                                        total_diamond_value=float(diamond['diamond_rate']*diamond['diamond_pieces'])
                                        diamond['total_diamond_value'] = total_diamond_value


                                    estimation_diamond_serializer=EstimationDiamondDetailsSerializer(data=diamond)
                                    if estimation_diamond_serializer.is_valid():
                                        estimation_diamond_serializer.save()
                                    else:
                                        raise Exception(estimation_diamond_serializer.errors)

                            else:
                                raise Exception(estimation_taggeditem_serializer.errors)
                        except Exception as err:
                            raise Exception(err)
                        
                estimation_return_details=request.data.get('estimation_return_details', [])

                if len(estimation_return_details) != 0:

                    for return_items in estimation_return_details:
                        try:
                            bill_item_queryset = BillingParticularDetails.objects.get(id=return_items)
                            estimation_return_data={
                                'estimation_details': estimation_details['id'],
                                'bill_details' : bill_item_queryset.billing_details.pk,
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
                                'per_gram_weight_type' : bill_item_queryset.per_gram_weight_type,
                                'wastage_percentage' : bill_item_queryset.wastage_percentage,
                                'flat_wastage' : bill_item_queryset.flat_wastage,
                                'making_charge' : bill_item_queryset.making_charge,
                                'flat_making_charge' : bill_item_queryset.flat_making_charge,
                                'wastage_calculation_type': bill_item_queryset.wastage_calculation_type.pk,
                                'making_charge_calculation_type': bill_item_queryset.making_charge_calculation_type.pk,
                                'gst' : bill_item_queryset.gst,
                                'total_rate' : bill_item_queryset.total_rate,
                                'without_gst_rate' : bill_item_queryset.without_gst_rate,
                                'huid_rate':bill_item_queryset.huid_rate
                            }   
                            return_serializer=EstimationSaleReturnItemsSerializer(data=estimation_return_data)


                            if return_serializer.is_valid():
                                return_serializer.save()

                                bill_item_queryset.is_returned = True

                                bill_item_queryset.save()

                                try:

                                    return_stone_queryset = BillingParticularStoneDetails.objects.filter(billing_details=bill_item_queryset.billing_details.pk,billing_item_details=bill_item_queryset.pk)

                                    for return_stone in return_stone_queryset:

                                        stone_dict={}

                                        stone_dict['estimation_details'] = estimation_details['id']
                                        stone_dict['estimation_return_item'] = return_serializer.data['id']
                                        stone_dict['stone_name']=return_stone.stone.pk
                                        stone_dict['stone_pieces']=return_stone.stone_pieces
                                        stone_dict['stone_weight']=return_stone.stone_weight
                                        stone_dict['stone_weight_type']=return_stone.stone_weight_type.pk
                                        stone_dict['stone_rate']=return_stone.stone_amount
                                        stone_dict['stone_rate_type']=return_stone.stone_rate_type.pk
                                        stone_dict['include_stone_weight']=return_stone.include_stone_weight
                                        stone_dict['total_stone_value']=return_stone.total_stone_value


                                        estimation_return_stone_serializer=EstimationReturnStoneDetailsSerializer(data=stone_dict)
                                        if estimation_return_stone_serializer.is_valid():
                                            estimation_return_stone_serializer.save()
                                        else:
                                            raise Exception (estimation_return_stone_serializer.errors)
                                        
                                except Exception as err: 
                                    raise Exception(err)

                                try:
                                    
                                    return_diamond_queryset = BillingParticularsDiamondDetails.objects.filter(billing_details=bill_item_queryset.billing_details.pk,billing_item_details=bill_item_queryset.pk)

                                    for return_diamond in return_diamond_queryset:

                                        diamond_dict={}

                                        diamond_dict['estimation_details'] = estimation_details['id']
                                        diamond_dict['estimation_return_item'] = return_serializer.data['id']
                                        diamond_dict['diamond_name'] = return_diamond.diamond.pk
                                        diamond_dict['diamond_pieces'] = return_diamond.diamond_pieces
                                        diamond_dict['diamond_weight'] = return_diamond.diamond_weight
                                        diamond_dict['diamond_weight_type'] = return_diamond.diamond_weight_type.pk
                                        diamond_dict['diamond_rate'] = return_diamond.diamond_amount
                                        diamond_dict['diamond_rate_type'] = return_diamond.diamond_rate_type.pk
                                        diamond_dict['include_diamond_weight'] = return_diamond.include_diamond_weight


                                        estimation_return_diamond_serializer=EstimationReturnDiamondDetailsSerializer(data=diamond_dict)
                                        if estimation_return_diamond_serializer.is_valid():
                                            estimation_return_diamond_serializer.save()
                                        else:
                                            raise Exception (estimation_return_diamond_serializer.errors)
                                        
                                except Exception as err:
                                    raise Exception(err)
                                
                            else:
                                raise Exception (return_serializer.errors)

                        except Exception as err:
                            raise Exception (err)
                StockReduceEstimation(serializer.data['id'])
                return Response(
                    {
                        "data":serializer.data,
                        "message":res_msg.create("Estimation Biling"),
                        "status":status.HTTP_201_CREATED
                    },status=status.HTTP_200_OK)
            
            else:
                raise Exception(serializer.errors)
        
        except Exception as err:
            
            # try:
            #     DeleteEstimation(serializer.data['id'])
            # except:
            #     pass

            transaction.set_rollback(True)

            return Response(
                {
                    "data":str(err),
                    "message":res_msg.something_else(),
                    "status":status.HTTP_204_NO_CONTENT
                },status=status.HTTP_200_OK
            )
        
    def delete(self,request,pk):
        DeleteEstimation(pk)
        return Response(
            {
                "message":res_msg.delete("Estimation Details"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
    

@transaction.atomic
def StockReduceEstimation(pk):
    try:
        # with transaction.atomic():
            estimation_items=list(EstimationTagItems.objects.filter(estimation_details=pk))
            for items in estimation_items:
                stock_queryset=TaggedItems.objects.get(tag_number=items.tag_number)
                
                if str(items.stock_type.pk) == settings.TAG:
                    stock_details={}
                    if stock_queryset.is_billed == False:

                        stock_details['remaining_pieces']=stock_queryset.remaining_pieces-int(items.pieces)
                        stock_details['remaining_gross_weight']=stock_queryset.remaining_gross_weight-float(items.gross_weight)
                        stock_details['remaining_net_weight']=stock_queryset.remaining_net_weight-float(items.net_weight)
                        stock_details['is_billed']=True

                        tag_item_serializer=TaggedItemsSerializer(stock_queryset,data=stock_details,partial=True)

                        if tag_item_serializer.is_valid():
                            tag_item_serializer.save()
                        else:
                            raise Exception(tag_item_serializer.errors)
                        
                    else:
                        raise Exception("The Item is already Billed")
                    
                elif str(items.stock_type.pk) == settings.NON_TAG:
                    
                    if stock_queryset.remaining_gross_weight >= items.gross_weight:

                        stock_details={}
                        stock_details['remaining_gross_weight']=float(stock_queryset.remaining_gross_weight)-(float(items.gross_weight))
                        stock_details['remaining_net_weight']=float(stock_queryset.remaining_net_weight)-(float(items.net_weight))

                        tag_item_serializer=TaggedItemsSerializer(stock_queryset,data=stock_details,partial=True)

                        if tag_item_serializer.is_valid():
                            tag_item_serializer.save()

                            if stock_queryset.remaining_gross_weight == 0:
                                stock_queryset.is_billed = True
                                stock_queryset.save()

                        else:
                            raise Exception(tag_item_serializer.errors)
                        
                    else:
                        raise Exception ("The ramining weight is"+str(stock_queryset.remaining_gross_weight)+'gm')
                    
                elif str(items.stock_type.pk) == settings.PACKET:


                    if stock_queryset.remaining_pieces >= items.pieces:

                        stock_details={}
                        stock_details['remaining_pieces']=int(stock_queryset.remaining_pieces)-(int(items.pieces))
                        

                        tag_item_serializer=TaggedItemsSerializer(stock_queryset,data=stock_details,partial=True)

                        if tag_item_serializer.is_valid():
                            tag_item_serializer.save()

                            if stock_queryset.remaining_pieces == 0:
                                stock_queryset.is_billed = not(stock_queryset.is_billed)
                                stock_queryset.save()

                        else:
                            raise Exception(tag_item_serializer.errors)
                    
                else:

                    raise Exception("The Remaining pieces is"+str(stock_queryset.remaining_pieces))
                
            return 1
    
    except Exception as err:
        # try:
        #     DeleteEstimation(pk)
        # except:
        #     pass

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
class EstimationWithoutStockReduceView(APIView):
    @transaction.atomic
    def post(self,request):

        try:

            data = request.data

            if request.user.role.is_admin == True:
                branch = data.get('branch')
            else:
                branch = request.user.branch.pk

            estimation_status = settings.PENDING

            res_data={
                'branch':branch,
                'estimate_no':data.get('estimation_no'),
                'bill_type':data.get('bill_type'),
                'estimation_date':data.get('estimation_date'),
                'customer_details':data.get('customer_details'),
                'total_amount':data.get('total_amount'),
                'discount_percentage':data.get('discount_percentage'),
                'discount_amount':data.get('discount_amount'),
                'chit_amount':data.get('chit_amount'),
                'salereturn_amount':data.get('salereturn_amount'),
                'exchange_amount':data.get('exchange_amount'),
                'gst_percentage':data.get('gst_percentage'),
                'gst_amount':data.get('gst_amount'),
                'gst_type':data.get('gst_type'),
                'payable_amount':data.get('payable_amount'),
                'advance_amount':data.get('advance_amount'),
                'balance_amount':data.get('balance_amount'),
                'sale_return_type':data.get('sale_return_type'),
            }
            
            res_data['created_at'] = timezone.now()
            res_data['created_by'] = request.user.id
            
            serializer = EstimateDetailsSerializer(data=res_data)
            if serializer.is_valid():
                serializer.save()
                estimation_details=serializer.data

                if int(res_data['bill_type']) == 1:
                    estimation_id_dict={}
                    estimation_id_dict['gold_estimation_id']=serializer.data['estimate_no']
                    estimation_number_serializer = GoldEstimationIDSerializer(data=estimation_id_dict)

                    if estimation_number_serializer.is_valid():
                        estimation_number_serializer.save()
                    
                elif int(res_data['bill_type']) == 2:

                    estimation_id_dict={}
                    estimation_id_dict['silver_estimation_id']=serializer.data['id']
                    estimation_number_serializer = SilverEstimationIDSerializer(data=estimation_id_dict)

                    if estimation_number_serializer.is_valid():
                        estimation_number_serializer.save()
                
                else:
                    pass

                oldgold_details = request.data.get('exchange_details', {})
                
                new_oldgold_data = {}
                new_oldgold_data['old_gold_no']=data['old_gold_no']
                if len(oldgold_details) != 0:
                    for oldgold in oldgold_details:
                        try:
                            new_oldgold_data['old_metal']=oldgold['old_metal']
                            new_oldgold_data['old_gross_weight']=oldgold['old_gross_weight']
                            new_oldgold_data['old_reduce_weight']=oldgold['old_reduce_weight']
                            new_oldgold_data['old_net_weight']=oldgold['old_net_weight']
                            new_oldgold_data['old_touch']=oldgold['old_touch']
                            new_oldgold_data['old_dust_weight']=oldgold['old_dust_weight']
                            new_oldgold_data['estimation_details']=serializer.data['id']
                            new_oldgold_data['old_rate']=oldgold['old_rate']
                            new_oldgold_data['old_amount']=oldgold['old_amount']
                            new_oldgold_data['gst_amount']=oldgold['gst_amount']
                            new_oldgold_data['total_amount']=oldgold['total_amount']
                            new_oldgold_data['employee_id']=oldgold['employee_id']
                            
                            oldgold_serializer = EstimationOldGoldSerializer(data=new_oldgold_data)
                            if oldgold_serializer.is_valid():
                                oldgold_serializer.save()
                            else:
                                raise Exception(oldgold_serializer.errors)
                            
                        except Exception as error:
                            raise Exception(error)
                        
                old_purchase_details = data.get('old_purchase_details',[])
                    
                for old_purchase in old_purchase_details:
                    
                    old_purchase_data = {}
                    
                    old_purchase_data['estimation_details'] = serializer.data['id']
                    old_purchase_data['old_purchase_details'] = old_purchase
                    
                    old_purchase_serializer = EstimationOldPurchaseDetailsSerializer(data=old_purchase_data)
                    
                    if old_purchase_serializer.is_valid():
                        
                        old_purchase_serializer.save()
                        
                    else:
                        transaction.set_rollback(True)
                        return Response(
                            {
                                "data":old_purchase_serializer.errors,
                                "message":res_msg.not_create("Estimation"),
                                "status":status.HTTP_400_BAD_REQUEST
                            },status=status.HTTP_200_OK
                        )
                        
                advance_details = data.get('advance_details',[])
                
                for advance in advance_details:
                    
                    advance['estimation_details'] = serializer.data['id']
                    
                    advance_serializer = EstimationAdvanceDetailsSerializer(data=advance)
                    
                    if advance_serializer.is_valid():
                        advance_serializer.save()
                        
                    else:
                        transaction.set_rollback(True)
                        return Response(
                            {
                                "data":advance_serializer.errors,
                                "message":res_msg.not_create("Estimation"),
                                "status":status.HTTP_400_BAD_REQUEST
                            },status=status.HTTP_200_OK
                        )
                    
                chit_details = data.get('chit_details',[])
            
                for chit in chit_details:
                    
                    chit['estimation_details'] = serializer.data['id']
                    
                    chit_serializer = EstimationChitDetailsSerializer(data=chit)
                    
                    if chit_serializer.is_valid():
                        chit_serializer.save()
                        
                    else:
                        transaction.set_rollback(True)
                        return Response(
                            {
                                "data":chit_serializer.errors,
                                "message":res_msg.not_create("Estimation"),
                                "status":status.HTTP_400_BAD_REQUEST
                            },status=status.HTTP_200_OK
                        )
                        
                estimation_item_details = request.data.get('particular_details', [])
                if len(estimation_item_details) != 0:
                    for item in estimation_item_details:
                        try:
                            tag_number=item.get('tag_number')

                            tag_queryset=TaggedItems.objects.get(tag_number=tag_number)
                            estimation_tag_data = {
                                'estimation_details': estimation_details['id'],
                                'estimation_tag_item': tag_queryset.pk,
                                'tag_number': item.get('tag_number'),
                                'item_details': item.get('item_details'),
                                'sub_item_details': item.get('sub_item_details'),
                                'metal': item.get('metal'),
                                'net_weight': item.get('net_weight'),
                                'gross_weight' : item.get('gross_weight'),
                                'pieces' : item.get('pieces'),
                                'rate' : item.get('metal_rate'),
                                'stone_rate' : item.get('stone_rate'),
                                'diamond_rate' : item.get('diamond_rate'),
                                'stock_type' : item.get('stock_type'),
                                'calculation_type' : item.get('calculation_type'),
                                'gst_percent' : item.get('gst_percent'),
                                'per_gram_weight_type' : item.get('per_gram_weight_type',None),
                                'wastage_percentage' : item.get('wastage_percent', None),
                                'flat_wastage' : item.get('flat_wastage', None),
                                'making_charge' : item.get('making_charge', None),
                                'flat_making_charge' : item.get('flat_making_charge', None),
                                'wastage_calculation_type': item.get('wastage_calculation_type', None),
                                'making_charge_calculation_type': item.get('making_charge_calculation_type', None),
                                'gst' : item.get('gst'),
                                'total_amount' : item.get('rate'),
                                'with_gst_total_rate':item.get('with_gst_rate'),
                                'huid_rate':item.get('item_huid_rate'),
                                'employee_id':item.get('employee_id')
                            }
                            
                            estimation_taggeditem_serializer = EstimationTagItemsSerializer(data=estimation_tag_data)
                            if estimation_taggeditem_serializer.is_valid():
                                estimation_taggeditem_serializer.save()

                                stone_details=item.get('stone_details') if item.get('stone_details') else []

                                for stone in stone_details:
                                    stone['estimation_details'] = estimation_details['id']
                                    stone['estimation_item_details'] = estimation_taggeditem_serializer.data['id']
                                    stone['stone_name']=float(stone['stone_name'])
                                    stone['stone_pieces']=float(stone['stone_pieces'])
                                    stone['stone_weight']=float(stone['stone_weight'])
                                    stone['stone_weight_type']=int(stone['stone_weight_type'])
                                    stone['stone_rate']=float(stone['stone_rate'])
                                    stone['stone_rate_type']=int(stone['stone_rate_type'])
                                    stone['include_stone_weight']=stone['include_stone_weight']

                                    if int(stone['stone_weight_type']) == int(settings.CARAT):
                                        stone['stone_weight']=(float(stone['stone_weight'])/5)

                                    if int(stone['stone_rate_type']) == int(settings.PERGRAM):
                                        total_stone_value=float(stone['stone_rate']*stone['stone_weight'])
                                        stone['total_stone_value']=total_stone_value
                                    
                                    if int(stone['stone_rate_type']) == int(settings.PERCARAT):
                                        stone_rate = float(stone['stone_rate'])*5
                                        stone['stone_rate'] = stone_rate
                                        total_stone_value=float(stone['stone_rate']*stone['stone_weight'])
                                        stone['total_stone_value']=total_stone_value

                                    if int(stone['stone_rate_type']) == int(settings.PERPIECE):
                                        total_stone_value=float(stone['stone_rate']*stone['stone_pieces'])
                                        stone['total_stone_value']=total_stone_value

                                    estimation_stone_serializer=EstimationStoneDetailsSerializer(data=stone)
                                    if estimation_stone_serializer.is_valid():
                                        estimation_stone_serializer.save()
                                    else:
                                        raise Exception (estimation_stone_serializer.errors)

                                diamond_details=item.get('diamond_details') if item.get('diamond_details') else []

                                for diamond in diamond_details :

                                    diamond['estimation_details'] = estimation_details['id']
                                    diamond['estimation_item_details'] = estimation_taggeditem_serializer.data['id']
                                    diamond['diamond_name'] = float(diamond['diamond_name'])
                                    diamond['diamond_pieces'] = float(diamond['diamond_pieces'])
                                    diamond['diamond_weight'] = float(diamond['diamond_weight'])
                                    diamond['diamond_weight_type'] = int(diamond['diamond_weight_type'])
                                    diamond['diamond_rate'] = float(diamond['diamond_rate'])
                                    diamond['diamond_rate_type'] = int(diamond['diamond_rate_type'])
                                    diamond['include_diamond_weight'] = diamond['include_diamond_weight']

                                    if int(diamond['diamond_weight_type']) == settings.CARAT :
                                        diamond_weight=float(diamond['diamond_weight'])/5
                                        diamond['diamond_weight']=diamond_weight

                                    if int(diamond['diamond_rate_type']) ==settings.PERGRAM:
                                        total_diamond_value=float(diamond['diamond_rate']*diamond['diamond_weight'])
                                        diamond['total_diamond_value'] = total_diamond_value

                                    if int(diamond['diamond_rate_type']) == settings.PERCARAT:
                                        diamond_rate=float(diamond['diamond_rate'])*5
                                        diamond['diamond_rate']=diamond_rate
                                        total_diamond_value=float(diamond['diamond_rate']*diamond['diamond_weight'])
                                        diamond['total_diamond_value'] = total_diamond_value

                                    if int(diamond['diamond_rate_type']) ==settings.PERPIECE:
                                        total_diamond_value=float(diamond['diamond_rate']*diamond['diamond_pieces'])
                                        diamond['total_diamond_value'] = total_diamond_value

                                    estimation_diamond_serializer=EstimationDiamondDetailsSerializer(data=diamond)
                                    if estimation_diamond_serializer.is_valid():
                                        estimation_diamond_serializer.save()
                                    else:
                                        raise Exception(estimation_diamond_serializer.errors)

                            else:
                                raise Exception(estimation_taggeditem_serializer.errors)
                        except Exception as err:
                            raise Exception(err)
                        
                estimation_return_details=request.data.get('estimation_return_details', [])
                
                if len(estimation_return_details) != 0:
                    if request.data.get('sale_return_type') == settings.AUTOMATIC:
                        for return_items in estimation_return_details:
                            try:
                                bill_item_queryset = BillingParticularDetails.objects.get(id=return_items)
                                
                                subitem_queryset = SubItem.objects.get(id=bill_item_queryset.tag_details.sub_item_details.pk)

                                tag_queryset = TaggedItems.objects.get(id=bill_item_queryset.tag_details.pk)
                              
                                estimation_return_data={
                                    'estimation_details': estimation_details['id'],
                                    'bill_details' : bill_item_queryset.billing_details.pk,
                                    'return_items' : bill_item_queryset.pk,
                                    'tag_number' : tag_queryset.tag_number,
                                    'item_details': tag_queryset.item_details.item_details.pk,
                                    'sub_item_details': tag_queryset.sub_item_details.pk,
                                    'metal': tag_queryset.sub_item_details.metal.pk,
                                    'net_weight':bill_item_queryset.net_weight,
                                    'gross_weight':bill_item_queryset.gross_weight,
                                    'tag_weight':tag_queryset.tag_weight,
                                    'cover_weight':tag_queryset.cover_weight,
                                    'loop_weight':tag_queryset.loop_weight,
                                    'other_weight':tag_queryset.other_weight,
                                    'pieces':bill_item_queryset.pieces,
                                    'rate' : bill_item_queryset.rate,
                                    'stone_rate' : bill_item_queryset.stone_amount,
                                    'diamond_rate' : bill_item_queryset.diamond_amount,
                                    'stock_type' : tag_queryset.sub_item_details.stock_type.pk,
                                    'calculation_type' : tag_queryset.calculation_type.pk,
                                    'tax_percent' : bill_item_queryset.gst_percent,
                                    # 'additional_charges' : bill_item_queryset.additional_charges,
                                    # 'total_stone_weight' : bill_item_queryset.total_stone_weight,
                                    # 'total_diamond_weight' : bill_item_queryset.total_diamond_weight,
                                    # 'per_gram_weight_type' : bill_item_queryset.per_gram_weight_type.pk,
                                    'wastage_percentage' : bill_item_queryset.wastage_percent,
                                    'flat_wastage' : bill_item_queryset.flat_wastage,
                                    'making_charge' : bill_item_queryset.making_charge_per_gram,
                                    'flat_making_charge' : bill_item_queryset.flat_making_charge,
                                    # 'wastage_calculation_type': bill_item_queryset.wastage_calculation_type.pk,
                                    # 'making_charge_calculation_type': bill_item_queryset.making_charge_calculation_type.pk,
                                    'gst' : bill_item_queryset.gst_amount,
                                    'total_rate' : bill_item_queryset.total_amount,
                                    # 'without_gst_rate' : bill_item_queryset.without_gst_rate,
                                    'huid_rate':bill_item_queryset.huid_amount,
                                }   
                                
                                if str(tag_queryset.calculation_type.pk) == settings.WEIGHTCALCULATION:
                                    subitem_weight_queryset=SubItemWeightCalculation.objects.get(sub_item_details=subitem_queryset.pk)

                                    estimation_return_data['wastage_calculation_type'] = subitem_weight_queryset.wastage_calculation.pk
                                    estimation_return_data['making_charge_calculation_type'] = subitem_weight_queryset.making_charge_calculation.pk
                                    
                                elif str(tag_queryset.calculation_type.pk) == settings.PERGRAMRATE:
                                    estimation_return_data['per_gram_weight_type'] = tag_queryset.per_gram_weight_type.pk

                                else:
                                    estimation_return_data['wastage_calculation_type'] = None
                                    estimation_return_data['making_charge_calculation_type'] = None
                                    estimation_return_data['per_gram_weight_type'] = None

                                return_serializer=EstimationSaleReturnItemsSerializer(data=estimation_return_data)
                                if return_serializer.is_valid():
                                    return_serializer.save()
                                    try:
                                        return_stone_queryset = BillingParticularStoneDetails.objects.filter(billing_particular_details=bill_item_queryset.pk)

                                        for return_stone in return_stone_queryset:
                                            stone_dict={}
                                            stone_dict['estimation_details'] = estimation_details['id']
                                            stone_dict['estimation_return_item'] = return_serializer.data['id']
                                            stone_dict['stone_name']=return_stone.stone_name.pk
                                            stone_dict['stone_pieces']=return_stone.stone_pieces
                                            stone_dict['stone_weight']=return_stone.stone_weight
                                            stone_dict['stone_weight_type']=return_stone.stone_weight_type.pk
                                            stone_dict['stone_rate']=return_stone.stone_amount
                                            stone_dict['stone_rate_type']=return_stone.stone_rate_type.pk
                                            stone_dict['include_stone_weight']=return_stone.include_stone_weight

                                            estimation_return_stone_serializer=EstimationReturnStoneDetailsSerializer(data=stone_dict)
                                            if estimation_return_stone_serializer.is_valid():
                                                estimation_return_stone_serializer.save()
                                            else:
                                                raise Exception (estimation_return_stone_serializer.errors)
                                            
                                    except Exception as err: 
                                        raise Exception(err)

                                    try:
                                        return_diamond_queryset = BillingParticularsDiamondDetails.objects.filter(billing_particular_details=bill_item_queryset.pk)

                                        for return_diamond in return_diamond_queryset:
                                            diamond_dict={}
                                            diamond_dict['estimation_details'] = estimation_details['id']
                                            diamond_dict['estimation_return_item'] = return_serializer.data['id']
                                            diamond_dict['diamond_name'] = return_diamond.diamond_name.pk
                                            diamond_dict['diamond_pieces'] = return_diamond.diamond_pieces
                                            diamond_dict['diamond_weight'] = return_diamond.diamond_weight
                                            diamond_dict['diamond_weight_type'] = return_diamond.diamond_weight_type.pk
                                            diamond_dict['diamond_rate'] = return_diamond.diamond_amount
                                            diamond_dict['diamond_rate_type'] = return_diamond.diamond_rate_type.pk
                                            diamond_dict['include_diamond_weight'] = return_diamond.include_diamond_weight

                                            estimation_return_diamond_serializer=EstimationReturnDiamondDetailsSerializer(data=diamond_dict)
                                            if estimation_return_diamond_serializer.is_valid():
                                                estimation_return_diamond_serializer.save()
                                            else:
                                                raise Exception (estimation_return_diamond_serializer.errors)
                                            
                                    except Exception as err:
                                        raise Exception(err)
                                    
                                else:
                                    raise Exception (return_serializer.errors)

                            except Exception as err:
                                raise Exception (err)
                    
                    elif request.data.get('sale_return_type') == settings.MANUAL:
                        for return_items in estimation_return_details:
                            try:
                                subitem_queryset = SubItem.objects.get(id=return_items.get('sub_item_details'))
                                
                                estimation_return_data={
                                    'estimation_details': estimation_details['id'],
                                    'bill_details' : return_items.get('bill_details') if return_items.get('bill_details') != '' else None,
                                    'return_items' : return_items.get('return_items') if return_items.get('return_items') != '' else None,
                                    'tag_number' : return_items.get('tag_number') if return_items.get('tag_number') != '' else None,
                                    'item_details': return_items.get('item_details'),
                                    'sub_item_details': return_items.get('sub_item_details'),
                                    'metal': subitem_queryset.metal.pk,
                                    'net_weight':return_items.get('net_weight'),
                                    'gross_weight':return_items.get('gross_weight'),
                                    'tag_weight':return_items.get('tag_weight'),
                                    'cover_weight':return_items.get('cover_weight'),
                                    'loop_weight':return_items.get('loop_weight'),
                                    'other_weight': return_items.get('other_weight'),
                                    'pieces': return_items.get('pieces'),
                                    'total_pieces': return_items.get('total_pieces'),
                                    'rate' : return_items.get('rate'),
                                    'stone_rate' : return_items.get('stone_rate'),
                                    'diamond_rate' : return_items.get('diamond_rate'),
                                    'stock_type' : subitem_queryset.stock_type.pk,
                                    'calculation_type' : subitem_queryset.calculation_type.pk,
                                    # 'tax_percent' : return_items.get('tax_percent'),
                                    'additional_charges' : return_items.get('additional_charges'),
                                    'total_stone_weight' : return_items.get('total_stone_weight'),
                                    'total_diamond_weight' : return_items.get('total_diamond_weight'),
                                    # 'per_gram_weight_type' : return_items.get('per_gram_weight_type',None),
                                    'wastage_percentage' : return_items.get('wastage_percent',None),
                                    'flat_wastage' : return_items.get('flat_wastage',None),
                                    'making_charge' : return_items.get('making_charge',None),
                                    'flat_making_charge' : return_items.get('flat_making_charge',None),
                                    # 'wastage_calculation_type': return_items.get('wastage_calculation_type',None),
                                    # 'making_charge_calculation_type': return_items.get('making_charge_calculation_type',None),
                                    'gst' : return_items.get('gst'),
                                    'total_rate' : return_items.get('total_rate'),
                                    'without_gst_rate' : return_items.get('without_gst_rate'),
                                    'huid_rate': return_items.get('huid_rate'),
                                }   

                                if str(subitem_queryset.calculation_type.pk) == settings.WEIGHTCALCULATION:
                                    subitem_weight_queryset=SubItemWeightCalculation.objects.get(sub_item_details=subitem_queryset.pk)

                                    estimation_return_data['wastage_calculation_type'] = subitem_weight_queryset.wastage_calculation.pk
                                    estimation_return_data['making_charge_calculation_type'] = subitem_weight_queryset.making_charge_calculation.pk
                                   
                                elif str(subitem_queryset.calculation_type.pk) == settings.PERGRAMRATE:
                                    subitem_weight_queryset=SubItemPerGramRate.objects.get(sub_item_details=subitem_queryset.pk)

                                    estimation_return_data['per_gram_weight_type'] = subitem_weight_queryset.per_gram_weight_type.pk

                                try:
                                    tax_queryset = TaxDetailsAudit.objects.filter(metal=subitem_queryset.metal.pk).order_by('-id').first()
                                    if tax_queryset:
                                        tax_percent_queryset = SalesTaxDetails.objects.get(tax_details=tax_queryset.tax_details)
                                        if return_items.get('gst_type') == settings.INTRA_STATE_GST:
                                            estimation_return_data['tax_percent'] = tax_percent_queryset.sales_tax_cgst + tax_percent_queryset.sales_tax_sgst
                                        elif return_items.get('gst_type') == settings.INTER_STATE_GST:
                                            estimation_return_data['tax_percent'] = tax_percent_queryset.sales_tax_igst
                                except Exception as err:
                                    estimation_return_data['tax_percent'] = 0

                                return_serializer=EstimationSaleReturnItemsSerializer(data=estimation_return_data)
                                if return_serializer.is_valid():
                                    return_serializer.save()
                                else:
                                    raise Exception(return_serializer.errors)

                            except Exception as err:
                                raise Exception (err)
                return Response(
                    {
                        "data":serializer.data,
                        "message":res_msg.create("Estimation Biling"),
                        "status":status.HTTP_201_CREATED
                    },status=status.HTTP_200_OK)
            
            else:
                raise Exception(serializer.errors)
        
        except Exception as err:
            # try:
            #     DeleteEstimation(serializer.data['id'])
            # except:
            #     pass
            transaction.set_rollback(True)
            return Response(
                {
                    "data":str(err),
                    "message":res_msg.something_else(),
                    "status":status.HTTP_204_NO_CONTENT
                },status=status.HTTP_200_OK
            )
        
    def delete(self,request,pk):
        DeleteEstimation(pk)
        return Response(
            {
                "message":res_msg.delete("Estimation Details"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class EstimationListView(APIView):
    def get(self,request,branch=None):
        
        try:
            # if request.user.role.is_admin == True:
            #     if branch != None:            
            #         branch = branch
            #     else:
            #         request.user.branch.pk
            # else:
            #     branch = request.user.branch.pk
                
            filter_dict={}

            if branch != None:
                filter_dict['branch'] = int(branch)    
                
            queryset = list(EstimateDetails.objects.filter(**filter_dict).values('id','estimate_no','customer_details__phone','customer_details__id','customer_details__customer_name').order_by('-id'))

            return Response(
                {
                    "data":{
                        'list':queryset
                    },
                    "message":res_msg.retrieve("Estimation Details"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        except EstimateDetails.DoesNotExist:

            return Response(
                {
                    "message":res_msg.not_exists("Estimation Details"),
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
        
    def post(self,request):

        try:

            request_data=request.data
            search=request_data.get('search') if request_data.get('search') else ""
            branch = request_data.get('branch') if request_data.get('branch') else None

            filter_condition={}

            if request.user.role.is_admin == True:
                if branch != None:
                    filter_condition['branch'] = branch
            else:
                filter_condition['branch'] = request.user.branch.pk

            if len(filter_condition) != 0:
                queryset=EstimateDetails.objects.filter(Q(estimate_no__icontains=search) | Q(customer_details__customer_name__icontains=search) | Q(customer_details__phone__icontains=search),**filter_condition)
            else:
                queryset=EstimateDetails.objects.filter(Q(estimate_no__icontains=search) | Q(customer_details__customer_name__icontains=search) | Q(customer_details__phone__icontains=search))

            response_data=[]
            for data in queryset:
                serializer=EstimateDetailsSerializer(data)
                res_data=serializer.data
                res_data['customer_name']=data.customer_details.customer_name
                res_data['customer_mobile']=data.customer_details.phone
                response_data.append(res_data)

            return Response(
                {
                    "data":{
                        "list":response_data
                    },
                    "message":res_msg.retrieve("Estimation List"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        
        except Exception as err:
            pass

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class EstimateNumberSearch(APIView):
    def get(self,request):
       
        metal_type = request.GET.get('metal_type',None)
        customer = request.GET.get('customer',None)
        branch = request.GET.get('branch',None)
       
        filter_condition = {}
       
        if metal_type != None:
           
            filter_condition['bill_type'] = metal_type
       
        if customer != None:
           
            filter_condition['customer_details'] = customer
           
        if request.user.role.is_admin == True:
           
            if branch != None:
               
                filter_condition['branch'] = branch
               
        else:
           
            filter_condition['branch'] = request.user.branch.pk
           
           
        filter_condition['is_billed'] = False
   
        queryset = list(EstimateDetails.objects.filter(**filter_condition).order_by('-id'))
        serializer = EstimateDetailsSerializer(queryset,many=True)
        res_data = []
       
        for item in serializer.data:
           
            estimate_data = {}
            estimate_data['id'] = item['id']
            estimate_data['estimate_number'] = item['estimate_no']
 
            res_data.append(estimate_data)
        return Response(
            {
                "data": {
                    "list" : res_data
                },
                "message" : res_msg.retrieve("Estimate details"),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK
        )

def DeleteBill(pk):

    try:
        queryset=BillingDetails.objects.get(id=pk)
        queryset.delete() 
    except:
        pass
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class BillingWithOutStockReduceView(APIView):
    @transaction.atomic
    def post(self,request):

        try:

            data = request.data
            res_data={
                'estimation_details':data.get('estimation_details') if data.get('estimation_details') else None ,
                'bill_no':data.get('bill_no'),
                'bill_type':data.get('bill_type'),
                'bill_date':data.get('bill_date'),
                'customer_details':data.get('customer_details'),
                'customer_mobile':data.get('customer_no'),
                'total_amount':data.get('total_amount'),
                'gst_amount':data.get('gst_amount'),
                'advance_amount':data.get('advance_amount') ,
                'discount_amount':data.get('discount_amount'),
                'exchange_amount':data.get('exchange_amount'),
                'payable_amount':data.get('payable_amount'),
                'chit_amount':data.get('chit_amount') if data.get('chit_amount') else 0,
                'cash_amount':data.get('cash_amount') if data.get('cash_amount') else 0,
                'return_amount':data.get('return_amount') if data.get('return_amount') else 0,
                'card_amount':data.get('card_amount') if data.get('card_amount') else 0,
                'account_transfer_amount':data.get('account_transfer_amount') if data.get('account_transfer_amount') else 0,
                'upi_amount':data.get('upi_amount') if data.get('upi_amount') else 0,
                'paid_amount':data.get('paid_amount') if data.get('paid_amount') else 0,  
            }

            if request.user.role.is_admin == True :

                res_data['branch'] = data.get('branch')

            else:
                
                res_data['branch'] = request.user.branch.pk

            
            res_data['created_at'] = timezone.now()
            res_data['created_by'] = request.user.id

            serializer = BillingDetailsSerializer(data=res_data)
            if serializer.is_valid():
                serializer.save()
                billing_details = serializer.data

                if int(res_data['bill_type']) == 1:
                        bill_id_dict={}
                        bill_id_dict['bill_id']=serializer.data['bill_no']
                        bill_number_serializer=BillIDSerializer(data=bill_id_dict)

                        if bill_number_serializer.is_valid():
                            bill_number_serializer.save()
                    
                elif int(res_data['bill_type']) == 2:

                    bill_id_dict={}
                    bill_id_dict['silver_bill_id']=serializer.data['id']
                    bill_number_serializer=SilverBillIDSerializer(data=bill_id_dict)

                    if bill_number_serializer.is_valid():
                        bill_number_serializer.save()
                
                else:
                    pass
                
                new_oldgold_data = {}
                new_oldgold_data['old_gold_no']=request.data.get('old_gold_no')
                oldgold_details = request.data.get('old_gold_particulars', {})
                if len(oldgold_details) != 0:
                    for oldgold in oldgold_details:
                        try:
                            
                            new_oldgold_data['old_metal']=oldgold['metal']
                            new_oldgold_data['item_name']=oldgold['item_name']
                            new_oldgold_data['metal_rate']=0
                            new_oldgold_data['old_gross_weight']=oldgold['gross_weight']
                            new_oldgold_data['old_net_weight']=0
                            new_oldgold_data['dust_weight']=0
                            new_oldgold_data['billing_details']=serializer.data['id']
                            # new_oldgold_data['old_metal_rate']=oldgold['old_rate']
                            # new_oldgold_data['today_metal_rate']=oldgold['today_rate']
                            new_oldgold_data['total_old_gold_value']=oldgold['total']
                            # new_oldgold_data['purity']=oldgold['purity']

                            if len(new_oldgold_data) != 0 :
                                oldgold_serializer = BillingOldGoldSerializer(data=new_oldgold_data)
                                if oldgold_serializer.is_valid():
                                    oldgold_serializer.save()
                                else:
                                    raise Exception(oldgold_serializer.errors)
                            else:
                                pass
                        except Exception as error:
                            raise Exception(error)
                billing_item_details = request.data.get('particulars', [])
                
                if len(billing_item_details) != 0:
                    for item in billing_item_details:
                        try:

                            tag_number=item.get('tag_number')

                            tag_queryset=TaggedItems.objects.get(tag_number=tag_number)
                            billing_tag_data = {
                                'billing_details': billing_details['id'],
                                'billing_tag_item': tag_queryset.pk,
                                'tag_number': item.get('tag_number'),
                                'item_details': item.get('item_details'),
                                'sub_item_details': item.get('sub_item_details'),
                                'metal': item.get('metal'),
                                'net_weight': item.get('net_weight'),
                                'gross_weight' : item.get('gross_weight'),
                                'tag_weight' : item.get('tag_weight'),
                                'cover_weight' : item.get('cover_weight'),
                                'loop_weight' : item.get('loop_weight'),
                                'other_weight' : item.get('other_weight'),
                                'pieces' : item.get('pieces'),
                                'total_pieces' : item.get('total_pieces'),
                                'rate' : item.get('metal_rate'),
                                'stone_rate' : item.get('stone_rate'),
                                'diamond_rate' : item.get('diamond_rate'),
                                'stock_type' : item.get('stock_type'),
                                'calculation_type' : item.get('calculation_type'),
                                'tax_percent' : item.get('tax_percent'),
                                'additional_charges' : item.get('additional_charges'),
                                'total_stone_weight' : item.get('total_stone_weight'),
                                'total_diamond_weight' : item.get('total_diamond_weight'),
                                'per_gram_weight_type' : item.get('per_gram_weight_type',None),
                                'wastage_percentage' : item.get('wastage_percent', None),
                                'flat_wastage' : item.get('flat_wastage', None),
                                'making_charge' : item.get('making_charge', None),
                                'flat_making_charge' : item.get('flat_making_charge', None),
                                'wastage_calculation_type': item.get('wastage_calculation_type', None),
                                'making_charge_calculation_type': item.get('making_charge_calculation_type', None),
                                'gst' : item.get('gst'),
                                'total_rate' : item.get('with_gst_rate'),
                                'without_gst_rate':item.get('rate'),
                                'huid_rate':item.get('item_huid_rate')
                            }
                            
                            billing_taggeditem_serializer = BillingTagItemsSerializer(data=billing_tag_data)
                            if billing_taggeditem_serializer.is_valid():
                                billing_taggeditem_serializer.save()

                                stone_details=item.get('stone_details') if item.get('stone_details') else []

                                for stone in stone_details:
                                    stone['billing_details'] = billing_details['id']
                                    stone['billing_item_details'] = billing_taggeditem_serializer.data['id']
                                    stone['stone_name']=float(stone['stone_name'])
                                    stone['stone_pieces']=float(stone['stone_pieces'])
                                    stone['stone_weight']=float(stone['stone_weight'])
                                    stone['stone_weight_type']=int(stone['stone_weight_type'])
                                    stone['stone_rate']=float(stone['stone_rate'])
                                    stone['stone_rate_type']=int(stone['stone_rate_type'])
                                    stone['include_stone_weight']=stone['include_stone_weight']

                                    if int(stone['stone_weight_type']) == int(settings.CARAT):
                                        stone['stone_weight']=(float(stone['stone_weight'])/5)

                                    if int(stone['stone_rate_type']) == int(settings.PERGRAM):
                                        total_stone_value=float(stone['stone_rate']*stone['stone_weight'])
                                        stone['total_stone_value']=total_stone_value
                                    
                                    if int(stone['stone_rate_type']) == int(settings.PERCARAT):
                                        stone_rate = float(stone['stone_rate'])*5
                                        stone['stone_rate'] = stone_rate
                                        total_stone_value=float(stone['stone_rate']*stone['stone_weight'])
                                        stone['total_stone_value']=total_stone_value

                                    if int(stone['stone_rate_type']) == int(settings.PERPIECE):
                                        total_stone_value=float(stone['stone_rate']*stone['stone_pieces'])
                                        stone['total_stone_value']=total_stone_value

                                    billing_stone_serializer=BillingStoneDetailsSerializer(data=stone)
                                    if billing_stone_serializer.is_valid():
                                        billing_stone_serializer.save()
                                    else:
                                        raise Exception (billing_stone_serializer.errors)

                                diamond_details=item.get('diamond_details') if item.get('diamond_details') else []

                                for diamond in diamond_details :

                                    diamond['billing_details'] = billing_details['id']
                                    diamond['billing_item_details'] = billing_taggeditem_serializer.data['id']
                                    diamond['diamond_name'] = float(diamond['diamond_name'])
                                    diamond['diamond_pieces'] = float(diamond['diamond_pieces'])
                                    diamond['diamond_weight'] = float(diamond['diamond_weight'])
                                    diamond['diamond_weight_type'] = int(diamond['diamond_weight_type'])
                                    diamond['diamond_rate'] = float(diamond['diamond_rate'])
                                    diamond['diamond_rate_type'] = int(diamond['diamond_rate_type'])
                                    diamond['include_diamond_weight'] = diamond['include_diamond_weight']

                                    if int(diamond['diamond_weight_type']) == settings.CARAT :
                                        diamond_weight=float(diamond['diamond_weight'])/5
                                        diamond['diamond_weight']=diamond_weight

                                    if int(diamond['diamond_rate_type']) ==settings.PERGRAM:
                                        total_diamond_value=float(diamond['diamond_rate']*diamond['diamond_weight'])
                                        diamond['total_diamond_value'] = total_diamond_value

                                    if int(diamond['diamond_rate_type']) == settings.PERCARAT:
                                        diamond_rate=float(diamond['diamond_rate'])*5
                                        diamond['diamond_rate']=diamond_rate
                                        total_diamond_value=float(diamond['diamond_rate']*diamond['diamond_weight'])
                                        diamond['total_diamond_value'] = total_diamond_value

                                    if int(diamond['diamond_rate_type']) ==settings.PERPIECE:
                                        total_diamond_value=float(diamond['diamond_rate']*diamond['diamond_pieces'])
                                        diamond['total_diamond_value'] = total_diamond_value

                                    billing_diamond_serializer=BillingDiamondDetailsSerializer(data=diamond)
                                    if billing_diamond_serializer.is_valid():
                                        billing_diamond_serializer.save()
                                    else:
                                        raise Exception(billing_diamond_serializer.errors)
                            else:
                                raise Exception(billing_taggeditem_serializer.errors)
                        except Exception as err:
                            raise Exception(err)
                        
                billing_return_details = request.data.get('billing_return_details')

                if len(billing_return_details) != 0:

                    for return_items in billing_return_details:
                        try:
                            bill_item_queryset = BillingTagItems.objects.get(id=return_items)
                            estimation_return_data={
                                'billing_details': serializer.data['id'],
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
                                'per_gram_weight_type' : bill_item_queryset.per_gram_weight_type,
                                'wastage_percentage' : bill_item_queryset.wastage_percentage,
                                'flat_wastage' : bill_item_queryset.flat_wastage,
                                'making_charge' : bill_item_queryset.making_charge,
                                'flat_making_charge' : bill_item_queryset.flat_making_charge,
                                'wastage_calculation_type': bill_item_queryset.wastage_calculation_type.pk,
                                'making_charge_calculation_type': bill_item_queryset.making_charge_calculation_type.pk,
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

                                    for return_stone in return_stone_queryset:

                                        stone_dict={}

                                        stone_dict['billing_details'] = serializer.data['id']
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

                                    for return_diamond in return_diamond_queryset:

                                        diamond_dict={}

                                        diamond_dict['billing_details'] = serializer.data['id']
                                        diamond_dict['estimation_return_item'] = return_serializer.data['id']
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
                
                return Response(
                    {
                        "data":serializer.data,
                        "message":res_msg.create("Biling"),
                        "status":status.HTTP_201_CREATED
                    },status=status.HTTP_200_OK)
            
            else:
                raise Exception(serializer.errors)
            
        
        except Exception as err:

            # try:
            #     DeleteBill(serializer.data['id'])
            # except:
            #     pass

            transaction.set_rollback(True)
            return Response(
                {
                    "data":str(err),
                    "message":res_msg.something_else(),
                    "status":status.HTTP_204_NO_CONTENT
                },status=status.HTTP_200_OK
            )
        

# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# class BillingView(APIView):

#     def get(self,reqeust,pk):

#         try:

#             queryset = BillingDetails.objects.get(id=pk)
            
#             res_data={}

#             customer_details = []
#             try:
#                 customer_queryset = Customer.objects.get(id=queryset.customer_details.pk,is_active=True)
#                 customer_serializer = CustomerSerializer(customer_queryset)
#                 customer_details = customer_serializer.data
                
#             except Exception as err:
#                 return Response(
#                     {
#                         "message" : res_msg.not_exists('Customer'),
#                         "status": status.HTTP_204_NO_CONTENT
#                     }, status=status.HTTP_200_OK
#                 )

#             try:
#                 res_data['estimation_details']=queryset.estimation_details.pk
#             except:
#                 res_data['estimation_details']=None

#             res_data['id']=queryset.pk
#             res_data['bill_no']=queryset.bill_no
#             res_data['bill_type']=queryset.bill_type.pk
#             res_data['bill_type_name']=queryset.bill_type.bill_type
#             res_data['bill_date']=queryset.bill_date
#             res_data['bill_no']=queryset.bill_no

#             try:
#                 payment_queryset = CommonPaymentDetails.objects.get(refference_number=queryset.bill_no)
#                 payment_serializer = CommonPaymentSerializer(payment_queryset)
                
#             except Exception as err:
#                 return Response(
#                     {
#                         "message" : res_msg.not_exists('Payment details'),
#                         "status": status.HTTP_204_NO_CONTENT
#                     }, status=status.HTTP_200_OK
#                 )

#             res_data['total_amount']=payment_queryset.total_amount
#             res_data['gst_type']=payment_queryset.gst_type.pk
#             res_data['igst_amount']=payment_queryset.igst_amount
#             res_data['igst_percentage']=payment_queryset.igst_percentage
#             res_data['sgst_amount']=payment_queryset.sgst_amount
#             res_data['sgst_percentage']=payment_queryset.sgst_percentage
#             res_data['cgst_amount']=payment_queryset.cgst_amount
#             res_data['cgst_percentage']=payment_queryset.cgst_percentage
#             res_data['discount_percentage']=payment_queryset.discount_percentage
#             res_data['discount_amount']=payment_queryset.discount_amount
#             res_data['advance_amount']=payment_queryset.advance_amount
#             res_data['exchange_amount']=payment_queryset.exchange_amount
#             res_data['payable_amount']=payment_queryset.payable_amount
#             res_data['balance_amount']=payment_queryset.balance_amount
#             res_data['salereturn_amount']=payment_queryset.salereturn_amount
#             res_data['diamond_amount']=payment_queryset.diamond_amount
#             res_data['stone_amount']=payment_queryset.stone_amount
#             res_data['billed_date']=payment_queryset.created_at
#             res_data['created_by']=queryset.created_by.get_username()
                
#             try:

#                 bill_items = BillingTagItems.objects.filter(billing_details=queryset.pk)

#                 billing_item_details=[]

#                 for items in bill_items:

#                     item_dict={}

#                     item_dict['id']=items.pk
#                     item_dict['diamond_rate']=items.diamond_rate
#                     item_dict['flat_making_charge']=items.flat_making_charge
#                     item_dict['gross_weight']=items.gross_weight
#                     item_dict['item_details']=items.item_details.pk
#                     item_dict['item']=items.item_details.item_name
#                     item_dict['jewel_type']=items.metal.metal_name
#                     item_dict['loop_weight']=items.loop_weight
#                     item_dict['cover_weight']=items.cover_weight
#                     item_dict['cover_weight']=items.cover_weight
#                     item_dict['making_charge']=items.making_charge
#                     item_dict['metal']=items.metal.pk
#                     item_dict['metal_rate']=items.rate
#                     item_dict['net_weight']=items.net_weight
#                     item_dict['other_weight']=items.other_weight
#                     item_dict['pieces']=items.pieces
#                     item_dict['rate']=items.without_gst_rate
#                     item_dict['stock_type']=items.stock_type.pk
#                     item_dict['stock_type_name']=items.stock_type.stock_type_name
#                     item_dict['calculation_type']=items.calculation_type.pk
#                     item_dict['calculation_type_name']=items.calculation_type.calculation_name
#                     item_dict['stone_rate']=items.stone_rate
#                     item_dict['sub_item_details']=items.sub_item_details.pk
#                     item_dict['sub_item_name']=items.sub_item_details.sub_item_name
#                     item_dict['tag_item_id']=items.billing_tag_item.pk
#                     item_dict['tag_number']=items.billing_tag_item.tag_number
#                     item_dict['tag_weight']=items.tag_weight
#                     item_dict['tax_percent']=items.tax_percent
#                     item_dict['total_diamond_weight']=items.total_diamond_weight
#                     item_dict['total_pieces']=items.total_pieces
#                     item_dict['total_stone_weight']=items.total_stone_weight
#                     item_dict['wastage_percent']=items.wastage_percentage
#                     item_dict['flat_wastage']=items.flat_wastage
#                     item_dict['item_huid_rate']=items.huid_rate
#                     item_dict['gst']=items.gst
#                     item_dict['with_gst_rate']=items.total_rate
#                     item_dict['is_returned']=items.is_returned
#                     item_dict['employee_id']=items.employee_id.pk
#                     item_dict['employee_name']=items.employee_id.staff_id

#                     if str(items.calculation_type.pk) == settings.FIXEDRATE:
#                         item_dict['min_metal_rate'] = items.billing_tag_item.min_fixed_rate
#                         item_dict['max_metal_rate'] = items.billing_tag_item.max_fixed_rate

#                     elif str(items.calculation_type.pk) == settings.WEIGHTCALCULATION:

#                         subitem_weight_queryset=SubItemWeightCalculation.objects.get(sub_item_details=items.billing_tag_item.sub_item_details.pk)
                        
#                         item_dict['wastage_calculation_type'] = subitem_weight_queryset.wastage_calculation.pk
#                         item_dict['wastage_calculation_name'] = subitem_weight_queryset.wastage_calculation.weight_name
                        
#                         item_dict['making_charge_calculation_type'] = subitem_weight_queryset.making_charge_calculation.pk
#                         item_dict['making_charge_calculation_name'] = subitem_weight_queryset.making_charge_calculation.weight_name

#                         item_dict['min_wastage_percent'] = items.billing_tag_item.min_wastage_percent
#                         item_dict['min_wastage_percent'] = items.billing_tag_item.min_wastage_percent
#                         item_dict['min_flat_wastage'] = items.billing_tag_item.min_flat_wastage
#                         item_dict['max_wastage_percent'] = items.billing_tag_item.max_wastage_percent
#                         item_dict['max_flat_wastage'] = items.billing_tag_item.max_flat_wastage
#                         item_dict['min_making_charge'] = items.billing_tag_item.min_making_charge_gram
#                         item_dict['min_flat_making_charge'] = items.billing_tag_item.min_flat_making_charge
#                         item_dict['max_making_charge'] = items.billing_tag_item.max_making_charge_gram
#                         item_dict['max_flat_making_charge'] = items.billing_tag_item.max_flat_making_charge
                    
#                     elif str(items.calculation_type.pk) == settings.PERGRAMRATE:

#                         item_dict['min_metal_rate'] = items.billing_tag_item.min_pergram_rate
#                         item_dict['max_metal_rate'] = items.billing_tag_item.max_pergram_rate
#                         item_dict['per_gram_weight_type'] = items.billing_tag_item.per_gram_weight_type.pk
#                         item_dict['per_gram_weight_type_name'] = items.billing_tag_item.per_gram_weight_type.weight_name

#                     elif str(items.calculation_type.pk) == settings.PERPIECERATE:
#                         # subitem_piece_queryset=SubItemPerPiece.objects.get(sub_item_details=items.billing_tag_item.sub_item_details.pk)                        
#                         item_dict['min_per_piece_rate'] = items.billing_tag_item.min_per_piece_rate
#                         item_dict['per_piece_rate'] = items.billing_tag_item.per_piece_rate

#                     if items.per_gram_weight_type != None:
#                         item_dict['per_gram_weight_type']=items.per_gram_weight_type.pk if items.per_gram_weight_type.pk != None else None
#                         item_dict['per_gram_weight_type_name']=items.per_gram_weight_type.weight_name if items.per_gram_weight_type.weight_name != None else None


#                     try:

#                         stone_queryset = BillingStoneDetails.objects.filter(billing_details=queryset.pk,billing_item_details=items.pk)

#                         stone_details=[]

#                         for stone in stone_queryset:

#                             stone_data={
#                                     'id':stone.pk,
#                                     'stone_name':stone.stone_name.pk,
#                                     'stone_pieces':stone.stone_pieces,
#                                     'stone_weight_type':stone.stone_weight_type.pk,
#                                     'stone_weight_type_name':stone.stone_weight_type.weight_name,
#                                     'stone_rate_type':stone.stone_rate_type.pk,
#                                     'stone_rate_type_name':stone.stone_rate_type.type_name,
#                                     'include_stone_weight':stone.include_stone_weight
#                             }

#                             if str(stone.stone_weight_type.pk) == settings.CARAT:
#                                     stone_data['stone_weight'] = float(stone.stone_weight)*5

#                             else:
#                                 stone_data['stone_weight'] = float(stone.stone_weight)

#                             if str(stone.stone_rate_type.pk) == settings.PERCARAT:
#                                 stone_data['stone_rate'] = float(stone.stone_rate)/5

#                             elif str(stone.stone_rate_type.pk) == settings.PERPIECE:
#                                 stone_data['stone_rate'] = float(stone.stone_rate)
#                             else:
#                                 stone_data['stone_rate'] = float(stone.stone_rate)
                                

#                             stone_details.append(stone_data)

#                         item_dict['stone_details']=stone_details


#                     except BillingStoneDetails.DoesNotExist:
#                         stone_details=[]
#                         item_dict['stone_details']=stone_details

#                     except Exception  as err:

#                         raise Exception(err)
                    

#                     try:


#                         diamond_queryset = BillingDiamondDetails.objects.filter(billing_details=queryset.pk,billing_item_details=items.pk)
#                         diamond_details=[]

#                         for diamond in diamond_queryset:

#                             diamond_data={
#                                 'id':diamond.pk,
#                                 'diamond_name':diamond.diamond_name.pk,
#                                 'diamond_pieces':diamond.diamond_pieces,
#                                 'diamond_weight_type':diamond.diamond_weight_type.pk,
#                                 'diamond_weight_type_name':diamond.diamond_weight_type.weight_name,
#                                 'diamond_rate_type':diamond.diamond_rate_type.pk,
#                                 'diamond_rate_type_name':diamond.diamond_rate_type.type_name,
#                                 'include_diamond_weight':diamond.include_diamond_weight
#                             }

#                             if str(diamond.diamond_weight_type.pk) == settings.CARAT:
#                                     diamond_data['diamond_weight'] = float(diamond.diamond_weight)*5

#                             else:
#                                 diamond_data['diamond_weight'] = float(diamond.diamond_weight)

#                             if str(diamond.diamond_rate_type.pk) == settings.PERCARAT:
#                                 diamond_data['diamond_rate'] = float(diamond.diamond_rate)/5

#                             else:
#                                 diamond_data['diamond_rate'] = float(diamond.diamond_rate)

#                             diamond_details.append(diamond_data)

#                         item_dict['diamond_details']=diamond_details


#                     except BillingDiamondDetails.DoesNotExist:
#                         diamond_details=[]
#                         item_dict['diamond_details']=diamond_details

#                     except Exception as err:

#                         raise Exception(err)

#                     billing_item_details.append(item_dict)

#                 res_data['billing_item_details']=billing_item_details

#             except BillingTagItems.DoesNotExist:
#                 billing_item_details=[]
#                 res_data['billing_item_details']=billing_item_details

#             try:

#                 billing_return_details = []

#                 billing_return_queryset = BillingSaleReturnItems.objects.filter(billing_details=pk)

#                 for return_item in billing_return_queryset:

#                     return_details={
#                         'id':return_item.pk,
#                         'billing_details': return_item.billing_details.pk,
#                         'return_bill_details' : return_item.return_bill_details.pk,
#                         'return_items' : return_item.return_items.pk,
#                         'tag_number' : return_item.tag_number,
#                         'item_details': return_item.item_details.pk,
#                         'item_details_name': return_item.item_details.item_name,
#                         'sub_item_details': return_item.sub_item_details.pk,
#                         'sub_item_details_name': return_item.sub_item_details.sub_item_name,
#                         'metal': return_item.metal.pk,
#                         'metal': return_item.metal.pk,
#                         'net_weight':return_item.net_weight,
#                         'gross_weight':return_item.gross_weight,
#                         'tag_weight':return_item.tag_weight,
#                         'cover_weight':return_item.cover_weight,
#                         'loop_weight':return_item.loop_weight,
#                         'other_weight':return_item.other_weight,
#                         'pieces':return_item.pieces,
#                         'total_pieces':return_item.total_pieces,
#                         'metal_rate' : return_item.rate,
#                         'rate':return_item.without_gst_rate,
#                         'stone_rate' : return_item.stone_rate,
#                         'diamond_rate' : return_item.diamond_rate,
#                         'stock_type' : return_item.stock_type.pk,
#                         'calculation_type' : return_item.calculation_type.pk,
#                         'tax_percent' : return_item.tax_percent,
#                         'additional_charges' : return_item.additional_charges,
#                         'total_stone_weight' : return_item.total_stone_weight,
#                         'total_diamond_weight' : return_item.total_diamond_weight,
#                         'per_gram_weight_type' : return_item.per_gram_weight_type,
#                         'wastage_percentage' : return_item.wastage_percentage,
#                         'flat_wastage' : return_item.flat_wastage,
#                         'making_charge' : return_item.making_charge,
#                         'flat_making_charge' : return_item.flat_making_charge,
#                         'wastage_calculation_type': return_item.wastage_calculation_type.pk,
#                         'wastage_calculation_type_name': return_item.wastage_calculation_type.weight_name,
#                         'making_charge_calculation_type': return_item.making_charge_calculation_type.pk,
#                         'making_charge_calculation_type_name': return_item.making_charge_calculation_type.weight_name,
#                         'gst' : return_item.gst,
#                         'with_gst_rate' : return_item.total_rate,
#                         'item_huid_rate':return_item.huid_rate
#                     }

#                     stone_return_details=[]

#                     return_stone_queryset = BillingReturnStoneDetails.objects.filter(billing_details=pk,billing_return_item=return_item.pk)

#                     for return_stone in return_stone_queryset:

#                         stone_details_return={
#                             "id":return_stone.pk,
#                             "billing_details":return_stone.billing_details.pk,
#                             "billing_return_item":return_stone.billing_return_item.pk,
#                             "stone":return_stone.stone_name.pk,
#                             "stone_name":return_stone.stone_name.stone_name,
#                             "stone_pieces":return_stone.stone_pieces,
#                             "stone_weight":return_stone.stone_weight,
#                             "stone_weight_type":return_stone.stone_weight_type.pk,
#                             "stone_weight_type_name":return_stone.stone_weight_type.weight_name,
#                             "stone_rate":return_stone.stone_rate,
#                             "stone_rate_type":return_stone.stone_rate_type.pk,
#                             "stone_rate_type_name":return_stone.stone_rate_type.type_name,
#                             "include_stone_weight":return_stone.include_stone_weight,
#                             "total_stone_value":return_stone.total_stone_value
#                         }

#                         stone_return_details.append(stone_details_return)

#                     return_details['stone_details'] = stone_return_details

#                     diamond_return_details=[]

#                     return_diamond_queryset = BillingReturnDiamondDetails.objects.filter(billing_details=pk,billing_return_item=return_item.pk)

#                     for return_diamond in return_diamond_queryset:

#                         diamond_details_return={

#                             "id":return_diamond.pk,
#                             "billing_details":return_diamond.billing_details.pk,
#                             "billing_return_item":return_diamond.billing_return_item.pk,
#                             "diamond":return_diamond.diamond_name.pk,
#                             "diamond_name":return_diamond.diamond_name.stone_name,
#                             "diamond_pieces":return_diamond.diamond_pieces,
#                             "diamond_weight":return_diamond.diamond_weight,
#                             "diamond_weight_type":return_diamond.diamond_weight_type.pk,
#                             "diamond_weight_type_name":return_diamond.diamond_weight_type.weight_name,
#                             "diamond_rate":return_diamond.diamond_rate,
#                             "diamond_rate_type":return_diamond.diamond_rate_type.pk,
#                             "diamond_rate_type_name":return_diamond.diamond_rate_type.type_name,
#                             "include_diamond_weight":return_diamond.include_diamond_weight,
#                             "total_diamond_value":return_diamond.total_diamond_value
#                         }

#                         diamond_return_details.append(diamond_details_return)

#                     return_details['diamond_details'] = diamond_return_details


                    
#                     billing_return_details.append(return_details)

#                 res_data['billing_return_details'] = billing_return_details

#             except Exception as err:

#                 raise Exception(err)

#             try:

#                 old_gold_details=[]

#                 old_gold_queryset = RepairOrderOldGold.objects.filter(refference_number=queryset.bill_no)

#                 for old_gold in old_gold_queryset:
                        
#                     old_details={
#                         'id':old_gold.pk,
#                         'dust_weight':old_gold.dust_weight,
#                         'gross_weight':old_gold.gross_weight,
#                         'metal':old_gold.metal.pk,
#                         'metal_name':old_gold.metal.metal_name,
#                         'metal_rate':old_gold.metal_rate,
#                         'net_weight':old_gold.net_weight,
#                         'old_rate':old_gold.metal_rate,
#                         'today_rate':old_gold.today_metal_rate,
#                         'purity':old_gold.purity,
#                         'total':old_gold.total_amount,
#                         'old_rate':old_gold.old_rate,
#                         'employee_id':old_gold.employee_id.pk,
#                         'employee_name':old_gold.employee_id.staff_id,
#                     }
#                     if old_gold.purity != None:
#                         old_details['purity']= old_gold.purity.pk
#                     else:
#                         old_details['purity']= "-"
#                     old_gold_details.append(old_details)

#                     res_data["old_gold_no"] = old_gold.old_gold_no
                        
#                 res_data["old_item_details"] = old_gold_details

#             except BillingOldGold.DoesNotExist:
#                 old_gold_details=[]
#                 res_data["old_item_details"] = old_gold_details

#             except Exception as err:
#                 raise Exception(err)

#             return Response(
#                 {
#                     "data":{
#                         "customer_details" : customer_details,
#                         "billing_details": res_data
#                     },
#                     "message":res_msg.retrieve("Billing Details"),
#                     "status":status.HTTP_200_OK
#                 },status=status.HTTP_200_OK
#             )

#         except BillingDetails.DoesNotExist :

#             return Response(
#                 {
#                     "message":res_msg.not_exists("Billing Details"),
#                     "status":status.HTTP_404_NOT_FOUND
#                 },status=status.HTTP_200_OK
#             )
        
#         except Exception as err:

#             return Response(
#                 {
#                     "data":str(err),
#                     "message":res_msg.something_else(),
#                     "status":status.HTTP_204_NO_CONTENT
#                 },status=status.HTTP_200_OK
#             )

#     @transaction.atomic
#     def post(self,request):

#         try:
#             data = request.data
            
#             res_data={
#                 'estimation_details':data.get('estimation_details') if data.get('estimation_details') else None ,
#                 'bill_no':data.get('bill_no'),
#                 'bill_type':data.get('bill_type'),
#                 'bill_date':data.get('bill_date'),
#                 'customer_details':data.get('customer_details'),
#                 'customer_mobile':data.get('customer_no'),
#                 'cash_counter':data.get('cash_counter'),
#                 # 'total_amount':data.get('total_amount'),
#                 # 'gst_amount':data.get('gst_amount'),
#                 # 'advance_amount':data.get('advance_amount') ,
#                 # 'discount_amount':data.get('discount_amount'),
#                 # 'exchange_amount':data.get('exchange_amount'),
#                 # 'payable_amount':data.get('payable_amount'),
#                 # 'chit_amount':data.get('chit_amount') if data.get('chit_amount') else 0,
#                 # 'cash_amount':data.get('cash_amount') if data.get('cash_amount') else 0,
#                 # 'return_amount':data.get('return_amount') if data.get('return_amount') else 0,
#                 # 'card_amount':data.get('card_amount') if data.get('card_amount') else 0,
#                 # 'account_transfer_amount':data.get('account_transfer_amount') if data.get('account_transfer_amount') else 0,
#                 # 'upi_amount':data.get('upi_amount') if data.get('upi_amount') else 0,
#                 # 'paid_amount':data.get('paid_amount') if data.get('paid_amount') else 0, 
#             }

#             if request.user.role.is_admin == False:
#                 res_data['branch'] = request.user.branch.pk

#             else:
#                 res_data['branch'] = data.get('branch')

#             res_data['created_at'] = timezone.now()
#             res_data['created_by'] = request.user.id
 
#             serializer = BillingDetailsSerializer(data=res_data)
#             if serializer.is_valid():
#                 serializer.save()
                
#                 if int(res_data['bill_type']) == 1:
#                     bill_id_dict={}
#                     bill_id_dict['bill_id']=serializer.data['bill_no']
#                     bill_number_serializer=BillIDSerializer(data=bill_id_dict)

#                     if bill_number_serializer.is_valid():
#                         bill_number_serializer.save()
                    
#                 elif int(res_data['bill_type']) == 2:

#                     bill_id_dict={}
#                     bill_id_dict['silver_bill_id']=serializer.data['id']
#                     bill_number_serializer=SilverBillIDSerializer(data=bill_id_dict)

#                     if bill_number_serializer.is_valid():
#                         bill_number_serializer.save()
                
#                 else:
#                     pass
                
#                 # oldgold_details = request.data.get('old_gold_particulars', {})
#                 # if len(oldgold_details) != 0:
#                 #     new_oldgold_data = {}
#                 #     for oldgold in oldgold_details:
#                 #         try:
#                 #             new_oldgold_data['old_gold_no']=request.data.get('old_gold_no')
#                 #             # if len(str(oldgold.get('metal'))) != 0:
#                 #             # new_oldgold_data['old_gold_no']=oldgold['old_gold_no']
#                 #             new_oldgold_data['old_metal']=oldgold['metal']
#                 #             new_oldgold_data['item_name']=oldgold['item_name']
#                 #             new_oldgold_data['metal_rate']=oldgold['metal_rate']
#                 #             new_oldgold_data['old_gross_weight']=oldgold['gross_weight']
#                 #             new_oldgold_data['old_net_weight']=oldgold['net_weight']
#                 #             new_oldgold_data['dust_weight']=oldgold['dust_weight']
#                 #             new_oldgold_data['billing_details']=serializer.data['id']
#                 #             # new_oldgold_data['old_metal_rate']=oldgold['old_rate']
#                 #             # new_oldgold_data['today_metal_rate']=oldgold['today_rate']
#                 #             new_oldgold_data['total_old_gold_value']=oldgold['total']
#                 #             # new_oldgold_data['purity']=oldgold['purity']


#                 #             # if len(new_oldgold_data) != 0 :
#                 #             oldgold_serializer = BillingOldGoldSerializer(data=new_oldgold_data)
#                 #             if oldgold_serializer.is_valid():
#                 #                 oldgold_serializer.save()
#                 #             else:
#                 #                 raise Exception(oldgold_serializer.errors)
                            
#                 #         except Exception as error:
#                 #             raise Exception(error)
#                 billing_item_details = request.data.get('particulars', [])
                
#                 if len(billing_item_details) != 0:
#                     for item in billing_item_details:
#                         try:

#                             tag_number=item.get('tag_number')

#                             tag_queryset=TaggedItems.objects.get(tag_number=tag_number)
                            
#                             billing_tag_data = {
#                                 'billing_details': serializer.data['id'],
#                                 'billing_tag_item': tag_queryset.pk,
#                                 'tag_number': item.get('tag_number'),
#                                 'item_details': item.get('item_details'),
#                                 'sub_item_details': item.get('sub_item_details'),
#                                 'metal': item.get('metal'),
#                                 'net_weight': item.get('net_weight'),
#                                 'gross_weight' : item.get('gross_weight'),
#                                 'tag_weight' : item.get('tag_weight'),
#                                 'cover_weight' : item.get('cover_weight'),
#                                 'loop_weight' : item.get('loop_weight'),
#                                 'other_weight' : item.get('other_weight'),
#                                 'pieces' : item.get('pieces'),
#                                 'total_pieces' : item.get('total_pieces'),
#                                 'rate' : item.get('metal_rate'),
#                                 'stone_rate' : item.get('stone_rate'),
#                                 'diamond_rate' : item.get('diamond_rate'),
#                                 'stock_type' : item.get('stock_type'),
#                                 'calculation_type' : item.get('calculation_type'),
#                                 'tax_percent' : item.get('tax_percent'),
#                                 'additional_charges' : item.get('additional_charges'),
#                                 'total_stone_weight' : item.get('total_stone_weight'),
#                                 'total_diamond_weight' : item.get('total_diamond_weight'),
#                                 'per_gram_weight_type' : item.get('per_gram_weight_type',None),
#                                 'wastage_percentage' : item.get('wastage_percent', None),
#                                 'flat_wastage' : item.get('flat_wastage', None),
#                                 'making_charge' : item.get('making_charge', None),
#                                 'flat_making_charge' : item.get('flat_making_charge', None),
#                                 'wastage_calculation_type': item.get('wastage_calculation_type', None),
#                                 'making_charge_calculation_type': item.get('making_charge_calculation_type', None),
#                                 'gst' : item.get('gst'),
#                                 'total_rate' : item.get('with_gst_rate'),
#                                 'without_gst_rate':item.get('rate'),
#                                 'huid_rate':item.get('item_huid_rate'),
#                                 'employee_id':item.get('employee_id')
#                             }
#                             billing_taggeditem_serializer = BillingTagItemsSerializer(data=billing_tag_data)
#                             if billing_taggeditem_serializer.is_valid():
#                                 billing_taggeditem_serializer.save()

#                                 stone_details=item.get('stone_details') if item.get('stone_details') else []

#                                 for stone in stone_details:
#                                     stone['billing_details'] = serializer.data['id']
#                                     stone['billing_item_details'] = billing_taggeditem_serializer.data['id']
#                                     stone['stone_name']=float(stone['stone_name'])
#                                     stone['stone_pieces']=float(stone['stone_pieces'])
#                                     stone['stone_weight']=float(stone['stone_weight'])
#                                     stone['stone_weight_type']=int(stone['stone_weight_type'])
#                                     stone['stone_rate']=float(stone['stone_rate'])
#                                     stone['stone_rate_type']=int(stone['stone_rate_type'])
#                                     stone['include_stone_weight']=stone['include_stone_weight']

#                                     if int(stone['stone_weight_type']) == int(settings.CARAT):
#                                         stone['stone_weight']=(float(stone['stone_weight'])/5)

#                                     if int(stone['stone_rate_type']) == int(settings.PERGRAM):
#                                         total_stone_value=float(stone['stone_rate']*stone['stone_weight'])
#                                         stone['total_stone_value']=total_stone_value
                                    
#                                     if int(stone['stone_rate_type']) == int(settings.PERCARAT):
#                                         stone_rate = float(stone['stone_rate'])*5
#                                         stone['stone_rate'] = stone_rate
#                                         total_stone_value=float(stone['stone_rate']*stone['stone_weight'])
#                                         stone['total_stone_value']=total_stone_value

#                                     if int(stone['stone_rate_type']) == int(settings.PERPIECE):
#                                         total_stone_value=float(stone['stone_rate']*stone['stone_pieces'])
#                                         stone['total_stone_value']=total_stone_value

#                                     billing_stone_serializer=BillingStoneDetailsSerializer(data=stone)
#                                     if billing_stone_serializer.is_valid():
#                                         billing_stone_serializer.save()
#                                     else:
#                                         raise Exception (billing_stone_serializer.errors)

#                                 diamond_details=item.get('diamond_details') if item.get('diamond_details') else []

#                                 for diamond in diamond_details :

#                                     diamond['billing_details'] = serializer.data['id']
#                                     diamond['billing_item_details'] = billing_taggeditem_serializer.data['id']
#                                     diamond['diamond_name'] = float(diamond['diamond_name'])
#                                     diamond['diamond_pieces'] = float(diamond['diamond_pieces'])
#                                     diamond['diamond_weight'] = float(diamond['diamond_weight'])
#                                     diamond['diamond_weight_type'] = int(diamond['diamond_weight_type'])
#                                     diamond['diamond_rate'] = float(diamond['diamond_rate'])
#                                     diamond['diamond_rate_type'] = int(diamond['diamond_rate_type'])
#                                     diamond['include_diamond_weight'] = diamond['include_diamond_weight']

#                                     if int(diamond['diamond_weight_type']) == settings.CARAT :
#                                         diamond_weight=float(diamond['diamond_weight'])/5
#                                         diamond['diamond_weight']=diamond_weight

#                                     if int(diamond['diamond_rate_type']) ==settings.PERGRAM:
#                                         total_diamond_value=float(diamond['diamond_rate']*diamond['diamond_weight'])
#                                         diamond['total_diamond_value'] = total_diamond_value

#                                     if int(diamond['diamond_rate_type']) == settings.PERCARAT:
#                                         diamond_rate=float(diamond['diamond_rate'])*5
#                                         diamond['diamond_rate']=diamond_rate
#                                         total_diamond_value=float(diamond['diamond_rate']*diamond['diamond_weight'])
#                                         diamond['total_diamond_value'] = total_diamond_value

#                                     if int(diamond['diamond_rate_type']) ==settings.PERPIECE:
#                                         total_diamond_value=float(diamond['diamond_rate']*diamond['diamond_pieces'])
#                                         diamond['total_diamond_value'] = total_diamond_value

#                                     billing_diamond_serializer=BillingDiamondDetailsSerializer(data=diamond)
#                                     if billing_diamond_serializer.is_valid():
#                                         billing_diamond_serializer.save()
#                                     else:
#                                         raise Exception(billing_diamond_serializer.errors)
#                             else:
#                                 raise Exception(billing_taggeditem_serializer.errors)
#                         except Exception as err:
#                             raise Exception(err)
            
#                 stock_response=StockReduceBill(serializer.data['id'])
#                 print(stock_response)
#                 if stock_response != True:
#                     raise Exception(stock_response)

#                 return Response(
#                 {
#                     "data":serializer.data,
#                     "message":res_msg.create("Biling"),
#                     "status":status.HTTP_201_CREATED
#                 },status=status.HTTP_200_OK)
            
#             else:
#                 raise Exception(serializer.errors)
        
#         except Exception as err:
#             print(err)
#             transaction.set_rollback(True)
#             return Response(
#                 {
#                     "data":str(err),
#                     "message":res_msg.something_else(),
#                     "status":status.HTTP_204_NO_CONTENT
#                 },status=status.HTTP_200_OK
#             )

# @transaction.atomic
# def StockReduceBill(pk):
#     try:
#         billied_items=list(BillingTagItems.objects.filter(billing_details=pk))

#         for items in billied_items:

#             stock_queryset=TaggedItems.objects.get(tag_number=items.tag_number)
#             tag_details = []

#             if str(items.stock_type.pk) == settings.TAG:
#                 stock_details={}
#                 if stock_queryset.is_billed == False:

#                     res_data={
#                         "tag_number":stock_queryset.tag_number,
#                         "remaining_pieces":stock_queryset.remaining_pieces,
#                         "remaining_gross_weight":stock_queryset.remaining_gross_weight,
#                         "remaining_net_weight":stock_queryset.remaining_net_weight,
#                         "is_billed":False
#                     }

#                     stock_details['remaining_pieces']=stock_queryset.remaining_pieces-int(items.pieces)
#                     stock_details['remaining_gross_weight']=stock_queryset.remaining_gross_weight-float(items.gross_weight)
#                     stock_details['remaining_net_weight']=stock_queryset.remaining_net_weight-float(items.net_weight)
#                     stock_details['is_billed']=True

#                     tag_item_serializer=TaggedItemsSerializer(stock_queryset,data=stock_details,partial=True)

#                     if tag_item_serializer.is_valid():
#                         tag_item_serializer.save()
#                         tag_details.append(res_data)
#                     else:
#                         raise Exception(tag_item_serializer.errors)
                    
#                 else:
#                     raise Exception("The Item is already Billed")
                
#             elif str(items.stock_type.pk) == settings.NON_TAG:

#                 if stock_queryset.remaining_gross_weight >= items.gross_weight:

#                     stock_details={}
#                     res_data={
#                         "tag_number":stock_queryset.tag_number,
#                         "remaining_gross_weight":stock_queryset.remaining_gross_weight,
#                         "remaining_net_weight":stock_queryset.remaining_net_weight,
#                         "is_billed":False
#                     }
                    
#                     stock_details['remaining_gross_weight']=float(stock_queryset.remaining_gross_weight)-(float(items.gross_weight))
#                     stock_details['remaining_net_weight']=float(stock_queryset.remaining_net_weight)-(float(items.net_weight))

#                     tag_item_serializer=TaggedItemsSerializer(stock_queryset,data=stock_details,partial=True)

#                     if tag_item_serializer.is_valid():
#                         tag_item_serializer.save()

#                         if stock_queryset.remaining_gross_weight == 0:
#                             stock_queryset.is_billed = True
#                             stock_queryset.save()

#                         tag_details.append(res_data)


#                     else:
#                         raise Exception(tag_item_serializer.errors)
                    
#                 else:
#                     raise Exception ("The ramining weight is"+str(stock_queryset.remaining_gross_weight)+'gm')
                
#             elif str(items.stock_type.pk) == settings.PACKET:

#                 if stock_queryset.remaining_pieces >= items.pieces:

#                     stock_details={}
#                     res_data={
#                         "tag_number":stock_queryset.tag_number,
#                         "remaining_pieces":stock_queryset.remaining_pieces,
#                         "is_billed":False
#                     }

#                     stock_details['remaining_pieces']=int(stock_queryset.remaining_pieces)-(int(items.pieces))
                    

#                     tag_item_serializer=TaggedItemsSerializer(stock_queryset,data=stock_details,partial=True)

#                     if tag_item_serializer.is_valid():
#                         tag_item_serializer.save()

#                         if stock_queryset.remaining_pieces == 0:
#                             stock_queryset.is_billed = True
#                             stock_queryset.save()

#                         tag_details.append(res_data)
                            

#                     else:
#                         raise Exception(tag_item_serializer.errors)
                
#                 else:

#                     raise Exception("The Remaining pieces is"+str(stock_queryset.remaining_pieces))
            
#         return True
    
#     except Exception as err:
        
#         transaction.set_rollback(True)

#         return Response(
#             {
#                 "data":str(err),
#                 "message":res_msg.something_else(),
#                 "status":status.HTTP_204_NO_CONTENT
#             },status=status.HTTP_200_OK
#         )

       
        
       
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class EstimationDetailsApprovalView(APIView):

    def post(self, request):

        data = request.data

        # try:
        #     approve_rule_queryset = ApprovalRule.objects.get(approval_type=settings.ESTIMATION_APPROVAL_TYPE, approved_by=request.user.id, user_role=request.user.role,is_active=True)
            
        # except ApprovalRule.DoesNotExist:
        #     return Response({
        #         "message": "you don't have a permission to see the Estimate details approvals",
        #         "status": status.HTTP_401_UNAUTHORIZED
        # }, status=status.HTTP_200_OK)
        # except:
        #     return Response({
        #         "message": res_msg.something_else(),
        #         "status": status.HTTP_401_UNAUTHORIZED
        # }, status=status.HTTP_200_OK)

        data = request.data

        search = data.get('search') if data.get('search') else ""
        from_date = data.get('from_date') if data.get('from_date') != None else None
        to_date = data.get('to_date') if data.get('to_date') != None else None
        page = request.data.get('page') if request.data.get('page') else 1
        try:
            items_per_page = int(request.data.get('items_per_page', EstimateDetails.objects.all().count()))
            if items_per_page == 0:
                items_per_page = 10 
        except Exception as err:
            items_per_page = 10 

        if from_date != None and to_date != None:
            queryset = list(EstimateDetails.objects.filter(created_at__range=(from_date, to_date), estimate_no__icontains=search).order_by('-id'))
        else:
            queryset = list(EstimateDetails.objects.filter(estimate_no__icontains=search).order_by('-id'))
            
        paginated_data = Paginator(queryset, items_per_page)
        serializer = EstimateDetailsSerializer(paginated_data.get_page(page), many=True)

        res_data = []

        for i in range(0, len(serializer.data)):
            dict_data = serializer.data[i]
    
            dict_data['estimate_no'] = queryset[i].estimate_no
            dict_data['estimate_date'] = queryset[i].estimation_date
            dict_data['customer_name'] = queryset[i].customer_details.customer_name
            dict_data['customer_mobile'] = queryset[i].customer_details.phone
            dict_data['advance_amount'] = queryset[i].advance_amount
            dict_data['discount_amount'] = queryset[i].discount_amount
            dict_data['exchange_amount'] = queryset[i].exchange_amount
            dict_data['payable_amount'] = queryset[i].payable_amount
                
            res_data.append(dict_data)

        return Response({
            "data": {
                "list": res_data,
                "total_pages": paginated_data.num_pages,
                "current_page": page,
                "total_items": len(queryset),
                "current_items": len(res_data)
            },
            "message": res_msg.retrieve('Estimation Details'),
            "status": status.HTTP_200_OK
        },status=status.HTTP_200_OK)


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class EstimationStatusApprovalView(APIView):
    @transaction.atomic
    def put(self,request,pk):
        if pk != None:
            data = request.data
            try:
                estimate_queryset = EstimateDetails.objects.get(id=pk)

                # estimation_status = settings.ESTIMATION_APPROVAL_STATUS

                res_data={
                    'estimate_no':data.get('estimation_no'),
                    'bill_type':data.get('bill_type'),
                    'estimation_date':data.get('estimation_date'),
                    'customer_details':data.get('customer_details'),
                    'customer_mobile':data.get('customer_no'),
                    'total_amount':data.get('total_amount'),
                    'discount_percentage':data.get('discount_percentage'),
                    'discount_amount':data.get('discount_amount'),
                    'stone_amount':data.get('stone_amount'),
                    'diamond_amount':data.get('diamond_amount'),
                    'gst_amount':data.get('gst_amount'),
                    'advance_amount':data.get('advance_amount'),
                    'chit_amount':data.get('chit_amount'),
                    'salereturn_amount':data.get('salereturn_amount'),
                    'exchange_amount':data.get('exchange_amount'),
                    'gst_percentage':data.get('gst_percentage'),
                    'gst_amount':data.get('gst_amount'),
                    'gst_type':data.get('gst_type'),
                    'payable_amount':data.get('payable_amount'),
                    'advance_amount':data.get('advance_amount'),
                    'balance_amount':data.get('balance_amount'),
                }
                res_data['created_at'] = timezone.now()
                res_data['created_by'] = request.user.id
                
                serializer = EstimateDetailsSerializer(estimate_queryset,data=res_data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    estimation_details=serializer.data

                    oldgold_details = request.data.get('old_gold_particulars', {})
                    new_oldgold_data = {}
                    # new_oldgold_data['old_gold_no']=request.data.get('old_gold_no')
                    if len(oldgold_details) != 0:
                        for oldgold in oldgold_details:
                            try:
                                
                                oldgold_id = oldgold.get('id') if oldgold.get('id') != None else 0
                                oldgold_queryset = EstimationOldGold.objects.get(id=oldgold_id)

                                new_oldgold_data['old_metal']=oldgold['metal']
                                new_oldgold_data['metal_rate']=oldgold['metal_rate']
                                new_oldgold_data['old_gross_weight']=oldgold['gross_weight']
                                new_oldgold_data['old_reduce_weight']=oldgold['old_reduce_weight']
                                new_oldgold_data['old_net_weight']=oldgold['net_weight']
                                new_oldgold_data['old_touch']=oldgold['old_touch']
                                new_oldgold_data['dust_weight']=oldgold['dust_weight']
                                new_oldgold_data['estimation_details']=serializer.data['id']
                                new_oldgold_data['old_metal_rate']=oldgold['old_rate']
                                new_oldgold_data['total_old_gold_value']=oldgold['total']
                                new_oldgold_data['employee_id']=oldgold['employee_id']
                            
                                if len(new_oldgold_data) != 0 :
                                    oldgold_serializer = EstimationOldGoldSerializer(oldgold_queryset,data=new_oldgold_data,partial=True)
                                    if oldgold_serializer.is_valid():
                                        oldgold_serializer.save()
                                    else:
                                        raise Exception(oldgold_serializer.errors)
                                else:
                                    pass
                                
                            except EstimationOldGold.DoesNotExist:
                                

                                new_oldgold_data['estimation_details'] = estimation_details['id']
                                new_oldgold_data['old_metal']=oldgold['metal']
                                new_oldgold_data['metal_rate']=oldgold['metal_rate']
                                new_oldgold_data['old_gross_weight']=oldgold['gross_weight']
                                new_oldgold_data['old_reduce_weight']=oldgold['old_reduce_weight']
                                new_oldgold_data['old_net_weight']=oldgold['net_weight']
                                new_oldgold_data['old_touch']=oldgold['old_touch']
                                new_oldgold_data['dust_weight']=oldgold['dust_weight']
                                new_oldgold_data['estimation_details']=serializer.data['id']
                                new_oldgold_data['old_metal_rate']=oldgold['old_rate']
                                new_oldgold_data['total_old_gold_value']=oldgold['total']
                                new_oldgold_data['employee_id']=oldgold['employee_id']
                            
                                if len(new_oldgold_data) != 0 :
                                    oldgold_serializer = EstimationOldGoldSerializer(data=new_oldgold_data)
                                    if oldgold_serializer.is_valid():
                                        oldgold_serializer.save()
                                    else:
                                        raise Exception(oldgold_serializer.errors)
                                else:
                                    pass
                            
                    estimation_item_details = request.data.get('particulars', [])
                    
                    if len(estimation_item_details) != 0:
                        for item in estimation_item_details:
                            
                            try:
                                item_id=item.get('id') if item.get('id') else 0
                                
                                estimation_tagitem_queryset = EstimationTagItems.objects.get(id=item_id)
                                
                                tag_number=item.get('tag_number')
                                tag_queryset=TaggedItems.objects.get(tag_number=tag_number)

                                estimation_tag_data = {
                                    'estimation_details': estimation_details['id'],
                                    'estimation_tag_item': tag_queryset.pk,
                                    'tag_number': item.get('tag_number'),
                                    'item_details': item.get('item_details'),
                                    'sub_item_details': item.get('sub_item_details'),
                                    'metal': item.get('metal'),
                                    'net_weight': item.get('net_weight'),
                                    'gross_weight' : item.get('gross_weight'),
                                    'tag_weight' : item.get('tag_weight'),
                                    'cover_weight' : item.get('cover_weight'),
                                    'loop_weight' : item.get('loop_weight'),
                                    'other_weight' : item.get('other_weight'),
                                    'pieces' : item.get('pieces'),
                                    'total_pieces' : item.get('total_pieces'),
                                    'rate' : item.get('metal_rate'),
                                    'stone_rate' : item.get('stone_rate'),
                                    'diamond_rate' : item.get('diamond_rate'),
                                    'stock_type' : item.get('stock_type'),
                                    'calculation_type' : item.get('calculation_type'),
                                    'tax_percent' : item.get('tax_percent'),
                                    'additional_charges' : item.get('additional_charges'),
                                    'total_stone_weight' : item.get('total_stone_weight'),
                                    'total_diamond_weight' : item.get('total_diamond_weight'),
                                    'per_gram_weight_type' : item.get('per_gram_weight_type',None),
                                    'wastage_percentage' : item.get('wastage_percent', None),
                                    'flat_wastage' : item.get('flat_wastage', None),
                                    'making_charge' : item.get('making_charge', None),
                                    'flat_making_charge' : item.get('flat_making_charge', None),
                                    'wastage_calculation_type': item.get('wastage_calculation_type', None),
                                    'making_charge_calculation_type': item.get('making_charge_calculation_type', None),
                                    'gst' : item.get('gst'),
                                    'total_rate' : item.get('with_gst_rate'),
                                    'without_gst_rate':item.get('rate'),
                                    'huid_rate':item.get('item_huid_rate'),
                                    'employee_id':item.get('employee_id')
                                }
                                
                                estimation_taggeditem_serializer = EstimationTagItemsSerializer(estimation_tagitem_queryset,data=estimation_tag_data,partial=True)
                                if estimation_taggeditem_serializer.is_valid():
                                    estimation_taggeditem_serializer.save()

                                    stone_details=item.get('stone_details') if item.get('stone_details') else []
                                    
                                    for stone in stone_details:
                                        try:
                                            stone_id=stone.get('id') if stone.get('id') else None
                                            
                                            stone_queryset = EstimationStoneDetails.objects.get(id=stone_id)
                                            
                                            stone_item = {
                                                'estimation_details': estimation_details['id'],
                                                'estimation_item_details': estimation_taggeditem_serializer.data['id'],
                                                'id': int(stone.get('id')),
                                                'stone_name': int(stone.get('stone_name')),
                                                'stone_pieces': int(stone.get('stone_pieces')),
                                                'stone_weight': float(stone.get('stone_weight')),
                                                'stone_weight_type': int(stone.get('stone_weight_type')),
                                                'stone_rate': float(stone.get('stone_rate')),
                                                'stone_rate_type': int(stone.get('stone_rate_type')),
                                                'include_stone_weight': stone.get('include_stone_weight'),
                                            }
                                            
                                            if int(stone.get('stone_weight_type')) == int(settings.CARAT):
                                                stone_item['stone_weight']=(float(stone.get('stone_weight'))/5)

                                            if int(stone.get('stone_rate_type')) == int(settings.PERGRAM):
                                                total_stone_value=float(stone.get('stone_rate'))*float(stone.get('stone_weight'))
                                                stone_item['total_stone_value']=total_stone_value
                                            
                                            if int(stone.get('stone_rate_type')) == int(settings.PERCARAT):
                                                stone_rate = float(stone.get('stone_rate'))*5
                                                stone_item['stone_rate'] = stone_rate
                                                total_stone_value=float(stone.get('stone_rate'))*float(stone.get('stone_weight'))
                                                stone_item['total_stone_value']=total_stone_value

                                            if int(stone.get('stone_rate_type')) == int(settings.PERPIECE):
                                                total_stone_value=float(stone.get('stone_rate'))*float(stone.get('stone_pieces'))
                                                stone_item['total_stone_value']=total_stone_value
                                            
                                            estimation_stone_serializer=EstimationStoneDetailsSerializer(stone_queryset,data=stone_item,partial=True)
                                            if estimation_stone_serializer.is_valid():
                                                estimation_stone_serializer.save()
                                            else:
                                                raise Exception (estimation_stone_serializer.errors)
                                        
                                        except EstimationStoneDetails.DoesNotExist:
                                            
                                            stone_item = {
                                                'estimation_details': estimation_details['id'],
                                                'estimation_item_details': estimation_taggeditem_serializer.data['id'],
                                                'stone_name': int(stone.get('stone_name')),
                                                'stone_pieces': int(stone.get('stone_pieces')),
                                                'stone_weight': float(stone.get('stone_weight')),
                                                'stone_weight_type': int(stone.get('stone_weight_type')),
                                                'stone_rate': float(stone.get('stone_rate')),
                                                'stone_rate_type': int(stone.get('stone_rate_type')),
                                                'include_stone_weight': stone.get('include_stone_weight')
                                            }
                                            
                                            if int(stone.get('stone_weight_type')) == int(settings.CARAT):
                                                stone_item['stone_weight']=(float(stone.get('stone_weight'))/5)

                                            if int(stone.get('stone_rate_type')) == int(settings.PERGRAM):
                                                total_stone_value=float(stone.get('stone_rate'))*float(stone.get('stone_weight'))
                                                stone_item['total_stone_value']=total_stone_value
                                            
                                            if int(stone.get('stone_rate_type')) == int(settings.PERCARAT):
                                                stone_rate = float(stone.get('stone_rate'))*5
                                                stone_item['stone_rate'] = stone_rate
                                                total_stone_value=float(stone.get('stone_rate'))*float(stone.get('stone_weight'))
                                                stone_item['total_stone_value']=total_stone_value

                                            if int(stone.get('stone_rate_type')) == int(settings.PERPIECE):
                                                total_stone_value=float(stone.get('stone_rate'))*float(stone.get('stone_pieces'))
                                                stone_item['total_stone_value']=total_stone_value

                                            stone_new_serializer=EstimationStoneDetailsSerializer(data=stone_item)

                                            if stone_new_serializer.is_valid():
                                                stone_new_serializer.save()

                                        except Exception as err:
                                            raise Exception(err)

                                    diamond_details=item.get('diamond_details') if item.get('diamond_details') else []

                                    for diamond in diamond_details :
                                        try:
                                            diamond_id=diamond.get('id') if diamond.get('id') else None

                                            diamond_queryset = EstimationDiamondDetails.objects.get(id=diamond_id)

                                            diamond_item = {
                                                'estimation_details': estimation_details['id'],
                                                'estimation_item_details': estimation_taggeditem_serializer.data['id'],
                                                'id': int(diamond.get('id')),
                                                'diamond_name': int(diamond.get('diamond_name')),
                                                'diamond_pieces': int(diamond.get('diamond_pieces')),
                                                'diamond_weight': float(diamond.get('diamond_weight')),
                                                'diamond_weight_type': int(diamond.get('diamond_weight_type')),
                                                'diamond_rate': float(diamond.get('diamond_rate')),
                                                'diamond_rate_type': int(diamond.get('diamond_rate_type')),
                                                'include_diamond_weight': diamond.get('include_diamond_weight')
                                            }
                                            
                                            if int(diamond.get('diamond_weight_type')) == settings.CARAT :
                                                diamond_weight=float(diamond.get('diamond_weight'))/5
                                                diamond_item['diamond_weight']=diamond_weight

                                            if int(diamond.get('diamond_rate_type')) ==settings.PERGRAM:
                                                total_diamond_value=float(diamond.get('diamond_rate'))*float(diamond.get('diamond_weight'))
                                                diamond_item['total_diamond_value'] = total_diamond_value

                                            if int(diamond.get('diamond_rate_type')) == settings.PERCARAT:
                                                diamond_rate=float(diamond.get('diamond_rate'))*5
                                                diamond_item['diamond_rate']=diamond_rate
                                                total_diamond_value=float(diamond.get('diamond_rate'))*float(diamond.get('diamond_weight'))
                                                diamond_item['total_diamond_value'] = total_diamond_value

                                            if int(diamond.get('diamond_rate_type')) ==settings.PERPIECE:
                                                total_diamond_value=float(diamond.get('diamond_rate'))*int(diamond.get('diamond_pieces'))
                                                diamond_item['total_diamond_value'] = total_diamond_value
                                            
                                            estimation_diamond_serializer=EstimationDiamondDetailsSerializer(diamond_queryset,data=diamond_item,partial=True)
                                            if estimation_diamond_serializer.is_valid():
                                                estimation_diamond_serializer.save()
                                            else:
                                                raise Exception(estimation_diamond_serializer.errors)
                                            
                                        except EstimationDiamondDetails.DoesNotExist:
                                            
                                            diamond_item = {
                                                'estimation_details': estimation_details['id'],
                                                'estimation_item_details': estimation_taggeditem_serializer.data['id'],
                                                'diamond_name': int(diamond.get('diamond_name')),
                                                'diamond_pieces': int(diamond.get('diamond_pieces')),
                                                'diamond_weight': float(diamond.get('diamond_weight')),
                                                'diamond_weight_type': int(diamond.get('diamond_weight_type')),
                                                'diamond_rate': float(diamond.get('diamond_rate')),
                                                'diamond_rate_type': int(diamond.get('diamond_rate_type')),
                                                'include_diamond_weight': diamond.get('include_diamond_weight')
                                            }

                                            if int(diamond.get('diamond_weight_type')) == settings.CARAT :
                                                diamond_weight=float(diamond.get('diamond_weight'))/5
                                                diamond_item['diamond_weight']=diamond_weight

                                            if int(diamond.get('diamond_rate_type')) ==settings.PERGRAM:
                                                total_diamond_value=float(diamond.get('diamond_rate')*diamond.get('diamond_weight'))
                                                diamond_item['total_diamond_value'] = total_diamond_value

                                            if int(diamond.get('diamond_rate_type')) == settings.PERCARAT:
                                                diamond_rate=float(diamond.get('diamond_rate'))*5
                                                diamond_item['diamond_rate']=diamond_rate
                                                total_diamond_value=float(diamond.get('diamond_rate')*diamond.get('diamond_weight'))
                                                diamond_item['total_diamond_value'] = total_diamond_value

                                            if int(diamond.get('diamond_rate_type')) ==settings.PERPIECE:
                                                total_diamond_value=float(diamond.get('diamond_rate')*diamond.get('diamond_pieces'))
                                                diamond_item['total_diamond_value'] = total_diamond_value
                                            
                                            diamond_new_serializer=EstimationDiamondDetailsSerializer(data=diamond_item)

                                            if diamond_new_serializer.is_valid():
                                                diamond_new_serializer.save()
                                        
                                        except Exception as err:
                                            raise Exception(err)
                                else:
                                    raise Exception(estimation_taggeditem_serializer.errors)
                                
                            except EstimationTagItems.DoesNotExist:

                                tag_number=item.get('tag_number')
                                tag_queryset=TaggedItems.objects.get(tag_number=tag_number)

                                estimation_tag_data = {
                                    'estimation_details': estimation_details['id'],
                                    'estimation_tag_item': tag_queryset.pk,
                                    'tag_number': item.get('tag_number'),
                                    'item_details': item.get('item_details'),
                                    'sub_item_details': item.get('sub_item_details'),
                                    'metal': item.get('metal'),
                                    'net_weight': item.get('net_weight'),
                                    'gross_weight' : item.get('gross_weight'),
                                    'tag_weight' : item.get('tag_weight'),
                                    'cover_weight' : item.get('cover_weight'),
                                    'loop_weight' : item.get('loop_weight'),
                                    'other_weight' : item.get('other_weight'),
                                    'pieces' : item.get('pieces'),
                                    'total_pieces' : item.get('total_pieces'),
                                    'rate' : item.get('metal_rate'),
                                    'stone_rate' : item.get('stone_rate'),
                                    'diamond_rate' : item.get('diamond_rate'),
                                    'stock_type' : item.get('stock_type'),
                                    'calculation_type' : item.get('calculation_type'),
                                    'tax_percent' : item.get('tax_percent'),
                                    'additional_charges' : item.get('additional_charges'),
                                    'total_stone_weight' : item.get('total_stone_weight'),
                                    'total_diamond_weight' : item.get('total_diamond_weight'),
                                    'per_gram_weight_type' : item.get('per_gram_weight_type',None),
                                    'wastage_percentage' : item.get('wastage_percent', None),
                                    'flat_wastage' : item.get('flat_wastage', None),
                                    'making_charge' : item.get('making_charge', None),
                                    'flat_making_charge' : item.get('flat_making_charge', None),
                                    'wastage_calculation_type': item.get('wastage_calculation_type', None),
                                    'making_charge_calculation_type': item.get('making_charge_calculation_type', None),
                                    'gst' : item.get('gst'),
                                    'total_rate' : item.get('with_gst_rate'),
                                    'without_gst_rate':item.get('rate'),
                                    'huid_rate':item.get('item_huid_rate'),
                                    'employee_id':item.get('employee_id')
                                }
                                
                                estimation_taggeditem_serializer = EstimationTagItemsSerializer(data=estimation_tag_data)
                                if estimation_taggeditem_serializer.is_valid():
                                    estimation_taggeditem_serializer.save()

                                    stone_details=item.get('stone_details') if item.get('stone_details') else []
                                    
                                    for stone in stone_details:
                                        stone_item = {
                                            'estimation_details': estimation_details['id'],
                                            'estimation_item_details': estimation_taggeditem_serializer.data['id'],
                                            'stone_name': int(stone.get('stone_name')),
                                            'stone_pieces': int(stone.get('stone_pieces')),
                                            'stone_weight': float(stone.get('stone_weight')),
                                            'stone_weight_type': int(stone.get('stone_weight_type')),
                                            'stone_rate': float(stone.get('stone_rate')),
                                            'stone_rate_type': int(stone.get('stone_rate_type')),
                                            'include_stone_weight': stone.get('include_stone_weight')
                                        }
                                        
                                        if int(stone.get('stone_weight_type')) == int(settings.CARAT):
                                            stone_item['stone_weight']=(float(stone.get('stone_weight'))/5)

                                        if int(stone.get('stone_rate_type')) == int(settings.PERGRAM):
                                            total_stone_value=float(stone.get('stone_rate'))*float(stone.get('stone_weight'))
                                            stone_item['total_stone_value']=total_stone_value
                                        
                                        if int(stone.get('stone_rate_type')) == int(settings.PERCARAT):
                                            stone_rate = float(stone.get('stone_rate'))*5
                                            stone_item['stone_rate'] = stone_rate
                                            total_stone_value=float(stone.get('stone_rate'))*float(stone.get('stone_weight'))
                                            stone_item['total_stone_value']=total_stone_value

                                        if int(stone.get('stone_rate_type')) == int(settings.PERPIECE):
                                            total_stone_value=float(stone.get('stone_rate'))*float(stone.get('stone_pieces'))
                                            stone_item['total_stone_value']=total_stone_value

                                        stone_new_serializer=EstimationStoneDetailsSerializer(data=stone_item)

                                        if stone_new_serializer.is_valid():
                                            stone_new_serializer.save()
                                        else:
                                            raise Exception(stone_new_serializer.errors)
                                        
                                    diamond_details=item.get('diamond_details') if item.get('diamond_details') else []

                                    for diamond in diamond_details :  
                                        diamond_item = {
                                            'estimation_details': estimation_details['id'],
                                            'estimation_item_details': estimation_taggeditem_serializer.data['id'],
                                            'diamond_name': int(diamond.get('diamond_name')),
                                            'diamond_pieces': int(diamond.get('diamond_pieces')),
                                            'diamond_weight': float(diamond.get('diamond_weight')),
                                            'diamond_weight_type': int(diamond.get('diamond_weight_type')),
                                            'diamond_rate': float(diamond.get('diamond_rate')),
                                            'diamond_rate_type': int(diamond.get('diamond_rate_type')),
                                            'include_diamond_weight': diamond.get('include_diamond_weight')
                                        }

                                        if int(diamond.get('diamond_weight_type')) == settings.CARAT :
                                            diamond_weight=float(diamond.get('diamond_weight'))/5
                                            diamond_item['diamond_weight']=diamond_weight

                                        if int(diamond.get('diamond_rate_type')) ==settings.PERGRAM:
                                            total_diamond_value=float(diamond.get('diamond_rate')*diamond.get('diamond_weight'))
                                            diamond_item['total_diamond_value'] = total_diamond_value

                                        if int(diamond.get('diamond_rate_type')) == settings.PERCARAT:
                                            diamond_rate=float(diamond.get('diamond_rate'))*5
                                            diamond_item['diamond_rate']=diamond_rate
                                            total_diamond_value=float(diamond.get('diamond_rate')*diamond.get('diamond_weight'))
                                            diamond_item['total_diamond_value'] = total_diamond_value

                                        if int(diamond.get('diamond_rate_type')) ==settings.PERPIECE:
                                            total_diamond_value=float(diamond.get('diamond_rate')*diamond.get('diamond_pieces'))
                                            diamond_item['total_diamond_value'] = total_diamond_value
                                        
                                        diamond_new_serializer=EstimationDiamondDetailsSerializer(data=diamond_item)

                                        if diamond_new_serializer.is_valid():
                                            diamond_new_serializer.save()
                                        else:
                                            raise Exception(diamond_new_serializer.errors)

                            except Exception as err:
                                raise Exception(err)

                    return Response(
                        {
                            "message":res_msg.update("Estimation Biling"),
                            "status":status.HTTP_200_OK
                        },status=status.HTTP_200_OK) 
                else:
                    raise Exception(serializer.errors)
            
            except Exception as err:
                transaction.set_rollback(True)
                return Response(
                    {
                        "data":str(err),
                        "message":res_msg.something_else(),
                        "status":status.HTTP_204_NO_CONTENT
                    },status=status.HTTP_200_OK
                )
        else:
            return Response(
                {
                    "data":str(err),
                    "message":res_msg.not_exists("Given Id"),
                    "status":status.HTTP_204_NO_CONTENT
                },status=status.HTTP_200_OK
            )

            
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# class BillingListView(APIView):

#     def get(self,request,branch=None):

#         filter_condition = {}

#         if request.user.role.is_admin == False:
#             filter_condition['branch'] = request.user.branch.pk

#         else:
#             filter_condition['branch'] = branch

#         queryset = list(BillingDetails.objects.all().values('id','bill_no','bill_date','customer_mobile','customer_details__customer_name'))

#         return Response(
#             {
#                 "data":{
#                     "list":queryset
#                 },
#                 "message":res_msg.retrieve('Bill List'),
#                 "status":status.HTTP_200_OK
#             },status=status.HTTP_200_OK
#         )


#     def post(self, request):

#         search = request.data.get('search') if request.data.get('search') else ''
#         from_date = request.data.get('from_date') if request.data.get('from_date') else None
#         to_date = request.data.get('to_date') if request.data.get('to_date') else None
#         page = request.data.get('page') if request.data.get('page') else 1
#         try:
#             items_per_page = int(request.data.get('items_per_page', BillingDetails.objects.all().count()))
#             if items_per_page == 0:
#                 items_per_page = 10 
#         except Exception as err:
#             items_per_page = 10 
        
#         filter_condition={}

#         if from_date != None and to_date!= None:
#            date_range=(from_date,to_date)
#            filter_condition['payment_date__range']=date_range

#         if len(filter_condition) != 0:
#                 queryset = list(BillingDetails.objects.filter(Q(customer_details__customer_name__icontains=search) | Q(customer_mobile__icontains=search) | Q(bill_no=search),**filter_condition).order_by('-id'))
#         elif search != '':
#                 queryset = list(BillingDetails.objects.filter(Q(customer_id__customer_name__icontains=search) | Q(customer_mobile__icontains=search) | Q(bill_no=search)).order_by('-id'))
#         else:
#             queryset = list(BillingDetails.objects.all().order_by('-id'))

#         paginated_data = Paginator(queryset, items_per_page)
#         serializer = BillingDetailsSerializer(paginated_data.get_page(page), many=True)

#         res_data = []
        
#         for i in range(len(serializer.data)):
#             dict_data = serializer.data[i]

#             bill_tagitem_queryset = BillingTagItems.objects.filter(billing_details=queryset[i].pk).order_by('-id')
#             total_weight = 0
#             for data in bill_tagitem_queryset:
#                 total_weight = data.gross_weight
#                 dict_data['total_weight'] =total_weight

#             try:
#                 payment_queryset = CommonPaymentDetails.objects.get(refference_number=queryset[i].bill_no)
#                 dict_data['igst_amount'] = payment_queryset.igst_amount
#                 dict_data['sgst_amount'] = payment_queryset.sgst_amount
#                 dict_data['cgst_amount'] = payment_queryset.cgst_amount
#             except:
#                 dict_data['igst_amount'] = 0
#                 dict_data['sgst_amount'] = 0
#                 dict_data['cgst_amount'] = 0

#             dict_data['customer_name'] = queryset[i].customer_details.customer_name
            
#             res_data.append(dict_data)

#         return Response({
#             "data": {
#                 "list": res_data,
#                 "total_pages": paginated_data.num_pages,
#                 "current_page": page,
#                 "total_items": len(queryset),
#                 "current_items": len(serializer.data)
#             },
#             "message": res_msg.retrieve('Billing Payment Details'),
#             "status": status.HTTP_200_OK
#         }, status=status.HTTP_200_OK)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class BillnumberView(APIView):  
    def get(self, request):  
        try:
            queryset=BillID.objects.all().order_by('-id')[0]
            prefix = 'BILLGD-00'
            new_bill_id=f'{prefix}{int(queryset.pk)+1}'
            return Response(
                {
                    "bill_number":new_bill_id,
                    "message":res_msg.retrieve("Bill Number"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        
        except Exception as err:
            return Response(
                {
                    "bill_number":"BILLGD-001",
                    "message":res_msg.retrieve("Bill Number"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
    
# Generate Estimate Number
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class OldgoldNumberGenerateAPIView(APIView):
    def get(self,request):
        prefix = 'OG'  # Prefix for the estimate number
        # timestamp = datetime.now().strftime('%Y%m%d%H%M%S')  # Current date and time
        random_number = random.randint(1000000, 9999999)
        estimate_number = f'{prefix}-{random_number}'

        return Response(
            {
                "data": estimate_number,
                "message" : res_msg.create("Old Gold Number"),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK
        ) 

# Generate Estimate Number
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class OldgoldNumberForBillAPIView(APIView):
    def get(self,request):
        prefix = 'OG'  # Prefix for the estimate number
        random_number = random.randint(1000000, 5555555)
        estimate_number = f'{prefix}-{random_number}'

        return Response(
            {
                "data": estimate_number,
                "message" : res_msg.create("Old Gold Number"),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK
        ) 
  

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class GetEstimateNoForApprovedOnly(APIView):
    def get(self,request,branch=None):
        if branch != None:
            queryset = list(EstimateDetails.objects.filter(is_billed=False,estimation_status=6,branch=branch).order_by('-id'))
        else:
            queryset = list(EstimateDetails.objects.filter(is_billed=False,estimation_status=6).order_by('-id'))
        serializer = EstimateDetailsSerializer(queryset,many=True)
        res_data = []
        
        for item in serializer.data:
            estimate_data = {}
            estimate_data['id'] = item['id']
            estimate_data['estimate_number'] = item['estimate_no']

            res_data.append(estimate_data)
        return Response(
            {
                "data": {
                    "list" : res_data
                },
                "message" : res_msg.retrieve("Estimate details"),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK
        ) 
       


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class BillingReviseView(APIView):
    @transaction.atomic
    def put(self,request,pk):
        if pk != None:
            data = request.data
            
            billing_queryset = BillingDetails.objects.get(id=pk)
            try:
                res_data={
                    'estimation_details':data.get('estimation_details') if data.get('estimation_details') else None ,
                    'bill_no':data.get('bill_no'),
                    'bill_date':data.get('bill_date'),
                    'customer_details':data.get('customer_details'),
                    'customer_mobile':data.get('customer_no'),
                    'total_amount':data.get('total_amount'),
                    'gst_amount':data.get('gst_amount'),
                    'advance_amount':data.get('advance_amount') ,
                    'discount_amount':data.get('discount_amount'),
                    'exchange_amount':data.get('exchange_amount'),
                    'payable_amount':data.get('payable_amount'),
                    'cash_amount':data.get('cash_amount') if data.get('cash_amount') else 0,
                    'card_amount':data.get('card_amount') if data.get('card_amount') else 0,
                    'return_amount':data.get('return_amount') if data.get('return_amount') else 0,
                    'account_transfer_amount':data.get('account_transfer_amount') if data.get('account_transfer_amount') else 0,
                    'upi_amount':data.get('upi_amount') if data.get('upi_amount') else 0,
                    'paid_amount':data.get('paid_amount') if data.get('paid_amount') else 0,
                
                }

                if request.user.role.is_admin == True:
                    res_data['branch'] = data.get('branch')
                else:
                    res_data['branch'] = request.user.branch.pk
            
                res_data['modified_at'] = timezone.now()
                res_data['modified_by'] = request.user.id
                
                serializer = BillingDetailsSerializer(billing_queryset,data=res_data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    
                    # new_oldgold_data = {}
                    # new_oldgold_data['old_gold_no']=data.get('old_gold_no')
                    # oldgold_details = request.data.get('old_gold_particulars', {})
                    
                    # if len(oldgold_details) != 0:
                    #     for oldgold in oldgold_details:
                    #         try:
                    #             oldgold_id = oldgold.get('id') if oldgold.get('id') != None else 0
                                
                    #             old_gold_queryset = BillingOldGold.objects.get(id=oldgold_id)

                    #             new_oldgold_data['old_metal']=oldgold['metal']
                    #             # new_oldgold_data['metal_rate']=oldgold['metal_rate']
                    #             new_oldgold_data['old_gross_weight']=oldgold['gross_weight']
                    #             # new_oldgold_data['old_net_weight']=oldgold['net_weight']
                    #             # new_oldgold_data['dust_weight']=oldgold['dust_weight']
                    #             new_oldgold_data['billing_details']=serializer.data['id']
                    #             # new_oldgold_data['old_metal_rate']=oldgold['old_rate']
                    #             # new_oldgold_data['today_metal_rate']=oldgold['today_rate']
                    #             new_oldgold_data['total_old_gold_value']=oldgold['total']
                    #             new_oldgold_data['purity']=oldgold['purity']
                               
                    #             oldgold_serializer = BillingOldGoldSerializer(old_gold_queryset,data=new_oldgold_data,partial=True)
                    #             if oldgold_serializer.is_valid():
                    #                 oldgold_serializer.save()
                                    
                    #             else:
                    #                 raise Exception(oldgold_serializer.errors)
                                
                    #         except BillingOldGold.DoesNotExist:
                    #             new_oldgold_data['old_metal']=oldgold['metal']
                    #             new_oldgold_data['old_gross_weight']=oldgold['gross_weight']
                    #             new_oldgold_data['billing_details']=serializer.data['id']
                    #             new_oldgold_data['total_old_gold_value']=oldgold['total']
                    #             new_oldgold_data['purity']=oldgold['purity']
                               
                    #             oldgold_serializer = BillingOldGoldSerializer(data=new_oldgold_data)
                    #             if oldgold_serializer.is_valid():
                    #                 oldgold_serializer.save()
                    #             else:
                    #                 raise Exception(oldgold_serializer.errors)
                            
                    #         except Exception as err:
                    #             raise Exception(err)
                                
                    billing_item_details = request.data.get('particulars', [])
                    
                    if len(billing_item_details) != 0:
                        for item in billing_item_details:
                            try:
                                item_id = item.get('id') if item.get('id') != None else 0
                                
                                billing_tagitem_queryset = BillingParticularDetails.objects.get(id=item_id)

                                billing_tag_data = {
                                    'billing_details': serializer.data['id'],
                                    'billing_tag_item': item.get('tag_item_id'),
                                    'tag_number': item.get('tag_number'),
                                    'item_details': item.get('item_details'),
                                    'sub_item_details': item.get('sub_item_details'),
                                    'metal': item.get('metal'),
                                    'net_weight': item.get('net_weight'),
                                    'gross_weight' : item.get('gross_weight'),
                                    'tag_weight' : item.get('tag_weight'),  
                                    'cover_weight' : item.get('cover_weight'),
                                    'loop_weight' : item.get('loop_weight'),
                                    'other_weight' : item.get('other_weight'),
                                    'pieces' : item.get('pieces'),
                                    'total_pieces' : item.get('total_pieces'),
                                    'rate' : item.get('metal_rate'),
                                    'stone_rate' : item.get('stone_rate'),
                                    'diamond_rate' : item.get('diamond_rate'),
                                    'stock_type' : item.get('stock_type'),
                                    'calculation_type' : item.get('calculation_type'),
                                    'tax_percent' : item.get('tax_percent'),
                                    'additional_charges' : item.get('additional_charges'),
                                    'total_stone_weight' : item.get('total_stone_weight'),
                                    'total_diamond_weight' : item.get('total_diamond_weight'),
                                    'per_gram_weight_type' : item.get('per_gram_weight_type',None),
                                    'wastage_percentage' : item.get('wastage_percent', None),
                                    'flat_wastage' : item.get('flat_wastage', None),
                                    'making_charge' : item.get('making_charge', None),
                                    'flat_making_charge' : item.get('flat_making_charge', None),
                                    'wastage_calculation_type': item.get('wastage_calculation_type', None),
                                    'making_charge_calculation_type': item.get('making_charge_calculation_type', None),
                                    'gst' : item.get('gst'),
                                    'total_rate' : item.get('with_gst_rate'),
                                    'without_gst_rate':item.get('rate'),
                                    'huid_rate':item.get('item_huid_rate'),
                                    'employee_id':item.get('employee_id')
                                }
                                
                                billing_taggeditem_serializer = BillingParticularDetailsSerializer(billing_tagitem_queryset,data=billing_tag_data,partial=True)
                                if billing_taggeditem_serializer.is_valid():
                                    billing_taggeditem_serializer.save()

                                    stone_details=item.get('stone_details') if item.get('stone_details') else []

                                    for stone in stone_details:
                                        try:

                                            stone_id = stone.get('id') if stone.get('id') != None else 0
                                            billing_stone_queryset = BillingParticularStoneDetails.objects.get(id=stone_id)

                                            stone['billing_details'] = serializer.data['id']
                                            stone['billing_item_details'] = billing_taggeditem_serializer.data['id']
                                            stone['stone']=float(stone['stone_name'])
                                            stone['stone_pieces']=float(stone['stone_pieces'])
                                            stone['stone_weight']=float(stone['stone_weight'])
                                            stone['stone_weight_type']=int(stone['stone_weight_type'])
                                            stone['stone_amount']=float(stone['stone_rate'])
                                            stone['stone_rate_type']=int(stone['stone_rate_type'])
                                            stone['reduce_weight']=stone['include_stone_weight']

                                            if int(stone['stone_weight_type']) == int(settings.CARAT):
                                                stone['stone_weight']=(float(stone['stone_weight'])/5)

                                            if int(stone['stone_rate_type']) == int(settings.PERGRAM):
                                                total_stone_value=float(stone['stone_rate']*stone['stone_weight'])
                                                stone['total_stone_value']=total_stone_value
                                            
                                            if int(stone['stone_rate_type']) == int(settings.PERCARAT):
                                                stone_rate = float(stone['stone_rate'])*5
                                                stone['stone_rate'] = stone_rate
                                                total_stone_value=float(stone['stone_rate']*stone['stone_weight'])
                                                stone['total_stone_value']=total_stone_value

                                            if int(stone['stone_rate_type']) == int(settings.PERPIECE):
                                                total_stone_value=float(stone['stone_rate']*stone['stone_pieces'])
                                                stone['total_stone_value']=total_stone_value

                                            billing_stone_serializer=BillingStoneDetailsSerializer(billing_stone_queryset,data=stone,partial=True)
                                            if billing_stone_serializer.is_valid():
                                                billing_stone_serializer.save()
                                            else:
                                                raise Exception (billing_stone_serializer.errors)
                                            
                                        except BillingParticularStoneDetails.DoesNotExist:

                                            stone['billing_details'] = serializer.data['id']
                                            stone['billing_item_details'] = billing_taggeditem_serializer.data['id']
                                            stone['stone']=float(stone['stone_name'])
                                            stone['stone_pieces']=float(stone['stone_pieces'])
                                            stone['stone_weight']=float(stone['stone_weight'])
                                            stone['stone_weight_type']=int(stone['stone_weight_type'])
                                            stone['stone_amount']=float(stone['stone_rate'])
                                            stone['stone_rate_type']=int(stone['stone_rate_type'])
                                            stone['reduce_weight']=stone['include_stone_weight']

                                            if int(stone['stone_weight_type']) == int(settings.CARAT):
                                                stone['stone_weight']=(float(stone['stone_weight'])/5)

                                            if int(stone['stone_rate_type']) == int(settings.PERGRAM):
                                                total_stone_value=float(stone['stone_rate']*stone['stone_weight'])
                                                stone['total_stone_value']=total_stone_value
                                            
                                            if int(stone['stone_rate_type']) == int(settings.PERCARAT):
                                                stone_rate = float(stone['stone_rate'])*5
                                                stone['stone_rate'] = stone_rate
                                                total_stone_value=float(stone['stone_rate']*stone['stone_weight'])
                                                stone['total_stone_value']=total_stone_value

                                            if int(stone['stone_rate_type']) == int(settings.PERPIECE):
                                                total_stone_value=float(stone['stone_rate']*stone['stone_pieces'])
                                                stone['total_stone_value']=total_stone_value

                                            billing_stone_serializer=BillingStoneDetailsSerializer(data=stone)
                                            if billing_stone_serializer.is_valid():
                                                billing_stone_serializer.save()
                                            else:
                                                raise Exception (billing_stone_serializer.errors)
                                            
                                        except Exception as err:
                                            raise Exception(err)

                                    diamond_details=item.get('diamond_details') if item.get('diamond_details') else []

                                    for diamond in diamond_details :
                                        try:

                                            diamond_id = diamond.get('id') if diamond.get('id') != None else 0
                                            billing_diamond_queryset = BillingParticularsDiamondDetails.objects.get(id=diamond_id)

                                            diamond['billing_details'] = serializer.data['id']
                                            diamond['billing_item_details'] = billing_taggeditem_serializer.data['id']
                                            diamond['diamond'] = float(diamond['diamond_name'])
                                            diamond['diamond_pieces'] = float(diamond['diamond_pieces'])
                                            diamond['diamond_weight'] = float(diamond['diamond_weight'])
                                            diamond['diamond_weight_type'] = int(diamond['diamond_weight_type'])
                                            diamond['diamond_amount'] = float(diamond['diamond_rate'])
                                            diamond['diamond_rate_type'] = int(diamond['diamond_rate_type'])
                                            diamond['reduce_weight'] = diamond['include_diamond_weight']

                                            if int(diamond['diamond_weight_type']) == settings.CARAT :
                                                diamond_weight=float(diamond['diamond_weight'])/5
                                                diamond['diamond_weight']=diamond_weight


                                            if int(diamond['diamond_rate_type']) ==settings.PERGRAM:
                                                total_diamond_value=float(diamond['diamond_rate']*diamond['diamond_weight'])
                                                diamond['total_diamond_value'] = total_diamond_value

                                            if int(diamond['diamond_rate_type']) == settings.PERCARAT:
                                                diamond_rate=float(diamond['diamond_rate'])*5
                                                diamond['diamond_rate']=diamond_rate
                                                total_diamond_value=float(diamond['diamond_rate']*diamond['diamond_weight'])
                                                diamond['total_diamond_value'] = total_diamond_value

                                            if int(diamond['diamond_rate_type']) ==settings.PERPIECE:
                                                total_diamond_value=float(diamond['diamond_rate']*diamond['diamond_pieces'])
                                                diamond['total_diamond_value'] = total_diamond_value

                                            billing_diamond_serializer=BillingDiamondDetailsSerializer(billing_diamond_queryset,data=diamond,partial=True)
                                            if billing_diamond_serializer.is_valid():
                                                billing_diamond_serializer.save()
                                            else:
                                                raise Exception(billing_diamond_serializer.errors)
                                            
                                        except BillingParticularsDiamondDetails.DoesNotExist:

                                            diamond['billing_details'] = serializer.data['id']
                                            diamond['billing_item_details'] = billing_taggeditem_serializer.data['id']
                                            diamond['diamond'] = float(diamond['diamond_name'])
                                            diamond['diamond_pieces'] = float(diamond['diamond_pieces'])
                                            diamond['diamond_weight'] = float(diamond['diamond_weight'])
                                            diamond['diamond_weight_type'] = int(diamond['diamond_weight_type'])
                                            diamond['diamond_amount'] = float(diamond['diamond_rate'])
                                            diamond['diamond_rate_type'] = int(diamond['diamond_rate_type'])
                                            diamond['reduce_weight'] = diamond['include_diamond_weight']

                                            if int(diamond['diamond_weight_type']) == settings.CARAT :
                                                diamond_weight=float(diamond['diamond_weight'])/5
                                                diamond['diamond_weight']=diamond_weight

                                            if int(diamond['diamond_rate_type']) ==settings.PERGRAM:
                                                total_diamond_value=float(diamond['diamond_rate']*diamond['diamond_weight'])
                                                diamond['total_diamond_value'] = total_diamond_value

                                            if int(diamond['diamond_rate_type']) == settings.PERCARAT:
                                                diamond_rate=float(diamond['diamond_rate'])*5
                                                diamond['diamond_rate']=diamond_rate
                                                total_diamond_value=float(diamond['diamond_rate']*diamond['diamond_weight'])
                                                diamond['total_diamond_value'] = total_diamond_value

                                            if int(diamond['diamond_rate_type']) ==settings.PERPIECE:
                                                total_diamond_value=float(diamond['diamond_rate']*diamond['diamond_pieces'])
                                                diamond['total_diamond_value'] = total_diamond_value

                                            billing_diamond_serializer=BillingDiamondDetailsSerializer(data=diamond)
                                            if billing_diamond_serializer.is_valid():
                                                billing_diamond_serializer.save()
                                            else:
                                                raise Exception(billing_diamond_serializer.errors)
                                        except Exception as err:
                                            raise Exception(err)
                                else:
                                    raise Exception(billing_taggeditem_serializer.errors)
                                
                            except BillingParticularDetails.DoesNotExist:
                                tag_number=item.get('tag_number')

                                tag_queryset=TaggedItems.objects.get(tag_number=tag_number)
                                billing_tag_data = {
                                    'billing_details': serializer.data['id'],
                                    'billing_tag_item': tag_queryset.pk,
                                    'tag_number': item.get('tag_number'),
                                    'item_details': item.get('item_details'),
                                    'sub_item_details': item.get('sub_item_details'),
                                    'metal': item.get('metal'),
                                    'net_weight': item.get('net_weight'),
                                    'gross_weight' : item.get('gross_weight'),
                                    'tag_weight' : item.get('tag_weight'),
                                    'cover_weight' : item.get('cover_weight'),
                                    'loop_weight' : item.get('loop_weight'),
                                    'other_weight' : item.get('other_weight'),
                                    'pieces' : item.get('pieces'),
                                    'total_pieces' : item.get('total_pieces'),
                                    'rate' : item.get('metal_rate'),
                                    'stone_rate' : item.get('stone_rate'),
                                    'diamond_rate' : item.get('diamond_rate'),
                                    'stock_type' : item.get('stock_type'),
                                    'calculation_type' : item.get('calculation_type'),
                                    'tax_percent' : item.get('tax_percent'),
                                    'additional_charges' : item.get('additional_charges'),
                                    'total_stone_weight' : item.get('total_stone_weight'),
                                    'total_diamond_weight' : item.get('total_diamond_weight'),
                                    'per_gram_weight_type' : item.get('per_gram_weight_type',None),
                                    'wastage_percentage' : item.get('wastage_percent', None),
                                    'flat_wastage' : item.get('flat_wastage', None),
                                    'making_charge' : item.get('making_charge', None),
                                    'flat_making_charge' : item.get('flat_making_charge', None),
                                    'wastage_calculation_type': item.get('wastage_calculation_type', None),
                                    'making_charge_calculation_type': item.get('making_charge_calculation_type', None),
                                    'gst' : item.get('gst'),
                                    'total_rate' : item.get('with_gst_rate'),
                                    'without_gst_rate':item.get('rate'),
                                    'huid_rate':item.get('item_huid_rate'),
                                    'employee_id':item.get('employee_id')
                                }
                                
                                billing_taggeditem_serializer = BillingParticularDetailsSerializer(data=billing_tag_data)
                                if billing_taggeditem_serializer.is_valid():
                                    billing_taggeditem_serializer.save()

                                    stone_details=item.get('stone_details') if item.get('stone_details') else []

                                    for stone in stone_details:
                                        stone['billing_details'] = serializer.data['id']
                                        stone['billing_item_details'] = billing_taggeditem_serializer.data['id']
                                        stone['stone_name']=float(stone['stone_name'])
                                        stone['stone_pieces']=float(stone['stone_pieces'])
                                        stone['stone_weight']=float(stone['stone_weight'])
                                        stone['stone_weight_type']=int(stone['stone_weight_type'])
                                        stone['stone_rate']=float(stone['stone_rate'])
                                        stone['stone_rate_type']=int(stone['stone_rate_type'])
                                        stone['include_stone_weight']=stone['include_stone_weight']

                                        if int(stone['stone_weight_type']) == int(settings.CARAT):
                                            stone['stone_weight']=(float(stone['stone_weight'])/5)

                                        if int(stone['stone_rate_type']) == int(settings.PERGRAM):
                                            total_stone_value=float(stone['stone_rate']*stone['stone_weight'])
                                            stone['total_stone_value']=total_stone_value
                                        
                                        if int(stone['stone_rate_type']) == int(settings.PERCARAT):
                                            stone_rate = float(stone['stone_rate'])*5
                                            stone['stone_rate'] = stone_rate
                                            total_stone_value=float(stone['stone_rate']*stone['stone_weight'])
                                            stone['total_stone_value']=total_stone_value

                                        if int(stone['stone_rate_type']) == int(settings.PERPIECE):
                                            total_stone_value=float(stone['stone_rate']*stone['stone_pieces'])
                                            stone['total_stone_value']=total_stone_value

                                        billing_stone_serializer=BillingStoneDetailsSerializer(data=stone)
                                        if billing_stone_serializer.is_valid():
                                            billing_stone_serializer.save()
                                        else:
                                            raise Exception (billing_stone_serializer.errors)

                                    diamond_details=item.get('diamond_details') if item.get('diamond_details') else []

                                    for diamond in diamond_details :

                                        diamond['billing_details'] = serializer.data['id']
                                        diamond['billing_item_details'] = billing_taggeditem_serializer.data['id']
                                        diamond['diamond_name'] = float(diamond['diamond_name'])
                                        diamond['diamond_pieces'] = float(diamond['diamond_pieces'])
                                        diamond['diamond_weight'] = float(diamond['diamond_weight'])
                                        diamond['diamond_weight_type'] = int(diamond['diamond_weight_type'])
                                        diamond['diamond_rate'] = float(diamond['diamond_rate'])
                                        diamond['diamond_rate_type'] = int(diamond['diamond_rate_type'])
                                        diamond['include_diamond_weight'] = diamond['include_diamond_weight']

                                        if int(diamond['diamond_weight_type']) == settings.CARAT :
                                            diamond_weight=float(diamond['diamond_weight'])/5
                                            diamond['diamond_weight']=diamond_weight


                                        if int(diamond['diamond_rate_type']) ==settings.PERGRAM:
                                            total_diamond_value=float(diamond['diamond_rate']*diamond['diamond_weight'])
                                            diamond['total_diamond_value'] = total_diamond_value

                                        if int(diamond['diamond_rate_type']) == settings.PERCARAT:
                                            diamond_rate=float(diamond['diamond_rate'])*5
                                            diamond['diamond_rate']=diamond_rate
                                            total_diamond_value=float(diamond['diamond_rate']*diamond['diamond_weight'])
                                            diamond['total_diamond_value'] = total_diamond_value

                                        if int(diamond['diamond_rate_type']) ==settings.PERPIECE:
                                            total_diamond_value=float(diamond['diamond_rate']*diamond['diamond_pieces'])
                                            diamond['total_diamond_value'] = total_diamond_value

                                        billing_diamond_serializer=BillingDiamondDetailsSerializer(data=diamond)
                                        if billing_diamond_serializer.is_valid():
                                            billing_diamond_serializer.save()
                                        else:
                                            raise Exception(billing_diamond_serializer.errors)
                                else:
                                    raise Exception(billing_taggeditem_serializer.errors)
                            except Exception as err:
                                raise Exception(err)
                            
                    return Response(
                        {
                            "data":serializer.data,
                            "message":res_msg.update("Biling"),
                            "status":status.HTTP_200_OK
                        },status=status.HTTP_200_OK)
                
                else:
                    raise Exception(serializer.errors)
        
            except Exception as err:
                transaction.set_rollback(True)
                return Response(
                    {
                        "data":str(err),
                        "message":res_msg.something_else(),
                        "status":status.HTTP_204_NO_CONTENT
                    },status=status.HTTP_200_OK
                )
        else:
            return Response(
                    {
                        "message":res_msg.not_exists('Billing Details'),
                        "status":status.HTTP_204_NO_CONTENT
                    },status=status.HTTP_200_OK
                )
        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class BillTypeList(APIView):
    
    def get(self,request):

        queryset = list(BillingType.objects.all().values('id','bill_type').order_by('id'))

        return Response(
            {
                "data":{
                    "list":queryset
                },
                "message":res_msg.retrieve('Bill Type'),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class SilverBillnumberView(APIView):  
    def get(self, request):  
        try:
            queryset=SilverBillID.objects.all().order_by('-id')[0]
            prefix = 'BILLSV-00'
            new_bill_id=f'{prefix}{int(queryset.pk)+1}'
            return Response(
                {
                    "bill_number":new_bill_id,
                    "message":res_msg.retrieve("Bill Number"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        
        except Exception as err:
            return Response(
                {
                    "bill_number":"BILLSV-001",
                    "message":res_msg.retrieve("Bill Number"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
          


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class GoldEstimationnumberView(APIView):  
    def get(self, request):  
        try:
            queryset=GoldEstimationID.objects.all().order_by('-id')[0]
            prefix = 'ESTGD-00'
            new_estimation_id=f'{prefix}{int(queryset.pk)+1}'
            return Response(
                {
                    "estimation_number":new_estimation_id,
                    "message":res_msg.retrieve("Estimation Number"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        
        except Exception as err:
            return Response(
                {
                    "estimation_number":"ESTGD-001",
                    "message":res_msg.retrieve("Estimation Number"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class SilverEstimationnumberView(APIView):  
    def get(self, request):  
        try:
            queryset=SilverEstimationID.objects.all().order_by('-id')[0]
            prefix = 'ESTSV-00'
            new_estimation_id=f'{prefix}{int(queryset.pk)+1}'
            return Response(
                {
                    "estimation_number":new_estimation_id,
                    "message":res_msg.retrieve("Estimation Number"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        
        except Exception as err:
            return Response(
                {
                    "estimation_number":"ESTSV-001",
                    "message":res_msg.retrieve("Estimation Number"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )

        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class GenerateMiscIssueId(APIView):

    def get(self, request):

        res_data = {}
        try:
            ses_misc_queryset = SessionMiscIssueId.objects.get(user=request.user.id)
            res_data['misc_issue_id'] = ses_misc_queryset.ses_misc_issue_id.misc_issue_id

        except SessionMiscIssueId.DoesNotExist:
            data = {
                'misc_issue_id': None,
                'created_at': timezone.now(),
                'created_by': request.user.id
            }    

            misc_issue_id_serializer = MiscIssueIdSerializer(data=data)

            if misc_issue_id_serializer.is_valid():
                misc_issue_id_serializer.save()

                update_data = {
                    'misc_issue_id': 'MISC-'+(str(misc_issue_id_serializer.data.get('id')).zfill(4)),
                }

                get_misc_issue_id_queryset = MiscIssueId.objects.get(id=misc_issue_id_serializer.data.get('id'))

                update_misc_issue_id_serializer = MiscIssueIdSerializer(get_misc_issue_id_queryset, data=update_data, partial=True)

                if update_misc_issue_id_serializer.is_valid():
                    update_misc_issue_id_serializer.save()

                    ses_data = {
                        'ses_misc_issue_id': misc_issue_id_serializer.data.get('id'),
                        'user': request.user.id
                    }

                    ses_misc_issue_id_serializer = SessionMiscIssueIdSerializer(data=ses_data)

                    if ses_misc_issue_id_serializer.is_valid():
                        ses_misc_issue_id_serializer.save()

                        res_data['misc_issue_id'] = update_misc_issue_id_serializer.data.get('misc_issue_id')
                    else:
                        return Response({
                            "data": ses_misc_issue_id_serializer.errors,
                            "message": res_msg.in_valid_fields(),
                            "status": status.HTTP_200_OK
                        }, status=status.HTTP_200_OK)
                    
            else:
                return Response({
                    "data": misc_issue_id_serializer.errors,
                    "message": res_msg.in_valid_fields(),
                    "status": status.HTTP_200_OK
                }, status=status.HTTP_200_OK)       
        except Exception as err:
            return Response({
                "data": str(err),
                "message": res_msg.something_else(),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        
        return Response({
            "data": res_data,
            "message": res_msg.retrieve('Misc issue Id'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)        


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class CreateMiscBillingView(APIView):

    @transaction.atomic
    def post(self, request):

        data = request.data

        try:
            with transaction.atomic():
                ses_misc_queryset = SessionMiscIssueId.objects.get(user=request.user.id)

                branch = data.get('branch', None) if data.get('branch') else request.user.branch.id

                misc_details_data = {
                    "misc_issue_id": ses_misc_queryset.ses_misc_issue_id.pk,
                    "issue_date": data.get('issue_date'),
                    "branch": branch,
                    "customer": data.get('customer'),
                    "giver_name": data.get('giver_name'),
                    "remarks": data.get('remarks'),
                    "total_gross_weight": data.get('gross_weight'),
                    "total_net_weight": data.get('net_weight'),
                    "total_pieces": data.get('pieces'),
                    "total_amount": data.get('total_amount'),
                    "created_at": timezone.now(),
                    "created_by": request.user.id
                }

                misc_details_serializer = MiscIssueDetailsSerializer(data=misc_details_data)

                if misc_details_serializer.is_valid():
                    misc_details_serializer.save()

                    for i in data.get('particulars', []):
                        try:
                            tag_details_queryset = TaggedItems.objects.get(tag_number=i.get('tag_no'))


                            item_data = {
                                "misc_issue_details": misc_details_serializer.data.get('id'),
                                "tag_number": tag_details_queryset.pk,
                                "metal_rate": i.get('rate'),
                                "amount": i.get('total_amount'),
                                "pieces": i.get('pieces')
                            }

                            misc_items_serializer = MiscParticularsSerializer(data=item_data)

                            if misc_items_serializer.is_valid():
                                misc_items_serializer.save()
                                
                                
                                if tag_details_queryset.sub_item_details.stock_type.pk == int(settings.PACKET):
                                    if (tag_details_queryset.remaining_pieces - int(i.get('pieces',0))) <= 0:
                                        tag_details_queryset.is_billed = True
                                    else:
                                        tag_details_queryset.is_billed = False

                                    tag_details_queryset.remaining_pieces = tag_details_queryset.remaining_pieces - int(i.get('pieces',0))
                                else:
                                    tag_details_queryset.is_billed = True
                                tag_details_queryset.save()
                            else:
                                transaction.set_rollback(True)
                                return Response({
                                    "data": misc_items_serializer.errors,
                                    "message": res_msg.retrieve('Misc Issue'),
                                    "status": status.HTTP_200_OK
                                }, status=status.HTTP_200_OK)  
                        except Exception as err:
                            transaction.set_rollback(True)
                            return Response({
                                "message": "Something wrong to adding the item details",
                                "status": status.HTTP_204_NO_CONTENT
                            }, status=status.HTTP_200_OK)

                    ses_misc_queryset.delete()
                    return Response({
                        "data": misc_details_serializer.data,
                        "message": res_msg.create('Misc Issue'),
                        "status": status.HTTP_200_OK
                    }, status=status.HTTP_200_OK)  
                else:
                    return Response({
                        "data": misc_details_serializer.errors,
                        "message": res_msg.retrieve('Misc Issue'),
                        "status": status.HTTP_200_OK
                    }, status=status.HTTP_200_OK)  
        except:
            return Response({
                "message": "Something wrong in given Misc id",
                "status": status.HTTP_204_NO_CONTENT
            }, status=status.HTTP_200_OK)
        
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class MetalEstimationListView(APIView):
    def post(self,request):

        request_data = request.data
        
        try:
            if request.user.role.is_admin == True:
                branch = int(request_data.get('branch'))
            else:
                branch = int(request.user.branch.pk)

            bill_type = request_data.get('bill_type')
                
            queryset = list(EstimateDetails.objects.filter(bill_type=bill_type,branch=branch).values('id','estimate_no').order_by('-id'))

            return Response(
                {
                    "data":{
                        'list':queryset
                    },
                    "message":res_msg.retrieve("Estimation Details"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        except EstimateDetails.DoesNotExist:
            
            return Response(
                {
                    "message":res_msg.not_exists("Estimation Details"),
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


class TestView(APIView):
    def get(self,request):

        try:
            # Make HTTP request to trigger frontend function
            response = requests.get('http://192.168.1.209:3000/trigger-function/',timeout=10)
            
            # Handle response if necessary
            return Response(response)
        except Exception as err:
            return Response(str(err))


# TAG DETAILS API VIEW
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class TagItemListView(APIView):
    def post(self,request):
        request_data = request.data
        item_details = request_data.get('item_details')
        from_weight = request_data.get('from_weight')
        to_weight = request_data.get("to_weight")
        try:
            
            queryset = list(TaggedItems.objects.filter(item_details=item_details,gross_weight__range=(from_weight,to_weight)).values('id','tag_number','gross_weight','item_details','item_details__item_details__item_name','sub_item_details','sub_item_details__sub_item_name').order_by('-id'))
           
            res_data = []
            for item in queryset:
                dict_data = item
                dict_data['item_name'] = item['item_details__item_details__item_name']
                dict_data['sub_item_name'] = item['sub_item_details__sub_item_name']

                res_data.append(dict_data)
            return Response(
                {
                    "data":{
                        'list':res_data
                    },
                    "message":res_msg.retrieve("Tag Item Details"),
                    "status":status.HTTP_200_OK
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
        

# STAFF ID CHECK API 
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class StaffIdCheckAPIView(APIView):
    def get(self,request,staff_id=None):
        if staff_id != None:
            try:
                queryset = Staff.objects.get(staff_id=staff_id)
                serializer = StaffSerializer(queryset)
                return Response(
                {
                    "data": serializer.data,
                    "message" : res_msg.retrieve("Staff Details"),
                    "status": status.HTTP_200_OK
                }, status=status.HTTP_200_OK
            )
            except Staff.DoesNotExist:
                return Response(
                {
                    "message" : res_msg.not_exists("Staff Details"),
                    "status": status.HTTP_404_NOT_FOUND
                }, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    "message" : "Invalid Staff ID",
                    "status": status.HTTP_204_NO_CONTENT
                }, status=status.HTTP_200_OK
            )
        


# ESTIMATION ITEM LIST SHOW API
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class EstimationItemListAPIView(APIView):
    def post(self,request):
        data = request.data
        try:
            estimation_details = data.get('estimation_details',[])
            res_data = []
            
            for item in estimation_details:
                queryset = EstimationTagItems.objects.filter(estimation_details=item)
                serializer = EstimationTagItemsSerializer(queryset,many=True)

                for i in range(0, len(serializer.data)):
                    dict_data = serializer.data[i]
                    dict_data['purity'] = queryset[i].item_details.purity.purity_name
                    dict_data['item_name'] = queryset[i].item_details.item_name
                    dict_data['sub_item_name'] = queryset[i].sub_item_details.sub_item_name
                    dict_data['employee_name'] = queryset[i].employee_id.staff_id

                    res_data.append(dict_data)

            return Response(
            {
                "data": res_data,
                "message" : res_msg.retrieve("Tag Item List"),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK
            )
        except Exception as err:
            return Response(
            {
                "data" : err,
                "message" : res_msg.not_exists("Estimation"),
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_200_OK
        )


# ESTIMATION ITEM LIST SHOW API
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class GetEstimationListByCustomerView(APIView):
    def get(self,request,pk):

        res_data = []
        try:
            queryset = EstimateDetails.objects.filter(customer_details=pk)
            serializer = EstimateDetailsSerializer(queryset,many=True)

            for i in range(0, len(serializer.data)):
                dict_data = serializer.data[i]

                res_data.append(dict_data)

            return Response(
            {
                "data": res_data,
                "message" : res_msg.retrieve("Estimation List"),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK
            )
        except Exception as err:
            return Response(
            {
                "message" : res_msg.not_exists("Estimation"),
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_200_OK
        )


##### ESTIMATION MULTIPLE SELECT DETAILS RETRIEVE API ####
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class EstimationMultiSelectAPIView(APIView):
    def post(self,request):
        estimation_details = {}
        res_data = []
        estimation_ids = request.data.get('estimation_details',[])
        gst_type = request.data.get('gst_type')
        customer_details = []
        try:
            # customer_details = []
            # try:
            #     customer_queryset = Customer.objects.get(id=request.data.get('customer_details'),is_active=True)
            #     customer_serializer = CustomerSerializer(customer_queryset)
            #     customer_details = customer_serializer.data
            # except Exception as err:
            #     return Response(
            #         {
            #             "message" : res_msg.not_exists('Customer'),
            #             "status": status.HTTP_204_NO_CONTENT
            #         }, status=status.HTTP_200_OK
            #     )

            estimation_data = []
            
            old_gold_details=[]
            estimation_return_details = []
            
            for estimation_id in estimation_ids:
                
                queryset = EstimateDetails.objects.get(id=estimation_id)
                
                # estimation_billing_quryset = BillingEstimationDetails.objects.filter(estimation_details__in = estimation_id)
                # if len(estimation_billing_quryset) == 0:
                serializer = EstimateDetailsSerializer(queryset)
                estimation_data.append(serializer.data)
                
                estimate_tag_item_queryset = EstimationTagItems.objects.filter(estimation_details=estimation_id)
                particulars = []
                for item in estimate_tag_item_queryset:
                    tag_details={
                        'id':item.pk,
                        'diamond_rate':item.diamond_rate,
                        'flat_making_charge':item.flat_making_charge,
                        'flat_wastage':item.flat_wastage,
                        'gross_weight':item.gross_weight,
                        'gst':item.gst,
                        'item_details':item.item_details.pk,
                        'item':item.item_details.item_name,
                        'jewel_type':item.metal.metal_name,
                        'making_charge':item.making_charge,
                        'metal':item.metal.pk,
                        'metal_rate':item.rate,
                        'net_weight':item.net_weight,
                        'pieces':item.pieces,
                        'rate':item.total_amount,
                        'stock_type':item.stock_type.pk,
                        'stock_type_name':item.stock_type.stock_type_name,
                        'calculation_type':item.calculation_type.pk,
                        'calculation_type_name':item.calculation_type.calculation_name,
                        'stone_rate':item.stone_rate,
                        'sub_item_details':item.sub_item_details.pk,
                        'sub_item_name':item.sub_item_details.sub_item_name,
                        'tag_item_id':item.estimation_tag_item.pk,
                        'tag_number':item.estimation_tag_item.tag_number,
                        'gst_percent':item.gst_percent,
                        'total_diamond_weight':item.total_diamond_weight,
                        'total_pieces':item.total_pieces,
                        'total_stone_weight':item.total_stone_weight,
                        'wastage_percent':item.wastage_percentage,
                        "item_huid_rate":item.huid_rate,
                        "with_gst_rate":item.with_gst_total_rate,
                        "employee_id":item.employee_id.pk,
                        "employee_name":item.employee_id.staff_id,
                    }
                    
                    if str(item.calculation_type.pk) == settings.FIXEDRATE:
                        tag_details['min_fixed_rate'] = item.estimation_tag_item.min_fixed_rate
                        tag_details['max_fixed_rate'] = item.estimation_tag_item.max_fixed_rate

                        tag_details['min_sale_value']=(item.estimation_tag_item.min_fixed_rate + item.estimation_tag_item.stone_rate + item.estimation_tag_item.diamond_rate)
                        tag_details['max_sale_value']=(item.estimation_tag_item.max_fixed_rate + item.estimation_tag_item.stone_rate + item.estimation_tag_item.diamond_rate)

                        tag_details['rate'] = tag_details['max_sale_value'] + item.estimation_tag_item.item_details.item_details.huid_rate

                    elif str(item.calculation_type.pk) == settings.WEIGHTCALCULATION:

                        subitem_weight_queryset=SubItemWeightCalculation.objects.get(sub_item_details=item.estimation_tag_item.sub_item_details.pk)
                        try:
                            metal_rate_queryset = MetalRate.objects.filter(purity=item.estimation_tag_item.sub_item_details.purity.pk).order_by('-id')[0]
                            metal_rate = metal_rate_queryset.rate
                        except Exception as err:
                            metal_rate=0
                    
                        metal_value=(float(metal_rate)*float(item.estimation_tag_item.net_weight))

                        subitem_weight_queryset=SubItemWeightCalculation.objects.get(sub_item_details=item.estimation_tag_item.sub_item_details.pk)

                        if str(subitem_weight_queryset.wastage_calculation.pk) == settings.GROSSWEIGHT :

                            min_wastage_value=((item.estimation_tag_item.gross_weight*item.estimation_tag_item.min_wastage_percent)/100)*metal_rate

                        else:

                            min_wastage_value=((item.estimation_tag_item.net_weight*item.estimation_tag_item.min_wastage_percent)/100)*metal_rate

                        min_flat_wastage=item.estimation_tag_item.min_flat_wastage

                        if str(subitem_weight_queryset.making_charge_calculation.pk) == settings.GROSSWEIGHT :

                            min_making_Charge=(item.estimation_tag_item.min_making_charge_gram*item.estimation_tag_item.gross_weight)

                        else:

                            min_making_Charge=(item.estimation_tag_item.min_making_charge_gram*item.estimation_tag_item.net_weight)


                        min_flat_making_charge=item.estimation_tag_item.min_flat_making_charge

                        min_sale_value = metal_value + min_wastage_value + min_flat_wastage + min_making_Charge + min_flat_making_charge + item.estimation_tag_item.stone_rate + item.estimation_tag_item.diamond_rate

                        #max sale value calculation

                        if str(subitem_weight_queryset.wastage_calculation.pk) == settings.GROSSWEIGHT :

                            max_wastage_value=((item.estimation_tag_item.gross_weight * item.estimation_tag_item.max_wastage_percent)/100)*metal_rate

                        else:

                            max_wastage_value=((item.estimation_tag_item.net_weight * item.estimation_tag_item.max_wastage_percent)/100)*metal_rate


                        max_flat_wastage=item.estimation_tag_item.max_flat_wastage

                        if str(subitem_weight_queryset.making_charge_calculation.pk) == settings.GROSSWEIGHT :

                            max_making_Charge=(item.estimation_tag_item.max_making_charge_gram * item.estimation_tag_item.gross_weight)
                        
                        else:

                            max_making_Charge=(item.estimation_tag_item.max_making_charge_gram * item.estimation_tag_item.net_weight)

                        
                        max_flat_making_charge = item.estimation_tag_item.max_flat_making_charge
                        
                        max_sale_value = metal_value + max_wastage_value + max_flat_wastage + max_making_Charge + max_flat_making_charge + item.estimation_tag_item.stone_rate + item.estimation_tag_item.diamond_rate
                        
                        tag_details['metal_rate'] = metal_rate
                        tag_details['wastage_calculation_type'] = subitem_weight_queryset.wastage_calculation.pk
                        tag_details['wastage_calculation_name'] = subitem_weight_queryset.wastage_calculation.weight_name
                        tag_details['making_charge_calculation_type'] = subitem_weight_queryset.making_charge_calculation.pk
                        tag_details['making_charge_calculation_name'] = subitem_weight_queryset.making_charge_calculation.weight_name

                        tag_details['min_wastage_percent'] = item.estimation_tag_item.min_wastage_percent
                        tag_details['min_wastage_percent'] = item.estimation_tag_item.min_wastage_percent
                        tag_details['min_flat_wastage'] = item.estimation_tag_item.min_flat_wastage
                        tag_details['max_wastage_percent'] = item.estimation_tag_item.max_wastage_percent
                        tag_details['max_flat_wastage'] = item.estimation_tag_item.max_flat_wastage
                        tag_details['min_making_charge'] = item.estimation_tag_item.min_making_charge_gram
                        tag_details['min_flat_making_charge'] = item.estimation_tag_item.min_flat_making_charge
                        tag_details['max_making_charge'] = item.estimation_tag_item.max_making_charge_gram
                        tag_details['max_flat_making_charge'] = item.estimation_tag_item.max_flat_making_charge

                        tag_details['min_sale_value']=min_sale_value
                        tag_details['max_sale_value']=max_sale_value

                        tag_details['rate'] = tag_details['max_sale_value'] + item.estimation_tag_item.item_details.item_details.huid_rate

                    elif str(item.calculation_type.pk) == settings.PERGRAMRATE:
                        tag_details['min_metal_rate'] = item.estimation_tag_item.min_pergram_rate
                        tag_details['max_metal_rate'] = item.estimation_tag_item.max_pergram_rate
                        tag_details['per_gram_weight_type'] = item.estimation_tag_item.per_gram_weight_type.pk
                        tag_details['per_gram_weight_type_name'] = item.estimation_tag_item.per_gram_weight_type.weight_name

                        if str(item.estimation_tag_item.per_gram_weight_type.pk) == settings.GROSSWEIGHT :
                            min_per_gram_value=float(item.estimation_tag_item.gross_weight) * float(item.estimation_tag_item.min_pergram_rate)
                            max_per_gram_value=float(item.estimation_tag_item.gross_weight) * float(item.estimation_tag_item.max_pergram_rate)
                        else:
                            min_per_gram_value=float(item.estimation_tag_item.net_weight) * float(item.estimation_tag_item.min_pergram_rate)
                            max_per_gram_value=float(item.estimation_tag_item.net_weight) * float(item.estimation_tag_item.max_pergram_rate)

                        tag_details['min_sale_value']=(min_per_gram_value + item.estimation_tag_item.stone_rate + item.estimation_tag_item.diamond_rate)
                        tag_details['max_sale_value']=(max_per_gram_value + item.estimation_tag_item.stone_rate + item.estimation_tag_item.diamond_rate)

                        tag_details['rate'] = tag_details['max_sale_value'] + item.estimation_tag_item.item_details.item_details.huid_rate

                    elif str(item.calculation_type.pk) == settings.PERPIECERATE:
                        
                        tag_details['min_per_piece_rate'] = item.estimation_tag_item.min_per_piece_rate
                        tag_details['per_piece_rate'] = item.estimation_tag_item.per_piece_rate

                        tag_details['min_per_piece_rate']=item.estimation_tag_item.min_per_piece_rate  
                        tag_details['max_per_piece_rate']=item.estimation_tag_item.max_per_piece_rate  
                        min_rate =  item.estimation_tag_item.tag_pieces * item.estimation_tag_item.min_per_piece_rate
                        max_rate =  item.estimation_tag_item.tag_pieces * item.estimation_tag_item.max_per_piece_rate
                        tag_details['min_sale_value']=(min_rate + item.estimation_tag_item.stone_rate + item.estimation_tag_item.diamond_rate)
                        tag_details['max_sale_value']=(max_rate + item.estimation_tag_item.stone_rate + item.estimation_tag_item.diamond_rate)  

                        tag_details['rate'] = tag_details['max_sale_value'] + item.estimation_tag_item.item_details.item_details.huid_rate

                    try:
                        tax_queryset = TaxDetailsAudit.objects.filter(metal=item.estimation_tag_item.item_details.item_details.metal.pk).order_by('-id').first()

                        if tax_queryset:
                            tax_percent_queryset = SalesTaxDetails.objects.get(tax_details=tax_queryset.tax_details)

                            if int(gst_type) == settings.INTRA_STATE_GST:
                                tag_details['gst'] = (((tax_percent_queryset.sales_tax_cgst + tax_percent_queryset.sales_tax_sgst + tax_percent_queryset.sales_surcharge_percent)/100) * tag_details['rate']) + tax_percent_queryset.sales_additional_charges
                                tag_details['sales_tax_cgst']=tax_percent_queryset.sales_tax_cgst
                                tag_details['sales_tax_sgst']=tax_percent_queryset.sales_tax_sgst

                            elif int(gst_type) == settings.INTER_STATE_GST:
                                tag_details['gst'] = (((tax_percent_queryset.sales_tax_igst + tax_percent_queryset.sales_surcharge_percent)/100) * tag_details['rate']) + tax_percent_queryset.sales_additional_charges
                                tag_details['sales_tax_igst']=tax_percent_queryset.sales_tax_igst
                    except Exception as err:
                        tag_details['gst'] = 0
                        tag_details['sales_tax_igst']=0
                        tag_details['sales_tax_cgst']=0
                        tag_details['sales_tax_sgst']=0
                        tag_details['sales_surcharge_percent']=0
                        tag_details['sales_additional_charges'] = 0
                    
                    stone_queryset=EstimationStoneDetails.objects.filter(estimation_details=estimation_id,estimation_item_details=item.pk)
                    stone_details=[]
                    
                    for stone in stone_queryset:
                        stone_data={
                            'id' : stone.pk,
                            'stone_name':stone.stone_name.pk,
                            'stone_pieces':stone.stone_pieces,
                            'stone_weight':stone.stone_weight,
                            'stone_weight_type':stone.stone_weight_type.pk,
                            'stone_weight_type_name':stone.stone_weight_type.weight_name,
                            'stone_rate':stone.stone_rate,
                            'stone_rate_type':stone.stone_rate_type.pk,
                            'stone_rate_type_name':stone.stone_rate_type.type_name,
                            'include_stone_weight':stone.include_stone_weight
                        }

                        if str(stone.stone_weight_type.pk) == settings.CARAT:
                            stone_data['stone_weight'] = float(stone.stone_weight)*5

                        else:
                            stone_data['stone_weight'] = float(stone.stone_weight)

                        if str(stone.stone_rate_type.pk) == settings.PERCARAT:
                            stone_data['stone_rate'] = float(stone.stone_rate)/5

                        elif str(stone.stone_rate_type.pk) == settings.PERPIECE:
                            stone_data['stone_rate'] = float(stone.stone_rate)
                        else:
                            stone_data['stone_rate'] = float(stone.stone_rate)

                        stone_details.append(stone_data)
                    tag_details['stone_details']=stone_details
                    
                    diamond_queryset=EstimationDiamondDetails.objects.filter(estimation_details=estimation_id,estimation_item_details=item.pk)
                    diamond_details=[]
                    for diamond in diamond_queryset:
                        diamond_data={
                            'id' : diamond.pk,
                            'diamond_name':diamond.diamond_name.pk,
                            'diamond_pieces':diamond.diamond_pieces,
                            'diamond_weight':diamond.diamond_weight,
                            'diamond_weight_type':diamond.diamond_weight_type.pk,
                            'diamond_weight_type_name':diamond.diamond_weight_type.weight_name,
                            'diamond_rate':diamond.diamond_rate,
                            'diamond_rate_type':diamond.diamond_rate_type.pk,
                            'diamond_rate_type_name':diamond.diamond_rate_type.type_name,
                            'include_diamond_weight':diamond.include_diamond_weight
                        }

                        if str(diamond.diamond_weight_type.pk) == settings.CARAT:
                            diamond_data['diamond_weight'] = float(diamond.diamond_weight)*5

                        else:
                            diamond_data['diamond_weight'] = float(diamond.diamond_weight)

                        if str(diamond.diamond_rate_type.pk) == settings.PERCARAT:
                            diamond_data['diamond_rate'] = float(diamond.diamond_rate)/5

                        else:
                            diamond_data['diamond_rate'] = float(diamond.diamond_rate)

                        diamond_details.append(diamond_data)

                    tag_details['diamond_details']=diamond_details
                    
                    particulars.append(tag_details)
                    
                old_gold_particulars = []
                old_gold_queryset = EstimationOldGold.objects.filter(estimation_details=estimation_id)
                
                if len(old_gold_queryset) != 0:
                    for old_gold in old_gold_queryset:
                        old_gold_details={
                            'id':old_gold.pk,
                            'old_gold_no':old_gold.old_gold_no,
                            'old_dust_weight':old_gold.old_dust_weight,
                            'old_gross_weight':old_gold.old_gross_weight,
                            'old_metal':old_gold.old_metal.pk,
                            'metal_name':old_gold.old_metal.metal_name,
                            'old_touch':old_gold.old_touch,
                            'old_net_weight':old_gold.old_net_weight,
                            'old_rate':old_gold.old_rate,
                            'old_amount':old_gold.old_amount,
                            'total_amount':old_gold.total_amount,
                            'employee_id':old_gold.employee_id.pk,
                            'employee_name':old_gold.employee_id.staff_id
                        }
                        old_gold_particulars.append(old_gold_details)
                        
                estimation_return_queryset = EstimationSaleReturnItems.objects.filter(estimation_details=estimation_id)
                
                if len(estimation_return_queryset) != 0:
                    for return_item in estimation_return_queryset:
                        return_details={
                            'id':return_item.pk,
                            'estimation_details': return_item.estimation_details.pk,
                            'bill_details' : return_item.bill_details.pk if return_item.bill_details is not None else None,
                            'return_items' : return_item.return_items.pk if return_item.return_items is not None else None,
                            'tag_number' : return_item.tag_number if return_item.tag_number is not None else None,
                            'item_details': return_item.item_details.pk,
                            'item_details_name': return_item.item_details.item_name,
                            'sub_item_details': return_item.sub_item_details.pk,
                            'sub_item_details_name': return_item.sub_item_details.sub_item_name,
                            'metal': return_item.metal.pk,
                            'metal_name': return_item.metal.metal_name,
                            'net_weight':return_item.net_weight,
                            'gross_weight':return_item.gross_weight,
                            'tag_weight':return_item.tag_weight,
                            'cover_weight':return_item.cover_weight,
                            'loop_weight':return_item.loop_weight,
                            'other_weight':return_item.other_weight,
                            'pieces':return_item.pieces,
                            'total_pieces':return_item.total_pieces,
                            'metal_rate' : return_item.rate,
                            'rate':return_item.without_gst_rate,
                            'stone_rate' : return_item.stone_rate,
                            'diamond_rate' : return_item.diamond_rate,
                            'stock_type' : return_item.stock_type.pk,
                            'calculation_type' : return_item.calculation_type.pk,
                            'tax_percent' : return_item.tax_percent,
                            'additional_charges' : return_item.additional_charges,
                            'total_stone_weight' : return_item.total_stone_weight,
                            'total_diamond_weight' : return_item.total_diamond_weight,
                            'per_gram_weight_type' : return_item.per_gram_weight_type.pk if return_item.per_gram_weight_type is not None else None,
                            'per_gram_weight_type_name' : return_item.per_gram_weight_type.weight_name if return_item.per_gram_weight_type is not None else None,
                            'wastage_percentage' : return_item.wastage_percentage,
                            'flat_wastage' : return_item.flat_wastage,
                            'making_charge' : return_item.making_charge,
                            'flat_making_charge' : return_item.flat_making_charge,
                            'wastage_calculation_type': return_item.wastage_calculation_type.pk,
                            'wastage_calculation_type_name': return_item.wastage_calculation_type.weight_name,
                            'making_charge_calculation_type': return_item.making_charge_calculation_type.pk,
                            'making_charge_calculation_type_name': return_item.making_charge_calculation_type.weight_name,
                            'gst' : return_item.gst,
                            'without_gst_rate' : return_item.without_gst_rate,
                            'total_rate' : return_item.total_rate,
                            'huid_rate':return_item.huid_rate,
                            
                        }
                        
                        stone_return_details=[]
                        return_stone_queryset = EstimationReturnStoneDetails.objects.filter(estimation_details=estimation_id,estimation_return_item=return_item.pk)
                        for return_stone in return_stone_queryset:
                            stone_details_return={
                                "id":return_stone.pk,
                                "estimation_details":return_stone.estimation_details.pk,
                                "estimation_return_item":return_stone.estimation_return_item.pk,
                                "stone":return_stone.stone_name.pk,
                                "stone_name":return_stone.stone_name.stone_name,
                                "stone_pieces":return_stone.stone_pieces,
                                "stone_weight":return_stone.stone_weight,
                                "stone_weight_type":return_stone.stone_weight_type.pk,
                                "stone_weight_type_name":return_stone.stone_weight_type.weight_name,
                                "stone_rate":return_stone.stone_rate,
                                "stone_rate_type":return_stone.stone_rate_type.pk,
                                "stone_rate_type_name":return_stone.stone_rate_type.type_name,
                                "include_stone_weight":return_stone.include_stone_weight,
                                "total_stone_value":return_stone.total_stone_value
                            }

                            stone_return_details.append(stone_details_return)

                        return_details['stone_details'] = stone_return_details

                        diamond_return_details=[]
                        return_diamond_queryset = EstimationReturnDiamondDetails.objects.filter(estimation_details=estimation_id,estimation_return_item=return_item.pk)
                        for return_diamond in return_diamond_queryset:
                            diamond_details_return={
                                "id":return_diamond.pk,
                                "estimation_details":return_diamond.estimation_details.pk,
                                "estimation_return_item":return_diamond.estimation_return_item.pk,
                                "diamond":return_diamond.diamond_name.pk,
                                "diamond_name":return_diamond.diamond_name.stone_name,
                                "diamond_pieces":return_diamond.diamond_pieces,
                                "diamond_weight":return_diamond.diamond_weight,
                                "diamond_weight_type":return_diamond.diamond_weight_type.pk,
                                "diamond_weight_type_name":return_diamond.diamond_weight_type.weight_name,
                                "diamond_rate":return_diamond.diamond_rate,
                                "diamond_rate_type":return_diamond.diamond_rate_type.pk,
                                "diamond_rate_type_name":return_diamond.diamond_rate_type.type_name,
                                "include_diamond_weight":return_diamond.include_diamond_weight,
                                "total_diamond_value":return_diamond.total_diamond_value
                            }

                            diamond_return_details.append(diamond_details_return)

                        return_details['diamond_details'] = diamond_return_details

                        estimation_return_details.append(return_details)

                old_purchase_queryset = EstimationOldPurchaseDetails.objects.filter(estimation_details=queryset.pk)
                
                old_purchase_details = []
                
                for old_purchase in old_purchase_queryset:
                    
                    old_purchase_serializer = EstimationOldPurchaseDetailsSerializer(old_purchase)
                    
                    old_purchase_data = old_purchase_serializer.data
                    
                    old_purchase_data['old_bill_number'] = old_purchase.old_purchase_details.old_gold_bill_number
                    
                    old_purchase_details.append(old_purchase_data)
                    
                
                advance_queryset = EstimationAdvanceDetails.objects.filter(estimation_details=queryset.pk)
                
                advance_details = []
                
                for advance in advance_queryset:
                    
                    advance_serializer = EstimationAdvanceDetailsSerializer(advance)
                    
                    advance_data = advance_serializer.data
                    
                    advance_data['advance_id'] = advance.advance_details.advance_id
                    
                    advance_details.append(advance_data)
                

            estimation_details['estimation_data']=estimation_data
            estimation_details['tag_item_details']=particulars
            estimation_details["old_item_details"] = old_gold_particulars
            estimation_details['estimation_return_details'] = estimation_return_details
            estimation_details['old_purchase_details'] = old_purchase_details
            estimation_details['advance_details'] = advance_details
            res_data.append(estimation_details)
                
        except Exception as err:

            return Response(
                {
                    "data":err,
                    "message" : res_msg.something_else(),
                    "status": status.HTTP_204_NO_CONTENT,                        
                }, status=status.HTTP_200_OK
        )  
        
        return Response(
            {
                "data" : res_data,
                # "data":{
                #     "customer_details" : customer_details,
                #     "estimation_details": res_data,
                # },
                "message" : res_msg.retrieve("Estimate details"),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK
        )  


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class EstimationEditView(APIView):
    # @transaction.atomic
    def put(self,request,pk):
        if pk != None:
            data = request.data
            # print(data)
            try:
                estimate_queryset = EstimateDetails.objects.get(id=pk)
                
                if request.user.role.is_admin == False:
                    branch = int(request.user.branch.pk)
                else:
                    branch = int(data.get('branch'))
            
                res_data={
                    'estimate_no':data.get('estimation_no'),
                    'bill_type':data.get('bill_type'),
                    'estimation_date':data.get('estimation_date'),
                    'customer_details':data.get('customer_details'),
                    'total_amount':data.get('total_amount'),
                    'discount_percentage':data.get('discount_percentage'),
                    'discount_amount':data.get('discount_amount'),
                    'stone_amount':data.get('stone_amount'),
                    'diamond_amount':data.get('diamond_amount'),
                    'chit_amount':data.get('chit_amount'),
                    'salereturn_amount':data.get('salereturn_amount'),
                    'exchange_amount':data.get('exchange_amount'),
                    'gst_percentage':data.get('gst_percentage'),
                    'gst_amount':data.get('gst_amount'),
                    'gst_type':data.get('gst_type'),
                    'payable_amount':data.get('payable_amount'),
                    'advance_amount':data.get('advance_amount'),
                    'balance_amount':data.get('balance_amount'),
                    'round_off_amount':data.get('round_off_amount'),
                    'branch': branch
                }
                res_data['modified_at'] = timezone.now()
                res_data['modified_by'] = request.user.id
                
                serializer = EstimateDetailsSerializer(estimate_queryset,data=res_data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    estimation_details=serializer.data

                    oldgold_details = request.data.get('exchange_details', {})
                    new_oldgold_data = {}
                    new_oldgold_data['old_gold_no']=data['old_gold_no']
                    if len(oldgold_details) != 0:
                        for oldgold in oldgold_details:
                            try:
                                oldgold_id = oldgold.get('id') if oldgold.get('id') != None else 0
                                oldgold_queryset = EstimationOldGold.objects.get(id=oldgold_id)

                                new_oldgold_data['old_metal']=oldgold['old_metal']
                                new_oldgold_data['old_gross_weight']=oldgold['old_gross_weight']
                                new_oldgold_data['old_reduce_weight']=oldgold['old_reduce_weight']
                                new_oldgold_data['old_net_weight']=oldgold['old_net_weight']
                                new_oldgold_data['old_touch']=oldgold['old_touch']
                                new_oldgold_data['old_dust_weight']=oldgold['old_dust_weight']
                                new_oldgold_data['estimation_details']=serializer.data['id']
                                new_oldgold_data['old_rate']=oldgold['old_rate']
                                new_oldgold_data['old_amount']=oldgold['old_amount']
                                new_oldgold_data['gst_amount']=oldgold['gst_amount']
                                new_oldgold_data['total_amount']=oldgold['total_amount']
                                new_oldgold_data['employee_id']=oldgold['employee_id']

                                oldgold_serializer = EstimationOldGoldSerializer(oldgold_queryset,data=new_oldgold_data,partial=True)
                                if oldgold_serializer.is_valid():
                                    oldgold_serializer.save()
                                else:
                                    raise Exception(oldgold_serializer.errors)
                            
                            except EstimationOldGold.DoesNotExist:
                                new_oldgold_data['old_metal']=oldgold['old_metal']
                                new_oldgold_data['old_gross_weight']=oldgold['old_gross_weight']
                                new_oldgold_data['old_reduce_weight']=oldgold['old_reduce_weight']
                                new_oldgold_data['old_net_weight']=oldgold['old_net_weight']
                                new_oldgold_data['old_touch']=oldgold['old_touch']
                                new_oldgold_data['old_dust_weight']=oldgold['old_dust_weight']
                                new_oldgold_data['estimation_details']=serializer.data['id']
                                new_oldgold_data['old_rate']=oldgold['old_rate']
                                new_oldgold_data['old_amount']=oldgold['old_amount']
                                new_oldgold_data['gst_amount']=oldgold['gst_amount']
                                new_oldgold_data['total_amount']=oldgold['total_amount']
                                new_oldgold_data['employee_id']=oldgold['employee_id']
                                
                                oldgold_newserializer = EstimationOldGoldSerializer(data=new_oldgold_data)
                                if oldgold_newserializer.is_valid():
                                    oldgold_newserializer.save()
                                else:
                                    raise Exception(oldgold_newserializer.errors)
                                
                            except Exception as error:
                                raise Exception(error)
                            
                    old_purchase_details = data.get('old_purchase_details',[])
                    
                    for old_purchase in old_purchase_details:
                        
                        old_purchase_data = {}
                        estimation_oldgold_queryset = EstimationOldPurchaseDetails.objects.filter(old_purchase_details=old_purchase.get('old_purchase_details'))
                        
                        if len(estimation_oldgold_queryset) == 0: 
                           
                            old_purchase_data['estimation_details'] = serializer.data['id']
                            old_purchase_data['old_purchase_details'] = old_purchase
                        
                            old_purchase_serializer = EstimationOldPurchaseDetailsSerializer(data=old_purchase_data)
                            
                            if old_purchase_serializer.is_valid():
                                
                                old_purchase_serializer.save()
                                
                            else:
                                transaction.set_rollback(True)
                                return Response(
                                    {
                                        "data":old_purchase_serializer.errors,
                                        "message":res_msg.not_create("Estimation"),
                                        "status":status.HTTP_400_BAD_REQUEST
                                    },status=status.HTTP_200_OK
                                )
                                
                    advance_details = data.get('advance_details',[])
                
                    for advance in advance_details:
                        
                        advance['estimation_details'] = serializer.data['id']
                        
                        advance_queryset = EstimationAdvanceDetails.objects.filter(Q(estimation_details=serializer.data['id']) & Q(advance_details=advance.get('advance_details')))
                        
                        if len(advance_queryset) != 0:
                            advance_serializer = EstimationAdvanceDetailsSerializer(advance_queryset,data=advance,partial=True)
                            if advance_serializer.is_valid():
                                advance_serializer.save()
                            else:
                                transaction.set_rollback(True)
                                return Response(
                                    {
                                        "data":advance_serializer.errors,
                                        "message":res_msg.not_create("Estimation"),
                                        "status":status.HTTP_400_BAD_REQUEST
                                    },status=status.HTTP_200_OK
                                )
                        else:
                            advance_serializer = EstimationAdvanceDetailsSerializer(data=advance)
                            if advance_serializer.is_valid():
                                advance_serializer.save()
                            else:
                                transaction.set_rollback(True)
                                return Response(
                                    {
                                        "data":advance_serializer.errors,
                                        "message":res_msg.not_create("Estimation"),
                                        "status":status.HTTP_400_BAD_REQUEST
                                    },status=status.HTTP_200_OK
                                )
                
                    chit_details = data.get('chit_details',[])
                
                    for chit in chit_details:
                        
                        chit['estimation_details'] = serializer.data['id']

                        chit_queryset = EstimationChitDetails.objects.filter(Q(estimation_details=serializer.data['id']) & Q(scheme_account_number=chit.get('scheme_account_number')))
                        
                        if len(chit_queryset) != 0:
                            chit_serializer = EstimationChitDetailsSerializer(chit_queryset,data=chit,partial=True)
                            if chit_serializer.is_valid():
                                chit_serializer.save()
                            else:
                                transaction.set_rollback(True)
                                return Response(
                                    {
                                        "data":chit_serializer.errors,
                                        "message":res_msg.not_create("Estimation"),
                                        "status":status.HTTP_400_BAD_REQUEST
                                    },status=status.HTTP_200_OK
                                )
                        else:
                            chit_serializer = EstimationChitDetailsSerializer(data=chit)
                            if chit_serializer.is_valid():
                                chit_serializer.save()
                            else:
                                transaction.set_rollback(True)
                                return Response(
                                    {
                                        "data":chit_serializer.errors,
                                        "message":res_msg.not_create("Estimation"),
                                        "status":status.HTTP_400_BAD_REQUEST
                                    },status=status.HTTP_200_OK
                                )

                    estimation_item_details = request.data.get('particular_details', [])
                    if len(estimation_item_details) != 0:
                        for item in estimation_item_details:
                            try:
                                item_id=item.get('id') if item.get('id') else 0
                                
                                estimation_tagitem_queryset = EstimationTagItems.objects.get(id=item_id)
                                
                                tag_number=item.get('tag_number')
                                tag_queryset=TaggedItems.objects.get(tag_number=tag_number)

                                estimation_tag_data = {
                                    'estimation_details': estimation_details['id'],
                                    'estimation_tag_item': tag_queryset.pk,
                                    'tag_number': item.get('tag_number'),
                                    'item_details': item.get('item_details'),
                                    'sub_item_details': item.get('sub_item_details'),
                                    'metal': item.get('metal'),
                                    'net_weight': item.get('net_weight'),
                                    'gross_weight' : item.get('gross_weight'),
                                    'pieces' : item.get('pieces'),
                                    'rate' : item.get('metal_rate'),
                                    'stone_rate' : item.get('stone_amount'),
                                    'huid_rate':item.get('item_huid_rate'),
                                    'diamond_rate' : item.get('diamond_amount'),
                                    'wastage_percentage' : item.get('wastage_percent', None),
                                    'flat_wastage' : item.get('flat_wastage', None),
                                    'making_charge' : item.get('making_charge', None),
                                    'flat_making_charge' : item.get('flat_making_charge', None),
                                    'calculation_type' : item.get('calculation_type'),
                                    'stock_type' : item.get('stock_type'),
                                    'additional_charges' : item.get('additional_charges'),
                                    'gst_percent' : item.get('gst_percent'),
                                    'gst' : item.get('gst'),
                                    'total_amount' : item.get('rate'),
                                    'with_gst_total_rate':item.get('with_gst_rate'),
                                    'making_charge_calculation_type': item.get('making_charge_calculation_type', None),
                                    'per_gram_weight_type' : item.get('per_gram_weight_type',None),
                                    'wastage_calculation_type': item.get('wastage_calculation_type', None),
                                    'employee_id':item.get('employee_id')
                                }
                                estimation_taggeditem_serializer = EstimationTagItemsSerializer(estimation_tagitem_queryset,data=estimation_tag_data,partial=True)
                                if estimation_taggeditem_serializer.is_valid():
                                    estimation_taggeditem_serializer.save()
                                    
                                    stone_details=item.get('stone_details') if item.get('stone_details') else []
                                    for stone in stone_details:
                                        try:
                                            stone_id=stone.get('id') if stone.get('id') else None
                                            
                                            stone_queryset = EstimationStoneDetails.objects.get(id=stone_id)

                                            stone['estimation_details'] = estimation_details['id']
                                            stone['estimation_item_details'] = estimation_taggeditem_serializer.data['id']
                                            stone['stone_name']=float(stone['stone_name'])
                                            stone['stone_pieces']=float(stone['stone_pieces'])
                                            stone['stone_weight']=float(stone['stone_weight'])
                                            stone['stone_weight_type']=int(stone['stone_weight_type'])
                                            stone['stone_rate']=float(stone['stone_rate'])
                                            stone['stone_rate_type']=int(stone['stone_rate_type'])
                                            stone['include_stone_weight']=stone['include_stone_weight']

                                            if int(stone['stone_weight_type']) == int(settings.CARAT):
                                                stone['stone_weight']=(float(stone['stone_weight'])/5)

                                            if int(stone['stone_rate_type']) == int(settings.PERGRAM):
                                                total_stone_value=float(stone['stone_rate']*stone['stone_weight'])
                                                stone['total_stone_value']=total_stone_value
                                            
                                            if int(stone['stone_rate_type']) == int(settings.PERCARAT):
                                                stone_rate = float(stone['stone_rate'])*5
                                                stone['stone_rate'] = stone_rate
                                                total_stone_value=float(stone['stone_rate']*stone['stone_weight'])
                                                stone['total_stone_value']=total_stone_value

                                            if int(stone['stone_rate_type']) == int(settings.PERPIECE):
                                                total_stone_value=float(stone['stone_rate']*stone['stone_pieces'])
                                                stone['total_stone_value']=total_stone_value
                                                
                                            estimationold_stone_serializer=EstimationStoneDetailsSerializer(stone_queryset,data=stone,partial=True)
                                            if estimationold_stone_serializer.is_valid():
                                                estimationold_stone_serializer.save()
                                            else:
                                                raise Exception (estimationold_stone_serializer.errors)
                                            
                                        except EstimationStoneDetails.DoesNotExist:
                                            stone['estimation_details'] = estimation_details['id']
                                            stone['estimation_item_details'] = estimation_taggeditem_serializer.data['id']
                                            stone['stone_name']=float(stone['stone_name'])
                                            stone['stone_pieces']=float(stone['stone_pieces'])
                                            stone['stone_weight']=float(stone['stone_weight'])
                                            stone['stone_weight_type']=int(stone['stone_weight_type'])
                                            stone['stone_rate']=float(stone['stone_rate'])
                                            stone['stone_rate_type']=int(stone['stone_rate_type'])
                                            stone['include_stone_weight']=stone['include_stone_weight']

                                            if int(stone['stone_weight_type']) == int(settings.CARAT):
                                                stone['stone_weight']=(float(stone['stone_weight'])/5)

                                            if int(stone['stone_rate_type']) == int(settings.PERGRAM):
                                                total_stone_value=float(stone['stone_rate']*stone['stone_weight'])
                                                stone['total_stone_value']=total_stone_value
                                            
                                            if int(stone['stone_rate_type']) == int(settings.PERCARAT):
                                                stone_rate = float(stone['stone_rate'])*5
                                                stone['stone_rate'] = stone_rate
                                                total_stone_value=float(stone['stone_rate']*stone['stone_weight'])
                                                stone['total_stone_value']=total_stone_value

                                            if int(stone['stone_rate_type']) == int(settings.PERPIECE):
                                                total_stone_value=float(stone['stone_rate']*stone['stone_pieces'])
                                                stone['total_stone_value']=total_stone_value
                                                
                                            estimationnew_stone_serializer=EstimationStoneDetailsSerializer(data=stone)
                                            if estimationnew_stone_serializer.is_valid():
                                                estimationnew_stone_serializer.save()
                                            else:
                                                raise Exception (estimationnew_stone_serializer.errors)

                                        except Exception as err:
                                            raise Exception(err)

                                    diamond_details=item.get('diamond_details') if item.get('diamond_details') else []
                                    for diamond in diamond_details :
                                        try:
                                            diamond_id=diamond.get('id') if diamond.get('id') else None

                                            diamond_queryset = EstimationDiamondDetails.objects.get(id=diamond_id)

                                            diamond['estimation_details'] = estimation_details['id']
                                            diamond['estimation_item_details'] = estimation_taggeditem_serializer.data['id']
                                            diamond['diamond_name'] = float(diamond['diamond_name'])
                                            diamond['diamond_pieces'] = float(diamond['diamond_pieces'])
                                            diamond['diamond_weight'] = float(diamond['diamond_weight'])
                                            diamond['diamond_weight_type'] = int(diamond['diamond_weight_type'])
                                            diamond['diamond_rate'] = float(diamond['diamond_rate'])
                                            diamond['diamond_rate_type'] = int(diamond['diamond_rate_type'])
                                            diamond['include_diamond_weight'] = diamond['include_diamond_weight']

                                            if int(diamond['diamond_weight_type']) == settings.CARAT :
                                                diamond_weight=float(diamond['diamond_weight'])/5
                                                diamond['diamond_weight']=diamond_weight


                                            if int(diamond['diamond_rate_type']) ==settings.PERGRAM:
                                                total_diamond_value=float(diamond['diamond_rate']*diamond['diamond_weight'])
                                                diamond['total_diamond_value'] = total_diamond_value

                                            if int(diamond['diamond_rate_type']) == settings.PERCARAT:
                                                diamond_rate=float(diamond['diamond_rate'])*5
                                                diamond['diamond_rate']=diamond_rate
                                                total_diamond_value=float(diamond['diamond_rate']*diamond['diamond_weight'])
                                                diamond['total_diamond_value'] = total_diamond_value

                                            if int(diamond['diamond_rate_type']) ==settings.PERPIECE:
                                                total_diamond_value=float(diamond['diamond_rate']*diamond['diamond_pieces'])
                                                diamond['total_diamond_value'] = total_diamond_value

                                            estimationold_diamond_serializer=EstimationDiamondDetailsSerializer(diamond_queryset,data=diamond,partial=True)
                                            if estimationold_diamond_serializer.is_valid():
                                                estimationold_diamond_serializer.save()
                                            else:
                                                raise Exception(estimationold_diamond_serializer.errors)
                                            
                                        except EstimationDiamondDetails.DoesNotExist:
                                            diamond['estimation_details'] = estimation_details['id']
                                            diamond['estimation_item_details'] = estimation_taggeditem_serializer.data['id']
                                            diamond['diamond_name'] = float(diamond['diamond_name'])
                                            diamond['diamond_pieces'] = float(diamond['diamond_pieces'])
                                            diamond['diamond_weight'] = float(diamond['diamond_weight'])
                                            diamond['diamond_weight_type'] = int(diamond['diamond_weight_type'])
                                            diamond['diamond_rate'] = float(diamond['diamond_rate'])
                                            diamond['diamond_rate_type'] = int(diamond['diamond_rate_type'])
                                            diamond['include_diamond_weight'] = diamond['include_diamond_weight']

                                            if int(diamond['diamond_weight_type']) == settings.CARAT :
                                                diamond_weight=float(diamond['diamond_weight'])/5
                                                diamond['diamond_weight']=diamond_weight


                                            if int(diamond['diamond_rate_type']) ==settings.PERGRAM:
                                                total_diamond_value=float(diamond['diamond_rate']*diamond['diamond_weight'])
                                                diamond['total_diamond_value'] = total_diamond_value

                                            if int(diamond['diamond_rate_type']) == settings.PERCARAT:
                                                diamond_rate=float(diamond['diamond_rate'])*5
                                                diamond['diamond_rate']=diamond_rate
                                                total_diamond_value=float(diamond['diamond_rate']*diamond['diamond_weight'])
                                                diamond['total_diamond_value'] = total_diamond_value

                                            if int(diamond['diamond_rate_type']) ==settings.PERPIECE:
                                                total_diamond_value=float(diamond['diamond_rate']*diamond['diamond_pieces'])
                                                diamond['total_diamond_value'] = total_diamond_value

                                            estimationnew_diamond_serializer=EstimationDiamondDetailsSerializer(data=diamond)
                                            if estimationnew_diamond_serializer.is_valid():
                                                estimationnew_diamond_serializer.save()
                                        
                                        except Exception as err:
                                            raise Exception(err)
                                else:
                                    raise Exception(estimation_taggeditem_serializer.errors)
                                
                            except EstimationTagItems.DoesNotExist:
                                tag_number=item.get('tag_number')

                                tag_queryset=TaggedItems.objects.get(tag_number=tag_number)
                                estimation_tag_data = {
                                    'estimation_details': estimation_details['id'],
                                    'estimation_tag_item': tag_queryset.pk,
                                    'tag_number': item.get('tag_number'),
                                    'item_details': item.get('item_details'),
                                    'sub_item_details': item.get('sub_item_details'),
                                    'metal': item.get('metal'),
                                    'net_weight': item.get('net_weight'),
                                    'gross_weight' : item.get('gross_weight'),
                                    'tag_weight' : item.get('tag_weight'),
                                    'cover_weight' : item.get('cover_weight'),
                                    'loop_weight' : item.get('loop_weight'),
                                    'other_weight' : item.get('other_weight'),
                                    'pieces' : item.get('pieces'),
                                    'total_pieces' : item.get('total_pieces'),
                                    'rate' : item.get('metal_rate'),
                                    'stone_rate' : item.get('stone_rate'),
                                    'diamond_rate' : item.get('diamond_rate'),
                                    'stock_type' : item.get('stock_type'),
                                    'calculation_type' : item.get('calculation_type'),
                                    'tax_percent' : item.get('tax_percent'),
                                    'additional_charges' : item.get('additional_charges'),
                                    'total_stone_weight' : item.get('total_stone_weight'),
                                    'total_diamond_weight' : item.get('total_diamond_weight'),
                                    'per_gram_weight_type' : item.get('per_gram_weight_type',None),
                                    'wastage_percentage' : item.get('wastage_percent', None),
                                    'flat_wastage' : item.get('flat_wastage', None),
                                    'making_charge' : item.get('making_charge', None),
                                    'flat_making_charge' : item.get('flat_making_charge', None),
                                    'wastage_calculation_type': item.get('wastage_calculation_type', None),
                                    'making_charge_calculation_type': item.get('making_charge_calculation_type', None),
                                    'gst' : item.get('gst'),
                                    'total_rate' : item.get('with_gst_rate'),
                                    'without_gst_rate':item.get('rate'),
                                    'huid_rate':item.get('item_huid_rate'),
                                    'employee_id':item.get('employee_id')
                                }
                                
                                estimationnew_taggeditem_serializer = EstimationTagItemsSerializer(data=estimation_tag_data)
                                if estimationnew_taggeditem_serializer.is_valid():
                                    estimationnew_taggeditem_serializer.save()

                                    stone_details=item.get('stone_details') if item.get('stone_details') else []

                                    for stone in stone_details:
                                        stone['estimation_details'] = estimation_details['id']
                                        stone['estimation_item_details'] = estimationnew_taggeditem_serializer.data['id']
                                        stone['stone_name']=float(stone['stone_name'])
                                        stone['stone_pieces']=float(stone['stone_pieces'])
                                        stone['stone_weight']=float(stone['stone_weight'])
                                        stone['stone_weight_type']=int(stone['stone_weight_type'])
                                        stone['stone_rate']=float(stone['stone_rate'])
                                        stone['stone_rate_type']=int(stone['stone_rate_type'])
                                        stone['include_stone_weight']=stone['include_stone_weight']

                                        if int(stone['stone_weight_type']) == int(settings.CARAT):
                                            stone['stone_weight']=(float(stone['stone_weight'])/5)

                                        if int(stone['stone_rate_type']) == int(settings.PERGRAM):
                                            total_stone_value=float(stone['stone_rate']*stone['stone_weight'])
                                            stone['total_stone_value']=total_stone_value
                                        
                                        if int(stone['stone_rate_type']) == int(settings.PERCARAT):
                                            stone_rate = float(stone['stone_rate'])*5
                                            stone['stone_rate'] = stone_rate
                                            total_stone_value=float(stone['stone_rate']*stone['stone_weight'])
                                            stone['total_stone_value']=total_stone_value

                                        if int(stone['stone_rate_type']) == int(settings.PERPIECE):
                                            total_stone_value=float(stone['stone_rate']*stone['stone_pieces'])
                                            stone['total_stone_value']=total_stone_value

                                        estimation_stone_serializer=EstimationStoneDetailsSerializer(data=stone)
                                        if estimation_stone_serializer.is_valid():
                                            estimation_stone_serializer.save()
                                        else:
                                            raise Exception (estimation_stone_serializer.errors)

                                    diamond_details=item.get('diamond_details') if item.get('diamond_details') else []

                                    for diamond in diamond_details :

                                        diamond['estimation_details'] = estimation_details['id']
                                        diamond['estimation_item_details'] = estimationnew_taggeditem_serializer.data['id']
                                        diamond['diamond_name'] = float(diamond['diamond_name'])
                                        diamond['diamond_pieces'] = float(diamond['diamond_pieces'])
                                        diamond['diamond_weight'] = float(diamond['diamond_weight'])
                                        diamond['diamond_weight_type'] = int(diamond['diamond_weight_type'])
                                        diamond['diamond_rate'] = float(diamond['diamond_rate'])
                                        diamond['diamond_rate_type'] = int(diamond['diamond_rate_type'])
                                        diamond['include_diamond_weight'] = diamond['include_diamond_weight']

                                        if int(diamond['diamond_weight_type']) == settings.CARAT :
                                            diamond_weight=float(diamond['diamond_weight'])/5
                                            diamond['diamond_weight']=diamond_weight


                                        if int(diamond['diamond_rate_type']) ==settings.PERGRAM:
                                            total_diamond_value=float(diamond['diamond_rate']*diamond['diamond_weight'])
                                            diamond['total_diamond_value'] = total_diamond_value

                                        if int(diamond['diamond_rate_type']) == settings.PERCARAT:
                                            diamond_rate=float(diamond['diamond_rate'])*5
                                            diamond['diamond_rate']=diamond_rate
                                            total_diamond_value=float(diamond['diamond_rate']*diamond['diamond_weight'])
                                            diamond['total_diamond_value'] = total_diamond_value

                                        if int(diamond['diamond_rate_type']) ==settings.PERPIECE:
                                            total_diamond_value=float(diamond['diamond_rate']*diamond['diamond_pieces'])
                                            diamond['total_diamond_value'] = total_diamond_value

                                        estimation_diamond_serializer=EstimationDiamondDetailsSerializer(data=diamond)
                                        if estimation_diamond_serializer.is_valid():
                                            estimation_diamond_serializer.save()
                                        else:
                                            raise Exception(estimation_diamond_serializer.errors)

                                else:
                                    raise Exception(estimationnew_taggeditem_serializer.errors)
                            except Exception as err:
                                raise Exception(err)
                            
                    return Response(
                        {
                            "message":res_msg.update("Estimation Biling"),
                            "status":status.HTTP_200_OK
                        },status=status.HTTP_200_OK)
                    
                else:
                    raise Exception(serializer.errors)
            
            except Exception as err:
                # transaction.set_rollback(True)
                return Response(
                    {
                        "data":str(err),
                        "message":res_msg.something_else(),
                        "status":status.HTTP_204_NO_CONTENT
                    },status=status.HTTP_200_OK
                )
        else:
            return Response(
                {
                    "data":str(err),
                    "message":res_msg.not_exists("Given Id"),
                    "status":status.HTTP_204_NO_CONTENT
                },status=status.HTTP_200_OK
            )


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class BillingView(viewsets.ViewSet):
    @transaction.atomic
    def create(self,request):
                
        request_data = request.data 
        
        request_data['created_at'] = timezone.now()
        request_data['created_by'] = request.user.id
            
        request_data['bill_id'] = request_data.get('bill_id')
        
        if request.user.role.is_admin == True:
            branch = request_data.get('branch')
        else:
            branch = request.user.branch.pk

        request_data['branch'] = branch
                
        serializer = BillingDetailsSerializer(data=request_data)
        
        if serializer.is_valid():
            
            serializer.save()

            if int(request_data['bill_type']) == 1:
                bill_id_dict={}
                bill_id_dict['bill_id']=serializer.data['bill_id']
                bill_number_serializer=BillIDSerializer(data=bill_id_dict)

                if bill_number_serializer.is_valid():
                    bill_number_serializer.save()
                
            elif int(request_data['bill_type']) == 2:

                bill_id_dict={}
                bill_id_dict['silver_bill_id']=serializer.data['bill_id']
                bill_number_serializer=SilverBillIDSerializer(data=bill_id_dict)

                if bill_number_serializer.is_valid():
                    bill_number_serializer.save()
            
            else:
                pass
            
            estimation_details = request_data.get('estimation_details',[])
            
            for estimation in  estimation_details:
                
                estimation_data = {}
                
                estimation_data['billing_details'] = serializer.data['id']
                estimation_data['estimation_details'] = estimation
                
                estimation_serializer = BillingEstimationDetailsSerializer(data=estimation_data)
                
                if estimation_serializer.is_valid():
                    
                    estimation_serializer.save()
                    
                else:
                    transaction.set_rollback(True)
                    return Response(
                        {
                            "data":estimation_serializer.errors,
                            "message":res_msg.not_create("Billing"),
                            "status":status.HTTP_400_BAD_REQUEST
                        },status=status.HTTP_200_OK
                    )
                
            
            particular_details = request_data.get('particular_details',[])
            
            for particular in particular_details:
                
                tag_number = particular.get('tag_number',None)
                
                if tag_number == None:
                    
                    return Response(
                        {
                            "message":res_msg.missing_fields("Tag Number"),
                            "status":status.HTTP_204_NO_CONTENT
                        },status=status.HTTP_200_OK
                    )
                    
                try:
                    
                    tag_queryset = TaggedItems.objects.get(tag_number=tag_number)
                    
                    if tag_queryset.is_billed == True:
                        transaction.set_rollback(True)
                        return Response(
                            {
                                "message":str(tag_queryset.tag_number)+"is already billed",
                                "status":status.HTTP_204_NO_CONTENT
                            },status=status.HTTP_200_OK
                        )
                    
                    particular['tag_details'] = tag_queryset.pk
                    
                except TaggedItems.DoesNotExist:
                    transaction.set_rollback(True)
                    return Response(
                        {
                            "message":res_msg.not_exists("Tag"),
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
                
                particular['billing_details'] = serializer.data['id']
                particular['rate'] = particular.get('metal_rate')
                particular['pieces'] = particular.get('pieces')
                particular['gross_weight'] = particular.get('gross_weight')
                particular['reduce_weight'] = particular.get('reduce_weight')
                particular['net_weight'] = particular.get('net_weight')
                particular['wastage_percent'] = particular.get('wastage_percent')
                particular['flat_wastage'] = particular.get('flat_wastage')
                particular['making_charge_per_gram'] = particular.get('making_charge')
                particular['flat_making_charge'] = particular.get('flat_making_charge')
                particular['stone_amount'] = particular.get('stone_rate')
                particular['diamond_amount'] = particular.get('diamond_rate')
                particular['huid_amount'] = particular.get('item_huid_rate')
                particular['total_amount'] = particular.get('rate')
                particular['gst_percent'] = particular.get('gst_percent')
                particular['gst_amount'] = particular.get('gst')
                particular['payable_amount'] = particular.get('with_gst_rate')

                particular_serializer = BillingParticularDetailsSerializer(data=particular)
                
                if particular_serializer.is_valid():
                    
                    particular_serializer.save()
                    
                    # stone_details = particular.get('stone_details',[])

                    # for stone in stone_details:
                    #     stone_item = {}
                    #     stone_item['billing_particular_details'] = particular_serializer.data['id']
                    #     stone_item['stone_name']=float(stone['stone_name'])
                    #     stone_item['stone_pieces']=float(stone['stone_pieces'])
                    #     stone_item['stone_weight']=float(stone['stone_weight'])
                    #     stone_item['stone_weight_type']=int(stone['stone_weight_type'])
                    #     stone_item['stone_rate']=float(stone['stone_rate'])
                    #     stone_item['stone_rate_type']=int(stone['stone_rate_type'])
                    #     stone_item['include_stone_weight']=stone['include_stone_weight']

                    #     if int(stone_item['stone_weight_type']) == int(settings.CARAT):
                    #         stone_item['stone_weight']=(float(stone_item['stone_weight'])/5)

                    #     if int(stone_item['stone_rate_type']) == int(settings.PERGRAM):
                    #         stone_amount=float(stone_item['stone_rate']*stone_item['stone_weight'])
                    #         stone_item['stone_amount']=stone_amount
                        
                    #     if int(stone_item['stone_rate_type']) == int(settings.PERCARAT):
                    #         stone_rate = float(stone_item['stone_rate'])*5
                    #         stone_item['stone_rate'] = stone_rate
                    #         stone_amount=float(stone_item['stone_rate']*stone_item['stone_weight'])
                    #         stone_item['stone_amount']=stone_amount

                    #     if int(stone_item['stone_rate_type']) == int(settings.PERPIECE):
                    #         stone_amount=float(stone_item['stone_rate']*stone_item['stone_pieces'])
                    #         stone_item['stone_amount']=stone_amount

                    #     stone_serializer=BillingParticularStoneDetails(data=stone_item)
                    #     if stone_serializer.is_valid():
                    #         stone_serializer.save()
                    #     else:
                    #         transaction.set_rollback(True)
                    #         return Response(
                    #             {
                    #                 "data":stone_serializer.errors,
                    #                 "message":res_msg.not_create("Billing"),
                    #                 "status":status.HTTP_400_BAD_REQUEST
                    #             },status=status.HTTP_200_OK
                    #         )

                    #     diamond_details=particular.get('diamond_details',[])

                    #     for diamond in diamond_details :

                    #         diamond['billing_particular_details'] = particular_serializer.data['id']
                    #         diamond['diamond_name'] = float(diamond['diamond_name'])
                    #         diamond['diamond_pieces'] = float(diamond['diamond_pieces'])
                    #         diamond['diamond_weight'] = float(diamond['diamond_weight'])
                    #         diamond['diamond_weight_type'] = int(diamond['diamond_weight_type'])
                    #         diamond['diamond_rate'] = float(diamond['diamond_rate'])
                    #         diamond['diamond_rate_type'] = int(diamond['diamond_rate_type'])
                    #         diamond['include_diamond_weight'] = diamond['include_diamond_weight']

                    #         if int(diamond['diamond_weight_type']) == settings.CARAT :
                    #             diamond_weight=float(diamond['diamond_weight'])/5
                    #             diamond['diamond_weight']=diamond_weight

                    #         if int(diamond['diamond_rate_type']) ==settings.PERGRAM:
                    #             diamond_amount=float(diamond['diamond_rate']*diamond['diamond_weight'])
                    #             diamond['diamond_amount'] = diamond_amount

                    #         if int(diamond['diamond_rate_type']) == settings.PERCARAT:
                    #             diamond_rate=float(diamond['diamond_rate'])*5
                    #             diamond['diamond_rate']=diamond_rate
                    #             diamond_amount=float(diamond['diamond_rate']*diamond['diamond_weight'])
                    #             diamond['diamond_amount'] = diamond_amount

                    #         if int(diamond['diamond_rate_type']) ==settings.PERPIECE:
                    #             diamond_amount=float(diamond['diamond_rate']*diamond['diamond_pieces'])
                    #             diamond['diamond_amount'] = diamond_amount

                    #         diamond_serializer=BillingParticularsDiamondDetails(data=diamond)
                    #         if diamond_serializer.is_valid():
                    #             diamond_serializer.save()
                    #         else:
                    #             transaction.set_rollback(True)
                    #             return Response(
                    #                 {
                    #                     "data":diamond_serializer.errors,
                    #                     "message":res_msg.not_create("Billing"),
                    #                     "status":status.HTTP_400_BAD_REQUEST
                    #                 },status=status.HTTP_200_OK
                    #             )
                            
                    tag_update_data = {}
                    
                    tag_update_data['remaining_pieces'] = tag_queryset.tag_pieces - particular_serializer.data['pieces']
                    tag_update_data['remaining_gross_weight'] = tag_queryset.gross_weight - particular_serializer.data['gross_weight']
                    tag_update_data['remaining_net_weight'] = tag_queryset.net_weight - particular_serializer.data['net_weight']
                    
                    if tag_update_data['remaining_pieces'] == 0 and tag_update_data['remaining_gross_weight'] == 0.0 and tag_update_data['remaining_net_weight'] == 0.0:
                        
                        tag_update_data['is_billed'] = True
                        tag_update_data['billed_at'] = timezone.now()
                    
                    tag_update_serializer = TaggedItemsSerializer(tag_queryset,data=tag_update_data,partial=True)
                    
                    if tag_update_serializer.is_valid():
                        
                        tag_update_serializer.save()
                        
                    else:
                        
                        transaction.set_rollback(True)
                        
                        return Response(
                            {
                                "data":tag_update_serializer.errors,
                                "message":res_msg.not_create("Billing"),
                                "status":status.HTTP_400_BAD_REQUEST
                            },status=status.HTTP_200_OK
                        )
                        
                    stock_ledger_data = {}
                    
                    stock_ledger_data['tag_details'] = tag_queryset.pk
                    stock_ledger_data['stock_type'] = settings.OUT
                    stock_ledger_data['entry_type'] = None
                    stock_ledger_data['entry_date'] = timezone.now()
                    stock_ledger_data['pieces'] = particular_serializer.data['pieces']
                    stock_ledger_data['gross_weight'] = particular_serializer.data['gross_weight']
                    
                    stock_ledger_serializer = StockLedgerSerializer(data=stock_ledger_data)
                    
                    if stock_ledger_serializer.is_valid():
                        
                        stock_ledger_serializer.save()
                        
                    else:
                        transaction.set_rollback(True)
                        return Response(
                            {
                                "data":stock_ledger_serializer.errors,
                                "message":res_msg.not_create("Billing"),
                                "status":status.HTTP_400_BAD_REQUEST
                            },status=status.HTTP_200_OK
                        )
                    
                else:
                    
                    transaction.set_rollback(True)
                    
                    return Response(
                        {
                            "data":particular_serializer.errors,
                            "message":res_msg.not_create("Billing"),
                            "status":status.HTTP_400_BAD_REQUEST
                        },status=status.HTTP_200_OK
                    )
                    
            customer_ledger_data = {}
            
            customer_ledger_data['customer_details'] = serializer.data['customer_details']
            customer_ledger_data['entry_date'] = timezone.now()
            customer_ledger_data['entry_type'] = settings.SALES_ENTRY
            customer_ledger_data['transaction_type'] = settings.CREDIT_ENTRY
            customer_ledger_data['invoice_number'] = serializer.data['bill_id']
            customer_ledger_data['reffrence_number'] = None
            customer_ledger_data['transaction_amount'] = serializer.data['payable_amount']
            customer_ledger_data['transaction_weight'] = 0.0
            customer_ledger_data['branch'] = branch
            
            customer_ledger_serializer = CustomerLedgerSerializer(data=customer_ledger_data)
            
            if customer_ledger_serializer.is_valid():
                
                customer_ledger_serializer.save()
                
            else:
                
                transaction.set_rollback(True)
                
                return Response(
                    {
                        "data":customer_ledger_serializer.errors,
                        "message":res_msg.not_create("Billing"),
                        "status":status.HTTP_400_BAD_REQUEST
                    },status=status.HTTP_200_OK
                )
                    
            is_payment = request_data.get('is_payment',None)
            
            if is_payment == None:
                transaction.set_rollback(True)
                return Response(
                    {
                        "message":res_msg.missing_fields("is_payment"),
                        "status":status.HTTP_204_NO_CONTENT
                    },status=status.HTTP_200_OK
                )
                
            if is_payment == True:
                
                payment_details_data = {}
                payment_details_data['billing_details'] = serializer.data['id'] 
                payment_details_data['payment_date'] = timezone.now()
                payment_details_data['created_by'] = request.user.id
                payment_details_data['branch'] = branch
                
                pay_id = True
        
                while pay_id ==True:
                    
                    random_number = random.randint(100, 9999999)
                    
                    generated_number = "BPMT"+str(random_number)
                    
                    try:
                    
                        bill_number_queryset = BillingPaymentDetails.objects.get(payment_id=generated_number)
                        pay_id = True
                    except BillingPaymentDetails.DoesNotExist:
                        payment_details_data['payment_id'] = generated_number
                        pay_id=False
                        
                    except Exception  as err:
                        transaction.set_rollback(True)
                        return Response(
                            {
                                "data":str(err),
                                "message":res_msg.something_else(),
                                "status":status.HTTP_204_NO_CONTENT
                            },status=status.HTTP_200_OK
                        )
                
                payment_details_serializer = BillingPaymentDetailsSerializer(data=payment_details_data)
                
                if payment_details_serializer.is_valid():
                    
                    payment_details_serializer.save()
                    
                    payment_denomination_details = request_data.get('payment_denomination_details',[])
                    
                    for denominations in payment_denomination_details:
                        
                        denominations['payment_details'] = payment_details_serializer.data['id']
                        
                        denomination_serializer = BillingPaymentDenominationSerializer(data=denominations)
                        
                        if denomination_serializer.is_valid():
                            
                            denomination_serializer.save()
                            
                        else:
                            
                            transaction.set_rollback(True)
                            
                            return Response(
                                {
                                    "data":denomination_serializer.errors,
                                    "message":res_msg.not_create("Billing"),
                                    "status":status.HTTP_400_BAD_REQUEST
                                },status=status.HTTP_200_OK
                            )
                            
                    exchange_details = request_data.get('exchange_details',[])
                    
                    for exchange in  exchange_details:
                        
                        exchange_data = {}
                        
                        exchange_data['payment_details'] = payment_details_serializer.data['id']
                        exchange_data['old_purchase_details'] = exchange
                        
                        exchange_serializer = BillingExchangeDetailsSerializer(data=exchange_data)
                        
                        if exchange_serializer.is_valid():
                            
                            exchange_serializer.save()
                            
                            old_bill_queryset = OldGoldBillDetails.objects.get(id=exchange_serializer.data['old_purchase_details'])
                            
                            if old_bill_queryset.is_canceled == True:
                                transaction.set_rollback(True)
                                return Response(
                                    {
                                        "message":str(old_bill_queryset.old_gold_bill_number)+"is already cancelled",
                                        "status":status.HTTP_204_NO_CONTENT
                                    },status=status.HTTP_200_OK
                                )
                                
                            if old_bill_queryset.is_billed == True:
                                transaction.set_rollback(True)
                                return Response(
                                    {
                                        "message":str(old_bill_queryset.old_gold_bill_number)+"is Already Billed",
                                        "status":status.HTTP_204_NO_CONTENT
                                    },status=status.HTTP_200_OK
                                )
                            
                            old_bill_update_data = {}
                            
                            old_bill_update_data['is_billed'] = True
                            old_bill_update_data['refference_number'] = serializer.data['bill_id']
                            
                            old_bill_update_serializer = OldGoldBillDetailsSerializer(old_bill_queryset,data=old_bill_update_data,partial=True)
                            
                            if old_bill_update_serializer.is_valid():
                                
                                old_bill_update_serializer.save()
                                
                                exchange_customer_ledger_data = {}
                            
                                exchange_customer_ledger_data['customer_details'] = old_bill_queryset.customer_details.pk
                                exchange_customer_ledger_data['entry_date'] = timezone.now()
                                exchange_customer_ledger_data['entry_type'] = settings.OLD_PURCHASE_ENTRY
                                exchange_customer_ledger_data['transaction_type'] = settings.CREDIT_ENTRY
                                exchange_customer_ledger_data['invoice_number'] = serializer.data['bill_id']
                                exchange_customer_ledger_data['reffrence_number'] = str(old_bill_queryset.old_gold_bill_number)
                                exchange_customer_ledger_data['transaction_amount'] = old_bill_queryset.old_gold_amount
                                exchange_customer_ledger_data['transaction_weight'] = 0.0
                                exchange_customer_ledger_data['branch'] = branch
                                
                                exchange_customer_ledger_serializer = CustomerLedgerSerializer(data=exchange_customer_ledger_data)
                                
                                if exchange_customer_ledger_serializer.is_valid():
                                    
                                    exchange_customer_ledger_serializer.save()
                                    
                                else:
                                    
                                    transaction.set_rollback(True)
                                    
                                    return Response(
                                        {
                                            "data":exchange_customer_ledger_serializer.errors,
                                            "message":res_msg.not_create("Billing"),
                                            "status":status.HTTP_400_BAD_REQUEST
                                        },status=status.HTTP_200_OK
                                    )
                                
                            else:
                                transaction.set_rollback(True)
                                return Response(
                                    {
                                        "data":old_bill_update_serializer.errors,
                                        "message":res_msg.not_create("Billing"),
                                        "status":status.HTTP_400_BAD_REQUEST
                                    },status=status.HTTP_200_OK
                                )
                            
                        else:
                            transaction.set_rollback(True)
                            return Response(
                                {
                                    "data":exchange_serializer.errors,
                                    "message":res_msg.not_create("Billing"),
                                    "stauts":status.HTTP_400_BAD_REQUEST
                                },status=status.HTTP_200_OK
                            )
                    
                    advance_details = request_data.get('advance_details',[])
                    
                    for advance in advance_details:
                        
                        advance['payment_details'] = payment_details_serializer.data['id']
                        
                        advance_serializer = BillingAdvanceDetailsSerializer(data=advance)
                        
                        if advance_serializer.is_valid():
                            
                            advance_serializer.save()
                            
                            advance_queryset = AdvanceDetails.objects.get(id=advance_serializer.data['advance_details'])
                            
                            if advance_queryset.is_cancelled == True:
                                
                                transaction.set_rollback(True)
                                
                                return Response(
                                    {
                                        "message":str(advance_queryset.advance_id)+"Advance is already cancelled",
                                        "status":status.HTTP_204_NO_CONTENT
                                    },status=status.HTTP_200_OK
                                )
                                
                            
                            if advance_queryset.is_redeemed == True:
                                
                                transaction.set_rollback(True)
                                return Response(
                                    {
                                        "message":str(advance_queryset.advance_id)+"Advance is already redeemed",
                                        "status":status.HTTP_204_NO_CONTENT
                                    },status=status.HTTP_200_OK
                                )
                                
                            redeem_amount = 0
                            redeem_weight = 0
                                
                            advance_log_queryset = AdvanceLogs.objects.filter(advance_details=advance_queryset.pk,is_cancelled=False)
                            
                            for logs in advance_log_queryset:
                                
                                redeem_amount += logs.redeem_amount
                                redeem_weight += logs.redeem_weight
                                
                            remaining_weight = advance_queryset.total_advance_weight - redeem_weight
                            remaining_amount = advance_queryset.total_advance_amount - redeem_amount
                            
                            advance_log_update_data = {}
                            
                            advance_log_update_data['advance_details'] = advance_queryset.pk
                            
                            advance_log_update_data['redeem_weight'] = advance_serializer.data['redeem_weight']
                            advance_log_update_data['redeem_amount'] = advance_serializer.data['redeem_amount']
                            
                            if remaining_weight < advance_serializer.data['redeem_weight'] or remaining_amount < advance_serializer.data['redeem_amount']:
                                
                                transaction.set_rollback(True)
                                return Response(
                                    {
                                        "message":"for advance"+str(advance_queryset.advance_id)+"remaining weight is"+str(remaining_weight)+"remaining amount is"+str(remaining_amount),
                                        "status":status.HTTP_204_NO_CONTENT
                                    },status=status.HTTP_200_OK
                                )
                                
                            advance_log_update_serializer = AdvanceLogsSerializer(data=advance_log_update_data)
                            
                            if advance_log_update_serializer.is_valid():
                                
                                advance_log_update_serializer.save()
                                
                                advance_customer_ledger_data = {}
                            
                                advance_customer_ledger_data['customer_details'] = advance_queryset.customer_details.pk
                                advance_customer_ledger_data['entry_date'] = timezone.now()
                                advance_customer_ledger_data['entry_type'] = settings.ADVANCE_ENTRY
                                advance_customer_ledger_data['transaction_type'] = settings.CREDIT_ENTRY
                                advance_customer_ledger_data['invoice_number'] = serializer.data['bill_id']
                                advance_customer_ledger_data['reffrence_number'] = advance_queryset.advance_id
                                advance_customer_ledger_data['transaction_amount'] = advance_log_update_serializer.data['redeem_amount']
                                advance_customer_ledger_data['transaction_weight'] = advance_log_update_serializer.data['redeem_weight']
                                advance_customer_ledger_data['branch'] = branch
                                
                                advance_customer_ledger_serializer = CustomerLedgerSerializer(data=advance_customer_ledger_data)
                                
                                if advance_customer_ledger_serializer.is_valid():
                                    
                                    advance_customer_ledger_serializer.save()
                                    
                                else:
                                    
                                    transaction.set_rollback(True)
                                    return Response(
                                        {
                                            "data":advance_customer_ledger_serializer.errors,
                                            "message":res_msg.not_create("Billing"),
                                            "status":status.HTTP_400_BAD_REQUEST
                                        },status=status.HTTP_200_OK
                                    )
                                
                            else:
                                transaction.set_rollback(True)
                                return Response(
                                    {
                                        "data":advance_log_update_serializer.errors,
                                        "message":res_msg.not_create("Billing"),
                                        "status":status.HTTP_400_BAD_REQUEST
                                    },status=status.HTTP_200_OK
                                )
                                
                            log_calculation_queryset = AdvanceLogs.objects.filter(advance_details=advance_queryset.pk,is_cancelled=False)
                            
                            updated_redeem_amount = 0
                            updated_redeem_weight = 0
                            
                            for update_calculation in log_calculation_queryset:
                                
                                updated_redeem_amount += update_calculation.redeem_amount
                                updated_redeem_weight += update_calculation.redeem_weight
                                
                            if advance_queryset.total_advance_amount == updated_redeem_amount and advance_queryset.total_advance_weight == updated_redeem_weight :
                                
                                advance_update_data = {}
                                
                                advance_update_data['is_redeemed'] = True
                                
                                advance_update_serializer = AdvanceDetailsSerializer(advance_queryset,data=advance_update_data,partial=True)
                                
                                if advance_update_serializer.is_valid():
                                    
                                    advance_update_serializer.save()
                                    
                                else:
                                    
                                    transaction.set_rollback(True)
                                    
                                    return Response(
                                        {
                                            "data":advance_update_serializer.errors,
                                            "message":res_msg.not_create("Billing"),
                                            "status":status.HTTP_400_BAD_REQUEST
                                        },status=status.HTTP_200_OK
                                    )
                                    
                        else:
                            
                            transaction.set_rollback(True)
                            
                            return Response(
                                {
                                    "data":advance_serializer.errors,
                                    "message":res_msg.not_create("Billing"),
                                    "status":status.HTTP_400_BAD_REQUEST
                                },status=status.HTTP_200_OK
                            )
                            
                    chit_details = request_data.get('chit_details',[])
                    
                    for chit in chit_details:
                        
                        chit['payment_details'] = payment_details_serializer.data['id']
                        
                        chit_serializer = BillingChitDetailsSerializer(data=chit)
                        
                        if chit_serializer.is_valid():
                            
                            chit_serializer.save()
                            
                        else:
                            
                            transaction.set_rollback(True)
                            
                            return Response(
                                {
                                    "data":chit_serializer.errors,
                                    "message":res_msg.not_create("Billing"),
                                    "status":status.HTTP_400_BAD_REQUEST
                                },status=status.HTTP_200_OK
                            )
                            
                    suspense_details = request_data.get('suspense_details',[])
                
                    for suspense in suspense_details :
                        
                        suspense_data = {}
                        
                        suspense_data['payment_details'] = payment_details_serializer.data['id']
                        suspense_data['suspense_details'] = suspense
                        
                        suspense_serializer = BillingSuspenseDetailsSerializer(data=suspense_data)
                        
                        if suspense_serializer.is_valid():
                            
                            suspense_serializer.save()
                            
                            try:
                            
                                suspense_queryset = SuspenseDetails.objects.get(id=suspense)
                                
                            except SuspenseDetails.DoesNotExist:
                                transaction.set_rollback(True)
                                return Response(
                                    {
                                        "message":res_msg.not_exists("Suspense"),
                                        "status":status.HTTP_404_NOT_FOUND
                                    },status=status.HTTP_200_OK
                                )
                                
                            except Exception as err:
                                transaction.set_rollback(True)
                                return Response(
                                    {
                                        "data":str(err),
                                        "status":status.HTTP_204_NO_CONTENT
                                    },status=status.HTTP_200_OK
                                )
                                
                            if suspense_queryset.is_redeemed == True:
                                transaction.set_rollback(True)
                                return Response(
                                    {
                                        "message":"The Suspense"+str(suspense_queryset.suspense_id)+"is already used",
                                        "status":status.HTTP_204_NO_CONTENT
                                    },status=status.HTTP_200_OK
                                )
                            if suspense_queryset.is_cancelled== True:
                                transaction.set_rollback(True)
                                return Response(
                                    {
                                        "message":"The Suspense"+str(suspense_queryset.suspense_id)+"is already Cancelled",
                                        "status":status.HTTP_204_NO_CONTENT
                                    },status=status.HTTP_200_OK
                                )
                                
                            suspense_item_queryset = SuspenseItemDetails.objects.filter(suspense_details=suspense_queryset.pk)
                            
                            total_amount = 0.0
                            
                            for items in suspense_item_queryset:
                                
                                total_amount += items.total_amount
                                
                            suspense_update_data = {}
                            suspense_update_data['is_redeemed'] = True
                            suspense_update_data['bill_number'] = serializer.data['bill_id']
                                
                            suspense_update_serializer = SuspenseDetailsSerializer(suspense_queryset,data=suspense_update_data,partial=True)
                            
                            if suspense_update_serializer.is_valid():
                                
                                suspense_update_serializer.save()
                                
                                suspense_customer_ledger_data = {}
                            
                                suspense_customer_ledger_data['customer_details'] = suspense_queryset.customer_details.pk
                                suspense_customer_ledger_data['entry_date'] = timezone.now()
                                suspense_customer_ledger_data['entry_type'] = settings.SUSPENSE_ENTRY
                                suspense_customer_ledger_data['transaction_type'] = settings.CREDIT_ENTRY
                                suspense_customer_ledger_data['invoice_number'] = serializer.data['bill_id']
                                suspense_customer_ledger_data['reffrence_number'] = suspense_queryset.suspense_id
                                suspense_customer_ledger_data['transaction_amount'] = total_amount
                                suspense_customer_ledger_data['transaction_weight'] = 0.0
                                suspense_customer_ledger_data['branch'] = branch
                                
                                suspense_customer_ledger_serializer = CustomerLedgerSerializer(data=suspense_customer_ledger_data)
                                
                                if suspense_customer_ledger_serializer.is_valid():
                                    
                                    suspense_customer_ledger_serializer.save()
                                    
                                else:
                                    
                                    transaction.set_rollback(True)
                                    return Response(
                                        {
                                            "data":suspense_customer_ledger_serializer.errors,
                                            "message":res_msg.not_create("Bill Payment"),
                                            "status":status.HTTP_400_BAD_REQUEST
                                        },status=status.HTTP_200_OK
                                    )
                                
                            else:
                                
                                transaction.set_rollback(True)
                                return Response(
                                    {
                                        "data":suspense_update_serializer.errors,
                                        "message":res_msg.not_create("bill payment"),
                                        "status":status.HTTP_400_BAD_REQUEST
                                    },status=status.HTTP_200_OK
                                )
                            
                        else:
                            
                            transaction.set_rollback(True)
                            
                            return Response(
                                {
                                    "data":suspense_serializer.errors,
                                    "message":res_msg.not_create("Bill Payment"),
                                    "status":status.HTTP_400_BAD_REQUEST
                                },status=status.HTTP_200_OK
                            )
                            
                    total_denomination = 0
                    total_exchange = 0
                    total_advance = 0
                    total_chit = 0
                    total_suspense = 0
                    
                    denomination_queryset = BillPaymentDenominationDetails.objects.filter(payment_details=payment_details_serializer.data['id'])
                    
                    for denomination in denomination_queryset:
                        
                        total_denomination += denomination.paid_amount
                        
                        
                    exchange_queryset = BillingExchangeDetails.objects.filter(payment_details=payment_details_serializer.data['id'])
                    
                    for exchange_amount in exchange_queryset:
                        
                        total_exchange += exchange_amount.old_purchase_details.old_gold_amount
                        
                    advance_amount_queryset = BillingAdvanceDetails.objects.filter(payment_details=payment_details_serializer.data['id'])
                    
                    for advance_amount in advance_amount_queryset:
                        
                        total_advance += advance_amount.total_amount
                        
                    chit_queryset = BillingChitDetails.objects.filter(payment_details=payment_details_serializer.data['id'])
                    
                    for chit_amount in chit_queryset:
                        
                        total_chit += chit_amount.total_amount
                        
                        
                    suspense_amount_queryset = BillingSuspenseDetails.objects.filter(payment_details=payment_details_serializer.data['id'])
                
                    for suspense_amount in suspense_amount_queryset:
                        
                        suspense_item_amount_queryset = SuspenseItemDetails.objects.filter(suspense_details=suspense_amount.suspense_details.pk)
                        
                        for suspense_item in suspense_item_amount_queryset:
                            
                            total_suspense += suspense_item.total_amount
                            
                    total_amount = total_denomination + total_exchange + total_advance + total_chit+total_suspense
                        
                    
                    total_customer_ledger_data={}
                    
                    total_customer_ledger_data['customer_details'] = serializer.data['customer_details']
                    total_customer_ledger_data['entry_date'] = timezone.now()
                    total_customer_ledger_data['entry_type'] = settings.SALES_ENTRY
                    total_customer_ledger_data['transaction_type'] = settings.DEBIT_ENTRY
                    total_customer_ledger_data['invoice_number'] = serializer.data['bill_id']
                    total_customer_ledger_data['reffrence_number'] = payment_details_serializer.data['payment_id']
                    total_customer_ledger_data['transaction_amount'] = total_amount
                    total_customer_ledger_data['transaction_weight'] = 0.0
                    total_customer_ledger_data['branch'] = branch
                    
                    total_customer_ledger_serializer = CustomerLedgerSerializer(data=total_customer_ledger_data)
                    
                    if total_customer_ledger_serializer.is_valid():
                        
                        total_customer_ledger_serializer.save()
                        
                    else:
                        
                        transaction.set_rollback(True)
                        return Response(
                            {
                                "data":total_customer_ledger_serializer.errors,
                                "message":res_msg.not_create("Billing"),
                                "status":status.HTTP_400_BAD_REQUEST
                            },status=status.HTTP_200_OK
                        )
                    
                else:
                    transaction.set_rollback(True)
                    return Response(
                        {
                            "data":payment_details_serializer.errors,
                            "message":res_msg.not_create("Billing"),
                            "status":status.HTTP_400_BAD_REQUEST
                        },status=status.HTTP_200_OK
                    )
                

                billing_return_details=request.data.get('billing_return_details', [])
                
                if len(billing_return_details) != 0:
                    if request.data.get('sale_return_type') == settings.AUTOMATIC:
                        for return_items in billing_return_details:
                            
                            bill_item_queryset = BillingParticularDetails.objects.get(id=return_items)
                            
                            tag_queryset = TaggedItems.objects.get(id=bill_item_queryset.tag_details)
                            
                            billing_return_data={
                                'billing_details': serializer.data['id'],
                                'return_bill_details' : bill_item_queryset.billing_details.pk,
                                'return_items' : bill_item_queryset.pk,
                                'tag_number' : tag_queryset.tag_number,
                                'item_details': tag_queryset.item_details.item_details.pk,
                                'sub_item_details': tag_queryset.sub_item_details.pk,
                                'metal': tag_queryset.sub_item_details.metal.pk,
                                'net_weight':bill_item_queryset.net_weight,
                                'gross_weight':bill_item_queryset.gross_weight,
                                'tag_weight':tag_queryset.tag_weight,
                                'cover_weight':tag_queryset.cover_weight,
                                'loop_weight':tag_queryset.loop_weight,
                                'other_weight':tag_queryset.other_weight,
                                'pieces':bill_item_queryset.pieces,
                                'rate' : bill_item_queryset.rate,
                                'stone_rate' : bill_item_queryset.stone_amount,
                                'diamond_rate' : bill_item_queryset.diamond_amount,
                                'stock_type' : tag_queryset.sub_item_details.stock_type.pk,
                                'calculation_type' : tag_queryset.calculation_type.pk,
                                'tax_percent' : bill_item_queryset.gst_percent,
                                # 'additional_charges' : bill_item_queryset.additional_charges,
                                # 'total_stone_weight' : bill_item_queryset.total_stone_weight,
                                # 'total_diamond_weight' : bill_item_queryset.total_diamond_weight,
                                'wastage_percentage' : bill_item_queryset.wastage_percent,
                                'flat_wastage' : bill_item_queryset.flat_wastage,
                                'making_charge' : bill_item_queryset.making_charge_per_gram,
                                'flat_making_charge' : bill_item_queryset.flat_making_charge,
                                'gst' : bill_item_queryset.gst_amount,
                                'total_rate' : bill_item_queryset.payable_amount,
                                'without_gst_rate' : bill_item_queryset.rate,
                                'huid_rate':bill_item_queryset.huid_amount
                            }   
                            
                            if str(tag_queryset.calculation_type.pk) == settings.WEIGHTCALCULATION:

                                sub_wastage_queryset=SubItemWeightCalculation.objects.get(sub_item_details=tag_queryset.sub_item_details.pk)
                                billing_return_data['wastage_calculation_type'] = sub_wastage_queryset.making_charge_calculation.pk
                                billing_return_data['making_charge_calculation_type'] = sub_wastage_queryset.wastage_calculation.pk
                                
                            elif str(tag_queryset.calculation_type.pk) == settings.PERGRAMRATE:
                                billing_return_data['per_gram_weight_type'] = tag_queryset.per_gram_weight_type.pk

                            else:
                                billing_return_data['wastage_calculation_type'] = None
                                billing_return_data['making_charge_calculation_type'] = None
                                billing_return_data['per_gram_weight_type'] = None

                            return_serializer=BillingSaleReturnItemsSerializer(data=estimation_return_data)
                            if return_serializer.is_valid():
                                return_serializer.save()
                                
                                return_stone_queryset = BillingParticularStoneDetails.objects.filter(billing_details=bill_item_queryset.billing_details.pk,billing_item_details=bill_item_queryset.pk)

                                for return_stone in return_stone_queryset:
                                    stone_dict={}
                                    stone_dict['billing_details'] = serializer.data['id']
                                    stone_dict['billing_return_item'] = return_serializer.data['id']
                                    stone_dict['stone_name']=return_stone.stone_name.pk
                                    stone_dict['stone_pieces']=return_stone.stone_pieces
                                    stone_dict['stone_weight']=return_stone.stone_weight
                                    stone_dict['stone_weight_type']=return_stone.stone_weight_type.pk
                                    stone_dict['stone_rate']=return_stone.stone_amount
                                    stone_dict['stone_rate_type']=return_stone.stone_rate_type.pk
                                    stone_dict['include_stone_weight']=return_stone.include_stone_weight

                                    billing_return_stone_serializer=BillingReturnStoneDetailsSerializer(data=stone_dict)
                                    if billing_return_stone_serializer.is_valid():
                                        billing_return_stone_serializer.save()
                                    else:
                                        transaction.set_rollback(True)
                                        return Response(
                                            {
                                                "data":billing_return_stone_serializer.errors,
                                                "message":res_msg.not_create("Billing"),
                                                "status":status.HTTP_400_BAD_REQUEST
                                            },status=status.HTTP_200_OK
                                        )

                                return_diamond_queryset = BillingParticularsDiamondDetails.objects.filter(billing_details=bill_item_queryset.billing_details.pk,billing_item_details=bill_item_queryset.pk)

                                for return_diamond in return_diamond_queryset:
                                    diamond_dict={}
                                    diamond_dict['billing_details'] = estimation_details['id']
                                    diamond_dict['billing_return_item'] = return_serializer.data['id']
                                    diamond_dict['diamond_name'] = return_diamond.diamond_name.pk
                                    diamond_dict['diamond_pieces'] = return_diamond.diamond_pieces
                                    diamond_dict['diamond_weight'] = return_diamond.diamond_weight
                                    diamond_dict['diamond_weight_type'] = return_diamond.diamond_weight_type.pk
                                    diamond_dict['diamond_rate'] = return_diamond.diamond_amount
                                    diamond_dict['diamond_rate_type'] = return_diamond.diamond_rate_type.pk
                                    diamond_dict['include_diamond_weight'] = return_diamond.include_diamond_weight

                                    billing_return_diamond_serializer=BillingReturnDiamondDetailsSerializer(data=diamond_dict)
                                    if billing_return_diamond_serializer.is_valid():
                                        billing_return_diamond_serializer.save()
                                    else:
                                        transaction.set_rollback(True)
                                        return Response(
                                            {
                                                "data":billing_return_diamond_serializer.errors,
                                                "message":res_msg.not_create("Billing"),
                                                "status":status.HTTP_400_BAD_REQUEST
                                            },status=status.HTTP_200_OK
                                        )
                                
                            else:
                                transaction.set_rollback(True)
                                return Response(
                                    {
                                        "data":return_serializer.errors,
                                        "message":res_msg.not_create("Billing"),
                                        "status":status.HTTP_400_BAD_REQUEST
                                    },status=status.HTTP_200_OK
                                )
                    
                elif request.data.get('sale_return_type') == settings.MANUAL:
                    for return_items in billing_return_details:
                           
                        subitem_queryset = SubItem.objects.get(id=return_items.get('sub_item_details'))
                        
                        estimation_return_data={
                            'billing_details': serializer.data['id'],
                            'return_bill_details' : return_items.get('return_bill_details') if return_items.get('return_bill_details') != '' else None,
                            'return_items' : return_items.get('return_items') if return_items.get('return_items') != '' else None,
                            'tag_number' : return_items.get('tag_number') if return_items.get('tag_number') != '' else None,
                            'item_details': return_items.get('item_details'),
                            'sub_item_details': return_items.get('sub_item_details'),
                            'metal': subitem_queryset.metal.pk,
                            'net_weight':return_items.get('net_weight'),
                            'gross_weight':return_items.get('gross_weight'),
                            'tag_weight':return_items.get('tag_weight'),
                            'cover_weight':return_items.get('cover_weight'),
                            'loop_weight':return_items.get('loop_weight'),
                            'other_weight': return_items.get('other_weight'),
                            'pieces': return_items.get('pieces'),
                            'total_pieces': return_items.get('total_pieces'),
                            'rate' : return_items.get('rate'),
                            'stone_rate' : return_items.get('stone_rate'),
                            'diamond_rate' : return_items.get('diamond_rate'),
                            'stock_type' : subitem_queryset.stock_type.pk,
                            'calculation_type' : subitem_queryset.calculation_type.pk,
                            # 'tax_percent' : return_items.get('tax_percent'),
                            'additional_charges' : return_items.get('additional_charges'),
                            'total_stone_weight' : return_items.get('total_stone_weight'),
                            'total_diamond_weight' : return_items.get('total_diamond_weight'),
                            'wastage_percentage' : return_items.get('wastage_percent',None),
                            'flat_wastage' : return_items.get('flat_wastage',None),
                            'making_charge' : return_items.get('making_charge',None),
                            'flat_making_charge' : return_items.get('flat_making_charge',None),
                            'gst' : return_items.get('gst'),
                            'total_rate' : return_items.get('total_rate'),
                            'without_gst_rate' : return_items.get('without_gst_rate'),
                            'huid_rate': return_items.get('huid_rate'),
                        }   

                        if str(subitem_queryset.calculation_type.pk) == settings.WEIGHTCALCULATION:
                            subitem_weight_queryset=SubItemWeightCalculation.objects.get(sub_item_details=subitem_queryset.pk)

                            estimation_return_data['wastage_calculation_type'] = subitem_weight_queryset.wastage_calculation.pk
                            estimation_return_data['making_charge_calculation_type'] = subitem_weight_queryset.making_charge_calculation.pk
                            
                        elif str(subitem_queryset.calculation_type.pk) == settings.PERGRAMRATE:
                            subitem_weight_queryset=SubItemPerGramRate.objects.get(sub_item_details=subitem_queryset.pk)

                            estimation_return_data['per_gram_weight_type'] = subitem_weight_queryset.per_gram_weight_type.pk

                            try:
                                tax_queryset = TaxDetailsAudit.objects.filter(metal=subitem_queryset.metal.pk).order_by('-id').first()
                                if tax_queryset:
                                    tax_percent_queryset = SalesTaxDetails.objects.get(tax_details=tax_queryset.tax_details)
                                    if return_items.get('gst_type') == settings.INTRA_STATE_GST:
                                        estimation_return_data['tax_percent'] = tax_percent_queryset.sales_tax_cgst + tax_percent_queryset.sales_tax_sgst
                                    elif return_items.get('gst_type') == settings.INTER_STATE_GST:
                                        estimation_return_data['tax_percent'] = tax_percent_queryset.sales_tax_igst
                            except Exception as err:
                                estimation_return_data['tax_percent'] = 0

                            return_serializer=BillingSaleReturnItemsSerializer(data=estimation_return_data)
                            if return_serializer.is_valid():
                                return_serializer.save()
                            else:
                                transaction.set_rollback(True)
                                return Response(
                                    {
                                        "data":return_serializer.errors,
                                        "message":res_msg.not_create("Billing"),
                                        "status":status.HTTP_400_BAD_REQUEST
                                    },status=status.HTTP_200_OK
                                )

            return Response(
                {
                    "data":serializer.data,
                    "message":res_msg.create("Billing"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
            
        else:
            return Response(
                {
                    "data":serializer.errors,
                    "message":res_msg.not_create("Billing"),
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
               
            queryset = BillingDetails.objects.get(id=pk)
           
            serializer = BillingDetailsSerializer(queryset)
           
            res_data = serializer.data
           
            res_data['customer_name'] = queryset.customer_details.customer_name
            res_data['customer_mobile'] = queryset.customer_details.phone
            res_data['street'] = queryset.customer_details.street_name
            res_data['country'] = queryset.customer_details.country
            res_data['state'] = queryset.customer_details.state
            res_data['pincode'] = queryset.customer_details.pincode
           
            particular_queryset = BillingParticularDetails.objects.filter(billing_details=queryset.pk)
           
            particular_details = []
           
            for particulars in particular_queryset:
               
                particular_serializer = BillingParticularDetailsSerializer(particulars)
               
                particular_data = particular_serializer.data
               
                particular_data['tag_number'] = particulars.tag_details.tag_number
                particular_data['sub_item_details_name'] = particulars.tag_details.sub_item_details.sub_item_name
                particular_data['item_details_name'] = particulars.tag_details.sub_item_details.item_details.item_name
                particular_data['purity_name'] = particulars.tag_details.sub_item_details.item_details.purity.purity_name
                particular_data['metal_name'] = particulars.tag_details.sub_item_details.item_details.purity.metal.metal_name
                particular_data['vendor_name'] = particulars.tag_details.tag_entry_details.lot_details.designer_name.account_head_name
               
                particular_details.append(particular_data)
               
            res_data['particular_details'] = particular_details
               
            payment_details = []
           
            total_denomination_amount = 0.0
            total_exchange_amount = 0.0
            total_advance_amount = 0.0
            total_chit_amount = 0.0
            total_suspense_amount = 0.0
               
            payment_queryset = BillingPaymentDetails.objects.filter(billing_details=queryset.pk)
           
            for payment in payment_queryset:
               
                payment_serializer = BillingPaymentDetailsSerializer(payment)
               
                payment_data = payment_serializer.data
               
                denomination_amount = 0.0
                exchange_amount = 0.0
                advance_amount = 0.0
                chit_amount = 0.0
                suspense_amount = 0.0
               
                denomination_queryset = BillPaymentDenominationDetails.objects.filter(payment_details=payment.pk)
               
                denomination_details = []
               
                for denomination in denomination_queryset:
                   
                    denomination_amount += denomination.paid_amount
                   
                    denomination_serializer = BillingPaymentDenominationSerializer(denomination)
                   
                    denomination_data = denomination_serializer.data
                   
                    denomination_details.append(denomination_data)
                   
                payment_data['denomination_details'] = denomination_details
                   
                exhcange_queryset = BillingExchangeDetails.objects.filter(payment_details=payment.pk)
               
                exchange_details = []
               
                for exchange in exhcange_queryset:
                   
                    exchange_amount += exchange.old_purchase_details.old_gold_amount
                   
                    exchange_data = {}
                   
                    exchange_data['old_bill_number'] = exchange.old_purchase_details.old_gold_bill_number
                    exchange_data['old_gold_pieces'] = exchange.old_purchase_details.old_gold_pieces
                    exchange_data['old_gold_weight'] = exchange.old_purchase_details.old_gold_weight
                    exchange_data['old_gold_amount'] = exchange.old_purchase_details.old_gold_amount
                   
                    exchange_details.append(exchange_data)
                   
                payment_data['exchange_details'] = exchange_details
               
                advance_queryset = BillingAdvanceDetails.objects.filter(payment_details=payment.pk)
               
                advance_details = []
               
                for advance in advance_queryset:
                   
                    advance_amount += advance.total_amount
                   
                    advance_serializer = BillingAdvanceDetailsSerializer(advance)
                   
                    advance_data = advance_serializer.data
                   
                    advance_data['advance_id'] = advance.advance_details.advance_id
                   
                    advance_details.append(advance_data)
                   
                payment_data['advance_details'] = advance_details
               
                chit_queryset = BillingChitDetails.objects.filter(payment_details=payment.pk)
               
                chit_details = []
               
                for chit in chit_queryset:
                   
                    chit_amount += chit.total_amount
                   
                    chit_serializer = BillingChitDetailsSerializer(chit)
                   
                    chit_data = chit_serializer.data
                   
                    chit_details.append(chit_data)
                   
                payment_data['chit_details'] = chit_details
               
                suspense_queryset = BillingSuspenseDetails.objects.filter(payment_details=payment.pk)
               
                suspense_details = []
               
                for suspense in suspense_queryset:
                   
                    suspense_data = {}
                   
                    suspense_data['suspense_id'] = suspense.suspense_details.suspense_id
                   
                    item_details = []
                   
                    suspense_total_amount = 0.0
                   
                    suspense_item_queryset = SuspenseItemDetails.objects.filter(suspense_details=suspense.suspense_details.pk)
                   
                    for item in suspense_item_queryset:
                       
                        suspense_total_amount += item.total_amount
                       
                        item_data = {}
                       
                        item_data['metal_name'] = item.metal_details.metal_name
                        item_data['metal_weight'] = item.metal_weight
                        item_data['metal_amount'] = item.metal_amount
                        item_data['total_amount'] = item.total_amount
                       
                        item_details.append(item_data)
                       
                    suspense_data['suspense_total_amount'] = suspense_total_amount
                    suspense_data['item_details'] = item_details
                   
                    suspense_amount += suspense_total_amount
                   
                    suspense_details.append(suspense_data)
                   
                payment_data['suspense_details'] = suspense_details
               
               
                payment_data['denomination_amount'] = denomination_amount
                payment_data['exchange_amount'] = exchange_amount
                payment_data['advance_amount'] = advance_amount
                payment_data['chit_amount'] = chit_amount
                payment_data['suspense_amount'] = suspense_amount
 
               
                total_denomination_amount += denomination_amount
                total_exchange_amount += exchange_amount
                total_advance_amount += advance_amount
                total_chit_amount += chit_amount
                total_suspense_amount += suspense_amount
               
                payment_details.append(payment_data)
               
            res_data['payment_details'] = payment_details
           
           
            res_data['total_denomination_amount'] = total_denomination_amount
            res_data['total_exchange_amount'] = total_exchange_amount
            res_data['total_advance_amount'] = total_advance_amount
            res_data['total_suspense_amount'] = total_suspense_amount
           
            paid_amount = total_denomination_amount+total_exchange_amount+total_advance_amount+total_suspense_amount
           
            res_data['paid_amount'] = paid_amount
           
            balance_amount = queryset.payable_amount - paid_amount
           
            res_data['balance_amount']=balance_amount
           
            return Response(
                {
                    "data":res_data,
                    "message":res_msg.retrieve("Billing Details"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
           
        except BillingDetails.DoesNotExist:
           
            return Response(
                {
                    "message":res_msg.not_exists("Billing Details"),
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
class BillPaymentView(APIView):
    @transaction.atomic
    def post(self,request):
    
        try:
            
            pk = request.data.get('id',None)
            
            if pk == None:
                
                return Response(
                    {
                        "message":res_msg.missing_fields("ID"),
                        "status":status.HTTP_204_NO_CONTENT
                    },status=status.HTTP_200_OK
                )
                    
            request_data = request.data
                
            queryset = BillingDetails.objects.get(id=pk)
            
            payment_details_data = {}
            payment_details_data['billing_details'] = queryset.pk
            payment_details_data['payment_date'] = timezone.now()
            payment_details_data['created_by'] = request.user.id

            if request.user.role.is_admin == True:
                branch = request_data.get('branch')
            else:
                branch = request.user.branch.pk

            payment_details_data['branch'] = branch

            pay_id = True

            while pay_id ==True:
                
                random_number = random.randint(100, 9999999)
                
                generated_number = "BPMT"+str(random_number)
                
                try:
                
                    bill_number_queryset = BillingPaymentDetails.objects.get(payment_id=generated_number)
                    pay_id = True
                except BillingPaymentDetails.DoesNotExist:
                    payment_details_data['payment_id'] = generated_number
                    pay_id=False
                    
                except Exception  as err:
                    transaction.set_rollback(True)
                    return Response(
                        {
                            "data":str(err),
                            "message":res_msg.something_else(),
                            "status":status.HTTP_204_NO_CONTENT
                        },status=status.HTTP_200_OK
                    )
                    
            payment_details_serializer = BillingPaymentDetailsSerializer(data=payment_details_data)
            
            if payment_details_serializer.is_valid():
                
                payment_details_serializer.save()
                
                payment_denomination_details = request_data.get('payment_denomination_details',[])
                
                for denominations in payment_denomination_details:
                    
                    denominations['payment_details'] = payment_details_serializer.data['id']
                    
                    denomination_serializer = BillingPaymentDenominationSerializer(data=denominations)
                    
                    if denomination_serializer.is_valid():
                        
                        denomination_serializer.save()
                        
                    else:
                        
                        transaction.set_rollback(True)
                        
                        return Response(
                            {
                                "data":denomination_serializer.errors,
                                "message":res_msg.not_create("Billing"),
                                "status":status.HTTP_400_BAD_REQUEST
                            },status=status.HTTP_200_OK
                        )
                        
                exchange_details = request_data.get('exchange_details',[])
                
                for exchange in  exchange_details:
                    
                    exchange_data = {}
                    
                    exchange_data['payment_details'] = payment_details_serializer.data['id']
                    exchange_data['old_purchase_details'] = exchange
                    
                    exchange_serializer = BillingExchangeDetailsSerializer(data=exchange_data)
                    
                    if exchange_serializer.is_valid():
                        
                        exchange_serializer.save()
                        
                        old_bill_queryset = OldGoldBillDetails.objects.get(id=exchange_serializer.data['old_purchase_details'])
                        
                        if old_bill_queryset.is_canceled == True:
                            transaction.set_rollback(True)
                            return Response(
                                {
                                    "message":str(old_bill_queryset.old_gold_bill_number)+"is already cancelled",
                                    "status":status.HTTP_204_NO_CONTENT
                                },status=status.HTTP_200_OK
                            )
                            
                        if old_bill_queryset.is_billed == True:
                            transaction.set_rollback(True)
                            return Response(
                                {
                                    "message":str(old_bill_queryset.old_gold_bill_number)+"is Already Billed",
                                    "status":status.HTTP_204_NO_CONTENT
                                },status=status.HTTP_200_OK
                            )
                        
                        old_bill_update_data = {}
                        
                        old_bill_update_data['is_billed'] = True
                        old_bill_update_data['refference_number'] = queryset.bill_id
                        
                        old_bill_update_serializer = OldGoldBillDetailsSerializer(old_bill_queryset,data=old_bill_update_data,partial=True)
                        
                        if old_bill_update_serializer.is_valid():
                            
                            old_bill_update_serializer.save()
                            
                            exchange_customer_ledger_data = {}
                        
                            exchange_customer_ledger_data['customer_details'] = old_bill_queryset.customer_details.pk
                            exchange_customer_ledger_data['entry_date'] = timezone.now()
                            exchange_customer_ledger_data['entry_type'] = settings.OLD_PURCHASE_ENTRY
                            exchange_customer_ledger_data['transaction_type'] = settings.CREDIT_ENTRY
                            exchange_customer_ledger_data['invoice_number'] = queryset.bill_id
                            exchange_customer_ledger_data['reffrence_number'] = str(old_bill_queryset.old_gold_bill_number)
                            exchange_customer_ledger_data['transaction_amount'] = old_bill_queryset.old_gold_amount
                            exchange_customer_ledger_data['transaction_weight'] = 0.0
                            exchange_customer_ledger_data['branch'] = branch
                            
                            exchange_customer_ledger_serializer = CustomerLedgerSerializer(data=exchange_customer_ledger_data)
                            
                            if exchange_customer_ledger_serializer.is_valid():
                                
                                exchange_customer_ledger_serializer.save()
                                
                            else:
                                
                                transaction.set_rollback(True)
                                
                                return Response(
                                    {
                                        "data":exchange_customer_ledger_serializer.errors,
                                        "message":res_msg.not_create("Billing"),
                                        "status":status.HTTP_400_BAD_REQUEST
                                    },status=status.HTTP_200_OK
                                )
                            
                        else:
                            transaction.set_rollback(True)
                            return Response(
                                {
                                    "data":old_bill_update_serializer.errors,
                                    "message":res_msg.not_create("Billing"),
                                    "status":status.HTTP_400_BAD_REQUEST
                                },status=status.HTTP_200_OK
                            )
                        
                    else:
                        transaction.set_rollback(True)
                        return Response(
                            {
                                "data":exchange_serializer.errors,
                                "message":res_msg.not_create("Billing"),
                                "stauts":status.HTTP_400_BAD_REQUEST
                            },status=status.HTTP_200_OK
                        )
                
                advance_details = request_data.get('advance_details',[])
                
                for advance in advance_details:
                    
                    advance['payment_details'] = payment_details_serializer.data['id']
                    
                    advance_serializer = BillingAdvanceDetailsSerializer(data=advance)
                    
                    if advance_serializer.is_valid():
                        
                        advance_serializer.save()
                            
                        advance_queryset = AdvanceDetails.objects.get(id=advance_serializer.data['advance_details'])
                        
                        if advance_queryset.is_cancelled == True:
                            
                            transaction.set_rollback(True)
                            
                            return Response(
                                {
                                    "message":str(advance_queryset.advance_id)+"Advance is already cancelled",
                                    "status":status.HTTP_204_NO_CONTENT
                                },status=status.HTTP_200_OK
                            )
                            
                        
                        if advance_queryset.is_redeemed == True:
                            
                            transaction.set_rollback(True)
                            return Response(
                                {
                                    "message":str(advance_queryset.advance_id)+"Advance is already redeemed",
                                    "status":status.HTTP_204_NO_CONTENT
                                },status=status.HTTP_200_OK
                            )
                            
                        redeem_amount = 0
                        redeem_weight = 0
                            
                        advance_log_queryset = AdvanceLogs.objects.filter(advance_details=advance_queryset.pk,is_cancelled=False)
                        
                        for logs in advance_log_queryset:
                            
                            redeem_amount += logs.redeem_amount
                            redeem_weight += logs.redeem_weight
                            
                        remaining_weight = advance_queryset.total_advance_weight - redeem_weight
                        remaining_amount = advance_queryset.total_advance_amount - redeem_amount
                        
                        advance_log_update_data = {}
                        
                        advance_log_update_data['advance_details'] = advance_queryset.pk
                        
                        advance_log_update_data['redeem_weight'] = advance_serializer.data['redeem_weight']
                        advance_log_update_data['redeem_amount'] = advance_serializer.data['redeem_amount']
                        
                        if remaining_weight < advance_serializer.data['redeem_weight'] or remaining_amount < advance_serializer.data['redeem_amount']:
                            
                            transaction.set_rollback(True)
                            return Response(
                                {
                                    "message":"for advance"+str(advance_queryset.advance_id)+"remaining weight is"+str(remaining_weight)+"remaining amount is"+str(remaining_amount),
                                    "status":status.HTTP_204_NO_CONTENT
                                },status=status.HTTP_200_OK
                            )
                            
                        advance_log_update_serializer = AdvanceLogsSerializer(data=advance_log_update_data)
                        
                        if advance_log_update_serializer.is_valid():
                            
                            advance_log_update_serializer.save()
                            
                            advance_customer_ledger_data = {}
                        
                            advance_customer_ledger_data['customer_details'] = advance_queryset.customer_details.pk
                            advance_customer_ledger_data['entry_date'] = timezone.now()
                            advance_customer_ledger_data['entry_type'] = settings.ADVANCE_ENTRY
                            advance_customer_ledger_data['transaction_type'] = settings.CREDIT_ENTRY
                            advance_customer_ledger_data['invoice_number'] = queryset.bill_id
                            advance_customer_ledger_data['reffrence_number'] = advance_queryset.advance_id
                            advance_customer_ledger_data['transaction_amount'] = advance_log_update_serializer.data['redeem_amount']
                            advance_customer_ledger_data['transaction_weight'] = advance_log_update_serializer.data['redeem_weight']
                            advance_customer_ledger_data['branch'] = branch
                            
                            advance_customer_ledger_serializer = CustomerLedgerSerializer(data=advance_customer_ledger_data)
                            
                            if advance_customer_ledger_serializer.is_valid():
                                
                                advance_customer_ledger_serializer.save()
                                
                            else:
                                
                                transaction.set_rollback(True)
                                return Response(
                                    {
                                        "data":advance_customer_ledger_serializer.errors,
                                        "message":res_msg.not_create("Billing"),
                                        "status":status.HTTP_400_BAD_REQUEST
                                    },status=status.HTTP_200_OK
                                )
                            
                        else:
                            transaction.set_rollback(True)
                            return Response(
                                {
                                    "data":advance_log_update_serializer.errors,
                                    "message":res_msg.not_create("Billing"),
                                    "status":status.HTTP_400_BAD_REQUEST
                                },status=status.HTTP_200_OK
                            )
                            
                        log_calculation_queryset = AdvanceLogs.objects.filter(advance_details=advance_queryset.pk,is_cancelled=False)
                        
                        updated_redeem_amount = 0
                        updated_redeem_weight = 0
                        
                        for update_calculation in log_calculation_queryset:
                            
                            updated_redeem_amount += update_calculation.redeem_amount
                            updated_redeem_weight += update_calculation.redeem_weight
                            
                        if advance_queryset.total_advance_amount == updated_redeem_amount and advance_queryset.total_advance_weight == updated_redeem_weight :
                            
                            advance_update_data = {}
                            
                            advance_update_data['is_redeemed'] = True
                            
                            advance_update_serializer = AdvanceDetailsSerializer(advance_queryset,data=advance_update_data,partial=True)
                            
                            if advance_update_serializer.is_valid():
                                
                                advance_update_serializer.save()
                                
                            else:
                                
                                transaction.set_rollback(True)
                                
                                return Response(
                                    {
                                        "data":advance_update_serializer.errors,
                                        "message":res_msg.not_create("Billing"),
                                        "status":status.HTTP_400_BAD_REQUEST
                                    },status=status.HTTP_200_OK
                                )
                       
                    else:
                        
                        transaction.set_rollback(True)
                        
                        return Response(
                            {
                                "data":advance_serializer.errors,
                                "message":res_msg.not_create("Billing"),
                                "status":status.HTTP_400_BAD_REQUEST
                            },status=status.HTTP_200_OK
                        )
                        
                chit_details = request_data.get('chit_details',[])
                
                for chit in chit_details:
                    
                    chit['payment_details'] = payment_details_serializer.data['id']
                    
                    chit_serializer = BillingChitDetailsSerializer(data=chit)
                    
                    if chit_serializer.is_valid():
                        
                        chit_serializer.save()
                        
                    else:
                        
                        transaction.set_rollback(True)
                        
                        return Response(
                            {
                                "data":chit_serializer.errors,
                                "message":res_msg.not_create("Billing"),
                                "status":status.HTTP_400_BAD_REQUEST
                            },status=status.HTTP_200_OK
                        )
                        
                suspense_details = request_data.get('suspense_details',[])
                
                for suspense in suspense_details :
                    
                    suspense_data = {}
                    
                    suspense_data['payment_details'] = payment_details_serializer.data['id']
                    suspense_data['suspense_details'] = suspense
                    
                    suspense_serializer = BillingSuspenseDetailsSerializer(data=suspense_data)
                    
                    if suspense_serializer.is_valid():
                        
                        suspense_serializer.save()
                        
                        try:
                        
                            suspense_queryset = SuspenseDetails.objects.get(id=suspense)
                            
                        except SuspenseDetails.DoesNotExist:
                            transaction.set_rollback(True)
                            return Response(
                                {
                                    "message":res_msg.not_exists("Suspense"),
                                    "status":status.HTTP_404_NOT_FOUND
                                },status=status.HTTP_200_OK
                            )
                            
                        except Exception as err:
                            transaction.set_rollback(True)
                            return Response(
                                {
                                    "data":str(err),
                                    "status":status.HTTP_204_NO_CONTENT
                                },status=status.HTTP_200_OK
                            )
                            
                        if suspense_queryset.is_redeemed == True:
                            transaction.set_rollback(True)
                            return Response(
                                {
                                    "message":"The Suspense"+str(suspense_queryset.suspense_id)+"is already used",
                                    "status":status.HTTP_204_NO_CONTENT
                                },status=status.HTTP_200_OK
                            )
                        if suspense_queryset.is_cancelled== True:
                            transaction.set_rollback(True)
                            return Response(
                                {
                                    "message":"The Suspense"+str(suspense_queryset.suspense_id)+"is already Cancelled",
                                    "status":status.HTTP_204_NO_CONTENT
                                },status=status.HTTP_200_OK
                            )
                            
                        suspense_item_queryset = SuspenseItemDetails.objects.filter(suspense_details=suspense_queryset.pk)
                        
                        total_amount = 0.0
                        
                        for items in suspense_item_queryset:
                            
                            total_amount += items.total_amount
                            
                        suspense_update_data = {}
                        suspense_update_data['is_redeemed'] = True
                        suspense_update_data['bill_number'] = queryset.bill_id
                            
                        suspense_update_serializer = SuspenseDetailsSerializer(suspense_queryset,data=suspense_update_data,partial=True)
                        
                        if suspense_update_serializer.is_valid():
                            
                            suspense_update_serializer.save()
                            
                            suspense_customer_ledger_data = {}
                        
                            suspense_customer_ledger_data['customer_details'] = suspense_queryset.customer_details.pk
                            suspense_customer_ledger_data['entry_date'] = timezone.now()
                            suspense_customer_ledger_data['entry_type'] = settings.SUSPENSE_ENTRY
                            suspense_customer_ledger_data['transaction_type'] = settings.CREDIT_ENTRY
                            suspense_customer_ledger_data['invoice_number'] = queryset.bill_id
                            suspense_customer_ledger_data['reffrence_number'] = suspense_queryset.suspense_id
                            suspense_customer_ledger_data['transaction_amount'] = total_amount
                            suspense_customer_ledger_data['transaction_weight'] = 0.0
                            suspense_customer_ledger_data['branch'] = branch
                                    
                            suspense_customer_ledger_serializer = CustomerLedgerSerializer(data=suspense_customer_ledger_data)
                            
                            if suspense_customer_ledger_serializer.is_valid():
                                
                                suspense_customer_ledger_serializer.save()
                                
                            else:
                                
                                transaction.set_rollback(True)
                                return Response(
                                    {
                                        "data":suspense_customer_ledger_serializer.errors,
                                        "message":res_msg.not_create("Bill Payment"),
                                        "status":status.HTTP_400_BAD_REQUEST
                                    },status=status.HTTP_200_OK
                                )
                            
                        else:
                            
                            transaction.set_rollback(True)
                            return Response(
                                {
                                    "data":suspense_update_serializer.errors,
                                    "message":res_msg.not_create("bill payment"),
                                    "status":status.HTTP_400_BAD_REQUEST
                                },status=status.HTTP_200_OK
                            )
                        
                    else:
                        
                        transaction.set_rollback(True)
                        
                        return Response(
                            {
                                "data":suspense_serializer.errors,
                                "message":res_msg.not_create("Bill Payment"),
                                "status":status.HTTP_400_BAD_REQUEST
                            },status=status.HTTP_200_OK
                        )
                        
                total_denomination = 0
                total_exchange = 0
                total_advance = 0
                total_chit = 0
                total_suspense = 0
                
                denomination_queryset = BillPaymentDenominationDetails.objects.filter(payment_details=payment_details_serializer.data['id'])
                
                for denomination in denomination_queryset:
                    
                    total_denomination += denomination.paid_amount
                    
                    
                exchange_queryset = BillingExchangeDetails.objects.filter(payment_details=payment_details_serializer.data['id'])
                
                for exchange_amount in exchange_queryset:
                    
                    total_exchange += exchange_amount.old_purchase_details.old_gold_amount
                    
                advance_amount_queryset = BillingAdvanceDetails.objects.filter(payment_details=payment_details_serializer.data['id'])
                
                for advance_amount in advance_amount_queryset:
                    
                    total_advance += advance_amount.total_amount
                    
                chit_queryset = BillingChitDetails.objects.filter(payment_details=payment_details_serializer.data['id'])
                
                for chit_amount in chit_queryset:
                    
                    total_chit += chit_amount.total_amount
                    
                suspense_amount_queryset = BillingSuspenseDetails.objects.filter(payment_details=payment_details_serializer.data['id'])
                
                for suspense_amount in suspense_amount_queryset:
                    
                    suspense_item_amount_queryset = SuspenseItemDetails.objects.filter(suspense_details=suspense_amount.suspense_details.pk)
                    
                    for suspense_item in suspense_item_amount_queryset:
                        
                        total_suspense += suspense_item.total_amount
                        
                total_amount = total_denomination + total_exchange + total_advance + total_chit+total_suspense
                
                total_customer_ledger_data={}
                
                total_customer_ledger_data['customer_details'] = queryset.customer_details.pk
                total_customer_ledger_data['entry_date'] = timezone.now()
                total_customer_ledger_data['entry_type'] = settings.SALES_ENTRY
                total_customer_ledger_data['transaction_type'] = settings.DEBIT_ENTRY
                total_customer_ledger_data['invoice_number'] = queryset.bill_id
                total_customer_ledger_data['reffrence_number'] = payment_details_serializer.data['payment_id']
                total_customer_ledger_data['transaction_amount'] = total_amount
                total_customer_ledger_data['transaction_weight'] = 0.0
                total_customer_ledger_data['branch'] = branch
                
                total_customer_ledger_serializer = CustomerLedgerSerializer(data=total_customer_ledger_data)
                
                if total_customer_ledger_serializer.is_valid():
                    
                    total_customer_ledger_serializer.save()
                    
                else:
                    
                    transaction.set_rollback(True)
                    return Response(
                        {
                            "data":total_customer_ledger_serializer.errors,
                            "message":res_msg.not_create("Billing"),
                            "status":status.HTTP_400_BAD_REQUEST
                        },status=status.HTTP_200_OK
                    )
                
                return Response(
                    {
                        "data":payment_details_serializer.data,
                        "message":res_msg.create("Payment Details"),
                        "status":status.HTTP_200_OK
                    },status=status.HTTP_200_OK
                )
            
            else:
                transaction.set_rollback(True)
                return Response(
                    {
                        "data":payment_details_serializer.errors,
                        "message":res_msg.not_create("Billing"),
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
class BillingListView(APIView):
    def get(self,request):
        queryset = BillingDetails.objects.all().order_by('-id')

        serializer = BillingDetailsSerializer(queryset, many=True)

        return Response(
            {
                "data":{
                    "list":serializer.data,
                },
                "message":res_msg.retrieve("Billing Table List"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )

    def post(self,request):
                
        filter_condition = {}
        
        if request.user.role.is_admin == True:
            branch = request.data.get('branch')
        else:
            branch = request.user.branch.pk
                
        customer = request.data.get('customer',None)
        from_date = request.data.get('from_date',None)
        to_date = request.data.get('to_date',None)
        search = request.data.get('search',"")
        page = request.data.get('page',1)
        items_per_page = request.data.get('items_per_page',10)
        
        if customer != None:
            
            filter_condition['customer_details'] = customer
            
        if from_date != None and to_date != None:
            
            date_range = (from_date,to_date)
            
            filter_condition['bill_date__range'] = date_range
            
        if search != "":
            
            filter_condition['bill_id__icontains'] = search

        if branch != None:
            
            filter_condition['branch'] = branch
            
        if len(filter_condition) != 0 :
            
            queryset = BillingDetails.objects.filter(**filter_condition).order_by('-id')
            
        else:
            
            queryset = BillingDetails.objects.all().order_by('-id')
        
        paginated_data = Paginator(queryset, items_per_page)
        serializer = BillingDetailsSerializer(paginated_data.get_page(page), many=True)
        total_items = len(queryset)
        
        response_data = []
        
        for data in serializer.data:
            
            res_data = data
            
            bill_queryset = BillingDetails.objects.get(id=data['id'])
            
            res_data['customer_details_name'] = bill_queryset.customer_details.customer_name
            
            bill_payment_queryset = BillingPaymentDetails.objects.filter(billing_details=data['id'])
            
            paid_amount = 0.0
            
            for payments in bill_payment_queryset:
                
                
                denomination_queryset = BillPaymentDenominationDetails.objects.filter(payment_details=payments.pk)
                
                for denomination in denomination_queryset:
                    
                    paid_amount += denomination.paid_amount
                    
                exchange_queryset = BillingExchangeDetails.objects.filter(payment_details=payments.pk)
                
                for exchange in exchange_queryset:
                    
                    paid_amount += exchange.old_purchase_details.old_gold_amount
                    
                advance_queryset = BillingAdvanceDetails.objects.filter(payment_details=payments.pk)
                
                for advance in advance_queryset:
                    
                    paid_amount += advance.total_amount
                    
                chit_queryset = BillingChitDetails.objects.filter(payment_details=payments.pk)
                
                for chit in chit_queryset:
                    
                    paid_amount += chit.total_amount
                    
                suspense_queryset = BillingSuspenseDetails.objects.filter(payment_details=payments.pk)
                
                for suspense in suspense_queryset:
                    
                    total_amount = 0
                    
                    suspense_item_queryset = SuspenseItemDetails.objects.filter(suspense_details=suspense.suspense_details.pk)
                    
                    for item in suspense_item_queryset:
                        
                        total_amount += item.total_amount
                        
                    paid_amount += total_amount
                    
            res_data['paid_amount'] = paid_amount
            res_data['balance_amount'] = bill_queryset.payable_amount - paid_amount
            
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
                "message":res_msg.retrieve("Billing Table List"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )