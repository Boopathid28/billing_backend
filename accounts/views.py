from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .models import *
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes, authentication_classes
from .serializer import *
import phonenumbers
from app_lib.utility import Email
from django.utils import timezone
from app_lib.response_messages import ResponseMessages
from settings.models import Menu, MenuPermission, MenuGroup
from organizations.models import Staff
import requests
from django.conf import settings

res_msg = ResponseMessages()

class LoginView(APIView):

    def post(self, request):

        data = request.data
    
        validate_data = Email.check_email(data.get('username'))
     
        if validate_data:
            try:
                queryset = User.object.get(email__iexact=data.get('username'), is_active=True, is_deleted=False,is_superuser=False)
            except Exception as err:
                return Response({"message": res_msg.not_exists('User'), "status": status.HTTP_401_UNAUTHORIZED}, status=status.HTTP_200_OK)
        
            user = authenticate(username=data.get('username'), password=data.get('password'))
                        
            if user is not None:
                queryset.is_loggedin = True
                queryset.last_login = timezone.now()
                queryset.save()

                login_serializer = UserSerializer(queryset)

                try:
                    roles_queryset = UserRole.objects.get(id=login_serializer.data['role'])
                except Exception as e:
                    pass

                try:
                    temp_token = Token.objects.get(user=queryset)
                    # return Response({
                    #     "message": "Already your sessioin is active",
                    #     "status": status.HTTP_100_CONTINUE
                    # }, status=status.HTTP_200_OK)
                    temp_token.delete()
                except Exception as error:
                    pass
                token = Token.objects.create(user=queryset)
            
                if queryset.role.is_admin == True:
                    branch =True
                else:
                    branch = False
                
                branch_queryset = Branch.objects.get(id=login_serializer.data['branch'])

                response_data = {
                        "data": {
                        "token": token.key,
                        "phone": login_serializer.data['phone'],
                        "email": login_serializer.data['email'],
                        "user_id": login_serializer.data['id'],
                        "logged_in": login_serializer.data['is_loggedin'],
                        "is_active": login_serializer.data['is_active'],
                        "user_role": roles_queryset.role_name,
                        "user_role_id": login_serializer.data['role'],
                        "branch": branch,
                        "branch_shortname":branch_queryset.branch_name
                        },
                        "message": res_msg.login("Loggedin"),
                        "status": status.HTTP_200_OK
                    }
                
                try:
                    staff_queryset=Staff.objects.get(phone=queryset.phone)
                    response_data['data']['name'] = staff_queryset.first_name
                except:
                    pass
                
                    
                
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response({
                    "message": res_msg.in_valid("Username or password"), 
                    "status": status.HTTP_401_UNAUTHORIZED
                    }, status=status.HTTP_200_OK)
            
        else:
            try:
                mobile_no = phonenumbers.parse("+91" + str(data.get('username')))
            except Exception as mob_err:
                return Response({"message": res_msg.in_valid("Phone number or email"), "status": status.HTTP_401_UNAUTHORIZED}, status=status.HTTP_200_OK)

            if phonenumbers.is_possible_number(mobile_no) and len(data.get('username')) == 10:
                try:
                    queryset = User.object.get(phone=data.get('username'), is_active=True, is_deleted=False, is_superuser=False)
                except Exception as err:
                    return Response({
                        "message": res_msg.not_exists('User'),
                        "status": status.HTTP_401_UNAUTHORIZED
                    }, status=status.HTTP_200_OK)
                
                user = authenticate(username=queryset.email, password=data.get('password'))

                if user is not None:
                    queryset.is_loggedin = True
                    queryset.last_login = timezone.now()
                    queryset.save()                    

                    login_serializer = UserSerializer(queryset)

                    try:
                        roles_queryset = UserRole.objects.get(id=login_serializer.data['role'])
                    except Exception as e:
                        pass
                    
                    try:
                        temp_token = Token.objects.get(user=queryset)
                        # return Response({
                        #     "message": "Already your sessioin is active",
                        #     "status": status.HTTP_100_CONTINUE
                        # }, status=status.HTTP_200_OK)
                        temp_token.delete()
                    except Exception as error:
                        pass
                    token = Token.objects.create(user=queryset)
                    if queryset.role.is_admin == True:
                        branch =True
                    else:
                        branch = False
                    
                    branch_queryset = Branch.objects.get(id=login_serializer.data['branch'])
                    response_data = {
                        "data": {
                        "token": token.key,
                        "phone": login_serializer.data['phone'],
                        "email": login_serializer.data['email'],
                        "user_id": login_serializer.data['id'],
                        "logged_in": login_serializer.data['is_loggedin'],
                        "is_active": login_serializer.data['is_active'],
                        "user_role": roles_queryset.role_name,
                        "user_role_id": login_serializer.data['role'],
                        "branch": branch,
                        "branch_shortname":branch_queryset.branch_name
                        },
                        "message": res_msg.login("Loggedin"),
                        "status": status.HTTP_200_OK
                    }

                    try:
                        staff_queryset=Staff.objects.get(phone=queryset.phone)
                        response_data['data']['name'] = staff_queryset.first_name
                    except:
                        pass

                    return Response(response_data, status=status.HTTP_200_OK)
                else:
                    return Response({
                        "message": res_msg.in_valid("Username or password"), 
                        "status": status.HTTP_401_UNAUTHORIZED
                        }, status=status.HTTP_200_OK)
                
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ChangePasswordView(APIView):
    def put(self, request, pk):
        data = request.data

        try:
            user = User.object.get(id=pk, is_active=True)
        except Exception as err:
            return Response({"message": res_msg.not_exists('User'), "status": status.HTTP_404_NOT_FOUND}, status=status.HTTP_200_OK)

        user.set_password(data.get('password'))
        user.modified_at = timezone.now()
        user.modified_by = request.user.id
        user.save()

        serializer = UserSerializer(user)

        try:
            roles_queryset = UserRole.objects.get(id=serializer.data['role'])
        except Exception as e:
            pass
                    
        response_data = {
            "data": {
                "phone": serializer.data['phone'],
                "email": serializer.data['email'],
                "user_id": serializer.data['id'],
                "logged_in": serializer.data['is_loggedin'],
                "is_active": serializer.data['is_active'],
                "user_role": roles_queryset.role_name
            },
            "message": res_msg.change('Password'),
            "status": status.HTTP_200_OK
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class LogoutView(APIView):

    def get(self, request):
        token = str(request.headers['Authorization']).split(' ')[1]
        try:
            token_data = Token.objects.get(key=token)
        except Exception as err:
            return Response({'message': str(err), "status": status.HTTP_401_UNAUTHORIZED}, status=status.HTTP_200_OK)
        
        try:
            user = User.object.get(id=token_data.user_id)
        except Exception as err:
            return Response({'message': str(err), "status": status.HTTP_401_UNAUTHORIZED}, status=status.HTTP_200_OK)

        user.is_loggedin = False
        user.save()
        Token.objects.get(key=token).delete()
        
        return Response({
            'message': res_msg.login('Logged out'), 
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
    

