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
from django.db import connection
from books.models import *
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
from approval.models import *
from approval.serializer import *
from accounts.models import *
from django.contrib.sessions.models import Session
from django.db import transaction

# Create your views here.
res_msg = ResponseMessages()

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class BackupGoldBillnumberView(APIView):  
    def get(self, request): 
        try:
            queryset=BackupBillID.objects.all().order_by('-id')[0]
            prefix = 'BILLBGD-00'
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
                    "bill_number":"BILLBGD-001",
                    "message":res_msg.retrieve("Bill Number"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
     
        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class BackupSilverBillnumberView(APIView):  
    def get(self, request): 
        try:
            queryset=BackupBillSilverBillID.objects.all().order_by('-id')[0]
            prefix = 'BILLBSV-00'
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
                    "bill_number":"BILLBSV-001",
                    "message":res_msg.retrieve("Bill Number"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class BillinBackupView(APIView):
    def get(self,reqeust,pk):

        try:

            queryset = BillingBackupDetails.objects.get(id=pk)
            
            res_data={}

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


            res_data['id']=queryset.pk
            res_data['bill_no']=queryset.bill_no
            res_data['bill_type']=queryset.bill_type.pk
            res_data['bill_type_name']=queryset.bill_type.bill_type
            res_data['bill_date']=queryset.bill_date
            res_data['bill_no']=queryset.bill_no
            res_data['total_amount']=queryset.total_amount
            res_data['gst_amount']=queryset.gst_amount
            res_data['advance_amount']=queryset.advance_amount
            res_data['chit_amount']=queryset.chit_amount
            res_data['discount_amount']=queryset.discount_amount
            res_data['exchange_amount']=queryset.exchange_amount
            res_data['payable_amount']=queryset.payable_amount
            res_data['cash_amount']=queryset.cash_amount
            res_data['card_amount']=queryset.card_amount
            res_data['account_transfer_amount']=queryset.account_transfer_amount
            res_data['upi_amount']=queryset.upi_amount
            res_data['paid_amount']=queryset.paid_amount
            res_data['billed_date']=queryset.created_at
            res_data['created_by']=queryset.created_by.pk
            try:

                bill_items = BillingBackupTagItems.objects.filter(billing_details=queryset.pk)

                billing_item_details=[]

                for items in bill_items:

                    item_dict={}

                    item_dict['id']=items.pk
                    item_dict['diamond_rate']=items.diamond_rate
                    item_dict['flat_making_charge']=items.flat_making_charge
                    item_dict['gross_weight']=items.gross_weight
                    item_dict['item_details']=items.item_details.pk
                    item_dict['item']=items.item_details.item_name
                    item_dict['jewel_type']=items.metal.metal_name
                    item_dict['loop_weight']=items.loop_weight
                    item_dict['cover_weight']=items.cover_weight
                    item_dict['cover_weight']=items.cover_weight
                    item_dict['making_charge']=items.making_charge
                    item_dict['metal']=items.metal.pk
                    item_dict['metal_rate']=items.rate
                    item_dict['net_weight']=items.net_weight
                    item_dict['other_weight']=items.other_weight
                    item_dict['pieces']=items.pieces
                    item_dict['rate']=items.without_gst_rate
                    item_dict['stock_type']=items.stock_type.pk
                    item_dict['stock_type_name']=items.stock_type.stock_type_name
                    item_dict['calculation_type']=items.calculation_type.pk
                    item_dict['calculation_type_name']=items.calculation_type.calculation_name
                    item_dict['stone_rate']=items.stone_rate
                    item_dict['sub_item_details']=items.sub_item_details.pk
                    item_dict['sub_item_name']=items.sub_item_details.sub_item_name
                    item_dict['tag_item_id']=items.billing_tag_item.pk
                    item_dict['tag_number']=items.billing_tag_item.tag_number
                    item_dict['tag_weight']=items.tag_weight
                    item_dict['tax_percent']=items.tax_percent
                    item_dict['total_diamond_weight']=items.total_diamond_weight
                    item_dict['total_pieces']=items.total_pieces
                    item_dict['total_stone_weight']=items.total_stone_weight
                    item_dict['wastage_percent']=items.wastage_percentage
                    item_dict['flat_wastage']=items.flat_wastage
                    item_dict['item_huid_rate']=items.huid_rate
                    item_dict['gst']=items.gst
                    item_dict['with_gst_rate']=items.total_rate
                    

                    if str(items.calculation_type.pk) == settings.FIXEDRATE:
                        item_dict['min_metal_rate'] = items.billing_tag_item.min_fixed_rate
                        item_dict['max_metal_rate'] = items.billing_tag_item.max_fixed_rate

                    elif str(items.calculation_type.pk) == settings.WEIGHTCALCULATION:

                        subitem_weight_queryset=SubItemWeightCalculation.objects.get(sub_item_details=items.billing_tag_item.sub_item_details.pk)
                        
                        item_dict['wastage_calculation_type'] = subitem_weight_queryset.wastage_calculation.pk
                        item_dict['wastage_calculation_name'] = subitem_weight_queryset.wastage_calculation.weight_name
                        
                        item_dict['making_charge_calculation_type'] = subitem_weight_queryset.making_charge_calculation.pk
                        item_dict['making_charge_calculation_name'] = subitem_weight_queryset.making_charge_calculation.weight_name

                        item_dict['min_wastage_percent'] = items.billing_tag_item.min_wastage_percent
                        item_dict['min_wastage_percent'] = items.billing_tag_item.min_wastage_percent
                        item_dict['min_flat_wastage'] = items.billing_tag_item.min_flat_wastage
                        item_dict['max_wastage_percent'] = items.billing_tag_item.max_wastage_percent
                        item_dict['max_flat_wastage'] = items.billing_tag_item.max_flat_wastage
                        item_dict['min_making_charge'] = items.billing_tag_item.min_making_charge_gram
                        item_dict['min_flat_making_charge'] = items.billing_tag_item.min_flat_making_charge
                        item_dict['max_making_charge'] = items.billing_tag_item.max_making_charge_gram
                        item_dict['max_flat_making_charge'] = items.billing_tag_item.max_flat_making_charge
                    
                    elif str(items.calculation_type.pk) == settings.PERGRAMRATE:

                        item_dict['min_metal_rate'] = items.billing_tag_item.min_pergram_rate
                        item_dict['max_metal_rate'] = items.billing_tag_item.max_pergram_rate
                        item_dict['per_gram_weight_type'] = items.billing_tag_item.per_gram_weight_type.pk
                        item_dict['per_gram_weight_type_name'] = items.billing_tag_item.per_gram_weight_type.weight_name

                    elif str(items.calculation_type.pk) == settings.PERPIECERATE:
                        # subitem_piece_queryset=SubItemPerPiece.objects.get(sub_item_details=items.billing_tag_item.sub_item_details.pk)                        
                        item_dict['min_per_piece_rate'] = items.billing_tag_item.min_per_piece_rate
                        item_dict['per_piece_rate'] = items.billing_tag_item.per_piece_rate

                    if items.per_gram_weight_type != None:
                        item_dict['per_gram_weight_type']=items.per_gram_weight_type.pk if items.per_gram_weight_type.pk != None else None
                        item_dict['per_gram_weight_type_name']=items.per_gram_weight_type.weight_name if items.per_gram_weight_type.weight_name != None else None


                    try:

                        stone_queryset = BillingBackupStoneDetails.objects.filter(billing_details=queryset.pk,billing_item_details=items.pk)

                        stone_details=[]

                        for stone in stone_queryset:

                            stone_data={
                                    'id':stone.pk,
                                    'stone_name':stone.stone_name.pk,
                                    'stone_pieces':stone.stone_pieces,
                                    'stone_weight_type':stone.stone_weight_type.pk,
                                    'stone_weight_type_name':stone.stone_weight_type.weight_name,
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

                        item_dict['stone_details']=stone_details


                    except BillingBackupStoneDetails.DoesNotExist:
                        stone_details=[]
                        item_dict['stone_details']=stone_details

                    except Exception  as err:

                        raise Exception(err)

                    try:

                        diamond_queryset = BillingBackupDiamondDetails.objects.filter(billing_details=queryset.pk,billing_item_details=items.pk)
                        diamond_details=[]

                        for diamond in diamond_queryset:

                            diamond_data={
                                'id':diamond.pk,
                                'diamond_name':diamond.diamond_name.pk,
                                'diamond_pieces':diamond.diamond_pieces,
                                'diamond_weight_type':diamond.diamond_weight_type.pk,
                                'diamond_weight_type_name':diamond.diamond_weight_type.weight_name,
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

                        item_dict['diamond_details']=diamond_details



                    except BillingBackupDiamondDetails.DoesNotExist:
                        diamond_details=[]
                        item_dict['diamond_details']=diamond_details

                    except Exception as err:

                        raise Exception(err)

                    billing_item_details.append(item_dict)

                res_data['billing_item_details']=billing_item_details

            except BillingBackupTagItems.DoesNotExist:
                billing_item_details=[]
                res_data['billing_item_details']=billing_item_details

            try:

                old_gold_details=[]

                old_gold_queryset = BillingBackupOldGold.objects.filter(billing_details=queryset.pk)

                for old_gold in old_gold_queryset:
                        
                    old_details={
                        'id':old_gold.pk,
                        'dust_weight':old_gold.dust_weight,
                        'item_name':old_gold.item_name,
                        'gross_weight':old_gold.old_gross_weight,
                        'metal':old_gold.old_metal.pk,
                        'metal_name':old_gold.old_metal.metal_name,
                        'metal_rate':old_gold.metal_rate,
                        'net_weight':old_gold.old_net_weight,
                        'old_rate':old_gold.old_metal_rate,
                        'today_rate':old_gold.today_metal_rate,
                        'total':old_gold.total_old_gold_value
                    }
                    if old_gold.purity != None:
                        old_details['purity']= old_gold.purity.pk
                    else:
                        old_details['purity']= "-"
                    old_gold_details.append(old_details)

                    res_data["old_gold_no"] = old_gold.old_gold_no
                        
                res_data["old_item_details"] = old_gold_details

            except BillingBackupOldGold.DoesNotExist:
                old_gold_details=[]
                res_data["old_item_details"] = old_gold_details

            except Exception as err:
                raise Exception(err)

            return Response(
                {
                    "data":{
                        "customer_details" : customer_details,
                        "billing_details": res_data
                    },
                    "message":res_msg.retrieve("Billing Details"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )

        except BillingBackupDetails.DoesNotExist :

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
        
    @transaction.atomic
    def post(self,request):
        try:
            
            data = request.data
            
            res_data={
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

            if request.user.role.is_admin == False:
                res_data['branch'] = request.user.branch.pk

            else:
                res_data['branch'] = data.get('branch')

            res_data['created_at'] = timezone.now()
            res_data['created_by'] = request.user.id
            
            serializer = BillingBackupDetailsSerializer(data=res_data)
            if serializer.is_valid():
                serializer.save()
                billing_details=serializer.data

                if int(res_data['bill_type']) == 1:
                    bill_id_dict={}
                    bill_id_dict['bill_id']=serializer.data['id']
                    bill_number_serializer=BackupBillID(data=bill_id_dict)

                    if bill_number_serializer.is_valid():
                        bill_number_serializer.save()
                
                elif int(res_data['bill_type']) == 2:

                    bill_id_dict={}
                    bill_id_dict['bill_id']=serializer.data['id']
                    bill_number_serializer=BackupBillSilverBillID(data=bill_id_dict)

                    if bill_number_serializer.is_valid():
                        bill_number_serializer.save()
                
                else:
                    pass
                
                oldgold_details = request.data.get('old_gold_particulars', {})
                if len(oldgold_details) != 0:
                    for oldgold in oldgold_details:
                        try:
                            new_oldgold_data = {}
                
                            if len(str(oldgold.get('metal'))) != 0:
                                new_oldgold_data['old_metal']=oldgold['metal']
                                new_oldgold_data['item_name']=oldgold['item_name']
                                new_oldgold_data['old_gold_no']=request.data.get('old_gold_no')
                                new_oldgold_data['metal_rate']=oldgold['metal_rate']
                                new_oldgold_data['old_gross_weight']=oldgold['gross_weight']
                                new_oldgold_data['old_net_weight']=oldgold['net_weight']
                                new_oldgold_data['dust_weight']=oldgold['dust_weight']
                                new_oldgold_data['billing_details']=serializer.data['id']
                                # new_oldgold_data['old_metal_rate']=oldgold['old_rate']
                                # new_oldgold_data['today_metal_rate']=oldgold['today_rate']
                                new_oldgold_data['total_old_gold_value']=oldgold['total']
                                # new_oldgold_data['purity']=oldgold['purity']
                                

                            if len(new_oldgold_data) != 0 :

                                oldgold_serializer = BillingBackupOldGoldSerializer(data=new_oldgold_data)
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
                            
                            billing_taggeditem_serializer = BillingBackupTagItemsSerializer(data=billing_tag_data)
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

                                    billing_stone_serializer=BillingBackupStoneDetailsSerializer(data=stone)
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

                                    billing_diamond_serializer=BillingBackupDiamondDetailsSerializer(data=diamond)
                                    if billing_diamond_serializer.is_valid():
                                        billing_diamond_serializer.save()
                                    else:
                                        raise Exception(billing_diamond_serializer.errors)

                            else:
                                raise Exception(billing_taggeditem_serializer.errors)
                            
                        except Exception as err:
                            raise Exception(err)
            
                StockReduceBillingBackup(serializer.data['id'])
                return Response(
                    {
                        "data":serializer.data,
                        "message":res_msg.create("Biling"),
                        "status":status.HTTP_201_CREATED
                    },status=status.HTTP_200_OK)
            
            else:
                raise Exception(serializer.errors)
        
        except Exception as err:
            # DeleteBillBackup(serializer.data['id'])
            transaction.set_rollback(True)
            return Response(
            {
                "data":str(err),
                "message":res_msg.not_create("Biling"),
                "status":status.HTTP_400_BAD_REQUEST
            },status=status.HTTP_200_OK)
        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class TruncateModelView(APIView):
    def post(self, request):
        billing_bill_number_table = BackupBillNumber._meta.db_table
        billing_bill_id_table = BackupBillID._meta.db_table
        billing_bill_silver_number_table = BackupBillSilverNumber._meta.db_table
        billing_bill_silver_id_table = BackupBillSilverBillID._meta.db_table
        billing_table = BillingBackupDetails._meta.db_table
        item_table = BillingBackupTagItems._meta.db_table
        stone_table = BillingBackupStoneDetails._meta.db_table
        diamond_table = BillingBackupDiamondDetails._meta.db_table
        oldgold_table = BillingBackupOldGold._meta.db_table
        with connection.cursor() as cursor:
            cursor.execute('SET FOREIGN_KEY_CHECKS=0;')
 
            cursor.execute(f"TRUNCATE TABLE {oldgold_table}")
            cursor.execute(f"TRUNCATE TABLE {diamond_table}")
            cursor.execute(f"TRUNCATE TABLE {stone_table}")
            cursor.execute(f"TRUNCATE TABLE {item_table}")
            cursor.execute(f"TRUNCATE TABLE {billing_table}")
            cursor.execute(f"TRUNCATE TABLE {billing_bill_number_table}")
            cursor.execute(f"TRUNCATE TABLE {billing_bill_id_table}")
            cursor.execute(f"TRUNCATE TABLE {billing_bill_silver_number_table}")
            cursor.execute(f"TRUNCATE TABLE {billing_bill_silver_id_table}")
 
            cursor.execute('SET FOREIGN_KEY_CHECKS=1;')
 
            return Response ({
                "message" : "Tables truncated successfully",
                "status" : status.HTTP_200_OK,
            } , status=status.HTTP_200_OK)
        

def stock_check(pk):
    try:

        queryset = TaggedItems.objects.get(tag_number=pk)

        gross_weight = queryset.gross_weight
        net_weight = queryset.net_weight
        pieces = queryset.tag_pieces

        if int(queryset.sub_item_details.stock_type.pk) == int(settings.TAG):

            lot_queryset = Lot.objects.get(queryset.tag_entry_details.lot_details.pk)

            lot_dict_data = {}

            lot_item_queryset = LotItem.objects.get(id=queryset.item_details.pk)

            item_data_dict = {}

            item_data_dict['gross_weight'] = float(lot_item_queryset.gross_weight) - float(gross_weight)
            item_data_dict['net_weight'] = float(lot_item_queryset.net_weight) - float(net_weight)
            item_data_dict['pieces'] = int(lot_item_queryset.pieces) - int(pieces)

            lot_serializer = LotItemSerializer(lot_item_queryset,data=item_data_dict,partial=True)

            if lot_serializer.is_valid():
                lot_serializer.save()
                queryset.delete()

    except:
        pass


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class DeleteModelView(APIView):
    def post(self, request):
        billing_backup_queryset = BillingBackupDetails.objects.all()
        
        for data in billing_backup_queryset:

            tagitem_backup_queryset = BillingBackupTagItems.objects.get(billing_details=data.pk)
            tagitem_backup_queryset.delete()

            stone_backup_queryset = BillingBackupStoneDetails.objects.get(billing_details=data.pk)
            stone_backup_queryset.delete()

            diamond_backup_queryset = BillingBackupDiamondDetails.objects.get(billing_details=data.pk)
            diamond_backup_queryset.delete()

            old_gold_queryset = BillingBackupOldGold.objects.get(billing_details=data.pk)
            old_gold_queryset.delete()

            backup_bill_queryset = BillingBackupDetails.objects.get(id=data.pk)
            backup_bill_queryset.delete()

        return Response ({
            "message" : "Tables deleted successfully",
            "status" : status.HTTP_200_OK,
        } , status=status.HTTP_200_OK)
        

def DeleteBillBackup(pk):
    try:
        
        queryset = BillingBackupDetails.objects.get(id=pk)
        queryset.delete()
        
    except:
        pass

@transaction.atomic
def StockReduceBillingBackup(pk):
    try:
        # with transaction.atomic():
        estimation_items=list(BillingBackupTagItems.objects.filter(billing_details=pk))
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
        #     DeleteBillBackup(pk)
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