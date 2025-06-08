from organizations.models import Staff
from rest_framework import status, viewsets
from rest_framework.response import Response
from .models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes, authentication_classes
from django.utils import timezone
from django.db.models import ProtectedError
from django.db.models import Q
from app_lib.response_messages import ResponseMessages
from .serializer import *
from rest_framework.views import APIView
from django.core.paginator import Paginator
from django.core.files.storage import FileSystemStorage
import uuid
from django.db.models import ProtectedError
from django.conf import settings
from value_addition.models import *
from value_addition.serializer import *
from accounts.models import *
from django.db import transaction


res_msg = ResponseMessages()
# Create your views here.
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class CalculationTypeView(APIView):
    def get(self,request):

        try:

            queryset=list(CalculationType.objects.all().values('id','calculation_name'))

            return Response(
                {
                    "data":{
                        "list":queryset
                    },
                    "message":res_msg.retrieve("Calculation Type"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        except CalculationType.DoesNotExist:
            return Response(
                {
                    "message":res_msg.not_exists("Calculation Type"),
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
class StockTypeView(APIView):
    def get(self,request):

        try:

            queryset=list(StockType.objects.filter(is_active=True).values('id','stock_type_name'))

            return Response(
                {
                    "data":{
                        "list":queryset
                    },
                    "message":res_msg.retrieve("Stock Type"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        
        except StockType.DoesNotExist:
            return Response(
                {
                    "message":res_msg.not_exists("Stock Type"),
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
class MeasurementTypeView(APIView):
    def get(self,request):

        try:

            queryset=list(MeasurementType.objects.filter(is_active=True).values('id','measurement_name'))

            return Response(
                {
                    "data":{
                        "list":queryset
                            },
                    "message":res_msg.retrieve("Measurement Type"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        
        except MeasurementType.DoesNotExist:
            return Response(
                {
                    "message":res_msg.not_exists("Measurement Type"),
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
class WeightTypeView(APIView):
    def get(self,request):

        try:
            queryset=list(WeightType.objects.filter(is_active=True).values('id','weight_name'))

            return Response(
                {
                    "data":{
                        "list":queryset
                        },
                    "message":res_msg.retrieve("Weight Type"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        except WeightType.DoesNotExist:
            return Response(
                {
                    "message":res_msg.not_exists("Weight Type"),
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
class ItemIdview(APIView):
    def get(self,reuquest):
        try:
            queryset=ItemID.objects.all().order_by('-id')[0]
            new_id=int(queryset.item_id)+1
            return Response(
                {
                    "item_id":+new_id,
                    "message":res_msg.retrieve("Item ID"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        except Exception as err:

            return Response(
                {
                    "item_id":"1",
                    "message":res_msg.retrieve("Item ID"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ItemImageUpload(APIView):
 
    def post(self, request):
        request_file = request.FILES['image'] if 'image' in request.FILES else None
        if request_file:
            fs = FileSystemStorage()
            file_name = str(uuid.uuid1()) + str(request_file.name).replace(' ','-')
            file = fs.save(file_name, request_file)
            # the fileurl variable now contains the url to the file. This can be used to serve the file when needed.
            fileurl = fs.url(file)
 
            return Response({
                "item_image_url": fileurl,
                "message": 'Item Image uploaded',
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        return Response({
                "message": res_msg.something_else(),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
    
    def put(self, request, file):
        request_file = request.FILES['image'] if 'image' in request.FILES else None
        if request_file:
            fs = FileSystemStorage()
            file_name = file
            fs.delete(file)
            file = fs.save(file_name, request_file)
            # the fileurl variable now contains the url to the file. This can be used to serve the file when needed.
            fileurl = fs.url(file)
 
            return Response({
                "item_image_url": fileurl,
                "message": 'Item Image uploaded',
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        return Response({
                "message": res_msg.something_else(),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
    
def delete_item(pk):
    try:    
        queryset=Item.objects.get(id=pk)

        queryset.delete()
    except Exception as err:
        pass


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ItemDetailViewset(viewsets.ViewSet):
    @transaction.atomic
    def create(self,request):
        response_data={}
        try:

            request_data=request.data

            item_details={}
            item_details['metal']=request_data.get('metal')
            item_details['purity']=request_data.get('purity')
            item_details['hsn_code']=request_data.get('hsn_code')
            item_details['stock_type']=request_data.get('stock_type')
            item_details['item_id']=request_data.get('item_id')
            item_details['item_name']=request_data.get('item_name')
            item_details['item_image']=request_data.get('item_image')
            item_details['item_counter']=request_data.get('item_counter')
            item_details['allow_zero_weight']=request_data.get('allow_zero_weight')
            item_details['calculation_type']=request_data.get('calculation_type')
            item_details['huid_rate']=request_data.get('huid_rate')
            item_details['created_at']=timezone.now()
            item_details['created_by']=request.user.id

            item_serializer=ItemSerializer(data=item_details)

            if item_serializer.is_valid():
                item_serializer.save()
                response_data['item_details']=item_serializer.data
                item_id_dict={}
                item_id_dict['item_id']=item_details['item_id']
                item_id_serializer=ItemIDSerializer(data=item_id_dict)
                if item_id_serializer.is_valid():
                    item_id_serializer.save()
            
                
                calculation_details={}
                calculation_details['item_details']=item_serializer.data['id']
                calculation_details['created_at']=timezone.now()
                calculation_details['created_by']=request.user.id   
                

                if str(item_details['calculation_type']) == settings.FIXEDRATE:

                    calculation_details['fixed_rate']=request_data.get('fixed_rate')
                    fixed_serializer=FixedRateSerializer(data=calculation_details)

                    if fixed_serializer.is_valid():
                        fixed_serializer.save()
                        response_data['calculation_details']=fixed_serializer.data
                        return Response(
                            {
                                "data":response_data,
                                "message":res_msg.create("Item"),
                                "status":status.HTTP_201_CREATED
                            },status=status.HTTP_200_OK
                        )

                    else:
                        # delete_item(pk=item_serializer.data['id'])
                        raise Exception(fixed_serializer.errors)
                        return Response(
                            {
                                "data":fixed_serializer.errors,
                                "message":res_msg.not_create("Items"),
                                "status":status.HTTP_404_NOT_FOUND
                            },status=status.HTTP_200_OK
                        )
                    
                elif str(item_details['calculation_type']) == settings.PERGRAMRATE:

                    calculation_details['per_gram_rate']=request_data.get('per_gram_rate')
                    per_gram_serializer=PerGramRateSerializer(data=calculation_details)

                    if per_gram_serializer.is_valid():
                        per_gram_serializer.save()
                        response_data['calculation_details']=per_gram_serializer.data

                        return Response(
                            {
                                "data":response_data,
                                "message":res_msg.create("Item"),
                                "status":status.HTTP_201_CREATED
                            },status=status.HTTP_200_OK
                        )
                    else:
                        # delete_item(pk=item_serializer.data['id'])
                        raise Exception(per_gram_serializer.errors)
                        return Response(
                            {
                                "data":per_gram_serializer.errors,
                                "message":res_msg.not_create("Items"),
                                "status":status.HTTP_404_NOT_FOUND
                            },status=status.HTTP_200_OK
                        )


                elif str(item_details['calculation_type']) == settings.WEIGHTCALCULATION:

                    calculation_details['wastage_calculation']=request.data.get('wastage_calculation')
                    calculation_details['wastage_percent']=request.data.get('wastage_percent')
                    calculation_details['flat_wastage']=request.data.get('flat_wastage')
                    calculation_details['making_charge_calculation']=request.data.get('making_charge_calculation')
                    calculation_details['making_charge_gram']=request.data.get('making_charge_gram')
                    calculation_details['flat_making_charge']=request.data.get('flat_making_charge')
                    weight_serializer=WeightCalculationSerializer(data=calculation_details)

                    if weight_serializer.is_valid():
                        weight_serializer.save()
                        response_data['calculation_details']=weight_serializer.data

                        return Response(
                            {
                                "data":response_data,
                                "message":res_msg.create("Item"),
                                "status":status.HTTP_201_CREATED
                            },status=status.HTTP_200_OK
                        )

                    else:
                        # delete_item(pk=item_serializer.data['id'])
                        raise Exception(weight_serializer.errors)
                        return Response(
                            {
                                "data":weight_serializer.errors,
                                "message":res_msg.not_create("Items"),
                                "status":status.HTTP_404_NOT_FOUND
                            },status=status.HTTP_200_OK
                        )
                    
                elif str(item_details['calculation_type']) == settings.PERPIECERATE:

                    calculation_details['min_per_piece_rate']=request_data.get('min_per_piece_rate')
                    calculation_details['per_piece_rate']=request_data.get('per_piece_rate')
                    per_piece_serializer=PerPieceSerializer(data=calculation_details)

                    if per_piece_serializer.is_valid():
                        per_piece_serializer.save()
                        response_data['calculation_details']=per_piece_serializer.data

                        return Response(
                            {
                                "data":response_data,
                                "message":res_msg.create("Item"),
                                "status":status.HTTP_201_CREATED
                            },status=status.HTTP_200_OK
                        )
                    else:
                        # delete_item(pk=item_serializer.data['id'])
                        raise Exception(per_piece_serializer.errors)
                        return Response(
                            {
                                "data":per_piece_serializer.errors,
                                "message":res_msg.not_create("Items"),
                                "status":status.HTTP_404_NOT_FOUND
                            },status=status.HTTP_200_OK
                        )

            else:
                return Response(
                    {
                        "data":item_serializer.errors,
                        "message":res_msg.not_create("Items"),
                        "status":status.HTTP_404_NOT_FOUND
                    },status=status.HTTP_200_OK
                )
            
        except Exception as err:
            transaction.set_rollback(True)
            return Response(
                {
                    "data" : str(err),
                    "message":res_msg.something_else(),
                    "status":status.HTTP_204_NO_CONTENT
                },status=status.HTTP_200_OK
            )
        
            
        
    def retrieve(self,request,pk):
        try:

            item_queryset=Item.objects.get(id=pk)
            item_serializer=ItemSerializer(item_queryset)
            item_dict=item_serializer.data
            item_dict['purity_name']=item_queryset.purity.purity_name
            item_dict['metal_name']=item_queryset.metal.metal_name
            item_dict['stock_type_name']=item_queryset.stock_type.stock_type_name
            item_dict['calculation_type_name']=item_queryset.calculation_type.calculation_name
            item_dict['item_image']=settings.IMAGE_URL+str(item_queryset.item_image) if str(item_queryset.item_image) else ''

            if str(item_dict['calculation_type'])==settings.FIXEDRATE:
                try:
                    fixed_queryset=FixedRate.objects.get(item_details=pk)
                    item_dict['fixed_rate']=fixed_queryset.fixed_rate
                    
                except Exception as err:
                    return Response(
                        {
                            "message":res_msg.not_exists("Fixed Rate Details"),
                            "status":status.HTTP_404_NOT_FOUND
                        },status=status.HTTP_200_OK
                    )
            
            elif str(item_dict['calculation_type']) == settings.PERGRAMRATE :
                try:
                    per_gram_queryset=PerGramRate.objects.get(item_details=pk)
                    item_dict['per_gram_rate']=per_gram_queryset.per_gram_rate
                    
                except Exception as err:
                    return Response(
                        {
                            "message":res_msg.not_exists("Per Gram Rate Details"),
                            "status":status.HTTP_404_NOT_FOUND
                        },status=status.HTTP_200_OK
                    )
                
            elif str(item_dict['calculation_type']) == settings.PERPIECERATE:
                try:
                    per_piece_queryset=PerPiece.objects.get(item_details=pk)
                    item_dict['min_per_piece_rate']=per_piece_queryset.min_per_piece_rate
                    item_dict['per_piece_rate']=per_piece_queryset.per_piece_rate
                    
                except Exception as err:
                    return Response(
                        {
                            "message":res_msg.not_exists("Per Piece Details"),
                            "status":status.HTTP_404_NOT_FOUND
                        },status=status.HTTP_200_OK
                    )
                    
            else:
                try:
                    weight_queryset=WeightCalculation.objects.get(item_details=pk)
                    item_dict['wastage_calculation']=weight_queryset.wastage_calculation.pk
                    item_dict['wastage_calculation_name']=weight_queryset.wastage_calculation.weight_name
                    item_dict['wastage_percent']=weight_queryset.wastage_percent
                    item_dict['flat_wastage']=weight_queryset.flat_wastage
                    item_dict['making_charge_calculation']=weight_queryset.making_charge_calculation.pk
                    item_dict['making_charge_calculation_name']=weight_queryset.making_charge_calculation.weight_name
                    item_dict['making_charge_gram']=weight_queryset.making_charge_gram
                    item_dict['flat_making_charge']=weight_queryset.flat_making_charge
                except Exception as err:
                    return Response(
                        {
                            "message":res_msg.not_exists("Weight Calculation Details"),
                            "status":status.HTTP_404_NOT_FOUND
                        },status=status.HTTP_200_OK
                    )
            
            return Response(
                {
                    "data":item_dict,
                    "message":res_msg.retrieve("Item Details"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        except Exception as err:
            return Response(
                        {
                            "message":res_msg.not_exists("Item Details"),
                            "status":status.HTTP_404_NOT_FOUND
                        },status=status.HTTP_200_OK
                    )
    
    @transaction.atomic
    def update(self,request,pk):
        response_data={}
        try:

            item_queryset=Item.objects.get(id=pk)
            original_item_state = item_queryset.__dict__.copy()

            item_calculation_type=str(item_queryset.calculation_type.pk)

            item_details={}
            item_details['metal']=request.data.get('metal') 
            item_details['purity']=request.data.get('purity')   
            item_details['hsn_code']=request.data.get('hsn_code')   
            item_details['stock_type']=request.data.get('stock_type')   
            item_details['item_id']=request.data.get('item_id')     
            item_details['item_name']=request.data.get('item_name')   
            item_details['item_image']=request.data.get('item_image')   
            item_details['item_counter']=request.data.get('item_counter')   
            item_details['allow_zero_weight']=request.data.get('allow_zero_weight')   
            item_details['calculation_type']=request.data.get('calculation_type')   
            item_details['huid_rate']=request.data.get('huid_rate')
            item_details['created_at']=timezone.now()
            item_details['created_by']=request.user.id
            item_details['modified_at']=timezone.now()
            item_details['modified_by']=request.user.id

            item_serializer=ItemSerializer(item_queryset,data=item_details,partial=True)

            if item_serializer.is_valid():
                item_serializer.save()
                item_dict=item_serializer.data
                response_data['item_details']=item_dict

                calculation_details={}
                calculation_details['modified_at']=timezone.now()
                calculation_details['modified_by']=request.user.id

                if str(item_dict['calculation_type'])==str(item_calculation_type):

                    if str(item_dict['calculation_type'])==settings.FIXEDRATE:
                        calculation_details['fixed_rate']=request.data.get('fixed_rate')
                        try:
                            fixed_queryset=FixedRate.objects.get(item_details=pk)
                        except Exception as err:
                            pass

                        fixed_serializer=FixedRateSerializer(fixed_queryset,data=calculation_details,partial=True)
                        if fixed_serializer.is_valid():
                            fixed_serializer.save()
                            response_data['Calculation_details']=fixed_serializer.data
                        else:
                            raise Exception(fixed_serializer.errors)
                        
                    elif str(item_dict['calculation_type']) == settings.PERGRAMRATE:
                        calculation_details['per_gram_rate']=request.data.get('per_gram_rate')
                        try:
                            per_gram_queryset=PerGramRate.objects.get(item_details=pk)
                        except Exception as err:
                            pass

                        per_gram_serializer=PerGramRateSerializer(per_gram_queryset,data=calculation_details,partial=True)
                        if per_gram_serializer.is_valid():
                            per_gram_serializer.save()
                            response_data['Calculation_details']=per_gram_serializer.data
                        else:
                            raise Exception(per_gram_serializer.errors)
                        
                    elif str(item_dict['calculation_type']) == settings.PERPIECERATE:
                        calculation_details['per_piece_rate']=request.data.get('per_piece_rate')
                        calculation_details['min_per_piece_rate']=request.data.get('min_per_piece_rate')
                        try:
                            per_piece_queryset=PerPiece.objects.get(item_details=pk)
                        except Exception as err:
                            pass

                        per_piece_serializer=PerPieceSerializer(per_piece_queryset,data=calculation_details,partial=True)
                        if per_piece_serializer.is_valid():
                            per_piece_serializer.save()
                            response_data['Calculation_details']=per_piece_serializer.data
                        else:
                            raise Exception(per_piece_serializer.errors)
                        
                    else:
                        try:
                            weight_queryset=WeightCalculation.objects.get(item_details=pk)
                        except Exception as err:
                            pass

                        calculation_details['wastage_calculation']=request.data.get('wastage_calculation')
                        calculation_details['wastage_percent']=request.data.get('wastage_percent')
                        calculation_details['flat_wastage']=request.data.get('flat_wastage')
                        calculation_details['making_charge_calculation']=request.data.get('making_charge_calculation')
                        calculation_details['making_charge_gram']=request.data.get('making_charge_gram')
                        calculation_details['flat_making_charge']=request.data.get('flat_making_charge')

                        weight_serializer=WeightCalculationSerializer(weight_queryset,data=calculation_details,partial=True)
                        if weight_serializer.is_valid():
                            weight_serializer.save()
                            response_data['Calculation_details']=weight_serializer.data

                        else:
                            raise Exception(weight_serializer.errors)
                else:

                    if str(item_dict['calculation_type'])==settings.FIXEDRATE:

                        calculation_details['fixed_rate']=request.data.get('fixed_rate')
                        calculation_details['item_details']=pk
                        calculation_details['created_at']=timezone.now()
                        calculation_details['created_by']=request.user.id
                        fixed_rate_serializer=FixedRateSerializer(data=calculation_details)

                        if fixed_rate_serializer.is_valid():
                            fixed_rate_serializer.save()
                            response_data['Calculation_details']=fixed_rate_serializer.data
                            if str(item_calculation_type) == settings.WEIGHTCALCULATION:
                                try:
                                    weight_calculation_queryset=WeightCalculation.objects.get(item_details=pk)
                                    weight_calculation_queryset.delete()
                                except Exception as err:
                                    pass

                            elif str(item_calculation_type) == settings.PERGRAMRATE:
                                try:
                                    per_gram_rate_queryset=PerGramRate.objects.get(item_details=pk)
                                    per_gram_rate_queryset.delete()
                                except Exception as err:
                                    pass

                            elif str(item_calculation_type) == settings.PERPIECERATE:
                                try:
                                    per_piece_queryset=PerPiece.objects.get(item_details=pk)
                                    per_piece_queryset.delete()
                                except Exception as err:
                                    pass
                        else:
                            raise Exception(fixed_rate_serializer.errors)
                    
                    elif str(item_dict['calculation_type'])==settings.PERGRAMRATE:

                        calculation_details['per_gram_rate']=request.data.get('per_gram_rate')
                        calculation_details['item_details']=pk
                        calculation_details['created_at']=timezone.now()
                        calculation_details['created_by']=request.user.id

                        per_gram_rate_serializer=PerGramRateSerializer(data=calculation_details)

                        if per_gram_rate_serializer.is_valid():
                            per_gram_rate_serializer.save()
                            response_data['Calculation_details']=per_gram_rate_serializer.data

                            if str(item_calculation_type) == settings.WEIGHTCALCULATION:

                                try:
                                    weight_calculation_queryset=WeightCalculation.objects.get(item_details=pk)
                                    weight_calculation_queryset.delete()
                                except Exception as err:
                                    pass

                            elif str(item_calculation_type) == settings.FIXEDRATE:

                                try:
                                    fixed_rate_queryset=FixedRate.objects.get(item_details=pk)
                                    fixed_rate_queryset.delete()
                                except Exception as err:
                                    pass

                            elif str(item_calculation_type) == settings.PERPIECERATE:

                                try:
                                    per_piece_queryset=PerPiece.objects.get(item_details=pk)
                                    per_piece_queryset.delete()
                                except Exception as err:
                                    pass
                        
                        else:
                            raise Exception(per_gram_rate_serializer.errors)
                        
                    elif str(item_dict['calculation_type'])==settings.PERPIECERATE:

                        calculation_details['min_per_piece_rate']=request.data.get('min_per_piece_rate')
                        calculation_details['per_piece_rate']=request.data.get('per_piece_rate')
                        calculation_details['item_details']=pk
                        calculation_details['created_at']=timezone.now()
                        calculation_details['created_by']=request.user.id

                        per_piece_serializer=PerPieceSerializer(data=calculation_details)

                        if per_piece_serializer.is_valid():
                            per_piece_serializer.save()
                            response_data['Calculation_details']=per_piece_serializer.data

                            if str(item_calculation_type) == settings.WEIGHTCALCULATION:

                                try:
                                    weight_calculation_queryset=WeightCalculation.objects.get(item_details=pk)
                                    weight_calculation_queryset.delete()
                                except Exception as err:
                                    pass

                            elif str(item_calculation_type) == settings.FIXEDRATE:

                                try:
                                    fixed_rate_queryset=FixedRate.objects.get(item_details=pk)
                                    fixed_rate_queryset.delete()
                                except Exception as err:
                                    pass

                            elif str(item_calculation_type) == settings.PERGRAMRATE:

                                try:
                                    per_gram_rate_queryset=PerGramRate.objects.get(item_details=pk)
                                    per_gram_rate_queryset.delete()
                                except Exception as err:
                                    pass
                        
                        else:
                            raise Exception(per_piece_serializer.errors)
                        
                    elif str(item_dict['calculation_type'])==settings.WEIGHTCALCULATION:
                        calculation_details['wastage_calculation']=request.data.get('wastage_calculation')
                        calculation_details['wastage_percent']=request.data.get('wastage_percent')
                        calculation_details['flat_wastage']=request.data.get('flat_wastage')
                        calculation_details['making_charge_calculation']=request.data.get('making_charge_calculation')
                        calculation_details['making_charge_gram']=request.data.get('making_charge_gram')
                        calculation_details['flat_making_charge']=request.data.get('flat_making_charge')
                        calculation_details['item_details']=pk
                        calculation_details['created_at']=timezone.now()
                        calculation_details['created_by']=request.user.id

                        weight_calculation_serializer=WeightCalculationSerializer(data=calculation_details)
                        if weight_calculation_serializer.is_valid():
                            weight_calculation_serializer.save()
                            response_data['Calculation_details']=weight_calculation_serializer.data

                            if str(item_calculation_type) == settings.FIXEDRATE: 
                                try:
                                    fixed_rate_queryset=FixedRate.objects.get(item_details=pk)
                                    fixed_rate_queryset.delete()
                                except Exception as err:
                                    pass

                            elif str(item_calculation_type) == settings.PERGRAMRATE:
                                try:
                                    per_gram_rate_queryset=PerGramRate.objects.get(item_details=pk)
                                    per_gram_rate_queryset.delete()
                                except Exception as err:
                                    pass

                            elif str(item_calculation_type) == settings.PERPIECERATE:
                                try:
                                    per_piece_queryset=PerPiece.objects.get(item_details=pk)
                                    per_piece_queryset.delete()
                                except Exception as err:
                                    pass
                        else:
                            raise Exception(weight_calculation_serializer.errors)
                        
                return Response(
                    {
                        "data":response_data,
                        "message":res_msg.update("Item Details"),
                        "status":status.HTTP_200_OK
                    },status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        "data":item_serializer.errors,
                        "message":res_msg.something_else(),
                        "status":status.HTTP_400_BAD_REQUEST
                    },status=status.HTTP_200_OK
                )
        except Item.DoesNotExist:
            return Response(
                {
                    "message":res_msg.not_exists("Item Details"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        except Exception as err:
            for key, value in original_item_state.items():
                setattr(item_queryset, key, value)
            item_queryset.save()
            transaction.set_rollback(True)
            return Response(
                {
                    "data":str(err),
                    "message":res_msg.something_else(),
                    "status":status.HTTP_400_BAD_REQUEST
                },status=status.HTTP_200_OK
            )
    
    def delete(self,request,pk):
        try:
            item_queryset=Item.objects.get(id=pk)
            item_queryset.delete()

            return Response(
                {
                    "message":res_msg.delete("Item Details"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        except Item.DoesNotExist:
            return Response(
                {
                    "message":res_msg.not_exists("Item Details"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        except ProtectedError:
            return Response(
                {
                    "message":res_msg.related_item("Delete"),
                    "status":status.HTTP_400_BAD_REQUEST
                },status=status.HTTP_200_OK
            )
        except Exception as err:

            return Response(
                {
                    "message":res_msg.something_else(),
                    "status":status.HTTP_400_BAD_REQUEST
                },status=status.HTTP_200_OK
            )
        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ItemStatusView(APIView):
    def get(self,request,pk):

        try:

            queryset=Item.objects.get(id=pk)

            subitem_queryset=SubItem.objects.filter(item_details=pk)

            for data in subitem_queryset:
                data.is_active=not(queryset.is_active)
                data.save()

            queryset.is_active=not(queryset.is_active)
            queryset.save()

            serializer=ItemSerializer(queryset)

            return Response(
                {
                    "data":serializer.data,
                    "message":res_msg.change("Item Detail Status"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        except Item.DoesNotExist:
            return Response(
                {
                    "message":res_msg.not_exists("Item Details"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        except Exception as err:
            return Response(
                {
                    "message":res_msg.something_else(),
                    "status":status.HTTP_400_BAD_REQUEST
                },status=status.HTTP_200_OK
            )
        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ItemListView(APIView):

    def get(self,request):

        queryset=Item.objects.filter(is_active=True).values('huid_rate','id','item_id','item_name','hsn_code','stock_type','stock_type__stock_type_name')

        return Response(
            {
                "data":{
                    "list":queryset
                },
                "message":res_msg.retrieve("Item Details"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
    
    def post(self,request):

        response_data=[]

        search = request.data.get('search') if request.data.get('search') else ''
        active_status = request.data.get('active_status')
        from_date = request.data.get('from_date') if request.data.get('from_date') else None
        to_date = request.data.get('to_date') if request.data.get('to_date') else None
        page = request.data.get('page') if request.data.get('page') else 1
        try:
            items_per_page = int(request.data.get('items_per_page', Item.objects.all().count()))
            if items_per_page == 0:
                items_per_page = 10 
        except Exception as err:
            items_per_page = 10 

        filter_dict={}
        combined_conditions = Q()
        if search != "":
            or_conditions = []
            or_conditions.append(Q(item_name__icontains=search))
            or_conditions.append(Q(item_counter__counter_name__icontains=search))
            or_conditions.append(Q(metal__metal_name__icontains=search))
            or_conditions.append(Q(calculation_type__calculation_name__icontains=search))
            
            for condition in or_conditions:
                combined_conditions |= condition
            
        if active_status != None:
            filter_dict['is_active'] = active_status

        if from_date != None and to_date != None :
            date_range=(from_date,to_date)
            filter_dict['created_at__range'] = date_range

        if len(filter_dict) != 0 :
            queryset=list(Item.objects.filter(combined_conditions, **filter_dict).order_by('id'))
        
        else:
            queryset=list(Item.objects.filter(combined_conditions).order_by('id'))

        paginated_data = Paginator(queryset, items_per_page)
        serializer = ItemSerializer(paginated_data.get_page(page), many=True)

        for item in serializer.data:
            try:
                staff = Staff.objects.get(user = item['created_by'])
                username = staff.first_name
            except Exception as err:
                username = "---"
            res_data={}
            
            counter = Counter.objects.get(id = item['item_counter'])
            if counter:
                counter_name = counter.counter_name
            else:
                counter_name = None

            metal = Metal.objects.get(id = item['metal'])
            if metal:
                metal_name = metal.metal_name
            else:
                metal_name = None

            calculation = CalculationType.objects.get(id = item['calculation_type'])
            if calculation:
                calculation_type_name = calculation.calculation_name
            else:
                calculation_type_name = None
            
            res_data['id']=item['id']
            res_data['item_id']=item['item_id']
            res_data['item_counter']=counter_name
            res_data['item_name']=item['item_name']
            res_data['metal']=metal_name
            res_data['huid_rate']=item['huid_rate'] 
            res_data['calculation_type']=calculation_type_name
            res_data['is_active']=item['is_active']
            res_data['created_by']=username
            res_data['created_at']=item['created_at']
           
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
                "message":res_msg.retrieve("Item Details"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ItemByMetalStock(APIView):
    def post(self,request):

        metal=request.data.get('metal')
        stock_type=request.data.get('stock_type')
        calculation_type=request.data.get('calculation_type')

        filter_condition={}

        if metal != None:
            filter_condition['metal']=metal

        if stock_type != None:
            filter_condition['stock_type']=stock_type

        if calculation_type != None:
            filter_condition['calculation_type']=calculation_type

        if len(filter_condition) != 0 :

            queryset=list(Item.objects.filter(**filter_condition).values('id','item_id','item_name'))
        
        else:
            queryset=list(Item.objects.all().values('id','item_id','item_name'))

        return Response(
            {
                "data":{
                    "list":queryset
                },
                "message":res_msg.retrieve("Item List"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ItemByMetal(APIView):

    def post(sel,request):

        metal=request.data.get('metal')
        purity=request.data.get('purity')

        filter_condition={}

        if metal != None:
            filter_condition['metal'] = metal
        
        if purity != None :
            filter_condition['purity'] = purity

        if len(filter_condition) != 0 :

            queryset=list(Item.objects.filter(**filter_condition).values('huid_rate','id','item_id','item_name','hsn_code','stock_type','stock_type__stock_type_name','item_counter'))

        else:
            
            queryset=list(Item.objects.all().values('huid_rate','id','item_id','item_name','hsn_code','stock_type','stock_type__stock_type_name','item_counter'))    

        return Response(
            {
                "data":{
                    "list":queryset
                },
                "message":res_msg.retrieve("Item Details"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class SubItemImageUpload(APIView):
 
    def post(self, request):
        request_file = request.FILES['image'] if 'image' in request.FILES else None
        if request_file:
            fs = FileSystemStorage()
            file_name = str(uuid.uuid1()) + str(request_file.name).replace(' ','-')
            file = fs.save(file_name, request_file)
            # the fileurl variable now contains the url to the file. This can be used to serve the file when needed.
            fileurl = fs.url(file)
 
            return Response({
                "sub_item_image_url": fileurl,
                "message": 'SubItem Image uploaded',
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        return Response({
                "message": res_msg.something_else(),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
    
    def put(self, request, file):
        request_file = request.FILES['image'] if 'image' in request.FILES else None
        if request_file:
            fs = FileSystemStorage()
            file_name = file
            fs.delete(file)
            file = fs.save(file_name, request_file)
            # the fileurl variable now contains the url to the file. This can be used to serve the file when needed.
            fileurl = fs.url(file)
 
            return Response({
                "sub_item_image_url": fileurl,
                "message": 'SubItem Image uploaded',
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        return Response({
                "message": res_msg.something_else(),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class SubItemIdview(APIView):
    def get(self,reuquest):
        try:
            queryset=SubItemID.objects.all().order_by('-id')
            if len(queryset) == 0:
                return Response(
                    {
                        "sub_item_id":1,
                        "message":res_msg.retrieve("Item ID"),
                        "status":status.HTTP_200_OK
                    },status=status.HTTP_200_OK
                )
            else:
                new_id=int(queryset[0].pk)+1
                return Response(
                    {
                        "sub_item_id":new_id,
                        "message":res_msg.retrieve("Item ID"),
                        "status":status.HTTP_200_OK
                    },status=status.HTTP_200_OK
                )
        except Exception as err:
            return Response(
                {
                    "sub_item_id":"1",
                    "message":res_msg.retrieve("Item ID"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )

def delete_subitem(pk):

    try:

        queryset=SubItem.objects.get(id=pk)
        queryset.delete()

    except Exception as err:
        pass

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class SubItemViewset(viewsets.ViewSet):
    @transaction.atomic
    def create(self,request):

        response_data={}
        
        try:
            subitem_details={}
            subitem_details['metal']=request.data.get('metal')
            subitem_details['purity']=request.data.get('purity')
            subitem_details['item_details']=request.data.get('item_details')
            subitem_details['sub_item_id']=request.data.get('sub_item_id')
            subitem_details['subitem_hsn_code']=request.data.get('subitem_hsn_code')
            subitem_details['sub_item_name']=request.data.get('sub_item_name')
            subitem_details['allow_zero_weight']=request.data.get('allow_zero_weight')
            subitem_details['measurement_type']=request.data.get('measurement_type')
            subitem_details['sub_item_counter']=request.data.get('sub_item_counter')
            subitem_details['calculation_type']=request.data.get('calculation_type')
            subitem_details['sub_item_image']=request.data.get('sub_item_image')
            subitem_details['created_at']=timezone.now()
            subitem_details['created_by']=request.user.id
            
            item_queryset=Item.objects.get(id=subitem_details['item_details'])
            subitem_details['stock_type']=item_queryset.stock_type.pk
            
            subitem_serailizer=SubItemSerializer(data=subitem_details)
            
            if subitem_serailizer.is_valid():
                subitem_serailizer.save()
                subitem_dict=subitem_serailizer.data
                response_data['subitem_details']=subitem_serailizer.data
                sub_item_id_dict={}
                sub_item_id_dict['sub_item_id']=subitem_dict['sub_item_id']
                sub_item_id_serializer=SubItemIDSerializer(data=sub_item_id_dict)

                if sub_item_id_serializer.is_valid():
                    sub_item_id_serializer.save()
                    
                calculation_details={}

                calculation_details['sub_item_details']=subitem_dict['id']
                calculation_details['created_at']=timezone.now()
                calculation_details['created_by']=request.user.id

                if str(subitem_details['calculation_type'])==settings.FIXEDRATE:  

                    calculation_details['fixed_rate']=request.data.get('fixed_rate')

                    fixed_serailizer=SubItemFixedRateSerializer(data=calculation_details)

                    if fixed_serailizer.is_valid():
                        fixed_serailizer.save()
                        response_data['calculation_details']=fixed_serailizer.data
                    
                    else:
                        # delete_subitem(pk=subitem_serailizer.data)
                        raise Exception(fixed_serailizer.errors)
                        return Response(
                            {
                                "data":fixed_serailizer.errors,
                                "message":res_msg.something_else(),
                                "status":status.HTTP_400_BAD_REQUEST
                            },status=status.HTTP_200_OK
                        )

                elif str(subitem_details['calculation_type'])==settings.PERGRAMRATE:
                    calculation_details['per_gram_rate']=request.data.get('per_gram_rate')
                    pergram_serializer=SubItemPerGramRateSerializer(data=calculation_details)
                    if pergram_serializer.is_valid():
                        pergram_serializer.save()
                        response_data['calculation_details']=pergram_serializer.data
                    else:
                        # delete_subitem(pk=subitem_serailizer.data)
                        raise Exception(fixed_serailizer.errors)
                        return Response(
                            {
                                "data":pergram_serializer.errors,
                                "message":res_msg.something_else(),
                                "status":status.HTTP_400_BAD_REQUEST
                            },status=status.HTTP_200_OK
                        )
                    
                elif str(subitem_details['calculation_type']) == settings.PERPIECERATE:

                    calculation_details['min_per_piece_rate']=request.data.get('min_per_piece_rate')
                    calculation_details['per_piece_rate']=request.data.get('per_piece_rate')
                    per_piece_serializer=SubItemPerPieceSerializer(data=calculation_details)

                    if per_piece_serializer.is_valid():
                        per_piece_serializer.save()
                        response_data['calculation_details']=per_piece_serializer.data

                        return Response(
                            {
                                "data":response_data,
                                "message":res_msg.create("Item"),
                                "status":status.HTTP_201_CREATED
                            },status=status.HTTP_200_OK
                        )
                    else:
                        raise Exception(per_piece_serializer.errors)
                else:

                    calculation_details['wastage_calculation']=request.data.get('wastage_calculation')
                    calculation_details['wastage_percent']=request.data.get('wastage_percent')
                    calculation_details['flat_wastage']=request.data.get('flat_wastage')
                    calculation_details['making_charge_calculation']=request.data.get('making_charge_calculation')
                    calculation_details['making_charge_gram']=request.data.get('making_charge_gram')
                    calculation_details['flat_making_charge']=request.data.get('flat_making_charge')
                    
                    weight_serializer=SubItemWeightCalculationSerializer(data=calculation_details)

                    if weight_serializer.is_valid():
                        weight_serializer.save()
                        response_data['calculation_details']=weight_serializer.data

                    else:
                        # delete_subitem(pk=subitem_serailizer.data)
                        raise Exception(weight_serializer.errors)
                        return Response(
                            {
                                "data":weight_serializer.errors,
                                "message":res_msg.something_else(),
                                "status":status.HTTP_400_BAD_REQUEST
                            },status=status.HTTP_200_OK
                        )
                return Response(
                    {
                        "data":response_data,
                        "message":res_msg.create("Sub Item Details"),
                        "status":status.HTTP_201_CREATED
                    },status=status.HTTP_200_OK
                )

            else:
                return Response(
                    {
                        "data":subitem_serailizer.errors,
                        "message":res_msg.something_else(),
                        "status":status.HTTP_400_BAD_REQUEST
                    },status=status.HTTP_200_OK
                )
        except Exception as err:
            transaction.set_rollback(True)
            return Response(
                {
                    "data" : str(err),
                    "message":res_msg.something_else(),
                    "status":status.HTTP_204_NO_CONTENT
                },status=status.HTTP_200_OK
            )
        
    def retrieve(self,request,pk):
        response_data={}
        try:
 
            subitem_queryset=SubItem.objects.get(id=pk)
            subitem_dict={
                "id":subitem_queryset.pk,
                "metal": subitem_queryset.metal.pk,
                "metal_name":subitem_queryset.metal.metal_name,
                "purity": subitem_queryset.purity.pk,
                "purity_name":subitem_queryset.purity.purity_name,
                "item_name":subitem_queryset.item_details.item_name,
                "item_id":subitem_queryset.item_details.item_id,               
                "item_details": {
                    "huid_rate":subitem_queryset.item_details.huid_rate,
                    "id": subitem_queryset.item_details.pk,
                    "item_id":subitem_queryset.item_details.item_id,
                    "item_name":subitem_queryset.item_details.item_name,
                    "hsn_code":subitem_queryset.item_details.hsn_code,
                    "stock_type":subitem_queryset.stock_type.pk,
                    "stock_type__stock_type_name":subitem_queryset.stock_type.stock_type_name,
                },
                "sub_item_id":subitem_queryset.sub_item_id,
                "subitem_hsn_code":subitem_queryset.subitem_hsn_code,
                "sub_item_name":subitem_queryset.sub_item_name,
                "allow_zero_weight":subitem_queryset.allow_zero_weight,
                "sub_item_counter":subitem_queryset.sub_item_counter.pk,
                "sub_item_counter_name":subitem_queryset.sub_item_counter.counter_name,
                "sub_item_counter_name":subitem_queryset.sub_item_counter.counter_name,
                "sub_item_image":settings.IMAGE_URL+str(subitem_queryset.sub_item_image) if str(subitem_queryset.sub_item_image) else '',
                "allow_zero_weight": subitem_queryset.allow_zero_weight,
                "measurement_type":subitem_queryset.measurement_type.pk,
                "measurement_type_name":subitem_queryset.measurement_type.measurement_name,
                "calculation_type":subitem_queryset.calculation_type.pk,
                "calculation_type_name":subitem_queryset.calculation_type.calculation_name,
                "is_active":subitem_queryset.is_active
            }
            response_data['subitem_details']=subitem_dict
 
            if str(subitem_dict['calculation_type'])==settings.FIXEDRATE:
 
                fixed_queryset=SubItemFixedRate.objects.get(sub_item_details=pk)
                fixed_serializer=SubItemFixedRateSerializer(fixed_queryset)
                response_data['calculation_details']=fixed_serializer.data

            elif str(subitem_dict['calculation_type'])==settings.PERGRAMRATE:

                per_gram_retrive=SubItemPerGramRate.objects.get(sub_item_details=pk)
                per_gram_retrive_serializer=SubItemPerGramRateSerializer(per_gram_retrive)
                response_data['calculation_details']=per_gram_retrive_serializer.data
                
            elif str(subitem_dict['calculation_type']) == settings.PERPIECERATE:
                per_piece_retrive=SubItemPerPiece.objects.get(sub_item_details=pk)
                per_piece_retrive_serializer=SubItemPerPieceSerializer(per_piece_retrive)
                response_data['calculation_details']=per_piece_retrive_serializer.data
            else:
 
                weight_queryset=SubItemWeightCalculation.objects.get(sub_item_details=pk)
                weight_serializer=SubItemWeightCalculationSerializer(weight_queryset)
                response_data['calculation_details']=weight_serializer.data
                response_data['calculation_details']['wastage_calculation_name']=weight_queryset.wastage_calculation.weight_name
                response_data['calculation_details']['making_charge_calculation_name']=weight_queryset.making_charge_calculation.weight_name
 
            return Response(
                {
                    "data":response_data,
                    "message":res_msg.retrieve("Sub Item Details"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
 
        except SubItem.DoesNotExist:
            
            return Response(
                {
                    "message":res_msg.not_exists("Sub Item Details"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        except Exception as err:
            
            return Response(
                {
                    "message":res_msg.something_else(),
                    "status":status.HTTP_400_BAD_REQUEST
                },status=status.HTTP_200_OK
            )
    
    @transaction.atomic
    def update(self,request,pk):
        try:
            # with transaction.atomic():
            response_data={}

            subitem_queryset=SubItem.objects.get(id=pk)
            original_subitem_state = subitem_queryset.__dict__.copy()

            subitem_calculation_type=str(subitem_queryset.calculation_type.pk)

            subitem_details={}
            subitem_details['metal']=request.data.get('metal')
            subitem_details['purity']=request.data.get('purity')
            subitem_details['item_details']=request.data.get('item_details')
            subitem_details['stock_type']=request.data.get('stock_type')
            subitem_details['sub_item_id']=request.data.get('sub_item_id')
            subitem_details['subitem_hsn_code']=request.data.get('subitem_hsn_code')
            subitem_details['sub_item_name']=request.data.get('sub_item_name')
            subitem_details['allow_zero_weight']=request.data.get('allow_zero_weight')
            subitem_details['measurement_type']=request.data.get('measurement_type')
            subitem_details['measurement_value']=request.data.get('measurement_value')
            subitem_details['sub_item_counter']=request.data.get('sub_item_counter')
            subitem_details['calculation_type']=request.data.get('calculation_type')
            subitem_details['sub_item_image']=request.data.get('sub_item_image')
            subitem_details['modified_at']=timezone.now()
            subitem_details['modified_by']=request.user.id

            item_queryset=Item.objects.get(id=subitem_details['item_details'])

            subitem_details['stock_type']=item_queryset.stock_type.pk

            subitem_serializer=SubItemSerializer(subitem_queryset,data=subitem_details,partial=True)
            
            if subitem_serializer.is_valid():
                subitem_serializer.save()

                subitem_dict=subitem_serializer.data
                response_data['subitem_details']=subitem_serializer.data

                calculation_details={}
                calculation_details['modified_at']=timezone.now()
                calculation_details['modified_by']=request.user.id

                if str(subitem_dict['calculation_type'])==subitem_calculation_type:

                    if str(subitem_dict['calculation_type'])==settings.FIXEDRATE:

                        calculation_details['fixed_rate']=request.data.get('fixed_rate')

                        try:

                            fixedrate_queryset=SubItemFixedRate.objects.get(sub_item_details=pk)

                        except Exception as err:
                            pass

                        fixedrate_serializer=SubItemFixedRateSerializer(fixedrate_queryset,data=calculation_details,partial=True)

                        if fixedrate_serializer.is_valid():
                            fixedrate_serializer.save()
                            response_data['calculation_details']=fixedrate_serializer.data

                        else:
                            raise Exception(fixedrate_serializer.errors)
                        
                    elif str(subitem_dict['calculation_type'])==settings.PERGRAMRATE :

                        calculation_details['per_gram_rate']=request.data.get('per_gram_rate')
                        calculation_details['sub_item_details']=pk
                        calculation_details['created_at']=timezone.now()
                        calculation_details['created_by']=request.user.id

                        try:

                            pergram_queryset=SubItemPerGramRate.objects.get(sub_item_details=pk)
                        
                        except Exception as err:
                            pass

                        pergram_serializer=SubItemPerGramRateSerializer(pergram_queryset,data=calculation_details,partial=True)

                        if pergram_serializer.is_valid():
                            pergram_serializer.save()
                            response_data['calculation_details']=pergram_serializer.data

                        else:
                            raise Exception(pergram_serializer.errors)
                        
                    elif str(subitem_dict['calculation_type'])==settings.PERPIECERATE :

                        calculation_details['per_piece_rate']=request.data.get('per_piece_rate')
                        calculation_details['min_per_piece_rate']=request.data.get('min_per_piece_rate')
                        calculation_details['sub_item_details']=pk
                        calculation_details['created_at']=timezone.now()
                        calculation_details['created_by']=request.user.id

                        try:

                            perpiece_queryset=SubItemPerPiece.objects.get(sub_item_details=pk)
                        
                        except Exception as err:
                            pass

                        perpiece_serializer=SubItemPerPieceSerializer(perpiece_queryset,data=calculation_details,partial=True)

                        if perpiece_serializer.is_valid():
                            perpiece_serializer.save()
                            response_data['calculation_details']=perpiece_serializer.data

                        else:
                            raise Exception(perpiece_serializer.errors)
                        
                    else:

                        calculation_details['wastage_calculation']=request.data.get('wastage_calculation')
                        calculation_details['wastage_percent']=request.data.get('wastage_percent')
                        calculation_details['flat_wastage']=request.data.get('flat_wastage')
                        calculation_details['making_charge_calculation']=request.data.get('making_charge_calculation')
                        calculation_details['making_charge_gram']=request.data.get('making_charge_gram')
                        calculation_details['flat_making_charge']=request.data.get('flat_making_charge')

                        try:

                            weightcalculation_queryset=SubItemWeightCalculation.objects.get(sub_item_details=pk)

                        except Exception as err:
                            pass

                        weightcalculation_serializer=SubItemWeightCalculationSerializer(weightcalculation_queryset,data=calculation_details,partial=True)

                        if weightcalculation_serializer.is_valid():

                            weightcalculation_serializer.save()
                            response_data['calculation_details']=weightcalculation_serializer.data

                        else:
                            raise Exception(weightcalculation_serializer.errors)
                        
                else:

                    if str(subitem_dict["calculation_type"])==settings.FIXEDRATE:

                        calculation_details['fixed_rate']=request.data.get('fixed_rate')
                        calculation_details['sub_item_details']=pk
                        calculation_details['created_at']=timezone.now()
                        calculation_details['created_by']=request.user.id

                        fixed_serializer=SubItemFixedRateSerializer(data=calculation_details)

                        if fixed_serializer.is_valid():
                            fixed_serializer.save()
                            response_data['calculation_details']=fixed_serializer.data

                            if str(subitem_calculation_type) == settings.WEIGHTCALCULATION:

                                try:
                                    weight_queryset=SubItemWeightCalculation.objects.get(sub_item_details=pk)
                                    weight_queryset.delete()
                                except Exception as err:
                                    pass

                            if str(subitem_calculation_type) == settings.PERGRAMRATE:
                            
                                try:
                                    pergram_delete=SubItemPerGramRate.objects.get(sub_item_details=pk)
                                    pergram_delete.delete()

                                except Exception as err:
                                    pass

                            if str(subitem_calculation_type) == settings.PERPIECERATE:
                            
                                try:
                                    perpiece_delete=SubItemPerPiece.objects.get(sub_item_details=pk)
                                    perpiece_delete.delete()

                                except Exception as err:
                                    pass

                        else:
                            raise Exception(fixed_serializer.errors) 
                        
                    elif str(subitem_dict["calculation_type"])==settings.PERGRAMRATE:

                        calculation_details['per_gram_rate']=request.data.get('per_gram_rate')
                        calculation_details['sub_item_details']=pk
                        calculation_details['created_at']=timezone.now()
                        calculation_details['created_by']=request.user.id

                        Pergram_new_serializer=SubItemPerGramRateSerializer(data=calculation_details)

                        if Pergram_new_serializer.is_valid():
                            Pergram_new_serializer.save()
                            response_data['calculation_details']=Pergram_new_serializer.data

                            if str(subitem_calculation_type) == settings.WEIGHTCALCULATION:

                                try:
                                    weight_queryset=SubItemWeightCalculation.objects.get(sub_item_details=pk)
                                    weight_queryset.delete()
                                except Exception as err:
                                    pass

                            if str(subitem_queryset.calculation_type.pk) == settings.FIXEDRATE:
                                
                                try:
                                    fixed_delete_queryset=SubItemFixedRate.objects.get(sub_item_details=pk)
                                    fixed_delete_queryset.delete()
                                except Exception as err:
                                    pass
                            if str(subitem_calculation_type) == settings.PERPIECERATE:
                            
                                try:
                                    perpiece_delete=SubItemPerPiece.objects.get(sub_item_details=pk)
                                    perpiece_delete.delete()

                                except Exception as err:
                                    pass
                        else:
                            raise Exception(Pergram_new_serializer.errors) 

                    elif str(subitem_dict["calculation_type"])==settings.PERPIECERATE:

                        calculation_details['per_piece_rate']=request.data.get('per_piece_rate')
                        calculation_details['min_per_piece_rate']=request.data.get('min_per_piece_rate')
                        calculation_details['sub_item_details']=pk
                        calculation_details['created_at']=timezone.now()
                        calculation_details['created_by']=request.user.id

                        Pergram_new_serializer=SubItemPerGramRateSerializer(data=calculation_details)

                        if Pergram_new_serializer.is_valid():
                            Pergram_new_serializer.save()
                            response_data['calculation_details']=Pergram_new_serializer.data

                            if str(subitem_calculation_type) == settings.WEIGHTCALCULATION:

                                try:
                                    weight_queryset=SubItemWeightCalculation.objects.get(sub_item_details=pk)
                                    weight_queryset.delete()
                                except Exception as err:
                                    pass

                            if str(subitem_queryset.calculation_type.pk) == settings.FIXEDRATE:
                                
                                try:
                                    fixed_delete_queryset=SubItemFixedRate.objects.get(sub_item_details=pk)
                                    fixed_delete_queryset.delete()
                                except Exception as err:
                                    pass
                            if str(subitem_calculation_type) == settings.PERGRAMRATE:
                            
                                try:
                                    pergram_delete=SubItemPerGramRate.objects.get(sub_item_details=pk)
                                    pergram_delete.delete()

                                except Exception as err:
                                    pass
                        else:
                            raise Exception(Pergram_new_serializer.errors) 
                        
                    else:

                        calculation_details['wastage_calculation']=request.data.get('wastage_calculation')
                        calculation_details['wastage_percent']=request.data.get('wastage_percent')
                        calculation_details['flat_wastage']=request.data.get('flat_wastage')
                        calculation_details['making_charge_calculation']=request.data.get('making_charge_calculation')
                        calculation_details['making_charge_gram']=request.data.get('making_charge_gram')
                        calculation_details['flat_making_charge']=request.data.get('flat_making_charge')
                        calculation_details['sub_item_details']=pk
                        calculation_details['created_at']=timezone.now()
                        calculation_details['created_by']=request.user.id

                        weight_serializer=SubItemWeightCalculationSerializer(data=calculation_details)

                        if weight_serializer.is_valid():
                            weight_serializer.save()
                            response_data['calculation_details']=weight_serializer.data

                            if str(subitem_calculation_type) == settings.PERGRAMRATE:

                                try:
                                    pergram_delete=SubItemPerGramRate.objects.get(sub_item_details=pk)
                                    pergram_delete.delete()
                                except Exception as err:
                                    pass

                            if str(subitem_calculation_type) == settings.FIXEDRATE:
                                
                                try:
                                    fixed_delete_queryset=SubItemFixedRate.objects.get(sub_item_details=pk)
                                    fixed_delete_queryset.delete()
                                except Exception as err:
                                    pass

                            if str(subitem_calculation_type) == settings.PERPIECERATE:
                            
                                try:
                                    perpiece_delete=SubItemPerPiece.objects.get(sub_item_details=pk)
                                    perpiece_delete.delete()

                                except Exception as err:
                                    pass
                        else:

                            raise Exception(weight_serializer.errors) 
                        
                return Response(
                    {
                        "data":response_data,
                        "message":res_msg.update("Sub Item Details"),
                        "status":status.HTTP_200_OK
                    },status=status.HTTP_200_OK
                )
            
            else:
                return Response(
                    {
                        "data":subitem_serializer.errors,
                        "message":res_msg.something_else(),
                        "status":status.HTTP_400_BAD_REQUEST
                    },status=status.HTTP_200_OK
                )

        except SubItem.DoesNotExist:
            return Response(
                {
                    "message":res_msg.not_exists("Sub Item Details"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        except Exception as err:

            for key, value in original_subitem_state.items():
                setattr(subitem_queryset, key, value)
            subitem_queryset.save()
            transaction.set_rollback(True)
            return Response(
                {
                    "data":str(err),
                    "message":res_msg.something_else(),
                    "status":status.HTTP_204_NO_CONTENT
                },status=status.HTTP_200_OK
            )
        

    def delete(self,request,pk):

        try:

            subitem_queryset=SubItem.objects.get(id=pk)
            subitem_queryset.delete()

            return Response(
                {
                    "message":res_msg.delete("Sub Item Details"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )

        except SubItem.DoesNotExist:

            return Response(
                {
                    "message":res_msg.not_exists("Sub Item"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        
        except Exception as err:

            return Response(
                {
                    "message":res_msg.something_else(),
                    "status":status.HTTP_400_BAD_REQUEST
                },status=status.HTTP_200_OK
            )
        


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class SubItemStatusView(APIView):

    def get(self,request,pk):

        try:

            subitem_queryset=SubItem.objects.get(id=pk)

            if not(subitem_queryset.is_active)==True:

                item_queryset=Item.objects.get(id=subitem_queryset.item_details.pk)

                if item_queryset.is_active==True:

                    subitem_queryset.is_active=not(subitem_queryset.is_active)
                    subitem_queryset.save()

                    subitem_serializer=SubItemSerializer(subitem_queryset)

                    return Response(
                        {
                            "data":subitem_serializer.data,
                            "message":res_msg.change("Sub Item Status"),
                            "status":status.HTTP_200_OK
                        },status=status.HTTP_200_OK
                    )
                
                else:
                    return Response(
                        {
                            "message":"Please active the Item"+item_queryset.item_name,
                            "status":status.HTTP_200_OK
                        },status=status.HTTP_200_OK
                    )
                
            else:

                subitem_queryset.is_active=not(subitem_queryset.is_active)
                subitem_queryset.save()


                subitem_serializer=SubItemSerializer(subitem_queryset)

                return Response(
                    {
                        "data":subitem_serializer.data,
                        "message":res_msg.change("Sub Item Status"),
                        "status":status.HTTP_200_OK
                    },status=status.HTTP_200_OK
                )


            

        except SubItem.DoesNotExist:

            return Response(
                {
                    "message":res_msg.not_exists("Sub Items Details"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class SubItemByItemCalculation(APIView):

    def post(self,request):

        item_details = request.data.get('item_details')
        calculation_type = request.data.get('calculation_type')
        
        queryset=list(SubItem.objects.filter(calculation_type=calculation_type,item_details=item_details,is_active=True).values('id','sub_item_name','sub_item_id'))

        return Response(
            {
                "data":{
                    "list":queryset
                },
                "message":res_msg.retrieve("Sub Item Details"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class SubItemList(APIView):

    def get(self,request,pk=None):
 
        if pk == None:
            queryset=SubItem.objects.filter(is_active=True).order_by('id')
        else:
            queryset=SubItem.objects.filter(item_details=pk,is_active=True).order_by('id')
        response_data=[]
       
        for j in queryset:
            dict_data ={}
            dict_data['id'] = j.pk
            dict_data['sub_item_id'] = j.sub_item_id
            dict_data['subitem_hsn_code'] = j.subitem_hsn_code
            dict_data['sub_item_name'] = j.sub_item_name
            dict_data['allow_zero_weight'] = j.allow_zero_weight                            
            dict_data['metal'] = j.metal.pk
            dict_data['purity'] = j.purity.pk
            dict_data['item_details'] = j.item_details.pk
            dict_data['stock_type'] = j.stock_type.pk
            dict_data['sub_item_counter'] = j.sub_item_counter.pk
            dict_data['calculation_type'] = j.calculation_type.pk
            dict_data['measurement_type'] = j.measurement_type.pk
            
            tax = TaxDetailsAudit.objects.filter(metal = j.metal.pk).order_by('-id').first()
            purchase_tax= PurchaseTaxDetails.objects.get(tax_details = tax.tax_details)
            
            dict_data['intra'] = purchase_tax.purchase_tax_igst
            dict_data['inter'] = float(purchase_tax.purchase_tax_cgst) + float(purchase_tax.purchase_tax_sgst)

            dict_data['igst'] = purchase_tax.purchase_tax_igst
            dict_data['cgst'] = purchase_tax.purchase_tax_cgst
            dict_data['sgst'] = purchase_tax.purchase_tax_sgst

            if int(j.calculation_type.pk) == int(settings.FIXEDRATE) :
                
                fixed_rate_queryset = SubItemFixedRate.objects.get(sub_item_details=j.pk)
                dict_data['metal_rate']=fixed_rate_queryset.fixed_rate

            elif int(j.calculation_type.pk) == int(settings.WEIGHTCALCULATION) :
                
                weight_calculation_queryset = SubItemWeightCalculation.objects.get(sub_item_details=j.pk)
                dict_data['wastage_calculation']=weight_calculation_queryset.wastage_calculation.pk
                dict_data['wastage_calculation_name']=weight_calculation_queryset.wastage_calculation.weight_name
                dict_data['min_wastage_percent']=weight_calculation_queryset.wastage_percent
                dict_data['min_flat_wastage']=weight_calculation_queryset.flat_wastage
                dict_data['making_charge_calculation']=weight_calculation_queryset.making_charge_calculation.pk
                dict_data['making_charge_calculation_name']=weight_calculation_queryset.making_charge_calculation.weight_name
                dict_data['min_making_charge_gram']=weight_calculation_queryset.making_charge_gram
                dict_data['min_flat_making_charge']=weight_calculation_queryset.flat_making_charge

                try:
                    # metal_rate_queryset=MetalRate.objects.all().order_by('-id')[0]

                    # metal_purity=str(j.metal.metal_name)+'_'+str(j.purity.purity_name)

                    # metal_rate=metal_rate_queryset.rate[metal_purity]

                    # dict_data['metal_rate']=metal_rate
                    metal_rate_queryset = MetalRate.objects.filter(purity=j.purity.pk).order_by('-id')[0]

                    dict_data['metal_rate']=metal_rate_queryset['rate']

                except Exception as err:
                    
                    dict_data['metal_rate']=0

            elif int(j.calculation_type.pk) == int(settings.PERGRAMRATE) :

                per_gram_queryset = SubItemPerGramRate.objects.get(sub_item_details=j.pk)

                dict_data['metal_rate']=per_gram_queryset.per_gram_rate

            elif int(j.calculation_type.pk) == int(settings.PERPIECERATE) :

                per_piece_queryset = SubItemPerPiece.objects.get(sub_item_details=j.pk)

                dict_data['per_piece_rate']=per_piece_queryset.per_piece_rate
                dict_data['min_per_piece_rate']=per_piece_queryset.min_per_piece_rate

            response_data.append(dict_data)
           
        return Response(
            {
                "data":{
                    "list":response_data,
                },
                "message":res_msg.retrieve("Sub Item List"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
    
    def post(self,request):

        search = request.data.get('search') if request.data.get('search') else ''
        active_status = request.data.get('active_status') if request.data.get('active_status') != None else None
        from_date = request.data.get('from_date') if request.data.get('from_date') else None 
        to_date = request.data.get('to_date') if request.data.get('to_date') else None
        page = request.data.get('page') if request.data.get('page') else 1
        try:
            items_per_page = int(request.data.get('items_per_page', SubItem.objects.all().count()))
            if items_per_page == 0:
                items_per_page = 10 
        except Exception as err:
            items_per_page = 10 

        if from_date!=None and to_date!=None:
            if active_status!=None:
                queryset=SubItem.objects.filter(Q(sub_item_name__icontains=search)|Q(sub_item_counter__counter_name__icontains=search)|Q(item_details__item_name__icontains=search),is_active=active_status,created_at__range=(from_date,to_date)).order_by('id')
            else:
                queryset=SubItem.objects.filter(Q(sub_item_name__icontains=search)|Q(sub_item_counter__counter_name__icontains=search)|Q(item_details__item_name__icontains=search),created_at__range=(from_date,to_date)).order_by('id')
        else:
            if active_status!=None:
                queryset=SubItem.objects.filter(Q(sub_item_name__icontains=search)|Q(sub_item_counter__counter_name__icontains=search)|Q(item_details__item_name__icontains=search),is_active=active_status).order_by('id')
            else:
                queryset=SubItem.objects.filter(Q(sub_item_name__icontains=search)|Q(sub_item_counter__counter_name__icontains=search)|Q(item_details__item_name__icontains=search)).order_by('id')

        paginated_data = Paginator(queryset, items_per_page)
        serializer = SubItemSerializer(paginated_data.get_page(page), many=True)

        response_data=[]

        for sub_item in serializer.data:
            try:
                staff = Staff.objects.get(user = sub_item['created_by'])
                username = staff.first_name  
            except Exception as err:
                username = "---"    
            item = Item.objects.get(id =sub_item['item_details'] )
            if item :
                # item_code = item.item_code
                item_name = item.item_name
            else:
                # item_code = None
                item_name = None

            calculation = CalculationType.objects.get(id = sub_item['calculation_type'])
            if calculation:
                calculation_type_name = calculation.calculation_name
            else:
                calculation_type_name = None

            counter = Counter.objects.get(id = sub_item['sub_item_counter'])
            if counter:
                counter_name = counter.counter_name
            else:
                counter_name = None
                
            try:
                
                sub_item_queryset = SubItem.objects.get(id=sub_item['id'])
                
                metal_name = sub_item_queryset.metal.metal_name
            except:
                metal_name = "-"

            list_dict={
                "id":sub_item['id'],
                # "item_code":item_code,
                "item_name":item_name,
                "sub_item_id":sub_item['sub_item_id'],
                # "sub_item_code":sub_item['sub_item_code'],
                "sub_item_name":sub_item['sub_item_name'],
                "metal_name":metal_name,
                "calculation_type":calculation_type_name,
                "sub_item_counter":counter_name,
                "created_by":username,
                "is_active":sub_item['is_active']
            }

            response_data.append(list_dict)

        return Response(
            {
                "data":{
                    "list":response_data,
                    "total_pages": paginated_data.num_pages,
                    "current_page": page,
                    "total_items": len(queryset),
                    "current_items": len(serializer.data)
                },
                "message":res_msg.retrieve("SubItem List"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
    

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ItemByMetalStockCalc(APIView):

    def post(self,request):

        request_data = request.data

        metal=request_data.get('metal')
        stock_type=request_data.get('stock_type')
        calculation_type=request_data.get('calculation_type')

        try:

            filter_dict={}

            if metal != None :
                filter_dict['metal']=metal

            if stock_type != None :
                filter_dict['stock_type']=stock_type

            if calculation_type != None :
                filter_dict['calculation_type']=calculation_type

            if len(filter_dict) == 0:

                queryset=list(Item.objects.all().values('id','item_id','hsn_code','item_name'))

            else:

                queryset=list(Item.objects.filter(**filter_dict).values('id','item_id','hsn_code','item_name'))

            return Response(
                {
                    "data":{
                        "list":queryset
                    },
                    "message":res_msg.retrieve("Item List"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        
        except Item.DoesNotExist :

            return Response(
                {
                    "message":res_msg.not_exists("Item Details"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        
        except Exception as err:

            return Response(
                {
                    "data" : str(err),
                    "message":res_msg.something_else(),
                    "status":status.HTTP_204_NO_CONTENT
                },status=status.HTTP_200_OK
            )
        

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class SubItemByMetalStockCalc(APIView):

    def post(self,request):

        request_data = request.data

        item_details=request_data.get('item_details')
        metal=request_data.get('metal')
        stock_type=request_data.get('stock_type')
        calculation_type=request_data.get('calculation_type')

        try:

            filter_dict={}

            if metal != None :
                filter_dict['metal']=metal

            if stock_type != None :
                filter_dict['stock_type']=stock_type

            if calculation_type != None :
                filter_dict['calculation_type']=calculation_type

            if item_details != None :
                filter_dict['item_details']=item_details

            if len(filter_dict) == 0:

                queryset=list(SubItem.objects.all().values('id','sub_item_id','subitem_hsn_code','sub_item_name'))

            else:

                queryset=list(SubItem.objects.filter(**filter_dict).values('id','sub_item_id','subitem_hsn_code','sub_item_name'))

            return Response(
                {
                    "data":{
                        "list":queryset
                    },
                    "message":res_msg.retrieve("Sub Item List"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        
        except SubItem.DoesNotExist :

            return Response(
                {
                    "message":res_msg.not_exists("Sub Item Details"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        
        except Exception as err:

            return Response(
                {
                    "data" : str(err),
                    "message":res_msg.something_else(),
                    "status":status.HTTP_204_NO_CONTENT
                },status=status.HTTP_200_OK
            )


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])

class SubItemByItem(APIView):

    def post(self,request):

        request_data=request.data

        metal=request_data.get('metal')

        item_details=request_data.get('item_details')

        sub_item_queryset=list(SubItem.objects.filter(metal=metal,item_details=item_details).values('id','sub_item_id','subitem_hsn_code','sub_item_name'))
        
        return Response(
            {
                "data":{
                    "list":sub_item_queryset
                },
                "message":res_msg.retrieve("Sub Item List"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
    
    

    




        



        
        




    
    






        
    



        


        
        






                    










            

