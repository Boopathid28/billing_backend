
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
from stock.serializer import StockLedgerSerializer
from order_management.models import *
from order_management.serializer import *


res_msg = ResponseMessages()
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class EntryTypeView(APIView):
    def get(self,request):

        queryset=list(EntryType.objects.filter(is_active=True).order_by('id').values('id','entry_name'))

        return Response(
            {
                "data":{
                    "list":queryset
                },
                "message":res_msg.retrieve("Entry Type"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class WeightTypeView(APIView):
    def get(self,request):

        queryset=list(StoneWeightType.objects.filter(is_active=True).order_by('id').values('id','weight_name'))
        
        return Response(
            {
                "data":{
                    "list":queryset
                },
                "message":res_msg.retrieve("Weight Type"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class RateTypeView(APIView):
    def get(self,request):

        queryset=list(RateType.objects.filter(is_active=True).order_by('id').values('id','type_name'))

        return Response(
            {
                "data":{
                    "list":queryset
                },
                "message":res_msg.retrieve("Rate Type"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class DiamondListView(APIView):
    def get(self,request):

        queryset=list(StoneDetails.objects.filter(is_active=True).order_by('id').values('id','stone_name'))

        return Response(
            {
                "data":{
                    "list":queryset
                },
                "message":res_msg.retrieve("Diamond Details"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class LotIDView(APIView):

    def get(self,request):
        try:
            queryset=LotID.objects.all().order_by('-id')[0]
            new_id=int(queryset.pk)+1
            return Response(
                {
                    "lot_number":new_id,
                    "message":res_msg.retrieve("Lot Number"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        
        except Exception as err:
            return Response(
                {
                    "lot_number":1,
                    "message":res_msg.retrieve("Lot Number"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        

def delete_lot(pk):

    try:
        queryset=Lot.objects.get(id=pk)
        queryset.delete()

    except:
        pass
        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class LotViewset(viewsets.ViewSet):
    @transaction.atomic
    def create(self,request):
        try:

            request_data=request.data
            
            lot_detail=request_data.get('lot_details') if request_data.get('lot_details') else {}
           
            if lot_detail.get('hallmark_center') == "":
                lot_detail['hallmark_center'] = None

            if lot_detail.get('hallmark_number') == "":
                lot_detail['hallmark_number'] = None

            if lot_detail.get('invoice_number') == "":
                lot_detail['invoice_number'] = None

            lot_detail['created_at']=timezone.now()
            lot_detail['created_by']=request.user.id

            if request.user.role.is_admin == False :
                lot_detail['branch'] = request.user.branch.pk

            lot_serializer=LotSerializer(data=lot_detail)

            total_pieces=0
            total_netweight=0
            total_grossweight=0
            total_stone_pieces=0
            total_stone_weight=0
            total_stone_rate=0
            total_diamond_pieces=0
            total_diamond_weight=0
            total_diamond_rate=0
            total_tag_count=0

            if lot_serializer.is_valid():
                lot_serializer.save()
                lot_id_dict={}
                lot_id_dict['lot_number']=lot_detail['lot_number']

                lot_number_serializer=LotIDSerializer(data=lot_id_dict)

                if lot_number_serializer.is_valid():
                    lot_number_serializer.save()

                item_details=request_data.get('item_details') if request_data.get('item_details') else {}

                for item in item_details:
                    print(lot_serializer.data['entry_type'])
                    print(settings.ORDER_ENTRY)
                    if lot_serializer.data['entry_type'] == settings.ORDER_ENTRY:
                        order_item_queryset = OrderItemDetails.objects.get(id=item['id'])
                        update_order_item = {
                            'is_converted_to_lot' : True,
                            'order_status' : settings.LOT_CONVERTED
                        }
                        order_item_serializer = OrderItemDetailsSerializer(order_item_queryset,data=update_order_item,partial=True)
                        if order_item_serializer.is_valid():
                            order_item_serializer.save()

                            orderitem_queryset = OrderItemDetails.objects.filter(order_id=order_item_queryset.order_id)
                            print(orderitem_queryset)
                            count = len(orderitem_queryset)
                            print(count)
                            true_status = 0
                            for order in orderitem_queryset:
                                if order.is_converted_to_lot == True:
                                    true_status += 1
                            print(true_status)
                            if count == true_status:
                                update_orderitem = {
                                    'order_status' : settings.LOT_CONVERTED
                                }
                                order_queryset = OrderDetails.objects.get(id=order_item_queryset.order_id.pk)
                                
                                order_serializer = OrderDetailsSerializer(order_queryset,data=update_orderitem,partial=True)
                                if order_serializer.is_valid():
                                    order_serializer.save()
                                    print(order_serializer.data)
                                else:
                                    raise Exception(order_serializer.errors)
                            else:
                                raise Exception("count not match")
                        else:
                            raise Exception(order_item_serializer.errors)
                        
                    item['lot_details']=str(lot_serializer.data['id'])
                    item['gross_weight'] = 0 if item['gross_weight'] is None else float(item['gross_weight'])
                    item['tag_weight'] = 0 if item['tag_weight'] is None else float(item['tag_weight'])
                    item['cover_weight'] = 0 if item['cover_weight']is None else float(item['cover_weight'])
                    item['loop_weight'] = 0 if item['loop_weight']is None else float(item['loop_weight'])
                    item['other_weight'] = 0 if item['other_weight']is None else float(item['other_weight'])

                    item['pieces']=int(item['pieces'])
                    item['tag_count']=int(item['tag_count'])

                    item['net_weight']=0

                    item_stone_pieces=0
                    item_stone_weight=0
                    item_diamond_pieces=0
                    item_diamond_weight=0

                    item_serializer=LotItemSerializer(data=item)

                    if item_serializer.is_valid():
                        item_serializer.save()

                        total_pieces+=int(item['pieces'])
                        total_grossweight+=float(item['gross_weight'])
                        total_tag_count+=int(item['tag_count'])

                        stone_details=item.get('stone_details') if item.get('stone_details') else []

                        for stone in stone_details:

                            stone['lot_details']=lot_serializer.data['id']
                            stone['lot_item']=item_serializer.data['id']

                            stone['stone_weight']=float(stone['stone_weight'])
                            stone['stone_rate']=float(stone['stone_rate'])
                            stone['stone_pieces']=int(stone['stone_pieces'])

                            if str(stone['stone_weight_type'])==settings.CARAT:

                                stone_weight=float(stone['stone_weight'])/5
                                stone['stone_weight']=stone_weight

                            if str(stone['stone_rate_type'])==settings.PERGRAM:

                                stone['total_stone_value']=float(stone['stone_weight'])*float(stone['stone_rate'])

                            if str(stone['stone_rate_type'])==settings.PERCARAT:

                                stone_rate=float(stone['stone_rate'])*5
                                stone['stone_rate']=stone_rate
                                stone['total_stone_value']=float(stone['stone_weight'])*float(stone['stone_rate'])

                            if str(stone['stone_rate_type'])==settings.PERPIECE:
                                stone['total_stone_value']=float(stone['stone_pieces'])*float(stone['stone_rate'])

                            item_stone_pieces+=int(stone['stone_pieces'])

                            if stone['include_stone_weight'] == True :
                                item_stone_weight+=stone['stone_weight']

                            stone_serializer=LotItemStoneSerializer(data=stone)
                            if stone_serializer.is_valid():
                                stone_serializer.save()

                                total_stone_pieces+=int(stone['stone_pieces'])
                                total_stone_weight+=float(item_stone_weight)
                                total_stone_rate+=float(stone['total_stone_value'])

                            else:
                                raise Exception(stone_serializer.errors)
                                
                        diamond_details=item.get('diamond_details') if item.get('diamond_details') else []

                        for diamond in diamond_details:

                            diamond['lot_details']=lot_serializer.data['id']
                            diamond['lot_item']=item_serializer.data['id']

                            diamond['diamond_weight']=float(diamond['diamond_weight'])
                            diamond['diamond_rate']=float(diamond['diamond_rate'])
                            diamond['diamond_pieces']=int(diamond['diamond_pieces'])

                            if str(diamond['diamond_weight_type'])==settings.CARAT:
                                diamond_weight=float(diamond['diamond_weight'])/5
                                diamond['diamond_weight']=diamond_weight


                            if str(diamond['diamond_rate_type'])==settings.PERGRAM:
                                diamond['total_diamond_value']=float(diamond['diamond_weight'])*float(diamond['diamond_rate'])

                            if str(diamond['diamond_rate_type'])==settings.PERCARAT:
                                diamono_rate=float(diamond['diamond_rate'])*5
                                diamond['diamond_rate']=diamono_rate
                                diamond['total_diamond_value']=float(diamond['diamond_weight'])*float(diamond['diamond_rate'])

                            if str(diamond['diamond_rate_type'])==settings.PERPIECE:
                                diamond['total_diamond_value']=float(diamond['diamond_pieces'])*float(diamond['diamond_rate'])

                            item_diamond_pieces+=diamond['diamond_pieces']

                            if diamond['include_diamond_weight'] == True :
                                item_diamond_weight+=diamond['diamond_weight']
                            
                            diamond_serializer=LotItemDiamondSerializer(data=diamond)

                            if diamond_serializer.is_valid():
                                diamond_serializer.save()

                                total_diamond_pieces+=int(diamond['diamond_pieces'])
                                total_diamond_weight+=float(item_diamond_weight)
                                total_diamond_rate+=float(diamond['total_diamond_value'])

                            else:
                                raise Exception(diamond_serializer.errors)

                        net_weight = float(item['gross_weight'])-(item['tag_weight']+item['cover_weight']+item['loop_weight']+item['other_weight']+item_stone_weight+item_diamond_weight)
                        total_netweight+=float(net_weight)
                        item_calc={
                            "item_stone_pieces":item_stone_pieces,
                            "item_stone_weight":item_stone_weight,
                            "item_diamond_pieces":item_diamond_pieces,
                            "item_diamond_weight":item_diamond_weight,
                            "net_weight":net_weight
                        }
                        item_queryset=LotItem.objects.get(id=item_serializer.data['id'])

                        item_calc_serializer=LotItemSerializer(item_queryset,data=item_calc,partial=True)

                        if item_calc_serializer.is_valid():
                            item_calc_serializer.save()

                    else:
                        raise Exception(item_serializer.errors)

                lot_queryset=Lot.objects.get(id=lot_serializer.data['id'])

                data={
                    'total_pieces':total_pieces,
                    'total_netweight':total_netweight,
                    'total_grossweight':total_grossweight,
                    'total_stone_pieces':total_stone_pieces,
                    'total_stone_weight':total_stone_weight,
                    'total_stone_rate':total_stone_rate,
                    'total_diamond_pieces':total_diamond_pieces,
                    'total_diamond_weight':total_diamond_weight,
                    'total_diamond_rate':total_diamond_rate,
                    'total_tag_count':total_tag_count,
                    }
                
                
                if lot_queryset.tagged_grossweight==0 :

                    data['tag_status']=settings.PENDING
                
                elif 0 <  lot_queryset.tagged_grossweight < lot_queryset.total_grossweight :

                    data['tag_status']=settings.PARTIAL
                
                elif lot_queryset.tagged_grossweight>=lot_queryset.total_grossweight :

                    data['tag_status']=settings.COMPLETED


                lot_calc_serializer=LotSerializer(lot_queryset,data=data,partial=True)

                if lot_calc_serializer.is_valid():
                    lot_calc_serializer.save()

                return Response(
                    {
                        "data":lot_calc_serializer.data,
                        "message":res_msg.create("Lot"),
                        "status":status.HTTP_200_OK
                    },status=status.HTTP_200_OK
                )
                    
            else:
                return Response(
                    {
                        "data":lot_serializer.errors,
                        "message":res_msg.something_else(),
                        "status":status.HTTP_204_NO_CONTENT
                    },status=status.HTTP_200_OK
                )
        
        except Exception as err:
            # try:
            #     delete_lot(pk=lot_serializer.data['id'])
            # except:
            #     pass
            transaction.set_rollback(True)
            return Response(
                {
                    "data":str(err),
                    "message":res_msg.something_else(),
                    "status":status.HTTP_400_BAD_REQUEST
                },status=status.HTTP_200_OK
            )
        
    def retrieve(self,request,pk):
 
        try:

            queryset=Lot.objects.get(id=pk)
            
            Response_data={}
 
            Lot_serializer=LotSerializer(queryset)
            
            lotdata = Lot_serializer.data
            Response_data['remaining_pieces'] = queryset.total_pieces - queryset.tagged_pieces
            Response_data['remaining_grossweight'] = queryset.total_grossweight - queryset.tagged_grossweight
            Response_data['remaining_netweight'] = queryset.total_netweight - queryset.tagged_netweight
            Response_data['remaining_tag_count'] = queryset.total_tag_count - queryset.tagged_tag_count

            
            Response_data['lot_details']=lotdata
            Response_data['lot_details']['branch_name']=queryset.branch.branch_name
            Response_data['lot_details']['color']=queryset.tag_status.color
            Response_data['lot_details']['status_name']=queryset.tag_status.status_name
            Response_data['lot_details']['entry_type_name']=queryset.entry_type.entry_name
            
            if queryset.designer_name != None:
                Response_data['lot_details']['designer_name'] = {
                    "id": queryset.designer_name.pk,
                    "account_head_name": queryset.designer_name.account_head_name,
                    "account_head_code": queryset.designer_name.account_head_code,
                    "upi_id":queryset.designer_name.upi_id
                }
            else:
                Response_data['lot_details']['designer_name'] = None
            
            item_details=[]

            try:
                item_queryset=list(LotItem.objects.filter(lot_details=queryset.pk))
                
                for item in item_queryset:
                    item_dict={}
                    item_serializer=LotItemSerializer(item)
                    item_dict=item_serializer.data

                    item_dict['remaining_grossweight'] = item.gross_weight - item.tagged_grossweight
                    item_dict['remaining_netweight'] = item.net_weight - item.tagged_netweight
                    item_dict['remaining_pieces'] = item.pieces - item.tagged_pieces
                    item_dict['remaining_tag_count'] = item.tag_count - item.tagged_tag_count

                    item_dict['item_counter_name']=item.item_details.item_counter.counter_name
                    item_dict['item_counter']=item.item_details.item_counter.pk
    
                    item_dict['item_details'] = {
                        "huid_rate": item.item_details.huid_rate,
                        "id": item.item_details.pk,
                        "item_id": item.item_details.item_id,
                        # "item_code": item.item_details.item_code,
                        "item_name": item.item_details.item_name,
                        "hsn_code":item.item_details.hsn_code,
                        "stock_type":item.item_details.stock_type.pk,
                        "stock_type__stock_type_name":item.item_details.stock_type.stock_type_name
                    }
                    

                    item_metal=str(item.item_details.metal.metal_name)

                    item_purity=str(item.item_details.purity.purity_name)

                    item_metal_purity=item_metal+'_'+item_purity

                    try:

                        # metal_rate_queryset=MetalRate.objects.all().order_by('-id')[0]

                        # item_metal_rate=float(metal_rate_queryset.rate[item_metal_purity])

                        # item_dict['item_metal_rate']=float(item_metal_rate)
                        metal_rate_queryset = MetalRate.objects.filter(purity=item.item_details.purity.pk).order_by('-id')[0]
                        item_dict['item_metal_rate']= metal_rate_queryset.rate

                    except Exception as err:

                        item_dict['item_metal_rate']=0
                    
                    item_dict['item_calculation_type']=item.item_details.calculation_type.pk
                    item_dict['item_calculation_type_name']=item.item_details.calculation_type.calculation_name

                    if str(item.item_details.calculation_type.pk) == settings.FIXEDRATE:
                        try:
                            
                            item_fixed_queryset=FixedRate.objects.get(item_details=item.item_details.pk)
    
                            item_dict['item_min_fixedrate']=item_fixed_queryset.fixed_rate
                        except Exception as err:
                            pass
    
                    elif str(item.item_details.calculation_type.pk) == settings.WEIGHTCALCULATION:
                        try:
                            item_weight_queryset=WeightCalculation.objects.get(item_details=item.item_details.pk)
                            item_dict['item_wastage_calculation']=item_weight_queryset.wastage_calculation.pk
                            item_dict['item_wastage_calculation_name']=item_weight_queryset.wastage_calculation.weight_name
                            item_dict['item_min_wastagepercent']=item_weight_queryset.wastage_percent
                            item_dict['item_min_flatwastage']=item_weight_queryset.flat_wastage
                            item_dict['item_making_charge_calculation']=item_weight_queryset.making_charge_calculation.pk
                            item_dict['item_making_charge_calculation_name']=item_weight_queryset.making_charge_calculation.weight_name
                            item_dict['item_min_makingcharge_gram']=item_weight_queryset.making_charge_gram
                            item_dict['item_min_flat_makingcharge']=item_weight_queryset.flat_making_charge
                        except:
                            pass

                    elif str(item.item_details.calculation_type.pk) == settings.PERPIECERATE:
                        try:
                            
                            item_perpiece_queryset=PerPiece.objects.get(item_details=item.item_details.pk)    
                            item_dict['item_min_per_piece_rate']=item_perpiece_queryset.min_per_piece_rate
                            item_dict['item_per_piece_rate']=item_perpiece_queryset.per_piece_rate

                        except Exception as err:
                            pass
                    elif str(item.item_details.calculation_type.pk) == settings.PERGRAMRATE:
                        try:
                            item_fixed_queryset=PerGramRate.objects.get(item_details=item.item_details.pk)

                            item_dict['item_min_pergram_rate']=item_fixed_queryset.per_gram_rate
                        except Exception as err:
                            pass

                    elif str(item.item_details.calculation_type.pk) == settings.PERPIECERATE:
                        try:
                            item_perpiece_queryset=PerPiece.objects.get(item_details=item.item_details.pk)

                            item_dict['item_per_piece_rate']=item_perpiece_queryset.per_piece_rate
                            item_dict['item_min_per_piece_rate']=item_perpiece_queryset.min_per_piece_rate
                        except Exception as err:
                            pass

    
                    if item.subitem_details != None:                        
                        try:
                            # metal_rate_queryset=MetalRate.objects.all().order_by('-id')[0]
                            # metal_purity=str(item.subitem_details.metal.metal_name)+'_'+str(item.subitem_details.purity.purity_name)
                            # metal_rate=metal_rate_queryset.rate[metal_purity]
                            # sub_item_metalrate=metal_rate
                            metal_rate_queryset = MetalRate.objects.filter(purity=item.subitem_details.purity.pk).order_by('-id')[0]
                            sub_item_metalrate = metal_rate_queryset.rate
                        except Exception as err:                            
                            sub_item_metalrate =0

                        item_dict['subitem_details'] = {                            
                            "id": item.subitem_details.pk,
                            "sub_item_id": item.subitem_details.sub_item_id,
                            "subitem_hsn_code":item.subitem_details.subitem_hsn_code,
                            # "sub_item_code": item.subitem_details.sub_item_code,
                            "sub_item_name": item.subitem_details.sub_item_name,
                            "allow_zero_weight":item.subitem_details.allow_zero_weight,                            
                            "metal":item.subitem_details.metal.pk,
                            "purity":item.subitem_details.purity.pk,
                            "item_details":item.subitem_details.item_details.pk,
                            "stock_type":item.subitem_details.stock_type.pk,
                            "sub_item_counter": item.subitem_details.sub_item_counter.pk,
                            "calculation_type":item.subitem_details.calculation_type.pk,
                            "measurement_type": item.subitem_details.measurement_type.pk,
                            "measurement_name": item.subitem_details.measurement_type.measurement_name,
                            "metal_rate":sub_item_metalrate   
                        }
                        
                        item_dict['sub_item_counter']=item.subitem_details.sub_item_counter.pk
                        item_dict['sub_item_counter_name']=item.subitem_details.sub_item_counter.counter_name
                        item_dict['measurement_type']=item.subitem_details.measurement_type.pk
                        item_dict['measurement_type_name']=item.subitem_details.measurement_type.measurement_name
                        item_dict['is_subitem_detail']=True
                        item_dict['subitem_calculation_type']=item.subitem_details.calculation_type.pk
                        item_dict['subitem_calculation_type_name']=item.subitem_details.calculation_type.calculation_name

                        sub_item_metal=str(item.subitem_details.metal.metal_name)

                        sub_item_purity=str(item.subitem_details.purity.purity_name)

                        sub_item_metal_purity=sub_item_metal+'_'+sub_item_purity

                        try:

                            # sub_metal_rate_queryset=MetalRate.objects.all().order_by('-id')[0]

                            # subitem_metal_rate=float(sub_metal_rate_queryset.rate[sub_item_metal_purity])

                            # item_dict['sub_item_metalrate'] = float(subitem_metal_rate)
                            metal_rate_queryset = MetalRate.objects.filter(purity=item.subitem_details.purity.pk).order_by('-id')[0]
                            item_dict['sub_item_metalrate'] = metal_rate_queryset.rate

                        except:
                            item_dict['sub_item_metalrate'] = 0

                        if str(item.subitem_details.calculation_type.pk) == settings.FIXEDRATE:
    
                            try:
                                fixed_queryset=SubItemFixedRate.objects.get(sub_item_details=item.subitem_details.pk)
                                item_dict['subitem_min_fixedrate']=fixed_queryset.fixed_rate
                            except Exception as err:
                                pass
                        elif str(item.subitem_details.calculation_type.pk) == settings.WEIGHTCALCULATION:
                            try:
                                weight_queryset=SubItemWeightCalculation.objects.get(sub_item_details=item.subitem_details.pk)
                                item_dict['subitem_wastage_calculation']=weight_queryset.wastage_calculation.pk
                                item_dict['subitem_wastage_calculation_name']=weight_queryset.wastage_calculation.weight_name
                                item_dict['subitem_min_wastagepercent']=weight_queryset.wastage_percent
                                item_dict['subitem_min_flatwastage']=weight_queryset.flat_wastage
                                item_dict['subitem_making_charge_calculation']=weight_queryset.making_charge_calculation.pk
                                item_dict['subitem_making_charge_calculation_name']=weight_queryset.making_charge_calculation.weight_name
                                item_dict['subitem_min_makingcharge_gram']=weight_queryset.making_charge_gram
                                item_dict['subitem_min_flat_makingcharge']=weight_queryset.flat_making_charge
                            except:
                                pass

                        elif str(item.subitem_details.calculation_type.pk) == settings.PERPIECERATE:
    
                            try:
                                perpiece_queryset=SubItemPerPiece.objects.get(sub_item_details=item.subitem_details.pk)
                                item_dict['subitem_min_per_piece_rate']=perpiece_queryset.min_per_piece_rate
                                item_dict['subitem_per_piece_rate']=perpiece_queryset.per_piece_rate
                            except Exception as err:
                                pass

                        elif str(item.subitem_details.calculation_type.pk) == settings.PERGRAMRATE:
                            try:
                                fixed_gram_queryset=SubItemPerGramRate.objects.get(sub_item_details=item.subitem_details.pk)
                                item_dict['subitem_min_per_gram_rate']=fixed_gram_queryset.per_gram_rate
                            except :
                                pass

                    else:
                        item_dict['subitem_details'] = None
                        item_dict['is_subitem_detail']=False

                    try:
    
                        stone_queryset=list(LotItemStone.objects.filter(lot_details=queryset.pk,lot_item=item))
                        stone_data=[]

                        item_stone_pieces=0
                        item_stone_weight=0
                        tagged_stone_pieces = 0
                        tagged_stone_weight = 0
        
                        for stone in stone_queryset:
        
                            stone_serializer=LotItemStoneSerializer(stone)
                            stone_dict=stone_serializer.data

                            item_stone_pieces+=int(stone_dict['stone_pieces'])
                            tagged_stone_pieces += int(stone.tagged_stone_pieces)
                            tagged_stone_weight += float(stone.tagged_stone_weight)
        
                            if str(stone_dict['stone_weight_type'])==settings.CARAT:
                                stone_weight=float(stone_dict['stone_weight'])*5
                                stone_dict['stone_weight']=stone_weight
        
                            if str(stone_dict['stone_rate_type'])==settings.PERCARAT:
                                stone_rate=float(stone_dict['stone_rate'])/5
                                stone_dict['stone_rate']=stone_rate

                            item_stone_weight+=float(stone_dict['stone_weight'])

                            stone_dict['remaining_stone_pieces'] = stone.stone_pieces - stone.tagged_stone_pieces
                            stone_dict['remaining_stone_weight'] = stone.stone_weight - stone.tagged_stone_weight

                            stone_data.append(stone_dict)
        
                        item_dict['stone_details']=stone_data
                        item_dict['item_stone_pieces']=item_stone_pieces
                        item_dict['item_stone_weight']=item_stone_weight
                        item_dict['tagged_stone_pieces'] = tagged_stone_pieces
                        item_dict['tagged_stone_weight'] = tagged_stone_weight
                        item_dict['remaining_stone_pieces'] = item_stone_pieces - tagged_stone_pieces
                        item_dict['remaining_stone_weight'] = item_stone_weight - tagged_stone_weight

                    except :
                        pass

                    try:
                        
                        diamond_queryset=list(LotItemDiamond.objects.filter(lot_details=queryset.pk,lot_item=item))
                        diamond_data=[]

                        item_diamond_pieces=0
                        item_diamond_weight=0
                        tagged_diamond_pieces = 0
                        tagged_diamond_weight = 0
        
                        for diamond in diamond_queryset:
        
                            diamond_serializer=LotItemDiamondSerializer(diamond)
                            diamond_dict=diamond_serializer.data
        
                            item_diamond_pieces+=int(diamond_dict['diamond_pieces'])

                            tagged_diamond_pieces += int(diamond.tagged_diamond_pieces)
                            tagged_diamond_weight += float(diamond.tagged_diamond_weight)

                            if str(diamond_dict['diamond_weight_type'])==settings.CARAT:
                                diamond_weight=float(diamond_dict['diamond_weight'])*5
                                
                                diamond_dict['diamond_weight']=diamond_weight
        
                            if str(diamond_dict['diamond_rate_type'])==settings.PERCARAT:
                                diamond_rate=float(diamond_dict['diamond_rate'])/5
                                diamond_dict['diamond_rate']=diamond_rate

                            item_diamond_weight+=float(diamond_dict['diamond_weight'])
                            
                            diamond_data.append(diamond_dict)
        
                        item_dict['diamond_details']=diamond_data
                        item_dict['item_diamond_pieces']=item_diamond_pieces
                        item_dict['item_diamond_weight']=item_diamond_weight
                        item_dict['tagged_diamond_pieces']=tagged_diamond_pieces
                        item_dict['tagged_diamond_weight']=tagged_diamond_weight
                        item_dict['remaining_diamond_pieces'] = item_diamond_pieces - tagged_diamond_pieces
                        item_dict['remaining_diamond_weight'] = item_diamond_weight - tagged_diamond_weight
                        
        
                        item_details.append(item_dict)

                    except :
                        pass
    
                Response_data['item_details']=item_details

            except Exception as err:
                pass
            return Response(
                {
                    "data":Response_data,
                    "message":res_msg.retrieve("Lot Details"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
            
        except Lot.DoesNotExist:
            
            return Response(
                {
                    "message":res_msg.not_exists("Lot"),
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
    
    @transaction.atomic
    def update(self,request,pk):
        try:
            lot_querset=Lot.objects.get(id=pk)

            original_lot_state = lot_querset.__dict__.copy()

            data=request.data

            lot_detail=data.get('lot_details') if data.get('lot_details') else {}
            if lot_detail.get('hallmark_center') == "":
                lot_detail['hallmark_center'] = None

            if lot_detail.get('hallmark_number') == "":
                lot_detail['hallmark_number'] = None

            if lot_detail.get('invoice_number') == "":
                lot_detail['invoice_number'] = None

            lot_detail['modified_at']=timezone.now()
            lot_detail['modified_by']=request.user.id
            
            if request.user.role.is_admin == False:
              lot_detail['branch'] = request.user.branch.pk

            lot_serializer=LotSerializer(lot_querset,data=lot_detail,partial=True)

            if lot_serializer.is_valid():
                lot_serializer.save()

                item_details=data.get('item_details') if data.get('item_details') else {}

                for item in item_details:

                    try:
                        
                        item_id=item.get('id') if item.get('id') else 0

                        item_queryset=LotItem.objects.get(id=item_id,lot_details=lot_serializer.data['id'])
                        
                        net_weight = item['gross_weight']-(item['tag_weight']+item['cover_weight']+item['loop_weight']+item['other_weight'])

                        item['net_weight']=net_weight

                        item_serializer=LotItemSerializer(item_queryset,data=item,partial=True)
                        if item_serializer.is_valid():
                            item_serializer.save()
                        
                        stone_details=item.get('stone_details') if item.get('stone_details') else []
                        
                        for stone in stone_details:
                            try:
                                
                                stone_id=stone.get('id') if stone.get('id') else 0

                                stone_queryset=LotItemStone.objects.get(id=stone_id)

                                if str(stone['stone_weight_type'])==settings.CARAT:
                                    stone_weight=float(stone['stone_weight'])/5
                                    stone['stone_weight']=stone_weight

                                if str(stone['stone_rate_type'])==settings.PERGRAM:
                                    stone['total_stone_value']=float(stone['stone_weight'])*float(stone['stone_rate'])

                                if str(stone['stone_rate_type'])==settings.PERCARAT:
                                    stone_rate=float(stone['stone_rate'])*5
                                    stone['stone_rate']=stone_rate
                                    stone['total_stone_value']=float(stone['stone_weight'])*float(stone['stone_rate'])

                                if str(stone['stone_rate_type'])==settings.PERPIECE:
                                    stone['total_stone_value']=float(stone['stone_pieces'])*float(stone['stone_rate'])
                                
                                
                                stone_old_seriaizer=LotItemStoneSerializer(stone_queryset,data=stone,partial=True)
                                if stone_old_seriaizer.is_valid():
                                    stone_old_seriaizer.save()

                            except LotItemStone.DoesNotExist:
                                
                                stone['lot_details']=pk
                                stone['lot_item']=item_serializer.data['id']
                                
                                if str(stone['stone_weight_type'])==settings.CARAT:
                                    stone_weight=float(stone['stone_weight'])/5
                                    stone['stone_weight']=stone_weight

                                if str(stone['stone_rate_type'])==settings.PERGRAM:
                                    stone['total_stone_value']=float(stone['stone_weight'])*float(stone['stone_rate'])

                                if str(stone['stone_rate_type'])==settings.PERCARAT:
                                    stone_rate=float(stone['stone_rate'])*5
                                    stone['stone_rate']=stone_rate
                                    stone['total_stone_value']=float(stone['stone_weight'])*float(stone['stone_rate'])

                                if str(stone['stone_rate_type'])==settings.PERPIECE:
                                    stone['total_stone_value']=float(stone['stone_pieces'])*float(stone['stone_rate'])


                                stone_new_serializer=LotItemStoneSerializer(data=stone)

                                if stone_new_serializer.is_valid():
                                    stone_new_serializer.save()
                        
                        diamond_details=item.get('diamond_details') if item.get('diamond_details') else []

                        for diamond in diamond_details:
                            try:
                               
                                diamond_id=diamond.get('id') if diamond.get('id') else 0

                                diamond_queryset=LotItemDiamond.objects.get(id=diamond_id)
                               
                                if str(diamond['diamond_weight_type'])==settings.CARAT:
                                    diamond_weight=float(diamond['diamond_weight'])/5
                                    diamond['diamond_weight']=diamond_weight

                                if str(diamond['diamond_rate_type'])==settings.PERGRAM:
                                    diamond['total_diamond_value']=float(diamond['diamond_weight'])*float(diamond['diamond_rate'])

                                if str(diamond['diamond_rate_type'])==settings.PERCARAT:
                                    diamond_rate=float(diamond['diamond_rate'])*5
                                    diamond['diamond_rate']=diamond_rate
                                    diamond['total_diamond_value']=float(diamond['diamond_weight'])*float(diamond['diamond_rate'])

                                if str(diamond['diamond_rate_type'])==settings.PERPIECE:
                                    diamond['total_diamond_value']=float(diamond['diamond_pieces'])*float(diamond['diamond_rate'])


                                diamond_serializer=LotItemDiamondSerializer(diamond_queryset,data=diamond,partial=True)

                                if diamond_serializer.is_valid():
                                    diamond_serializer.save()

                            except LotItemDiamond.DoesNotExist:

                                diamond['lot_details']=lot_serializer.data['id']
                                diamond['lot_item']=item_serializer.data['id']


                                if str(diamond['diamond_weight_type'])==settings.CARAT:
                                    diamond_weight=float(diamond['diamond_weight'])/5
                                    diamond['diamond_weight']=diamond_weight

                                if str(diamond['diamond_rate_type'])==settings.PERGRAM:
                                    diamond['total_diamond_value']=float(diamond['diamond_weight'])*float(diamond['diamond_rate'])

                                if str(diamond['diamond_rate_type'])==settings.PERCARAT:
                                    diamond_rate=float(diamond['diamond_rate'])*5
                                    diamond['diamond_rate']=diamond_rate
                                    diamond['total_diamond_value']=float(diamond['diamond_weight'])*float(diamond['diamond_rate'])

                                if str(diamond['diamond_rate_type'])==settings.PERPIECE:
                                    diamond['total_diamond_value']=float(diamond['diamond_pieces'])*float(diamond['diamond_rate'])


                                diamond_new_serializer=LotItemDiamondSerializer(data=diamond)

                                if diamond_new_serializer.is_valid():
                                    diamond_new_serializer.save()

                    except LotItem.DoesNotExist:

                        item['lot_details']=str(lot_serializer.data['id'])

                        net_weight = item['gross_weight']-(item['tag_weight']+item['cover_weight']+item['loop_weight']+item['other_weight'])

                        item['net_weight']=net_weight

                        item_serializer=LotItemSerializer(data=item)

                        if item_serializer.is_valid():
                            item_serializer.save()

                            stone_details=item.get('stone_details') if item.get('stone_details') else []

                            for stone in stone_details:
                                    
                                stone['lot_details']=lot_serializer.data['id']
                                stone['lot_item']=item_serializer.data['id']

                                if str(stone['stone_weight_type'])==settings.CARAT:
                                    stone_weight=float(stone['stone_weight'])/5
                                    stone['stone_weight']=stone_weight

                                if str(stone['stone_rate_type'])==settings.PERGRAM:
                                    stone['total_stone_value']=float(stone['stone_weight'])*float(stone['stone_rate'])

                                if str(stone['stone_rate_type'])==settings.PERCARAT:
                                    stone_rate=float(stone['stone_rate'])*5
                                    stone['stone_rate']=stone_rate
                                    stone['total_stone_value']=float(stone['stone_weight'])*float(stone['stone_rate'])

                                if str(stone['stone_rate_type'])==settings.PERPIECE:
                                    stone['total_stone_value']=float(stone['stone_pieces'])*float(stone['stone_rate'])


                                stone_serializer=LotItemStoneSerializer(data=stone)

                                if stone_serializer.is_valid():
                                    stone_serializer.save()
                                       

                            diamond_details=item.get('diamond_details') if item.get('diamond_details') else []

                            for diamond in diamond_details:
                                    
                                diamond['lot_details']=lot_serializer.data['id']
                                diamond['lot_item']=item_serializer.data['id']

                                if str(diamond['diamond_weight_type'])==settings.CARAT:
                                    diamond_weight=float(diamond['diamond_weight'])/5
                                    diamond['diamond_weight']=diamond_weight

                                if str(diamond['diamond_rate_type'])==settings.PERGRAM:
                                    diamond['total_diamond_value']=float(diamond['diamond_weight'])*float(diamond['diamond_rate'])

                                if str(diamond['diamond_rate_type'])==settings.PERCARAT:
                                    diamond_rate=float(diamond['diamond_rate'])*5
                                    diamond['diamond_rate']=diamond_rate
                                    diamond['total_diamond_value']=float(diamond['diamond_weight'])*float(diamond['diamond_rate'])

                                if str(diamond['diamond_rate_type'])==settings.PERPIECE:
                                    diamond['total_diamond_value']=float(diamond['diamond_pieces'])*float(diamond['diamond_rate'])
                                    

                                diamond_serializer=LotItemDiamondSerializer(data=diamond)

                                if diamond_serializer.is_valid():
                                    diamond_serializer.save()

                total_pieces=0
                total_netweight=0
                total_grossweight=0
                total_stone_pieces=0
                total_stone_weight=0
                total_stone_rate=0
                total_diamond_pieces=0
                total_diamond_weight=0
                total_diamond_rate=0
                
                item_calc_queryset=list(LotItem.objects.filter(lot_details=pk))

                for i in item_calc_queryset:

                    item_stone_pieces=0
                    item_stone_weight=0
                    item_diamond_pieces=0
                    item_diamond_weight=0


                    total_pieces+=int(i.pieces)
                    total_grossweight+=float(i.gross_weight)

                    stone_calc_queryset=list(LotItemStone.objects.filter(lot_details=pk,lot_item=i.pk))

                    for s in stone_calc_queryset:

                        total_stone_pieces+=int(s.stone_pieces)
                        total_stone_rate+=float(s.total_stone_value)
                        item_stone_pieces+=int(s.stone_pieces)

                        if s.include_stone_weight==True:

                            total_stone_weight+=float(s.stone_weight)
                            item_stone_weight+=float(s.stone_weight)
                    
                    diamond_calc_queryset=list(LotItemDiamond.objects.filter(lot_details=pk,lot_item=i.pk))
                    
                    for d in diamond_calc_queryset:

                        total_diamond_pieces+=int(d.diamond_pieces)
                        total_diamond_rate+=float(d.total_diamond_value)
                        item_diamond_pieces+=int(d.diamond_pieces)

                        if d.include_diamond_weight==True:
                            item_diamond_weight+=float(d.diamond_weight)
                            total_diamond_weight+=float(d.diamond_weight)
                    
                    item_net_weight=(i.net_weight-(item_stone_weight+item_diamond_weight))
                    total_netweight+=item_net_weight
                    calc_item_queryset=LotItem.objects.get(id=i.pk)

                    item_data={
                        'net_weight':item_net_weight,
                        "item_stone_pieces":item_stone_pieces,
                        "item_stone_weight":item_stone_weight,
                        "item_diamond_pieces":item_diamond_pieces,
                        "item_diamond_weight":item_diamond_weight
                    }

                    item_calc_serializer=LotItemSerializer(calc_item_queryset,data=item_data,partial=True)

                    if item_calc_serializer.is_valid():
                        item_calc_serializer.save()
                        
                lot_calc_queryset=Lot.objects.get(id=pk)

                calc_data={'total_pieces':total_pieces,
                           'total_netweight':total_netweight,
                           'total_grossweight':total_grossweight,
                           'total_stone_pieces':total_stone_pieces,
                            'total_stone_weight':total_stone_weight,
                            'total_stone_rate':total_stone_rate,
                            'total_diamond_pieces':total_diamond_pieces,
                            'total_diamond_weight':total_diamond_weight,
                            'total_diamond_rate':total_diamond_rate
                           }

                lot_calc_serializer=LotSerializer(lot_calc_queryset,data=calc_data,partial=True)

                if lot_calc_serializer.is_valid():
                    lot_calc_serializer.save()


                return Response(
                    {
                        "data":lot_serializer.data ,
                        "message":res_msg.update("Lot Details"),
                        "status":status.HTTP_200_OK
                    },status=status.HTTP_200_OK
                )

            else:

                return Response(
                    {
                        "data":lot_serializer.errors,
                        "message":res_msg.not_update("Lot Detials"),
                        "status":status.HTTP_400_BAD_REQUEST
                    },status=status.HTTP_200_OK
                )
        except Lot.DoesNotExist:

            return Response(
                {
                    "message":res_msg.not_exists("Lot Details"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        except Exception as err:
            transaction.set_rollback(True)
            # for key, value in original_lot_state.items():
            #     setattr(lot_querset, key, value)
            # lot_querset.save()
            return Response(    
                {
                    "data":str(err),
                    "message":res_msg.something_else(),
                    "status":status.HTTP_204_NO_CONTENT
                },status=status.HTTP_200_OK
            )
        
    def delete(self,request,pk):

        try:

            lot_queryset=Lot.objects.get(id=pk)

            if str(lot_queryset.tag_status_id) != settings.PENDING :

                return Response(
                    {
                        "message":"Cannot Delete the Lot After tagging",
                        "status":status.HTTP_204_NO_CONTENT
                    },status=status.HTTP_200_OK
                )

            else:
                
                item_queryset=list(LotItem.objects.filter(lot_details=pk))

                for item in item_queryset:
                    stone_queryset=list(LotItemStone.objects.filter(lot_details=pk))

                    if stone_queryset:
                        for stone in stone_queryset:
                            stone.delete()

                    diamond_queryset=list(LotItemDiamond.objects.filter(lot_details=pk))
                    if diamond_queryset:
                        for diamond in diamond_queryset:
                            diamond.delete()

                    item.delete()

                lot_queryset.delete()

                return Response(
                    {
                        "message":res_msg.delete("Lot Details"),
                        "status":status.HTTP_200_OK
                    },status=status.HTTP_200_OK
                )
        except Lot.DoesNotExist:

            return Response(
                {
                    "message":res_msg.not_exists('Lot Details'),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        except ProtectedError:
            return Response(
                {
                    "message":res_msg.related_item("Delete"),
                    "status":status.HTTP_204_NO_CONTENT
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
class LotStoneList(APIView):

    def get(self,request,pk):

        lot_stone_queryset=LotItemStone.objects.filter(lot_item=pk).order_by('id')

        stone_serializer=LotItemStoneSerializer(lot_stone_queryset,many=True)

        stone_data=[]
        for i in range(0, len(stone_serializer.data)):

            stone_dict=stone_serializer.data[i]

            item_stone_pieces=0
            item_stone_weight=0

            item_stone_pieces+=int(stone_dict['stone_pieces'])

            if str(stone_dict['stone_weight_type'])==settings.CARAT:
                stone_weight=float(stone_dict['stone_weight'])*5
                stone_dict['stone_weight']=stone_weight

            if str(stone_dict['stone_rate_type'])==settings.PERCARAT:
                stone_rate=float(stone_dict['stone_rate'])/5
                stone_dict['stone_rate']=stone_rate

            item_stone_weight+=float(stone_dict['stone_weight'])

            stone_dict['stone_name']=lot_stone_queryset[i].stone_name.stone_name
            stone_dict['rate_type_name']=lot_stone_queryset[i].stone_rate_type.type_name
            stone_dict['weight_type_name']=lot_stone_queryset[i].stone_weight_type.weight_name

            stone_dict['remaining_stone_pieces'] = lot_stone_queryset[i].stone_pieces - lot_stone_queryset[i].tagged_stone_pieces
            stone_dict['remaining_stone_weight'] = lot_stone_queryset[i].stone_weight - lot_stone_queryset[i].tagged_stone_weight


            stone_data.append(stone_dict)

        return Response(
            {
                "data":{
                    "list":stone_data
                },
                "message":res_msg.retrieve("Lot Stone Details"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class LotDiamondList(APIView):
    def get(self,request,pk):

        lot_diamond_queryset=LotItemDiamond.objects.filter(lot_item=pk).order_by('id')

        diamond_serializer=LotItemDiamondSerializer(lot_diamond_queryset,many=True)

        diamond_data=[]
        item_diamond_pieces=0
        item_diamond_weight=0

        for i in range(0, len(diamond_serializer.data)):

            diamond_dict = diamond_serializer.data[i]

            item_diamond_pieces+=int(diamond_dict['diamond_pieces'])

            if str(diamond_dict['diamond_weight_type'])==settings.CARAT:
                diamond_weight=float(diamond_dict['diamond_weight'])*5
                
                diamond_dict['diamond_weight']=diamond_weight

            if str(diamond_dict['diamond_rate_type'])==settings.PERCARAT:
                diamond_rate=float(diamond_dict['diamond_rate'])/5
                diamond_dict['diamond_rate']=diamond_rate

            item_diamond_weight+=float(diamond_dict['diamond_weight'])

            diamond_dict['diamond_name']=lot_diamond_queryset[i].diamond_name.stone_name
            diamond_dict['rate_type_name']=lot_diamond_queryset[i].diamond_rate_type.type_name
            diamond_dict['weight_type_name']=lot_diamond_queryset[i].diamond_weight_type.weight_name

            diamond_dict['remaining_diamond_pieces'] = lot_diamond_queryset[i].diamond_pieces - lot_diamond_queryset[i].tagged_diamond_pieces
            diamond_dict['remaining_diamond_weight'] = lot_diamond_queryset[i].diamond_weight - lot_diamond_queryset[i].tagged_diamond_weight
            
            diamond_data.append(diamond_dict)

        return Response(
            {
                "data":{
                    "list":diamond_data
                },
                "message":res_msg.retrieve("Lot Diamond Details"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class LotListView(APIView):
   
    def get(self,request,branch=None):

        filter_dict={}

        if request.user.role.is_admin == True:
            if branch != None:            
                filter_dict['branch'] = branch
        else:
            filter_dict['branch'] = request.user.branch_id
        
        queryset=list(Lot.objects.filter(**filter_dict).values('id','lot_number','entry_type__entry_name','designer_name__account_head_name','invoice_number').order_by('-id').exclude(tag_status=3))

        return Response(
            {
                "data":{
                    "list":queryset
                },
                "message":res_msg.retrieve("Lot List"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
    
    def post(self,request):
        request_data=request.data 

        search = request_data.get('search') if request_data.get('search') else ''
        tagging_status = request_data.get('tag_status') if request_data.get('tag_status') else None
        from_date = request_data.get('from_date') if request_data.get('from_date') else None
        to_date = request_data.get('to_date') if request_data.get('to_date') else None
        page = request.data.get('page') if request.data.get('page') else 1
        entry_type=request_data.get('entry_type') if request_data.get('entry_type') else None
        items_per_page = request.data.get('items_per_page') if request.data.get('items_per_page') else 10
        branch = request.data.get('branch') if request.data.get('branch') else None
        
        filter_dict={}

        if request.user.role.is_admin == True:
            if branch != None:            
                filter_dict['branch'] = branch
        else:
            filter_dict['branch'] = request.user.branch_id

        # try:
        #     items_per_page = int(request.data.get('items_per_page', Lot.objects.all().count()))
        #     if items_per_page == 0:
        #         items_per_page = 10 
        # except Exception as err:
        #     items_per_page = 10 

        
        combined_conditions = Q()
        if search != None :
            or_conditions = []
            or_conditions.append(Q(entry_type__entry_name__icontains=search))
            or_conditions.append(Q(designer_name__account_head_name__icontains=search))
            or_conditions.append(Q(invoice_number__icontains=search))

            for condition in or_conditions:
                combined_conditions |= condition
        if entry_type != None :

            filter_dict['entry_type'] = entry_type

        if tagging_status != None :
            filter_dict['tag_status'] = tagging_status

        if from_date != None and to_date != None :
            date_range=(from_date,to_date)
            filter_dict['entry_date__range'] = date_range

        if len(filter_dict) != 0 :

            queryset=list(Lot.objects.filter(combined_conditions, **filter_dict).order_by('-id'))

        else:
            queryset=list(Lot.objects.filter(combined_conditions).order_by('-id'))
        
        paginated_data = Paginator(queryset, items_per_page)
        serializer = LotSerializer(paginated_data.get_page(page), many=True)

        response_data=[]

        for data in queryset:

            try:
                staff = Staff.objects.get(user = data.created_by_id)
                username = staff.first_name

            except:
                username = '-'
                
            total_pieces = data.total_pieces if data.total_pieces != None else 0
            tagged_pieces = data.tagged_pieces if data.tagged_pieces != None else 0

            pending_pieces = int(total_pieces) - int(tagged_pieces)

            if data.invoice_number != None:
                invoice_number = data.invoice_number
            else:
                invoice_number = "-----"

            res_data={
                "id":data.pk,
                "lot_number":data.lot_number,
                "entry_date":data.entry_date,
                "entry_type":data.entry_type.entry_name,
                "designer_name":data.designer_name.account_head_name,
                "invoice_number":invoice_number,
                "total_pieces":data.total_pieces,
                "total_grossweight":data.total_grossweight,
                "total_netweight":data.total_netweight,
                "taging_status":data.tag_status.status_name,
                "tagged_pieces":data.tagged_pieces,
                "tagged_tag_count":data.tagged_tag_count,
                "tag_count":data.total_tag_count,
                "pending_pieces":pending_pieces,
                "status_id":data.tag_status.pk,
                "branch":data.branch.branch_name,
                "color":data.tag_status.color,
                "created_by":username,
                "total_tag_grossweight":data.tagged_grossweight,
                "total_tag_netweight":data.tagged_netweight,
            }

            response_data.append(res_data)

        return Response(
            {
                "data":{
                    "list":response_data,
                    "total_pages": paginated_data.num_pages,
                    "current_page": page,
                    "total_items": len(queryset),
                    "current_items": len(serializer.data)
                },
                "message":res_msg.retrieve("Lot Table"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
    

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class LotItemDeleteView(APIView):
     
    def delete(self,request,pk):

        item_delete_queryset=LotItem.objects.get(id=pk)

        stone_delete_queryset=LotItemStone.objects.filter(lot_item=pk)

        for stone_data in stone_delete_queryset:
            stone_data.delete()

        diamond_delete_queryset=LotItemDiamond.objects.filter(lot_item=pk)

        for diamond_data in diamond_delete_queryset:
            diamond_data.delete()

        item_delete_queryset.delete()
        
        return Response(
            {
                "message":res_msg.delete("Item Details"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class LotStoneDeleteView(APIView):
     
    def delete(self,request,pk):

        stonedelete_queryset=LotItemStone.objects.get(id=pk)

        stonedelete_queryset.delete()

        return Response(
            {
                "message":res_msg.delete("Stone Details"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class LotDiamondDeleteView(APIView):
     
    def delete(self,request,pk):

        diamonddelete_queryset=LotItemDiamond.objects.get(id=pk)

        diamonddelete_queryset.delete()

        return Response(
            {
                "message":res_msg.delete("Diamond Details"),
                "status":status.HTTP_200_OK                                                                                                                                                                                                                                                                                                                                                 
            },status=status.HTTP_200_OK
        )


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class TagNumberView(APIView):
    def get(self,request,pk): 
        response_data=[]
        
        for i in range(0,pk):

            starting_tag_number = 1000000
            existing_tag_numbers=TagNumber.objects.values_list('tag_number',flat=True)
            
            tag_number=starting_tag_number+random.randint(0,9000000)
            if tag_number not in existing_tag_numbers:
                tag_dict={}
                tag_dict['tag_number']=tag_number
                serializer=TagNumberSerializer(data=tag_dict)
                if serializer.is_valid():
                    serializer.save()
                    response_data.append(tag_number)
                    
        return Response(
            {
                "data":response_data,
                "message":res_msg.retrieve("Tag Number"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
    
    def delete(self,request,pk):

        queryset=TagNumber.objects.get(tag_number=pk)

        queryset.delete()

        return Response(
            {
                "message":res_msg.delete("Tag Number"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
    
    def post(self, request): 

        data = request.data 
        lotdetails =Lot.objects.get(id = data.get('lot_details'))
        remain_pieces = lotdetails.total_pieces-lotdetails.tagged_pieces
        remain_gross_weight = lotdetails.total_grossweight-lotdetails.tagged_grossweight
        remain_net_weight = lotdetails.total_netweight-lotdetails.tagged_netweight
        tagged_pieces = int(data.get('tagged_pieces'))
        tagged_grossweight = float(data.get('tagged_grossweight'))
        tag_netweight = float(data.get('tag_netweight'))
       
        if tagged_pieces > remain_pieces  :
            return Response({
                "message": "Tag Pieces greater than value "+ str(remain_pieces),
                "status": status.HTTP_204_NO_CONTENT
            }, status=status.HTTP_200_OK)
        elif tagged_grossweight > remain_gross_weight  :
            return Response({
                "message": "Tag gross weight greater than value "+ str(remain_gross_weight),
                "status": status.HTTP_204_NO_CONTENT
            }, status=status.HTTP_200_OK)
        elif tag_netweight > remain_net_weight  :

            return Response({
                "message": "Tag net weight greater than value "+ str(remain_net_weight),
                "status": status.HTTP_204_NO_CONTENT
            }, status=status.HTTP_200_OK)       
        else:
            response_data=[]
            for i in range(0,tagged_pieces):
                
                starting_tag_number = 1000000
                existing_tag_numbers=TagNumber.objects.values_list('tag_number',flat=True)

                tag_number=starting_tag_number+random.randint(0,9000000)
                if tag_number not in existing_tag_numbers:
                    tag_dict={}
                    # if data.get('entry_type') == settings.ORDER_ENTRY:
                    #     prefix = 'ORD'
                    #     tag_number_new=f'{prefix}{int(tag_number)}'
                    #     tag_dict['tag_number']=tag_number_new
                    #     print(tag_dict['tag_number'])
                    # else:
                    tag_dict['tag_number']=tag_number

                    serializer=TagNumberSerializer(data=tag_dict)
                    if serializer.is_valid():
                        serializer.save()
                        response_data.append(serializer.data['tag_number'])
                        
            return Response(
                {
                    "data":response_data,
                    "message":res_msg.retrieve("Tag Number"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        
def delete_tag_entry(pk):
    queryset=TagEntry.objects.get(id=pk)
    queryset.delete()

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class TagEntryViewset(viewsets.ViewSet):
    @transaction.atomic
    def create(self,request):

        try:

            request_data=request.data
            
            request_data['created_at']=timezone.now()
            request_data['created_by']=request.user.id

            if request.user.role.is_admin == False:
                branch = request.user.branch.pk
            else:
                branch = request_data.get('branch')

            request_data['branch'] = branch

            tag_entry_serializer=TagEntrySerializer(data=request_data)

            if tag_entry_serializer.is_valid():

                tag_entry_serializer.save()
    
                tag_item_details=request_data.get('tag_item_details') if request_data.get('tag_item_details') else []

                tag_item_id=[]
                for item in tag_item_details :
                    
                    tagged_gross_weight=0
                    tagged_item_pieces=0

                    item['halmark_huid'] = str(item['halmark_huid']) if item['halmark_huid'] else 0

                    item['halmark_center'] = item['halmark_center'] if item['halmark_center'] else None

                    item['tag_entry_details']=tag_entry_serializer.data['id']

                    item['gross_weight'] = 0 if item['gross_weight'] is None else float(item['gross_weight'])
                    item['tag_weight'] = 0 if item['tag_weight'] is None else float(item['tag_weight'])
                    item['cover_weight'] = 0 if item['cover_weight'] is None else float(item['cover_weight'])
                    item['loop_weight'] = 0 if item['loop_weight'] is None else float(item['loop_weight'])
                    item['other_weight'] = 0 if item['other_weight'] is None else float(item['other_weight'])

                    item['remaining_gross_weight'] = 0 if item['gross_weight'] is None else float(item['gross_weight'])

                    item['tag_pieces'] = int(item['tag_pieces'])
                    item['tag_count'] = int(item['tag_count'])
                    
                    item['remaining_pieces'] = int(item['tag_pieces'])
                    item['remaining_tag_count'] = int(item['tag_count'])
                    tagged_gross_weight += item['gross_weight']
                    tagged_item_pieces += item['tag_pieces']

                    item['stone_weight']=0
                    item['stone_rate']=0
                    item['rough_sale_value']=0
                    item['created_at']=timezone.now()
                    item['created_by']=request.user.id
                    item['branch']=branch

                    lot_item_queryset=LotItem.objects.get(id=item['item_details'])

                    if str(item['calculation_type']) == settings.FIXEDRATE :
                        
                        item['max_pergram_rate'] = 0
                        item['max_wastage_percent'] = 0 
                        item['max_flat_wastage'] = 0 
                        item['max_making_charge_gram'] = 0 
                        item['max_flat_making_charge'] = 0 

                    elif str(item['calculation_type']) == settings.PERGRAMRATE :

                        item['max_fixed_rate'] = 0
                        item['max_wastage_percent'] = 0 
                        item['max_flat_wastage'] = 0 
                        item['max_making_charge_gram'] = 0 
                        item['max_flat_making_charge'] = 0

                    elif str(item['calculation_type']) == settings.PERPIECERATE :

                        item['per_piece_rate'] = 0
                        item['min_per_piece_rate'] = 0 
                    
                    else:
                        
                        item['max_pergram_rate'] = 0
                        item['max_fixed_rate'] = 0 

                    tag_item_serializer=TaggedItemsSerializer(data=item)

                    if tag_item_serializer.is_valid():
                        tag_item_serializer.save()

                        tag_item_id.append(tag_item_serializer.data['id'])

                        stone_weight_calc=0
                        stone_rate_calc=0
                        stone_piece_calc=0
                        diamond_weight_calc=0
                        diamond_rate_calc=0
                        diamond_piece_calc=0

                        stone_details=item.get('stone_details') if item.get('stone_details') else []

                        for stone in stone_details:
                                            
                            tagged_stoneweight =0
                            tagged_stonepieces =0

                            stone['tag_details'] = tag_item_serializer.data['id']
                            stone['tag_entry_details'] = tag_entry_serializer.data['id']

                            stone['stone_weight']=float(stone['stone_weight'])      
                            stone['stone_rate']=float(stone['stone_rate'])
                            stone['stone_pieces']=int(stone['stone_pieces'])

                            if str(stone['stone_weight_type']) == settings.CARAT:
                                stone_weight = float(stone['stone_weight'])/5
                                stone['stone_weight'] = stone_weight

                            if str(stone['stone_rate_type'])==settings.PERGRAM:
                                total_stone_value=float(stone['stone_rate']*stone['stone_weight'])

                            if str(stone['stone_rate_type']) == settings.PERCARAT:
                                stone_rate = float(stone['stone_rate'])*5
                                stone['stone_rate'] = stone_rate
                                total_stone_value=float(stone['stone_rate']*stone['stone_weight'])

                            if str(stone['stone_rate_type'])==settings.PERPIECE:
                                total_stone_value=float(stone['stone_rate']*stone['stone_pieces'])

                            stone_rate_calc += total_stone_value
                            stone_piece_calc += int(stone['stone_pieces'])


                            if stone['include_stone_weight'] == True :
                                stone_weight_calc += float(stone['stone_weight'])

                            stone['total_stone_value']=total_stone_value

                            tagged_stoneweight += float(stone['stone_weight'])
                            tagged_stonepieces += int(stone['stone_pieces'])

                            tag_stone_serializer=TaggedItemStoneSerializer(data=stone)

                            if tag_stone_serializer.is_valid():
                                                
                                tag_stone_serializer.save()

                                try:
                            
                                    lot_stone_queryset=LotItemStone.objects.get(id=stone['stone_name'])


                                    data={
                                        'tagged_stoneweight':lot_stone_queryset.tagged_stone_weight+tagged_stoneweight,
                                        'tagged_stonepieces':lot_stone_queryset.tagged_stone_pieces+tagged_stonepieces
                                        }

                                    lot_stone_serializer=LotItemStoneSerializer(lot_stone_queryset,data=data,partial=True)

                                    if lot_stone_serializer.is_valid():
                                        lot_stone_serializer.save()
                            
                                except:
                                    pass

                            else:
                                raise Exception(tag_stone_serializer.errors)


                        diamond_details=item.get('diamond_details') if item.get('diamond_details') else []

                        for diamond in diamond_details :
                                    
                                            
                            tagged_diamondweight =0
                            tagged_diamondPieces =0


                            diamond['tag_details'] = tag_item_serializer.data['id']
                            diamond['tag_entry_details'] = tag_entry_serializer.data['id']

                            diamond['diamond_weight'] = float(diamond['diamond_weight'])
                            diamond['diamond_rate'] = float(diamond['diamond_rate'])
                            diamond['diamond_pieces'] = int(diamond['diamond_pieces'])

                            if str(diamond['diamond_weight_type']) == settings.CARAT :
                                diamond_weight=float(diamond['diamond_weight'])/5
                                diamond['diamond_weight']=diamond_weight


                            if str(diamond['diamond_rate_type'])==settings.PERGRAM:
                                total_diamond_value=float(diamond['diamond_rate']*diamond['diamond_weight'])

                            if str(diamond['diamond_rate_type']) == settings.PERCARAT:
                                diamond_rate=float(diamond['diamond_rate'])*5
                                diamond['diamond_rate']=diamond_rate
                                total_diamond_value=float(diamond['diamond_rate']*diamond['diamond_weight'])

                            if str(diamond['diamond_rate_type'])==settings.PERPIECE:
                                total_diamond_value=float(diamond['diamond_rate']*diamond['diamond_pieces'])

                            diamond_rate_calc += total_diamond_value
                            diamond_piece_calc += diamond['diamond_pieces']

                            if diamond['include_diamond_weight'] == True :
                                diamond_weight_calc += (diamond['diamond_weight'])

                            tagged_diamondweight += diamond['diamond_weight']
                            tagged_diamondPieces += diamond['diamond_pieces']


                            diamond['total_diamond_value']=total_diamond_value
                            tag_diamond_serializer=TaggedItemDiamondSerializer(data=diamond)

                            if tag_diamond_serializer.is_valid():
                                tag_diamond_serializer.save()

                                try:

                                    lot_diamond_queryset=LotItemDiamond.objects.get(id=diamond['diamond_name'])

                                    data={
                                        'tagged_diamondweight':lot_diamond_queryset.tagged_diamond_weight+tagged_diamondweight,
                                        'tagged_diamondPieces':lot_diamond_queryset.tagged_diamond_pieces+tagged_diamondweight
                                        }

                                    lot_diamond_serializer=LotItemDiamondSerializer(lot_diamond_queryset,data=data,partial=True)

                                    if lot_diamond_serializer.is_valid():
                                        lot_diamond_serializer.save()

                                except:
                                    pass

                            else:
                                raise Exception(tag_diamond_serializer.errors)

                    
                        net_weight=tag_item_serializer.data['gross_weight']-(tag_item_serializer.data['tag_weight']+tag_item_serializer.data['cover_weight']+tag_item_serializer.data['loop_weight']+tag_item_serializer.data['other_weight']+stone_weight_calc+diamond_weight_calc)
                        
                        lot_item_data_dict={}

                        lot_item_data_dict['tagged_grossweight'] = float(lot_item_queryset.tagged_grossweight) + tag_item_serializer.data['gross_weight']
                        lot_item_data_dict['tagged_pieces'] = float(lot_item_queryset.tagged_pieces) + tag_item_serializer.data['tag_pieces']
                        lot_item_data_dict['tagged_netweight'] = lot_item_queryset.tagged_netweight +  net_weight
                        lot_item_data_dict['tagged_tag_count'] = lot_item_queryset.tagged_tag_count + tag_item_serializer.data['tag_count']

                        
                        lot_item_calc_serializer = LotItemSerializer(lot_item_queryset,data=lot_item_data_dict,partial=True)

                        if lot_item_calc_serializer.is_valid():
                            lot_item_calc_serializer.save()

                        calc_dict={}
                        
                        calc_dict['remaining_net_weight'] = net_weight
                        calc_dict['net_weight']=net_weight
                        calc_dict['stone_weight']=stone_weight_calc
                        calc_dict['stone_rate']=stone_rate_calc
                        calc_dict['stone_pieces']=stone_piece_calc
                        calc_dict['diamond_weight']=diamond_weight_calc
                        calc_dict['diamond_rate']=diamond_rate_calc
                        calc_dict['diamond_pieces']=diamond_piece_calc
                        

                        if str(item['calculation_type']) == settings.WEIGHTCALCULATION:
                                    
                            sub_item_queryset=SubItem.objects.get(id=item['sub_item_details'])

                            sub_weight_queryset=SubItemWeightCalculation.objects.get(sub_item_details=sub_item_queryset.pk)

                            try:
                                # metal=str(sub_item_queryset.metal.metal_name)

                                # purity=str(sub_item_queryset.purity.purity_name)

                                # metal_purity=metal+'_'+purity

                                # metal_rate_queryset=MetalRate.objects.all().order_by('-id')[0]

                                # metal_rate = float(metal_rate_queryset.rate[metal_purity])
                                metal_rate_queryset = MetalRate.objects.filter(purity=sub_item_queryset.purity.pk).order_by('-id')[0]
                                metal_rate = metal_rate_queryset.rate
                            except:
                                metal_rate = 0

                            metal_value=(float(metal_rate)*float(net_weight))

                            if str(sub_weight_queryset.wastage_calculation.pk) == settings.GROSSWEIGHT :

                                wastage=float((float(item['gross_weight']) * (float(item['min_wastage_percent']) / 100)) * float(metal_rate))

                            else:

                                wastage=float((float(net_weight) * (float(item['min_wastage_percent']) / 100)) * float(metal_rate))


                            flat_wastage=float(item['min_flat_wastage'])

                            if str(sub_weight_queryset.making_charge_calculation.pk) == settings.GROSSWEIGHT :

                                making_charge=(float(item['min_making_charge_gram']) * float(item['gross_weight']))

                            else:

                                making_charge=(float(item['min_making_charge_gram']) * float(net_weight))


                            flat_making_charge=float(item['min_flat_making_charge'])

                            stone_value=stone_rate_calc

                            diamond_value=diamond_rate_calc

                            sale_value=float(metal_value+wastage+flat_wastage+making_charge+flat_making_charge+stone_value+diamond_value)

                        elif str(item['calculation_type']) == settings.PERGRAMRATE:

                            if str(item['per_gram_weight_type']) == settings.GROSSWEIGHT:

                                sale_value = float((float(item['gross_weight'])) * float(item['min_pergram_rate'] + stone_rate_calc + diamond_rate_calc))

                            else:

                                sale_value = float((float(net_weight) * float(item['min_pergram_rate'])) + stone_rate_calc + diamond_rate_calc)
                        
                        elif str(item['calculation_type']) == settings.PERPIECERATE: 
                            calc_dict['min_per_piece_rate']=item['min_per_piece_rate']
                            calc_dict['per_piece_rate']=item['per_piece_rate']

                        else:
                                    
                            sale_value=float(item['min_fixed_rate']+ stone_rate_calc + diamond_rate_calc)

                        calc_dict['rough_sale_value']=sale_value
                        calc_dict['net_weight']=net_weight

                        tag_calc_queryset=TaggedItems.objects.get(id=tag_item_serializer.data['id'])
                        
                        tag_calc_serializer=TaggedItemsSerializer(tag_calc_queryset,data=calc_dict,partial=True)

                        if tag_calc_serializer.is_valid():
                            tag_calc_serializer.save()

                        else:
                            raise Exception(tag_calc_serializer.errors)
                        
                    else:
                        raise Exception(tag_item_serializer.errors)

                    
                tagged_grossweight = 0
                tagged_netweight = 0
                tagged_pieces = 0
                tagged_stone_pieces = 0
                tagged_stone_weight = 0
                tagged_diamond_pieces = 0
                tagged_diamond_weight = 0
                tagged_tag_count = 0
                    
                item_queryset=list(TaggedItems.objects.filter(tag_entry_details=tag_entry_serializer.data['id']))
        
                for i in item_queryset :
                    tagged_grossweight += float(i.gross_weight)
                    tagged_netweight += float(i.net_weight)
                    tagged_pieces += int(i.tag_pieces)
                    tagged_tag_count += int(i.tag_count)

                    stone_queryset=list(TaggedItemStone.objects.filter(tag_details=i.pk))
        
                    for s in stone_queryset:
                        
                        tagged_stone_pieces += int(s.stone_pieces)
                        tagged_stone_weight += float(s.stone_weight)
        
                    diamond_queryser=list(TaggedItemDiamond.objects.filter(tag_details=i.pk))
        
                    for d in diamond_queryser :
                        
                        tagged_diamond_pieces += int(d.diamond_pieces)
                        tagged_diamond_weight += float(d.diamond_weight)
                    
                lot_queryset=Lot.objects.get(id=tag_entry_serializer.data['lot_details'])

                stock_ledger_data = {}
                            
                stock_ledger_data['tag_details'] = tag_item_serializer.data['id']
                stock_ledger_data['stock_type'] = settings.IN
                stock_ledger_data['entry_type'] = lot_queryset.entry_type.pk
                stock_ledger_data['entry_date'] = timezone.now()
                stock_ledger_data['pieces'] = tag_item_serializer.data['tag_pieces']
                stock_ledger_data['gross_weight'] = tag_item_serializer.data['gross_weight']
                
                stock_ledger_serializer = StockLedgerSerializer(data=stock_ledger_data)
                
                if stock_ledger_serializer.is_valid():
                    stock_ledger_serializer.save()
                else:
                    raise Exception(stock_ledger_serializer.errors)
                

                old_tagged_grossweight=lot_queryset.tagged_grossweight
                old_tagged_netweight=lot_queryset.tagged_netweight
                old_tagged_pieces=lot_queryset.tagged_pieces
                old_tagged_stone_pieces=lot_queryset.tagged_stone_pieces
                old_tagged_stone_weight=lot_queryset.tagged_stone_weight
                old_tagged_diamond_pieces=lot_queryset.tagged_diamond_pieces
                old_tagged_diamond_weight=lot_queryset.tagged_diamond_weight
                old_tagged_tag_count=lot_queryset.tagged_tag_count
                    
                lot_calc={
                    'tagged_grossweight' :tagged_grossweight+old_tagged_grossweight,
                    'tagged_netweight' :tagged_netweight+old_tagged_netweight,
                    'tagged_pieces' :tagged_pieces+old_tagged_pieces,
                    'tagged_stone_pieces' : tagged_stone_pieces+old_tagged_stone_pieces,
                    'tagged_stone_weight' :tagged_stone_weight+old_tagged_stone_weight,
                    'tagged_diamond_pieces' : tagged_diamond_pieces+old_tagged_diamond_pieces,
                    'tagged_diamond_weight' :tagged_diamond_weight+old_tagged_diamond_weight,
                    'tagged_tag_count' :tagged_tag_count+old_tagged_tag_count,
                }
        
                lot_serializer=LotSerializer(lot_queryset,data=lot_calc,partial=True)
        
                if lot_serializer.is_valid():
                    lot_serializer.save()

                if lot_queryset.tagged_tag_count == 0:
                    status_queryset= StatusTable.objects.get(id=int(settings.PENDING))
                    lot_queryset.tag_status = status_queryset
                elif 0 <  lot_queryset.tagged_tag_count < lot_queryset.total_tag_count:
                    status_queryset= StatusTable.objects.get(id=int(settings.PARTIAL))
                    lot_queryset.tag_status = status_queryset
                elif lot_queryset.tagged_tag_count>=lot_queryset.total_tag_count :
                    status_queryset= StatusTable.objects.get(id=int(settings.COMPLETED))
                    lot_queryset.tag_status = status_queryset

                lot_queryset.save()

                return Response(
                    {
                        "data":tag_entry_serializer.data,
                        "message":res_msg.create("Tag Entry"),
                        "status":status.HTTP_200_OK
                    },status=status.HTTP_200_OK
                )
            
            else:
                return Response(
                    {
                        "data":tag_entry_serializer.errors,
                        "message":res_msg.not_create("Tag Details"),
                        "status":status.HTTP_400_BAD_REQUEST
                    },status=status.HTTP_200_OK
                )
        except Exception as err:
            # delete_tag_entry(pk=tag_entry_serializer.data['id'])
            transaction.set_rollback(True)
            return Response(
                {
                    "data":str(err),
                    "message":res_msg.something_else(),
                    "stauts":status.HTTP_400_BAD_REQUEST
                },status=status.HTTP_200_OK
            )
        

    def retrieve(self,request,pk):
        response_dict={}

        try:
         
            tag_entry_queryset=TagEntry.objects.get(id=pk)

            tag_entry_details={
                "id":pk,
                "lot_number":tag_entry_queryset.lot_details.lot_number,
                "entry_type":tag_entry_queryset.lot_details.entry_type.entry_name,
                "vendor_name":tag_entry_queryset.lot_details.designer_name.account_head_name,
                "invoice_number":tag_entry_queryset.lot_details.invoice_number
            }

            response_dict['tag_entry_details']=tag_entry_details

        except Exception as err:
            pass

        try:

            tag_item_queryset=list(TaggedItems.objects.filter(tag_entry_details=pk))

            item_details=[]

            for item in tag_item_queryset:

                item_dict={
                    "id":item.pk,
                    "tag_number":item.tag_number,
                    "item_details":item.item_details.item_details.pk,
                    "item_details_name":item.item_details.item_details.item_name,
                    "sub_item_details":item.sub_item_details.pk,
                    "sub_item_details_name":item.sub_item_details.sub_item_name,
                    "mesaurement_type":item.sub_item_details.measurement_type.pk,
                    "mesaurement_type_name":item.sub_item_details.measurement_type.measurement_name,
                    "size_value":item.size_value,
                    "tag_type":item.tag_type.pk,
                    "tag_type_name":item.tag_type.tag_name,
                    "tag_pieces":item.tag_pieces,
                    "tag_count":item.tag_count,
                    "gross_weight":item.gross_weight,
                    "net_weight":item.net_weight,
                    "tag_weight":item.tag_weight,
                    "cover_weight":item.cover_weight,
                    "loop_weight":item.loop_weight,
                    "other_weight":item.other_weight,
                    "calculation_type":item.calculation_type.pk,
                    "calculation_type_name":item.calculation_type.calculation_name,
                    "rough_sale_value":item.rough_sale_value,
                    "halmark_huid":item.halmark_huid,
                    "halmark_center":item.halmark_center,
                    "display_counter":item.display_counter.pk,
                    "display_counter_name":item.display_counter.counter_name,
                }

                if str(item.calculation_type.pk) == settings.FIXEDRATE :

                    item_dict['min_fixed_rate']=item.min_fixed_rate
                    item_dict['max_fixed_rate']=item.max_fixed_rate

                elif str(item.calculation_type.pk) == settings.PERGRAMRATE :

                    item_dict['min_pergram_rate']=item.min_pergram_rate
                    item_dict['max_pergram_rate']=item.max_pergram_rate

                elif str(item.calculation_type.pk) == settings.PERPIECERATE :

                    item_dict['min_per_piece_rate']=item.min_per_piece_rate
                    item_dict['per_piece_rate']=item.per_piece_rate
                
                else:

                    item_dict['min_wastage_percent']=item.min_wastage_percent
                    item_dict['min_flat_wastage']=item.min_flat_wastage
                    item_dict['min_making_charge_gram']=item.min_making_charge_gram
                    item_dict['min_flat_making_charge']=item.min_flat_making_charge
                    
                    item_dict['max_wastage_percent']=item.max_wastage_percent
                    item_dict['max_flat_wastage']=item.max_flat_wastage
                    item_dict['max_making_charge_gram']=item.max_making_charge_gram
                    item_dict['max_flat_making_charge']=item.max_flat_making_charge

                stone_details=[]
                diamond_details=[]

                try:

                    stone_queryset=list(TaggedItemStone.objects.filter(tag_entry_details=pk,tag_details=item.pk))

                    for stone in stone_queryset :

                        stone_dict={
                            "id":stone.pk,
                            "stone_name":stone.stone_name.stone_name.stone_name,
                            "stone_pieces":stone.stone_pieces,
                            "stone_weight":stone.stone_weight,
                            "stone_weight_type":stone.stone_weight_type.weight_name,
                            "stone_rate":stone.stone_rate,
                            "stone_rate_type":stone.stone_rate_type.type_name,
                            "include_stone_weight":stone.include_stone_weight
                        }

                        if str(stone.stone_weight_type.pk) == settings.CARAT :

                            stone_dict['stone_weight']=float(stone.stone_weight*5)

                        if str(stone.stone_rate_type.pk) == settings.PERCARAT :

                            stone_dict['stone_rate']=float(stone.stone_rate/5)

                        stone_details.append(stone_dict)

                except Exception as err:
                    pass

                try:
                
                    diamond_queryset=list(TaggedItemDiamond.objects.filter(tag_entry_details=pk,tag_details=item.pk))

                    for diamond in diamond_queryset:

                        diamond_dict={
                            "id":diamond.pk,
                            "diamond_name":diamond.diamond_name.diamond_name.stone_name,
                            "diamond_pieces":diamond.diamond_pieces,
                            "diamond_weight":diamond.diamond_weight,
                            "diamond_weight_type":diamond.diamond_weight_type.weight_name,
                            "diamond_rate":diamond.diamond_rate,
                            "diamond_rate_type":diamond.diamond_rate_type.type_name,
                            "include_diamond_weight":diamond.include_diamond_weight
                        }

                        if str(diamond.diamond_weight_type.pk) == settings.CARAT :

                            diamond_dict['diamond_weight']=(float(diamond.diamond_weight)*5)
                        
                        if str(diamond.diamond_rate_type.pk) == settings.PERCARAT :

                            diamond_dict['diamond_rate']=(float(diamond.diamond_rate)/5)

                        diamond_details.append(diamond_dict)

                    item_dict['stone_details']=stone_details
                    item_dict['diamond_details']=diamond_details
                    
                    item_details.append(item_dict)

                except :
                    pass

            response_dict['tag_entry_details']['item_details']=item_details

            response_dict['tag_entry_details']=tag_entry_details

        except Exception as err:
            pass
        
        return Response(
            {
                "data":response_dict,
                "message":res_msg.retrieve("Tag Details"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
    

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class TagEntryListView(APIView):
    def get(self,request,branch=None):

        filter_dict={}
        if request.user.role.is_admin == True:
            if branch != None:            
                filter_dict['branch'] = branch
        else:
            filter_dict['branch'] = request.user.branch.pk
            
        filter_dict['is_billed'] = False
    
        tag_queryset=list(TaggedItems.objects.filter(**filter_dict).values('id','tag_number').order_by('-id'))

        return Response(
            {
                "data":{
                    "list":tag_queryset
                },
                "message":res_msg.retrieve("Tag List"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )


    def post(self,request):

        search = request.data.get('search') if request.data.get('search') else ''
        from_date = request.data.get('from_date') if request.data.get('from_date') else None
        to_date = request.data.get('to_date') if request.data.get('to_date') else None
        page = request.data.get('page') if request.data.get('page') else 1
        items_per_page = request.data.get('items_per_page') if request.data.get('items_per_page') else 10
        branch = request.data.get('branch') if request.data.get('branch') else None
        
        filter_dict={}

        if request.user.role.is_admin == True:
            if branch != None:            
               filter_dict['branch'] = branch
        else:
            filter_dict['branch'] = request.user.branch.pk
        # try:
        #     items_per_page = int(request.data.get('items_per_page', TagEntry.objects.all().count()))
        #     if items_per_page == 0:
        #         items_per_page = 10 
        # except Exception as err:
        #     items_per_page = 10 
        

        if from_date != None and to_date!= None:
           fdate =from_date+'T00:00:00.899010+05:30'
           tdate =to_date+'T23:59:59.899010+05:30'
           date_range=(fdate,tdate)
           filter_dict['created_at__range']=date_range

        
        if len(filter_dict) != 0 :

            queryset=(TagEntry.objects.filter(**filter_dict)).order_by('-id')

        else:

            queryset=list(TagEntry.objects.all().order_by('-id'))

        paginated_data = Paginator(queryset, items_per_page)
        serializer = TagEntrySerializer(paginated_data.get_page(page), many=True)

        response_data=[]

        for data in queryset:

            try:
                staff = Staff.objects.get(user = data.created_by_id)
                username = staff.first_name
            except:
                username = "-"

            res_dict={
                "id":data.pk,
                "lot_details__lot_number":data.lot_details.lot_number,
                "created_at":data.created_at,
                "branch":data.branch.branch_name,
                "entry_type":data.lot_details.entry_type.entry_name,
                "designer_name":data.lot_details.designer_name.account_head_name,
                "total_pieces":data.lot_details.total_pieces,
                "tagged_pieces":data.lot_details.tagged_pieces,
                "tag_count":data.lot_details.total_tag_count,
                "tagged_tag_count":data.lot_details.tagged_tag_count,
                "pending_pieces":data.lot_details.total_pieces-data.lot_details.tagged_pieces,
                "gross_weight":data.lot_details.total_grossweight,
                "net_weight":data.lot_details.total_netweight,
                "entry_date":data.lot_details.entry_date,
                "tagging_status":data.lot_details.tag_status.status_name,
                "status_colour":data.lot_details.tag_status.color,
                "created_by":username
            }

            try:
                staff_queryset=Staff.objects.get(phone=data.created_by.phone)
                res_dict["created_by"] = str(staff_queryset.first_name)+" "+str(staff_queryset.last_name)
            except Exception as err:
                res_dict["created_by"] = "--"

            response_data.append(res_dict)

        return Response(
            {
                "data":{
                    "list":response_data,
                    "total_pages": paginated_data.num_pages,
                    "current_page": page,
                    "total_items": len(queryset),
                    "current_items": len(serializer.data)
                },
                "message":res_msg.retrieve("Tag Entry Table"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
    

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class TagItemViewset(viewsets.ViewSet):
    def retrieve(self,request,pk):

        try:

            tag_item_queryset=TaggedItems.objects.get(tag_number=pk,is_billed=False)
            
            res_data={
                "id":tag_item_queryset.pk,
                "tagged_date":tag_item_queryset.created_at,
                "lot_number":tag_item_queryset.tag_entry_details.lot_details.lot_number,
                "entry_type":tag_item_queryset.tag_entry_details.lot_details.entry_type.entry_name,
                "stock_type":tag_item_queryset.sub_item_details.stock_type.pk,
                "stock_type_name":tag_item_queryset.sub_item_details.stock_type.stock_type_name,
                "tag_type":tag_item_queryset.tag_type.tag_name,
                "invoice_number":tag_item_queryset.tag_entry_details.lot_details.invoice_number,
                "item_name":tag_item_queryset.item_details.item_details.item_name,
                "sub_item_name":tag_item_queryset.sub_item_details.sub_item_name,
                "item_details":tag_item_queryset.item_details.item_details.pk,
                "item_huid_rate":tag_item_queryset.item_details.item_details.huid_rate,
                "sub_item_details":tag_item_queryset.sub_item_details.pk,
                "assigned_counter":tag_item_queryset.display_counter.counter_name,
                "pieces":tag_item_queryset.tag_pieces,
                "size":tag_item_queryset.size_value,
                "gross_weight":tag_item_queryset.gross_weight,
                "net_weight":tag_item_queryset.net_weight,
                "tag_weight":tag_item_queryset.tag_weight,
                "cover_weight":tag_item_queryset.cover_weight,
                "loop_weight":tag_item_queryset.loop_weight,
                "other_weight":tag_item_queryset.other_weight,
                "calculation_type":tag_item_queryset.calculation_type.pk,
                "calculation_type_name":tag_item_queryset.calculation_type.calculation_name,
                "item_metal_id":tag_item_queryset.item_details.item_details.metal.pk,
                "item_metal_name":tag_item_queryset.item_details.item_details.metal.metal_name,
                "sub_item_metal_id":tag_item_queryset.sub_item_details.metal.pk,
                "sub_item_metal_name":tag_item_queryset.sub_item_details.metal.metal_name,
                "item_purity_id":tag_item_queryset.item_details.item_details.purity.pk,
                "item_purity_name":tag_item_queryset.item_details.item_details.purity.purity_name,
                "sub_item_purity_id":tag_item_queryset.sub_item_details.purity.pk,
                "sub_item_purity_name":tag_item_queryset.sub_item_details.purity.purity_name,
                "stone_rate":tag_item_queryset.stone_rate,
                "diamond_rate":tag_item_queryset.diamond_rate,
                "total_stone_weight":tag_item_queryset.stone_weight,
                "total_diamond_weight":tag_item_queryset.diamond_weight,
                'remaining_pieces':tag_item_queryset.remaining_pieces,
                'remaining_gross_weight':tag_item_queryset.remaining_gross_weight,
                'remaining_net_weight':tag_item_queryset.remaining_net_weight,
                'remaining_tag_count':tag_item_queryset.remaining_tag_count,
                'is_billed':tag_item_queryset.is_billed
            }

            

            today=timezone.now()
            created_date=tag_item_queryset.created_at

            age=relativedelta(today, created_date)

            years, months, days = age.years, age.months, age.days

            res_data['item_age']=f"{years} years, {months} months, and {days} days"
                    
            
            if str(tag_item_queryset.calculation_type.pk)==settings.FIXEDRATE:

                res_data['min_fixed_rate']=tag_item_queryset.min_fixed_rate 
                res_data['max_fixed_rate']=tag_item_queryset.max_fixed_rate

                res_data['min_sale_value']=(tag_item_queryset.min_fixed_rate + tag_item_queryset.stone_rate + tag_item_queryset.diamond_rate)
                res_data['max_sale_value']=(tag_item_queryset.max_fixed_rate + tag_item_queryset.stone_rate + tag_item_queryset.diamond_rate)
            
            elif str(tag_item_queryset.calculation_type.pk)==settings.PERPIECERATE:
                res_data['min_per_piece_rate']=tag_item_queryset.min_per_piece_rate
                res_data['per_piece_rate']=tag_item_queryset.per_piece_rate          

                res_data['min_per_piece_rate']=tag_item_queryset.min_per_piece_rate  
                res_data['max_per_piece_rate']=tag_item_queryset.max_per_piece_rate  
                min_rate =  tag_item_queryset.tag_pieces * tag_item_queryset.min_per_piece_rate
                max_rate =  tag_item_queryset.tag_pieces * tag_item_queryset.max_per_piece_rate
                res_data['min_sale_value']=(min_rate + tag_item_queryset.stone_rate + tag_item_queryset.diamond_rate)
                res_data['max_sale_value']=(max_rate + tag_item_queryset.stone_rate + tag_item_queryset.diamond_rate)     

            elif str(tag_item_queryset.calculation_type.pk)==settings.PERGRAMRATE:
                res_data['min_pergram_rate']=tag_item_queryset.min_pergram_rate
                res_data['max_pergram_rate']=tag_item_queryset.max_pergram_rate
                res_data['per_gram_weight_type']=tag_item_queryset.per_gram_weight_type.pk
                res_data['per_gram_weight_type_name']=tag_item_queryset.per_gram_weight_type.weight_name

                if str(tag_item_queryset.per_gram_weight_type.pk) == settings.GROSSWEIGHT :

                    min_per_gram_value=float(tag_item_queryset.gross_weight) * float(tag_item_queryset.min_pergram_rate)
                    max_per_gram_value=float(tag_item_queryset.gross_weight) * float(tag_item_queryset.max_pergram_rate)

                else:

                    min_per_gram_value=float(tag_item_queryset.net_weight) * float(tag_item_queryset.min_pergram_rate)
                    max_per_gram_value=float(tag_item_queryset.net_weight) * float(tag_item_queryset.max_pergram_rate)

                res_data['min_sale_value']=(min_per_gram_value + tag_item_queryset.stone_rate + tag_item_queryset.diamond_rate)
                res_data['max_sale_value']=(max_per_gram_value + tag_item_queryset.stone_rate + tag_item_queryset.diamond_rate)
                
            else:
                try:

                    # metal=str(tag_item_queryset.sub_item_details.metal.metal_name)

                    # purity=str(tag_item_queryset.sub_item_details.purity.purity_name)
 
                    # metal_purity=metal+'_'+purity


                    # metal_rate_queryset=MetalRate.objects.all().order_by('-id')[0]

                    # metal_rate=float(metal_rate_queryset.rate[metal_purity])

                    # metal_rate = 0 if metal_rate is None else float(metal_rate)

                    metal_rate_queryset = MetalRate.objects.filter(purity=tag_item_queryset.sub_item_details.purity.pk).order_by('-id')[0]
                    metal_rate = metal_rate_queryset.rate

                except Exception as err:

                    metal_rate=0

                #min sale value calculation

                metal_value=(float(metal_rate)*float(tag_item_queryset.net_weight))
                
                sub_wastage_queryset=SubItemWeightCalculation.objects.get(sub_item_details=tag_item_queryset.sub_item_details.pk)

                res_data['making_charge_calculation_type'] = sub_wastage_queryset.making_charge_calculation.pk
                res_data['wastage_calculation_type'] = sub_wastage_queryset.wastage_calculation.pk

                if str(sub_wastage_queryset.wastage_calculation.pk) == settings.GROSSWEIGHT :

                    min_wastage_value=((tag_item_queryset.gross_weight*tag_item_queryset.min_wastage_percent)/100)*metal_rate

                else:

                    min_wastage_value=((tag_item_queryset.net_weight*tag_item_queryset.min_wastage_percent)/100)*metal_rate

                min_flat_wastage=tag_item_queryset.min_flat_wastage

                if str(sub_wastage_queryset.making_charge_calculation.pk) == settings.GROSSWEIGHT :

                    min_making_Charge=(tag_item_queryset.min_making_charge_gram*tag_item_queryset.gross_weight)

                else:

                    min_making_Charge=(tag_item_queryset.min_making_charge_gram*tag_item_queryset.net_weight)


                min_flat_making_charge=tag_item_queryset.min_flat_making_charge

                min_sale_value = metal_value + min_wastage_value + min_flat_wastage + min_making_Charge + min_flat_making_charge + tag_item_queryset.stone_rate + tag_item_queryset.diamond_rate

                #max sale value calculation

                if str(sub_wastage_queryset.wastage_calculation.pk) == settings.GROSSWEIGHT :

                    max_wastage_value=((tag_item_queryset.gross_weight * tag_item_queryset.max_wastage_percent)/100)*metal_rate

                else:

                    max_wastage_value=((tag_item_queryset.net_weight * tag_item_queryset.max_wastage_percent)/100)*metal_rate


                max_flat_wastage=tag_item_queryset.max_flat_wastage

                if str(sub_wastage_queryset.making_charge_calculation.pk) == settings.GROSSWEIGHT :

                    max_making_Charge=(tag_item_queryset.max_making_charge_gram * tag_item_queryset.gross_weight)
                
                else:

                    max_making_Charge=(tag_item_queryset.max_making_charge_gram * tag_item_queryset.net_weight)

                
                max_flat_making_charge=tag_item_queryset.max_flat_making_charge
                
                max_sale_value = metal_value + max_wastage_value + max_flat_wastage + max_making_Charge + max_flat_making_charge + tag_item_queryset.stone_rate + tag_item_queryset.diamond_rate
                
                res_data['metal_rate']=metal_rate
                res_data['min_wastage_percent']=tag_item_queryset.min_wastage_percent
                res_data['min_flat_wastage']=tag_item_queryset.min_flat_wastage
                res_data['max_wastage_percent']=tag_item_queryset.max_wastage_percent
                res_data['max_flat_wastage']=tag_item_queryset.max_flat_wastage
                res_data['min_making_charge_gram']=tag_item_queryset.min_making_charge_gram
                res_data['min_flat_making_charge']=tag_item_queryset.min_flat_making_charge
                res_data['max_making_charge_gram']=tag_item_queryset.max_making_charge_gram
                res_data['max_flat_making_charge']=tag_item_queryset.max_flat_making_charge

                res_data['min_sale_value']=min_sale_value
                res_data['max_sale_value']=max_sale_value
                
            try:
                tax_queryset = TaxDetailsAudit.objects.filter(metal=tag_item_queryset.sub_item_details.metal).order_by('-id').first()
                if tax_queryset:
                    tax_percent_queryset = SalesTaxDetails.objects.get(tax_details=tax_queryset.tax_details)
                    res_data['sales_tax_igst']=tax_percent_queryset.sales_tax_igst
                    res_data['sales_tax_cgst']=tax_percent_queryset.sales_tax_cgst
                    res_data['sales_tax_sgst']=tax_percent_queryset.sales_tax_sgst
                    res_data['sales_surcharge_percent']=tax_percent_queryset.sales_surcharge_percent
                    res_data['sales_additional_charges'] = tax_percent_queryset.sales_additional_charges
            except Exception as err:
                res_data['sales_tax_igst']=0
                res_data['sales_tax_cgst']=0
                res_data['sales_tax_sgst']=0
                res_data['sales_surcharge_percent']=0
                res_data['sales_additional_charges'] = 0
            
            stone_details=[]
            stone_queryset=list(TaggedItemStone.objects.filter(tag_details=tag_item_queryset.pk))

            for stone in stone_queryset :

                stone_dict={
                    "stone_name":stone.stone_name.stone_name.pk,
                    "stone_pieces":stone.stone_pieces,
                    "stone_weight":stone.stone_weight,
                    "stone_weight_type":stone.stone_weight_type.pk,
                    "stone_weight_type_name":stone.stone_weight_type.weight_name,
                    "stone_rate":stone.stone_rate,
                    "stone_rate_type":stone.stone_rate_type.pk,
                    "stone_rate_type_name":stone.stone_rate_type.type_name,
                    "include_stone_weight":stone.include_stone_weight
                }

                if str(stone.stone_weight_type.pk) == settings.CARAT :

                    stone_dict['stone_weight']=float(stone.stone_weight*5)

                if str(stone.stone_rate_type.pk) == settings.PERCARAT :

                    stone_dict['stone_rate']=float(stone.stone_rate/5)

                stone_details.append(stone_dict)
            
            diamond_details=[]
            diamond_queryset=TaggedItemDiamond.objects.filter(tag_details=tag_item_queryset.pk)

            for diamond in diamond_queryset:

                diamond_dict={
                    "diamond_name":diamond.diamond_name.diamond_name.pk,
                    "diamond_pieces":diamond.diamond_pieces,
                    "diamond_weight":diamond.diamond_weight,
                    "diamond_weight_type":diamond.diamond_weight_type.pk,
                    "diamond_weight_type_name":diamond.diamond_weight_type.weight_name,
                    "diamond_rate":diamond.diamond_rate,
                    "diamond_rate_type":diamond.diamond_rate_type.pk,
                    "diamond_rate_type_name":diamond.diamond_rate_type.type_name,
                    "include_diamond_weight":diamond.include_diamond_weight
                }

                if str(diamond.diamond_weight_type.pk) == settings.CARAT :

                    diamond_dict['diamond_weight']=(float(diamond.diamond_weight)*5)
                    
                if str(diamond.diamond_rate_type.pk) == settings.PERCARAT :

                    diamond_dict['diamond_rate']=(float(diamond.diamond_rate)/5)

                diamond_details.append(diamond_dict)
        
            res_data['stone_details']=stone_details
            res_data['diamond_details']=diamond_details
            
            return Response(
                {
                    "data":res_data,
                    "message":res_msg.retrieve('Tag Item Details'),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        
        except TaggedItems.DoesNotExist:

            return Response(
                {
                    "message":res_msg.not_exists("Tag Number"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        
        except Exception as err:

            return Response(
                {
                    "message":str(err),
                    "status":status.HTTP_204_NO_CONTENT
                },status=status.HTTP_200_OK
            )
        
    def create(self,request):

        try:

            tag_number = request.data.get('tag_number')

            tag_item_queryset=TaggedItems.objects.get(tag_number=tag_number)

            res_data={
                "id":tag_item_queryset.pk,
                "tagged_date":tag_item_queryset.created_at,
                "lot_number":tag_item_queryset.tag_entry_details.lot_details.lot_number,
                "entry_type":tag_item_queryset.tag_entry_details.lot_details.entry_type.entry_name,
                "stock_type":tag_item_queryset.sub_item_details.stock_type.pk,
                "stock_type_name":tag_item_queryset.sub_item_details.stock_type.stock_type_name,
                "tag_type":tag_item_queryset.tag_type.tag_name,
                "invoice_number":tag_item_queryset.tag_entry_details.lot_details.invoice_number,
                "item_name":tag_item_queryset.item_details.item_details.item_name,
                "sub_item_name":tag_item_queryset.sub_item_details.sub_item_name,
                "item_details":tag_item_queryset.item_details.item_details.pk,
                "item_huid_rate":tag_item_queryset.item_details.item_details.huid_rate,
                "sub_item_details":tag_item_queryset.sub_item_details.pk,
                "assigned_counter":tag_item_queryset.display_counter.counter_name,
                "pieces":tag_item_queryset.tag_pieces,
                "size":tag_item_queryset.size_value,
                "gross_weight":tag_item_queryset.gross_weight,
                "net_weight":tag_item_queryset.net_weight,
                "tag_weight":tag_item_queryset.tag_weight,
                "cover_weight":tag_item_queryset.cover_weight,
                "loop_weight":tag_item_queryset.loop_weight,
                "other_weight":tag_item_queryset.other_weight,
                "calculation_type":tag_item_queryset.calculation_type.pk,
                "calculation_type_name":tag_item_queryset.calculation_type.calculation_name,
                "item_metal_id":tag_item_queryset.item_details.item_details.metal.pk,
                "item_metal_name":tag_item_queryset.item_details.item_details.metal.metal_name,
                "sub_item_metal_id":tag_item_queryset.sub_item_details.metal.pk,
                "sub_item_metal_name":tag_item_queryset.sub_item_details.metal.metal_name,
                "item_purity_id":tag_item_queryset.item_details.item_details.purity.pk,
                "item_purity_name":tag_item_queryset.item_details.item_details.purity.purity_name,
                "sub_item_purity_id":tag_item_queryset.sub_item_details.purity.pk,
                "sub_item_purity_name":tag_item_queryset.sub_item_details.purity.purity_name,
                "stone_rate":tag_item_queryset.stone_rate,
                "diamond_rate":tag_item_queryset.diamond_rate,
                "total_stone_weight":tag_item_queryset.stone_weight,
                "total_diamond_weight":tag_item_queryset.diamond_weight,
                'remaining_pieces':tag_item_queryset.remaining_pieces,
                'remaining_gross_weight':tag_item_queryset.remaining_gross_weight,
                'remaining_net_weight':tag_item_queryset.remaining_net_weight,
                'remaining_tag_count':tag_item_queryset.remaining_tag_count,
                'is_billed':tag_item_queryset.is_billed
            }

            today=timezone.now()
            created_date=tag_item_queryset.created_at

            age=relativedelta(today, created_date)

            years, months, days = age.years, age.months, age.days

            res_data['item_age']=f"{years} years, {months} months, and {days} days"
                    

            if str(tag_item_queryset.calculation_type.pk)==settings.FIXEDRATE:

                res_data['min_fixed_rate']=tag_item_queryset.min_fixed_rate 
                res_data['max_fixed_rate']=tag_item_queryset.max_fixed_rate

                res_data['min_sale_value']=(tag_item_queryset.min_fixed_rate + tag_item_queryset.stone_rate + tag_item_queryset.diamond_rate)
                res_data['max_sale_value']=(tag_item_queryset.max_fixed_rate + tag_item_queryset.stone_rate + tag_item_queryset.diamond_rate)

            elif str(tag_item_queryset.calculation_type.pk)==settings.PERPIECERATE:
                res_data['min_per_piece_rate']=tag_item_queryset.min_per_piece_rate 
                res_data['per_piece_rate']=tag_item_queryset.per_piece_rate 

            elif str(tag_item_queryset.calculation_type.pk)==settings.PERGRAMRATE:
                res_data['min_pergram_rate']=tag_item_queryset.min_pergram_rate
                res_data['max_pergram_rate']=tag_item_queryset.max_pergram_rate
                res_data['per_gram_weight_type']=tag_item_queryset.per_gram_weight_type.pk
                res_data['per_gram_weight_type_name']=tag_item_queryset.per_gram_weight_type.weight_name

                if str(tag_item_queryset.per_gram_weight_type.pk) == settings.GROSSWEIGHT :

                    min_per_gram_value=float(tag_item_queryset.gross_weight) * float(tag_item_queryset.min_pergram_rate)
                    max_per_gram_value=float(tag_item_queryset.gross_weight) * float(tag_item_queryset.max_pergram_rate)

                else:

                    min_per_gram_value=float(tag_item_queryset.net_weight) * float(tag_item_queryset.min_pergram_rate)
                    max_per_gram_value=float(tag_item_queryset.net_weight) * float(tag_item_queryset.max_pergram_rate)

                res_data['min_sale_value']=(min_per_gram_value + tag_item_queryset.stone_rate + tag_item_queryset.diamond_rate)
                res_data['max_sale_value']=(max_per_gram_value + tag_item_queryset.stone_rate + tag_item_queryset.diamond_rate)

            else:

                try:

                    # metal=str(tag_item_queryset.sub_item_details.metal.metal_name)

                    # purity=str(tag_item_queryset.sub_item_details.purity.purity_name)

                    # metal_purity=metal+'_'+purity


                    # metal_rate_queryset=MetalRate.objects.all().order_by('-id')[0]

                    # metal_rate=float(metal_rate_queryset.rate[metal_purity])

                    # metal_rate = 0 if metal_rate is None else float(metal_rate)
                    metal_rate_queryset = MetalRate.objects.filter(purity=tag_item_queryset.sub_item_details.purity.pk).order_by('-id')[0]
                    metal_rate = metal_rate_queryset.rate

                except Exception as err:

                    metal_rate=0

                #min sale value calculation

                metal_value=(float(metal_rate)*float(tag_item_queryset.net_weight))
                
                sub_wastage_queryset=SubItemWeightCalculation.objects.get(sub_item_details=tag_item_queryset.sub_item_details.pk)

                res_data['making_charge_calculation_type'] = sub_wastage_queryset.making_charge_calculation.pk
                res_data['wastage_calculation_type'] = sub_wastage_queryset.wastage_calculation.pk

                if str(sub_wastage_queryset.wastage_calculation.pk) == settings.GROSSWEIGHT :

                    min_wastage_value=((tag_item_queryset.gross_weight*tag_item_queryset.min_wastage_percent)/100)*metal_rate

                else:

                    min_wastage_value=((tag_item_queryset.net_weight*tag_item_queryset.min_wastage_percent)/100)*metal_rate

                min_flat_wastage=tag_item_queryset.min_flat_wastage

                if str(sub_wastage_queryset.making_charge_calculation.pk) == settings.GROSSWEIGHT :

                    min_making_Charge=(tag_item_queryset.min_making_charge_gram*tag_item_queryset.gross_weight)

                else:

                    min_making_Charge=(tag_item_queryset.min_making_charge_gram*tag_item_queryset.net_weight)


                min_flat_making_charge=tag_item_queryset.min_flat_making_charge

                min_sale_value = metal_value + min_wastage_value + min_flat_wastage + min_making_Charge + min_flat_making_charge + tag_item_queryset.stone_rate + tag_item_queryset.diamond_rate

                #max sale value calculation

                if str(sub_wastage_queryset.wastage_calculation.pk) == settings.GROSSWEIGHT :

                    max_wastage_value=((tag_item_queryset.gross_weight * tag_item_queryset.max_wastage_percent)/100)*metal_rate

                else:

                    max_wastage_value=((tag_item_queryset.net_weight * tag_item_queryset.max_wastage_percent)/100)*metal_rate


                max_flat_wastage=tag_item_queryset.max_flat_wastage

                if str(sub_wastage_queryset.making_charge_calculation.pk) == settings.GROSSWEIGHT :

                    max_making_Charge=(tag_item_queryset.max_making_charge_gram * tag_item_queryset.gross_weight)
                
                else:

                    max_making_Charge=(tag_item_queryset.max_making_charge_gram * tag_item_queryset.net_weight)

                
                max_flat_making_charge=tag_item_queryset.max_flat_making_charge
                
                max_sale_value = metal_value + max_wastage_value + max_flat_wastage + max_making_Charge + max_flat_making_charge + tag_item_queryset.stone_rate + tag_item_queryset.diamond_rate
                
                res_data['metal_rate']=metal_rate
                res_data['min_wastage_percent']=tag_item_queryset.min_wastage_percent
                res_data['min_flat_wastage']=tag_item_queryset.min_flat_wastage
                res_data['max_wastage_percent']=tag_item_queryset.max_wastage_percent
                res_data['max_flat_wastage']=tag_item_queryset.max_flat_wastage
                res_data['min_making_charge_gram']=tag_item_queryset.min_making_charge_gram
                res_data['min_flat_making_charge']=tag_item_queryset.min_flat_making_charge
                res_data['max_making_charge_gram']=tag_item_queryset.max_making_charge_gram
                res_data['max_flat_making_charge']=tag_item_queryset.max_flat_making_charge

                res_data['min_sale_value']=min_sale_value
                res_data['max_sale_value']=max_sale_value

            try:
                tax_queryset = TaxDetailsAudit.objects.filter(metal=tag_item_queryset.sub_item_details.metal).order_by('-id').first()
                if tax_queryset:
                    tax_percent_queryset = SalesTaxDetails.objects.get(tax_details=tax_queryset.tax_details)
                    res_data['sales_tax_igst']=tax_percent_queryset.sales_tax_igst
                    res_data['sales_tax_cgst']=tax_percent_queryset.sales_tax_cgst
                    res_data['sales_tax_sgst']=tax_percent_queryset.sales_tax_sgst
                    res_data['sales_surcharge_percent']=tax_percent_queryset.sales_surcharge_percent
                    res_data['sales_additional_charges'] = tax_percent_queryset.sales_additional_charges
            except Exception as err:
                res_data['sales_tax_igst']=0
                res_data['sales_tax_cgst']=0
                res_data['sales_tax_sgst']=0
                res_data['sales_surcharge_percent']=0
                res_data['sales_additional_charges'] = 0

            stone_details=[]
            stone_queryset=list(TaggedItemStone.objects.filter(tag_details=tag_item_queryset.pk))

            for stone in stone_queryset :

                stone_dict={
                    "stone_name":stone.stone_name.stone_name.pk,
                    "stone_pieces":stone.stone_pieces,
                    "stone_weight":stone.stone_weight,
                    "stone_weight_type":stone.stone_weight_type.pk,
                    "stone_weight_type_name":stone.stone_weight_type.weight_name,
                    "stone_rate":stone.stone_rate,
                    "stone_rate_type":stone.stone_rate_type.pk,
                    "stone_rate_type_name":stone.stone_rate_type.type_name,
                    "include_stone_weight":stone.include_stone_weight
                }

                if str(stone.stone_weight_type.pk) == settings.CARAT :

                    stone_dict['stone_weight']=float(stone.stone_weight*5)

                if str(stone.stone_rate_type.pk) == settings.PERCARAT :

                    stone_dict['stone_rate']=float(stone.stone_rate/5)

                stone_details.append(stone_dict)
            
            diamond_details=[]
            diamond_queryset=TaggedItemDiamond.objects.filter(tag_details=tag_item_queryset.pk)

            for diamond in diamond_queryset:

                diamond_dict={
                    "diamond_name":diamond.diamond_name.diamond_name.pk,
                    "diamond_pieces":diamond.diamond_pieces,
                    "diamond_weight":diamond.diamond_weight,
                    "diamond_weight_type":diamond.diamond_weight_type.pk,
                    "diamond_weight_type_name":diamond.diamond_weight_type.weight_name,
                    "diamond_rate":diamond.diamond_rate,
                    "diamond_rate_type":diamond.diamond_rate_type.pk,
                    "diamond_rate_type_name":diamond.diamond_rate_type.type_name,
                    "include_diamond_weight":diamond.include_diamond_weight
                }

                if str(diamond.diamond_weight_type.pk) == settings.CARAT :

                    diamond_dict['diamond_weight']=(float(diamond.diamond_weight)*5)
                    
                if str(diamond.diamond_rate_type.pk) == settings.PERCARAT :

                    diamond_dict['diamond_rate']=(float(diamond.diamond_rate)/5)

                diamond_details.append(diamond_dict)
        
            res_data['stone_details']=stone_details
            res_data['diamond_details']=diamond_details
            
            return Response(
                {
                    "data":res_data,
                    "message":res_msg.retrieve('Tag Item Details'),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        
        except TaggedItems.DoesNotExist:

            return Response(
                {
                    "message":res_msg.not_exists("Tag Number"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        
        except Exception as err:

            return Response(
                {
                    "message":str(err),
                    "status":status.HTTP_204_NO_CONTENT
                },status=status.HTTP_200_OK
            )
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class TagItemByItem(APIView):

    def post(self,request):

        sub_item_details=list(request.data.get('sub_item_details'))
        item_details=request.data.get('item_details')
        tag_type=request.data.get('tag_type')
        calculation_type=request.data.get('calculation_type')
        from_weight=float(request.data.get('from_weight'))
        to_weight=float(request.data.get('to_weight'))

        request_data={
        'metal':request.data.get('metal'),
        'stock_type':request.data.get('stock_type'),
        'item_details':request.data.get('item_details'),
        'tag_type':request.data.get('tag_type'),
        'sub_item_list':list(request.data.get('sub_item_details')),
        'calculation_type':request.data.get('calculation_type'),
        'from_weight':float(request.data.get('from_weight')),
        'to_weight':float(request.data.get('to_weight'))
        }

        response_data=[]

        for data in sub_item_details :

            queryset=list(TaggedItems.objects.filter(item_details__item_details=item_details,sub_item_details=data,tag_type=tag_type,calculation_type=calculation_type,gross_weight__range=(from_weight,to_weight)))

            for tag in queryset:
            
                res_data={
                    "tag_number":tag.tag_number,
                    "metal":tag.item_details.item_details.metal.pk,
                    "metal_name":tag.item_details.item_details.metal.metal_name,
                    "stock_type":tag.item_details.item_details.stock_type.pk,
                    "stock_type_name":tag.item_details.item_details.stock_type.stock_type_name,
                    "tag_type":tag.tag_type.pk,
                    "tag_type_name":tag.tag_type.tag_name,
                    "item_details":tag.item_details.item_details.pk,
                    "item_details_name":tag.item_details.item_details.item_name,
                    "sub_item_details":tag.sub_item_details.pk,
                    "sub_item_details_name":tag.sub_item_details.sub_item_name,
                    "calculation_type":tag.calculation_type.pk,
                    "calculation_type_name":tag.calculation_type.calculation_name,
                    "gross_weight":tag.gross_weight
                }
                response_data.append(res_data)

        if from_weight > to_weight :

            return Response(
                {
                    "message":"From Weight cannot be greater than To Weight",
                    "status":status.HTTP_204_NO_CONTENT
                },status=status.HTTP_200_OK
            )
        
        if from_weight == to_weight :

            return Response(
                {
                    "message":"From Weight and To Weight cannot be equal",
                    "status":status.HTTP_204_NO_CONTENT
                },status=status.HTTP_200_OK
            )
        
        # if from_weight <= 0 or to_weight <=0 :

        #     return Response(
        #         {
        #             "message":"From Weight and To Weight cannot be less than or equal to Zero",
        #             "status":status.HTTP_204_NO_CONTENT
        #         },status=status.HTTP_200_OK
        #     )
        
        valid_subitems = []
        invalid_subitems = []

        for s in sub_item_details :

            try:

                value_queryset=list(ValueAdditionCustomer.objects.filter(metal= request_data['metal'],stock_type= request_data['stock_type'],tag_type= request_data['tag_type'],sub_item_details = s,item_details = request_data['item_details'],calculation_type= request_data['calculation_type']))
                
                if len(value_queryset) == 0 :
                    sub_item_queryset=SubItem.objects.get(id=s)
                    valid_dict={
                        "value":sub_item_queryset.pk,
                        "label":sub_item_queryset.sub_item_name
                    }
                    valid_subitems.append(valid_dict)

                else:

                    value_range_queryset=list(ValueAdditionCustomer.objects.filter(metal= request_data['metal'],stock_type= request_data['stock_type'],tag_type= request_data['tag_type'],sub_item_details= s,item_details = request_data['item_details'],calculation_type= request_data['calculation_type'],from_weight__range=(from_weight,to_weight),to_weight__range=(from_weight,to_weight)))

                    if len(value_range_queryset) == 0:

                        for data in value_queryset :

                            if data.from_weight <= from_weight <= data.to_weight :

                                from_weight_error={
                                    "sub_item_id":data.sub_item_details.pk,
                                    "sub_item_name":data.sub_item_details.sub_item_name,
                                    "message":"From Weight Already Exsist"
                                }

                                invalid_subitems.append(from_weight_error)

                            elif data.from_weight <= to_weight <= data.to_weight :

                                to_weight_error={
                                    "sub_item_id":data.sub_item_details.pk,
                                    "sub_item_name":data.sub_item_details.sub_item_name,
                                    "message":"To Weight Already Exsist"
                                }

                                invalid_subitems.append(to_weight_error)
                            
                            else:
                                valid_sub_dict={
                                    "value":data.sub_item_details.pk,
                                    "label":data.sub_item_details.sub_item_name
                                }
                                valid_subitems.append(valid_sub_dict)

                    else:
                        queryset=SubItem.objects.get(id=s)
                        error_dict={
                                    "sub_item_id":s,
                                    "sub_item_name":queryset.sub_item_name,
                                    "message":"Another Range Already exsist between this Weight Range"
                                }
                        
                        invalid_subitems.append(error_dict)
            except Exception as err: 
                pass

        validation_data=valid_subitems

        return Response(
            {
                "data":{
                    "list":response_data,
                    "valid_subitems":validation_data,
                    "invalid_subitems":invalid_subitems
                },
                "message":res_msg.retrieve("Tag Item details"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )

    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class SingleTagUpdate(APIView):

    def put(self,request,pk):

        try:
            request_data=request.data
            queryset=TaggedItems.objects.get(tag_number=pk)
            original_tag_state = queryset.__dict__.copy()

            res_data={}

            if queryset.calculation_type.pk == int(settings.FIXEDRATE):
                res_data['min_fixed_rate'] = float(request_data.get('min_fixed_rate'))
                res_data['min_fixed_rate'] = float(request_data.get('min_fixed_rate'))

            elif queryset.calculation_type.pk == int(settings.WEIGHTCALCULATION):
                res_data['min_wastage_percent'] = float(request_data.get('min_wastage_percent'))
                res_data['min_flat_wastage'] = float(request_data.get('min_flat_wastage'))
                res_data['max_wastage_percent'] = float(request_data.get('max_wastage_percent'))
                res_data['max_flat_wastage'] = float(request_data.get('max_wastage_percent'))
                res_data['min_making_charge_gram'] = float(request_data.get('min_making_charge_gram'))
                res_data['min_flat_making_charge'] = float(request_data.get('min_flat_making_charge'))
                res_data['max_making_charge_gram'] = float(request_data.get('max_making_charge_gram'))
                res_data['max_flat_making_charge'] = float(request_data.get('max_flat_making_charge'))

            elif queryset.calculation_type.pk == int(settings.PERPIECERATE):
                res_data['min_per_piece_rate'] = float(request_data.get('min_per_piece_rate'))
                res_data['per_piece_rate'] = float(request_data.get('per_piece_rate'))

            else:
                res_data['per_gram_weight_type'] = request_data.get('per_gram_weight_type')
                res_data['min_pergram_rate'] = float(request_data.get('min_pergram_rate'))
                res_data['max_pergram_rate'] = float(request_data.get('max_pergram_rate'))

           

            serializer = TaggedItemsSerializer(queryset,data=res_data,partial = True)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "data":serializer.data,
                        "message":res_msg.update("Tag Details"),
                        "status":status.HTTP_200_OK
                    },status=status.HTTP_200_OK
                )
            else:
                raise Exception(serializer.errors)

        except TaggedItems.DoesNotExist:

            return Response(
                {
                    "message":res_msg.not_exists("Tag Items"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        
        except Exception as err:
            for key, value in original_tag_state.items():
                setattr(queryset, key, value)
            queryset.save()

            return Response(
                {
                    "data":str(err),
                    "message":res_msg.something_else(),
                    "status":status.HTTP_204_NO_CONTENT
                },status=status.HTTP_200_OK
            )
        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class DuplicateTagView(APIView):

    def post(self,request):

        try:

            reqeust_data=request.data
            tag_number=reqeust_data.get('tag_number')

            tag_queryset=TaggedItems.objects.get(tag_number=tag_number)

            reqeust_data['tag_details'] = tag_queryset.pk
            reqeust_data['branch'] = tag_queryset.branch.branch_name

            reqeust_data['created_at'] = timezone.now()
            reqeust_data['created_by'] = request.user.id

            serializer=DuplicateTagSerializer(data=reqeust_data)

            if serializer.is_valid():
                serializer.save()

                return Response(
                    {
                        "data":serializer.data,
                        "message":res_msg.create("Duplicate Tag"),
                        "status":status.HTTP_201_CREATED
                    },status=status.HTTP_200_OK
                )
            
            else :
                return Response(
                    {
                        "data":serializer.errors,
                        "message":res_msg.not_create("Duplicate Tag"),
                        "status":status.HTTP_400_BAD_REQUEST
                    },status=status.HTTP_200_OK
                )
            
        except TaggedItems.DoesNotExist:
            return Response(
                {
                    "message":res_msg.not_exists("Tag Details"),
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
        
    def get(self,reqeust):

        queryset=DuplicateTag.objects.all()

        response_data=[]

        for i in queryset:

            res_dict={}

            res_dict['tag_details'] = i.tag_details.tag_number
            res_dict['number_copies'] = i.number_copies
            res_dict['created_at'] = i.created_at

            try:

                staff_queryset=Staff.objects.get(phone=i.created_by.phone)

                res_dict['created_by'] = str(staff_queryset.first_name) +" "+ str(staff_queryset.last_name)

            except Exception as err:
                res_dict['created_by'] = "-"

            response_data.append(res_dict)

        return Response(
            {
                "data":{
                    "list":response_data
                },
                "message":res_msg.retrieve("Duplicate Tag"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
        

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class StockList(APIView):

    def post(self,request):

        request_data=request.data
        branch = request_data.get('branch') if request_data.get('branch') else None
        search = request_data.get('search') if request_data.get('search') else None
        metal = request_data.get('metal')if request_data.get('metal') != None else None
        item_details = request_data.get('item_details')if request_data.get('item_details') != None else None
        sub_item_details = request_data.get('sub_item_details')if request_data.get('sub_item_details') != None else None
        tag_type = request_data.get('tag_type')if request_data.get('tag_type') != None else None
        stock_type = request_data.get('stock_type')if request_data.get('stock_type') != None else None
        calculation_type = request_data.get('calculation_type')if request_data.get('calculation_type') != None else None
        lot_details = request_data.get('lot_details')if request_data.get('lot_details') != None else None
        counter = request_data.get('counter')if request_data.get('counter') != None else None
        active_status = request_data.get('active_status')if request_data.get('active_status') != None else None
        page = request.data.get('page') if request.data.get('page') else 1
        items_per_page = request.data.get('items_per_page') if request.data.get('items_per_page') != None else 10
        from_size =  request.data.get('from_size') if request.data.get('from_size') else None
        to_size =  request.data.get('to_size') if request.data.get('to_size') else None
        from_weight = request.data.get('from_weight') if request.data.get('from_weight') else None
        to_weight = request.data.get('to_weight') if request.data.get('to_weight') else None

        filter_condition={}
        
        if request.user.role.is_admin == True:
            if branch != None:            
                filter_condition['tag_entry_details__branch'] = branch
        else:
            filter_condition['tag_entry_details__branch'] = request.user.branch.pk
            
        if metal != None:
            filter_condition['sub_item_details__metal'] = metal


        if search != None:
            filter_condition['tag_number__icontains'] = search

        if from_size != None and to_size != None : 
            size_range = (from_size,to_size)
            filter_condition['size_value__range'] = size_range

        if from_weight != None and to_weight != None:
            weight_range = (from_weight,to_weight)
            filter_condition['gross_weight__range'] = weight_range

        if item_details != None:
            filter_condition['item_details'] = item_details

        if sub_item_details != None:
            filter_condition['sub_item_details'] = sub_item_details

        if counter != None :
            filter_condition['display_counter'] = counter

        if tag_type!= None:
            filter_condition['tag_type'] = tag_type

        if stock_type!= None:
            filter_condition['sub_item_details__stock_type'] = stock_type

        if calculation_type != None :
            filter_condition['calculation_type'] = calculation_type

        if lot_details != None :
            filter_condition['tag_entry_details__lot_details__lot_number'] = lot_details

        if active_status != None :
            filter_condition['is_active'] = active_status

        if len(filter_condition) != 0:
            queryset=TaggedItems.objects.filter(**filter_condition)
        else:
            queryset=TaggedItems.objects.all().order_by('-id')
        
        paginated_data = Paginator(queryset, items_per_page)
        serializer = TaggedItemsSerializer(paginated_data.get_page(page), many=True)
        response_data=[]

        for i in range(0 , len(serializer.data)):
            res_data=serializer.data[i]
            res_data['stock_type']=queryset[i].sub_item_details.stock_type.pk
            res_data['stock_type_name']=queryset[i].sub_item_details.stock_type.stock_type_name
            res_data['lot_number']=queryset[i].tag_entry_details.lot_details.lot_number
            res_data['item_name']=queryset[i].item_details.item_details.item_name
            res_data['sub_item_name']=queryset[i].sub_item_details.sub_item_name
            res_data['tag_type_name']=queryset[i].tag_type.tag_name
            res_data['calculation_type_name']=queryset[i].calculation_type.calculation_name 
            res_data['branch_name']=queryset[i].branch.branch_name 
            res_data['display_counter_name']=queryset[i].display_counter.counter_name
            res_data['metal_name']=queryset[i].sub_item_details.metal.metal_name
            response_data.append(res_data)

        return Response(
            {
                "data":{
                    "list":response_data,
                    "total_pages": paginated_data.num_pages,
                    "current_page": page,
                    "total_items": len(queryset),
                    "current_items": len(serializer.data)
                },
                "message":res_msg.retrieve("Stock List"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ItemtagCheckView(APIView):
 
    def post(self, request):
 
        data = request.data
 
        lotdetails =Lot.objects.get(id = data.get('lot_id'))
        remain_pieces = lotdetails.total_pieces-lotdetails.tagged_pieces
        remain_gross_weight = lotdetails.total_grossweight-lotdetails.tagged_grossweight
        remain_net_weight = lotdetails.total_netweight-lotdetails.tagged_netweight
       
        if int(data.get('total_pieces')) > remain_pieces  :
            return Response({
                "message": "Tag Pieces greater than value "+ str(remain_pieces),
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_200_OK)
        elif float(data.get('gross_weight')) > remain_gross_weight  :
            return Response({
                "message": "Tag gross weight greater than value "+ str(remain_gross_weight),
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_200_OK)
        elif float(data.get('net_weight')) > remain_net_weight   :
            return Response({
                "message": "Tag net weight greater than value "+ str(remain_net_weight),
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_200_OK)       
        else:
            return Response({
                "message":res_msg.create("Item tag"),
                "status":status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class HUIDStockList(APIView):

    def post(self,request):



        request_data=request.data
        branch = request_data.get('branch') if request_data.get('branch') else None
        search = request_data.get('search') if request_data.get('search') else None
        metal = request_data.get('metal')if request_data.get('metal') != None else None
        item_details = request_data.get('item_details')if request_data.get('item_details') != None else None
        sub_item_details = request_data.get('sub_item_details')if request_data.get('sub_item_details') != None else None
        tag_type = request_data.get('tag_type')if request_data.get('tag_type') != None else None
        stock_type = request_data.get('stock_type')if request_data.get('stock_type') != None else None
        calculation_type = request_data.get('calculation_type')if request_data.get('calculation_type') != None else None
        lot_details = request_data.get('lot_details')if request_data.get('lot_details') != None else None
        counter = request_data.get('counter')if request_data.get('counter') != None else None
        active_status = request_data.get('active_status')if request_data.get('active_status') != None else None
        page = request.data.get('page') if request.data.get('page') else 1
        items_per_page = request.data.get('items_per_page') if request.data.get('items_per_page') else 10
        from_size =  request.data.get('from_size') if request.data.get('from_size') else None
        to_size =  request.data.get('to_size') if request.data.get('to_size') else None
        from_weight = request.data.get('from_weight') if request.data.get('from_weight') else None
        to_weight = request.data.get('to_weight') if request.data.get('to_weight') else None   

        filter_condition={}
        
        if request.user.role.is_admin == True:
            if branch != None:
                filter_condition['branch'] = branch
            else:
                filter_condition['branch'] = request.user.branch_id
        else:
            if branch != None:
                filter_condition['branch'] = branch


        if search != None:
            filter_condition['tag_number__icontains'] = search
            
        if metal != None:
            filter_condition['sub_item_details__metal'] = metal

        if item_details != None:
            filter_condition['item_details'] = item_details

        if from_size != None and to_size != None : 
            size_range = (from_size,to_size)
            filter_condition['size_value__range'] = size_range

        if from_weight != None and to_weight != None:
            weight_range = (from_weight,to_weight)
            filter_condition['gross_weight__range'] = weight_range

        if sub_item_details != None:
            filter_condition['sub_item_details'] = sub_item_details

        if counter != None :
            filter_condition['display_counter'] = counter

        if tag_type!= None:
            filter_condition['tag_type'] = tag_type

        if stock_type!= None:
            filter_condition['sub_item_details__stock_type'] = stock_type

        if calculation_type != None :
            filter_condition['calculation_type'] = calculation_type

        if lot_details != None :
            filter_condition['tag_entry_details__lot_details__lot_number'] = lot_details

        if active_status != None :
            filter_condition['is_active'] = active_status

        if len(filter_condition) != 0:
            queryset=TaggedItems.objects.exclude(halmark_huid=0).filter(**filter_condition).order_by('-id')
        else:
            queryset=TaggedItems.objects.exclude(halmark_huid=0).order_by('-id')

        paginated_data = Paginator(queryset, items_per_page)
        serializer = TaggedItemsSerializer(paginated_data.get_page(page), many=True)
        response_data=[]

        for i in range(0 , len(serializer.data)):
            res_data=serializer.data[i]
            res_data['stock_type']=queryset[i].sub_item_details.stock_type.pk
            res_data['stock_type_name']=queryset[i].sub_item_details.stock_type.stock_type_name
            res_data['lot_number']=queryset[i].tag_entry_details.lot_details.lot_number
            res_data['item_name']=queryset[i].item_details.item_details.item_name
            res_data['sub_item_name']=queryset[i].sub_item_details.sub_item_name
            res_data['tag_type_name']=queryset[i].tag_type.tag_name
            res_data['calculation_type_name']=queryset[i].calculation_type.calculation_name 
            # res_data['branch_name']=queryset[i].branch.branch_name 
            res_data['display_counter_name']=queryset[i].display_counter.counter_name
            res_data['metal_name']=queryset[i].sub_item_details.metal.metal_name
            response_data.append(res_data)

        return Response(
            {
                "data":{
                    "list":response_data,
                    "total_pages": paginated_data.num_pages,
                    "current_page": page,
                    "total_items": len(queryset),
                    "current_items": len(serializer.data)
                },
                "message":res_msg.retrieve("Stock List"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
    


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class TagEntryValidationView(APIView):
    def post(self,request):
        request_data=request.data
            
        request_data['created_at']=timezone.now()
        request_data['created_by']=request.user.id

        if request.user.role.is_admin == False:
            branch = request.user.branch.pk
        else:
            branch = request_data.get('branch')

        request_data['branch'] = branch

        tag_entry_serializer=TagEntrySerializer(data=request_data)

        if tag_entry_serializer.is_valid():

            tag_entry_serializer.save()

            return Response(
                {
                    "data":tag_entry_serializer.data,
                    "message":res_msg.create("Tag Entry"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        
        else:

            return Response(
                {
                    "data":tag_entry_serializer.errors,
                    "message":res_msg.not_create('Tag Entry'),
                    "status":status.HTTP_400_BAD_REQUEST
                },status=status.HTTP_200_OK
            )
        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class TagItemValidationView(APIView):
    def post(self,request,pk):
        
        # for i in range(0,pk):

        try:
            
            tag_entry_queryset = TagEntry.objects.get(id=pk)
            
            item=request.data
            
            item_details = item['item_details']
            item_gross_weight = item['gross_weight']
            item_net_weight = item['net_weight']

            item['remaining_gross_weight'] = item_gross_weight
            item['remaining_net_weight'] = item_net_weight

            item_tag_pieces = item['tag_pieces']

            item['remaining_pieces'] = int(item['tag_pieces'])

            item['branch'] = tag_entry_queryset.branch.pk

            lot_item_queryset = LotItem.objects.get(id=item_details)
            
            try:

                tag_value_queryset=ValueAdditionCustomer.objects.filter(metal=lot_item_queryset.item_details.metal.pk,tag_type=item['tag_type'],sub_item_details=item['sub_item_details'],calculation_type=item['calculation_type'])
                
                for value in tag_value_queryset :

                    if float(value.from_weight) <= item['gross_weight'] <= float(value.to_weight) :
                            
                        if str(item['calculation_type']) == settings.FIXEDRATE :
                                
                            item['max_fixed_rate']=float(value.max_fixed_rate)

                            break

                        elif str(item['calculation_type']) == settings.PERGRAMRATE :
                                    
                            item['max_pergram_rate']=float(value.max_per_gram_rate)

                            break

                        elif str(item['calculation_type']) == settings.PERPIECERATE :
                                    
                            item['min_per_piece_rate']=float(value.min_per_piece_rate)
                            item['per_piece_rate']=float(value.per_piece_rate)

                            break
                                
                        else :
                                
                            item['max_wastage_percent']=float(value.max_wastage_percent)
                            item['max_flat_wastage']=float(value.max_flat_wastage)
                            item['max_making_charge_gram']=float(value.max_making_charge_gram)
                            item['max_flat_making_charge']=float(value.max_flat_making_charge)

                            break
                                
                    else:
                        pass

            except ValueAdditionCustomer.DoesNotExist:

                if str(item['calculation_type']) == settings.FIXEDRATE :

                    item['max_fixed_rate'] = 0 

                elif str(item['calculation_type']) == settings.PERGRAMRATE :

                    item['max_pergram_rate'] = 0 

                elif str(item['calculation_type']) == settings.PERPIECERATE :

                    item['per_piece_rate'] = 0 
                    item['min_per_piece_rate'] = 0 

                else:
                        
                    item['max_wastage_percent'] = 0 
                    item['max_flat_wastage'] = 0 
                    item['max_making_charge_gram'] = 0 
                    item['max_flat_making_charge'] = 0

            remaining_gross_weight = lot_item_queryset.gross_weight - lot_item_queryset.tagged_grossweight
            remaining_net_weight = lot_item_queryset.net_weight - lot_item_queryset.tagged_netweight
            remaining_tag_pieces = lot_item_queryset.pieces - lot_item_queryset.tagged_pieces


            if item_gross_weight <= remaining_gross_weight and item_tag_pieces <= remaining_tag_pieces and  item_net_weight <=remaining_net_weight:

                tag_item_serializer=TaggedItemsSerializer(data=item)

                if tag_item_serializer.is_valid():
                    tag_item_serializer.save()

                    stone_weight_calc=0
                    stone_rate_calc=0
                    stone_piece_calc=0
                    
                    stone_details=item.get('stone_details') if item.get('stone_details') else []

                    for stone in stone_details: 
                                        
                        tagged_stoneweight =0
                        tagged_stonepieces =0

                        stone['tag_details'] = tag_item_serializer.data['id']
                        stone['tag_entry_details'] = tag_entry_queryset.pk

                        stone['stone_weight']=float(stone['stone_weight'])
                        stone['stone_rate']=float(stone['stone_rate'])
                        stone['stone_pieces']=int(stone['stone_pieces'])

                        if str(stone['stone_weight_type']) == settings.CARAT:
                            stone_weight = float(stone['stone_weight'])/5
                            stone['stone_weight'] = stone_weight

                        if str(stone['stone_rate_type'])==settings.PERGRAM:
                            total_stone_value=float(stone['stone_rate']*stone['stone_weight'])

                        if str(stone['stone_rate_type']) == settings.PERCARAT:
                            stone_rate = float(stone['stone_rate'])*5
                            stone['stone_rate'] = stone_rate
                            total_stone_value=float(stone['stone_rate']*stone['stone_weight'])

                        if str(stone['stone_rate_type'])==settings.PERPIECE:
                            total_stone_value=float(stone['stone_rate']*stone['stone_pieces'])

                        stone_rate_calc += total_stone_value
                        stone_piece_calc += int(stone['stone_pieces'])


                        if stone['include_stone_weight'] == True :
                            stone_weight_calc += float(stone['stone_weight'])

                        stone['total_stone_value'] = total_stone_value

                        tagged_stoneweight += float(stone['stone_weight'])
                        tagged_stonepieces += int(stone['stone_pieces'])

                        lot_stone_queryset=LotItemStone.objects.get(id=stone['stone_name'])

                        stone_remaining_pieces = lot_stone_queryset.stone_pieces - lot_stone_queryset.tagged_stone_pieces
                        stone_remaining_weight = lot_stone_queryset.stone_weight - lot_stone_queryset.tagged_stone_weight

                        if stone_remaining_pieces >= stone['stone_pieces'] and stone_remaining_weight >= stone['stone_weight'] :

                            tag_stone_serializer=TaggedItemStoneSerializer(data=stone)

                            if tag_stone_serializer.is_valid():
                                                
                                tag_stone_serializer.save()

                                try:

                                    data={
                                        'tagged_stoneweight':lot_stone_queryset.tagged_stone_weight+tagged_stoneweight,
                                        'tagged_stonepieces':lot_stone_queryset.tagged_stone_pieces+tagged_stonepieces
                                        }

                                    lot_stone_serializer=LotItemStoneSerializer(lot_stone_queryset,data=data,partial=True)

                                    if lot_stone_serializer.is_valid():
                                        lot_stone_serializer.save()
                            
                                except:
                                    pass

                            else:
                                raise Exception(tag_stone_serializer.errors)
                        elif stone_remaining_pieces < stone['stone_pieces']:
                            raise Exception("The Remaining Stone Pieces is "+str(stone_remaining_pieces))
                        elif stone_remaining_weight < stone['stone_weight']:
                            raise Exception("The Remaining Stone Weight is "+str(stone_remaining_weight))
                        
                    diamond_weight_calc=0
                    diamond_rate_calc=0
                    diamond_piece_calc=0

                    diamond_details=item.get('diamond_details') if item.get('diamond_details') else []

                    for diamond in diamond_details: 
                                        
                        tagged_diamondweight =0
                        tagged_diamondpieces =0

                        diamond['tag_details'] = tag_item_serializer.data['id']
                        diamond['tag_entry_details'] = tag_entry_queryset.pk

                        diamond['diamond_weight']=float(diamond['diamond_weight'])
                        diamond['diamond_rate']=float(diamond['diamond_rate'])
                        diamond['diamond_pieces']=int(diamond['diamond_pieces'])

                        if str(diamond['diamond_weight_type']) == settings.CARAT:
                            diamond_weight = float(diamond['diamond_weight'])/5
                            diamond['diamond_weight'] = diamond_weight

                        if str(diamond['diamond_rate_type'])==settings.PERGRAM:
                            total_diamond_value=float(diamond['diamond_rate']*diamond['diamond_weight'])

                        if str(diamond['diamond_rate_type']) == settings.PERCARAT:
                            diamond_rate = float(diamond['diamond_rate'])*5
                            diamond['diamond_rate'] = diamond_rate
                            total_diamond_value=float(diamond['diamond_rate']*diamond['diamond_weight'])

                        if str(diamond['diamond_rate_type'])==settings.PERPIECE:
                            total_diamond_value=float(diamond['diamond_rate']*diamond['diamond_pieces'])

                        diamond_rate_calc += total_diamond_value
                        diamond_piece_calc += int(diamond['diamond_pieces'])

                        if diamond['include_diamond_weight'] == True :
                            diamond_weight_calc += float(diamond['diamond_weight'])

                        diamond['total_diamond_value'] = total_diamond_value

                        tagged_diamondweight += float(diamond['diamond_weight'])
                        tagged_diamondpieces += int(diamond['diamond_pieces'])

                        lot_diamond_queryset=LotItemDiamond.objects.get(id=diamond['diamond_name'])

                        diamond_remaining_pieces = lot_diamond_queryset.diamond_pieces - lot_diamond_queryset.tagged_diamond_pieces
                        diamond_remaining_weight = lot_diamond_queryset.diamond_weight - lot_diamond_queryset.tagged_diamond_weight

                        if diamond_remaining_pieces >= diamond['diamond_pieces'] and diamond_remaining_weight >= diamond['diamond_weight'] :

                            tag_diamond_serializer=TaggedItemDiamondSerializer(data=diamond)

                            if tag_diamond_serializer.is_valid():
                                                
                                tag_diamond_serializer.save()

                                try:

                                    data={
                                        'tagged_diamondweight':lot_diamond_queryset.tagged_diamond_weight+tagged_diamondweight,
                                        'tagged_diamondpieces':lot_diamond_queryset.tagged_diamond_pieces+tagged_diamondpieces
                                        }

                                    lot_diamond_serializer=LotItemDiamondSerializer(lot_diamond_queryset,data=data,partial=True)

                                    if lot_diamond_serializer.is_valid():
                                        lot_diamond_serializer.save()
                            
                                except:
                                    pass

                            else:
                                raise Exception(tag_diamond_serializer.errors)
                        elif diamond_remaining_pieces < diamond['diamond_pieces']:
                            raise Exception("The Remaining Diamond Pieces is "+str(diamond_remaining_pieces))
                        elif diamond_remaining_weight < diamond['diamond_weight']:
                            raise Exception("The Remaining Diamond Weight is "+str(diamond_remaining_weight))
                else:
                    return Response(
                        {
                            "data":tag_item_serializer.errors,
                            "message":res_msg.not_create("Tag Item"),
                            "status":status.HTTP_400_BAD_REQUEST
                        },status=status.HTTP_200_OK
                    )
            
            elif item_gross_weight > remaining_gross_weight :
                return Response(
                    {
                        "data":"The Remaining Gross Weight is "+str(remaining_gross_weight),
                        "message":res_msg.not_create("Tag Item"),
                        "status":status.HTTP_204_NO_CONTENT
                    },status=status.HTTP_200_OK
                )
            elif item_net_weight > remaining_net_weight :
                return Response(
                    {
                        "data":"The Remaining Net Weight is "+str(remaining_net_weight),
                        "message":res_msg.not_create("Tag Item"),
                        "status":status.HTTP_204_NO_CONTENT
                    },status=status.HTTP_200_OK
                )
            elif item_tag_pieces > remaining_tag_pieces:
                return Response(
                    {
                        "data":"The Remaining Pieces is "+str(remaining_tag_pieces),
                        "message":res_msg.not_create("Tag Item"),
                        "status":status.HTTP_204_NO_CONTENT
                    },status=status.HTTP_200_OK
                )
                
        except:
             return Response(
                    {
                        "message":res_msg.not_create("Tag Item"),
                        "status":status.HTTP_204_NO_CONTENT
                    },status=status.HTTP_200_OK
                )
        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class TagItemGOldViewset(APIView):

    def get(self,request,pk):

        try:
            tag_item_queryset=TaggedItems.objects.get(tag_number=pk)
            if tag_item_queryset.is_billed == True:
                return Response(
                    {
                        "message":"Given Tag number is already billed",
                        "status":status.HTTP_204_NO_CONTENT
                    },status=status.HTTP_200_OK
                )
            
            else:
                # tag_item_queryset=TaggedItems.objects.get(tag_number=pk,is_billed=False)
                print(tag_item_queryset)
                if tag_item_queryset.sub_item_details.metal.pk != int(settings.GOLD):
                    return Response(
                        {
                            "message":"The Tag is not Gold",
                            "status":status.HTTP_404_NOT_FOUND
                        },status=status.HTTP_200_OK
                    )
                
                res_data={
                    "id":tag_item_queryset.pk,
                    "tagged_date":tag_item_queryset.created_at,
                    "lot_number":tag_item_queryset.tag_entry_details.lot_details.lot_number,
                    "entry_type":tag_item_queryset.tag_entry_details.lot_details.entry_type.entry_name,
                    "stock_type":tag_item_queryset.sub_item_details.stock_type.pk,
                    "stock_type_name":tag_item_queryset.sub_item_details.stock_type.stock_type_name,
                    "tag_type":tag_item_queryset.tag_type.tag_name,
                    "invoice_number":tag_item_queryset.tag_entry_details.lot_details.invoice_number,
                    "item_name":tag_item_queryset.item_details.item_details.item_name,
                    "sub_item_name":tag_item_queryset.sub_item_details.sub_item_name,
                    "item_details":tag_item_queryset.item_details.item_details.pk,
                    "item_huid_rate":tag_item_queryset.item_details.item_details.huid_rate,
                    "sub_item_details":tag_item_queryset.sub_item_details.pk,
                    "assigned_counter":tag_item_queryset.display_counter.counter_name,
                    "pieces":tag_item_queryset.tag_pieces,
                    "size":tag_item_queryset.size_value,
                    "gross_weight":tag_item_queryset.gross_weight,
                    "net_weight":tag_item_queryset.net_weight,
                    "tag_weight":tag_item_queryset.tag_weight,
                    "cover_weight":tag_item_queryset.cover_weight,
                    "loop_weight":tag_item_queryset.loop_weight,
                    "other_weight":tag_item_queryset.other_weight,
                    "calculation_type":tag_item_queryset.calculation_type.pk,
                    "calculation_type_name":tag_item_queryset.calculation_type.calculation_name,
                    "item_metal_id":tag_item_queryset.item_details.item_details.metal.pk,
                    "item_id":tag_item_queryset.item_details.item_details.item_id,
                    "item_metal_name":tag_item_queryset.item_details.item_details.metal.metal_name,
                    "sub_item_metal_id":tag_item_queryset.sub_item_details.metal.pk,
                    "sub_item_metal_name":tag_item_queryset.sub_item_details.metal.metal_name,
                    "item_purity_id":tag_item_queryset.item_details.item_details.purity.pk,
                    "item_purity_name":tag_item_queryset.item_details.item_details.purity.purity_name,
                    "sub_item_purity_id":tag_item_queryset.sub_item_details.purity.pk,
                    "sub_item_purity_name":tag_item_queryset.sub_item_details.purity.purity_name,
                    "stone_rate":tag_item_queryset.stone_rate,
                    "diamond_rate":tag_item_queryset.diamond_rate,
                    "total_stone_weight":tag_item_queryset.stone_weight,
                    "total_diamond_weight":tag_item_queryset.diamond_weight,
                    'remaining_pieces':tag_item_queryset.remaining_pieces,
                    'remaining_gross_weight':tag_item_queryset.remaining_gross_weight,
                    'remaining_net_weight':tag_item_queryset.remaining_net_weight,
                    'remaining_tag_count':tag_item_queryset.remaining_tag_count,
                    'is_billed':tag_item_queryset.is_billed,
                    "designer_name":tag_item_queryset.tag_entry_details.lot_details.designer_name.account_head_name,
                }


                today=timezone.now()
                created_date=tag_item_queryset.created_at

                age=relativedelta(today, created_date)

                years, months, days = age.years, age.months, age.days

                res_data['item_age']=f"{years} years, {months} months, and {days} days"
                        
                
                if str(tag_item_queryset.calculation_type.pk)==settings.FIXEDRATE:

                    res_data['min_fixed_rate']=tag_item_queryset.min_fixed_rate 
                    res_data['max_fixed_rate']=tag_item_queryset.max_fixed_rate

                    res_data['min_sale_value']=(tag_item_queryset.min_fixed_rate + tag_item_queryset.stone_rate + tag_item_queryset.diamond_rate)
                    res_data['max_sale_value']=(tag_item_queryset.max_fixed_rate + tag_item_queryset.stone_rate + tag_item_queryset.diamond_rate)
                
                elif str(tag_item_queryset.calculation_type.pk)==settings.PERPIECERATE:
                    res_data['min_per_piece_rate']=tag_item_queryset.min_per_piece_rate   
                    res_data['min_per_piece_rate']=tag_item_queryset.per_piece_rate   

                elif str(tag_item_queryset.calculation_type.pk)==settings.PERGRAMRATE:
                    res_data['min_pergram_rate']=tag_item_queryset.min_pergram_rate
                    res_data['max_pergram_rate']=tag_item_queryset.max_pergram_rate
                    res_data['per_gram_weight_type']=tag_item_queryset.per_gram_weight_type.pk
                    res_data['per_gram_weight_type_name']=tag_item_queryset.per_gram_weight_type.weight_name
                
                

                    if str(tag_item_queryset.per_gram_weight_type.pk) == settings.GROSSWEIGHT :

                        min_per_gram_value=float(tag_item_queryset.gross_weight) * float(tag_item_queryset.min_pergram_rate)
                        max_per_gram_value=float(tag_item_queryset.gross_weight) * float(tag_item_queryset.max_pergram_rate)

                    else:

                        min_per_gram_value=float(tag_item_queryset.net_weight) * float(tag_item_queryset.min_pergram_rate)
                        max_per_gram_value=float(tag_item_queryset.net_weight) * float(tag_item_queryset.max_pergram_rate)

                    res_data['min_sale_value']=(min_per_gram_value + tag_item_queryset.stone_rate + tag_item_queryset.diamond_rate)
                    res_data['max_sale_value']=(max_per_gram_value + tag_item_queryset.stone_rate + tag_item_queryset.diamond_rate)
                    
                else:

                    try:

                        # metal=str(tag_item_queryset.sub_item_details.metal.metal_name)

                        # purity=str(tag_item_queryset.sub_item_details.purity.purity_name)
    
                        # metal_purity=metal+'_'+purity


                        # metal_rate_queryset=MetalRate.objects.all().order_by('-id')[0]

                        # metal_rate=float(metal_rate_queryset.rate[metal_purity])

                        # metal_rate = 0 if metal_rate is None else float(metal_rate)

                        metal_rate_queryset = MetalRate.objects.filter(purity=tag_item_queryset.sub_item_details.purity.pk).order_by('-id')[0]
                        metal_rate = metal_rate_queryset.rate

                    except Exception as err:

                        metal_rate=0

                    #min sale value calculation

                    metal_value=(float(metal_rate)*float(tag_item_queryset.net_weight))
                    
                    sub_wastage_queryset=SubItemWeightCalculation.objects.get(sub_item_details=tag_item_queryset.sub_item_details.pk)

                    res_data['making_charge_calculation_type'] = sub_wastage_queryset.making_charge_calculation.pk
                    res_data['wastage_calculation_type'] = sub_wastage_queryset.wastage_calculation.pk

                    if str(sub_wastage_queryset.wastage_calculation.pk) == settings.GROSSWEIGHT :

                        min_wastage_value=((tag_item_queryset.gross_weight*tag_item_queryset.min_wastage_percent)/100)*metal_rate

                    else:

                        min_wastage_value=((tag_item_queryset.net_weight*tag_item_queryset.min_wastage_percent)/100)*metal_rate

                    min_flat_wastage=tag_item_queryset.min_flat_wastage

                    if str(sub_wastage_queryset.making_charge_calculation.pk) == settings.GROSSWEIGHT :

                        min_making_Charge=(tag_item_queryset.min_making_charge_gram*tag_item_queryset.gross_weight)

                    else:

                        min_making_Charge=(tag_item_queryset.min_making_charge_gram*tag_item_queryset.net_weight)


                    min_flat_making_charge=tag_item_queryset.min_flat_making_charge

                    min_sale_value = metal_value + min_wastage_value + min_flat_wastage + min_making_Charge + min_flat_making_charge + tag_item_queryset.stone_rate + tag_item_queryset.diamond_rate

                    #max sale value calculation

                    if str(sub_wastage_queryset.wastage_calculation.pk) == settings.GROSSWEIGHT :

                        max_wastage_value=((tag_item_queryset.gross_weight * tag_item_queryset.max_wastage_percent)/100)*metal_rate

                    else:

                        max_wastage_value=((tag_item_queryset.net_weight * tag_item_queryset.max_wastage_percent)/100)*metal_rate


                    max_flat_wastage=tag_item_queryset.max_flat_wastage

                    if str(sub_wastage_queryset.making_charge_calculation.pk) == settings.GROSSWEIGHT :

                        max_making_Charge=(tag_item_queryset.max_making_charge_gram * tag_item_queryset.gross_weight)
                    
                    else:

                        max_making_Charge=(tag_item_queryset.max_making_charge_gram * tag_item_queryset.net_weight)

                    
                    max_flat_making_charge=tag_item_queryset.max_flat_making_charge
                    
                    max_sale_value = metal_value + max_wastage_value + max_flat_wastage + max_making_Charge + max_flat_making_charge + tag_item_queryset.stone_rate + tag_item_queryset.diamond_rate
                    
                    res_data['metal_rate']=metal_rate
                    res_data['min_wastage_percent']=tag_item_queryset.min_wastage_percent
                    res_data['min_flat_wastage']=tag_item_queryset.min_flat_wastage
                    res_data['max_wastage_percent']=tag_item_queryset.max_wastage_percent
                    res_data['max_flat_wastage']=tag_item_queryset.max_flat_wastage
                    res_data['min_making_charge_gram']=tag_item_queryset.min_making_charge_gram
                    res_data['min_flat_making_charge']=tag_item_queryset.min_flat_making_charge
                    res_data['max_making_charge_gram']=tag_item_queryset.max_making_charge_gram
                    res_data['max_flat_making_charge']=tag_item_queryset.max_flat_making_charge

                    res_data['min_sale_value']=min_sale_value
                    res_data['max_sale_value']=max_sale_value
                try:
                    tax_queryset = TaxDetailsAudit.objects.filter(metal=tag_item_queryset.sub_item_details.metal).order_by('-id').first()
                    if tax_queryset:
                        tax_percent_queryset = SalesTaxDetails.objects.get(tax_details=tax_queryset.tax_details)
                        res_data['sales_tax_igst']=tax_percent_queryset.sales_tax_igst
                        res_data['sales_tax_cgst']=tax_percent_queryset.sales_tax_cgst
                        res_data['sales_tax_sgst']=tax_percent_queryset.sales_tax_sgst
                        res_data['sales_surcharge_percent']=tax_percent_queryset.sales_surcharge_percent
                        res_data['sales_additional_charges'] = tax_percent_queryset.sales_additional_charges
                except Exception as err:
                    res_data['sales_tax_igst']=0
                    res_data['sales_tax_cgst']=0
                    res_data['sales_tax_sgst']=0
                    res_data['sales_surcharge_percent']=0
                    res_data['sales_additional_charges'] = 0
                
                stone_details=[]
                stone_queryset=list(TaggedItemStone.objects.filter(tag_details=tag_item_queryset.pk))

                for stone in stone_queryset :

                    stone_dict={
                        "stone_name":stone.stone_name.stone_name.pk,
                        "stone_pieces":stone.stone_pieces,
                        "stone_weight":stone.stone_weight,
                        "stone_weight_type":stone.stone_weight_type.pk,
                        "stone_weight_type_name":stone.stone_weight_type.weight_name,
                        "stone_rate":stone.stone_rate,
                        "stone_rate_type":stone.stone_rate_type.pk,
                        "stone_rate_type_name":stone.stone_rate_type.type_name,
                        "include_stone_weight":stone.include_stone_weight
                    }

                    if str(stone.stone_weight_type.pk) == settings.CARAT :

                        stone_dict['stone_weight']=float(stone.stone_weight*5)

                    if str(stone.stone_rate_type.pk) == settings.PERCARAT :

                        stone_dict['stone_rate']=float(stone.stone_rate/5)

                    stone_details.append(stone_dict)
                
                diamond_details=[]
                diamond_queryset=TaggedItemDiamond.objects.filter(tag_details=tag_item_queryset.pk)

                for diamond in diamond_queryset:

                    diamond_dict={
                        "diamond_name":diamond.diamond_name.diamond_name.pk,
                        "diamond_pieces":diamond.diamond_pieces,
                        "diamond_weight":diamond.diamond_weight,
                        "diamond_weight_type":diamond.diamond_weight_type.pk,
                        "diamond_weight_type_name":diamond.diamond_weight_type.weight_name,
                        "diamond_rate":diamond.diamond_rate,
                        "diamond_rate_type":diamond.diamond_rate_type.pk,
                        "diamond_rate_type_name":diamond.diamond_rate_type.type_name,
                        "include_diamond_weight":diamond.include_diamond_weight
                    }

                    if str(diamond.diamond_weight_type.pk) == settings.CARAT :

                        diamond_dict['diamond_weight']=(float(diamond.diamond_weight)*5)
                        
                    if str(diamond.diamond_rate_type.pk) == settings.PERCARAT :

                        diamond_dict['diamond_rate']=(float(diamond.diamond_rate)/5)

                    diamond_details.append(diamond_dict)
            
                res_data['stone_details']=stone_details
                res_data['diamond_details']=diamond_details
                
                return Response(
                    {
                        "data":res_data,
                        "message":res_msg.retrieve('Tag Item Details'),
                        "status":status.HTTP_200_OK
                    },status=status.HTTP_200_OK
                )
            
        except TaggedItems.DoesNotExist:

            return Response(
                {
                    "message":res_msg.not_exists("Tag Number"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        
        except Exception as err:

            return Response(
                {
                    "message":str(err),
                    "status":status.HTTP_204_NO_CONTENT
                },status=status.HTTP_200_OK
            )
        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class TagItemSilverViewset(APIView):

    def get(self,request,pk):

        try:

            tag_item_queryset=TaggedItems.objects.get(tag_number=pk,is_billed=False)

            if tag_item_queryset.sub_item_details.metal.pk != int(settings.SILVER):
                return Response(
                    {
                        "message":"The Tag is not Silver",
                        "status":status.HTTP_404_NOT_FOUND
                    },status=status.HTTP_200_OK
                )
            
            res_data={
                "id":tag_item_queryset.pk,
                "tagged_date":tag_item_queryset.created_at,
                "lot_number":tag_item_queryset.tag_entry_details.lot_details.lot_number,
                "entry_type":tag_item_queryset.tag_entry_details.lot_details.entry_type.entry_name,
                "stock_type":tag_item_queryset.sub_item_details.stock_type.pk,
                "stock_type_name":tag_item_queryset.sub_item_details.stock_type.stock_type_name,
                "tag_type":tag_item_queryset.tag_type.tag_name,
                "invoice_number":tag_item_queryset.tag_entry_details.lot_details.invoice_number,
                "item_name":tag_item_queryset.item_details.item_details.item_name,
                "sub_item_name":tag_item_queryset.sub_item_details.sub_item_name,
                "item_details":tag_item_queryset.item_details.item_details.pk,
                "item_huid_rate":tag_item_queryset.item_details.item_details.huid_rate,
                "sub_item_details":tag_item_queryset.sub_item_details.pk,
                "assigned_counter":tag_item_queryset.display_counter.counter_name,
                "pieces":tag_item_queryset.tag_pieces,
                "size":tag_item_queryset.size_value,
                "gross_weight":tag_item_queryset.gross_weight,
                "net_weight":tag_item_queryset.net_weight,
                "tag_weight":tag_item_queryset.tag_weight,
                "cover_weight":tag_item_queryset.cover_weight,
                "loop_weight":tag_item_queryset.loop_weight,
                "other_weight":tag_item_queryset.other_weight,
                "calculation_type":tag_item_queryset.calculation_type.pk,
                "calculation_type_name":tag_item_queryset.calculation_type.calculation_name,
                "item_metal_id":tag_item_queryset.item_details.item_details.metal.pk,
                "item_metal_name":tag_item_queryset.item_details.item_details.metal.metal_name,
                "sub_item_metal_id":tag_item_queryset.sub_item_details.metal.pk,
                "sub_item_metal_name":tag_item_queryset.sub_item_details.metal.metal_name,
                "item_purity_id":tag_item_queryset.item_details.item_details.purity.pk,
                "item_purity_name":tag_item_queryset.item_details.item_details.purity.purity_name,
                "sub_item_purity_id":tag_item_queryset.sub_item_details.purity.pk,
                "sub_item_purity_name":tag_item_queryset.sub_item_details.purity.purity_name,
                "stone_rate":tag_item_queryset.stone_rate,
                "diamond_rate":tag_item_queryset.diamond_rate,
                "total_stone_weight":tag_item_queryset.stone_weight,
                "total_diamond_weight":tag_item_queryset.diamond_weight,
                'remaining_pieces':tag_item_queryset.remaining_pieces,
                'remaining_gross_weight':tag_item_queryset.remaining_gross_weight,
                'remaining_net_weight':tag_item_queryset.remaining_net_weight,
                'remaining_tag_count':tag_item_queryset.remaining_tag_count,
                'is_billed':tag_item_queryset.is_billed
            }

            

            today=timezone.now()
            created_date=tag_item_queryset.created_at

            age=relativedelta(today, created_date)

            years, months, days = age.years, age.months, age.days

            res_data['item_age']=f"{years} years, {months} months, and {days} days"
                    
            
            if str(tag_item_queryset.calculation_type.pk)==settings.FIXEDRATE:

                res_data['min_fixed_rate']=tag_item_queryset.min_fixed_rate 
                res_data['max_fixed_rate']=tag_item_queryset.max_fixed_rate

                res_data['min_sale_value']=(tag_item_queryset.min_fixed_rate + tag_item_queryset.stone_rate + tag_item_queryset.diamond_rate)
                res_data['max_sale_value']=(tag_item_queryset.max_fixed_rate + tag_item_queryset.stone_rate + tag_item_queryset.diamond_rate)
            
            elif str(tag_item_queryset.calculation_type.pk)==settings.PERPIECERATE:
                res_data['min_per_piece_rate']=tag_item_queryset.min_per_piece_rate
                res_data['per_piece_rate']=tag_item_queryset.per_piece_rate

            elif str(tag_item_queryset.calculation_type.pk)==settings.PERGRAMRATE:
                res_data['min_pergram_rate']=tag_item_queryset.min_pergram_rate
                res_data['max_pergram_rate']=tag_item_queryset.max_pergram_rate
                res_data['per_gram_weight_type']=tag_item_queryset.per_gram_weight_type.pk
                res_data['per_gram_weight_type_name']=tag_item_queryset.per_gram_weight_type.weight_name

                if str(tag_item_queryset.per_gram_weight_type.pk) == settings.GROSSWEIGHT :

                    min_per_gram_value=float(tag_item_queryset.gross_weight) * float(tag_item_queryset.min_pergram_rate)
                    max_per_gram_value=float(tag_item_queryset.gross_weight) * float(tag_item_queryset.max_pergram_rate)

                else:

                    min_per_gram_value=float(tag_item_queryset.net_weight) * float(tag_item_queryset.min_pergram_rate)
                    max_per_gram_value=float(tag_item_queryset.net_weight) * float(tag_item_queryset.max_pergram_rate)

                res_data['min_sale_value']=(min_per_gram_value + tag_item_queryset.stone_rate + tag_item_queryset.diamond_rate)
                res_data['max_sale_value']=(max_per_gram_value + tag_item_queryset.stone_rate + tag_item_queryset.diamond_rate)
                
            else:

                try:

                    # metal=str(tag_item_queryset.sub_item_details.metal.metal_name)

                    # purity=str(tag_item_queryset.sub_item_details.purity.purity_name)
 
                    # metal_purity=metal+'_'+purity


                    # metal_rate_queryset=MetalRate.objects.all().order_by('-id')[0]

                    # metal_rate=float(metal_rate_queryset.rate[metal_purity])

                    # metal_rate = 0 if metal_rate is None else float(metal_rate)
                    metal_rate_queryset = MetalRate.objects.filter(purity=tag_item_queryset.sub_item_details.purity.pk).order_by('-id')[0]
                    metal_rate = metal_rate_queryset.rate

                except Exception as err:

                    metal_rate=0

                #min sale value calculation

                metal_value=(float(metal_rate)*float(tag_item_queryset.net_weight))
                
                sub_wastage_queryset=SubItemWeightCalculation.objects.get(sub_item_details=tag_item_queryset.sub_item_details.pk)

                res_data['making_charge_calculation_type'] = sub_wastage_queryset.making_charge_calculation.pk
                res_data['wastage_calculation_type'] = sub_wastage_queryset.wastage_calculation.pk

                if str(sub_wastage_queryset.wastage_calculation.pk) == settings.GROSSWEIGHT :

                    min_wastage_value=((tag_item_queryset.gross_weight*tag_item_queryset.min_wastage_percent)/100)*metal_rate

                else:

                    min_wastage_value=((tag_item_queryset.net_weight*tag_item_queryset.min_wastage_percent)/100)*metal_rate

                min_flat_wastage=tag_item_queryset.min_flat_wastage

                if str(sub_wastage_queryset.making_charge_calculation.pk) == settings.GROSSWEIGHT :

                    min_making_Charge=(tag_item_queryset.min_making_charge_gram*tag_item_queryset.gross_weight)

                else:

                    min_making_Charge=(tag_item_queryset.min_making_charge_gram*tag_item_queryset.net_weight)


                min_flat_making_charge=tag_item_queryset.min_flat_making_charge

                min_sale_value = metal_value + min_wastage_value + min_flat_wastage + min_making_Charge + min_flat_making_charge + tag_item_queryset.stone_rate + tag_item_queryset.diamond_rate

                #max sale value calculation

                if str(sub_wastage_queryset.wastage_calculation.pk) == settings.GROSSWEIGHT :

                    max_wastage_value=((tag_item_queryset.gross_weight * tag_item_queryset.max_wastage_percent)/100)*metal_rate

                else:

                    max_wastage_value=((tag_item_queryset.net_weight * tag_item_queryset.max_wastage_percent)/100)*metal_rate


                max_flat_wastage=tag_item_queryset.max_flat_wastage

                if str(sub_wastage_queryset.making_charge_calculation.pk) == settings.GROSSWEIGHT :

                    max_making_Charge=(tag_item_queryset.max_making_charge_gram * tag_item_queryset.gross_weight)
                
                else:

                    max_making_Charge=(tag_item_queryset.max_making_charge_gram * tag_item_queryset.net_weight)

                
                max_flat_making_charge=tag_item_queryset.max_flat_making_charge
                
                max_sale_value = metal_value + max_wastage_value + max_flat_wastage + max_making_Charge + max_flat_making_charge + tag_item_queryset.stone_rate + tag_item_queryset.diamond_rate
                
                res_data['metal_rate']=metal_rate
                res_data['min_wastage_percent']=tag_item_queryset.min_wastage_percent
                res_data['min_flat_wastage']=tag_item_queryset.min_flat_wastage
                res_data['max_wastage_percent']=tag_item_queryset.max_wastage_percent
                res_data['max_flat_wastage']=tag_item_queryset.max_flat_wastage
                res_data['min_making_charge_gram']=tag_item_queryset.min_making_charge_gram
                res_data['min_flat_making_charge']=tag_item_queryset.min_flat_making_charge
                res_data['max_making_charge_gram']=tag_item_queryset.max_making_charge_gram
                res_data['max_flat_making_charge']=tag_item_queryset.max_flat_making_charge

                res_data['min_sale_value']=min_sale_value
                res_data['max_sale_value']=max_sale_value
            try:
                tax_queryset = TaxDetailsAudit.objects.filter(metal=tag_item_queryset.sub_item_details.metal).order_by('-id').first()
                if tax_queryset:
                    tax_percent_queryset = SalesTaxDetails.objects.get(tax_details=tax_queryset.tax_details)
                    res_data['sales_tax_igst']=tax_percent_queryset.sales_tax_igst
                    res_data['sales_tax_cgst']=tax_percent_queryset.sales_tax_cgst
                    res_data['sales_tax_sgst']=tax_percent_queryset.sales_tax_sgst
                    res_data['sales_surcharge_percent']=tax_percent_queryset.sales_surcharge_percent
                    res_data['sales_additional_charges'] = tax_percent_queryset.sales_additional_charges
            except Exception as err:
                res_data['sales_tax_igst']=0
                res_data['sales_tax_cgst']=0
                res_data['sales_tax_sgst']=0
                res_data['sales_surcharge_percent']=0
                res_data['sales_additional_charges'] = 0
            
            stone_details=[]
            stone_queryset=list(TaggedItemStone.objects.filter(tag_details=tag_item_queryset.pk))

            for stone in stone_queryset :

                stone_dict={
                    "stone_name":stone.stone_name.stone_name.pk,
                    "stone_pieces":stone.stone_pieces,
                    "stone_weight":stone.stone_weight,
                    "stone_weight_type":stone.stone_weight_type.pk,
                    "stone_weight_type_name":stone.stone_weight_type.weight_name,
                    "stone_rate":stone.stone_rate,
                    "stone_rate_type":stone.stone_rate_type.pk,
                    "stone_rate_type_name":stone.stone_rate_type.type_name,
                    "include_stone_weight":stone.include_stone_weight
                }

                if str(stone.stone_weight_type.pk) == settings.CARAT :

                    stone_dict['stone_weight']=float(stone.stone_weight*5)

                if str(stone.stone_rate_type.pk) == settings.PERCARAT :

                    stone_dict['stone_rate']=float(stone.stone_rate/5)

                stone_details.append(stone_dict)
            
            diamond_details=[]
            diamond_queryset=TaggedItemDiamond.objects.filter(tag_details=tag_item_queryset.pk)

            for diamond in diamond_queryset:

                diamond_dict={
                    "diamond_name":diamond.diamond_name.diamond_name.pk,
                    "diamond_pieces":diamond.diamond_pieces,
                    "diamond_weight":diamond.diamond_weight,
                    "diamond_weight_type":diamond.diamond_weight_type.pk,
                    "diamond_weight_type_name":diamond.diamond_weight_type.weight_name,
                    "diamond_rate":diamond.diamond_rate,
                    "diamond_rate_type":diamond.diamond_rate_type.pk,
                    "diamond_rate_type_name":diamond.diamond_rate_type.type_name,
                    "include_diamond_weight":diamond.include_diamond_weight
                }

                if str(diamond.diamond_weight_type.pk) == settings.CARAT :

                    diamond_dict['diamond_weight']=(float(diamond.diamond_weight)*5)
                    
                if str(diamond.diamond_rate_type.pk) == settings.PERCARAT :

                    diamond_dict['diamond_rate']=(float(diamond.diamond_rate)/5)

                diamond_details.append(diamond_dict)
        
            res_data['stone_details']=stone_details
            res_data['diamond_details']=diamond_details
            
            return Response(
                {
                    "data":res_data,
                    "message":res_msg.retrieve('Tag Item Details'),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        
        except TaggedItems.DoesNotExist:

            return Response(
                {
                    "message":res_msg.not_exists("Tag Number"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        
        except Exception as err:

            return Response(
                {
                    "message":str(err),
                    "status":status.HTTP_204_NO_CONTENT
                },status=status.HTTP_200_OK
            )
            
            
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ApprovalGoldTagItemView(APIView):
    def post(self,request):
        
        try:
            
            request_data = request.data
            
            if request.user.role.is_admin == True:
                branch = int(request_data.get('branch'))
            else:
                branch = int(request.user.branch.pk)
            
            tag_number = request_data.get('tag_number')

            tag_queryset = TaggedItems.objects.get(tag_number=tag_number,sub_item_details__metal=int(settings.GOLD))
            
            if tag_queryset.transfer == True:
                return Response(
                    {
                        "message":"The Tag is already transfered",
                        "status":status.HTTP_400_BAD_REQUEST
                    },status=status.HTTP_200_OK
                )
                
            if tag_queryset.branch.pk != branch:
                
                return Response(
                    {
                        "message":"The Tag is from another branch",
                        "status":status.HTTP_400_BAD_REQUEST
                    },status=status.HTTP_200_OK
                )
            
            res_data = {}
            res_data['id']=tag_queryset.pk
            res_data['tag_number']=tag_queryset.tag_number
            res_data['metal']=tag_queryset.sub_item_details.metal.metal_name
            res_data['item_name']=tag_queryset.sub_item_details.item_details.item_name
            res_data['sub_item_name']=tag_queryset.sub_item_details.sub_item_name
            res_data['gross_weight']=tag_queryset.gross_weight
            res_data['net_weight']=tag_queryset.net_weight
            res_data['pieces']=tag_queryset.tag_pieces
            
            return Response(
                {
                    "data":res_data,
                    "message":res_msg.retrieve("Tag Details"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        except TaggedItems.DoesNotExist:
            return Response(
                {
                    "message":res_msg.not_exists("Tag Details"),
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
class ApprovalSilverTagItemView(APIView):
    def post(self,request):
        
        try:
            
            request_data = request.data
            
            tag_number = request_data.get('tag_number')
            
            if request.user.role.is_admin == True:
                branch = int(request_data.get('branch'))
            else:
                branch = int(request.user.branch.pk)
            
            tag_queryset = TaggedItems.objects.get(tag_number=tag_number,sub_item_details__metal=int(settings.SILVER))
            
            if tag_queryset.transfer == True:
                return Response(
                    {
                        "message":"The Tag is already transfered",
                        "status":status.HTTP_400_BAD_REQUEST
                    },status=status.HTTP_200_OK
                )
                
            if tag_queryset.branch.pk != branch:
                
                return Response(
                    {
                        "message":"The Tag is from another branch",
                        "status":status.HTTP_400_BAD_REQUEST
                    },status=status.HTTP_200_OK
                )
            
            res_data = {}
            res_data['id']=tag_queryset.pk
            res_data['tag_number']=tag_queryset.tag_number
            res_data['metal']=tag_queryset.sub_item_details.metal.metal_name
            res_data['item_name']=tag_queryset.sub_item_details.item_details.item_name
            res_data['sub_item_name']=tag_queryset.sub_item_details.sub_item_name
            res_data['gross_weight']=tag_queryset.gross_weight
            res_data['net_weight']=tag_queryset.net_weight
            res_data['pieces']=tag_queryset.tag_pieces
            
            return Response(
                {
                    "data":res_data,
                    "message":res_msg.retrieve("Tag Details"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        except TaggedItems.DoesNotExist:
            return Response(
                {
                    "message":res_msg.not_exists("Tag Details"),
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
class SingleTagViewset(viewsets.ViewSet):
    @transaction.atomic
    def create(self,request):
        try:

            request_data=request.data
            try:
                queryset=LotID.objects.all().order_by('-id')[0]
                new_id=int(queryset.pk)+1
            except:
                new_id='1'

            lot_detail=request_data.get('lot_dict') if request_data.get('lot_dict') else {}
            
            
            lot_detail['lot_number'] = new_id
            lot_detail['created_at']=timezone.now()
            lot_detail['created_by']=request.user.id

            if request.user.role.is_admin == False :
                branch = request.user.branch.pk
            else:
                branch = request_data.get('branch')

            lot_detail['branch']=branch
            lot_serializer=LotSerializer(data=lot_detail)

            total_pieces=0
            total_netweight=0
            total_grossweight=0
            total_stone_pieces=0
            total_stone_weight=0
            total_stone_rate=0
            total_diamond_pieces=0
            total_diamond_weight=0
            total_diamond_rate=0
            total_tag_count=0

            if lot_serializer.is_valid():
                lot_serializer.save()
                lot_id_dict={}
                lot_id_dict['lot_number']=lot_detail['lot_number']

                lot_number_serializer=LotIDSerializer(data=lot_id_dict)

                if lot_number_serializer.is_valid():
                    lot_number_serializer.save()

                tag_item_details=request_data.get('tag_item_details') if request_data.get('tag_item_details') else {}
                
                for item in tag_item_details:

                    item['lot_details']=str(lot_serializer.data['id'])
                    item['gross_weight'] = 0 if item['gross_weight'] is None else float(item['gross_weight'])
                    item['tag_weight'] = 0 if item['tag_weight'] is None else float(item['tag_weight'])
                    item['cover_weight'] = 0 if item['cover_weight']is None else float(item['cover_weight'])
                    item['loop_weight'] = 0 if item['loop_weight']is None else float(item['loop_weight'])
                    item['other_weight'] = 0 if item['other_weight']is None else float(item['other_weight'])

                    item['pieces']=int(item['pieces'])
                    item['tag_count']=int(item['tag_count'])

                    item['net_weight']=0 if item['net_weight'] is None else float(item['net_weight'])

                    item_stone_pieces=0
                    item_stone_weight=0
                    item_diamond_pieces=0
                    item_diamond_weight=0

                    item_serializer=LotItemSerializer(data=item)

                    if item_serializer.is_valid():
                        item_serializer.save()

                        total_pieces+=int(item['pieces'])
                        total_grossweight+=float(item['gross_weight'])
                        total_tag_count+=int(item['tag_count'])

                        stone_details=item.get('stone_details') if item.get('stone_details') else []

                        for stone in stone_details:

                            stone['lot_details']=lot_serializer.data['id']
                            stone['lot_item']=item_serializer.data['id']

                            stone['stone_weight']=float(stone['stone_weight'])
                            stone['stone_rate']=float(stone['stone_rate'])
                            stone['stone_pieces']=int(stone['stone_pieces'])

                            if str(stone['stone_weight_type'])==settings.CARAT:

                                stone_weight=float(stone['stone_weight'])/5
                                stone['stone_weight']=stone_weight

                            if str(stone['stone_rate_type'])==settings.PERGRAM:

                                stone['total_stone_value']=float(stone['stone_weight'])*float(stone['stone_rate'])

                            if str(stone['stone_rate_type'])==settings.PERCARAT:

                                stone_rate=float(stone['stone_rate'])*5
                                stone['stone_rate']=stone_rate
                                stone['total_stone_value']=float(stone['stone_weight'])*float(stone['stone_rate'])

                            if str(stone['stone_rate_type'])==settings.PERPIECE:
                                stone['total_stone_value']=float(stone['stone_pieces'])*float(stone['stone_rate'])

                            item_stone_pieces+=int(stone['stone_pieces'])

                            if stone['include_stone_weight'] == True :
                                item_stone_weight+=stone['stone_weight']

                            stone_serializer=LotItemStoneSerializer(data=stone)
                            if stone_serializer.is_valid():
                                stone_serializer.save()

                                total_stone_pieces+=int(stone['stone_pieces'])
                                total_stone_weight+=float(item_stone_weight)
                                total_stone_rate+=float(stone['total_stone_value'])

                            else:
                                raise Exception(stone_serializer.errors)
                                
                        diamond_details=item.get('diamond_details') if item.get('diamond_details') else []

                        for diamond in diamond_details:

                            diamond['lot_details']=lot_serializer.data['id']
                            diamond['lot_item']=item_serializer.data['id']

                            diamond['diamond_weight']=float(diamond['diamond_weight'])
                            diamond['diamond_rate']=float(diamond['diamond_rate'])
                            diamond['diamond_pieces']=int(diamond['diamond_pieces'])

                            if str(diamond['diamond_weight_type'])==settings.CARAT:
                                diamond_weight=float(diamond['diamond_weight'])/5
                                diamond['diamond_weight']=diamond_weight


                            if str(diamond['diamond_rate_type'])==settings.PERGRAM:
                                diamond['total_diamond_value']=float(diamond['diamond_weight'])*float(diamond['diamond_rate'])

                            if str(diamond['diamond_rate_type'])==settings.PERCARAT:
                                diamono_rate=float(diamond['diamond_rate'])*5
                                diamond['diamond_rate']=diamono_rate
                                diamond['total_diamond_value']=float(diamond['diamond_weight'])*float(diamond['diamond_rate'])

                            if str(diamond['diamond_rate_type'])==settings.PERPIECE:
                                diamond['total_diamond_value']=float(diamond['diamond_pieces'])*float(diamond['diamond_rate'])

                            item_diamond_pieces+=diamond['diamond_pieces']

                            if diamond['include_diamond_weight'] == True :
                                item_diamond_weight+=diamond['diamond_weight']
                            
                            diamond_serializer=LotItemDiamondSerializer(data=diamond)

                            if diamond_serializer.is_valid():
                                diamond_serializer.save()

                                total_diamond_pieces+=int(diamond['diamond_pieces'])
                                total_diamond_weight+=float(item_diamond_weight)
                                total_diamond_rate+=float(diamond['total_diamond_value'])

                            else:
                                raise Exception(diamond_serializer.errors)

                        # net_weight = float(item['gross_weight'])-(item['tag_weight']+item['cover_weight']+item['loop_weight']+item['other_weight']+item_stone_weight+item_diamond_weight)
                        total_netweight+=float(item['net_weight'])
                        item_calc={
                            "item_stone_pieces":item_stone_pieces,
                            "item_stone_weight":item_stone_weight,
                            "item_diamond_pieces":item_diamond_pieces,
                            "item_diamond_weight":item_diamond_weight,
                            # "net_weight":net_weight
                        }
                        item_queryset=LotItem.objects.get(id=item_serializer.data['id'])
                        
                        item_calc_serializer=LotItemSerializer(item_queryset,data=item_calc,partial=True)

                        if item_calc_serializer.is_valid():
                            item_calc_serializer.save()

                    else:
                        raise Exception(item_serializer.errors)

                lot_queryset=Lot.objects.get(id=lot_serializer.data['id'])

                data={
                    'total_pieces':total_pieces,
                    'total_netweight':total_netweight,
                    'total_grossweight':total_grossweight,
                    'total_stone_pieces':total_stone_pieces,
                    'total_stone_weight':total_stone_weight,
                    'total_stone_rate':total_stone_rate,
                    'total_diamond_pieces':total_diamond_pieces,
                    'total_diamond_weight':total_diamond_weight,
                    'total_diamond_rate':total_diamond_rate,
                    'total_tag_count':total_tag_count,
                    }
                
                if lot_queryset.tagged_grossweight==0 :

                    data['tag_status']=settings.PENDING
                
                elif 0 <  lot_queryset.tagged_grossweight < lot_queryset.total_grossweight :

                    data['tag_status']=settings.PARTIAL
                
                elif lot_queryset.tagged_grossweight>=lot_queryset.total_grossweight :

                    data['tag_status']=settings.COMPLETED


                lot_calc_serializer=LotSerializer(lot_queryset,data=data,partial=True)

                if lot_calc_serializer.is_valid():
                    lot_calc_serializer.save()

                tagentry_data ={}
                tagentry_data['lot_details']  = lot_serializer.data['id']
                tagentry_data['branch']  = branch
                tagentry_data['created_at']=timezone.now()
                tagentry_data['created_by']=request.user.id
                tag_entry_serializer=TagEntrySerializer(data=tagentry_data)

                if tag_entry_serializer.is_valid():

                    tag_entry_serializer.save()
        
                    tag_item_details=request_data.get('tag_item_details') if request_data.get('tag_item_details') else []

                    tag_item_id=[]
                    for item in tag_item_details :
                        
                        tagged_gross_weight=0
                        tagged_item_pieces=0

                        item['halmark_huid'] = str(item['halmark_huid']) if item['halmark_huid'] else 0
                        item['halmark_center'] = lot_queryset.hallmark_center

                        item['tag_entry_details']=tag_entry_serializer.data['id']
                        item['item_details']=item_serializer.data['id']
                        item['gross_weight'] = 0 if item['gross_weight'] is None else float(item['gross_weight'])
                        item['tag_weight'] = 0 if item['tag_weight'] is None else float(item['tag_weight'])
                        item['cover_weight'] = 0 if item['cover_weight'] is None else float(item['cover_weight'])
                        item['loop_weight'] = 0 if item['loop_weight'] is None else float(item['loop_weight'])
                        item['other_weight'] = 0 if item['other_weight'] is None else float(item['other_weight'])

                        item['remaining_gross_weight'] = 0 if item['gross_weight'] is None else float(item['gross_weight'])

                        item['tag_pieces'] = int(item['tag_pieces'])
                        item['tag_count'] = int(item['tag_count'])
                        
                        item['remaining_pieces'] = int(item['tag_pieces'])
                        item['remaining_tag_count'] = int(item['tag_count'])
                        tagged_gross_weight += item['gross_weight']
                        tagged_item_pieces += item['tag_pieces']

                        item['stone_weight']=0
                        item['stone_rate']=0
                        item['rough_sale_value']=0
                        item['created_at']=timezone.now()
                        item['created_by']=request.user.id
                        item['branch']=branch

                        lot_item_queryset=LotItem.objects.get(id=item_serializer.data['id'])
                        
                        item['item_details']=lot_item_queryset.pk
                        
                        if str(item['calculation_type']) == settings.FIXEDRATE :
                        
                            item['max_pergram_rate'] = 0
                            item['max_wastage_percent'] = 0 
                            item['max_flat_wastage'] = 0 
                            item['max_making_charge_gram'] = 0 
                            item['max_flat_making_charge'] = 0 

                        elif str(item['calculation_type']) == settings.PERGRAMRATE :

                            item['max_fixed_rate'] = 0
                            item['max_wastage_percent'] = 0 
                            item['max_flat_wastage'] = 0 
                            item['max_making_charge_gram'] = 0 
                            item['max_flat_making_charge'] = 0  

                        elif str(item['calculation_type']) == settings.PERPIECERATE :

                            item['per_piece_rate'] = 0
                            item['min_per_piece_rate'] = 0                         

                        else:
                            
                            item['max_pergram_rate'] = 0
                            item['max_fixed_rate'] = 0 

                        tag_item_serializer=TaggedItemsSerializer(data=item)

                        if tag_item_serializer.is_valid():
                            tag_item_serializer.save()

                            tag_item_id.append(tag_item_serializer.data['id'])

                            stone_weight_calc=0
                            stone_rate_calc=0
                            stone_piece_calc=0
                            diamond_weight_calc=0
                            diamond_rate_calc=0
                            diamond_piece_calc=0

                            stone_details=item.get('stone_details') if item.get('stone_details') else []

                            for stone in stone_details:
                                                
                                tagged_stoneweight =0
                                tagged_stonepieces =0

                                stone['tag_details'] = tag_item_serializer.data['id']
                                stone['tag_entry_details'] = tag_entry_serializer.data['id']

                                stone['stone_weight']=float(stone['stone_weight'])
                                stone['stone_rate']=float(stone['stone_rate'])
                                stone['stone_pieces']=int(stone['stone_pieces'])

                                if str(stone['stone_weight_type']) == settings.CARAT:
                                    stone_weight = float(stone['stone_weight'])/5
                                    stone['stone_weight'] = stone_weight

                                if str(stone['stone_rate_type'])==settings.PERGRAM:
                                    total_stone_value=float(stone['stone_rate']*stone['stone_weight'])

                                if str(stone['stone_rate_type']) == settings.PERCARAT:
                                    stone_rate = float(stone['stone_rate'])*5
                                    stone['stone_rate'] = stone_rate
                                    total_stone_value=float(stone['stone_rate']*stone['stone_weight'])

                                if str(stone['stone_rate_type'])==settings.PERPIECE:
                                    total_stone_value=float(stone['stone_rate']*stone['stone_pieces'])

                                stone_rate_calc += total_stone_value
                                stone_piece_calc += int(stone['stone_pieces'])


                                if stone['include_stone_weight'] == True :
                                    stone_weight_calc += float(stone['stone_weight'])

                                stone['total_stone_value']=total_stone_value

                                tagged_stoneweight = float(stone['stone_weight'])
                                tagged_stonepieces = int(stone['stone_pieces'])
                                tag_stone_serializer=TaggedItemStoneSerializer(data=stone)

                                if tag_stone_serializer.is_valid():
                                                    
                                    tag_stone_serializer.save()

                                    try:
                                
                                        lot_stone_queryset=LotItemStone.objects.get(id=stone['stone_name'])


                                        data={
                                            'tagged_stone_weight':tagged_stoneweight,
                                            'tagged_stone_pieces':tagged_stonepieces
                                            }
                                        lot_stone_serializer=LotItemStoneSerializer(lot_stone_queryset,data=data,partial=True)

                                        if lot_stone_serializer.is_valid():
                                            lot_stone_serializer.save()
                                    except:
                                        pass

                                else:
                                    raise Exception(tag_stone_serializer.errors)


                            diamond_details=item.get('diamond_details') if item.get('diamond_details') else []

                            for diamond in diamond_details :
                            
                                                
                                tagged_diamondweight =0
                                tagged_diamondPieces =0


                                diamond['tag_details'] = tag_item_serializer.data['id']
                                diamond['tag_entry_details'] = tag_entry_serializer.data['id']

                                diamond['diamond_weight'] = float(diamond['diamond_weight'])
                                diamond['diamond_rate'] = float(diamond['diamond_rate'])
                                diamond['diamond_pieces'] = int(diamond['diamond_pieces'])

                                if str(diamond['diamond_weight_type']) == settings.CARAT :
                                    diamond_weight=float(diamond['diamond_weight'])/5
                                    diamond['diamond_weight']=diamond_weight


                                if str(diamond['diamond_rate_type'])==settings.PERGRAM:
                                    total_diamond_value=float(diamond['diamond_rate']*diamond['diamond_weight'])

                                if str(diamond['diamond_rate_type']) == settings.PERCARAT:
                                    diamond_rate=float(diamond['diamond_rate'])*5
                                    diamond['diamond_rate']=diamond_rate
                                    total_diamond_value=float(diamond['diamond_rate']*diamond['diamond_weight'])

                                if str(diamond['diamond_rate_type'])==settings.PERPIECE:
                                    total_diamond_value=float(diamond['diamond_rate']*diamond['diamond_pieces'])

                                diamond_rate_calc += total_diamond_value
                                diamond_piece_calc += diamond['diamond_pieces']

                                if diamond['include_diamond_weight'] == True :
                                    diamond_weight_calc += (diamond['diamond_weight'])

                                tagged_diamondweight = diamond['diamond_weight']
                                tagged_diamondPieces = diamond['diamond_pieces']


                                diamond['total_diamond_value']=total_diamond_value
                                tag_diamond_serializer=TaggedItemDiamondSerializer(data=diamond)

                                if tag_diamond_serializer.is_valid():
                                    tag_diamond_serializer.save()

                                    try:

                                        lot_diamond_queryset=LotItemDiamond.objects.get(id=diamond['diamond_name'])

                                        data={
                                            'tagged_diamond_weight':tagged_diamondweight,
                                            'tagged_diamond_Pieces':tagged_diamondPieces
                                            }

                                        lot_diamond_serializer=LotItemDiamondSerializer(lot_diamond_queryset,data=data,partial=True)

                                        if lot_diamond_serializer.is_valid():
                                            lot_diamond_serializer.save()

                                    except:
                                        pass

                                else:
                                    raise Exception(tag_diamond_serializer.errors)

                        
                            # net_weight=tag_item_serializer.data['gross_weight']-(tag_item_serializer.data['tag_weight']+tag_item_serializer.data['cover_weight']+tag_item_serializer.data['loop_weight']+tag_item_serializer.data['other_weight']+stone_weight_calc+diamond_weight_calc)
                            net_weight = 0 if item['net_weight'] is None else float(item['net_weight'])
                            lot_item_data_dict={}
                            lot_item_data_dict['tagged_grossweight'] = float(lot_item_queryset.tagged_grossweight) + tag_item_serializer.data['gross_weight']
                            lot_item_data_dict['tagged_pieces'] = float(lot_item_queryset.tagged_pieces) + tag_item_serializer.data['tag_pieces']
                            lot_item_data_dict['tagged_netweight'] = lot_item_queryset.tagged_netweight +  net_weight
                            lot_item_data_dict['tagged_tag_count'] = lot_item_queryset.tagged_tag_count + tag_item_serializer.data['tag_count']
                                                        
                            lot_item_calc_serializer = LotItemSerializer(lot_item_queryset,data=lot_item_data_dict,partial=True)

                            if lot_item_calc_serializer.is_valid():
                                lot_item_calc_serializer.save()

                            calc_dict={}
                            
                            calc_dict['remaining_net_weight'] = net_weight
                            calc_dict['net_weight']=net_weight
                            calc_dict['stone_weight']=stone_weight_calc
                            calc_dict['stone_rate']=stone_rate_calc
                            calc_dict['stone_pieces']=stone_piece_calc
                            calc_dict['diamond_weight']=diamond_weight_calc
                            calc_dict['diamond_rate']=diamond_rate_calc
                            calc_dict['diamond_pieces']=diamond_piece_calc
                            

                            if str(item['calculation_type']) == settings.WEIGHTCALCULATION:
                                        
                                sub_item_queryset=SubItem.objects.get(id=item['sub_item_details'])

                                sub_weight_queryset=SubItemWeightCalculation.objects.get(sub_item_details=sub_item_queryset.pk)

                                try:
                                    # metal=str(sub_item_queryset.metal.metal_name)

                                    # purity=str(sub_item_queryset.purity.purity_name)

                                    # metal_purity=metal+'_'+purity

                                    # metal_rate_queryset=MetalRate.objects.all().order_by('-id')[0]

                                    # metal_rate = float(metal_rate_queryset.rate[metal_purity])

                                    metal_rate_queryset = MetalRate.objects.filter(purity=sub_item_queryset.purity.pk).order_by('-id')[0]
                                    metal_rate = metal_rate_queryset.rate

                                except:
                                    metal_rate = 0

                                metal_value=(float(metal_rate)*float(net_weight))

                                if (sub_weight_queryset.wastage_calculation.pk) == settings.GROSSWEIGHT:

                                    wastage=float((float(item['gross_weight']) * float((item['min_wastage_percent']) / 100)) * float(metal_rate))

                                else:

                                    wastage=float((float(net_weight) * float((item['min_wastage_percent']) / 100)) * float(metal_rate))


                                flat_wastage=float(item['min_flat_wastage'])

                                if (sub_weight_queryset.making_charge_calculation.pk) == settings.GROSSWEIGHT :

                                    making_charge=(float(item['min_making_charge_gram']) * float(item['gross_weight']))

                                else:

                                    making_charge=(float(item['min_making_charge_gram']) * float(net_weight))


                                flat_making_charge=float(item['min_flat_making_charge'])

                                stone_value=stone_rate_calc

                                diamond_value=diamond_rate_calc

                                sale_value=float(metal_value+wastage+flat_wastage+making_charge+flat_making_charge+stone_value+diamond_value)

                            
                            elif str(item['calculation_type']) == settings.PERGRAMRATE:

                                if str(item['per_gram_weight_type']) == settings.GROSSWEIGHT:

                                    sale_value = float((float(item['gross_weight'])) * float(item['min_pergram_rate'] + stone_rate_calc + diamond_rate_calc))

                                else:

                                    sale_value = float((float(net_weight) * float(item['min_pergram_rate'])) + stone_rate_calc + diamond_rate_calc)
                            
                            elif str(item['calculation_type']) == settings.PERPIECERATE: 
                                calc_dict['min_per_piece_rate']=item['min_per_piece_rate']
                                calc_dict['per_piece_rate']=item['per_piece_rate']
                            
                            else:
                                        
                                sale_value=float(item['min_fixed_rate']+ stone_rate_calc + diamond_rate_calc)

                            calc_dict['rough_sale_value']=sale_value

                            tag_calc_queryset=TaggedItems.objects.get(id=tag_item_serializer.data['id'])
                            
                            tag_calc_serializer=TaggedItemsSerializer(tag_calc_queryset,data=calc_dict,partial=True)

                            if tag_calc_serializer.is_valid():
                                tag_calc_serializer.save()

                            else:
                                raise Exception(tag_calc_serializer.errors)

                        else:
                            raise Exception(tag_item_serializer.errors)

                        
                    tagged_grossweight = 0
                    tagged_netweight = 0
                    tagged_pieces = 0
                    tagged_stone_pieces = 0
                    tagged_stone_weight = 0
                    tagged_diamond_pieces = 0
                    tagged_diamond_weight = 0
                    tagged_tag_count = 0
                        
                    item_queryset=list(TaggedItems.objects.filter(tag_entry_details=tag_entry_serializer.data['id']))
            
                    for i in item_queryset :
                        tagged_grossweight += float(i.gross_weight)
                        tagged_netweight += float(i.net_weight)
                        tagged_pieces += int(i.tag_pieces)
                        tagged_tag_count += int(i.tag_count)

                        stone_queryset=list(TaggedItemStone.objects.filter(tag_details=i.pk))
            
                        for s in stone_queryset:
                            
                            tagged_stone_pieces += int(s.stone_pieces)
                            tagged_stone_weight += float(s.stone_weight)
            
                        diamond_queryser=list(TaggedItemDiamond.objects.filter(tag_details=i.pk))
            
                        for d in diamond_queryser :
                            
                            tagged_diamond_pieces += int(d.diamond_pieces)
                            tagged_diamond_weight += float(d.diamond_weight)
                        
                    lot_queryset=Lot.objects.get(id=tag_entry_serializer.data['lot_details'])
                    old_tagged_grossweight=lot_queryset.tagged_grossweight
                    old_tagged_netweight=lot_queryset.tagged_netweight
                    old_tagged_pieces=lot_queryset.tagged_pieces
                    old_tagged_stone_pieces=lot_queryset.tagged_stone_pieces
                    old_tagged_stone_weight=lot_queryset.tagged_stone_weight
                    old_tagged_diamond_pieces=lot_queryset.tagged_diamond_pieces
                    old_tagged_diamond_weight=lot_queryset.tagged_diamond_weight
                    old_tagged_tag_count=lot_queryset.tagged_tag_count

                        
                    lot_calc={
                        'tagged_grossweight' :tagged_grossweight+old_tagged_grossweight,
                        'tagged_netweight' :tagged_netweight+old_tagged_netweight,
                        'tagged_pieces' :tagged_pieces+old_tagged_pieces,
                        'tagged_stone_pieces' : tagged_stone_pieces+old_tagged_stone_pieces,
                        'tagged_stone_weight' :tagged_stone_weight+old_tagged_stone_weight,
                        'tagged_diamond_pieces' : tagged_diamond_pieces+old_tagged_diamond_pieces,
                        'tagged_diamond_weight' :tagged_diamond_weight+old_tagged_diamond_weight,
                        'tagged_tag_count' :tagged_tag_count+old_tagged_tag_count,
                    }
                        
            
                    lot_serializer=LotSerializer(lot_queryset,data=lot_calc,partial=True)
            
                    if lot_serializer.is_valid():
                        lot_serializer.save()

                    if lot_queryset.tagged_tag_count == 0:
                        status_queryset= StatusTable.objects.get(id=int(settings.PENDING))
                        lot_queryset.tag_status = status_queryset
                    elif 0 <  lot_queryset.tagged_tag_count < lot_queryset.total_tag_count:
                        status_queryset= StatusTable.objects.get(id=int(settings.PARTIAL))
                        lot_queryset.tag_status = status_queryset
                    elif lot_queryset.tagged_tag_count>=lot_queryset.total_tag_count :
                        status_queryset= StatusTable.objects.get(id=int(settings.COMPLETED))
                        lot_queryset.tag_status = status_queryset

                    lot_queryset.save()

                    return Response(
                        {
                            "data":tag_entry_serializer.data,
                            "message":res_msg.create("Tag Entry"),
                            "status":status.HTTP_200_OK
                        },status=status.HTTP_200_OK
                    )
                
                else:
                    return Response(
                        {
                            "data":tag_entry_serializer.errors,
                            "message":res_msg.not_create("Tag Details"),
                            "status":status.HTTP_400_BAD_REQUEST
                        },status=status.HTTP_200_OK
                    )
                        
            else:
                return Response(
                    {
                        "data":lot_serializer.errors,
                        "message":res_msg.something_else(),
                        "status":status.HTTP_204_NO_CONTENT
                    },status=status.HTTP_200_OK
                )
        
        except Exception as err:
            transaction.set_rollback(True)
            # delete_lot(pk=lot_serializer.data['id'])
            # delete_tag_entry(pk=tag_entry_serializer.data['id'])
            return Response(
                {
                    "data":str(err),
                    "message":res_msg.something_else(),
                    "stauts":status.HTTP_400_BAD_REQUEST
                },status=status.HTTP_200_OK
            )
            
def delete_lot(pk):
    queryset=Lot.objects.get(id=pk)
    queryset.delete()








