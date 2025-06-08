from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.response import Response
from .models import *
from .serializer import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes, authentication_classes
from django.utils import timezone
from django.db.models import ProtectedError
from django.core.paginator import Paginator
from app_lib.response_messages import ResponseMessages
from django.conf import settings
from django.db.models import Q
from django.db import transaction
from books.models import AccountHeadAddress
from settings.models import *
from payment_management.models import *
from payment_management.serializer import *
from repair_management.models import *
from repair_management.serializer import *

res_msg = ResponseMessages()

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class OrderForListView(APIView):
    def get(self, request):
        queryset = OrderFor.objects.filter(is_active=True).order_by('id')
        serializer = OrderForSerializer(queryset, many=True)

        return Response({
            "data":  {
                "list": serializer.data
            },
            "message": res_msg.retrieve('Order for'),
            "status": status.HTTP_200_OK 
        }, status=status.HTTP_200_OK)
    

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class PriorityListView(APIView):
    def get(self, request):
        queryset = Priority.objects.filter(is_active=True).order_by('id')
        serializer = PrioritySerializer(queryset, many=True)

        return Response({
            "data":  {
                "list": serializer.data
            },
            "message": res_msg.retrieve('Priority'),
            "status": status.HTTP_200_OK 
        }, status=status.HTTP_200_OK)


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class GenerateOrderId(APIView):
    def get(self, request):

        res_data = {}
        try:
            ses_order_queryset = SessionOrderId.objects.get(user=request.user.id)

            try:
                queryset = OrderDetails.objects.get(order_id=ses_order_queryset.ses_order_id.pk)

                res_data['order_id'] = queryset.order_id.order_id
                res_data['order_for'] = queryset.order_for.pk
                res_data['order_date'] = queryset.order_date
                res_data['no_of_days'] = queryset.no_of_days
                res_data['due_date'] = queryset.due_date
                res_data['branch'] = queryset.branch.pk
                res_data['priority'] = queryset.priority.pk
                res_data['from_draft'] = True
                res_data['payment_module'] = 1
                
                # if str(queryset.order_for.pk) == str(settings.ORDER_FOR_CUSTOMER):
                res_data['customer_no'] = queryset.customer.phone
                res_data['customer'] = queryset.customer.pk
                res_data['customer_name'] = queryset.customer_name

            except OrderDetails.DoesNotExist:
                res_data['order_id'] = ses_order_queryset.ses_order_id.order_id
                res_data['payment_module'] = 1
                res_data['from_draft'] = False

        except SessionOrderId.DoesNotExist:
            data = {
                'order_id': None,
                'created_at': timezone.now(),
                'created_by': request.user.id
            }

            order_id_serializer = OrderIdSerializer(data=data)

            if order_id_serializer.is_valid():
                order_id_serializer.save()

                update_data = {
                    'order_id': 'ORDER-'+(str(order_id_serializer.data.get('id')).zfill(4)),
                }

                get_order_id_queryset = OrderId.objects.get(id=order_id_serializer.data.get('id'))

                update_order_id_serializer = OrderIdSerializer(get_order_id_queryset, data=update_data, partial=True)

                if update_order_id_serializer.is_valid():
                    update_order_id_serializer.save()

                    ses_data = {
                        'ses_order_id': order_id_serializer.data.get('id'),
                        'user': request.user.id
                    }

                    ses_oder_id_serializer = SessionOrderIdSerializer(data=ses_data)

                    if ses_oder_id_serializer.is_valid():
                        ses_oder_id_serializer.save()

                        res_data['order_id'] = update_order_id_serializer.data.get('order_id')
                        res_data['payment_module'] = 1
                        res_data['from_draft'] = False
                    else:
                        return Response({
                            "data": ses_oder_id_serializer.errors,
                            "message": res_msg.in_valid_fields(),
                            "status": status.HTTP_200_OK
                        }, status=status.HTTP_200_OK)
                    
            else:
                return Response({
                    "data": order_id_serializer.errors,
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
            "message": res_msg.retrieve('Order Id'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class OrderFileUpload(APIView):
    def post(self, request):

        data = {
            "image": request.FILES['image'] if 'image' in request.FILES else None,
            "order_id": '_'.join(request.POST.get('order_id').split(' ')),
            "order_item": '_'.join(request.POST.get('order_item').split(' '))
        }
        
        serializer = OrderItemAttachmentsSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": "Image uploaded successfully",
                "status": status.HTTP_201_CREATED
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "data": serializer.data,
                "message": "Image not uploaded",
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_200_OK)


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class OrderViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk):
        try:
            queryset = OrderDetails.objects.get(id=pk)
        except OrderDetails.DoesNotExist:
                return Response({
                    "message": res_msg.not_exists('Order details'),
                    "status": status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK)
        
        serializer = OrderDetailsSerializer(queryset)

        res_data = serializer.data
        res_data['order_id'] = queryset.order_id.order_id
        
        res_data['particular_list'] = []
        res_data['branch_name'] = queryset.branch.branch_name
        res_data['priority_name'] = queryset.priority.name
        res_data['pending_quantity'] = queryset.total_quantity
        res_data['order_status_name'] = queryset.order_status.status_name
        res_data['order_status_color'] = queryset.order_status.color
        
        # if str(queryset.order_for.pk) == str(settings.ORDER_FOR_CUSTOMER):
        res_data['customer_no'] = queryset.customer.phone
        
        item_queryset = list(OrderItemDetails.objects.filter(order_id=queryset.order_id).order_by('-id'))
        for i in item_queryset:
            order_item_data = {
                "id": i.pk,
                "order_id": i.order_id.order_id,
                "metal": i.metal.pk,
                "metal_name": i.metal.metal_name,
                "purity": i.purity.pk,
                "purity_name": i.purity.purity_name,
                "item": i.item.pk,
                "item_name": i.item.item_name,
                "sub_item": i.sub_item.pk,
                "sub_item_name": i.sub_item.sub_item_name,
                "gross_weight": i.gross_weight,
                "net_weight": i.net_weight,
                "pieces": i.pieces,
                "metal_rate": i.metal_rate,
                "gender": i.gender.pk,
                "gender_name": i.gender.name,
                "measurement_type": i.measurement_type.pk if i.measurement_type else None,
                "measurement_name": i.measurement_type.measurement_name if i.measurement_type else 'Not Mentioned',
                "measurement_value": i.measurement_value,
                "total_stone_weight": i.total_stone_weight,
                "total_stone_pieces": i.total_stone_pieces,
                "total_stone_amount": i.total_stone_amount,
                "stone_description": i.stone_description,
                "total_diamond_weight": i.total_diamond_weight,
                "total_diamond_pieces": i.total_diamond_pieces,
                "total_diamond_amount": i.total_diamond_amount,
                "diamond_description": i.diamond_description,
                "actual_amount": i.actual_amount,
                "total_amount": i.total_amount,
                "description": i.description,
                "is_assigned": i.is_assigned,
                "is_recieved": i.is_recieved,
                "assigned_by": i.assigned_by.email if i.assigned_by else None,
                "order_status_name": i.order_status.status_name,
                "order_status_color": i.order_status.color,
                "order_status": i.order_status.pk
            }

            try:
                order_issue_queryset = OrderIssue.objects.get(order_item=i.pk)
                order_item_data["vendor"] = order_issue_queryset.vendor.account_head_name
            except:
                order_item_data["vendor"] = None

            try:
                order_attachments_queryset = list(OrderItemAttachments.objects.filter(order_id=i.order_id.order_id, order_item='_'.join(i.item.item_name.split(' '))))
                order_attachments_serializer = OrderItemAttachmentsSerializer(order_attachments_queryset, many=True)
                order_item_data["attachments"] = order_attachments_serializer.data
            except:
                order_item_data["attachments"] = []

            if i.is_recieved:
                res_data['pending_quantity'] -= 1

            res_data['particular_list'].append(order_item_data)

        old_gold_queryset = list(RepairOrderOldGold.objects.filter(refference_number=queryset.order_id).order_by('-id'))
        oldgold_data = []
        for oldgold in old_gold_queryset:
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
                'purity':oldgold.purity,
            }
            
            oldgold_data.append(oldgold_details)
        res_data['oldgold_details']=oldgold_data

        return Response({
            "data" : res_data,
            "message": res_msg.retrieve('Order'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
    

    def create(self, request):
        data = request.data

        created_at = timezone.now()
        created_by = request.user.id

        try:
            ses_order_id_queryset = SessionOrderId.objects.get(user=request.user.id)
        except:
            return Response({
                "message": "Something wrong in given order id",
                "status": status.HTTP_204_NO_CONTENT
            }, status=status.HTTP_200_OK)
        
        branch = data.get('branch', None) if data.get('branch') else request.user.branch.id

        order_item_queryset = list(OrderItemDetails.objects.filter(order_id=ses_order_id_queryset.ses_order_id.pk))
            
        total_weight = 0
        total_quantity = 0
        approximate_amount = 0
        for i in order_item_queryset:
            total_weight += float(i.gross_weight)
            total_quantity += 1
            approximate_amount += float(i.total_amount)

        order_details_data = {
            "order_id": ses_order_id_queryset.ses_order_id.pk,
            "order_for": data.get('order_for'),
            "priority": data.get('priority'),
            "order_date": data.get("order_date"),
            "no_of_days": data.get('no_of_days'),
            "due_date": data.get('due_date'),
            "branch": branch,
            "customer": data.get('customer'),
            "customer_name": data.get('customer_name'),
            "total_weight": total_weight,
            "total_quantity": total_quantity,
            "approximate_amount": approximate_amount,
            "is_order_scheduled": True,
            "created_at": created_at,
            "created_by": created_by
        }
       
        try:
            order_details_queryset = OrderDetails.objects.get(order_id=ses_order_id_queryset.ses_order_id.pk)

            order_details_serializer = OrderDetailsSerializer(order_details_queryset, data=order_details_data, partial=True)

            try:
                if order_details_serializer.is_valid():
                    order_details_serializer.save()      
                    ses_order_id_queryset.delete()
                    return Response({
                        "data": order_details_serializer.data,
                        "message": res_msg.create('Order'),
                        "status": status.HTTP_201_CREATED
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        "data": order_details_serializer.errors,
                        "message": res_msg.in_valid_fields(),
                        "status": status.HTTP_400_BAD_REQUEST
                    }, status=status.HTTP_200_OK)
            except Exception as err:
                return Response({
                    "message": res_msg.something_else(),
                    "status": status.HTTP_204_NO_CONTENT
                }, status=status.HTTP_200_OK)
        except OrderDetails.DoesNotExist:
            
            order_details_serializer = OrderDetailsSerializer(data=order_details_data)

            try:
                if order_details_serializer.is_valid():
                    order_details_serializer.save()      

                    ses_order_id_queryset.delete()
                    return Response({
                        "data": order_details_serializer.data,
                        "message": res_msg.create('Order'),
                        "status": status.HTTP_201_CREATED
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        "data": order_details_serializer.errors,
                        "message": res_msg.in_valid_fields(),
                        "status": status.HTTP_400_BAD_REQUEST
                    }, status=status.HTTP_200_OK)
            except Exception as err:
                return Response({
                    "message": res_msg.something_else(),
                    "status": status.HTTP_204_NO_CONTENT
                }, status=status.HTTP_200_OK)
        

    def update(self, request, pk):

        data = request.data

        modified_at = timezone.now()
        modified_by = request.user.id

        try:
            queryset = OrderDetails.objects.get(id=pk)

            branch = data.get('branch', None) if data.get('branch') else request.user.branch.id

            order_item_queryset = list(OrderItemDetails.objects.filter(order_id=queryset.order_id.pk))
            
            total_weight = 0
            total_quantity = 0
            approximate_amount = 0
            for i in order_item_queryset:
                total_weight += float(i.gross_weight)
                total_quantity += 1
                approximate_amount += float(i.total_amount)

            order_details_data = {
                "order_for": data.get('order_for'),
                "priority": data.get('priority'),
                "order_date": data.get("order_date"),
                "no_of_days": data.get('no_of_days'),
                "due_date": data.get('due_date'),
                "branch": branch,
                "customer": data.get('customer'),
                "customer_name": data.get('customer_name'),
                "total_weight": total_weight,
                "total_quantity": total_quantity,
                "approximate_amount": approximate_amount,
                "modified_at": modified_at,
                "modified_by": modified_by
            }
            
            order_details_serializer = OrderDetailsSerializer(queryset, data=order_details_data, partial=True)

            if order_details_serializer.is_valid():
                order_details_serializer.save()
            
                return Response({
                        "data": order_details_serializer.data,
                        "message": res_msg.update('Order details'),
                        "status": status.HTTP_200_OK
                    }, status=status.HTTP_200_OK)
            
            else:
                return Response({
                    "data": order_details_serializer.errors,
                    "message": res_msg.in_valid_fields(),
                    "status": status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_200_OK)
        
        except OrderDetails.DoesNotExist:
            return Response({
                "message": res_msg.not_exists('Order details'),
                "status": status.HTTP_404_NOT_FOUND
            },status=status.HTTP_200_OK)
        except Exception as err:
            return Response({
                "message": res_msg.something_else(),
                "status": status.HTTP_204_NO_CONTENT
            },status=status.HTTP_200_OK)
        

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class OrderItemView(APIView):

    def get(self, request, pk=None):
        try:
            order_id_queryset = OrderId.objects.get(order_id=pk)
        except:
            return Response({
                    "message": res_msg.not_exists('Order Id'),
                    "status": status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK)
        try:
            queryset = list(OrderItemDetails.objects.filter(order_id=order_id_queryset.pk).order_by('-id'))
        except:
            return Response({
                "message": res_msg.related_item('Order Items'),
                "status": status.HTTP_201_CREATED
            }, status=status.HTTP_200_OK)

        res_data = []

        for i in queryset:
            order_item_data = {
                "id": i.pk,
                "order_id": i.order_id.order_id,
                "metal": i.metal.pk,
                "metal_name": i.metal.metal_name,
                "purity": i.purity.pk,
                "purity_name": i.purity.purity_name,
                "item": i.item.pk,
                "item_name": i.item.item_name,
                "sub_item": i.sub_item.pk,
                "sub_item_name": i.sub_item.sub_item_name,
                "gross_weight": i.gross_weight,
                "net_weight": i.net_weight,
                "net_weight": i.net_weight,
                "pieces": i.pieces,
                "gender": i.gender.pk,
                "gender_name": i.gender.name,
                "measurement_type": i.measurement_type.pk if i.measurement_type else None,
                "measurement_name": i.measurement_type.measurement_name if i.measurement_type else 'Not Mentioned',
                "measurement_value": i.measurement_value,
                "total_stone_weight": i.total_stone_weight,
                "total_stone_pieces": i.total_stone_pieces,
                "total_stone_amount": i.total_stone_amount,
                "stone_description": i.stone_description,
                "total_diamond_weight": i.total_diamond_weight,
                "total_diamond_pieces": i.total_diamond_pieces,
                "total_diamond_amount": i.total_diamond_amount,
                "diamond_description": i.diamond_description,
                "actual_amount": i.actual_amount,
                "total_amount": i.total_amount,
                "description": i.description,
                "is_assigned": i.is_assigned,
                "assigned_by": i.assigned_by.email if i.assigned_by else None,
                "order_status_name": i.order_status.status_name,
                "order_status_color": i.order_status.color,
            }

            try:
                order_issue_queryset = OrderIssue.objects.get(order_item=i.pk)
                order_item_data["vendor"] = order_issue_queryset.vendor.account_head_name
            except:
                order_item_data["vendor"] = None

            try:
                order_attachments_queryset = list(OrderItemAttachments.objects.filter(order_item=i.pk))
                order_item_data["attachments"] = order_attachments_queryset
            except:
                order_item_data["attachments"] = []

            res_data.append(order_item_data)
        return Response({
            "data": res_data,
            "message": res_msg.retrieve('Order Items'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)


    def post(self, request):
        data = request.data

        created_at = timezone.now()
        created_by = request.user.id

        try:
            order_id_queryset = OrderId.objects.get(order_id=data.get('order_id'))        
        
            total_weight = 0
            approximate_amount = 0
            for i in range(0, int(data.get('quantity', 0))):
                order_item_data = {
                    "order_id": order_id_queryset.pk,
                    "metal": data.get('metal'),
                    "purity": data.get('purity'),
                    "item": data.get('item'),
                    "sub_item": data.get('sub_item'),
                    "gross_weight": data.get('gross_weight'),
                    "net_weight": data.get('net_weight'),
                    "pieces": data.get('quantity'),
                    "metal_rate": data.get('metal_rate'),
                    "gender": data.get('gender'),
                    "measurement_type": data.get('measurement_type'),
                    "measurement_value": data.get('measurement_value'),
                    "total_stone_weight": data.get('total_stone_weight'),
                    "total_stone_pieces": data.get('total_stone_pieces'),
                    "total_stone_amount": data.get('total_stone_amount'),
                    "stone_description": data.get('stone_description'),
                    "total_diamond_weight": data.get('total_diamond_weight'),
                    "total_diamond_pieces": data.get('total_diamond_pieces'),
                    "total_diamond_amount": data.get('total_diamond_amount'),
                    "diamond_description": data.get('diamond_description'),
                    "actual_amount": data.get('actual_amount'),
                    "total_amount": data.get('total_amount'),
                    "description": data.get('description'),
                }

                total_weight += float(data.get('gross_weight', '0'))
                approximate_amount += float(data.get('total_amount'))

                item_serializer = OrderItemDetailsSerializer(data=order_item_data)

                if item_serializer.is_valid():
                    item_serializer.save()
                else:
                    try:
                        queryset = OrderItemDetails.objects.filter(order_id=data.get('order_id'))
                        queryset.delete()
                    except:
                        pass
                    return Response({
                        "data": item_serializer.errors,
                        "message": res_msg.in_valid_fields(),
                        "status": status.HTTP_400_BAD_REQUEST
                    }, status=status.HTTP_200_OK)
                
            try:
                order_detail_queryset = OrderDetails.objects.get(order_id=order_id_queryset.pk)
                order_detail_queryset.total_quantity = order_detail_queryset.total_quantity + int(data.get('quantity', 0))
                order_detail_queryset.total_weight = order_detail_queryset.total_weight + total_weight
                order_detail_queryset.approximate_amount = order_detail_queryset.approximate_amount + approximate_amount
                order_detail_queryset.save()
                
                return Response({
                    "message": data.get("quantity") + " quantity is added",
                    "status": status.HTTP_201_CREATED
                }, status=status.HTTP_200_OK)
            except OrderDetails.DoesNotExist:
                branch = data.get('branch', None) if data.get('branch') else request.user.branch.id

                order_details_data = {
                    "order_id": order_id_queryset.pk,
                    "order_for": data.get('order_for'),
                    "priority": data.get('priority'),
                    "order_date": data.get('order_date'),
                    "no_of_days": data.get('no_of_days'),
                    "due_date": data.get('due_date'),
                    "branch": branch,
                    "customer": data.get('customer'),
                    "customer_name": data.get('customer_name'),
                    "total_quantity": int(data.get('quantity', 0)),
                    "total_weight": total_weight,
                    "approximate_amount": approximate_amount,
                    "created_at": created_at,
                    "created_by": created_by,
                }

                order_details_serializer = OrderDetailsSerializer(data=order_details_data)

                if order_details_serializer.is_valid():
                    order_details_serializer.save()
                else:
                    try:
                        queryset = OrderItemDetails.objects.filter(order_id=data.get('order_id'))
                        queryset.delete()
                    except:
                        pass
                    return Response({
                        "data": order_details_serializer.errors,
                        "message": res_msg.in_valid_fields(),
                        "status": status.HTTP_400_BAD_REQUEST
                    }, status=status.HTTP_200_OK)
                
                return Response({
                    "message": data.get("quantity") + " quantity is added",
                    "status": status.HTTP_201_CREATED
                }, status=status.HTTP_200_OK)
            except Exception as err:
                try:
                    queryset = OrderItemDetails.objects.filter(order_id=data.get('order_id'))
                    queryset.delete()
                except:
                    pass
                return Response({
                    "message": res_msg.something_else(),
                    "status": status.HTTP_204_NO_CONTENT
                },status=status.HTTP_200_OK)
        
        except Exception as err:
            return Response({
                    "message": res_msg.not_exists('Order Id'),
                    "status": status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK)


    @transaction.atomic
    def delete(self, request, pk):
        if pk is None:
            return Response({
                "message": "Please give the order item details!",
                "status": status.HTTP_204_NO_CONTENT
            },status=status.HTTP_200_OK)
        else:
            try:
                queryset = OrderItemDetails.objects.get(id=pk)
                queryset.delete()
                try:
                    order_queryset = OrderDetails.objects.get(order_id=queryset.order_id.pk)

                    order_item_pending_count = OrderItemDetails.objects.filter(order_status=settings.PENDING).count()

                    order_status = settings.PENDING
                    if order_item_pending_count <= 0:
                        order_status = settings.ORDER_ISSUED

                    order_serializer = OrderDetailsSerializer(order_queryset, data= {
                        "approximate_amount": order_queryset.approximate_amount - queryset.total_amount,
                        "total_weight": order_queryset.total_weight - queryset.gross_weight,
                        "total_quantity": order_queryset.total_quantity - 1,
                        "order_status": order_status
                    }, partial=True)

                    if order_serializer.is_valid():
                        order_serializer.save()
                        
                        return Response({
                            "message": res_msg.delete('Item'),
                            "status": status.HTTP_200_OK
                        },status=status.HTTP_200_OK)
                    else:
                        return Response({
                            "data": order_serializer.errors,
                            "message": res_msg.in_valid_fields(),
                            "status": status.HTTP_400_BAD_REQUEST
                        },status=status.HTTP_200_OK)
                except OrderDetails.DoesNotExist:
                    queryset.delete()
                    return Response({
                        "message": res_msg.delete('Item'),
                        "status": status.HTTP_200_OK
                    },status=status.HTTP_200_OK)
                except Exception as err:
                    return Response({
                        "message": res_msg.something_else(),
                        "status": status.HTTP_404_NOT_FOUND
                    },status=status.HTTP_200_OK)
                
            except OrderItemDetails.DoesNotExist:
                return Response({
                    "message": res_msg.not_exists('Order details'),
                    "status": status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK)
            except Exception as err:
                return Response({
                    "message": res_msg.something_else(),
                    "status": status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK)


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class OrderCancelView(APIView):
    def get(self, request, pk=None):

        if pk is None:
            return Response({
                "message": "Please give the order details!",
                "status": status.HTTP_204_NO_CONTENT
            },status=status.HTTP_200_OK)
        else:
            try:
                queryset = OrderDetails.objects.get(id=pk)
                
                order_items_queryset = list(OrderItemDetails.objects.filter(order_id=queryset.order_id.pk))

                check_items = []
                for i in order_items_queryset:
                    if str(i.order_status.pk) == settings.PENDING:
                        check_items.append('1')
                    else:
                        check_items.append('0')

                if '0' in check_items:
                    return Response({
                        "message": "Can't able to put the order cancel",
                        "status": status.HTTP_204_NO_CONTENT
                    },status=status.HTTP_200_OK)

                if settings.CANCELLED == str(queryset.order_status.pk):
                    return Response({
                        "message": "The order is already in a cancelled state",
                        "status": status.HTTP_200_OK
                    },status=status.HTTP_200_OK)
                
                serializer = OrderDetailsSerializer(queryset, data={
                    "order_status": settings.CANCELLED
                }, partial=True)

                if serializer.is_valid():
                    serializer.save()
                    return Response({
                        "message": "The order is cancelled",
                        "status": status.HTTP_200_OK
                    },status=status.HTTP_200_OK)
                else:
                    return Response({
                        "message": res_msg.something_else(),
                        "status": status.HTTP_404_NOT_FOUND
                    },status=status.HTTP_200_OK)
            except OrderDetails.DoesNotExist:
                return Response({
                    "message": res_msg.not_exists('Order details'),
                    "status": status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK)
            except:
                return Response({
                    "message": res_msg.something_else(),
                    "status": status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK)
       

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class OrderListView(APIView):
    def post(self, request):

        search = request.data.get('search') if request.data.get('search') else ''
        order_for = request.data.get('order_for') if request.data.get('order_for') != None else None
        priority = request.data.get('priority') if request.data.get('priority') != None else None
        branch = request.data.get('branch') if request.data.get('branch') != None else None
        page = request.data.get('page') if request.data.get('page') else 1
        items_per_page = request.data.get('items_per_page')
        
        if items_per_page == None:
            order_details_count = OrderDetails.objects.count()

            if order_details_count <= 9:
                items_per_page = 10
            else:
                items_per_page = 10

        filter_condition = {
            "is_order_scheduled": True
        }

        if order_for != None:
           filter_condition['order_for'] = order_for 
        
        if priority != None:
           filter_condition['priority'] = priority

        if request.user.role.is_admin:
            if branch != None:
                filter_condition['branch'] = branch
        else:
            filter_condition['branch'] = request.user.branch.id


        queryset = OrderDetails.objects.filter(Q(order_id__order_id__icontains=search) | Q(customer_name__icontains=search) | Q(customer__phone__icontains=search), **filter_condition).order_by('id')
        
        paginated_data = Paginator(queryset, items_per_page)
        serializer = OrderDetailsSerializer(paginated_data.get_page(page),many=True)

        res_data = []
        for i in range(0, len(serializer.data)):
            res_dict = serializer.data[i]
            res_dict['order_no'] = queryset[i].order_id.order_id
            res_dict['issued_quantity'] = 0
            res_dict['recieved_quantity'] = 0
            res_dict['payment_history'] = []
            res_dict['order_status_name'] = queryset[i].order_status.status_name
            res_dict['order_status_color'] = queryset[i].order_status.color

            order_id = queryset[i].order_id.pk
            try:
                item_queryset = list(OrderItemDetails.objects.filter(order_id=queryset[i].order_id.pk))

                for i in item_queryset:
                    if i.is_recieved:
                        res_dict['recieved_quantity'] += 1

                    if str(i.order_status.pk) == str(settings.ORDER_ISSUED):
                        res_dict['issued_quantity'] += 1
            except:
                res_dict['recieved_quantity'] = 0
            
            try:
                images_queryset = list(OrderItemAttachments.objects.filter(order_id=order_id))
                images_serializer = OrderItemAttachmentsSerializer(images_queryset, many=True)
                res_dict['attachements'] = images_serializer.data
            except:
                res_dict['attachements'] = []

            res_data.append(res_dict)

        return Response({
            "data" : {
                "list": res_data,
                "total_pages": paginated_data.num_pages,
                "current_page": page,
                "total_items": len(queryset),
                "current_items": len(list(paginated_data.get_page(page)))
            },
            "message": res_msg.retrieve('Order'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
    

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class OrderIssueView(APIView):
    
    @transaction.atomic
    def post(self, request):

        data = request.data

        created_at = timezone.now()
        created_by = request.user.id

        try:
            with transaction.atomic():
                try:
                    order_id_queryset = OrderId.objects.get(order_id=data.get('order_id'))
                except:
                    return Response({
                        "message": res_msg.something_else(),
                        "status": status.HTTP_204_NO_CONTENT
                    },status=status.HTTP_200_OK)
                
                for i in data.get('order_items'):
                    queryset = OrderItemDetails.objects.select_for_update().get(id=i)

                    tempData = {
                        "order_id": order_id_queryset.pk,
                        "order_item": i,
                        "vendor": data.get('vendor'),
                        "issue_date": data.get('issue_date'),
                        "no_of_days": data.get('no_of_days'),
                        "remainder_date": data.get('remainder_date'),
                        "created_at": created_at,
                        "created_by": created_by
                    }

                    order_issue_serializer = OrderIssueSerializer(data=tempData)

                    if order_issue_serializer.is_valid():

                        order_item_data = {
                            "is_assigned": True,
                            "assigned_by": data.get('assigned_by'),
                            "order_status": settings.ORDER_ISSUED
                        }

                        order_item_serailizer = OrderItemDetailsSerializer(queryset, data=order_item_data, partial=True)

                        if order_item_serailizer.is_valid():
                            order_item_serailizer.save()
                            order_issue_serializer.save()
                        else:
                            transaction.set_rollback(True)
                            return Response({
                                "data": order_item_serailizer.errors,
                                "message": res_msg.in_valid_fields(),
                                "status": status.HTTP_400_BAD_REQUEST
                            }, status=status.HTTP_200_OK)
                    else:
                        transaction.set_rollback(True)
                        return Response({
                            "data": order_issue_serializer.errors,
                            "message": res_msg.in_valid_fields(),
                            "status": status.HTTP_400_BAD_REQUEST
                        }, status=status.HTTP_200_OK)

                try:
                    order_detail_queryset = OrderDetails.objects.get(order_id=order_id_queryset.pk)

                    update_data = {
                        "is_order_scheduled": True
                    }

                    order_item_pending_count = OrderItemDetails.objects.filter(order_status=settings.PENDING).count()

                    if order_item_pending_count <= 0:
                        update_data['order_status'] = settings.ORDER_ISSUED

                    order_details_serializer = OrderDetailsSerializer(order_detail_queryset, data=update_data, partial=True)

                    if order_details_serializer.is_valid():
                        order_details_serializer.save()
                    else:
                        transaction.set_rollback(True)
                        return Response({
                            "data": order_details_serializer.errors,
                            "message": res_msg.in_valid_fields(),
                            "status": status.HTTP_400_BAD_REQUEST
                        }, status=status.HTTP_200_OK)
                except Exception as err:
                    transaction.set_rollback(True)
                    return Response({
                        "message": "Vendor not assigned",
                        "status": status.HTTP_204_NO_CONTENT
                    }, status=status.HTTP_200_OK)
                
                try:
                    ses_order_id_queryset = SessionOrderId.objects.get(user=request.user.id, ses_order_id=order_id_queryset.pk)
                    ses_order_id_queryset.delete()
                except SessionOrderId.DoesNotExist:
                    pass
                except Exception as err:
                    transaction.set_rollback(True)
                    return Response({
                        "message": "Something wrong in given order id",
                        "status": status.HTTP_204_NO_CONTENT
                    }, status=status.HTTP_200_OK)

                return Response({
                    "message": "Vendor assigned successfully",
                    "status": status.HTTP_201_CREATED
                }, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({
                "data" : str(err),
                "message": res_msg.something_else(),
                "status": status.HTTP_204_NO_CONTENT
            },status=status.HTTP_200_OK)
        

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class RecieveItemView(APIView):
    def post(self, request):

        data = request.data

        try:
            queryset = OrderItemDetails.objects.get(id=data.get('item_id'))

            status_data = {
                "order_status": settings.ORDER_RECEIVED,
                "is_recieved": data.get('status')
            }

            order_item_serailizer = OrderItemDetailsSerializer(queryset, data=status_data, partial=True)

            if order_item_serailizer.is_valid():
                order_item_serailizer.save()

                order_items_queryset = list(OrderItemDetails.objects.filter(order_id=queryset.order_id.pk))

                order_status = settings.ORDER_ISSUED

                validation_list = []
                for item in order_items_queryset:
                    if str(item.order_status.pk) == str(settings.ORDER_RECEIVED):
                        validation_list.append(1)
                    else:
                        validation_list.append(0)

                if 0 in validation_list:
                    order_status = settings.ORDER_ISSUED
                else:
                    order_status = settings.ORDER_RECEIVED

                try:
                    order_queryset = OrderDetails.objects.get(order_id=queryset.order_id.pk)
                    
                    order_serializer = OrderDetailsSerializer(order_queryset, data={
                        "order_status": order_status
                    }, partial=True)

                    if order_serializer.is_valid():
                        order_serializer.save()
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
        except OrderItemDetails.DoesNotExist:
            return Response({
                "message": res_msg.not_exists('Order details'),
                "status": status.HTTP_404_NOT_FOUND
            },status=status.HTTP_200_OK)
        except Exception as err:
            return Response({
                "message": res_msg.something_else(),
                "status": status.HTTP_204_NO_CONTENT
            },status=status.HTTP_200_OK)


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class OrderConvertToLotGetByIDViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk):
        try:
            queryset = OrderDetails.objects.get(id=pk)
        except OrderDetails.DoesNotExist:
                return Response({
                    "message": res_msg.not_exists('Order details'),
                    "status": status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK)
        
        serializer = OrderDetailsSerializer(queryset)

        res_data = serializer.data
        res_data['order_id'] = queryset.order_id.order_id
        
        res_data['particular_list'] = []
        res_data['branch_name'] = queryset.branch.branch_name
        res_data['priority_name'] = queryset.priority.name
        res_data['pending_quantity'] = queryset.total_quantity
        res_data['order_status_name'] = queryset.order_status.status_name
        res_data['order_status_color'] = queryset.order_status.color
        
        
        # if str(queryset.order_for.pk) == str(settings.ORDER_FOR_CUSTOMER):
        res_data['customer_no'] = queryset.customer.phone
        
        item_queryset = list(OrderItemDetails.objects.filter(order_id=queryset.order_id).order_by('-id'))
        for i in item_queryset:
            order_item_data = {
                "id": i.pk,
                "order_id": i.order_id.order_id,
                "metal": i.metal.pk,
                "metal_name": i.metal.metal_name,
                "purity": i.purity.pk,
                "purity_name": i.purity.purity_name,
                "item": i.item.pk,
                "item_name": i.item.item_name,
                "sub_item": i.sub_item.pk,
                "sub_item_name": i.sub_item.sub_item_name,
                "gross_weight": i.gross_weight,
                "net_weight": i.net_weight,
                "metal_rate": i.metal_rate,
                "gender": i.gender.pk,
                "gender_name": i.gender.name,
                "measurement_type": i.measurement_type.pk if i.measurement_type else None,
                "measurement_name": i.measurement_type.measurement_name if i.measurement_type else 'Not Mentioned',
                "measurement_value": i.measurement_value,
                "total_stone_weight": i.total_stone_weight,
                "total_stone_pieces": i.total_stone_pieces,
                "total_stone_amount": i.total_stone_amount,
                "stone_description": i.stone_description,
                "total_diamond_weight": i.total_diamond_weight,
                "total_diamond_pieces": i.total_diamond_pieces,
                "total_diamond_amount": i.total_diamond_amount,
                "diamond_description": i.diamond_description,
                "actual_amount": i.actual_amount,
                "total_amount": i.total_amount,
                "description": i.description,
                "is_assigned": i.is_assigned,
                "is_recieved": i.is_recieved,
                "assigned_by": i.assigned_by.email if i.assigned_by else None,
                "order_status_name": i.order_status.status_name,
                "order_status_color": i.order_status.color,
                "order_status": i.order_status.pk
            }

            try:
                order_issue_queryset = OrderIssue.objects.get(order_item=i.pk)
                order_item_data["vendor"] = order_issue_queryset.vendor.account_head_name
            except:
                order_item_data["vendor"] = None

            try:
                order_attachments_queryset = list(OrderItemAttachments.objects.filter(order_id=i.order_id.order_id, order_item='_'.join(i.item.item_name.split(' '))))
                order_attachments_serializer = OrderItemAttachmentsSerializer(order_attachments_queryset, many=True)
                order_item_data["attachments"] = order_attachments_serializer.data
            except:
                order_item_data["attachments"] = []

            if i.is_recieved:
                order_item_data['pending_quantity'] -= 1

            res_data['particular_list'].append(order_item_data)

        return Response({
            "data" : res_data,
            "message": res_msg.retrieve('Order'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
    


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class OrderReceivedItemListView(APIView):

    def get(self, request, pk=None):
        try:
            order_id_queryset = OrderId.objects.get(order_id=pk)
        except:
            return Response({
                    "message": res_msg.not_exists('Order Id'),
                    "status": status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK)
        try:
            queryset = list(OrderItemDetails.objects.filter(order_id=order_id_queryset.pk,is_recieved=True,is_converted_to_lot=False).order_by('-id'))
        except:
            return Response({
                "message": res_msg.related_item('Order Items'),
                "status": status.HTTP_201_CREATED
            }, status=status.HTTP_200_OK)

        res_data = []

        for i in queryset:
            order_item_data = {
                "id": i.pk,
                "order_id": i.order_id.order_id,
                "metal": i.metal.pk,
                "metal_name": i.metal.metal_name,
                "purity": i.purity.pk,
                "purity_name": i.purity.purity_name,
                "item": i.item.pk,
                "item_name": i.item.item_name,
                "sub_item": i.sub_item.pk,
                "sub_item_name": i.sub_item.sub_item_name,
                "gross_weight": i.gross_weight,
                "net_weight": i.net_weight,
                "net_weight": i.net_weight,
                "pieces": i.pieces,
                "gender": i.gender.pk,
                "gender_name": i.gender.name,
                "measurement_type": i.measurement_type.pk if i.measurement_type else None,
                "measurement_name": i.measurement_type.measurement_name if i.measurement_type else 'Not Mentioned',
                "measurement_value": i.measurement_value,
                "total_stone_weight": i.total_stone_weight,
                "total_stone_pieces": i.total_stone_pieces,
                "total_stone_amount": i.total_stone_amount,
                "stone_description": i.stone_description,
                "total_diamond_weight": i.total_diamond_weight,
                "total_diamond_pieces": i.total_diamond_pieces,
                "total_diamond_amount": i.total_diamond_amount,
                "diamond_description": i.diamond_description,
                "actual_amount": i.actual_amount,
                "total_amount": i.total_amount,
                "description": i.description,
                "is_assigned": i.is_assigned,
                "assigned_by": i.assigned_by.email if i.assigned_by else None,
                "order_status_name": i.order_status.status_name,
                "order_status_color": i.order_status.color,
            }

            try:
                order_issue_queryset = OrderIssue.objects.get(order_item=i.pk)
                order_item_data["vendor"] = order_issue_queryset.vendor.account_head_name
            except:
                order_item_data["vendor"] = None

            try:
                order_attachments_queryset = list(OrderItemAttachments.objects.filter(order_item=i.pk))
                order_item_data["attachments"] = order_attachments_queryset
            except:
                order_item_data["attachments"] = []

            res_data.append(order_item_data)
        return Response({
            "data": res_data,
            "message": res_msg.retrieve('Order Items'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
