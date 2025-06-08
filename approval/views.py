from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.response import Response
from .models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes, authentication_classes
from django.utils import timezone
from django.db.models import ProtectedError
from django.db.models import Q
from django.core.paginator import Paginator
from app_lib.response_messages import ResponseMessages
from .serializer import *
from datetime import datetime

res_msg = ResponseMessages()

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ApprovalTypeViewSet(viewsets.ViewSet):

    def create(self, request):

        data = request.data
        data['created_at'] = timezone.now()
        data['created_by'] = request.user.id
        serializer = ApprovalTypeSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": res_msg.create('Approval Type'),
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
            queryset = ApprovalType.objects.get(id=pk)
        except Exception as err:
            return Response({
                "message": res_msg.not_exists('Approval Type'),
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_200_OK)
        
        data = request.data
        data['modified_at'] = timezone.now()
        data['modified_by'] = request.user.id
        serializer = ApprovalTypeSerializer(queryset, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": res_msg.update('Approval Type'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        return Response({
                "data": serializer.errors,
                "message": res_msg.in_valid_fields(),
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_200_OK)
    
    def destroy(self, request, pk):
        try:
            queryset = ApprovalType.objects.get(id=pk)
            queryset.delete()
            return Response({
                "message": res_msg.delete('Approval Type'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        except ApprovalType.DoesNotExist:
            return Response({
                "message": res_msg.not_exists('Approval Type'),
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
class ApprovalTypeList(APIView):

    def get(self, request):

        queryset = list(ApprovalType.objects.all().order_by('id'))
        serializer = ApprovalTypeSerializer(queryset, many=True)

        return Response({
            "data": {
                "list": serializer.data,
            },
            "message": res_msg.retrieve('ApprovalType'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
    
    def post(self, request):

        search = request.data.get('search') if request.data.get('search') else ''
        from_date = request.data.get('from_date') if request.data.get('from_date') else None
        to_date = request.data.get('to_date') if request.data.get('from_date') else None
        active_status = request.data.get('active_status') if request.data.get('active_status') !=  None else None
        page = request.data.get('page') if request.data.get('page') else 1
        try:
            items_per_page = int(request.data.get('items_per_page', ApprovalType.objects.all().count()))
            if items_per_page == 0:
                items_per_page = 10 
        except Exception as err:
            items_per_page = 10 

        filter_condition={}
    
        if active_status != None:
           filter_condition['is_active'] = active_status 

        if from_date != None and to_date!= None:
           fdate =from_date+'T00:00:00.899010+05:30'
           tdate =to_date+'T23:59:59.899010+05:30'
           date_range=(fdate,tdate)
           filter_condition['created_at__range']=date_range

        if len(filter_condition) != 0:
                queryset = list(ApprovalType.objects.filter(approval_type__icontains=search,**filter_condition).order_by('id'))
        elif search != '':
                queryset = list(ApprovalType.objects.filter(approval_type__icontains=search).order_by('id'))
        else:
            queryset = list(ApprovalType.objects.all().order_by('id'))

        paginated_data = Paginator(queryset, items_per_page)
        serializer = ApprovalTypeSerializer(paginated_data.get_page(page), many=True)

        return Response({
            "data": {
                "list": serializer.data,
                "total_pages": paginated_data.num_pages,
                "current_page": page,
                "total_items": len(queryset),
                "current_items": len(serializer.data)
            },
            "message": res_msg.retrieve('ApprovalType'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ApprovalTypeStatus(APIView):

    def get(self, request, pk=None):

        if pk != None:
            try:
                queryset = ApprovalType.objects.get(id=pk)
            except Exception as err:
                return Response({
                    "message": res_msg.not_exists('Approval Type'),
                    "status": status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_200_OK)
           
            
        queryset.is_active = not(queryset.is_active)
        queryset.save()

        serializer = ApprovalTypeSerializer(queryset)

        return Response({
                "data": serializer.data,
                "message": res_msg.update('Approval Type status'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ApprovalRuleViewSet(viewsets.ViewSet):

    def create(self, request):

        data = request.data
        data['created_at'] = timezone.now()
        data['created_by'] = request.user.id
        serializer = ApprovalRuleSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": res_msg.create('Approval Rule'),
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
            queryset = ApprovalRule.objects.get(id=pk)
        except Exception as err:
            return Response({
                "message": res_msg.not_exists('Approval Rule'),
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_200_OK)
        
        data = request.data
        data['modified_at'] = timezone.now()
        data['modified_by'] = request.user.id
        serializer = ApprovalRuleSerializer(queryset, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": res_msg.update('Approval Rule'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        return Response({
                "data": serializer.errors,
                "message": res_msg.in_valid_fields(),
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_200_OK)
    
    def destroy(self, request, pk):
        try:
            queryset = ApprovalRule.objects.get(id=pk)
            queryset.delete()
            return Response({
                "message": res_msg.delete('Approval Rule'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        except ApprovalRule.DoesNotExist:
            return Response({
                "message": res_msg.not_exists('Approval Rule'),
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
class ApprovalRuleList(APIView):

    def get(self, request):

        queryset = list(ApprovalRule.objects.all().order_by('id'))
        serializer = ApprovalRuleSerializer(queryset, many=True)

        return Response({
            "data": {
                "list": serializer.data,
            },
            "message": res_msg.retrieve('Approval Rule'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
    
    def post(self, request):
        search = request.data.get('search') if request.data.get('search') else ''
        active_status = request.data.get('active_status') if request.data.get('active_status') != None else None
        user_role = request.data.get('user_role') if request.data.get('user_role') else ''
        approve_by = request.data.get('approve_by') if request.data.get('approve_by') else ''
        from_date = request.data.get('from_date') if request.data.get('from_date') else None
        to_date = request.data.get('to_date') if request.data.get('to_date') else None
        page = request.data.get('page') if request.data.get('page') else 1
        try:
            items_per_page = int(request.data.get('items_per_page', ApprovalRule.objects.all().count()))
            if items_per_page == 0:
                items_per_page = 10 
        except Exception as err:
            items_per_page = 10 
            
        filter_condition={}
     

        if from_date != None and to_date!= None:
           fdate =from_date+'T00:00:00.899010+05:30'
           tdate =to_date+'T23:59:59.899010+05:30'
           date_range=(fdate,tdate)
           filter_condition['created_at__range']=date_range

        if len(filter_condition) != 0:
                queryset = list(ApprovalRule.objects.filter(approval_type__approval_type__icontains=search,**filter_condition).order_by('id'))
        elif search != '':
                queryset = list(ApprovalRule.objects.filter(approval_type__approval_type__icontains=search).order_by('id'))
        else:
            queryset = list(ApprovalRule.objects.all().order_by('id'))

        paginated_data = Paginator(queryset, items_per_page)
        serializer = ApprovalRuleSerializer(paginated_data.get_page(page), many=True)

        res_data = []

        for i in range(0, len(serializer.data)):        
            dict_data = serializer.data[i]
            dict_data['approval_type_name'] = queryset[i].approval_type.approval_type
            dict_data['approval_by_name'] = queryset[i].approved_by.email
            dict_data['user_role_name'] = queryset[i].user_role.role_name
            res_data.append(dict_data)

        return Response({
            "data": {
                "list": res_data,
                "total_pages": paginated_data.num_pages,
                "current_page": page,
                "total_items": len(queryset),
                "current_items": len(res_data)
                
            },
            "message": res_msg.retrieve('Approval Rule'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ApprovalRuleStatus(APIView):

    def get(self, request, pk=None):

        if pk != None:
            try:
                queryset = ApprovalRule.objects.get(id=pk)
            except Exception as err:
                return Response({
                    "message": res_msg.not_exists('Approval Rule'),
                    "status": status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_200_OK)
           
            
        queryset.is_active = not(queryset.is_active)
        queryset.save()

        serializer = ApprovalRuleSerializer(queryset)

        return Response({
                "data": serializer.data,
                "message": res_msg.update('Approval Rule status'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)