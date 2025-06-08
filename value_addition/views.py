from django.shortcuts import render
from rest_framework.decorators import permission_classes, authentication_classes
from app_lib.response_messages import ResponseMessages
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status,viewsets
from django.utils import timezone
from django.db.models import ProtectedError
from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework.response import Response
from django.conf import settings

from organizations.models import Staff
from .models import *
from .serializer import *
from tagging .models import *
from tagging.serializer import *
from product .models import *
from product .serializer import *
from rest_framework.views import APIView
from accounts.models import *

# Create your views here.
res_msg = ResponseMessages()

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])

class ValueAdditionCustomerViewset(viewsets.ViewSet):

    def create(self,request):

        request_data=request.data
    
        res_data={
        'metal':request_data.get('metal'),
        'stock_type':request_data.get('stock_type'),
        'tag_type':request_data.get('tag_type'),
        'item_details':request_data.get('item_details'),
        'sub_item_list':list(request_data.get('sub_item_list')),
        'calculation_type':request_data.get('calculation_type'),
        'from_weight':float(request_data.get('from_weight')),
        'to_weight':float(request_data.get('to_weight'))
        }

        res_data['created_by']=request.user.id
        res_data['created_at']=timezone.now()

        sub_item_list=list(request_data.get('sub_item_list'))

        if str(request_data['calculation_type']) == settings.FIXEDRATE :

            res_data['max_fixed_rate']=float(request_data.get('max_fixed_rate'))

            fixed_rate_data={
            "max_fixed_rate":float(res_data['max_fixed_rate'])
            }

        elif str(request_data['calculation_type'])==settings.PERGRAMRATE:

            res_data['max_per_gram_rate']=float(request_data.get('max_per_gram_rate'))

            pergram_rate_data={
                "max_pergram_rate":float(res_data.get('max_per_gram_rate'))
            }
        elif str(request_data['calculation_type'])==settings.PERPIECERATE:

            res_data['min_per_piece_rate']=float(request_data.get('min_per_piece_rate'))
            res_data['per_piece_rate']=float(request_data.get('per_piece_rate'))

            perpiece_rate_data={
                "min_per_piece_rate":float(res_data.get('min_per_piece_rate')),
                "per_piece_rate":float(res_data.get('per_piece_rate'))
            }
        else:

            res_data['max_wastage_percent']=float(request_data.get('max_wastage_percent'))
            res_data['max_flat_wastage']=float(request_data.get('max_flat_wastage'))
            res_data['max_making_charge_gram']=float(request_data.get('max_making_charge_gram'))
            res_data['max_flat_making_charge']=float(request_data.get('max_flat_making_charge'))

            weight_calcluation_data={
            "max_wastage_percent":float(res_data.get('max_wastage_percent')),
            "max_flat_wastage":float(res_data.get('max_flat_wastage')),
            "max_making_charge_gram": float(res_data.get('max_making_charge_gram')),
            "max_flat_making_charge":float(res_data.get('max_flat_making_charge')),
            }

        response_data=[]

        for s in sub_item_list :

            res_data['sub_item_details']=s

            serializer=ValueAdditionCustomerSerializer(data=res_data)

            if serializer.is_valid():
                serializer.save()
                value_data=serializer.data
                response_data.append(serializer.data)

            try:

                tag_queryset=list(TaggedItems.objects.filter(tag_type= value_data['tag_type'],item_details__item_details = value_data['item_details'],sub_item_details= value_data['sub_item_details'],calculation_type= value_data['calculation_type'],gross_weight__range=(value_data['from_weight'],value_data['to_weight'])))

                for tag in tag_queryset :


                    if str(serializer.data['calculation_type']) == settings.FIXEDRATE :

                        calc_data=fixed_rate_data

                    elif str(request_data['calculation_type'])==settings.PERGRAMRATE:
                                
                        calc_data=pergram_rate_data

                    elif str(request_data['calculation_type'])==settings.PERPIECERATE:
                                
                        calc_data=perpiece_rate_data

                    else:   
                        calc_data=weight_calcluation_data


                    update_tag_value_serializer=TaggedItemsSerializer(tag,data=calc_data,partial=True)

                    if update_tag_value_serializer.is_valid():

                        update_tag_value_serializer.save()

            except Exception as err:
                pass

        return Response(
            {
                "data":response_data,
                "message":res_msg.create("Value Addition Customer"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
                
    def retrieve(self,request,pk):

        try:

            queryset=ValueAdditionCustomer.objects.get(id=pk)

            response_data={}
            response_data['metal']=queryset.metal.pk
            response_data['metal_name']=queryset.metal.metal_name
            response_data['stock_type']=queryset.stock_type.pk
            response_data['stock_type_name']=queryset.stock_type.stock_type_name
            response_data['tag_type']=queryset.tag_type.pk
            response_data['tag_type_name']=queryset.tag_type.tag_name
            response_data['sub_item_details']=queryset.sub_item_details.pk
            response_data['sub_item_details_name']=queryset.sub_item_details.sub_item_name
            response_data['item_details']=queryset.item_details.pk
            response_data['item_details_name']=queryset.item_details.item_name
            response_data['calculation_type']=queryset.calculation_type.pk
            response_data['calculation_type_name']=queryset.calculation_type.calculation_name
            response_data['from_weight']=queryset.from_weight
            response_data['to_weight']=queryset.to_weight
            response_data['created_at']=queryset.created_at


            if str(queryset.calculation_type.pk) ==  settings.FIXEDRATE :

                response_data['max_fixed_rate']=queryset.max_fixed_rate

            elif str(queryset.calculation_type.pk) ==  settings.WEIGHTCALCULATION :

                response_data['max_wastage_percent']=queryset.max_wastage_percent
                response_data['max_flat_wastage']=queryset.max_flat_wastage
                response_data['max_making_charge_gram']=queryset.max_making_charge_gram
                response_data['max_flat_making_charge']=queryset.max_flat_making_charge

            elif str(queryset.calculation_type.pk) ==  settings.PERPIECERATE :

                response_data['min_per_piece_rate']=queryset.min_per_piece_rate
                response_data['per_piece_rate']=queryset.per_piece_rate
            

            elif str(queryset.calculation_type.pk) ==  settings.PERGRAMRATE :

                response_data['max_per_gram_rate']=queryset.max_per_gram_rate


            return Response(
                {
                    "data":response_data,
                    "message":res_msg.retrieve("Value Addition"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        
        except ValueAdditionCustomer.DoesNotExist:
            return Response(
                {
                    "message":res_msg.not_exists("Value Addition Customer"),
                    "stauts":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        
        except Exception as err:

            return Response(
                {
                    "data" : str(err),
                    "message":res_msg.something_else(),
                    "stauts":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
            
    def update(self,request,pk):

        request_data=request.data


        res_data={
        'metal':request_data.get('metal'),
        'stock_type':request_data.get('stock_type'),
        'tag_type':request_data.get('tag_type'),
        'item_details':request_data.get('item_details'),
        'sub_item_details':request_data.get('sub_item_details'),
        'calculation_type':request_data.get('calculation_type'),
        'from_weight':float(request_data.get('from_weight')),
        'to_weight':float(request_data.get('to_weight'))
        }

        res_data['modified_by']=request.user.id
        res_data['modified_at']=timezone.now()

        from_weight=float(request_data.get('from_weight'))
        to_weight=float(request_data.get('to_weight'))


        if str(request_data['calculation_type']) == settings.FIXEDRATE :

            res_data['max_fixed_rate']=float(request_data.get('max_fixed_rate'))

            fixed_rate_data={
            "max_fixed_rate":float(res_data['max_fixed_rate'])
            }

        elif str(request_data['calculation_type'])==settings.PERGRAMRATE:

            res_data['max_per_gram_rate']=float(request_data.get('max_per_gram_rate'))

            pergram_rate_data={
                "max_pergram_rate":float(res_data['max_per_gram_rate'])
            }

        elif str(request_data['calculation_type'])==settings.PERPIECERATE:

            res_data['min_per_piece_rate']=float(request_data.get('min_per_piece_rate'))
            res_data['per_piece_rate']=float(request_data.get('per_piece_rate'))

            perpiece_rate_data={
                "min_per_piece_rate":float(res_data.get('min_per_piece_rate')),
                "per_piece_rate":float(res_data.get('per_piece_rate'))
            }

        else:

            res_data['max_wastage_percent']=float(request_data.get('max_wastage_percent'))
            res_data['max_flat_wastage']=float(request_data.get('max_flat_wastage'))
            res_data['max_making_charge_gram']=float(request_data.get('max_making_charge_gram'))
            res_data['max_flat_making_charge']=float(request_data.get('max_flat_making_charge'))

            weight_calcluation_data={
            "max_wastage_percent":res_data.get('max_wastage_percent'),
            "max_flat_wastage":res_data.get('max_flat_wastage'),
            "max_making_charge_gram": res_data.get('max_making_charge_gram'),
            "max_flat_making_charge":res_data.get('max_flat_making_charge'),
            }

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
        
        if from_weight <= 0 or to_weight <=0 :

            return Response(
                {
                    "message":"From Weight and To Weight cannot be less than or equal to Zero",
                    "status":status.HTTP_204_NO_CONTENT
                },status=status.HTTP_200_OK
            )

        queryset=ValueAdditionCustomer.objects.get(id=pk)

        serializer=ValueAdditionCustomerSerializer(queryset,data=res_data,partial=True)

        if serializer.is_valid():
            serializer.save()
            value_data=serializer.data

            try:

                tag_queryset=list(TaggedItems.objects.filter(tag_type= value_data['tag_type'],item_details__item_details= value_data['item_details'],sub_item_details= value_data['sub_item_details'],calculation_type= value_data['calculation_type'],gross_weight__range=(value_data['from_weight'],value_data['to_weight'])))

                for tag in tag_queryset:

                    tag_value_queryset=TaggedItems.objects.get(id=tag.pk)

                    if str(serializer.data['calculation_type']) == settings.FIXEDRATE :

                        calc_data=fixed_rate_data

                    elif str(serializer.data['calculation_type']) ==settings.PERGRAMRATE:
                                        
                        calc_data=pergram_rate_data
                    
                    elif str(serializer.data['calculation_type']) ==settings.PERPIECERATE:
                                        
                        calc_data=perpiece_rate_data

                    else:
                        calc_data=weight_calcluation_data

                    tag_value_serializer=TaggedItemsSerializer(tag_value_queryset,data=calc_data,partial=True)

                    if tag_value_serializer.is_valid():
                        tag_value_serializer.save()
            
            except TaggedItems.DoesNotExist:
                pass
            except Exception as err:
                pass

            return Response(
                {
                    "data":serializer.data,
                    "message":res_msg.update("Value Addition Customer"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        
        else:
            return Response(
                {
                    "data":serializer.errors,
                    "message":res_msg.not_update("Value Addition Customer"),
                    "stauts":status.HTTP_400_BAD_REQUEST
                },status=status.HTTP_200_OK
            )
        
    def destroy(self,request,pk):

        try:

            queryset=ValueAdditionCustomer.objects.get(id=pk)

            queryset.delete()

            return Response(
                {
                    "message":res_msg.delete("Value Addition Customer"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        
        except ValueAdditionCustomer.DoesNotExist:

            return Response(
                {
                    "message":res_msg.not_exists("Value Addition Customer"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        
        except Exception as err:
            pass

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])

class ValueAdditionCustomerList(APIView):

    def post(self,request):

        request_data=request.data

        search = request_data.get('search') if request_data.get('search') else ''
        from_date = request_data.get('from_date') if request_data.get('from_date') else None
        to_date = request_data.get('to_date') if request_data.get('to_date') else None
        page = request.data.get('page') if request.data.get('page') else 1
        items_per_page = request.data.get('items_per_page') if request.data.get('items_per_page') else 10
        
        try:
            items_per_page = int(request.data.get('items_per_page', ValueAdditionCustomer.objects.all().count()))
            if items_per_page == 0:
                items_per_page = 10 
        except Exception as err:
            items_per_page = 10 

        filter_conditions = {}
        combined_conditions = Q()
        if search != "":
            or_conditions = []
            or_conditions.append(Q(sub_item_details__sub_item_name__icontains=search))
            or_conditions.append(Q(calculation_type__calculation_name__icontains=search))
            or_conditions.append(Q(tag_type__tag_name__icontains=search))
            or_conditions.append(Q(stock_type__stock_type_name__icontains=search))

            for condition in or_conditions:
                combined_conditions |= condition

        if from_date != None and to_date!= None:
            fdate =from_date+'T00:00:00.899010+05:30'
            tdate =to_date+'T23:59:59.899010+05:30'
            date_range=(fdate,tdate)
            filter_conditions['created_at__range']=date_range

        if len(filter_conditions) != 0 :

            queryset=list(ValueAdditionCustomer.objects.filter(combined_conditions, **filter_conditions).order_by('id'))

        else:

            queryset=list(ValueAdditionCustomer.objects.filter(combined_conditions).order_by('id'))

        paginated_data = Paginator(queryset, items_per_page)
        serializer = ValueAdditionCustomerSerializer(paginated_data.get_page(page), many=True)
        
        for i in range(len(serializer.data)):
            dict_data = serializer.data[i]
            try:
                staff = Staff.objects.get(phone =queryset[i].created_by.phone)
                dict_data['created_by'] = staff.first_name
            except:
                dict_data['created_by'] = None
            dict_data['sub_item_name'] = queryset[i].sub_item_details.sub_item_name
            dict_data['metal_name'] = queryset[i].metal.metal_name,
            dict_data['stock_type_name'] = queryset[i].stock_type.stock_type_name
            dict_data['tag_type_name'] = queryset[i].tag_type.tag_name
            dict_data['calculation_type_name'] = queryset[i].calculation_type.calculation_name


        return Response(
            {
                "data":{
                    "list":serializer.data,
                    "total_pages": paginated_data.num_pages,
                    "current_page": page,
                    "total_items": len(queryset),
                    "current_items": len(serializer.data)
                },
                "message":res_msg.retrieve("Value Addition"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )



@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ValueAdditionDesignerView(viewsets.ViewSet):

    def create(self,request):

        try:

            request_data=request.data
        
            res_data={
                "designer_name":request_data.get('designer'),
                "metal_name":request_data.get('metal'),
                "item_name":request_data.get('item_details'),
                "tag_type":request_data.get('tag_type'),
                "calculation_type":request_data.get('calculation_type'),
                "sub_item_name":request_data.get('sub_item'),
                "purchase_fixed_rate":request_data.get('purchase_fixed_rate'),
                "purchase_pergram_rate":request_data.get('purchase_pergram_rate'),
                "purchase_pergram_weight_type":request_data.get('purchase_pergram_weight_type'),
                "purchase_perpiece_rate":request_data.get('purchase_perpiece_rate'),
                "purchase_touch":request_data.get('purchase_touch'),
                "purchase_wastage_calculation_type":request_data.get('purchase_wastage_calculation_type'),
                "purchase_wastage_percent":request_data.get('purchase_wastage_percent'),
                "purchase_flat_wastage":request_data.get('purchase_flat_wastage'),
                "purchase_making_charge_calculation_type":request_data.get('purchase_making_charge_calculation_type'),
                "purchase_making_charge_gram":request_data.get('purchase_making_charge_gram'),
                "purchase_flat_making_charge":request_data.get('purchase_flat_making_charge'),
                "retail_touch":request_data.get('retail_touch'),
                "retail_wastage_percent":request_data.get('retail_wastage_percent'),
                "retail_flat_wastage":request_data.get('retail_flat_wastage'),
                "retail_making_charge_gram":request_data.get('retail_making_charge_gram'),
                "retail_flat_making_charge":request_data.get('retail_flat_making_charge'),
                "vip_touch":request_data.get('vip_touch'),
                "vip_wastage_percent":request_data.get('vip_wastage_percent'),
                "vip_flat_wastage":request_data.get('vip_flat_wastage'),
                "vip_making_charge_gram":request_data.get('vip_making_charge_gram'),
                "vip_flat_making_charge":request_data.get('vip_flat_making_charge'),
            }
           
            response_data=[]
            response_errors=[]

            try:
                value_addition_designer_queryset = ValueAdditionDesigner.objects.get(designer_name=res_data['designer_name'],metal_name=res_data['metal_name'],item_name=res_data['item_name'],sub_item_name=res_data['sub_item_name'],tag_type=res_data['tag_type'])
                res_data['modified_at'] = timezone.now()
                res_data['modified_by'] = request.user.id

                old_value_addition_serializer = ValueAdditionDesignerSerializer(value_addition_designer_queryset,data=res_data,partial=True)
                if old_value_addition_serializer.is_valid():
                    old_value_addition_serializer.save()
                    response_data.append(old_value_addition_serializer.data)

                else:
                    return Response(
                    {
                        "data":response_errors,
                        "status":status.HTTP_400_BAD_REQUEST
                    },status=status.HTTP_200_OK)
                    
                return Response(
                {
                    "data": response_data,
                    "message":res_msg.create("Value Addition Designer"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
                )
            except Exception as error:
                
                res_data['created_at'] = timezone.now()
                res_data['created_by'] = request.user.id
                new_value_addition_serializer = ValueAdditionDesignerSerializer(data=res_data)
                if new_value_addition_serializer.is_valid():
                    new_value_addition_serializer.save()
                    
                else:
                    return Response(
                    {
                        "data":new_value_addition_serializer,
                        "status":status.HTTP_400_BAD_REQUEST
                    },status=status.HTTP_200_OK)

                return Response(
                    {
                        "data":response_data,
                        "message":res_msg.update("Value Addition Designer"),
                        "status":status.HTTP_200_OK
                    },status=status.HTTP_200_OK
                )

        except Exception as err:

            return Response(
                {
                    "message":res_msg.something_else(),
                    "status":status.HTTP_204_NO_CONTENT
                },status=status.HTTP_200_OK
            )
        
    def retrieve(self,request,pk):

        try:

            queryset=ValueAdditionDesigner.objects.get(id=pk)

            serializer=ValueAdditionDesignerSerializer(queryset)

            res_data = serializer.data
            res_data['sub_item'] = queryset.sub_item_name.pk
            res_data['sub_item_name_name'] = queryset.sub_item_name.sub_item_name
            return Response(
                {
                    "data":res_data,
                    "message":res_msg.retrieve("Value Addition"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        
        except ValueAdditionDesigner.DoesNotExist:

            return Response(
                {
                    "message":res_msg.not_exists("Value Addition"),
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
        
    def update(self,request,pk):

        try:

            queryset=ValueAdditionDesigner.objects.get(id=pk)

            request_data=request.data
            
            request_data['purchase_touch']=float(request_data['purchase_touch']) if 'purchase_touch' in request_data  else queryset.purchase_touch
            request_data['purchase_wastage_percent']=float(request_data['purchase_wastage_percent']) if 'purchase_wastage_percent' in request_data  else queryset.purchase_wastage_percent
            request_data['purchase_flat_wastage']=float(request_data['purchase_flat_wastage']) if 'purchase_flat_wastage' in request_data  else queryset.purchase_flat_wastage
            request_data['purchase_making_charge_gram']=float(request_data['purchase_making_charge_gram']) if 'purchase_making_charge_gram' in request_data  else queryset.purchase_making_charge_gram
            request_data['purchase_flat_making_charge']=float(request_data['purchase_flat_making_charge']) if 'purchase_flat_making_charge' in request_data  else queryset.purchase_flat_making_charge

            request_data['retail_touch']=float(request_data['retail_touch']) if 'retail_touch' in request_data  else queryset.retail_touch
            request_data['retail_wastage_percent']=float(request_data['retail_wastage_percent']) if 'retail_wastage_percent' in request_data  else queryset.retail_wastage_percent
            request_data['retail_flat_wastage']=float(request_data['retail_flat_wastage']) if 'retail_flat_wastage' in request_data  else queryset.retail_flat_wastage
            request_data['retail_making_charge_gram']=float(request_data['retail_making_charge_gram']) if 'retail_making_charge_gram' in request_data  else queryset.retail_making_charge_gram
            request_data['retail_flat_making_charge']=float(request_data['retail_flat_making_charge']) if 'retail_flat_making_charge' in request_data  else queryset.retail_flat_making_charge

            request_data['vip_touch']=float(request_data['vip_touch']) if 'vip_touch' in request_data  else queryset.vip_touch
            request_data['vip_wastage_percent']=float(request_data['vip_wastage_percent']) if 'vip_wastage_percent' in request_data  else queryset.vip_wastage_percent
            request_data['vip_flat_wastage']=float(request_data['vip_flat_wastage']) if 'vip_flat_wastage' in request_data  else queryset.vip_flat_wastage
            request_data['vip_making_charge_gram']=float(request_data['vip_making_charge_gram']) if 'vip_making_charge_gram' in request_data  else queryset.vip_making_charge_gram
            request_data['vip_flat_making_charge']=float(request_data['vip_flat_making_charge']) if 'vip_flat_making_charge' in request_data  else queryset.vip_flat_making_charge

            request_data['modified_at']=timezone.now()
            request_data['modified_by']=request.user.id

            serializer=ValueAdditionDesignerSerializer(queryset,data=request_data,partial=True)

            if serializer.is_valid():
                serializer.save()

                return Response(
                    {
                        "data":serializer.data,
                        "message":res_msg.update("Value Addition Designer"),
                        "status":status.HTTP_200_OK
                    },status=status.HTTP_200_OK
                )
            
            else:

                return Response(
                    {
                        "data":serializer.errors,
                        "message":res_msg.not_update("Value Addition Designer"),
                        "status":status.HTTP_400_BAD_REQUEST
                    },status=status.HTTP_200_OK
                )
            
        except ValueAdditionDesigner.DoesNotExist:

            return Response(
                {
                    "message":res_msg.not_exists("Value Addition Designer"),
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
    

        
    def destroy(self,request,pk):

        try:

            queryset=ValueAdditionDesigner.objects.get(id=pk)

            queryset.purchase_touch = 0
            queryset.purchase_wastage_percent = 0
            queryset.purchase_flat_wastage = 0
            queryset.purchase_making_charge_gram = 0
            queryset.purchase_flat_making_charge = 0
            queryset.retail_touch = 0
            queryset.retail_wastage_percent = 0
            queryset.retail_flat_wastage = 0
            queryset.retail_making_charge_gram = 0
            queryset.retail_flat_making_charge = 0
            queryset.vip_touch = 0 
            queryset.vip_wastage_percent = 0
            queryset.vip_flat_wastage = 0
            queryset.vip_making_charge_gram = 0
            queryset.vip_flat_making_charge = 0

            queryset.save()

            return Response(
                {
                    "message":"Value Addition Designer Reset Successfully",
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        
        except ValueAdditionDesigner.DoesNotExist:

            return Response(
                {
                    "message":res_msg.not_exists("Value Addition Designer"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        
        except Exception as err:

            return Response(
                {
                    "message":res_msg.something_else(),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )

        

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])

class ValueAdditionDesignerList(APIView):

    def post(self,request):

        try:
            request_data=request.data

            search = request_data.get('search') if request_data.get('search') else ''
            from_date = request_data.get('from_date') if request_data.get('from_date') else None
            to_date = request_data.get('to_date') if request_data.get('to_date') else None
            page = request.data.get('page') if request.data.get('page') else 1
            items_per_page = request.data.get('items_per_page') if request.data.get('items_per_page') else 10
           
            # try:
            #     items_per_page = int(request.data.get('items_per_page', ValueAdditionDesigner.objects.all().count()))
            #     if items_per_page == 0:
            #         items_per_page = 10 
            # except Exception as err:
            #     items_per_page = 10 

            filter_conditions={}
            
            if from_date != None and to_date!= None:
                fdate =from_date+'T00:00:00.899010+05:30'
                tdate =to_date+'T23:59:59.899010+05:30'
                date_range=(fdate,tdate)
                filter_conditions['created_at__range']=date_range

            if len(filter_conditions) != 0:

                queryset = list(ValueAdditionDesigner.objects.filter(**filter_conditions).values('id','designer_name__account_head_name','metal_name__metal_name','item_name__item_name','sub_item_name__sub_item_name','tag_type__tag_name','purchase_touch','purchase_wastage_percent','purchase_flat_wastage','purchase_making_charge_gram','purchase_flat_making_charge','retail_touch','retail_wastage_percent','retail_flat_wastage','retail_making_charge_gram','retail_flat_making_charge','vip_touch','vip_wastage_percent','vip_flat_wastage','vip_making_charge_gram','vip_flat_making_charge','created_at','branch__branch_name').order_by('id'))

            else:

                queryset = list(ValueAdditionDesigner.objects.all().values('id','designer_name__account_head_name','metal_name__metal_name','item_name__item_name','sub_item_name__sub_item_name','tag_type__tag_name','purchase_touch','purchase_wastage_percent','purchase_flat_wastage','purchase_making_charge_gram','purchase_flat_making_charge','retail_touch','retail_wastage_percent','retail_flat_wastage','retail_making_charge_gram','retail_flat_making_charge','vip_touch','vip_wastage_percent','vip_flat_wastage','vip_making_charge_gram','vip_flat_making_charge','created_at','branch__branch_name').order_by('id'))

            paginated_data = Paginator(queryset, items_per_page)
            serializer = ValueAdditionDesignerSerializer(paginated_data.get_page(page), many=True)
            

            return Response(
                {
                    "data":{
                        "list":serializer.data,
                        "total_pages": paginated_data.num_pages,
                        "current_page": page,
                        "total_items": len(queryset),
                        "current_items": len(serializer.data)
                    },
                    "message":res_msg.retrieve("Value Addition Designer List"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        
        except Exception as err:
            pass
            

# @authentication_classes([TokenAuthentication]) 
# @permission_classes([IsAuthenticated])
# class SubitemDetailsAPIView(APIView):
#     def post(self,request):
        
#         request_data = request.data

#         queryset = list(SubItem.objects.filter(item_details=request_data.get('item'),metal=request_data.get('metal')))

#         serializer = SubItemSerializer(queryset, many=True)
       
#         res_data = []
#         for i in range(0,len(serializer.data)):
#             dict_data = serializer.data[i]
#             dict_data['item_name'] = queryset[i].item_details.item_name
#             dict_data['metal_name'] = queryset[i].metal.metal_name
#             dict_data['purity_name'] = queryset[i].purity.purity_name
#             dict_data['stock_type_name'] = queryset[i].stock_type.stock_type_name
#             dict_data['calculation_type_name'] = queryset[i].calculation_type.calculation_name
#             dict_data['measurement_type_name'] = queryset[i].measurement_type.measurement_name
#             dict_data['sub_item_counter_name'] = queryset[i].sub_item_counter.counter_name
#             try:
#                 valueaddition_queryset = ValueAdditionDesigner.objects.get(designer_name=request_data['designer'],tag_type=request_data['tag_type'],item_name=queryset[i].item_details,sub_item_name=queryset[i].pk,metal_name=queryset[i].metal)
#                 valueaddition_serializer = ValueAdditionDesignerSerializer(valueaddition_queryset)
                
#                 if valueaddition_serializer.data:
                    
#                     dict_data['value_addition_id'] = valueaddition_queryset.pk
#                     dict_data['designer'] = valueaddition_queryset.designer_name.pk
#                     dict_data['designer_name'] = valueaddition_queryset.designer_name.account_head_name
#                     dict_data['tag_type'] = valueaddition_queryset.tag_type.pk
#                     dict_data['tag_type_name'] = valueaddition_queryset.tag_type.tag_name
#                     dict_data['purchase_touch'] = valueaddition_queryset.purchase_touch
#                     dict_data['purchase_wastage_percent'] = valueaddition_queryset.purchase_wastage_percent
#                     dict_data['purchase_flat_wastage'] = valueaddition_queryset.purchase_flat_wastage
#                     dict_data['purchase_making_charge_gram'] = valueaddition_queryset.purchase_making_charge_gram
#                     dict_data['purchase_flat_making_charge'] = valueaddition_queryset.purchase_flat_making_charge
#                     dict_data['retail_touch'] = valueaddition_queryset.retail_touch 
#                     dict_data['retail_wastage_percent'] = valueaddition_queryset.retail_wastage_percent
#                     dict_data['retail_flat_wastage'] = valueaddition_queryset.retail_flat_wastage
#                     dict_data['retail_making_charge_gram'] = valueaddition_queryset.retail_making_charge_gram
#                     dict_data['retail_flat_making_charge'] = valueaddition_queryset.retail_flat_making_charge
#                     dict_data['vip_touch'] = valueaddition_queryset.vip_touch
#                     dict_data['vip_wastage_percent'] = valueaddition_queryset.vip_wastage_percent
#                     dict_data['vip_flat_wastage'] = valueaddition_queryset.vip_flat_wastage
#                     dict_data['vip_making_charge_gram'] = valueaddition_queryset.vip_making_charge_gram
#                     dict_data['vip_flat_making_charge'] = valueaddition_queryset.vip_flat_making_charge
#             except ValueAdditionDesigner.DoesNotExist:
#                 designer_queryset = AccountHeadDetails.objects.get(id=request_data['designer'])
#                 tag_queryset = TagTypes.objects.get(id=request_data['tag_type'])
#                 dict_data['value_addition_id'] = None
#                 dict_data['designer'] = request_data['designer']
#                 dict_data['designer_name'] = designer_queryset.account_head_name
#                 dict_data['tag_type'] = request_data['tag_type']
#                 dict_data['tag_type_name'] = tag_queryset.tag_name
#                 dict_data['purchase_touch'] = 0
#                 dict_data['purchase_wastage_percent'] = 0
#                 dict_data['purchase_flat_wastage'] = 0 
#                 dict_data['purchase_making_charge_gram'] = 0 
#                 dict_data['purchase_flat_making_charge'] = 0 
#                 dict_data['retail_touch'] = 0
#                 dict_data['retail_wastage_percent'] = 0
#                 dict_data['retail_flat_wastage'] = 0 
#                 dict_data['retail_making_charge_gram'] = 0
#                 dict_data['retail_flat_making_charge'] = 0
#                 dict_data['vip_touch'] = 0 
#                 dict_data['vip_wastage_percent'] = 0 
#                 dict_data['vip_flat_wastage'] = 0 
#                 dict_data['vip_making_charge_gram'] =0
#                 dict_data['vip_flat_making_charge'] = 0

#             res_data.append(dict_data)

#         return Response(
#             {
#                 "data" : res_data,
#                 "message" : res_msg.retrieve('Sub Item Details'),
#                 "status": status.HTTP_200_OK
#             }, status=status.HTTP_200_OK
#         )  
    


@authentication_classes([TokenAuthentication]) 
@permission_classes([IsAuthenticated])
class SubitemDetailsAPIView(APIView):
    def post(self,request):
        
        request_data = request.data
        
        item = request_data.get('item',[])
        queryset = list(SubItem.objects.filter(item_details__in=item,metal=request_data.get('metal')))
        
        serializer = SubItemSerializer(queryset, many=True)
        res_data = []
        for i in range(0,len(serializer.data)):
            dict_data = serializer.data[i]
            dict_data['item_name'] = queryset[i].item_details.item_name
            dict_data['metal_name'] = queryset[i].metal.metal_name
            dict_data['purity_name'] = queryset[i].purity.purity_name
            dict_data['stock_type_name'] = queryset[i].stock_type.stock_type_name
            dict_data['calculation_type_name'] = queryset[i].calculation_type.calculation_name
            dict_data['measurement_type_name'] = queryset[i].measurement_type.measurement_name
            dict_data['sub_item_counter_name'] = queryset[i].sub_item_counter.counter_name
            
            designer_ids = request_data.get('designer',[])
            for designer_id in designer_ids:
                try:
                    valueaddition_queryset = ValueAdditionDesigner.objects.get(designer_name=designer_id,tag_type=request_data['tag_type'],item_name=queryset[i].item_details,sub_item_name=queryset[i].pk,metal_name_id=queryset[i].metal)
                    valueaddition_serializer = ValueAdditionDesignerSerializer(valueaddition_queryset)
                    
                    if valueaddition_serializer.data:
                        
                        dict_data['value_addition_id'] = valueaddition_queryset.pk
                        dict_data['designer'] = valueaddition_queryset.designer_name.pk
                        dict_data['designer_name'] = valueaddition_queryset.designer_name.account_head_name
                        dict_data['tag_type'] = valueaddition_queryset.tag_type.pk
                        dict_data['tag_type_name'] = valueaddition_queryset.tag_type.tag_name
                        dict_data['purchase_fixed_rate'] = valueaddition_queryset.purchase_fixed_rate

                        if valueaddition_queryset.purchase_pergram_weight_type != None:
                            dict_data['purchase_pergram_weight_type'] = valueaddition_queryset.purchase_pergram_weight_type.pk
                        else: 
                            dict_data['purchase_pergram_weight_type'] = None
                        dict_data['purchase_pergram_rate'] = valueaddition_queryset.purchase_pergram_rate

                        dict_data['purchase_perpiece_rate'] = valueaddition_queryset.purchase_perpiece_rate
                        dict_data['purchase_touch'] = valueaddition_queryset.purchase_touch
                        if valueaddition_queryset.purchase_wastage_calculation_type != None:
                            dict_data['purchase_wastage_calculation_type'] = valueaddition_queryset.purchase_wastage_calculation_type.pk
                        else:
                            dict_data['purchase_wastage_calculation_type'] = None
                        dict_data['purchase_wastage_percent'] = valueaddition_queryset.purchase_wastage_percent
                        dict_data['purchase_flat_wastage'] = valueaddition_queryset.purchase_flat_wastage

                        if valueaddition_queryset.purchase_making_charge_calculation_type != None:
                            dict_data['purchase_making_charge_calculation_type'] = valueaddition_queryset.purchase_making_charge_calculation_type.pk
                        else:
                            dict_data['purchase_making_charge_calculation_type'] = None

                        dict_data['purchase_making_charge_gram'] = valueaddition_queryset.purchase_making_charge_gram
                        dict_data['purchase_flat_making_charge'] = valueaddition_queryset.purchase_flat_making_charge
                        dict_data['retail_touch'] = valueaddition_queryset.retail_touch 
                        dict_data['retail_wastage_percent'] = valueaddition_queryset.retail_wastage_percent
                        dict_data['retail_flat_wastage'] = valueaddition_queryset.retail_flat_wastage
                        dict_data['retail_making_charge_gram'] = valueaddition_queryset.retail_making_charge_gram
                        dict_data['retail_flat_making_charge'] = valueaddition_queryset.retail_flat_making_charge
                        dict_data['vip_touch'] = valueaddition_queryset.vip_touch
                        dict_data['vip_wastage_percent'] = valueaddition_queryset.vip_wastage_percent
                        dict_data['vip_flat_wastage'] = valueaddition_queryset.vip_flat_wastage
                        dict_data['vip_making_charge_gram'] = valueaddition_queryset.vip_making_charge_gram
                        dict_data['vip_flat_making_charge'] = valueaddition_queryset.vip_flat_making_charge
                except ValueAdditionDesigner.DoesNotExist:
                    designer_queryset = AccountHeadDetails.objects.get(id=designer_id)
                    tag_queryset = TagTypes.objects.get(id=request_data['tag_type'])
                    dict_data['value_addition_id'] = None
                    dict_data['designer'] = designer_id
                    dict_data['designer_name'] = designer_queryset.account_head_name
                    dict_data['tag_type'] = request_data['tag_type']
                    dict_data['tag_type_name'] = tag_queryset.tag_name
                    dict_data['purchase_fixed_rate'] = 0
                    dict_data['purchase_pergram_rate'] = 0
                    dict_data['purchase_pergram_weight_type'] = None
                    dict_data['purchase_perpiece_rate'] = 0
                    dict_data['purchase_touch'] = 0
                    dict_data['purchase_wastage_calculation_type'] = None
                    dict_data['purchase_wastage_percent'] = 0
                    dict_data['purchase_flat_wastage'] = 0 
                    dict_data['purchase_making_charge_calculation_type'] = None
                    dict_data['purchase_making_charge_gram'] = 0 
                    dict_data['purchase_flat_making_charge'] = 0 
                    dict_data['retail_touch'] = 0
                    dict_data['retail_wastage_percent'] = 0
                    dict_data['retail_flat_wastage'] = 0 
                    dict_data['retail_making_charge_gram'] = 0
                    dict_data['retail_flat_making_charge'] = 0
                    dict_data['vip_touch'] = 0 
                    dict_data['vip_wastage_percent'] = 0 
                    dict_data['vip_flat_wastage'] = 0 
                    dict_data['vip_making_charge_gram'] =0
                    dict_data['vip_flat_making_charge'] = 0

            res_data.append(dict_data)

        return Response(
            {
                "data" : res_data,
                "message" : res_msg.retrieve('Sub Item Details'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK
        )  
    

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class TagValueView(APIView):
    def post(self,reqeuest):
       
        metal = reqeuest.data.get('metal')
        tag_type = reqeuest.data.get('tag_type')
        sub_item_details = reqeuest.data.get('sub_item_details')
        calculation_type = reqeuest.data.get('calculation_type')
        gross_weight = float(reqeuest.data.get('gross_weight'))
       
        response_dict = {}
       
        try:
           
            tag_value_queryset=ValueAdditionCustomer.objects.filter(metal=metal,tag_type=tag_type,sub_item_details=sub_item_details,calculation_type=calculation_type)
 
            for value in tag_value_queryset :
 
                if float(value.from_weight) <= gross_weight <= float(value.to_weight) :
                       
                    if str(calculation_type) == settings.FIXEDRATE :
                           
                        response_dict['max_fixed_rate']=float(value.max_fixed_rate)
 
                        break
 
                    elif str(calculation_type) == settings.PERGRAMRATE :
                               
                        response_dict['max_pergram_rate']=float(value.max_per_gram_rate)
 
                        break
                    
                    elif str(calculation_type) == settings.PERPIECERATE :
                               
                        response_dict['min_per_piece_rate']=float(value.min_per_piece_rate)
                        response_dict['per_piece_rate']=float(value.per_piece_rate)
 
                        break
                           
                    else :
                           
                        response_dict['max_wastage_percent']=float(value.max_wastage_percent)
                        response_dict['max_flat_wastage']=float(value.max_flat_wastage)
                        response_dict['max_making_charge_gram']=float(value.max_making_charge_gram)
                        response_dict['max_flat_making_charge']=float(value.max_flat_making_charge)
 
                        break
                           
                else:
                    pass
 
        except ValueAdditionCustomer.DoesNotExist:
 
            if str(calculation_type) == settings.FIXEDRATE :
 
                response_dict['max_fixed_rate'] = 0
 
            elif str(calculation_type) == settings.PERGRAMRATE :
 
                response_dict['max_pergram_rate'] = 0

            elif str(calculation_type) == settings.PERPIECERATE :
 
                response_dict['per_piece_rate'] = 0
                response_dict['min_per_piece_rate'] = 0
 
            else:
                   
                response_dict['max_wastage_percent'] = 0
                response_dict['max_flat_wastage'] = 0
                response_dict['max_making_charge_gram'] = 0
                response_dict['max_flat_making_charge'] = 0
               
        return Response(
            {
                "data":response_dict,
                "message":res_msg.retrieve("Tag Value Details"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class PurchaseTagValueView(APIView):
    
    def post(self,request):
        
        try:
            
            designer_name = request.data.get('designer')
            metal = request.data.get('metal')
            item_details = request.data.get('item')
            
            queryset = ValueAdditionDesigner.objects.get(designer_name=designer_name,metal_name = metal,item_name=item_details)
            
            res_data = {
                "purchase_touch":queryset.purchase_touch,
                "purchase_wastage_percent":queryset.purchase_wastage_percent,
                "purchase_flat_wastage":queryset.purchase_flat_wastage,
                "purchase_making_charge_gram":queryset.purchase_making_charge_gram,
                "purchase_flat_making_charge":queryset.purchase_flat_making_charge,
            }
            
            return Response(
                {
                    "data":res_data,
                    "message":res_msg.retrieve("Purchase Value addition"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
            
        except:
            res_data = {
                "purchase_touch":0,
                "purchase_wastage_percent":0,
                "purchase_flat_wastage":0,
                "purchase_making_charge_gram":0,
                "purchase_flat_making_charge":0,
            }
            return Response(
                {
                    "data":res_data,
                    "message":res_msg.retrieve("Purchase Value addition"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        

    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class FlatWastageTypeView(APIView):
    def get(self,request):
        try:
            queryset=list(FlatWastageType.objects.filter(is_active=True).values('id','type_name'))
            return Response(
                {
                    "data":{
                        "list":queryset
                        },
                    "message":res_msg.retrieve("Flat Wastage Type"),
                    "status":status.HTTP_200_OK
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
class ValueadditionDesignerDetailsView(APIView):
    def post(self,request):
        
        request_data = request.data
        
        items = request_data.get('item',[])
       
        res_data = []
        for item in items:

            item_queryset = Item.objects.get(id=item)

            dict_data = {}
            dict_data['item_id'] = item_queryset.item_id
            dict_data['item_name'] = item_queryset.item_name
            dict_data['metal'] = item_queryset.metal.pk
            dict_data['metal_name'] = item_queryset.metal.metal_name
            dict_data['purity'] = item_queryset.purity.pk
            dict_data['purity_name'] = item_queryset.purity.purity_name
            dict_data['stock_type'] = item_queryset.stock_type.pk
            dict_data['stock_type_name'] = item_queryset.stock_type.stock_type_name
            dict_data['calculation_type'] = item_queryset.calculation_type.pk
            dict_data['calculation_type_name'] = item_queryset.calculation_type.calculation_name
            dict_data['item_counter'] = item_queryset.item_counter.pk
            dict_data['item_counter_name'] = item_queryset.item_counter.counter_name

            designer_ids = request_data.get('designer',[])
            for designer_id in designer_ids:
                try:
                    valueaddition_queryset = ValueAdditionDesigner.objects.get(designer_name=designer_id,item_name=item)
                    valueaddition_serializer = ValueAdditionDesignerSerializer(valueaddition_queryset)
                    
                    if valueaddition_serializer.data:
                        
                        dict_data['value_addition_id'] = valueaddition_queryset.pk
                        dict_data['designer'] = valueaddition_queryset.designer_name.pk
                        dict_data['designer_name'] = valueaddition_queryset.designer_name.account_head_name
                        dict_data['purchase_fixed_rate'] = valueaddition_queryset.purchase_fixed_rate

                        if valueaddition_queryset.purchase_pergram_weight_type != None:
                            dict_data['purchase_pergram_weight_type'] = valueaddition_queryset.purchase_pergram_weight_type.pk
                        else: 
                            dict_data['purchase_pergram_weight_type'] = None
                        dict_data['purchase_pergram_rate'] = valueaddition_queryset.purchase_pergram_rate

                        dict_data['purchase_perpiece_rate'] = valueaddition_queryset.purchase_perpiece_rate
                        dict_data['purchase_touch'] = valueaddition_queryset.purchase_touch
                        if valueaddition_queryset.purchase_wastage_calculation_type != None:
                            dict_data['purchase_wastage_calculation_type'] = valueaddition_queryset.purchase_wastage_calculation_type.pk
                        else:
                            dict_data['purchase_wastage_calculation_type'] = None
                        dict_data['purchase_wastage_percent'] = valueaddition_queryset.purchase_wastage_percent
                        dict_data['purchase_flat_wastage'] = valueaddition_queryset.purchase_flat_wastage
                        if valueaddition_queryset.purchase_making_charge_calculation_type != None:
                            dict_data['purchase_making_charge_calculation_type'] = valueaddition_queryset.purchase_making_charge_calculation_type.pk
                        else:
                            dict_data['purchase_making_charge_calculation_type'] = None

                        dict_data['purchase_making_charge_gram'] = valueaddition_queryset.purchase_making_charge_gram
                        dict_data['purchase_flat_making_charge'] = valueaddition_queryset.purchase_flat_making_charge
                        dict_data['retail_touch'] = valueaddition_queryset.retail_touch 
                        dict_data['retail_wastage_percent'] = valueaddition_queryset.retail_wastage_percent
                        dict_data['retail_flat_wastage'] = valueaddition_queryset.retail_flat_wastage
                        dict_data['retail_making_charge_gram'] = valueaddition_queryset.retail_making_charge_gram
                        dict_data['retail_flat_making_charge'] = valueaddition_queryset.retail_flat_making_charge
                        dict_data['vip_touch'] = valueaddition_queryset.vip_touch
                        dict_data['vip_wastage_percent'] = valueaddition_queryset.vip_wastage_percent
                        dict_data['vip_flat_wastage'] = valueaddition_queryset.vip_flat_wastage
                        dict_data['vip_making_charge_gram'] = valueaddition_queryset.vip_making_charge_gram
                        dict_data['vip_flat_making_charge'] = valueaddition_queryset.vip_flat_making_charge
                except ValueAdditionDesigner.DoesNotExist:
                    designer_queryset = AccountHeadDetails.objects.get(id=designer_id)
                    dict_data['value_addition_id'] = None
                    dict_data['designer'] = designer_id
                    dict_data['designer_name'] = designer_queryset.account_head_name
                    dict_data['purchase_fixed_rate'] = 0
                    dict_data['purchase_pergram_rate'] = 0
                    dict_data['purchase_pergram_weight_type'] = None
                    dict_data['purchase_perpiece_rate'] = 0
                    dict_data['purchase_touch'] = 0
                    dict_data['purchase_wastage_calculation_type'] = None
                    dict_data['purchase_wastage_percent'] = 0
                    dict_data['purchase_flat_wastage'] = 0 
                    dict_data['purchase_making_charge_calculation_type'] = None
                    dict_data['purchase_making_charge_gram'] = 0 
                    dict_data['purchase_flat_making_charge'] = 0 
                    dict_data['retail_touch'] = 0
                    dict_data['retail_wastage_percent'] = 0
                    dict_data['retail_flat_wastage'] = 0 
                    dict_data['retail_making_charge_gram'] = 0
                    dict_data['retail_flat_making_charge'] = 0
                    dict_data['vip_touch'] = 0 
                    dict_data['vip_wastage_percent'] = 0 
                    dict_data['vip_flat_wastage'] = 0 
                    dict_data['vip_making_charge_gram'] =0
                    dict_data['vip_flat_making_charge'] = 0

            res_data.append(dict_data)

        return Response(
            {
                "data" : res_data,
                "message" : res_msg.retrieve('Sub Item Details'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK
        )  

            



