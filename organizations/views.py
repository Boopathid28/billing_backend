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
from accounts.serializer import *
from accounts.models import *
from .serializer import *
from django.db.models import Q
from infrastructure.models import Floor
from infrastructure.views import FloorStatus
from django.db.models import Q
from django.conf import settings

res_msg = ResponseMessages()

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class LocationViewSet(viewsets.ViewSet):

    def create(self, request):

        data = request.data
        data['created_at'] = timezone.now()
        data['created_by'] = request.user.id
        serializer = LocationSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": res_msg.create('Location'),
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
            queryset = Location.objects.get(id=pk)
        except Exception as err:
            return Response({
                "message": res_msg.not_exists('Location'),
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_200_OK)
        
        data = request.data
        data['modified_at'] = timezone.now()
        data['modified_by'] = request.user.id
        serializer = LocationSerializer(queryset, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": res_msg.update('Location'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        return Response({
                "data": serializer.errors,
                "message": res_msg.in_valid_fields(),
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_200_OK)
    
    def destroy(self, request, pk):
        try:
            queryset = Location.objects.get(id=pk)
            queryset.delete()
            return Response({
                "message": res_msg.delete('Location'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        except Location.DoesNotExist:
            return Response({
                "message": res_msg.not_exists('Location'),
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
class LocationList(APIView):

    def get(self, request):

        queryset = list(Location.objects.filter(is_active=True).order_by('id'))
        serializer = LocationSerializer(queryset, many=True)

        return Response({
            "data": {
                "list": serializer.data,
            },
            "message": res_msg.retrieve('Location'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
    
    def post(self, request):

        search = request.data.get('search') if request.data.get('search') else ''
        from_date = request.data.get('from_date') if request.data.get('from_date') else None
        to_date = request.data.get('to_date') if request.data.get('to_date') else None
        active_status = request.data.get('active_status') if request.data.get('active_status') != None else None
        page = request.data.get('page') if request.data.get('page') else 1
        items_per_page = request.data.get('items_per_page') if request.data.get('items_per_page') else 10    
        try:
            items_per_page = int(request.data.get('items_per_page', Location.objects.all().count()))
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
                queryset = list(Location.objects.filter(location_name__icontains=search,**filter_condition).order_by('id'))
        elif search != '':
                queryset = list(Location.objects.filter(location_name__icontains=search).order_by('id'))
        else:
                queryset = list(Location.objects.all().order_by('id'))

        paginated_data = Paginator(queryset, items_per_page)
        serializer = LocationSerializer(paginated_data.get_page(page), many=True)
        res_data = []
        
        for i in range(len(serializer.data)):
            try:
                staff = Staff.objects.get(user =queryset[i].created_by)
                username = staff.first_name

            except:
                username = "-"
    
            dict_data = serializer.data[i]
            dict_data['created_by'] = username
            res_data.append(dict_data)

        return Response({
            "data": {
                "list": res_data,
                "total_pages": paginated_data.num_pages,
                "current_page": page,
                "total_items": len(queryset),
                "current_items": len(serializer.data)
            },
            "message": res_msg.retrieve('Location'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class LocationStatus(APIView):

    def get(self, request, pk=None):

        if pk != None:
            try:
                queryset = Location.objects.get(id=pk)
            except Exception as err:
                return Response({
                    "message": res_msg.not_exists('Location'),
                    "status": status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_200_OK)
            
            try:
                branch_queryset = list(Branch.objects.filter(location=pk))

                if not(queryset.is_active) == False:
                    for i in branch_queryset:
                        BranchStatus().get(request, i.pk, not(queryset.is_active))
            except:
                pass
            
        queryset.is_active = not(queryset.is_active)
        queryset.save()

        serializer = LocationSerializer(queryset)

        return Response({
                "data": serializer.data,
                "message": res_msg.update('Location status'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
  

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class BranchViewSet(viewsets.ViewSet):

    def create(self, request):

        data = request.data
        data['created_at'] = timezone.now()
        data['created_by'] = request.user.id
        serializer = BranchSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": res_msg.create('Branch'),
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
            queryset = Branch.objects.get(id=pk)
        except Exception as err:
            return Response({
                "message": res_msg.not_exists('Branch'),
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_200_OK)
        
        data = request.data
        data['modified_at'] = timezone.now()
        data['modified_by'] = request.user.id
        serializer = BranchSerializer(queryset, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": res_msg.update('Branch'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        return Response({
                "data": serializer.errors,
                "message": res_msg.in_valid_fields(),
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_200_OK)
    
    def destroy(self, request, pk):
        try:
            queryset = Branch.objects.get(id=pk)
            queryset.delete()
            return Response({
                "message": res_msg.delete('Branch'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        except Branch.DoesNotExist:
            return Response({
                "message": res_msg.not_exists('Branch'),
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
class BranchList(APIView):

    def get(self, request, location=None):

        if location != None:
            queryset = list(Branch.objects.filter(location=location, is_active=True).order_by('id').values('id', 'branch_name','branch_shortcode'))
        else:
            queryset = list(Branch.objects.filter(is_active=True).order_by('id').values('id', 'branch_name','branch_shortcode'))

        return Response({
            "data": {
                "list": queryset,
            },
            "message": res_msg.retrieve('Branch'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)

    def post(self, request):

        search = request.data.get('search') if request.data.get('search') else ''
        from_date = request.data.get('from_date') if request.data.get('from_date') else None
        to_date = request.data.get('to_date') if request.data.get('to_date') else None
        active_status = request.data.get('active_status') if request.data.get('active_status') != None else None
        page = request.data.get('page') if request.data.get('page') else 1
        try:
            items_per_page = int(request.data.get('items_per_page', Branch.objects.all().count()))
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
                queryset = list(Branch.objects.filter(Q(branch_name__icontains=search)|Q(location__location_name=search),**filter_condition).order_by('id'))
        elif search != '':
                queryset = list(Branch.objects.filter(Q(branch_name__icontains=search)|Q(location__location_name=search)).order_by('id'))
        else:
            queryset = list(Branch.objects.all().order_by('id'))

        paginated_data = Paginator(queryset, items_per_page)
        serializer = BranchSerializer(paginated_data.get_page(page), many=True)

        res_data = []

        for i in range(0, len(serializer.data)):
            dict_data = serializer.data[i]
            try:
                staff = Staff.objects.get(user =queryset[i].created_by)
                username = staff.first_name
            except:
                username = "-"

            dict_data['created_by'] = username
            dict_data['location_name'] = queryset[i].location.location_name

            res_data.append(dict_data)

        return Response({
            "data": {
                "list": res_data,
                "total_pages": paginated_data.num_pages,
                "current_page": page,
                "total_items": len(queryset),
                "current_items": len(serializer.data)
            },
            "message": res_msg.retrieve('Branch'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
       
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class BranchStatus(APIView):

    def get(self, request, pk=None, active=None):

        if pk != None:
            try:
                queryset = Branch.objects.get(id=pk)
            except Exception as err:
                return Response({
                    "message": res_msg.not_exists('Branch'),
                    "status": status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_200_OK)
            
            if not(queryset.is_active):
                try:
                    location_queryset = Location.objects.get(id=queryset.location.pk, is_active=True)
                    pass
                except Location.DoesNotExist:
                    return Response({
                        "message": res_msg.activate(queryset.location.location_name + ' location'),
                        "status": status.HTTP_204_NO_CONTENT
                    }, status=status.HTTP_200_OK)
            else:
                try:
                    staff_queryset = list(Staff.objects.filter(branch=pk))

                
                    for i in staff_queryset:
                        StaffStatus().get(request, i.pk, not(queryset.is_active))
                except:
                    pass

                try:
                    floor_queryset = list(Floor.objects.filter(branch=pk))

                    for i in floor_queryset:
                        FloorStatus().get(request, i.pk, not(queryset.is_active))
                except:
                    pass
            
        queryset.is_active = active if active != None else not(queryset.is_active)
        queryset.save()

        serializer = BranchSerializer(queryset)

        return Response({
                "data": serializer.data,
                "message": res_msg.update('Branch status'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class DepartmentViewSet(viewsets.ViewSet):

    def create(self, request):

        data = request.data
        data['created_at'] = timezone.now()
        data['created_by'] = request.user.id
        serializer = DepartmentSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": res_msg.create('Department'),
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
            queryset = Department.objects.get(id=pk)
        except Exception as err:
            return Response({
                "message": res_msg.not_exists('Department'),
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_200_OK)
        
        data = request.data
        data['modified_at'] = timezone.now()
        data['modified_by'] = request.user.id
        serializer = DepartmentSerializer(queryset, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": res_msg.update('Department'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        return Response({
                "data": serializer.errors,
                "message": res_msg.in_valid_fields(),
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_200_OK)
    
    def destroy(self, request, pk):
        try:
            queryset = Department.objects.get(id=pk)
            queryset.delete()
            return Response({
                "message": res_msg.delete('Department'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        except Department.DoesNotExist:
            return Response({
                "message": res_msg.not_exists('Department'),
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
class DepartmentList(APIView):

    def get(self, request):

        queryset = list(Department.objects.filter(is_active=True).order_by('id'))
        serializer = DepartmentSerializer(queryset, many=True)

        return Response({
            "data": {
                "list": serializer.data,
            },
            "message": res_msg.retrieve('Department'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)

    def post(self, request):

        search = request.data.get('search') if request.data.get('search') else ''
        from_date = request.data.get('from_date') if request.data.get('from_date') else None
        to_date = request.data.get('to_date') if request.data.get('to_date') else None
        active_status = request.data.get('active_status') if request.data.get('active_status') != None else None
        page = request.data.get('page') if request.data.get('page') else 1
        try:
            items_per_page = int(request.data.get('items_per_page', Department.objects.all().count()))
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
            queryset = list(Department.objects.filter(department_name__icontains=search,**filter_condition).order_by('id'))
        elif search != '':
            queryset = list(Department.objects.filter(department_name__icontains=search,**filter_condition).order_by('id'))
        else:
            queryset = list(Department.objects.all().order_by('id'))

        paginated_data = Paginator(queryset, items_per_page)
        serializer = DepartmentSerializer(paginated_data.get_page(page), many=True)

        res_data = []
        
        for i in range(len(serializer.data)):
            
            try :
                staff = Staff.objects.get(user =queryset[i].created_by_id)
                username = staff.first_name
            except:
                username = "-"
            dict_data = serializer.data[i]
            dict_data['created_by'] = username
            res_data.append(dict_data)

        return Response({
            "data": {
                "list": res_data,
                "total_pages": paginated_data.num_pages,
                "current_page": page,
                "total_items": len(queryset),
                "current_items": len(serializer.data)
            },
            "message": res_msg.retrieve('Department'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
     
     
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class DepartmentStatus(APIView):

    def get(self, request, pk=None):

        if pk != None:
            try:
                queryset = Department.objects.get(id=pk)
            except Exception as err:
                return Response({
                    "message": res_msg.not_exists('Department'),
                    "status": status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_200_OK)
            
            try:
                staff_queryset = list(Staff.objects.filter(department=pk))

                if not(queryset.is_active) == False:
                    for i in staff_queryset:
                        StaffStatus().get(request, i.pk, not(queryset.is_active))
            except:
                pass
            
        queryset.is_active = not(queryset.is_active)
        queryset.save()

        serializer = DepartmentSerializer(queryset)

        return Response({
                "data": serializer.data,
                "message": res_msg.update('Department status'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
  
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class DesignationViewSet(viewsets.ViewSet):

    def create(self, request):

        data = request.data
        data['created_at'] = timezone.now()
        data['created_by'] = request.user.id
        serializer = DesignationSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": res_msg.create('Designation'),
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
            queryset = Designation.objects.get(id=pk)
        except Exception as err:
            return Response({
                "message": res_msg.not_exists('Designation'),
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_200_OK)
        
        data = request.data
        data['modified_at'] = timezone.now()
        data['modified_by'] = request.user.id
        serializer = DesignationSerializer(queryset, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": res_msg.update('Designation'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        return Response({
                "data": serializer.errors,
                "message": res_msg.in_valid_fields(),
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_200_OK)
    
    def destroy(self, request, pk):
        try:
            queryset = Designation.objects.get(id=pk)
            queryset.delete()
            return Response({
                "message": res_msg.delete('Designation'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        except Designation.DoesNotExist:
            return Response({
                "message": res_msg.not_exists('Designation'),
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
class DesignationList(APIView):

    def get(self, request):

        queryset = list(Designation.objects.filter(is_active=True).order_by('id'))
        serializer = DesignationSerializer(queryset, many=True)

        return Response({
            "data": {
                "list": serializer.data,
            },
            "message": res_msg.retrieve('Designation'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)

    def post(self, request):

        search = request.data.get('search') if request.data.get('search') else ''
        from_date = request.data.get('from_date') if request.data.get('from_date') else None
        to_date = request.data.get('to_date') if request.data.get('to_date') else None
        active_status = request.data.get('active_status') if request.data.get('active_status') != None else None
        page = request.data.get('page') if request.data.get('page') else 1
        try:
            items_per_page = int(request.data.get('items_per_page', Designation.objects.all().count()))
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
            queryset = list(Designation.objects.filter(designation_name__icontains=search,**filter_condition).order_by('id'))
        elif search != '':
            queryset = list(Designation.objects.filter(designation_name__icontains=search).order_by('id'))
        else:
            queryset = list(Designation.objects.all().order_by('id'))

        paginated_data = Paginator(queryset, items_per_page)
        serializer = DesignationSerializer(paginated_data.get_page(page), many=True)
        res_data = []
        
        for i in range(len(serializer.data)):

            try:
                staff = Staff.objects.get(user =queryset[i].created_by_id)
                username = staff.first_name
            except:
                username = "-"
            dict_data = serializer.data[i]
            dict_data['created_by'] = username
            res_data.append(dict_data)


        return Response({
            "data": {
                "list": res_data,
                "total_pages": paginated_data.num_pages,
                "current_page": page,
                "total_items": len(queryset),
                "current_items": len(serializer.data)
            },
            "message": res_msg.retrieve('Designation'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
        
        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class DesignationStatus(APIView):

    def get(self, request, pk=None):

        if pk != None:
            try:
                queryset = Designation.objects.get(id=pk)
            except Exception as err:
                return Response({
                    "message": res_msg.not_exists('Designation'),
                    "status": status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_200_OK)
            
            try:
                staff_queryset = list(Staff.objects.filter(designation=pk))

                if not(queryset.is_active) == False:
                    for i in staff_queryset:
                        StaffStatus().get(request, i.pk, not(queryset.is_active))
            except:
                pass
            
        queryset.is_active = not(queryset.is_active)
        queryset.save()

        serializer = DesignationSerializer(queryset)

        return Response({
                "data": serializer.data,
                "message": res_msg.update('Designation status'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class StaffViewSet(viewsets.ViewSet):
 
    def retrieve(self, request, pk):
 
        try:
            queryset = Staff.objects.get(id=pk)
        except Exception as err:
            return Response({
                "message": res_msg.not_exists('Staff'),
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_200_OK)
        serializer = StaffSerializer(queryset)
        return Response({
            "data": serializer.data,
            "message": res_msg.retrieve('Staff Details'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
 
    def create(self, request):
 
        data = request.data
        data['created_at'] = timezone.now()
        data['created_by'] = request.user.id
        if request.user.role.is_admin == False:
           data['branch'] = request.user.branch.pk
        def create_staff_id():
            try:
                queryset = Staff.objects.all().last()
                return 'STAFF0000'+str(queryset.pk + 1)
            except Exception as err:
                return 'STAFF00001'
        data['staff_id'] = create_staff_id()
        serializer = StaffSerializer(data=data)
 
        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": res_msg.create('Staff'),
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
            queryset = Staff.objects.get(id=pk)
        except Exception as err:
            return Response({
                "message": res_msg.not_exists('Staff'),
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_200_OK)
        data = request.data
        phone=data.get('phone')
 
        data['modified_at'] = timezone.now()
        data['modified_by'] = request.user.id
        serializer = StaffSerializer(queryset, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            # try:
            #     user_queryset = User.object.get(staff_id=queryset.staff_id)
            #     user_serializer = UserSerializer(user_queryset, data=data, partial=True)
            #     if user_serializer.is_valid():
            #         user_serializer.save()
            # except Exception as err:
            #     pass
            return Response({
                "data": serializer.data,
                "message": res_msg.update('Staff'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        return Response({
                "data": serializer.errors,
                "message": res_msg.in_valid_fields(),
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        try:
            queryset = Staff.objects.get(id=pk)
            queryset.is_deleted = True
            queryset.is_active = False
            queryset.save()
            try:
                user_queryset = User.object.get(staff_id=queryset.staff_id)
                user_queryset.is_deleted = True
                user_queryset.is_active = False
                user_queryset.save()
            except:
                pass
            return Response({
                "message": res_msg.delete('Staff'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        except Staff.DoesNotExist:
            return Response({
                "message": res_msg.not_exists('Staff'),
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
class StaffList(APIView):
 
    def get(self, request):


        branch = request.data.get('branch') if request.data.get('branch') else None
        filter_condition={}
        if request.user.role.is_admin == True:
            if branch != None:            
                filter_condition['branch'] = branch
        else:
            filter_condition['branch'] = request.user.branch.pk
    
        filter_condition['is_active'] = True
        queryset = list(Staff.objects.filter(**filter_condition).order_by('id'))
        serializer = StaffSerializer(queryset, many=True)
 
        return Response({
            "data": {
                "list": serializer.data,
            },
            "message": res_msg.retrieve('Staff'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
 
    def post(self, request):
 
        search = request.data.get('search') if request.data.get('search') else ''
        from_date = request.data.get('from_date') if request.data.get('from_date') else None
        to_date = request.data.get('to_date') if request.data.get('to_date') else None
        active_status = request.data.get('active_status') if request.data.get('active_status') != None else None
        page = request.data.get('page') if request.data.get('page') else 1
        items_per_page = request.data.get('items_per_page') if request.data.get('items_per_page') else 10
        # try:
        #     items_per_page = int(request.data.get('items_per_page', Staff.objects.all().count()))
        #     if items_per_page == 0:
        #         items_per_page = 10 
        # except Exception as err:
        #     items_per_page = 10 
        branch = request.data.get('branch') if request.data.get('branch') else None
        filter_condition={}
        if request.user.role.is_admin == True:
            if branch != None:            
                filter_condition['branch'] = branch

        else:
            filter_condition['branch'] = request.user.branch.pk
 
        
        if active_status != None:
           filter_condition['is_active'] = active_status
 
        if from_date != None and to_date!= None:
           fdate =from_date+'T00:00:00.899010+05:30'
           tdate =to_date+'T23:59:59.899010+05:30'
           date_range=(fdate,tdate)
           filter_condition['created_at__range']=date_range
 
 
        if len(filter_condition) != 0:
           queryset = list(Staff.objects.filter(Q(first_name__icontains=search)|Q(email__icontains=search)|Q(phone__icontains=search),**filter_condition).order_by('id'))
        elif search != '':
           queryset = list(Staff.objects.filter(Q(first_name__icontains=search)|Q(email__icontains=search)|Q(phone__icontains=search)).order_by('id'))
        else:
           queryset=list(Staff.objects.all().order_by('id'))
 
        paginated_data = Paginator(queryset, items_per_page)
        serializer = StaffSerializer(paginated_data.get_page(page), many=True)
        res_data = []
 
        for i in range(0, len(serializer.data)):
            dict_data = serializer.data[i]
 
            try:
                staff = Staff.objects.get(phone =queryset[i].created_by.phone)
                dict_data['created_by'] = staff.first_name
            except:
                dict_data['created_by'] = None
 
            dict_data['branch_name'] = queryset[i].branch.branch_name
 
            res_data.append(dict_data)
 
        return Response({
            "data": {
                "list": res_data,
                "total_pages": paginated_data.num_pages,
                "current_page": page,
                "total_items": len(queryset),
                "current_items": len(serializer.data),
            },
            "message": res_msg.retrieve('Staff'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class StaffStatus(APIView):
 
    def get(self, request, pk=None, active=None):
 
        if pk != None:
            try:
                queryset = Staff.objects.get(id=pk)
            except Exception as err:
                return Response({
                    "message": res_msg.not_exists('Staff'),
                    "status": status.HTTP_404_NOT_FOUND
                }, status=status.HTTP_200_OK)
            if not(queryset.is_active):
                try:
                    location_queryset = Location.objects.get(id=queryset.location.pk, is_active=True)
                    pass
                except Location.DoesNotExist:
                    return Response({
                        "message": res_msg.activate(queryset.location.location_name + ' location'),
                        "status": status.HTTP_204_NO_CONTENT
                    }, status=status.HTTP_200_OK)
                try:
                    branch_queryset = Branch.objects.get(id=queryset.branch.pk, is_active=True)
                    pass
                except Branch.DoesNotExist:
                    return Response({
                        "message": res_msg.activate(queryset.branch.branch_name + ' branch'),
                        "status": status.HTTP_204_NO_CONTENT
                    }, status=status.HTTP_200_OK)
                try:
                    department_queryset = Department.objects.get(id=queryset.department.pk, is_active=True)
                    pass
                except Department.DoesNotExist:
                    return Response({
                        "message": res_msg.activate(queryset.department.department_name + ' department'),
                        "status": status.HTTP_204_NO_CONTENT
                    }, status=status.HTTP_200_OK)
                try:
                    designation_queryset = Designation.objects.get(id=queryset.designation.pk, is_active=True)
                    pass
                except Designation.DoesNotExist:
                    return Response({
                        "message": res_msg.activate(queryset.designation.designation_name + ' designation'),
                        "status": status.HTTP_204_NO_CONTENT
                    }, status=status.HTTP_200_OK)
            else:            
                try:
                    user_queryset = User.object.get(id=queryset.user)
                    user_queryset.is_active = active if active != None else not(queryset.is_active)
                    user_queryset.save()
                except Exception as err:
                    pass
        queryset.is_active = active if active != None else not(queryset.is_active)
        queryset.save()
 
        serializer = StaffSerializer(queryset)
 
        return Response({
                "data": serializer.data,
                "message": res_msg.update('Staff status'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class UserViewSet(viewsets.ViewSet):
 
    def retrieve(self, request, pk):
 
        try:
            queryset = User.object.get(id=pk)
        except Exception as err:
            return Response({
                "message": res_msg.not_exists('User'),
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_200_OK)
        try:
            staff_queryset = Staff.objects.get(user=pk)
        except Exception as err:
            return Response({
                "message": res_msg.not_exists('Staff Details'),
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_200_OK)
        serializer = UserSerializer(queryset)
        staff_serializer = StaffSerializer(staff_queryset)
        return Response({
            "data": {
                'user_details': serializer.data,
                'staff_details': staff_serializer.data
            },
            "message": res_msg.retrieve('User Details'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
 
    def create(self, request):
 
        data = request.data
        data['created_at'] = timezone.now()
        data['created_by'] = request.user.id
        
        valid_email = User.object.filter(email__iexact=data['email'])
 
        if valid_email:
            return Response({
                    "message": res_msg.already_exists('Email'),
                    "status": status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_200_OK)
 
        def create_staff_id():
            try:
                queryset = Staff.objects.all().last()
                return 'STAFF0000'+str(queryset.pk + 1)
            except Exception as err:
                return 'STAFF00001'
        data['staff_id'] = create_staff_id()
        serializer = UserSerializer(data=data)
 
        if serializer.is_valid():
            serializer.save()
            data['user'] = serializer.data['id']
 
            try:
                queryset_user = User.object.get(id=serializer.data['id'])
                queryset_user.set_password(serializer.data['password'])
                queryset_user.save()
            except Exception as error:
                return Response({
                    "message": res_msg.not_create("User"),
                    "status": status.HTTP_403_FORBIDDEN
                }, status=status.HTTP_403_FORBIDDEN)
 
            staff_serializer = StaffSerializer(data=data)
 
            if staff_serializer.is_valid():
                staff_serializer.save()                
                return Response({
                    "data": serializer.data,
                    "message": res_msg.create('User'),
                    "status": status.HTTP_201_CREATED
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "data": staff_serializer.errors,
                    "message": res_msg.in_valid_fields(),
                    "status": status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_200_OK)
        else:
            return Response({
                "data": serializer.errors,
                "message": res_msg.in_valid_fields(),
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_200_OK)
    def update(self, request, pk):
 
        try:
            queryset = User.object.get(id=pk)
        except Exception as err:
            return Response({
                "message": res_msg.not_exists('User'),
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_200_OK)                    
        data = request.data
        data['modified_at'] = timezone.now()
        data['modified_by'] = request.user.id

        serializer = UserSerializer(queryset, data=data, partial=True)
 
        if serializer.is_valid():
            serializer.save()
 
            try:
                queryset = Staff.objects.get(user=pk)
            except Exception as err:
                return Response({
                    "message": res_msg.not_exists('Staff details'),
                    "status": status.HTTP_404_NOT_FOUND
                }, status=status.HTTP_200_OK)
 
            staff_serializer = StaffSerializer(queryset, data=data, partial=True)
 
            if staff_serializer.is_valid():
                staff_serializer.save()
 
                return Response({
                    "data": serializer.data,
                    "message": res_msg.update('User'),
                    "status": status.HTTP_200_OK
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "data": staff_serializer.errors,
                    "message": res_msg.in_valid_fields(),
                    "status": status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_200_OK)
        return Response({
                "data": serializer.errors,
                "message": res_msg.in_valid_fields(),
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        try:
            queryset = User.object.get(id=pk)
            try:
                staff_queryset = Staff.objects.get(user=pk)
                updated_data = {
                 'user':None
                }
                staff_serializer = StaffSerializer(staff_queryset, data=updated_data, partial=True)
                if staff_serializer.is_valid():
                    staff_serializer.save()
            except:
                pass
                # return Response({
                #     "message": res_msg.not_exists('Staff details'),
                #     "status": status.HTTP_404_NOT_FOUND
                # }, status=status.HTTP_200_OK)
            # staff_queryset = Staff.objects.get(user=pk)
            
            queryset.delete()
            return Response({
                "message": res_msg.delete('User'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({
                "message": res_msg.not_exists('User'),
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_200_OK)
        except ProtectedError:
            return Response({
                "message": res_msg.related_item('Delete'),
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({
                "err":str(err),
                "message": res_msg.something_else(),
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_200_OK)
        

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class UserList(APIView):
 
    def get(self, request, branch=None):

        filter_condition={}

        if request.user.role.is_admin == True:
            if branch != None:            
                filter_condition['branch'] = branch
        else:
            filter_condition['branch'] = request.user.branch.pk
        
        filter_condition['is_active'] = True 
        filter_condition['is_superuser'] = False 
        queryset = list(User.object.filter(**filter_condition).order_by('id'))
        serializer = UserSerializer(queryset, many=True)
 
        res_data = []
 
        for i in range(0, len(serializer.data)):
            dict_data = serializer.data[i]
            dict_data['role_name'] = queryset[i].role.role_name
 
            res_data.append(dict_data)
 
        return Response({
            "data": {
                "list": res_data,
            },
            "message": res_msg.retrieve('User'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
    def post(self, request):
 
        search = request.data.get('search') if request.data.get('search') else ''
        from_date = request.data.get('from_date') if request.data.get('from_date') else None
        to_date = request.data.get('to_date') if request.data.get('to_date') else None
        active_status = request.data.get('active_status') if request.data.get('active_status') != None else None
        page = request.data.get('page') if request.data.get('page') else 1
        items_per_page = request.data.get('items_per_page') if request.data.get('items_per_page') else 10
        # try:
        #     items_per_page = int(request.data.get('items_per_page', User.objects.all().count()))
        #     if items_per_page == 0:
        #         items_per_page = 10 
        # except Exception as err:
        #     items_per_page = 10 
        branch = request.data.get('branch') if request.data.get('branch') else None
        filter_condition={}
        if request.user.role.is_admin == True:
            if branch != None:            
                filter_condition['branch'] = branch
        else:
            filter_condition['branch'] = request.user.branch.pk
 
        
        if active_status != None:
           filter_condition['is_active'] = active_status
 
        if from_date != None and to_date!= None:
           fdate =from_date+'T00:00:00.899010+05:30'
           tdate =to_date+'T23:59:59.899010+05:30'
           date_range=(fdate,tdate)
           filter_condition['created_at__range']=date_range
 
        filter_condition['is_superuser'] = False 
        if len(filter_condition) != 0:
           queryset = list(User.object.filter(Q(email__icontains=search)|Q(phone__icontains=search),**filter_condition).order_by('id'))
        elif search != '':
           queryset = list(User.object.filter(Q(email__icontains=search)|Q(phone__icontains=search),**filter_condition).order_by('id'))
        else:
           queryset=list(User.objects.all().order_by('id'))
        paginated_data = Paginator(queryset, items_per_page)
        serializer = UserSerializer(paginated_data.get_page(page), many=True)
 
        res_data = []
 
        for i in range(0, len(serializer.data)):
            dict_data = serializer.data[i]
            try :
                staff = Staff.objects.get(user =queryset[i].created_by)
                username = staff.first_name
            except:
                username = '-'
            dict_data['created_by'] = username
            dict_data['role_name'] = queryset[i].role.role_name
            dict_data['branch_name'] = queryset[i].branch.branch_name
            res_data.append(dict_data)
 
        return Response({
            "data": {
                "list": res_data,
                "total_pages": paginated_data.num_pages,
                "current_page": page,
                "total_items": len(queryset),
                "current_items": len(serializer.data)
            },
            "message": res_msg.retrieve('User'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)

 
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class UserStatus(APIView):
 
    def get(self, request, pk=None, active=None):
 
        if pk != None:
            try:
                queryset = User.object.get(id=pk)
            except Exception as err:
                return Response({
                    "message": res_msg.not_exists('User'),
                    "status": status.HTTP_404_NOT_FOUND
                }, status=status.HTTP_200_OK)

            if not(queryset.is_active):
                try:
                    staff_queryset = Staff.objects.get(user=pk)
                except Exception as err:
                    return Response({
                        "message": res_msg.not_exists('Staff'),
                        "status": status.HTTP_404_NOT_FOUND
                    }, status=status.HTTP_200_OK)
                try:
                    location_queryset = Location.objects.get(id=staff_queryset.location.pk, is_active=True)
                    pass
                except Location.DoesNotExist:
                    return Response({
                        "message": res_msg.activate(staff_queryset.location.location_name + ' location'),
                        "status": status.HTTP_204_NO_CONTENT
                    }, status=status.HTTP_200_OK)
                try:
                    branch_queryset = Branch.objects.get(id=staff_queryset.branch.pk, is_active=True)
                    pass
                except Branch.DoesNotExist:
                    return Response({
                        "message": res_msg.activate(staff_queryset.branch.branch_name + ' branch'),
                        "status": status.HTTP_204_NO_CONTENT
                    }, status=status.HTTP_200_OK)
                try:
                    department_queryset = Department.objects.get(id=staff_queryset.department.pk, is_active=True)
                    pass
                except Department.DoesNotExist:
                    return Response({
                        "message": res_msg.activate(staff_queryset.department.department_name + ' department'),
                        "status": status.HTTP_204_NO_CONTENT
                    }, status=status.HTTP_200_OK)
                try:
                    designation_queryset = Designation.objects.get(id=staff_queryset.designation.pk, is_active=True)
                    pass
                except Designation.DoesNotExist:
                    return Response({
                        "message": res_msg.activate(staff_queryset.designation.designation_name + ' designation'),
                        "status": status.HTTP_204_NO_CONTENT
                    }, status=status.HTTP_200_OK)
                try:
                    user_role_queryset = UserRole.objects.get(id=queryset.role.pk, is_active=True)
                    pass
                except UserRole.DoesNotExist:
                    return Response({
                        "message": res_msg.activate(queryset.role.role_name + ' role'),
                        "status": status.HTTP_204_NO_CONTENT
                    }, status=status.HTTP_200_OK)
            else: 
                try:
                    staff_queryset = Staff.objects.get(user=pk)
                    staff_queryset.is_active = active if active != None else not(queryset.is_active)
                    staff_queryset.save()
                except Exception as err:
                    return Response({
                        "message": res_msg.not_exists('Staff'),
                        "status": status.HTTP_404_NOT_FOUND
                    }, status=status.HTTP_200_OK)
        queryset.is_active = active if active != None else not(queryset.is_active)
        queryset.save()
 
        serializer = UserSerializer(queryset)
 
        return Response({
                "data": serializer.data,
                "message": res_msg.update('Staff status'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)

 
       
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class StaffBranchList(APIView):
 
    def get(self, request,branch=None):

        filter_condition={}

        if request.user.role.is_admin == True:
            if branch != None:            
                filter_condition['branch'] = branch
        else:
            filter_condition['branch'] = request.user.branch.pk
    
 
        filter_condition['is_active'] = True
        queryset = list(Staff.objects.filter(**filter_condition).order_by('id'))
        serializer = StaffSerializer(queryset, many=True)
 
        return Response({
            "data": {
                "list": serializer.data,
            },
            "message": res_msg.retrieve('Staff'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
    
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
class UserListByUserRole(APIView):
 
    def get(self, request, pk=None):

        if pk != None:

            queryset = list(User.object.filter(is_active=True, role=pk).order_by('id'))
            serializer = UserSerializer(queryset, many=True)

            res_data = []

            for i in range(0, len(serializer.data)):
                dict_data = serializer.data[i]
                dict_data['role_name'] = queryset[i].role.role_name

                res_data.append(dict_data)

        return Response({
            "data": {
                "list": res_data,
            },
            "message": res_msg.retrieve('User'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)