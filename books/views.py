from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework import viewsets
from rest_framework import status
import random
from organizations.models import Staff
from .serializer import *
from .models import *
import datetime
from rest_framework.response import Response
from django.core.paginator import Paginator
from app_lib.response_messages import ResponseMessages
from django.db.models import ProtectedError
from rest_framework.views import APIView
from django.db.models import Q
from django.utils import timezone
from django.db import transaction

res_msg=ResponseMessages()

# Create your views here.
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class CompanyViewset(viewsets.ViewSet):
   
    def retrieve(self,request,pk):
        res_data={}
        
        try:
            queryset=CompanyDetails.objects.get(id=pk)
            serializer=CompanyDetailsSerializer(queryset)
            res_data['company_details']=serializer.data
        except Exception as err:
            pass
        try:
            address_queryset=CompanyAddressDetails.objects.get(company_details=pk)
            address_serializer=CompanyAddressDetailsSerializer(address_queryset)
            res_data['address_details']=address_serializer.data
        except Exception as err:
            pass
        try:
            bank_queryset=list(CompanyBankDetails.objects.filter(company_details=pk))
            bank_serializer=CompanyBankDetailsSerializer(bank_queryset,many=True)
            res_data['bank_details']=bank_serializer.data
        except Exception as err:
            pass
        try:
            gst_queryset=CompanyGstDetails.objects.get(company_details=pk)
            gst_serializer=CompanyGstDetailsSerializer(gst_queryset)
            res_data['gst_details']=gst_serializer.data
        except Exception as err:
            pass

        return Response(
            {
                "data":res_data,
                "message":res_msg.retrieve('Company'),
                "status":status.HTTP_200_OK
            },status= status.HTTP_200_OK
        )
    
    def create(self,request):

        data=request.data

        response_data=[]

        com_details=data['company_details']
        com_details['created_at']=timezone.now()
        com_details['created_by']=request.user.id


        company_serializer=CompanyDetailsSerializer(data=com_details)


        if company_serializer.is_valid():
            company_serializer.save()
            company_dict=company_serializer.data
            response_data.append(company_dict)

            address_details=data['address_details']
            address_details['company_details']=company_serializer.data['id']
            address_details['created_at']=timezone.now()
            address_details['created_by']=request.user.id
            
            address_serializer=CompanyAddressDetailsSerializer(data=address_details)

            if address_serializer.is_valid():
                address_serializer.save()
                address_dict=address_serializer.data
                response_data.append(address_dict)
            
                bank_details=data['bank_details']

                for i in bank_details:
                    try:
                        get_bank_queryset = CompanyBankDetails.objects.get(account_no=i.get('account_no'),company_details=company_serializer.data['id'], ifsc_code=i.get('ifsc_code'), micr_code=i.get('micr_code'))

                        i['modified_at']=timezone.now()
                        i['modified_by']=request.user.id

                        bank_serializer=CompanyBankDetailsSerializer(get_bank_queryset,data=i,partial=True)

                        if bank_serializer.is_valid():
                            bank_serializer.save()
                    except:
                        new_bank = i
                        new_bank['company_details']=company_serializer.data['id']
                        new_bank['created_at']=timezone.now()
                        new_bank['created_by']=request.user.id

                        bank_serializer=CompanyBankDetailsSerializer(data=new_bank)

                        if bank_serializer.is_valid():
                            bank_serializer.save()
                            bank_dict=bank_serializer.data
                            response_data.append(bank_dict)
                            

                        else:
                            return Response(
                                {
                                 "data":bank_serializer.errors,
                                 "message":res_msg.not_create('Company'),
                                 "status":status.HTTP_400_BAD_REQUEST
                                },status=status.HTTP_200_OK
                         )
                gst_details=data['gst_details']
                gst_details['company_details']=company_serializer.data['id']
                gst_details['created_at']=timezone.now()
                gst_details['created_by']=request.user.id
                gst_serializer=CompanyGstDetailsSerializer(data=gst_details)

                if gst_serializer.is_valid():
                    gst_serializer.save()
                    gst_dict=gst_serializer.data
                    response_data.append(gst_dict)
                    return Response(
                        {
                            "data":response_data,
                            "message":res_msg.create('Company'),
                            "status":status.HTTP_201_CREATED
                        },status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {
                            "data":gst_serializer.errors,
                            "message":res_msg.not_create('Company'),
                            "status":status.HTTP_400_BAD_REQUEST
                        },status=status.HTTP_200_OK
                    )
            else:
                return Response(
                            {
                                "data":address_serializer.errors,
                                "message":res_msg.not_create('Company'),
                                "status":status.HTTP_400_BAD_REQUEST
                            },status=status.HTTP_200_OK
                        )
        else:
            return Response(
                            {
                                "data":company_serializer.errors,
                                "message":res_msg.not_create('Company'),
                                "status":status.HTTP_400_BAD_REQUEST
                            },status=status.HTTP_200_OK
                        )
    
    def update(self,request,pk):
        request_data=request.data
        try:
            queryset=CompanyDetails.objects.get(id=pk)

            company_details=request_data.get('company_details')
            company_details['modified_at']=timezone.now()
            company_details['modified_by']=request.user.id

            serializer=CompanyDetailsSerializer(queryset,data=company_details,partial=True)

            if serializer.is_valid():
                serializer.save()

            try:
                address_details=request_data.get('address_details') if request_data.get('address_details') else []
                address_details['modified_at']=timezone.now()
                address_details['modified_by']=request.user.id

                address_queryset=CompanyAddressDetails.objects.get(company_details=pk)

                address_serializer=CompanyAddressDetailsSerializer(address_queryset,data=address_details,partial=True)

                if address_serializer.is_valid():
                    address_serializer.save()
                
                try:
                    bank_details=request_data.get('bank_details') if request_data.get('bank_details') else []

                    for bank in bank_details:
                        try:
                            get_bank_queryset = CompanyBankDetails.objects.get(account_no=bank.get('account_no'),company_details=pk, ifsc_code=bank.get('ifsc_code'), micr_code=bank.get('micr_code'))

                            bank['modified_at']=timezone.now()
                            bank['modified_by']=request.user.id

                            bank_serializer=CompanyBankDetailsSerializer(get_bank_queryset,data=bank,partial=True)
                            
                            if bank_serializer.is_valid():
                                bank_serializer.save()
                           
                        except CompanyBankDetails.DoesNotExist:
                            new_bank = bank
                            new_bank['company_details'] = pk
                            new_bank['created_at']=timezone.now()
                            new_bank['created_by']=request.user.id

                            bank_serializer=CompanyBankDetailsSerializer(data=new_bank)

                            
                            if bank_serializer.is_valid():
                                bank_serializer.save()
                        except Exception as err:
                            pass

                    try:
                        gst_details=request_data.get('gst_details') if request_data.get('gst_details') else []
                        gst_details['modified_at']=timezone.now()
                        gst_details['modified_by']=request.user.id

                        gst_queryset=CompanyGstDetails.objects.get(company_details=pk)

                        gst_serializer=CompanyGstDetailsSerializer(gst_queryset,data=gst_details,partial=True)

                        if gst_serializer.is_valid():
                            gst_serializer.save()

                    except Exception as err:
                        return Response(
                        {
                            "message":res_msg.something_else(),
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
            except Exception as err:
                return Response(
                    {
                        "message":res_msg.something_else(),
                        "status":status.HTTP_400_BAD_REQUEST
                    },status=status.HTTP_200_OK
                )
        except Exception as err:
            return Response(
                {
                    "message":res_msg.not_exists("Company"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        return Response(
            {
                "data":request_data,
                "message":res_msg.update("Company"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
    
    def destroy(self,request,pk):
        try:
            company_queryset=CompanyDetails.objects.get(id=pk)
            company_queryset.delete()

            return Response({
            "message": res_msg.delete('Company'),
            "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        except CompanyDetails.DoesNotExist:
            return Response({
                'message': res_msg.not_exists('Company'),
                'status': status.HTTP_404_NOT_FOUND
            },status=status.HTTP_200_OK)
        except Exception as err:
            return Response({
                "message": res_msg.something_else(),
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_200_OK)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])   
class CompanyBankView(APIView):

    def post(self,request):
 
        id_list = request.data.get('id_list') if request.data.get('id_list') else []
 
        for i in id_list:
            try:
                queryset=CompanyBankDetails.objects.get(id=i)
                queryset.delete()
            except:
                pass

        return Response(
                    {
                        "message":res_msg.delete("Company Bank Details"),
                        "status":status.HTTP_200_OK
                    },status=status.HTTP_200_OK
                )

    def delete(self,request,pk):

        try:
            queryset=CompanyBankDetails.objects.get(id=pk)
            queryset.delete()

            return Response(
                {
                    "message":res_msg.delete("Bank Details"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        except CompanyBankDetails.DoesNotExist:
            return Response(
                {
                    "message":res_msg.not_exists("Bank Details"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        except Exception as err:
            return Response(
                {
                    "message":res_msg.something_else,
                    "status":status.HTTP_400_BAD_REQUEST
                },status=status.HTTP_200_OK
            )

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class CompanyList(APIView):

    def get(self,request):
       
        res_data = {}
 
        queryset=CompanyDetails.objects.filter(is_active=True).order_by('id').values('id','company_name','mobile_no','email_id','website','std_code','landline_no').first()
       
        if queryset:
            res_data['company_details'] = queryset
            try:
               
                address_queryset=CompanyAddressDetails.objects.get(company_details=queryset['id'])
                address_serializer=CompanyAddressDetailsSerializer(address_queryset)
                res_data['address_details']=address_serializer.data
            except Exception as err:
                pass
 
            try:
                gst_queryset=CompanyGstDetails.objects.get(company_details=queryset['id'])
                gst_serializer=CompanyGstDetailsSerializer(gst_queryset)
                res_data['gst_details']=gst_serializer.data
            except Exception as err:
                pass
 
        return Response(
            {
                "data":{
                    "list":res_data
                },
                "message":res_msg.retrieve('company'),
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
            items_per_page = int(request.data.get('items_per_page', CompanyDetails.objects.all().count()))
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
            queryset=list(CompanyDetails.objects.filter(Q(company_name__icontains=search)|Q(mobile_no__icontains=search)|Q(email_id__icontains=search)|Q(website__icontains=search),**filter_condition).order_by('id'))
        elif search != '':
                queryset=list(CompanyDetails.objects.filter(Q(company_name__icontains=search)|Q(mobile_no__icontains=search)|Q(email_id__icontains=search)|Q(website__icontains=search)).order_by('id'))
        else:
            queryset=list(CompanyDetails.objects.filter(Q(company_name__icontains=search)|Q(mobile_no__icontains=search)|Q(email_id__icontains=search)|Q(website__icontains=search)).order_by('id'))

        paginated_data = Paginator(queryset, items_per_page)
        serializer = CompanyDetailsSerializer(paginated_data.get_page(page), many=True)
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

        return Response(
            {
                "data":{
                    "list": res_data,
                    "total_pages": paginated_data.num_pages,
                    "current_page": page,
                    "total_items": len(queryset),
                    "current_items": len(serializer.data)
                },
                "message":res_msg.retrieve('company'),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
    
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class Companystatus(APIView):
    def get(self,request,pk):
        try:
            company_queryset=CompanyDetails.objects.get(id=pk)

        except Exception as err:
            return Response(
                {
                    "message":res_msg.not_exists("Company"),
                    "status":status.HTTP_404_NOT_FOUND
                },status= status.HTTP_200_OK
            )
        try:
            address_queryset=CompanyAddressDetails.objects.get(company_details=company_queryset.pk)
            address_queryset.is_active=not(company_queryset.is_active)
            address_queryset.save()
            
            try :
                bank_queryset=CompanyBankDetails.objects.filter(company_details=company_queryset.pk)

                for bank in bank_queryset:
                    bank.is_active=not(company_queryset.is_active)
                    bank.save()

                try:
                    gst_queryset=CompanyGstDetails.objects.get(company_details=company_queryset.pk)
                    gst_queryset.is_active=not(company_queryset.is_active)
                    gst_queryset.save()
                except Exception as err:
                    pass
            except Exception as err :
                pass
        except Exception as err :
            pass
        company_queryset.is_active=not(company_queryset.is_active)
        company_queryset.save()
        company_serializer=CompanyDetailsSerializer(company_queryset)

        return Response(
            {
                "data":company_serializer.data,
                "message":res_msg.change("Company status"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )


    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class GroupLedgerView(APIView):
    def get(self,request):

        queryset = list(GroupLedger.objects.all().order_by('id').values('id','group_ledger_name'))

        return Response(
            {
                "data": {
                    "list": queryset
                },
                "message":res_msg.retrieve('Group Ledger'),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class GroupTypeView(APIView):
    def get(self, request):

        queryset=list(GroupType.objects.all().order_by('id').values('id','group_type_name'))

        return Response(
            {
                "data": {
                    "list": queryset
                },
                "message":res_msg.retrieve('Group Type'),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class AccountGroupViewset(viewsets.ViewSet):

    def create(self,request):

        request_data=request.data
        request_data['account_group_name']=request_data['account_group_name'].lower()
        request_data['created_at']=timezone.now()
        request_data['created_by']=request.user.id

        serializer=AccountGroupSerailizer(data=request_data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "data":serializer.data,
                    "message":res_msg.create('Account Group'),
                    "status":status.HTTP_201_CREATED
                },status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    "data":serializer.errors,
                    "message":res_msg.not_create("Account Group"),
                    "status":status.HTTP_400_BAD_REQUEST
                },status.HTTP_200_OK
            )
        
    def update(self,request,pk):
        try:
            queryset=AccountGroup.objects.get(id=pk)
        except Exception as err:
            return Response(
                {
                    "message":res_msg.not_exists('Account Group'),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        request_data=request.data
        request_data['account_group_name']=request_data.get('account_group_name').lower() if request_data.get('account_group_name') else []
        request_data['modified_at']=timezone.now()
        request_data['modified_by']=request.user.id

        serializer=AccountGroupSerailizer(queryset,data=request_data,partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "data":serializer.data,
                    "message":res_msg.update("Account Group"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    "data":serializer.errors,
                    "message":res_msg.not_update('Account Group'),
                    "status":status.HTTP_400_BAD_REQUEST
                },status=status.HTTP_200_OK
            )
        
    def destroy(self,request,pk):
        try:
            queryset=AccountGroup.objects.get(id=pk)
            queryset.delete()
            return Response(
                {
                    "message":res_msg.delete("Account Group"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        except AccountGroup.DoesNotExist:
            return Response(
                {
                    "message":res_msg.not_exists("Account Group"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        except Exception as err:
            return Response(
                {
                    "message":res_msg.something_else("Account Group"),
                    "status":status.HTTP_400_BAD_REQUEST
                },status=status.HTTP_200_OK
            )
    
    def retrieve(self,request,pk):
        
        try:
            queryset=AccountGroup.objects.get(id=pk)
        except Exception as err:
            return Response(
                {
                    "message":res_msg.not_exists("Account Group"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        
        serializer=AccountGroupSerailizer(queryset)


        response_data=serializer.data
        response_data['group_ledger_name']=queryset.group_ledger.group_ledger_name
        response_data['group_type_name']=queryset.group_type.group_type_name



        return Response(
            {
                "data":response_data,
                "message":res_msg.retrieve("Account Group"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class AccountGroupStatusView(APIView):
    
    def get(self,request,pk):
        try:
            queryset=AccountGroup.objects.get(id=pk)
        except Exception as err:
            return Response(
                {
                    "message":res_msg.not_exists('Account Group'),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        queryset.is_active=not(queryset.is_active)
        queryset.save()
        serializer=AccountGroupSerailizer(queryset)

        
        return Response(
            {
                "data":serializer.data,
                "message":res_msg.change("Account Group Status"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class AccountGroupListView(APIView):
    
    def post(self,request):

        search = request.data.get('search') if request.data.get('search') else ''
        active_status = request.data.get('active_status') if request.data.get('active_status') else None
        from_date = request.data.get('from_date') if request.data.get('from_date') else None
        to_date = request.data.get('to_date') if request.data.get('to_date') else None
        page = request.data.get('page') if request.data.get('page') else 1
        try:
            items_per_page = int(request.data.get('items_per_page', AccountGroup.objects.all().count()))
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
                queryset=AccountGroup.objects.filter(Q(account_group_name__icontains=search)|Q(account_under__icontains=search)|Q(group_type__group_type_name__icontains=search)|Q(group_ledger__group_ledger_name__icontains=search),**filter_condition).order_by('id')
        elif search != '':
                queryset=AccountGroup.objects.filter(Q(account_group_name__icontains=search)|Q(account_under__icontains=search)|Q(group_type__group_type_name__icontains=search)|Q(group_ledger__group_ledger_name__icontains=search)).order_by('id')
        else:
            queryset=AccountGroup.objects.all().order_by('id')

        paginated_data = Paginator(queryset, items_per_page)
        serializer = AccountGroupSerailizer(paginated_data.get_page(page), many=True)

        response_data=[]
        for i in range(len(serializer.data)):
            # accountgroup_queryset=AccountGroup.objects.get(id=data.pk)

            # serializer=AccountGroupSerailizer(accountgroup_queryset)
            data_dict=serializer.data[i]
            # staff = Staff.objects.get(user = queryset[i].created_by.pk)
            # if staff is not None :
            #     username = staff.first_name
            # else:
            #     username = None
            # data_dict['created_by'] = username
            data_dict['group_ledger_name']=queryset[i].group_ledger.group_ledger_name
            data_dict['group_type_name']=queryset[i].group_type.group_type_name
            response_data.append(data_dict)
        
        return Response(
            {
                "data": {
                    "list": response_data,
                    "total_pages": paginated_data.num_pages,
                    "current_page": page,
                    "total_items": len(queryset),
                    "current_items": len(serializer.data)
                },
                "message":res_msg.retrieve("AccountGroup"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
    def get(self,request):
        queryset=list(AccountGroup.objects.filter(is_active=True).order_by('id').values('id','account_group_name'))
        return Response(
            {
               "data": {
                   "list":queryset
               },
               "message":res_msg.retrieve("Account Group"),
               "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class CustomerTypeview(APIView):
    def get(self,request):
        queryset=list(CustomerType.objects.all().order_by('id'))
        serializer=CustomerTypeSerailizer(queryset,many=True)
        return Response(
            {
                "data":{
                    "list":serializer.data
                },
                "message":res_msg.retrieve("Customer Type"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class AccountTypeview(APIView):
    def get(self,request):
        queryset=list(AccountType.objects.all().order_by('id'))
        serializer=AccountTypeSerailizer(queryset,many=True)
        return Response(
            {
                "data":{
                    "list":serializer.data
                },
                "message":res_msg.retrieve("Customer Type"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class AccountHeadViewset(viewsets.ViewSet):
    @transaction.atomic
    def create(self,request):
        try:
            request_data=request.data
            response_data=[]

            accounthead_details=request_data['accounthead_details']
            accounthead_details['account_head_code'] = account_head_code()
            accounthead_details['created_at']=timezone.now()
            accounthead_details['created_by']=request.user.id

            account_head_serailizer=AccountHeadDetailsSerailizer(data=accounthead_details)

            if account_head_serailizer.is_valid():
                account_head_serailizer.save()
                account_dict=account_head_serailizer.data
                response_data.append(account_dict)

                address_details=request_data['address_details']

                for address in address_details:
                    address['account_head']=account_head_serailizer.data['id']
                    address['created_at']=timezone.now()
                    address['created_by']=request.user.id

                    address_serializer=AccountHeadAddressSerailizer(data=address)

                    if address_serializer.is_valid():
                        address_serializer.save()
                        address_dict=address_serializer.data
                        response_data.append(address_dict)
                    else:
                        raise Exception(address_serializer.errors)
                        return Response(
                            {
                                "data":address_serializer.errors,
                                "message":res_msg.something_else(),
                                "status":status.HTTP_400_BAD_REQUEST
                            },status=status.HTTP_200_OK
                        )
                contact_details=request_data['contact_details']

                for contact in contact_details:
                    contact['account_head']=account_head_serailizer.data['id']
                    contact['created_at']=timezone.now()
                    contact['created_by']=request.user.id

                    contact_serialzer=AccountHeadContactSerailizer(data=contact)

                    if contact_serialzer.is_valid():
                        contact_serialzer.save()
                        conatact_dict=contact_serialzer.data
                        response_data.append(conatact_dict)
                    else:
                        raise Exception(contact_serialzer.errors)
                        return Response(
                            {
                                "data":contact_serialzer.errors,
                                "message":res_msg.something_else(),
                                "status":status.HTTP_400_BAD_REQUEST
                            },status=status.HTTP_200_OK
                        )
                
                bank_details=request_data['bank_details']

                for bank in bank_details:
                    bank['account_head']=account_head_serailizer.data['id']
                    bank['created_at']=timezone.now()
                    bank['created_by']=request.user.id

                    bank_serializer=AccountHeadBankDetailsSerailizer(data=bank)

                    if bank_serializer.is_valid():
                        bank_serializer.save()
                        bank_dict=bank_serializer.data  
                        response_data.append(bank_dict)
                    else:
                        raise Exception(bank_serializer.errors)
                        return Response(
                            {
                                "data":bank_serializer.errors,
                                "message":res_msg.something_else(),
                                "status":status.HTTP_400_BAD_REQUEST
                            },status=status.HTTP_200_OK
                        )
                gst_details=request_data['gst_details']
                gst_details['account_head']=account_head_serailizer.data['id']
                gst_details['created_at']=timezone.now()
                gst_details['created_by']=request.user.id

                gst_serializer=AccountHeadGstDetailsSerailizer(data=gst_details)

                if gst_serializer.is_valid():
                    gst_serializer.save()
                    gst_dict=gst_serializer.data  
                    response_data.append(gst_dict)
                else:
                    raise Exception(gst_serializer.errors)
                    return Response(
                        {
                            "data":gst_serializer.errors,
                            "message":res_msg.something_else(),
                            "status":status.HTTP_400_BAD_REQUEST
                        },status=status.HTTP_200_OK
                    )
            else:
                raise Exception(account_head_serailizer.errors)
                return Response(
                    {
                        "data":account_head_serailizer.errors,
                        "message":res_msg.something_else(),
                        "status":status.HTTP_400_BAD_REQUEST
                    },status=status.HTTP_200_OK
                    )
            return Response(
                {
                    "data":response_data,
                    "message":res_msg.create("Account Head"),
                    "status":status.HTTP_201_CREATED
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

    def retrieve(self,request,pk):
        res_data={}
        try:
            queryset=AccountHeadDetails.objects.get(id=pk)
            serializer=AccountHeadDetailsSerailizer(queryset)
            accounthead_details=serializer.data
            accounthead_details['customer_type_name']=queryset.customer_type.customer_type_name
            accounthead_details['account_type_name']=queryset.account_type.account_type_name
            accounthead_details['group_name_name']=queryset.group_name.account_group_name

            res_data['accounthead_details']=accounthead_details

        except Exception as err:
            pass

        try:
            address_queryset=list(AccountHeadAddress.objects.filter(account_head=pk))
            address_serializer=AccountHeadAddressSerailizer(address_queryset,many=True)
            res_data['address_detail']=address_serializer.data

        except Exception as err:
            pass

        try:
            contact_queryset=list(AccountHeadContact.objects.filter(account_head=pk))
            contact_serializer=AccountHeadContactSerailizer(contact_queryset,many=True)
            res_data['contact_detail']=contact_serializer.data
        except Exception as err:
            pass
                        
        try:
            bank_queryset=list(AccountHeadBankDetails.objects.filter(account_head=pk))
            bank_serializer=AccountHeadBankDetailsSerailizer(bank_queryset,many=True)
            res_data['bank_detail']=bank_serializer.data
        except Exception as err:
            pass
        try:
            gst_queryset=AccountHeadGstDetails.objects.get(account_head=pk)
            gst_serializer=AccountHeadGstDetailsSerailizer(gst_queryset)
            res_data['gst_detail']=gst_serializer.data
        except Exception as err:
            pass
        return Response(
            {
                "data":res_data,
                "message":res_msg.retrieve("Account Head"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
    
    
    def update(self,request,pk):
        request_data=request.data
        try:
            queryset=AccountHeadDetails.objects.get(id=pk)

            accounthead_details=request_data.get('accounthead_details') if request_data.get('accounthead_details') else []
            accounthead_details['modified_at']=timezone.now()
            accounthead_details['modified_by']=request.user.id

            serializer=AccountHeadDetailsSerailizer(queryset,data=accounthead_details,partial=True)
            if serializer.is_valid():
                serializer.save()
            
            try:

                address_details=request_data.get('address_details') if request_data.get('address_details') else []


                for address in address_details:
                    try:
                        address_queryset=AccountHeadAddress.objects.get(account_head=pk,door_no=address.get('door_no'),street_name=address.get('street_name'),district=address.get('district'))
                        address['modified_at']=timezone.now()
                        address['modified_by']=request.user.id

                        address_serializer=AccountHeadAddressSerailizer(address_queryset,data=address,partial=True)

                        if address_serializer.is_valid():
                           address_serializer.save()

                    except AccountHeadAddress.DoesNotExist:
                        new_address=address

                        new_address['account_head']=pk
                        new_address['created_at']=timezone.now()
                        new_address['created_by']=request.user.id

                        new_address_serializer=AccountHeadAddressSerailizer(data=new_address)

                        if new_address_serializer.is_valid():
                            new_address_serializer.save()
                    except Exception as err:
                        pass
                try:

                    contact_details=request_data.get('contact_details') if request_data.get('contact_details') else []


                    for contact in contact_details:

                        try:
                    
                            contact_queryset=AccountHeadContact.objects.get(account_head=pk,mobile_number=contact.get('mobile_number'),std_code=contact.get('std_code'),landline_number=contact.get('landline_number'))
                            contact['modified_at']=timezone.now()
                            contact['modified_by']=request.user.id

                            contact_serializer=AccountHeadContactSerailizer(contact_queryset,data=contact,partial=True)

                            if contact_serializer.is_valid():
                               contact_serializer.save()

                        except AccountHeadContact.DoesNotExist:

                            new_contact=contact
                            new_contact['account_head']=pk
                            new_contact['created_at']=timezone.now()
                            new_contact['created_by']=request.user.id

                            new_contact_serializer=AccountHeadContactSerailizer(data=new_contact)

                            if new_contact_serializer.is_valid():
                                new_contact_serializer.save()

                        except Exception as err:
                            pass
                    try:

                        bank_details=request_data.get('bank_details') if request_data.get('bank_details') else []


                        for bank in bank_details:

                            try:
                                bank_queryset=AccountHeadBankDetails.objects.get(account_no=bank.get('account_no'),account_head=pk, ifsc_code=bank.get('ifsc_code'), micr_code=bank.get('micr_code'))
                                bank['modified_at']=timezone.now()
                                bank['modified_by']=request.user.id

                                bank_serializer=AccountHeadBankDetailsSerailizer(bank_queryset,data=bank,partial=True)

                                if bank_serializer.is_valid():
                                   bank_serializer.save()
                            except AccountHeadBankDetails.DoesNotExist:

                                new_bank=bank
                                new_bank['account_head']=pk
                                new_bank['created_at']=timezone.now()
                                new_bank['created_by']=request.user.id

                                new_bank_serializer=AccountHeadBankDetailsSerailizer(data=new_bank)

                                if new_bank_serializer.is_valid():
                                    new_bank_serializer.save()
                            except Exception as err:
                                pass
                        try:
            

                            gst_details=request_data.get('gst_details') if request_data.get('gst_details') else []
                            gst_details['modified_at']=timezone.now()
                            gst_details['modified_by']=request.user.id

                            gst_queryset=AccountHeadGstDetails.objects.get(account_head=pk)


                            gst_serializer=AccountHeadGstDetailsSerailizer(gst_queryset,data=gst_details,partial=True)

                            if gst_serializer.is_valid():
                                gst_serializer.save()

                        except Exception as err:
                            return Response(
                                {
                                    "message":res_msg.something_else(),
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
                except Exception as err:
                    return Response(
                        {
                            "message":res_msg.something_else(),
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
        except Exception as err:
            return Response(
                {
                    "message":res_msg.not_exists("Account Head"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        return Response(
            {
                "data":request_data,
                "message":res_msg.update("Account Head"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )

    def destroy(self,request,pk):
        try:
            queryset=AccountHeadDetails.objects.get(id=pk)
            queryset.delete()
            
            return Response(
                {
                    "message":res_msg.delete("Account Head"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        except AccountHeadDetails.DoesNotExist:
            return Response(
                {
                    "message":res_msg.not_exists("Account Head"),
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
        except ProtectedError:
            return Response(
                {
                    "message":res_msg.related_item("Delete"),
                    "status":status.HTTP_400_BAD_REQUEST
                },status=status.HTTP_200_OK
            )
        

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])        
class AccountHeadStatusView(APIView):
    def get(self,request,pk):

        try:
            queryset=AccountHeadDetails.objects.get(id=pk)
        except Exception as err:
            return Response(
                {
                    "message":res_msg.not_exists("Account Head"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        
        try:
            contact_queryset=AccountHeadContact.objects.filter(account_head=queryset.pk)

            for contact in contact_queryset:
                contact.is_active=not(queryset.is_active)
                contact.save()
            try:
                address_queryset=AccountHeadAddress.objects.filter(account_head=queryset.pk)

                for address in address_queryset:
                    address.is_active=not(queryset.is_active)
                    address.save()
                try:
                    bank_queryset=AccountHeadBankDetails.objects.filter(account_head=queryset.pk)

                    for bank in bank_queryset:
                        bank.is_active=not(queryset.is_active)
                        bank.save()
                    try:
                        gst_queryset=AccountHeadGstDetails.objects.get(account_head=queryset.pk)
                        gst_queryset.is_active=not(queryset.is_active)
                        gst_queryset.save()

                        queryset.is_active=not(queryset.is_active)
                        queryset.save()
                        serializer=AccountHeadDetailsSerailizer(queryset)

                        return Response(
                            {
                                "data":serializer.data,
                                "message":res_msg.change("Account Head Status"),
                                "status":status.HTTP_200_OK
                            },status=status.HTTP_200_OK
                        )

                    except Exception as err:
                        pass
                except Exception as err:
                    pass
            except Exception as err:
                pass
        except Exception as err:
            pass


        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])        
class AccountHeadListView(APIView):
    def get(self,request):
        queryset=list(AccountHeadDetails.objects.all().order_by('id').values('id','account_head_name', 'account_head_code','upi_id'))

        return Response(
            {
                "data":{
                    "list":queryset
                    },
                "message":res_msg.retrieve("Account Group"),
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
            items_per_page = int(request.data.get('items_per_page', AccountHeadDetails.objects.all().count()))
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
                queryset=AccountHeadDetails.objects.filter(Q(account_head_name__icontains=search)|Q(customer_type__customer_type_name__icontains=search)|Q(account_type__account_type_name__icontains=search)|Q(group_name__account_group_name__icontains=search),**filter_condition).order_by('id')
        elif search != '':
                queryset=AccountHeadDetails.objects.filter(Q(account_head_name__icontains=search)|Q(customer_type__customer_type_name__icontains=search)|Q(account_type__account_type_name__icontains=search)|Q(group_name__account_group_name__icontains=search)).order_by('id')
        else:
            queryset=AccountHeadDetails.objects.all().order_by('id')

        paginated_data = Paginator(queryset, items_per_page)
        serializer = AccountHeadDetailsSerailizer(paginated_data.get_page(page), many=True)

        response_data=[]

        for i in range(len(serializer.data)):
            data_dict=serializer.data[i]
            try :
                staff = Staff.objects.get(user =queryset[i].created_by)
                username = staff.first_name
            except:
                username = "-"            
            data_dict['created_by'] = username
            data_dict['account_type']=queryset[i].account_type.account_type_name
            data_dict['group_name']=queryset[i].group_name.account_group_name
            data_dict['customer_type']=queryset[i].customer_type.customer_type_name
            data_dict['upi_id']=queryset[i].upi_id if queryset[i].upi_id else "-"

            response_data.append(data_dict)

        return Response(
            {
                "data":{
                    "list": response_data,
                    "total_pages": paginated_data.num_pages,
                    "current_page": page,
                    "total_items": len(queryset),
                    "current_items": len(serializer.data)
                },
                "message":res_msg.retrieve("Account Head"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])   
class AccountHeadAddressView(APIView):

    def post(self,request):

        try:
            address_list=request.data.get('id_list') if request.data.get('id_list') else []

            for id in address_list:
                queryset=AccountHeadAddress.objects.get(id=id)
                queryset.delete()

            return Response(
                {
                    "message":res_msg.delete("Address Details"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        except AccountHeadAddress.DoesNotExist:
            return Response(
                {
                    "message":res_msg.not_exists("Address Details"),
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
class AccountHeadContactView(APIView):

    def post(self,request):

        try:

            contact_list=request.data.get('id_list') if request.data.get('id_list') else[]

            for id in contact_list:
                queryset=AccountHeadContact.objects.get(id=id)
                queryset.delete()

            return Response(
                {
                    "message":res_msg.delete("Contact Details"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        except AccountHeadContact.DoesNotExist:
            return Response(
                {
                    "message":res_msg.not_exists("Contact Details"),
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
class AccountHeadBankView(APIView):

    def post(self,request):

        try:

            bank_list=request.data.get('id_list') if request.data.get('id_list') else[]
            
            for id in bank_list:
                queryset=AccountHeadBankDetails.objects.get(id=id)
                queryset.delete()

            return Response(
                {
                    "message":res_msg.delete("Bank Details"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        except AccountHeadBankDetails.DoesNotExist:
            return Response(
                {
                    "message":res_msg.not_exists("Bank Details"),
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



def account_head_code():
    # prefix = 'ACT'  
    # random_number = random.randint(1000000, 9999999)
    # account_head_code = f'{prefix}-{random_number}'
    # return account_head_code

    try:
        queryset = AccountHeadDetails.objects.all().last()
        return 'ACT000'+str(queryset.pk + 1)
    except Exception as err:
        return 'ACT0001'
    

    
        



            
        






        
    

















