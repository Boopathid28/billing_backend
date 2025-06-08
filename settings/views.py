from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .models import *
from billing.models import *
from books.models import *
from product.models import *
from django.db import connection,IntegrityError,transaction
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.test import APIRequestFactory
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
from advance_payment.models import *
from approval.models import *
from organizations.models import *
from tagging.models import *
from order_management.models import *
from repair_management.models import *
from payment_management.models import *
from organizations.views import UserViewSet
from django.urls import reverse
import requests
import json
from django.db.models import Q
from django.conf import settings

res_msg = ResponseMessages()

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class UserRoleViewSet(viewsets.ViewSet):
    def create(self, request):

        data = request.data
        data['role_name'] = data.get('role_name').lower()
        data['created_at'] = timezone.now()
        serializer = UserRoleSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": res_msg.create('User role'),
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
            queryset = UserRole.objects.get(id=pk, is_active=True)
        except Exception as err:
            return Response({
                "message": res_msg.not_exists('User role'),
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_200_OK)
        
        data = request.data
        data['role_name'] = data.get('role_name').lower()
        data['modified_at'] = timezone.now()
        serializer = UserRoleSerializer(queryset, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": res_msg.update('User role'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        return Response({
                "data": serializer.errors,
                "message": res_msg.in_valid_fields(),
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_200_OK)
    
    def destroy(self, request, pk):
        try:
            queryset = UserRole.objects.get(id=pk)
            queryset.delete()
            return Response({
                "message": res_msg.delete('User role'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        except UserRole.DoesNotExist:
            return Response({
                "message": res_msg.not_exists('User role'),
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
class UserRoleAdminStatus(APIView):
    def get(self,request,pk):

        try:

            queryset = UserRole.objects.get(id=pk)

            queryset.is_admin = not(queryset.is_admin)

            queryset.save()

            return Response(
                {
                    "message":res_msg.change("Admin Status"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )

        except Exception as err:

            return Response(
                {
                    "message":res_msg.not_exists("User Role"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class UserRolesList(APIView):

    def get(self, request):

        permission_exclude_list = []

        if request.user.role.pk == settings.ADMIN:
            permission_exclude_list = settings.USER_CREATION_ADMIN
        elif request.user.role.pk == settings.BRANCH_ADMIN:
            permission_exclude_list = settings.USER_CREATION_BRANCH_ADMIN

        role_exclude_of = [role for role in permission_exclude_list]

        queryset = list(UserRole.objects.filter(is_active=True).order_by('id').exclude(id__in=role_exclude_of))
        serializer = UserRoleSerializer(queryset, many=True)

        return Response({
            "data": {
                "list": serializer.data,
            },
            "message": res_msg.retrieve('User role'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)

    def post(self, request):

        search = request.data.get('search') if request.data.get('search') else ''
        from_date = request.data.get('from_date') if request.data.get('from_date') else None
        to_date = request.data.get('to_date') if request.data.get('to_date') else None
        active_status = request.data.get('active_status') if request.data.get('active_status') != None else None
        page = request.data.get('page') if request.data.get('page') else 1
        items_per_page = request.data.get('items_per_page') if request.data.get('items_per_page') else UserRole.objects.all().count()
        
        filter_condition={}
    
        if active_status != None:
           filter_condition['is_active'] = active_status 

        if from_date != None and to_date!= None:
           fdate =from_date+'T00:00:00.899010+05:30'
           tdate =to_date+'T23:59:59.899010+05:30'
           date_range=(fdate,tdate)
           filter_condition['created_at__range']=date_range

        if len(filter_condition) != 0:
            queryset = list(UserRole.objects.filter(role_name__icontains=search,**filter_condition).order_by('id'))
        elif search != '':
            queryset = list(UserRole.objects.filter(role_name__icontains=search).order_by('id'))
        else:
            queryset = list(UserRole.objects.all().order_by('id'))

        paginated_data = Paginator(queryset, items_per_page)
        serializer = UserRoleSerializer(paginated_data.get_page(page), many=True)

        return Response({
            "data": {
                "list": serializer.data,
                "total_pages": paginated_data.num_pages,
                "current_page": page,
                "total_items": len(queryset),
                "current_items": len(serializer.data)
            },
            "message": res_msg.retrieve('User role'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class UserRolesStatus(APIView):

    def get(self, request, pk=None):

        if pk != None:
            try:
                queryset = UserRole.objects.get(id=pk)
            except Exception as err:
                return Response({
                    "message": res_msg.not_exists('User role'),
                    "status": status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_200_OK)
            
            try:
                user_queryset = list(User.object.filter(role=pk))

                if not(queryset.is_active) == False:
                    for i in user_queryset:
                        i.is_loggedin = False
                        i.is_active = not(queryset.is_active)
                        i.save()
            except Exception as err:
                pass

            try:
                permission_queryset = list(MenuPermission.objects.filter(user_role=pk))
                for i in permission_queryset:
                    i.view_permit = False
                    i.add_permit = False
                    i.edit_permit = False
                    i.delete_permit = False
                    i.save()
            except:
                return Response({
                    "message": "Error while changing the menu permission",
                    "status": status.HTTP_200_OK
                }, status=status.HTTP_200_OK)

        queryset.is_active = not(queryset.is_active)
        queryset.save()

        serializer = UserRoleSerializer(queryset)

        return Response({
                "data": serializer.data,
                "message": res_msg.update('User role status'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
    

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class MenuGroupViewSet(viewsets.ViewSet):

    def create(self, request):

        data = request.data
        data['menu_group_name'] = data.get('menu_group_name').lower()
        data['created_at'] = timezone.now()
        data['created_by'] = request.user.id
        serializer = MenuGroupSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                "data": serializer.data,
                "message": res_msg.create('Menu Group'),
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
            queryset = MenuGroup.objects.get(id=pk)
        except Exception as err:
            return Response({
                "message": res_msg.not_exists('Menu Group'),
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_200_OK)
        
        data = request.data
        new_data = {}
        
        if bool(request.FILES.get('icon', False)) == True:
            new_data['icon'] = request.FILES['icon']

        new_data['menu_group_name'] = data.get('menu_group_name').lower()
        new_data['modified_at'] = timezone.now()
        new_data['modified_by'] = request.user.id
        serializer = MenuGroupSerializer(queryset, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": res_msg.update('Menu Group'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        return Response({
                "data": serializer.errors,
                "message": res_msg.in_valid_fields(),
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_200_OK)
    
    def destroy(self, request, pk):
        try:
            queryset = MenuGroup.objects.get(id=pk)
            queryset.delete()
            return Response({
                "message": res_msg.delete('Menu Group'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        except UserRole.DoesNotExist:
            return Response({
                "message": res_msg.not_exists('Menu Group'),
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
class MenuGroupList(APIView):

    def get(self, request, main_menu=None):

        if main_menu:
            queryset = list(MenuGroup.objects.filter(is_active=True,main_menu_group=main_menu).order_by('id').values('id','menu_group_name'))
        else:
            queryset = list(MenuGroup.objects.filter(is_active=True).order_by('id').values('id','menu_group_name'))
        
        return Response({
            "data": {
                "list": queryset,
            },
            "message": res_msg.retrieve('Menu Group'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
    
    def post(self, request):
       
        search = request.data.get('search') if request.data.get('search') else ''
        from_date = request.data.get('from_date') if request.data.get('from_date') else None
        to_date = request.data.get('to_date') if request.data.get('to_date') else None
        active_status = request.data.get('active_status') if request.data.get('active_status') != None else None
        page = request.data.get('page') if request.data.get('page') else 1
        items_per_page = request.data.get('items_per_page') if request.data.get('items_per_page') else MenuGroup.objects.all().count()

        filter_condition={}
    
        if active_status != None:
           filter_condition['is_active'] = active_status 

        if from_date != None and to_date!= None:
           fdate =from_date+'T00:00:00.899010+05:30'
           tdate =to_date+'T23:59:59.899010+05:30'
           date_range=(fdate,tdate)
           filter_condition['created_at__range']=date_range

        if len(filter_condition) != 0:
            queryset = list(MenuGroup.objects.filter(menu_group_name__icontains=search,**filter_condition).order_by('id'))
        elif search != '':
            queryset = list(MenuGroup.objects.filter(menu_group_name__icontains=search).order_by('id'))
        else:
            queryset = list(MenuGroup.objects.all().order_by('id'))

        paginated_data = Paginator(queryset, items_per_page)
        serializer = MenuGroupSerializer(paginated_data.get_page(page), many=True)

        return Response({
            "data": {
                "list": serializer.data,
                "total_pages": paginated_data.num_pages,
                "current_page": page,
                "total_items": len(queryset),
                "current_items": len(serializer.data)
            },
            "message": res_msg.retrieve('Menu Group'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
    

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class MenuGroupStatus(APIView):

    def get(self, request, pk=None):

        if pk != None:
            try:
                queryset = MenuGroup.objects.get(id=pk)
            except Exception as err:
                return Response({
                    "message": res_msg.not_exists('Menu Group'),
                    "status": status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_200_OK)
            
            try:
                menu_queryset = list(Menu.objects.filter(menu_group=pk))

                if not(queryset.is_active) == False:
                    for i in menu_queryset:
                        i.is_active = not(queryset.is_active)
                        i.save()

                        try:
                            permission_queryset = list(MenuPermission.objects.filter(menu=i.pk))
                            
                            for i in permission_queryset:
                                i.view_permit = False
                                i.add_permit = False
                                i.edit_permit = False
                                i.delete_permit = False
                                i.save()
                        except:
                            return Response({
                                "message": "Error while changing the menu permission",
                                "status": status.HTTP_200_OK
                            }, status=status.HTTP_200_OK)
            except Exception as err:
                pass

        queryset.is_active = not(queryset.is_active)
        queryset.save()

        serializer = MenuGroupSerializer(queryset)

        return Response({
                "data": serializer.data,
                "message": res_msg.update('Menu Group status'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class MenuViewSet(viewsets.ViewSet):

    def create(self, request):

        data = request.data
        data['menu_name'] = data.get('menu_name').lower()
        data['created_at'] = timezone.now()
        data['created_by'] = request.user.id

        # try:
        #     menu_group_queryset = MenuGroup.objects.get(id=data.get('menu_group'))
        #     menu_group_split = menu_group_queryset.menu_group_name.lower().split(' ')
        #     menu_split = data.get('menu_name').lower().split(' ')
        #     data['menu_path'] = "/" + '-'.join(menu_group_split) + "/" + '-'.join(menu_split)
        # except Exception as err:
        #     return Response({
        #         "message": res_msg.not_exists('Menu Group'),
        #         "status": status.HTTP_404_NOT_FOUND
        #     }, status=status.HTTP_200_OK)
        
        serializer = MenuSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                    "data": serializer.data,
                    "message": res_msg.create('Menu'),
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
            queryset = Menu.objects.get(id=pk)
        except Exception as err:
            return Response({
                "message": res_msg.not_exists('Menu'),
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_200_OK)
        
        data = request.data

        new_data = {}
        print(request.data)
        
        if bool(request.FILES.get('icon', False)) == True:
            new_data['icon'] = request.FILES['icon']

        new_data['menu_name'] = data.get('menu_name').lower()
        new_data['modified_at'] = timezone.now()
        new_data['menu_path'] = data.get('menu_path')
        new_data['modified_by'] = request.user.id

        # try:
        #     menu_group_queryset = MenuGroup.objects.get(id=data.get('menu_group'))
        #     menu_group_split = menu_group_queryset.menu_group_name.lower().split(' ')
        #     menu_split = data.get('menu_name').lower().split(' ')
        #     new_data['menu_path'] = "/" + '-'.join(menu_group_split) + "/" + '-'.join(menu_split)
        # except Exception as err:
        #     return Response({
        #         "message": res_msg.not_exists('Menu Group'),
        #         "status": status.HTTP_404_NOT_FOUND
        #     }, status=status.HTTP_200_OK)
        
        serializer = MenuSerializer(queryset, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": res_msg.update('Menu Group'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        return Response({
                "data": serializer.errors,
                "message": res_msg.in_valid_fields(),
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_200_OK)
    
    def destroy(self, request, pk):
        try:
            queryset = Menu.objects.get(id=pk)
            queryset.delete()
            return Response({
                "message": res_msg.delete('Menu'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        except UserRole.DoesNotExist:
            return Response({
                "message": res_msg.not_exists('Menu'),
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
class MenuList(APIView):

    def get(self, request,menu_group=None):

        if menu_group != None:
            queryset = Menu.objects.filter(menu_group=menu_group).order_by('id')
        else:
            queryset = Menu.objects.all().order_by('id')

        serializer = MenuSerializer(queryset, many=True)

        res_data = []
        for i in range(0,len(serializer.data)):
            dict_data = serializer.data[i]
            dict_data['menu_group_name'] = queryset[i].menu_group.menu_group_name

            res_data.append(dict_data)

        return Response({
            "data": {
                "list": res_data,
            },
            "message": res_msg.retrieve('Menu'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
    
    def post(self, request):

        search = request.data.get('search') if request.data.get('search') else ''
        from_date = request.data.get('from_date') if request.data.get('from_date') else None
        to_date = request.data.get('to_date') if request.data.get('to_date') else None 
        active_status = request.data.get('active_status') if request.data.get('active_status') != None else None
        page = request.data.get('page') if request.data.get('page') else 1
        items_per_page = request.data.get('items_per_page') if request.data.get('items_per_page') else Menu.objects.all().count()
        
        filter_condition={}
    
        if active_status != None:
           filter_condition['is_active'] = active_status 

        if from_date != None and to_date!= None:
           fdate =from_date+'T00:00:00.899010+05:30'
           tdate =to_date+'T23:59:59.899010+05:30'
           date_range=(fdate,tdate)
           filter_condition['created_at__range']=date_range

        if len(filter_condition) != 0:
            queryset = list(Menu.objects.filter(Q(menu_name__icontains=search) | Q(menu_group__menu_group_name__icontains=search),**filter_condition).order_by('id'))
        elif search != '':
            queryset = list(Menu.objects.filter(Q(menu_name__icontains=search) | Q(menu_group__menu_group_name__icontains=search)).order_by('id'))
        else:
            queryset = list(Menu.objects.all().order_by('id'))

        paginated_data = Paginator(queryset, items_per_page)
        serializer = MenuSerializer(paginated_data.get_page(page), many=True)

        res_data = []
        for i in range(0, len(serializer.data)):
            dict_data = serializer.data[i]
            dict_data['menu_group_name'] = queryset[i].menu_group.menu_group_name
        
            res_data.append(dict_data)

        return Response({
            "data": {
               "list": serializer.data,
                "total_pages": paginated_data.num_pages,
                "current_page": page,
                "total_items": len(queryset),
                "current_items": len(serializer.data)
            },
            "message": res_msg.retrieve('Menu'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class MenuStatus(APIView):

    def get(self, request, pk=None):

        if pk != None:
            try:
                queryset = Menu.objects.get(id=pk)
            except:
                return Response({
                    "message": res_msg.not_exists('Menu'),
                    "status": status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_200_OK)

            if not(queryset.is_active):
        
                try:
                    menu_group_queryset = MenuGroup.objects.get(id=queryset.menu_group.pk, is_active=True)
                    pass
                except MenuGroup.DoesNotExist:
                    return Response({
                        "message": res_msg.activate(queryset.menu_group.menu_group_name + ' menu group'),
                        "status": status.HTTP_204_NO_CONTENT
                    }, status=status.HTTP_200_OK)
            
            try:
                permission_queryset = list(MenuPermission.objects.filter(menu=pk))
                
                for i in permission_queryset:
                    i.view_permit = False
                    i.add_permit = False
                    i.edit_permit = False
                    i.delete_permit = False
                    i.save()
            except:
                return Response({
                    "message": "Error while changing the menu permission",
                    "status": status.HTTP_200_OK
                }, status=status.HTTP_200_OK)

        queryset.is_active = not(queryset.is_active)
        queryset.save()

        serializer = MenuSerializer(queryset)

        return Response({
                "data": serializer.data,
                "message": res_msg.update('Menu status'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class MenuPermissionView(APIView):

    def get(self, request, pk):
        if pk == None:
            return Response({
                        "message": "Role ID required for retrieving menu permissions",
                        "status": status.HTTP_403_FORBIDDEN
                    }, status=status.HTTP_200_OK)
        else:

            menu_queryset = list(Menu.objects.all())
            
            menu_list = []
            for menu in menu_queryset:

                if menu.is_active == True:

                    try:
                        queryset = MenuPermission.objects.get(user_role=pk, menu=menu.pk)

                        menu_dict = {}
                        menu_dict['menu_id'] = menu.pk
                        # menu_dict['menu_icon'] = menu.icon
                        menu_dict['menu_name'] = menu.menu_name
                        menu_dict['menu_path'] = menu.menu_path
                        menu_dict['menu_group'] = menu.menu_group.pk
                        menu_dict['view_permit'] = queryset.view_permit
                        menu_dict['add_permit'] = queryset.add_permit
                        menu_dict['edit_permit'] = queryset.edit_permit
                        menu_dict['delete_permit'] = queryset.delete_permit

                        menu_list.append(menu_dict)
                    except:
                        menu_dict = {}
                        menu_dict['menu_id'] = menu.pk
                        # menu_dict['menu_icon'] = menu.icon
                        menu_dict['menu_name'] = menu.menu_name
                        menu_dict['menu_path'] = menu.menu_path
                        menu_dict['menu_group'] = menu.menu_group.pk
                        menu_dict['view_permit'] = False
                        menu_dict['add_permit'] = False
                        menu_dict['edit_permit'] = False
                        menu_dict['delete_permit'] = False
                        
                        menu_list.append(menu_dict)
                    
            
            menu_group_queryset = list(MenuGroup.objects.filter(is_active=True))

            res_data = []

            for group in menu_group_queryset:
                group_dict = {}
                group_dict['menu_group_name'] = group.menu_group_name
                # group_dict['menu_group_icon'] = group.icon
                group_dict['menu_list'] = []
            
                for i in menu_list:

                    if i['menu_group'] == group.pk:
                        menu_dict = {}
                        menu_dict['menu_id'] = i['menu_id']
                        # menu_dict['menu_icon'] = i['menu_icon']
                        menu_dict['menu_name'] = i['menu_name']
                        menu_dict['menu_path'] = i['menu_path']
                        menu_dict['view_permit'] = i['view_permit']
                        menu_dict['add_permit'] = i['add_permit']
                        menu_dict['edit_permit'] = i['edit_permit']
                        menu_dict['delete_permit'] = i['delete_permit']
                        
                        group_dict['menu_list'].append(menu_dict)

                if len(group_dict['menu_list']) != 0:
                    res_data.append(group_dict)

            return Response({
                "data": res_data,
                "message": res_msg.retrieve('Menu Permission'),
                "status": status.HTTP_200_OK
                }, status=status.HTTP_200_OK)

    def post(self, request):

        data = request.data

        try:
            menu_permission_queryset = MenuPermission.objects.get(user_role=data.get('user_role'), menu=data.get('menu'))
            data['modified_at'] = timezone.now()

            serializer = MenuPermissionSerializer(menu_permission_queryset, data=data, partial=True)

            if serializer.is_valid():
                serializer.save()
            else:
                return Response({
                    "message": res_msg.in_valid_fields(),
                    "status": status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_200_OK)

        except Exception as err:
            data['created_at'] = timezone.now()
            data['created_by'] = request.user.id

            serializer = MenuPermissionSerializer(data=data)

            if serializer.is_valid():
                serializer.save()

            else:
                return Response({
                    "message": res_msg.in_valid_fields(),
                    "status": status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_200_OK)
        
        serializer_data = serializer.data

        response_data = {
            "data": serializer_data,
            "message": res_msg.change('Permission'),
            "status": status.HTTP_200_OK
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ActiveUserMenuPermissionView(APIView):
    
    def get(self, request):
        if settings.UNDER_MAINTANENCE:
            return Response({
                "data": [],
                "maintanance": True,
                "message": res_msg.retrieve('Permissions'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        try:
            queryset = list(MenuPermission.objects.filter(user_role=request.user.role))
        except Exception as err:
            return Response({
                    "message": "Error, While retrieving menu permissions",
                    "status": status.HTTP_403_FORBIDDEN
                }, status=status.HTTP_200_OK)
        
        menu_group_queryset = list(MenuGroup.objects.filter(is_active=True))
        res_data = []
        for group in menu_group_queryset:
            group_dict = {}
            group_dict['id'] = group.pk
            group_dict['menu_group_name'] = group.menu_group_name
            group_dict['menu_group_icon'] = group.icon
        
        for i in queryset:
            if i.menu.is_active and i.view_permit:
                menu_dict = {}
                menu_dict['menu_id'] = i.pk
                # menu_dict['menu_icon'] = i.menu.icon
                menu_dict['menu_name'] = i.menu.menu_name
                menu_dict['menu_path'] = i.menu.menu_path
                menu_dict['view_permit'] = i.view_permit
                menu_dict['add_permit'] = i.add_permit
                menu_dict['edit_permit'] = i.edit_permit
                menu_dict['delete_permit'] = i.delete_permit
                
                res_data.append(menu_dict)


        return Response({
            "data": res_data,
            "maintanance": False,
            "message": res_msg.retrieve('Permissions'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class GstVerificationView(APIView):
 
    def get(self, request, gst=""):
        if len(gst) == 0:
            return Response({
                "message": "Enter the GST No",
                "status": status.HTTP_400_BAD_REQUEST
            },  status = status.HTTP_200_OK)
       
        response_API = requests.get('https://razorpay.com/api/gstin/'+gst)

        if response_API.status_code == 200:
            data = json.loads(response_API.text)
            res_msg = {
                "gst_no": data['enrichment_details']['online_provider']['details']['gstin']['value'],
                "gst_status": data['enrichment_details']['online_provider']['details']['status']['value'],
                "tax_payer_type": data['enrichment_details']['online_provider']['details']['tax_payer_type']['value'],
                "registered_name": data['enrichment_details']['online_provider']['details']['legal_name']['value'],
                "bussiness_type": data['enrichment_details']['online_provider']['details']['constitution']['value']
               
            }
            return Response({
                "data": res_msg,
                "message": "Data retrieve successfully",
                "status": status.HTTP_200_OK
            }, status = status.HTTP_200_OK)
        else:
            data = json.loads(response_API.text)
            return Response({
                "message": data.get('error_description'),
                "status": status.HTTP_204_NO_CONTENT
            }, status = status.HTTP_200_OK)
        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class IFSCVerificationView(APIView):
 
    def get(self, request, ifsc=""):
        if len(ifsc) == 0:
            return Response({
                "message": "Enter the IFSC No",
                "status": status.HTTP_400_BAD_REQUEST
            },  status = status.HTTP_200_OK)
       
        response_API = requests.get('https://ifsc.razorpay.com/'+ifsc)
        if response_API.status_code == 200:
            data = json.loads(response_API.text)
            res_msg = {
                "ifsc": data['IFSC'],
                "bank_name": data['BANK'],
                "branch_name": data['BRANCH'],
                "micr_code": data['MICR'],
 
            }
            return Response({
                "data": res_msg,
                "message": "Data retrieve successfully",
                "status": status.HTTP_200_OK
            }, status = status.HTTP_200_OK)
        else:
            data = json.loads(response_API.text)
            return Response({
                "message": data,
                "status": status.HTTP_404_NOT_FOUND
            }, status = status.HTTP_200_OK)
        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class StatusLiView(APIView):

    def get(self,request,pk):

        queryset=list(StatusTable.objects.filter(module=pk).order_by('id').values('id','status_name','color'))

        return Response(
            {
                "data":{
                    "list":queryset
                },
                "message":res_msg.retrieve("Status"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
    
     
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class PaymentModeView(APIView):

    def get(self,request,pk):

        queryset=list(PaymentMode.objects.filter(module=pk).order_by('id').values('id','mode_name','short_code','color'))

        return Response(
            {
                "data":{
                    "list":queryset
                },
                "message":res_msg.retrieve("Payment Mode"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class PaymentStatusView(APIView):

    def get(self,request):

        queryset=list(PaymentStatus.objects.all().order_by('id').values('id','status_name','color'))

        return Response(
            {
                "data":{
                    "list":queryset
                },
                "message":res_msg.retrieve("Payment Mode"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
    

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class SaleReturnPolicyView(APIView):
    def post(self,request):

        request_data = request.data
        request_data['created_at']=timezone.now()
        request_data['created_by']=request.user.id

        serializer = SaleReturnPolicySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "data":serializer.data,
                    "message":res_msg.create("Return Policy"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    "data":serializer.errors,
                    "message":res_msg.not_create("Return Policy"),
                    "status":status.HTTP_400_BAD_REQUEST
                },status=status.HTTP_200_OK
            )
        
    def get(self,request):

        try:

            queryset = SaleReturnPolicy.objects.all().last()

            return Response(
                {
                    "data":queryset.return_days,
                    "message":res_msg.retrieve("Return Policy"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        
        except Exception as err:

            return Response(
                {
                    "data":0,
                    "message":res_msg.retrieve("Return Policy"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class AdminSecret(APIView):

    def post(self,request):

        secret=request.data.get('secret')

        if int(secret) == int(settings.ADMIN_SECRET):

            return Response(
                {
                    "authenticated":True,
                    "message":res_msg.login("Verified"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        
        else:

            return Response(
                {
                    "message":"Access Denied",
                    "status":status.HTTP_401_UNAUTHORIZED
                },status=status.HTTP_401_UNAUTHORIZED
            )
        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class GendersList(APIView):

    def get(self, request):

        queryset = list(Gender.objects.filter(is_active=True).order_by('id'))
        serializer = GenderSerializer(queryset, many=True)

        return Response({
            "data": {
                "list": serializer.data,
            },
            "message": res_msg.retrieve('Gender'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class GendersList(APIView):

    def get(self, request):

        queryset = list(Gender.objects.filter(is_active=True).order_by('id'))
        serializer = GenderSerializer(queryset, many=True)

        return Response({
            "data": {
                "list": serializer.data,
            },
            "message": res_msg.retrieve('Gender'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class PrintList(APIView):

    def get(self, request):

        queryset = PrintModule.objects.all().order_by('id')
        serializer = PrintModuleSerializer(queryset, many=True)

        return Response({
            "data": {
                "list": serializer.data,
            },
            "message": res_msg.retrieve('Print Options'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
        

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class PrintStatusChange(APIView):

    def get(self, request, pk=None):

        if pk != None:
            try:
                queryset = PrintModule.objects.get(id=pk)
            except Exception as err:
                return Response({
                    "message": res_msg.not_exists('Print Module'),
                    "status": status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_200_OK)
                    
        estimation_is_a4 = request.data.get('estimation_is_a4')
        billing_is_a4 = request.data.get('billing_is_a4')
        billing_backup_is_a4 = request.data.get('billing_backup_is_a4')
        order_is_a4 = request.data.get('order_is_a4')
        repair_is_a4 = request.data.get('repair_is_a4')

        queryset.estimation_is_a4 = estimation_is_a4
        queryset.billing_is_a4 = billing_is_a4
        queryset.billing_backup_is_a4 = billing_backup_is_a4
        queryset.order_is_a4 = order_is_a4
        queryset.repair_is_a4 = repair_is_a4
        queryset.save()
        
        serializer = PrintModuleSerializer(queryset)

        return Response({
                "data": serializer.data,
                "message": res_msg.update('Print status'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
    

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class DataInjectionView(APIView):
    def post(self,request):
        bill_Type =[{"bill_type" : "gold"},{"bill_type" : "silver"}]
        account_Type =[{"account_type_name" : "Personal"},{"account_type_name" : "Nominal"},{"account_type_name" : "Real"}]
        customer_Type =[{"customer_type_name" : "Customer"},{"customer_type_name" : "Retailer"},{"customer_type_name" : "Smith"},{"customer_type_name" : "Designer"},{"customer_type_name" : "Vip Customer"},{"customer_type_name" : "Vip Retailer"}]
        group_Ledger =[{"group_ledger_name" : "Profit & Loss"},{"group_ledger_name" : "Balance Sheet"},{"group_ledger_name" : "Trading"}]
        group_Type =[{"group_type_name" : "Assets"},{"group_type_name" : "Liabilities"},{"group_type_name" : "Income"},{"group_type_name" : "Expense"}]
        calculation_Type =[{"calculation_name" : "Fixed Rate","is_active":1},{"calculation_name" : "Weight Calculation","is_active":1},{"calculation_name" : "Per Gram Rate","is_active":1}]
        measurement_Type =[{"measurement_name" : "length","is_active" : 1},{"measurement_name" : "size","is_active" : 1}]
        stock_Type =[{"stock_type_name" : "tag","is_active" : 1},{"stock_type_name" : "non tag","is_active" : 1},{"stock_type_name" : "packet","is_active" : 1}]
        advance_Purpose =[{"purpose_name" : "Order","is_active" : 1},{"purpose_name" : "Repair","is_active" : 1}]
        approval_Type =[{"approval_type" : "Estimation Approval","is_active" : 1}]
        designation =[{"designation_name" : "Sales manager","is_active" : 1}]
        department =[{"department_name" : "Sales","is_active" : 1}]
        entry_Type =[{"entry_name" : "Regular","is_active" : 1},{"entry_name" : "Order","is_active" : 1},{"entry_name" : "Repair","is_active" : 1},{"entry_name" : "Sale Return","is_active" : 1}]
        gst_Type =[{"gst_type_name" : "Intra-state GST","is_active" : 1},{"gst_type_name" : "Inter-state GST","is_active" : 1}]
        order_For =[{"name" : "shop","is_active" : 1},{"name" : "Customer","is_active" : 1}]
        order_Priority =[{"name" : "Low","is_active" : 1},{"name" : "Medium","is_active" : 1},{"name" : "High","is_active" : 1}]
        repair_For =[{"repair_for" : "shop"},{"repair_for" : "Customer"}]
        gender_Type =[{"name" : "Male","is_active" :1 },{"name" : "Female", "is_active" : 1}]
        payment_Method =[{"payment_method_name" : "Cash","color" : "#1D1D1D","bg_color" : "#E2E8F0"},{"payment_method_name" : "UPI","color" : "#1D1D1D","bg_color" : "#E2E8F0"},{"payment_method_name" : "Card","color" : "#1D1D1D","bg_color" : "#E2E8F0"},{"payment_method_name" : "Bank","color" : "#1D1D1D","bg_color" : "#E2E8F0"},{"payment_method_name" : "Scheme","color" : "#FFFFFF","bg_color" : "#1E4E87"}]
        payment_Module =[{"module_name" : "Order"},{"name" : "Repair"},{"name" : "Billing"}]
        payment_Provider =[{"payment_provider_name" : "Gpay","payment_method_id" :2},{"payment_provider_name" : "Phonepe","payment_method_id" :2},{"payment_provider_name" : "Paytm","payment_method_id" :2}]
        payment_Status =[{"status_name" : "Pending","color" : "#FFFFFF"},{"status_name" : "Partially Paid","color" : "#FFFFFF"},{"status_name" : "Paid","color" : "#FFFFFF"}]
        printing_Module = [{"estimation_is_a4" : 1, "billing_is_a4" : 1, "billing_backup_is_a4" : 1, "order_is_a4" : 1, "repair_is_a4" : 1}]
        rate_Type =[{"type_name" : "Gross Weight","is_active" : 1},{"type_name" : "Net Weight","is_active" : 1}]
        stone_weight_Type =[{"weight_name" : "Carat","is_active" : 1},{"weight_name" : "Gram","is_active" : 1}]
        weight_Type =[{"weight_name" : "Gross Weight","is_active" : 1},{"weight_name" : "Net Weight","is_active" : 1}]
        location =[{"location_name" : "Coimbatore", "is_active" : 1}]
        branch =[{"branch_name":"Coimbatore","branch_shortcode":"CBE", "is_active":1, "location_id":1}]
        status_Type =[{"status_name":"Pending","module":1,"color":"#AD9FFF"},{"status_name":"Partial","module":1,"color":"#AD9FFF"},{"status_name":"Completed","module":1,"color":"#AD9FFF"},{"status_name":"Order Issued","module":1,"color":"#AD9FFF"},{"status_name":"Order Received","module":1,"color":"#AD9FFF"},{"status_name":"Order Delivered","module":1,"color":"#AD9FFF"},{"status_name":"Cancelled","module":1,"color":"#AD9FFF"},{"status_name":"Estimation Approval","module":1,"color":"#AD9FFF"},{"status_name":"Estimation Denied","module":1,"color":"#AD9FFF"},{"status_name":"Melting Issued","module":1,"color":"#AD9FFF"},{"status_name":"Melting Received","module":1,"color":"#AD9FFF"},{"status_name":"Purification Issued","module":1,"color":"#AD9FFF"},{"status_name":"Purification Received","module":1,"color":"#AD9FFF"},{"status_name":"Approval Issued","module":1,"color":"#AD9FFF"},{"status_name":"Approval Received","module":1,"color":"#AD9FFF"},{"status_name":"Repair Issued","module":1,"color":"#AD9FFF"},{"status_name":"Repair Received","module":1,"color":"#AD9FFF"},{"status_name":"Repair Deliverd","module":1,"color":"#AD9FFF"}]
        
        user_role =[{"role_name":"Super admin", "is_active":1, "is_active":1, "is_admin":1}]
        user_objects =[{"password":"Test@123", "email":"admin@atts.in", "phone":"9234454445", "is_active" : 1, "role":1, "first_name":"Jeyasekar", "last_name":"", "city":"Coimbatore", "state":"{name:Tamil Nadu,isoCode:TN}", "country":"{name:India,isoCode:IN}", "address":"coimbatore", "pincode":"626041", "aadhar_card":"", "pan_card":"", "location":1, "branch":1, "department":1, "designation":1}]
        try:
            with transaction.atomic():

                location_objects = [Location(**data) for data in location]
                Location.objects.bulk_create(location_objects)

                branch_objects = [Branch(**data) for data in branch]
                Branch.objects.bulk_create(branch_objects)
                
                user_role_objects = [UserRole(**data) for data in user_role]
                UserRole.objects.bulk_create(user_role_objects)

                designation_objects = [Designation(**data) for data in designation]
                Designation.objects.bulk_create(designation_objects)

                department_objects = [Department(**data) for data in department]
                Department.objects.bulk_create(department_objects)
                
                try:
                    if request.user.is_anonymous:
                        return Response({"error": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

                    url = request.build_absolute_uri(reverse('user-list'))
                    
                    token = request.auth

                    # Make a POST request to the UserViewSet create endpoint
                    headers = {'Authorization': f'Token {token}'}
                    response = requests.post(url, json=user_objects, headers=headers)

                    if response.status_code == status.HTTP_201_CREATED:
                        return Response({"message": "User created successfully in app1"}, status=status.HTTP_201_CREATED)
                    else:
                        return Response({"error": response.json()}, status=response.status_code)
                except Exception as err:
                    pass
                
                billing_type_objects = [BillingType(**data) for data in bill_Type]
                BillingType.objects.bulk_create(billing_type_objects)

                account_type_objects = [AccountType(**data) for data in account_Type]
                AccountType.objects.bulk_create(account_type_objects)

                customer_type_objects = [CustomerType(**data) for data in customer_Type]
                CustomerType.objects.bulk_create(customer_type_objects)

                group_ledger_objects = [GroupLedger(**data) for data in group_Ledger]
                GroupLedger.objects.bulk_create(group_ledger_objects)

                group_type_objects = [GroupType(**data) for data in group_Type]
                GroupType.objects.bulk_create(group_type_objects)

                calculation_type_objects = [CalculationType(**data) for data in calculation_Type]
                CalculationType.objects.bulk_create(calculation_type_objects)

                measurement_type_objects = [MeasurementType(**data) for data in measurement_Type]
                MeasurementType.objects.bulk_create(measurement_type_objects)

                stock_type_objects = [StockType(**data) for data in stock_Type]
                StockType.objects.bulk_create(stock_type_objects)

                advance_purpose_objects = [AdvancePurpose(**data) for data in advance_Purpose]
                AdvancePurpose.objects.bulk_create(advance_purpose_objects)

                approval_type_objects = [ApprovalType(**data) for data in approval_Type]
                ApprovalType.objects.bulk_create(approval_type_objects)

                entry_type_objects = [EntryType(**data) for data in entry_Type]
                EntryType.objects.bulk_create(entry_type_objects)

                gst_type_objects = [GSTType(**data) for data in gst_Type]
                GSTType.objects.bulk_create(gst_type_objects)

                order_for_objects = [OrderFor(**data) for data in order_For]
                OrderFor.objects.bulk_create(order_for_objects)

                order_priority_objects = [Priority(**data) for data in order_Priority]
                Priority.objects.bulk_create(order_priority_objects)

                repair_for_objects = [RepairFor(**data) for data in repair_For]
                RepairFor.objects.bulk_create(repair_for_objects)

                gender_type_objects = [Gender(**data) for data in gender_Type]
                Gender.objects.bulk_create(gender_type_objects)

                payment_method_objects = [PaymentMenthod(**data) for data in payment_Method]
                PaymentMenthod.objects.bulk_create(payment_method_objects)

                payment_module_objects = [PaymentModule(**data) for data in payment_Module]
                PaymentModule.objects.bulk_create(payment_module_objects)

                payment_provider_objects = [PaymentProviders(**data) for data in payment_Provider]
                PaymentProviders.objects.bulk_create(payment_provider_objects)

                payment_status_objects = [PaymentStatus(**data) for data in payment_Status]
                PaymentStatus.objects.bulk_create(payment_status_objects)

                print_module_objects = [PrintModule(**data) for data in printing_Module]
                PrintModule.objects.bulk_create(print_module_objects)

                print_module_objects = [PrintModule(**data) for data in printing_Module]
                PrintModule.objects.bulk_create(print_module_objects)

                rate_type_objects = [RateType(**data) for data in rate_Type]
                RateType.objects.bulk_create(rate_type_objects)

                stone_weight_type_objects = [StoneWeightType(**data) for data in stone_weight_Type]
                StoneWeightType.objects.bulk_create(stone_weight_type_objects)

                weight_type_objects = [WeightType(**data) for data in weight_Type]
                WeightType.objects.bulk_create(weight_type_objects)

                status_type_objects = [StatusTable(**data) for data in status_Type]
                StatusTable.objects.bulk_create(status_type_objects)

            return Response({
                "message": res_msg.create("bill type"),
                "status": status.HTTP_201_CREATED
            }, status=status.HTTP_200_OK)
        
        except IntegrityError as e:
            return Response({
                "data": str(e),  # Convert the exception to a string
                "message": res_msg.not_create("bill type"),
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                "data": str(e),  # Convert the exception to a string
                "message": res_msg.not_create("bill type"),
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)
            

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class MainMenuGroupViewSet(viewsets.ViewSet):

    def create(self, request):

        data = request.data
        data['main_menugroup_name'] = data.get('main_menugroup_name').lower()
        data['created_at'] = timezone.now()
        data['created_by'] = request.user.id

        serializer = MainMenuGroupSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": res_msg.create('Main Menu Group'),
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
            queryset = MainMenuGroup.objects.get(id=pk, is_active=True)
        except Exception as err:
            return Response({
                "message": res_msg.not_exists('Main Menu Group'),
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_200_OK)
        
        data = request.data
        data['main_menugroup_name'] = data.get('main_menugroup_name').lower()
        data['modified_at'] = timezone.now()
        data['modified_by'] = request.user.id

        serializer = MainMenuGroupSerializer(queryset, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": res_msg.update('Main Menu Group'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        return Response({
                "data": serializer.errors,
                "message": res_msg.in_valid_fields(),
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_200_OK)
    
    def destroy(self, request, pk):
        try:
            queryset = MainMenuGroup.objects.get(id=pk)
            queryset.delete()
            return Response({
                "message": res_msg.delete('Main Menu Group'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        except MainMenuGroup.DoesNotExist:
            return Response({
                "message": res_msg.not_exists('Main Menu Group'),
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
class MainMenuGroupStatus(APIView):
    def get(self,request,pk):

        try:

            queryset = MainMenuGroup.objects.get(id=pk)

            queryset.is_active = not(queryset.is_active)

            queryset.save()

            return Response(
                {
                    "message":res_msg.change("Main Menu Group Status"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        except Exception as err:
            return Response(
                {
                    "message":res_msg.not_exists("Main Menu Group"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class MainMenuGroupList(APIView):
    def get(self, request):

        queryset = list(MainMenuGroup.objects.filter(is_active=True).order_by('id'))
        serializer = MainMenuGroupSerializer(queryset, many=True)

        return Response({
            "data": {
                "list": serializer.data,
            },
            "message": res_msg.retrieve('Main Menu Group'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)

    def post(self, request):

        search = request.data.get('search') if request.data.get('search') else ''
        from_date = request.data.get('from_date') if request.data.get('from_date') else None
        to_date = request.data.get('to_date') if request.data.get('to_date') else None
        active_status = request.data.get('active_status') if request.data.get('active_status') != None else None
        page = request.data.get('page') if request.data.get('page') else 1
        items_per_page = request.data.get('items_per_page') if request.data.get('items_per_page') else 10
        
        filter_condition={}
    
        if active_status != None:
           filter_condition['is_active'] = active_status 

        if from_date != None and to_date!= None:
           fdate =from_date+'T00:00:00.899010+05:30'
           tdate =to_date+'T23:59:59.899010+05:30'
           date_range=(fdate,tdate)
           filter_condition['created_at__range']=date_range

        if len(filter_condition) != 0:
            queryset = list(MainMenuGroup.objects.filter(main_menugroup_name__icontains=search,**filter_condition).order_by('id'))
        elif search != '':
            queryset = list(MainMenuGroup.objects.filter(main_menugroup_name__icontains__icontains=search).order_by('id'))
        else:
            queryset = list(MainMenuGroup.objects.all().order_by('id'))

        paginated_data = Paginator(queryset, items_per_page)
        serializer = MainMenuGroupSerializer(paginated_data.get_page(page), many=True)

        response_data=[]
        for i in range(0, len(serializer.data)):
            dict_data=serializer.data[i]

            response_data.append(dict_data)

        return Response({
            "data": {
                "list": response_data,
                "total_pages": paginated_data.num_pages,
                "current_page": page,
                "total_items": len(queryset),
                "current_items": len(serializer.data)
            },
            "message": res_msg.retrieve('Main Menu Group List'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
    

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class IncentiveTypeViewSet(viewsets.ViewSet):

    def create(self, request):

        data = request.data
        data['incentive_typename']=data.get('incentive_typename')
        data['created_at'] = timezone.now()
        data['created_by'] = request.user.id
        serializer = IncentiveTypeSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": res_msg.create('Incentive type'),
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
            queryset = IncentiveType.objects.get(id=pk)
        except Exception as err:
            return Response({
                "message": res_msg.not_exists('Incentive Type'),
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_200_OK)
        
        data = request.data
        data['modified_at'] = timezone.now()
        data['modified_by'] = request.user.id
        serializer = IncentiveTypeSerializer(queryset, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": res_msg.update('Incentive Type'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        return Response({
                "data": serializer.errors,
                "message": res_msg.in_valid_fields(),
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_200_OK)
    
    def destroy(self, request, pk):
        try:
            queryset = IncentiveType.objects.get(id=pk)
            queryset.delete()
            return Response({
                "message": res_msg.delete('Incentive Type'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        except IncentiveType.DoesNotExist:
            return Response({
                "message": res_msg.not_exists('Incentive Type'),
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
        
    def get(self, request, pk=None):
        try:
            if pk != None:
                queryset = IncentiveType.objects.filter(id=pk,is_active=True)                 
            else:
                queryset = IncentiveType.objects.filter(is_active=True)

            serializer = IncentiveTypeSerializer(queryset,many=True)    

            return Response({
                "data": serializer.data,
                "message": res_msg.retrieve('Incentive Type'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        
        except Exception as err:
            return Response({
                "message": res_msg.not_exists('Incentive Type'),
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_200_OK)
       
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class IncentivePercentViewSet(viewsets.ViewSet):

    def create(self, request):

        data = request.data
        data['incentive_type']=data.get('incentive_type')
        # data['incentive_percent']=data.get('incentive_percent')
        # data['incentive_amount']=data.get('incentive_amount')
        data['from_amount']=data.get('from_amount')
        data['to_amount']=data.get('to_amount')
        data['created_at'] = timezone.now()
        data['created_by'] = request.user.id
        serializer = IncentivePercentSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": res_msg.create('Incentive'),
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
            queryset = IncentivePercent.objects.get(id=pk)
        except Exception as err:
            return Response({
                "message": res_msg.not_exists('Incentive'),
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_200_OK)
        
        data = request.data
        data['modified_at'] = timezone.now()
        data['modified_by'] = request.user.id
        serializer = IncentivePercentSerializer(queryset, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": res_msg.update('Incentive'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        return Response({
                "data": serializer.errors,
                "message": res_msg.in_valid_fields(),
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_200_OK)
    
    def destroy(self, request, pk):
        try:
            queryset = IncentivePercent.objects.get(id=pk)
            queryset.delete()
            return Response({
                "message": res_msg.delete('Incentive'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        except IncentivePercent.DoesNotExist:
            return Response({
                "message": res_msg.not_exists('Incentive'),
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
        
    def get(self, request, pk=None):
        try:
            if pk != None:
                queryset = IncentivePercent.objects.filter(id=pk,is_active=True)                 
            else:
                queryset = IncentivePercent.objects.filter(is_active=True)

            serializer = IncentivePercentSerializer(queryset,many=True)    
                
            return Response({
                "data": serializer.data,
                "message": res_msg.retrieve('Incentive Percent'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        
        except Exception as err:
            return Response({
                "message": res_msg.not_exists('Incentive Percent'),
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_200_OK)
        

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class IncentiveList(APIView):
    def post(self, request):

        search = request.data.get('search') if request.data.get('search') else ''
        from_date = request.data.get('from_date') if request.data.get('from_date') else None
        to_date = request.data.get('to_date') if request.data.get('to_date') else None 
        page = request.data.get('page') if request.data.get('page') else 1
        items_per_page = request.data.get('items_per_page') if request.data.get('items_per_page') else 10
        
        filter_condition={}
    
        if search != '':
           filter_condition['incentive_percent'] = search 
           

        if from_date != None and to_date!= None:
           fdate =from_date
           tdate =to_date
           date_range=(fdate,tdate)
           filter_condition['created_at__range']=date_range

        if len(filter_condition) != 0:
            queryset = list(IncentivePercent.objects.filter(**filter_condition).order_by('id'))
        else:
            queryset = list(IncentivePercent.objects.all().order_by('id'))

        paginated_data = Paginator(queryset, items_per_page)
        serializer = IncentivePercentSerializer(paginated_data.get_page(page), many=True)

        res_data = []
        for i in range(0, len(serializer.data)):
            dict_data = serializer.data[i]
            type_name = IncentivePercent.objects.get(id=dict_data['id'])
            dict_data['incentive_type_name'] = type_name.incentive_type.incentive_typename
        
            res_data.append(dict_data)

        return Response({
            "data": {
               "list": serializer.data,
                "total_pages": paginated_data.num_pages,
                "current_page": page,
                "total_items": len(queryset),
                "current_items": len(serializer.data)
            },
            "message": res_msg.retrieve('Incentive'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)    
    

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class SalesEntryTypeView(APIView):

    def get(self, request):

        queryset = list(SalesEntryType.objects.filter(is_active=True).order_by('id'))
        serializer = SalesEntryTypeSerializer(queryset, many=True)

        return Response({
            "data": {
                "list": serializer.data,
            },
            "message": res_msg.retrieve('Sales Entry Type'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
    



@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class TransactionTypeView(APIView):

    def get(self, request):

        queryset = list(TransactionType.objects.filter(is_active=True).order_by('id'))
        serializer = TransactionTypeSerializer(queryset, many=True)

        return Response({
            "data": {
                "list": serializer.data,
            },
            "message": res_msg.retrieve('Transaction Type'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)