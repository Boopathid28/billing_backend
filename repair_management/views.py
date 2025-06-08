from django.shortcuts import render
from rest_framework import status,viewsets
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from app_lib.response_messages import ResponseMessages
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes, authentication_classes
from django.utils import timezone
from django.db.models import ProtectedError
from django.db.models import Q,Sum
from django.core.paginator import Paginator
from rest_framework.generics import GenericAPIView
from rest_framework import parsers, renderers, status
from tagging.serializer import *
from accounts.models import *
from .serializer import *
from masters.models import *
from masters.serializer import *
from settings.models import *
from payment_management.serializer import *
from payment_management.models import *
import random
from django.db import transaction
from advance_payment.models import *
from advance_payment.serializer import *
from customer.serializer import *
from vendor_management.serializer import *

res_msg = ResponseMessages()

# Create your views here.
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class RepairOrderDetailsViewset(viewsets.ViewSet):
    @transaction.atomic
    def create(self,request):
        res_data = []
        try:
            request_data=request.data

            if request.user.role.is_admin == False:
                branch = request.user.branch.pk
            else:
                branch = request_data.get('branch')

            try:
                repair_queryset = RepairDetails.objects.get(repair_number = request_data.get('repair_number'))

                status_value  = settings.PENDING,
                item_data = {}
                item_data = {
                    'repair_type' : request_data.get('repair_type'),
                    'metal_details': request_data.get('metal_details'),
                    'item_details': request_data.get('item_details'),
                    'customer_charges': request_data.get('customer_charges'),
                    'vendor_charges': request_data.get('vendor_charges'),
                    'issued_gross_weight': 0 if request_data.get('issued_gross_weight') is None else float(request_data.get('issued_gross_weight')),
                    'issued_net_weight' : 0 if request_data.get('issued_net_weight') is None else float(request_data.get('issued_net_weight')),
                    'old_stone' : 0 if request_data.get('old_stone') is None else request_data.get('old_stone'),
                    'old_diamond' : 0 if request_data.get('old_diamond') is None else request_data.get('old_diamond'),
                    'order_status' : int(status_value[0]),
                    'total_pieces' : 0 if request_data.get('total_pieces') is None else request_data.get('total_pieces'),
                    'created_at' : timezone.now(),
                    'created_by' : request.user.id
                }

                repair_item_details_serializer=RepairItemDetailsSerializer(data=item_data)
                if repair_item_details_serializer.is_valid():
                    repair_item_details_serializer.save()
                else:
                    raise Exception(repair_item_details_serializer.errors)

            except RepairDetails.DoesNotExist:
                status_value  = settings.PENDING,
                
                request_data['customer_details'] = request_data.get('customer_details')
                request_data['repair_number'] = request_data.get('repair_number')
                request_data['repair_for'] = request_data.get('repair_for')
                request_data['branch'] = branch
                request_data['est_repair_delivery_date'] = request_data.get('est_repair_delivery_date')
                request_data['est_repair_delivery_days'] = request_data.get('est_repair_delivery_days')
                request_data['total_issued_weight'] = request_data.get('total_issued_weight')
                request_data['description'] = request_data.get('description')
                request_data['payment_status'] = int(settings.PAYMENT_PENDING)
                request_data['status'] = int(status_value[0])
                request_data['created_at']=timezone.now()
                request_data['created_by']=request.user.id

                repair_details_serializer=RepairDetailsSerializer(data=request_data)

                if repair_details_serializer.is_valid():
                    repair_details_serializer.save()
                    
                    repair_number_dict={}
                    repair_number_dict['repair_number']=request_data.get('repair_number')

                    repair_number_serializer=RepairOrderNumberSerializer(data=repair_number_dict)

                    if repair_number_serializer.is_valid():
                        repair_number_serializer.save()
                    
                    item_data = {}
                    item_data = {
                        'repair_order_details' : repair_details_serializer.data['id'],
                        'repair_type' : request_data.get('repair_type'),
                        'metal_details': request_data.get('metal_details'),
                        'item_details': request_data.get('item_details'),
                        'customer_charges': request_data.get('customer_charges'),
                        'vendor_charges': request_data.get('vendor_charges'),
                        'issued_gross_weight': 0 if request_data.get('issued_gross_weight') is None else float(request_data.get('issued_gross_weight')),
                        'issued_net_weight' : 0 if request_data.get('issued_net_weight') is None else float(request_data.get('issued_net_weight')),
                        'old_stone' : 0 if request_data.get('old_stone') is None else request_data.get('old_stone'),
                        'old_diamond' : 0 if request_data.get('old_diamond') is None else request_data.get('old_diamond'),
                        'order_status' : int(status_value[0]),
                        'total_pieces' : 0 if request_data.get('total_pieces') is None else request_data.get('total_pieces'),
                        'created_at' : timezone.now(),
                        'created_by' : request.user.id
                    }
                    
                    repair_item_details_serializer=RepairItemDetailsSerializer(data=item_data)
                    if repair_item_details_serializer.is_valid():
                        repair_item_details_serializer.save()
                    else:
                        raise Exception(repair_item_details_serializer.errors)
                        
                else:
                   raise Exception(repair_details_serializer.errors)
                
            return Response(
                {
                    "message":res_msg.create("Repair Order Details"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        except Exception as err:
            transaction.set_rollback(True)
            return Response(
                {
                    "data" : str(err),
                    "message":res_msg.something_else(),
                    "status":status.HTTP_400_BAD_REQUEST    
                },status=status.HTTP_200_OK
            )
        

    def retrieve(self,request,pk):
        if pk != None:
            try:
                repair_order_Details = {}
                queryset = RepairDetails.objects.get(id=pk)

                serializer = RepairDetailsSerializer(queryset)
                
                repair_order_Details = serializer.data
                # if serializer.data['repair_for'] == settings.ORDER_FOR_CUSTOMER:
                repair_order_Details['customer_name'] = queryset.customer_details.customer_name
                repair_order_Details['customer_mobile'] = queryset.customer_details.phone
                repair_order_Details['order_status'] = queryset.status.status_name
                repair_order_Details['payment_status'] = queryset.payment_status.status_name
                
                particulars = []
                try:
                    repair_item_queryset = RepairItemDetails.objects.filter(repair_order_details=pk)
                    
                    for item in repair_item_queryset:
                        item_details = {
                            'id':item.pk,
                            'repair_order_details': item.repair_order_details.pk if item.repair_order_details else None,
                            'repair_type': item.repair_type.pk if item.repair_type else None,
                            'repair_type_name': item.repair_type.repair_type_name if item.repair_type else None,
                            'item_details': item.item_details.pk if item.item_details else None,
                            'item_name': item.item_details.item_name if item.item_details else None,
                            'metal_details': item.metal_details.pk if item.metal_details else None,
                            'metal_name': item.metal_details.metal_name if item.metal_details else None,
                            'issued_gross_weight': item.issued_gross_weight,
                            'issued_net_weight': item.issued_net_weight,
                            'old_stone': item.old_stone,
                            'old_diamond': item.old_diamond,
                            'customer_charges': item.customer_charges,
                            'vendor_charges': item.vendor_charges,
                            'total_pieces': item.total_pieces,
                            'received_date': item.repair_order_details.repair_recived_date.isoformat() if item.repair_order_details and item.repair_order_details.repair_recived_date else None,
                            'is_assigned': item.is_assigned,
                            'is_received': item.is_recieved,
                            'assigned_by': item.assigned_by.email if item.assigned_by else None,
                            'order_status_name': item.order_status.status_name if item.order_status else None,
                            'order_status_color': item.order_status.color if item.order_status else None,
                            'order_status': item.order_status.pk if item.order_status else None
                        }
                        
                        try:
                            order_issue_queryset = RepairOrderIssued.objects.get(repair_item_details=pk)
                            item_details["vendor_name"] = order_issue_queryset.vendor_name.account_head_name
                        except RepairOrderIssued.DoesNotExist:
                            item_details["vendor_name"] = None
                     
                        particulars.append(item_details)
                    repair_order_Details['particular_list']=particulars

                except RepairItemDetails.DoesNotExist:
                    repair_order_Details['particular_list']=[]

                except Exception as err:
                    raise Exception(err)
                
                oldgold_data = []
                try:
                    oldgold_details = RepairOrderOldGold.objects.filter(refference_number=repair_order_Details['repair_number'])
                    
                    for oldgold in oldgold_details:
                        oldgold_details={
                            'id':oldgold.pk,
                            'refference_number':oldgold.refference_number,
                            'metal':oldgold.metal.pk,
                            'gross_weight':oldgold.gross_weight,
                            'net_weight':oldgold.net_weight,
                            'dust_weight':oldgold.dust_weight,
                            'metal_rate':oldgold.metal_rate,
                            'total_amount':oldgold.total_amount,
                            'old_rate':oldgold.old_rate,
                            'today_metal_rate':oldgold.today_metal_rate,
                            'purity':oldgold.purity,
                        }
                        
                        oldgold_data.append(oldgold_details)
                    repair_order_Details['oldgold_details']=oldgold_data
                except Exception as err:
                    raise Exception(err)
                
                payment_histroy = []
                try:
                    payment_history_queryset = list(RepairPayment.objects.filter(repair_details=queryset.pk).order_by('-id'))
                    
                    for data in payment_history_queryset:
                        payment_data = data
                       
                        payment_denomination_queryset = RepairPaymentDenominations.objects.filter(repair_payment_details=data.pk).order_by('-id')
                        for denomination in payment_denomination_queryset:
                            payment_data = {
                                'id' : denomination.pk,
                                'payment_method' : denomination.payment_method.pk,
                                'payment_method_name' : denomination.payment_method.payment_method_name,
                                'payment_provider' : denomination.payment_providers.pk if denomination.payment_providers != None else None,
                                'payment_provider_name' :denomination.payment_providers.payment_provider_name if denomination.payment_providers != None else None,
                                'total_amount' : denomination.total_amount,
                            }
                            payment_data['payment_date'] = data.payment_date
                            payment_histroy.append(payment_data)
                        
                    repair_order_Details['payment_history'] = payment_histroy
                except RepairPayment.DoesNotExist:
                    repair_order_Details['payment_history'] = []
                except Exception as err:
                    raise Exception(err)

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
                        "repair_order_Details": repair_order_Details,
                    },
                    "message" : res_msg.retrieve("Repair Order details"),
                    "status": status.HTTP_200_OK
                }, status=status.HTTP_200_OK
            )  
        else:
            return Response(
                {
                    "message" : "Invalid Repair Number",
                    "status": status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_200_OK
            )  
        

    @transaction.atomic
    def update(self,request,pk):
        request_data=request.data

        try:
            queryset = RepairDetails.objects.get(id=pk)
        except Exception as err:
            return Response({
                "message": res_msg.not_exists('Repair Order Details'),
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_200_OK)
        
        try:
            if request.user.role.is_admin == False:
                branch = request.user.branch.pk
            else:
                branch = request_data.get('branch')

            request_data['customer_details'] = request_data.get('customer_details')
            
            request_data['repair_number'] = request_data.get('repair_number')
            request_data['repair_for'] = request_data.get('repair_for')
            request_data['branch'] = branch
            request_data['est_repair_delivery_date'] = request_data.get('est_repair_delivery_date')
            request_data['est_repair_delivery_days'] = request_data.get('est_repair_delivery_days')
            request_data['total_issued_weight'] = request_data.get('total_issued_weight')
            request_data['description'] = request_data.get('description')
            request_data['modified_at']=timezone.now()
            request_data['modified_by']=request.user.id

            repair_details_serializer=RepairDetailsSerializer(queryset,data=request_data,partial=True)
            if repair_details_serializer.is_valid():
                repair_details_serializer.save() 
                return Response(
                    {
                        "message":res_msg.update("Repair Order Details"),
                        "status":status.HTTP_200_OK
                    },status=status.HTTP_200_OK
                )
            else:
                raise Exception(repair_details_serializer.errors)
            
        except Exception as err:
            transaction.set_rollback(True)
            return Response(
                {
                    "data" : str(err),
                    "message":res_msg.something_else(),
                    "status":status.HTTP_400_BAD_REQUEST    
                },status=status.HTTP_200_OK
            )
        

    def destroy(self, request, pk):
        try:
            queryset = RepairDetails.objects.get(id=pk)
            queryset.delete()
            return Response({
                "message": res_msg.delete('Repair Order Details'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        except RepairDetails.DoesNotExist:
            return Response({
                "message": res_msg.not_exists('Repair Order Details'),
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_200_OK)
        except ProtectedError:
            return Response({
                "message": res_msg.related_item('Delete'),
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({
                "message": res_msg.something_else(),
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_200_OK)
        
def DeleteRepairOrder(pk):
    try:
        queryset=RepairDetails.objects.get(id=pk)
        queryset.delete()
    except Exception as err:
        pass


##########  REPAIR ITEM UPDATE API ##########
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class RepairItemUpdateAPIView(APIView):
    # @transaction.atomic
    def put(self, request, pk):
        data = request.data
        try:
            repair_queryset = RepairDetails.objects.get(id=pk)
        except:
            return Response({
                "message": res_msg.not_exists('Repair Order'),
                "status": status.HTTP_404_NOT_FOUND
            },status=status.HTTP_200_OK)
        

        if request.user.role.is_admin == False:
            branch = request.user.branch.pk
        else:
            branch = data.get('branch')

        data['customer_details'] = data.get('customer_details')
        data['repair_number'] = data.get('repair_number')
        data['repair_for'] = data.get('repair_for')
        data['branch'] = branch
        data['est_repair_delivery_date'] = data.get('est_repair_delivery_date')
        data['est_repair_delivery_days'] = data.get('est_repair_delivery_days')
        data['total_issued_weight'] = data.get('total_issued_weight')
        data['description'] = data.get('description')
        data['modified_at']=timezone.now()
        data['modified_by']=request.user.id

        repair_details_serializer=RepairDetailsSerializer(repair_queryset,data=data,partial=True)
        if repair_details_serializer.is_valid():
            repair_details_serializer.save() 
        else:
            raise Exception(repair_details_serializer.errors)
    
        try:
            item_id = data.get('id') if data.get('id') else 0
        
            repair_item_queryset = RepairItemDetails.objects.get(id=item_id)

            item_data = {}
            item_data = {
                'repair_order_details' : pk,
                'repair_type' : data.get('repair_type'),
                'metal_details': data.get('metal_details'),
                'item_details': data.get('item_details'),
                'customer_charges': data.get('customer_charges'),
                'vendor_charges': data.get('vendor_charges'),
                'issued_gross_weight': 0 if data.get('issued_gross_weight') is None else float(data.get('issued_gross_weight')),
                'issued_net_weight' : 0 if data.get('issued_net_weight') is None else float(data.get('issued_net_weight')),
                'old_stone' : 0 if data.get('old_stone') is None else data.get('old_stone'),
                'old_diamond' : 0 if data.get('old_diamond') is None else data.get('old_diamond'),
                'total_pieces' : 0 if data.get('total_pieces') is None else data.get('total_pieces'),
                'modified_at' : timezone.now(),
                'modified_by' : request.user.id
            }
            
            repair_item_details_serializer=RepairItemDetailsSerializer(repair_item_queryset,data=item_data,partial=True)
            if repair_item_details_serializer.is_valid():
                repair_item_details_serializer.save()
                return Response({
                    "data" : repair_item_details_serializer.data,
                    "message": res_msg.update('Repair Item'),
                    "status": status.HTTP_200_OK
                },status=status.HTTP_200_OK)
            else:
                raise Exception(repair_item_details_serializer.errors)
            
        except RepairItemDetails.DoesNotExist:
            item_data = {
                'repair_order_details' : pk,
                'repair_type' : data.get('repair_type'),
                'metal_details': data.get('metal_details'),
                'item_details': data.get('item_details'),
                'customer_charges': data.get('customer_charges'),
                'vendor_charges': data.get('vendor_charges'),
                'issued_gross_weight': 0 if data.get('issued_gross_weight') is None else float(data.get('issued_gross_weight')),
                'issued_net_weight' : 0 if data.get('issued_net_weight') is None else float(data.get('issued_net_weight')),
                'old_stone' : 0 if data.get('old_stone') is None else data.get('old_stone'),
                'old_diamond' : 0 if data.get('old_diamond') is None else data.get('old_diamond'),
                'total_pieces' : 0 if data.get('total_pieces') is None else data.get('total_pieces'),
                'created_at' : timezone.now(),
                'created_by' : request.user.id
            }
            
            repair_item_details_serializer=RepairItemDetailsSerializer(data=item_data)
            if repair_item_details_serializer.is_valid():
                repair_item_details_serializer.save()
            else:
                raise Exception(repair_item_details_serializer.errors)
            
            return Response({
                "data" : repair_item_details_serializer.data,
                "message": res_msg.update('Repair Item'),
                "status": status.HTTP_200_OK
            },status=status.HTTP_200_OK)
    
        except Exception as err:
            transaction.set_rollback(True)
            return Response({
                "data" : str(err),
                "message": res_msg.not_exists('Repair Order'),
                "status": status.HTTP_404_NOT_FOUND
            },status=status.HTTP_200_OK)

    

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class RepairItemDetailsList(APIView):
    def get(self,request,pk):
        
        try:
            repair_queryset = RepairDetails.objects.get(repair_number=pk)
        except:
            return Response({
                    "message": res_msg.not_exists('Repair Order'),
                    "status": status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK)
        
        try:
            queryset = list(RepairItemDetails.objects.filter(repair_order_details=repair_queryset.pk).order_by('-id'))
        except:
            return Response({
                "message": res_msg.not_exists('Order Items'),
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_200_OK)

        res_data = []
        for i in queryset:
            order_item_data = {
                "id": i.pk,
                "repair_number": i.repair_order_details.repair_number,
                "metal": i.metal_details.pk,
                "metal_name": i.metal_details.metal_name,
                "repair_type": i.repair_type.pk,
                "repair_type_name": i.repair_type.repair_type_name,
                # "purity": i..pk,
                # "purity_name": i.purity.purity_name,
                "item": i.item_details.pk,
                "item_name": i.item_details.item_name,
                "issued_gross_weight": i.issued_gross_weight,
                "issued_net_weight": i.issued_net_weight,
                # "metal_rate": i.metal_rate,
                # "gender": i.gender.pk,
                # "gender_name": i.gender.name,
                "old_stone": i.old_stone,
                "old_diamond": i.old_diamond,
                "total_pieces": i.total_pieces,
                "customer_charges": i.customer_charges,
                "vendor_charges": i.vendor_charges,
                "is_assigned": i.is_assigned,
                "assigned_by": i.assigned_by.email if i.assigned_by else None,
                "order_status_name": i.order_status.status_name,
                "order_status_color": i.order_status.color,
            }

            try:
                repair_order_issue_queryset = RepairOrderIssued.objects.get(repair_item_details=i.pk)
                order_item_data["vendor_name"] = repair_order_issue_queryset.vendor_name.account_head_name
            except:
                order_item_data["vendor_name"] = None
        
            res_data.append(order_item_data)

        return Response(
            {
                "data":{
                    "list":res_data
                },
                "message":res_msg.retrieve('Repair Details List'),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
    

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class RepairOrderDetailsListView(APIView):

    def get(self,request):

        queryset = RepairDetails.objects.all()
        serializer = RepairDetailsSerializer(queryset,many=True)
        
        return Response(
            {
                "data":{
                    "list":serializer.data
                },
                "message":res_msg.retrieve('Repair Details List'),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )

   
    def post(self,request):
       
        filter_condition = {}

        if request.user.role.is_admin == False:
            branch = request.user.branch.pk
        else:
            branch = request.data.get('branch')


        if branch != None:
            
            filter_condition['branch'] = branch
                      
        customer = request.data.get('customer',None)
        search = request.data.get('search',"")
        page = request.data.get('page') if request.data.get('page') else 1 
        items_per_page = request.data.get('items_per_page') if request.data.get('items_per_page') else 10
       
        if customer != None:
            filter_condition['customer_details'] = customer        
           
        if search != "":
           
            filter_condition['repair_number__icontains'] = search
           
        if len(filter_condition) != None:
           
            queryset = RepairDetails.objects.filter(**filter_condition).order_by('-id')
           
        else:
            queryset = RepairDetails.objects.all().order_by('-id')
       
        paginated_data = Paginator(queryset, items_per_page)
        serializer = RepairDetailsSerializer(paginated_data.get_page(page), many=True)
        total_items = len(queryset)
       
        response_data = []
       
        for data in serializer.data:
           
            res_data = data
           
            repair_queryset = RepairDetails.objects.get(id=data['id'])
           
            res_data['customer_name'] = repair_queryset.customer_details.customer_name
            res_data['repair_for_name'] = repair_queryset.repair_for.repair_for
            res_data['branch_name'] = repair_queryset.branch.branch_name
            res_data['status_name'] = repair_queryset.status.status_name

            item_details_queryset = RepairItemDetails.objects.filter(repair_order_details=repair_queryset.pk)
           
            total_amount = 0.0
           
            for items in item_details_queryset:
               
                total_amount += items.customer_charges
               
            payment_queryset = RepairPayment.objects.filter(repair_details=repair_queryset.pk)
           
            total_payment = 0.0
           
            for payments in payment_queryset:
               
                denomination_queryset = RepairPaymentDenominations.objects.filter(repair_payment_details=payments.pk)
               
                total_denominations = 0.0
               
                for denominations in denomination_queryset:
                   
                    total_denominations += denominations.total_amount
                   
                advance_queryset = RepairAdvanceDetails.objects.filter(repair_payment_details=payments.pk)
               
                total_advance =0.0
               
                for advance in advance_queryset:
                   
                    total_advance += advance.total_amount
                   
                paid_amount = total_denominations+total_advance
               
                total_payment += paid_amount
               
            balance_amount = total_amount-total_payment
           
            res_data['total_amount'] =total_amount
            res_data['total_payment'] =total_payment
            res_data['balance_amount'] =balance_amount
           
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
                "message":res_msg.retrieve("Repair Details Table List"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class RepairOrderIssueViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk):

        try:
            queryset = RepairOrderIssued.objects.get(id=pk)
        except:
            return Response({
                "message": res_msg.not_exists('Repair Order'),
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_200_OK)
        
        serializer = RepairOrderIssuedSerializer(queryset)
        dict_data = serializer.data
        particulars = []
        try:
            repair_item_queryset = RepairItemDetails.objects.filter(repair_order_details=queryset.repair_details.pk)
            
            for item in repair_item_queryset:
                
                item_details={
                    'id':item.pk,
                    'repair_order_details':item.repair_order_details.pk,
                    'repair_type':item.repair_type.pk,
                    'repair_type':item.repair_type.repair_type_name,
                    'item_details':item.item_details.pk,
                    'item_name':item.item_details.item_name,
                    'metal_details':item.metal_details.pk,
                    'metal_name':item.metal_details.metal_name,
                    'issued_gross_weight':item.issued_gross_weight,
                    'issued_net_weight':item.issued_net_weight,
                    'old_stone':item.old_stone,
                    'old_diamond':item.old_diamond,
                    'total_pieces':item.total_pieces,
                    'received_date' : item.repair_order_details.repair_recived_date
                }
                particulars.append(item_details)
            dict_data['item_data'] = particulars
        except Exception as err:
            dict_data['item_data'] = []

        return Response({
                "data": dict_data,
                "message": res_msg.retrieve('Repair Order Issue Details'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)


    def create(self, request):

        data = request.data

        try:
            repair_queryset = RepairDetails.objects.get(repair_number = data.get('repair_number'))
        except Exception as err:
            return Response({
                "message": res_msg.not_exists('Given Repair Order Id'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        
        for i in data.get('repair_items'):

            queryset = RepairItemDetails.objects.select_for_update().get(id=i)

            data['repair_details'] = repair_queryset.pk
            data['repair_item_details'] = queryset.pk
            data['vendor_name'] = data.get('vendor_name')
            data['issue_date'] = data.get('issue_date') 
            data['estimate_due_date'] = data.get('estimate_due_date')
            data['remainder_days'] = data.get('remainder_days') 
            data['remainder_date'] = data.get('remainder_date')
            data['created_at'] = timezone.now()
            data['created_by'] = request.user.id

            repair_order_issue_serializer = RepairOrderIssuedSerializer(data=data)

            if repair_order_issue_serializer.is_valid():

                repair_order_item_data = {
                    "is_assigned": True,
                    "assigned_by": data.get('assigned_by'),
                    "order_status": settings.REPAIR_ISSUED
                }

                repair_order_item_serailizer = RepairItemDetailsSerializer(queryset, data=repair_order_item_data, partial=True)

                if repair_order_item_serailizer.is_valid():
                    repair_order_item_serailizer.save()

                    repair_order_issue_serializer.save()
                else:
                    transaction.set_rollback(True)
                    return Response({
                        "data": repair_order_item_serailizer.errors,
                        "message": res_msg.in_valid_fields(),
                        "status": status.HTTP_400_BAD_REQUEST
                    }, status=status.HTTP_200_OK)
            else:
                transaction.set_rollback(True)
                return Response({
                    "data": repair_order_issue_serializer.errors,
                    "message": res_msg.in_valid_fields(),
                    "status": status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_200_OK)

        update_status = {}
        update_status['status'] = settings.REPAIR_ISSUED

        repair_order_queryset = RepairDetails.objects.get(id=repair_queryset.pk)
        repair_order_serializer = RepairDetailsSerializer(repair_order_queryset,data=update_status,partial=True)
        if repair_order_serializer.is_valid():
            repair_order_serializer.save()
        else:
            return Response({
                "data": repair_order_serializer.errors,
                "message": res_msg.in_valid_fields(),
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_200_OK)
        
        return Response({
            "message": res_msg.create('Repair Order Issue'),
            "status": status.HTTP_201_CREATED
        }, status=status.HTTP_200_OK)
        
       
    def update(self, request, pk):

        try:
            queryset = RepairOrderIssued.objects.get(id=pk)
        except Exception as err:
            return Response({
                "message": res_msg.not_exists('Repair Order Issue'),
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_200_OK)
        
        data = request.data

        data['repair_details'] = data.get('repair_details') 
        data['vendor_name'] = data.get('vendor_name')
        data['issue_date'] = data.get('issue_date') 
        data['estimate_due_date'] = data.get('estimate_due_date')
        data['remainder_days'] = data.get('remainder_days') 
        data['remainder_date'] = data.get('remainder_date')
        data['modified_at'] = timezone.now()
        data['modified_by'] = request.user.id
        serializer = RepairOrderIssuedSerializer(queryset, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": res_msg.update('Repair Order Issue'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        return Response({
                "data": serializer.errors,
                "message": res_msg.in_valid_fields(),
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_200_OK)
    

    def destroy(self, request, pk):
        try:
            queryset = RepairOrderIssued.objects.get(id=pk)
            queryset.delete()
            return Response({
                "message": res_msg.delete('Repair Order Issue'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        except RepairOrderIssued.DoesNotExist:
            return Response({
                "message": res_msg.not_exists('Repair Order Issue'),
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_200_OK)
        except ProtectedError:
            return Response({
                "message": res_msg.related_item('Delete'),
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({
                "message": res_msg.something_else(),
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_200_OK)


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class RepairIssueListView(APIView):
    def get(self,request):

        queryset = RepairOrderIssued.objects.all()
        serializer = RepairOrderIssuedSerializer(queryset,many=True)
        
        return Response(
            {
                "data":{
                    "list":serializer.data
                },
                "message":res_msg.retrieve('Repair Order Issue List'),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )

    def post(self, request):

        search = request.data.get('search') if request.data.get('search') else ''
        from_date = request.data.get('from_date') if request.data.get('from_date') else None
        to_date = request.data.get('to_date') if request.data.get('to_date') else None
        page = request.data.get('page') if request.data.get('page') else 1
        try:
            items_per_page = int(request.data.get('items_per_page', RepairOrderIssued.objects.all().count()))
            if items_per_page == 0:
                items_per_page = 10 
        except Exception as err:
            items_per_page = 10 
        
        filter_condition={}

        if from_date != None and to_date!= None:
           date_range=(from_date,to_date)
           filter_condition['created_at__range']=date_range

        if len(filter_condition) != 0:
                queryset = list(RepairOrderIssued.objects.filter(Q(repair_details__customer_details__customer_name__icontains=search) | Q(vendor_name__account_head_name__icontains=search) | Q(repair_issued_number__icontains=search),**filter_condition).order_by('id'))
        elif search != '':
                queryset = list(RepairOrderIssued.objects.filter(Q(repair_details__customer_details__customer_name__icontains=search) | Q(vendor_name__account_head_name__icontains=search) | Q(repair_issued_number__icontains=search)).order_by('id'))
        else:
            queryset = list(RepairOrderIssued.objects.all().order_by('id'))

        paginated_data = Paginator(queryset, items_per_page)
        serializer = RepairOrderIssuedSerializer(paginated_data.get_page(page), many=True)

        res_data = []
        
        for i in range(len(serializer.data)):
            dict_data = serializer.data[i]
            dict_data['vendor_name'] = queryset[i].vendor_name.account_head_name
            dict_data['status_name'] = queryset[i].repair_details.status.status_name
            dict_data['payment_status_name'] = queryset[i].payment_status.status_name
            dict_data['customer_name'] = queryset[i].repair_details.customer_details.customer_name
            dict_data['repair_for_name'] = queryset[i].repair_details.repair_for.repair_for
            dict_data['received_date'] = queryset[i].repair_details.repair_recived_date
            try:
                repair_order_item_queryset = RepairItemDetails.objects.get(repair_order_details=queryset[i].repair_details)
                dict_data['metal'] = repair_order_item_queryset.metal_details.metal_name
                dict_data['gross_weight'] = repair_order_item_queryset.issued_gross_weight
                dict_data['net_weight'] = repair_order_item_queryset.issued_net_weight
                dict_data['pieces'] = repair_order_item_queryset.total_pieces
                
            except Exception as err:
                dict_data['metal'] = "----"
                dict_data['gross_weight'] = "----"
                dict_data['net_weight'] = "----"
                dict_data['pieces'] = "----"
            
            res_data.append(dict_data)

        return Response({
            "data": {
                "list": res_data,
                "total_pages": paginated_data.num_pages,
                "current_page": page,
                "total_items": len(queryset),
                "current_items": len(serializer.data)
            },
            "message": res_msg.retrieve('Repair Order Issue List'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class GetRepairForDetails(APIView):
    def get(self,request):
            
        queryset = RepairFor.objects.all().order_by('id')
        serializer = RepairForSerializer(queryset,many=True)

        return Response(
            {
                "data": {
                    "list" : serializer.data
                },
                "message" : res_msg.retrieve("Repair For details"),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK
        ) 
       

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class GetRepairTypeDetails(APIView):
    def get(self,request):
            
        queryset = RepairType.objects.all().order_by('id')
        serializer = RepairTypeSerializer(queryset,many=True)

        return Response(
            {
                "data": {
                    "list" : serializer.data
                },
                "message" : res_msg.retrieve("Repair Type details"),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK
        ) 


# Generate Estimate Number
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class RepairOrderId(APIView):
    def get(self,request):
        try:
            queryset=RepairOrderNumber.objects.all().order_by('-id')[0]
            prefix = 'REORD-00'  # Prefix for the estimate number
            # timestamp = datetime.now().strftime('%Y%m%d%H%M%S')  # Current date and time
            # random_number = random.randint(1000000, 9999999)
            # Repair_number = f'{prefix}-{random_number}'

            Repair_number=f'{prefix}{int(queryset.pk)+1}'
            return Response(
                {
                    "repair_number": Repair_number,
                    "message" : res_msg.create("Repair Order Number"),
                    "status": status.HTTP_200_OK
                }, status=status.HTTP_200_OK
            )
        except Exception as err:
            return Response(
                {
                    "repair_number":"REORD-001",
                    "message":res_msg.retrieve("Repair Order Number"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
    
# Generate Estimate Number
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class RepairIssueId(APIView):
    def get(self,request):
        prefix = 'RE-ISU'  # Prefix for the estimate number
        # timestamp = datetime.now().strftime('%Y%m%d%H%M%S')  # Current date and time
        random_number = random.randint(1000000, 8888888)
        Repair_issue_number = f'{prefix}-{random_number}'

        return Response(
            {
                "data": Repair_issue_number,
                "message" : res_msg.create("Repair Issue Number"),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK
        )
    
# Generate Vendor Receipt Number
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class DeliveryNoteId(APIView):
    def get(self,request):
        prefix = 'DEL'  
        random_number = random.randint(1000000, 5555555)
        Repair_issue_number = f'{prefix}-{random_number}'

        return Response(
            {
                "data": Repair_issue_number,
                "message" : res_msg.create("Vendor Receipt Number"),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK
        )
    

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class DeliveryBillViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk):

        try:
            queryset = DeliveryBill.objects.get(id=pk)
        except:
            return Response({
                "message": res_msg.not_exists('Delivery Bill'),
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_200_OK)
        
        serializer = DeliveryBillSerializer(queryset)
        dict_data = serializer.data

        particulars = []
        try:
            repair_item_queryset = RepairItemDetails.objects.filter(repair_order_details=queryset.repair_receipt_id.repair_details.pk)
            for item in repair_item_queryset:
                
                item_details={
                    'id':item.pk,
                    'repair_order_details':item.repair_order_details.pk,
                    'repair_type':item.repair_type.pk,
                    'repair_type':item.repair_type.repair_type_name,
                    'item_details':item.item_details.pk,
                    'item_name':item.item_details.item_name,
                    'metal_details':item.metal_details.pk,
                    'metal_name':item.metal_details.metal_name,
                    'issued_gross_weight':item.issued_gross_weight,
                    'issued_net_weight':item.issued_net_weight,
                    'added_weight':item.added_net_weight,
                    'less_weight':item.less_weight,
                    'old_stone':item.old_stone,
                    'old_diamond':item.old_diamond,
                    'total_pieces':item.total_pieces,
                    'received_date' : item.repair_order_details.repair_recived_date
                }
                particulars.append(item_details)
            dict_data['item_data'] = particulars
        except Exception as err:
            dict_data['item_data'] = []
        
        return Response({
                "data": dict_data,
                "message": res_msg.retrieve('Delivery Bill'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)


    def create(self, request):
        data = request.data
     
        if request.user.role.is_admin == False:
            data['branch'] = request.user.branch.pk

        else:
            data['branch'] = data.get('branch')

        data['repair_receipt_id'] = data.get('repair_receipt_id')
        data['delivery_note_id'] = data.get('delivery_note_id')
        data['customer_mobile'] = data.get('customer_mobile')
        data['customer_details'] = data.get('customer_details')
        data['delivery_date'] = data.get('delivery_date')
        data['status'] = data.get('status')
        data['total_stone_rate'] = data.get('total_stone_rate') if data.get('total_stone_rate') != None else 0
        data['total_diamond_rate'] = data.get('total_diamond_rate') if data.get('total_diamond_rate') != None else 0
        data['estimate_repair_charge'] = data.get('estimate_repair_charge') if data.get('estimate_repair_charge') != None else 0
        data['working_charge'] = data.get('working_charge')
        data['added_weight_amount'] = data.get('added_weight_amount') if data.get('added_weight_amount') != None else 0
        data['less_weight_amount'] = data.get('less_weight_amount') if data.get('less_weight_amount') != None else 0
        data['advance_amount'] = data.get('advance_amount') if data.get('advance_amount') != None else 0
        data['grand_total'] = data.get('grand_total') if data.get('grand_total') != None else 0
        data['balance_amount'] = data.get('balance_amount') if data.get('balance_amount') != None else 0
        data['cash'] = data.get('cash') if data.get('cash') != None else 0
        data['upi'] = data.get('upi') if data.get('upi') != None else 0
        data['debit_card_amount'] = data.get('debit_card_amount') if data.get('debit_card_amount') != None else 0
        data['credit_card_amount'] = data.get('credit_card_amount') if data.get('credit_card_amount') != None else 0
        data['account_transfer'] = data.get('account_transfer') if data.get('account_transfer') != None else 0
        data['created_at'] = timezone.now()
        data['created_by'] = request.user.id

        serializer = DeliveryBillSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            repair_item_details = data.get('repair_item_details') if data.get('repair_item_details') else []
            if len(repair_item_details) != 0:
                for item in repair_item_details:
                    item_id = item.get('id') if item.get('id') else 0
                    repair_item_queryset = RepairItemDetails.objects.get(id=item_id)
                    item_data = {
                        'added_net_weight': item.get('added_net_weight'),
                        'less_weight': item.get('less_weight'),
                        'modified_at' : timezone.now(),
                        'modified_by' : request.user.id
                    }
                    repair_item_serializer = RepairItemDetailsSerializer(repair_item_queryset,data=item_data,partial=True)
                    if repair_item_serializer.is_valid():
                        repair_item_serializer.save()

            update_payment = {}
            update_payment['total_stone_rate'] = data.get('total_stone_rate') if data.get('total_stone_rate') != None else 0
            update_payment['total_diamond_rate'] = data.get('total_diamond_rate') if data.get('total_diamond_rate') != None else 0
            update_payment['estimate_repair_charge'] = data.get('estimate_repair_charge') if data.get('estimate_repair_charge') != None else 0
            update_payment['advance_amount'] = data.get('advance_amount') if data.get('advance_amount') != None else 0
            update_payment['balance_amount'] = data.get('balance_amount') if data.get('balance_amount') != None else 0
            update_payment['grand_total'] = data.get('grand_total') if data.get('grand_total') != None else 0
            update_payment['cash'] = data.get('cash') if data.get('cash') != None else 0
            update_payment['upi'] = data.get('upi') if data.get('upi') != None else 0
            update_payment['debit_card_amount'] = data.get('debit_card_amount') if data.get('debit_card_amount') != None else 0
            update_payment['credit_card_amount'] = data.get('credit_card_amount') if data.get('credit_card_amount') != None else 0
            update_payment['account_transfer'] = data.get('account_transfer') if data.get('account_transfer') != None else 0
            update_payment['modified_at'] = timezone.now()
            update_payment['modified_by'] = request.user.id

            repair_receipt_details = CustomerReceipt.objects.get(id=data.get('repair_receipt_id'))
            repair_order_id = repair_receipt_details.repair_details.pk
            repair_order_queryset = RepairDetails.objects.get(id=repair_order_id)
            repair_order_serializer = RepairDetailsSerializer(repair_order_queryset,data=update_payment,partial=True)
            if repair_order_serializer.is_valid():
                repair_order_serializer.save()
           
            return Response({
                "data": serializer.data,
                "message": res_msg.create('Delivery Bill'),
                "status": status.HTTP_201_CREATED
            }, status=status.HTTP_200_OK)
        
        else:
            return Response({
                "data": serializer.errors,
                "message": res_msg.in_valid_fields(),
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_200_OK)
        
    def update(self, request, pk):

        try:
            queryset = DeliveryBill.objects.get(id=pk)
        except Exception as err:
            return Response({
                "message": res_msg.not_exists('Delivery Bill details'),
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_200_OK)
        
        data = request.data
               
        if request.user.role.is_admin == False:
            data['branch'] = request.user.branch.pk

        else:
            data['branch'] = data.get('branch')

        data['repair_receipt_id'] = data.get('repair_receipt_id')
        data['delivery_note_id'] = data.get('delivery_note_id')
        data['customer_mobile'] = data.get('customer_mobile')
        data['customer_details'] = data.get('customer_details')
        data['delivery_date'] = data.get('delivery_date')
        data['status'] = data.get('status')
        data['total_stone_rate'] = data.get('total_stone_rate') if data.get('total_stone_rate') != None else 0
        data['total_diamond_rate'] = data.get('total_diamond_rate') if data.get('total_diamond_rate') != None else 0
        data['estimate_repair_charge'] = data.get('estimate_repair_charge') if data.get('estimate_repair_charge') != None else 0
        data['working_charge'] = data.get('working_charge')
        data['added_weight_amount'] = data.get('added_weight_amount') if data.get('added_weight_amount') != None else 0
        data['less_weight_amount'] = data.get('less_weight_amount') if data.get('less_weight_amount') != None else 0
        data['advance_amount'] = data.get('advance_amount') if data.get('advance_amount') != None else 0
        data['grand_total'] = data.get('grand_total') if data.get('grand_total') != None else 0
        data['balance_amount'] = data.get('balance_amount') if data.get('balance_amount') != None else 0
        data['cash'] = data.get('cash') if data.get('cash') != None else 0
        data['upi'] = data.get('upi') if data.get('upi') != None else 0
        data['debit_card_amount'] = data.get('debit_card_amount') if data.get('debit_card_amount') != None else 0
        data['credit_card_amount'] = data.get('credit_card_amount') if data.get('credit_card_amount') != None else 0
        data['account_transfer'] = data.get('account_transfer') if data.get('account_transfer') != None else 0
        data['modified_at'] = timezone.now()
        data['modified_by'] = request.user.id

        serializer = DeliveryBillSerializer(queryset,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()

            repair_item_details = data.get('repair_item_details') if data.get('repair_item_details') else []
            if len(repair_item_details) != 0:
                for item in repair_item_details:
                    item_id = item.get('id') if item.get('id') else 0
                    repair_item_queryset = RepairItemDetails.objects.get(id=item_id)
                    item_data = {
                        'added_net_weight': item.get('added_net_weight'),
                        'less_weight': item.get('less_weight'),
                        'modified_at' : timezone.now(),
                        'modified_by' : request.user.id
                    }
                    repair_item_serializer = RepairItemDetailsSerializer(repair_item_queryset,data=item_data,partial=True)
                    if repair_item_serializer.is_valid():
                        repair_item_serializer.save()

            update_payment = {}
            update_payment['total_stone_rate'] = data.get('total_stone_rate') if data.get('total_stone_rate') != None else 0
            update_payment['total_diamond_rate'] = data.get('total_diamond_rate') if data.get('total_diamond_rate') != None else 0
            update_payment['estimate_repair_charge'] = data.get('estimate_repair_charge') if data.get('estimate_repair_charge') != None else 0
            update_payment['advance_amount'] = data.get('advance_amount') if data.get('advance_amount') != None else 0
            update_payment['balance_amount'] = data.get('balance_amount') if data.get('balance_amount') != None else 0
            update_payment['grand_total'] = data.get('grand_total') if data.get('grand_total') != None else 0
            update_payment['cash'] = data.get('cash') if data.get('cash') != None else 0
            update_payment['upi'] = data.get('upi') if data.get('upi') != None else 0
            update_payment['debit_card_amount'] = data.get('debit_card_amount') if data.get('debit_card_amount') != None else 0
            update_payment['credit_card_amount'] = data.get('credit_card_amount') if data.get('credit_card_amount') != None else 0
            update_payment['account_transfer'] = data.get('account_transfer') if data.get('account_transfer') != None else 0
            update_payment['modified_at'] = timezone.now()
            update_payment['modified_by'] = request.user.id

            repair_receipt_details = CustomerReceipt.objects.get(id=data.get('repair_receipt_id'))
            repair_order_id = repair_receipt_details.repair_details.pk
            repair_order_queryset = RepairDetails.objects.get(id=repair_order_id)
            repair_order_serializer = RepairDetailsSerializer(repair_order_queryset,data=update_payment,partial=True)
            if repair_order_serializer.is_valid():
                repair_order_serializer.save()
            return Response({
                "data": serializer.data,
                "message": res_msg.update('Delivery Bill Details'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        return Response({
                "data": serializer.errors,
                "message": res_msg.in_valid_fields(),
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_200_OK)
    
    def destroy(self, request, pk):
        try:
            queryset = DeliveryBill.objects.get(id=pk)
            queryset.delete()
            return Response({
                "message": res_msg.delete('Delivery Bill'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        except DeliveryBill.DoesNotExist:
            return Response({
                "message": res_msg.not_exists('Delivery Bill'),
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_200_OK)
        except ProtectedError:
            return Response({
                "message": res_msg.related_item('Delete'),
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({
                "message": res_msg.something_else(),
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_200_OK)
        

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class DeliveryBillListView(APIView):

    def get(self,request):

        queryset = DeliveryBill.objects.all()
        serializer = DeliveryBillSerializer(queryset,many=True)
        
        return Response(
            {
                "data":{
                    "list":serializer.data
                },
                "message":res_msg.retrieve('Delivery Bill Details'),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )

    def post(self, request):

        search = request.data.get('search') if request.data.get('search') else ''
        from_date = request.data.get('from_date') if request.data.get('from_date') else None
        to_date = request.data.get('to_date') if request.data.get('to_date') else None
        page = request.data.get('page') if request.data.get('page') else 1
        try:
            items_per_page = int(request.data.get('items_per_page', DeliveryBill.objects.all().count()))
            if items_per_page == 0:
                items_per_page = 10 
        except Exception as err:
            items_per_page = 10 
        
        filter_condition={}

        if from_date != None and to_date!= None:
           date_range=(from_date,to_date)
           filter_condition['created_at__range']=date_range

        if len(filter_condition) != 0:
                queryset = list(DeliveryBill.objects.filter(Q(customer_details__customer_name__icontains=search) | Q(customer_mobile__icontains=search) | Q(delivery_note_id=search),**filter_condition).order_by('-id'))
        elif search != '':
                queryset = list(DeliveryBill.objects.filter(Q(customer_details__customer_name__icontains=search) | Q(customer_mobile__icontains=search) | Q(delivery_note_id=search)).order_by('-id'))
        else:
            queryset = list(DeliveryBill.objects.all().order_by('-id'))

        paginated_data = Paginator(queryset, items_per_page)
        serializer = DeliveryBillSerializer(paginated_data.get_page(page), many=True)

        res_data = []
        
        for i in range(len(serializer.data)):
            dict_data = serializer.data[i]
            dict_data['status_name'] = queryset[i].status.status_name
            dict_data['payment_status_name'] = queryset[i].repair_receipt_id.payment_status.status_name
            dict_data['customer_name'] = queryset[i].customer_details.customer_name
            dict_data['repair_for_name'] = queryset[i].repair_receipt_id.repair_details.repair_for.repair_for
            dict_data['delivered_date'] = queryset[i].repair_receipt_id.repair_details.repair_delivery_date

            try:
                repair_order_issue_queryset = RepairOrderIssued.objects.get(repair_details=queryset[i].repair_receipt_id.repair_details)
                dict_data['vendor_name'] = repair_order_issue_queryset.vendor_name.account_head_name
            except Exception as err:
                dict_data['vendor_name'] = "-----"
                
            try:
                repair_order_item_queryset = RepairItemDetails.objects.get(repair_order_details=queryset[i].repair_receipt_id.repair_details)
                dict_data['metal'] = repair_order_item_queryset.metal_details.metal_name
                dict_data['gross_weight'] = repair_order_item_queryset.issued_gross_weight
                dict_data['net_weight'] = repair_order_item_queryset.issued_net_weight
                dict_data['pieces'] = repair_order_item_queryset.total_pieces
                
            except Exception as err:
                dict_data['metal'] = "----"
                dict_data['gross_weight'] = "----"
                dict_data['net_weight'] = "----"
                dict_data['pieces'] = "----"

            res_data.append(dict_data)

        return Response({
            "data": {
                "list": res_data,
                "total_pages": paginated_data.num_pages,
                "current_page": page,
                "total_items": len(queryset),
                "current_items": len(serializer.data)
            },
            "message": res_msg.retrieve('Vendor Receipt List'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
    


############# ORDER ITEM RECEIVED API ######################
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class RecieveItemView(APIView):
    def post(self, request):

        data = request.data

        try:
            queryset = RepairItemDetails.objects.get(id=data.get('item_id'))
            
            status_data = {
                "order_status": settings.REPAIR_RECEIVED,
                "is_recieved": data.get('status')
            }

            repair_item_serailizer = RepairItemDetailsSerializer(queryset, data=status_data, partial=True)

            if repair_item_serailizer.is_valid():
                repair_item_serailizer.save()

                repair_items_queryset = list(RepairItemDetails.objects.filter(repair_order_details=queryset.repair_order_details.pk))

                order_status = settings.REPAIR_ISSUED

                validation_list = []
                for item in repair_items_queryset:
                    if str(item.order_status.pk) == str(settings.REPAIR_RECEIVED):
                        validation_list.append(1)
                    else:
                        validation_list.append(0)

                if 0 in validation_list:
                    order_status = settings.REPAIR_ISSUED
                else:
                    order_status = settings.REPAIR_RECEIVED

                try:
                    repair_queryset = RepairDetails.objects.get(id=queryset.repair_order_details.pk)
                    
                    repair_serializer = RepairDetailsSerializer(repair_queryset, data={
                        "status": order_status
                    }, partial=True)

                    if repair_serializer.is_valid():
                        repair_serializer.save()
             
                        repair_issue_queryset = RepairOrderIssued.objects.get(repair_details=repair_serializer.data['id'])

                        ledger_data={}
                        ledger_data['vendor_details']=repair_issue_queryset.vendor_name.pk
                        ledger_data['transaction_date']=timezone.now()
                        ledger_data['refference_number']=repair_issue_queryset.repair_details.repair_number
                        ledger_data['transaction_type']=settings.REPAIR_VENDOR_LEDGER
                        ledger_data['transaction_amount']=queryset.vendor_charges
                        ledger_data['branch'] = queryset.repair_order_details.branch.pk
                                
                        ledger_serializer = VendorLedgerSerializer(data=ledger_data)
                    
                        if ledger_serializer.is_valid():
                            ledger_serializer.save()

                        else:                    
                            transaction.set_rollback(True)
                            return Response(
                                {
                                    "data":ledger_serializer.errors,
                                    "message":"Error while receiving item",
                                    "status":status.HTTP_400_BAD_REQUEST
                                }
                            ) 

                        customer_ledger_data={}
                        customer_ledger_data['customer_details']=queryset.repair_order_details.customer_details.pk
                        customer_ledger_data['entry_date']=timezone.now()
                        customer_ledger_data['transaction_type']=settings.CREDIT_ENTRY
                        customer_ledger_data['entry_type']=settings.REPAIR_ENTRY_CUSTOMER_LEDGER
                        customer_ledger_data['invoice_number']=queryset.repair_order_details.repair_number
                        customer_ledger_data['refference_number']=None
                        customer_ledger_data['transaction_amount'] = queryset.customer_charges
                        customer_ledger_data['transaction_weight'] = 0.0
                        customer_ledger_data['branch'] = queryset.repair_order_details.branch.pk
                        
                        customer_ledger_serializer = CustomerLedgerSerializer(data=customer_ledger_data)
                    
                        if customer_ledger_serializer.is_valid():
                            customer_ledger_serializer.save()

                        else:                    
                            transaction.set_rollback(True)
                            return Response(
                                {
                                    "data":customer_ledger_serializer.errors,
                                    "message":"Error while receiving item",
                                    "status":status.HTTP_400_BAD_REQUEST
                                }
                            )         
                except:
                    pass

                return Response({
                    "message": "Item recieved",
                    "status": status.HTTP_200_OK
                },status=status.HTTP_200_OK)
            else:
                return Response({
                    "message": "Item not recieved",
                    "status": status.HTTP_204_NO_CONTENT
                },status=status.HTTP_200_OK)
            
        except RepairItemDetails.DoesNotExist:
            return Response({
                "message": res_msg.not_exists('Repair details'),
                "status": status.HTTP_404_NOT_FOUND
            },status=status.HTTP_200_OK)
        
        except Exception as err:
            return Response({
                "data" : str(err),
                "message": res_msg.something_else(),
                "status": status.HTTP_204_NO_CONTENT
            },status=status.HTTP_200_OK)
        


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class RepairPaymentView(viewsets.ViewSet):
    @transaction.atomic
    def create(self,request):
    
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

            if request.user.role.is_admin == False:
                branch = request.user.branch.pk
            else:
                branch = request_data.get('branch')
                
            queryset = RepairDetails.objects.get(id=pk)
            
            payment_details_data = {}
            payment_details_data['repair_details'] = queryset.pk
            payment_details_data['payment_date'] = timezone.now()
            payment_details_data['created_by'] = request.user.id
            payment_details_data['branch'] = branch

            pay_id = True

            while pay_id ==True:
                
                random_number = random.randint(100, 9999999)
                
                generated_number = "RPT"+str(random_number)
                
                try:
                
                    bill_number_queryset = RepairPayment.objects.get(repair_payment_id=generated_number)
                    pay_id = True
                except RepairPayment.DoesNotExist:
                    payment_details_data['repair_payment_id'] = generated_number
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
                    
            payment_details_serializer = RepairPaymentSerializer(data=payment_details_data)
            
            if payment_details_serializer.is_valid():
                
                payment_details_serializer.save()
                
                payment_denomination_details = request_data.get('payment_denomination_details',[])
                
                for denominations in payment_denomination_details:
                    
                    denominations['repair_payment_details'] = payment_details_serializer.data['id']
                    
                    denomination_serializer = RepairPaymentDenominationsSerializer(data=denominations)
                    
                    if denomination_serializer.is_valid():
                        
                        denomination_serializer.save()
                        
                    else:
                        
                        transaction.set_rollback(True)
                        
                        return Response(
                            {
                                "data":denomination_serializer.errors,
                                "message":res_msg.not_create("Repair payment"),
                                "status":status.HTTP_400_BAD_REQUEST
                            },status=status.HTTP_200_OK
                        )
                        
                advance_details = request_data.get('advance_details',[])
                
                for advance in advance_details:
                    
                    advance['repair_payment_details'] = payment_details_serializer.data['id']
                    
                    advance_serializer = RepairAdvanceDetailsSerializer(data=advance)
                    
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
                                    "message":"for advance "+str(advance_queryset.advance_id)+" remaining weight is "+str(remaining_weight)+" remaining amount is "+str(remaining_amount),
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
                            advance_customer_ledger_data['invoice_number'] = queryset.repair_number
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
                                        "message":res_msg.not_create("Repair payment"),
                                        "status":status.HTTP_400_BAD_REQUEST
                                    },status=status.HTTP_200_OK
                                )
                            
                        else:
                            transaction.set_rollback(True)
                            return Response(
                                {
                                    "data":advance_log_update_serializer.errors,
                                    "message":res_msg.not_create("Repair payment"),
                                    "status":status.HTTP_400_BAD_REQUEST
                                },status=status.HTTP_200_OK
                            )
                            
                        log_calculation_queryset = AdvanceLogs.objects.filter(advance_details=advance_queryset.pk,is_cancelled=False)
                        
                        updated_redeem_amount = 0
                        updated_redeem_weight = 0
                        
                        for update_calculation in log_calculation_queryset:
                            
                            updated_redeem_amount += update_calculation.redeem_amount
                            updated_redeem_weight += update_calculation.redeem_weight
                            
                        if advance_queryset.total_advance_amount == updated_redeem_amount and advance_queryset.total_advance_weight == updated_redeem_weight:
                            
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
                                        "message":res_msg.not_create("Repair payment"),
                                        "status":status.HTTP_400_BAD_REQUEST
                                    },status=status.HTTP_200_OK
                                )      
                             
                        total_denomination = 0                        
                        total_advance = 0
                        
                        denomination_queryset = RepairPaymentDenominations.objects.filter(repair_payment_details=payment_details_serializer.data['id'])
                        
                        for denomination in denomination_queryset:
                            
                            total_denomination += denomination.total_amount
                            
                        advance_amount_queryset = RepairAdvanceDetails.objects.filter(repair_payment_details=payment_details_serializer.data['id'])
                        
                        for advance_amount in advance_amount_queryset:
                            
                            total_advance += advance_amount.total_amount
                           
                        total_amount = total_denomination  + total_advance 
                        
                        total_customer_ledger_data={}
                        
                        total_customer_ledger_data['customer_details'] = queryset.customer_details.pk
                        total_customer_ledger_data['entry_date'] = timezone.now()
                        total_customer_ledger_data['entry_type'] = settings.REPAIR_ENTRY_CUSTOMER_LEDGER
                        total_customer_ledger_data['transaction_type'] = settings.DEBIT_ENTRY
                        total_customer_ledger_data['invoice_number'] = queryset.repair_number
                        total_customer_ledger_data['reffrence_number'] = payment_details_serializer.data['repair_payment_id']
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
                                    "message":res_msg.not_create("Repair payment"),
                                    "status":status.HTTP_400_BAD_REQUEST
                                },status=status.HTTP_200_OK
                            )               
                    else:
                        
                        transaction.set_rollback(True)
                        
                        return Response(
                            {
                                "data":advance_serializer.errors,
                                "message":res_msg.not_create("Repair payment"),
                                "status":status.HTTP_400_BAD_REQUEST
                            },status=status.HTTP_200_OK
                        )
                    
                return Response(
                    {
                        "data":payment_details_serializer.data,
                        "message":res_msg.create("Repair payment"),
                        "status":status.HTTP_200_OK
                    },status=status.HTTP_200_OK
                )
            
            else:
                transaction.set_rollback(True)
                return Response(
                    {
                        "data":payment_details_serializer.errors,
                        "message":res_msg.not_create("Repair payment"),
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
        
    def retrieve(self,request,pk):
        
        try:
            
            if pk == None:
                
                return Response(
                    {
                        "data":res_msg.missing_fields("ID"),
                        "status":status.HTTP_204_NO_CONTENT
                    },status=status.HTTP_200_OK
                )
            
            queryset = RepairPayment.objects.get(id=pk)
            
            serializer = RepairPaymentSerializer(queryset)
            
            res_data = serializer.data
            
            res_data['repair_id'] = queryset.repair_details.repair_number
            
            denomination_queryset = RepairPaymentDenominations.objects.filter(repair_payment_details=queryset.pk)
            
            denomination_serializer = RepairPaymentDenominationsSerializer(denomination_queryset,many=True)
            
            res_data['repair_payment_details'] = denomination_serializer.data
            
            advance_queryset = RepairAdvanceDetails.objects.filter(repair_payment_details=queryset.pk)
            
            advance_serializer = RepairAdvanceDetailsSerializer(advance_queryset,many=True)
            
            res_data['advance_details'] = advance_serializer.data
            
            return Response(
                {
                    "data":res_data,
                    "message":res_msg.retrieve("Repair Payment"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
            
        except RepairPayment.DoesNotExist:
            
            return Response(
                {
                    "message":res_msg.not_exists("Repair Payment"),
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
           
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class RepairPaymentListView(APIView):
    
    def post(self,request):
        
        from_date = request.data.get('from_date',None)
        to_date = request.data.get('to_date',None)
        search = request.data.get('search',"")        
        page = request.data.get('page',1)
        items_per_page = request.data.get('items_per_page',10)
        
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
            or_conditions.append(Q(repair_payment_id__icontains=search))

            for condition in or_conditions:
                combined_conditions |= condition
           
        if from_date != None and to_date != None:
            
            data_range = (from_date,to_date)
            
            filter_condition['payment_date__range'] =  data_range
           
        if len(filter_condition) != 0 :
            
            queryset = RepairPayment.objects.filter(combined_conditions,**filter_condition).order_by('-id')
            
        else:
            
            queryset = RepairPayment.objects.filter(combined_conditions).order_by('-id')
            
        paginated_data = Paginator(queryset, items_per_page)
        serializer = RepairPaymentSerializer(paginated_data.get_page(page), many=True)
        total_items = len(queryset)

        response_data = []
        
        for data in serializer.data:
            
            res_data = data
            
            repair_payment_queryset = RepairPayment.objects.get(id=data['id'])
            total_redeemed = RepairAdvanceDetails.objects.filter(repair_payment_details = data['id']).aggregate(redeem_amount=Sum('redeem_amount'),redeem_weight=Sum('redeem_weight'))
            total_dominations = RepairPaymentDenominations.objects.filter(repair_payment_details = data['id']).aggregate(total_amount=Sum('total_amount'))

            res_data['repair_id'] = repair_payment_queryset.repair_details.repair_number
            res_data['total_redeemed_amount'] =total_redeemed['redeem_amount']
            res_data['total_redeemed_weight'] =total_redeemed['redeem_weight']
            res_data['total_dominations'] =total_dominations['total_amount']
            
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