from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.response import Response
from .models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes, authentication_classes
from django.utils import timezone
from django.db.models import ProtectedError,Q
from django.core.paginator import Paginator
from app_lib.response_messages import ResponseMessages
from .serializer import *
from django.conf import settings

res_msg = ResponseMessages()

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class CustomerViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk):

        try:
            queryset = Customer.objects.get(id=pk)
        except:
            return Response({
                "message": res_msg.not_exists('Customer'),
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_200_OK)
        
        serializer = CustomerSerializer(queryset)

        res_data = serializer.data
        res_data['customer_group_name'] = queryset.customer_group.customer_group_name

        return Response({
                "data": res_data,
                "message": res_msg.retrieve('Customer'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)

    def create(self, request):
        data = request.data
     
        if request.user.role.is_admin == False:
            data['branch'] = request.user.branch.pk

        else:
            data['branch'] = data.get('branch')

        data['created_at'] = timezone.now()
        data['created_by'] = request.user.id
        serializer = CustomerSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": res_msg.create('Customer'),
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
            queryset = Customer.objects.get(id=pk)
        except Exception as err:
            return Response({
                "message": res_msg.not_exists('Customer'),
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_200_OK)
        
        data = request.data
               
        if request.user.role.is_admin == False:
            data['branch'] = request.user.branch.pk

        else:
            data['branch'] = data.get('branch')
        data['modified_at'] = timezone.now()
        data['modified_by'] = request.user.id
        serializer = CustomerSerializer(queryset, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": res_msg.update('Customer'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        return Response({
                "data": serializer.errors,
                "message": res_msg.in_valid_fields(),
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_200_OK)
    
    def destroy(self, request, pk):
        try:
            queryset = Customer.objects.get(id=pk)
            queryset.delete()
            return Response({
                "message": res_msg.delete('Customer'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        except Customer.DoesNotExist:
            return Response({
                "message": res_msg.not_exists('Customer'),
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
class CustomerList(APIView):

    def get(self, request):

        filter_condition={}
        
        if request.user.role.is_admin == False:    
            filter_condition['branch'] = int(request.user.branch.pk)
           
        filter_condition['is_active'] = True

        queryset = list(Customer.objects.filter(**filter_condition).order_by('id'))
        serializer = CustomerSerializer(queryset, many=True)

        return Response({
            "data": {
                "list": serializer.data,
            },
            "message": res_msg.retrieve('Customer'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
    
    def post(self, request):

        search = request.data.get('search') if request.data.get('search') else ''
        from_date = request.data.get('from_date')
        to_date = request.data.get('to_date')
        active_status = request.data.get('active_status')
        branch = request.data.get('branch')
        page = request.data.get('page') if request.data.get('page') else 1
        try:
            items_per_page = int(request.data.get('items_per_page', Customer.objects.all().count()))
            if items_per_page == 0:
                items_per_page = 10 
        except Exception as err:
            items_per_page = 10


        filter_condition={}

        if request.user.role.is_admin == False:
            filter_condition['branch'] = int(request.user.branch.pk)

        else:
            if branch != None:
                filter_condition['branch'] = int(branch)

        
        if search != "" :
            filter_condition['customer_name__icontains'] = search

        if from_date != None and to_date != None :
            date_range=(from_date,to_date)
            filter_condition['created_at__range'] = date_range
        # if from_date != None and to_date!= None:
        #    fdate =from_date+'T00:00:00.899010+05:30'
        #    tdate =to_date+'T23:59:59.899010+05:30'
        #    date_range=(fdate,tdate)
        #    filter_condition['created_at__range']=date_range

        if active_status != None :
            filter_condition['is_active'] = active_status

        if len(filter_condition) != 0 :

            queryset = list(Customer.objects.filter(**filter_condition).order_by('id'))

        else :

            queryset = list(Customer.objects.all().order_by('id'))
            
        paginated_data = Paginator(queryset, items_per_page)
        serializer = CustomerSerializer(paginated_data.get_page(page), many=True)

        res_data = []

        for i in range(0, len(serializer.data)):
            dict_data = serializer.data[i]
            try :
                staff = Staff.objects.get(user =queryset[i].created_by_id)
                username = staff.first_name
            except:
                username = "-"
            dict_data['created_by'] = username
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
            "message": res_msg.retrieve('Customer'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class CustomerGroupList(APIView):

    def get(self, request):

        queryset = list(CustomerGroup.objects.filter(is_active=True).order_by('id'))
        serializer = CustomerGroupSerializer(queryset, many=True)

        return Response({
            "data": {
                "list": serializer.data,
            },
            "message": res_msg.retrieve('Customer Group'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
    
    def post(self,request):

        try:

            request_data=request.data

            active_status=request_data.get('active_status')
            from_date=request_data.get('from_date')
            to_date=request_data.get('to_date')

            filter_condition={}

            if active_status != None :

                filter_condition['is_active'] = active_status

            if from_date != None  and to_date != None :

                date_range=(from_date,to_date)

                filter_condition['created_at__range']=date_range

            if len(filter_condition) != 0 :

                queryset=list(CustomerGroup.objects.filter(**filter_condition).values('id','customer_group_name','is_active','created_at'))

            else:

                queryset=list(CustomerGroup.objects.all().values('id','customer_group_name','is_active','created_at'))
            

            return Response(
                {
                    "data":{
                        "list":queryset
                    },
                    "message":res_msg.retrieve("Customer Group"),
                    "status":status.HTTP_200_OK
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
class CustomerMobileNumberAPIView(APIView):
    def get(self,request,phone=None):
        if phone != None:
            try:
                customer_queryset = Customer.objects.get(phone=phone)
                customer_serializer = CustomerSerializer(customer_queryset)
                return Response(
                {
                    "data": customer_serializer.data,
                    "message" : res_msg.retrieve("Customer Details"),
                    "status": status.HTTP_200_OK
                }, status=status.HTTP_200_OK
            )
            except Customer.DoesNotExist:
                return Response(
                {
                    "message" : res_msg.not_exists("Customer Details"),
                    "status": status.HTTP_404_NOT_FOUND
                }, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    "message" : "Invalid Mobile number",
                    "status": status.HTTP_204_NO_CONTENT
                }, status=status.HTTP_200_OK
            )
        

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class CustomerMobileBranchNumberAPIView(APIView):
    def get(self,request,phone=None,branch=None):
        if phone != None:
             return Response(
                {
                    "message" : "Mobile number  required",
                    "status": status.HTTP_204_NO_CONTENT
                }, status=status.HTTP_200_OK
            )

        elif branch != None:
             return Response(
                {
                    "message" : "Branch Id required",
                    "status": status.HTTP_204_NO_CONTENT
                }, status=status.HTTP_200_OK
            )
        else:
            try:
                customer_queryset = Customer.objects.get(phone=phone,branch=branch)
                customer_serializer = CustomerSerializer(customer_queryset)
                return Response(
                {
                    "data": customer_serializer.data,
                    "message" : res_msg.retrieve("Customer Details"),
                    "status": status.HTTP_200_OK
                }, status=status.HTTP_200_OK
            )
            except Customer.DoesNotExist:
                return Response(
                {
                    "message" : res_msg.not_exists("Customer Details"),
                    "status": status.HTTP_404_NOT_FOUND
                }, status=status.HTTP_200_OK
            )
   
           
        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class CustomerGroupView(viewsets.ViewSet):

    def create(self,request):

        try:
            
            request_data=request.data

            request_data['created_at']=timezone.now()
            request_data['created_by']=request.user.id
            
            serializer=CustomerGroupSerializer(data=request_data)

            if serializer.is_valid():
                serializer.save()

                return Response(
                    {
                        "data":serializer.data,
                        "message":res_msg.create("Customer Group"),
                        "status":status.HTTP_201_CREATED
                    },status=status.HTTP_200_OK
                )
            else:
                raise Exception(serializer.errors)
            
        except Exception as err:

            return Response(
                {
                    "data":str(err),
                    "message":res_msg.something_else(),
                    "status":status.HTTP_400_BAD_REQUEST
                },status=status.HTTP_200_OK
            )
        
    def update(self,request,pk):

        try:

            queryset=CustomerGroup.objects.get(id=pk)

            request_data=request.data

            request_data['modified_at']=timezone.now()
            request_data['modified_by']=request.user.id

            serializer=CustomerGroupSerializer(queryset,data=request_data,partial=True)

            if serializer.is_valid():
                serializer.save()

                return Response(
                    {
                        "data":serializer.data,
                        "message":res_msg.update("Customer Group"),
                        "status":status.HTTP_200_OK
                    },status=status.HTTP_200_OK
                )
            
            else:
                raise Exception(serializer.errors)
            
        except CustomerGroup.DoesNotExist:

            return Response(
                {
                    "message":res_msg.not_exists("Customer Group"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
            
        except Exception as err:

            return Response(
                {
                    "data":str(err),
                    "message":res_msg.something_else(),
                    "status":status.HTTP_400_BAD_REQUEST
                },status=status.HTTP_200_OK
            )
        
    def retrieve(self,request,pk):

        try:

            queryset=CustomerGroup.objects.get(id=pk)

            serializer=CustomerGroupSerializer(queryset)

            return Response(
                {
                    "data":serializer.data,
                    "message":res_msg.retrieve("Customer Group"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        
        except CustomerGroup.DoesNotExist:

            return Response(
                {
                    "message":res_msg.not_exists("Customer Group"),
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
        
    def delete(self,request,pk):

        try:

            queryset=CustomerGroup.objects.get(id=pk)

            queryset.delete()

            return Response(
                {
                    "message":res_msg.delete("Customer Group"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        
        except CustomerGroup.DoesNotExist:

            return Response(
                {
                    "message":res_msg.not_exists("Customer Group"),
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
class CustomerGroupStatusView(APIView):

    def get(self,request,pk):

        try:

            queryset=CustomerGroup.objects.get(id=pk)

            queryset.is_active = not(queryset.is_active)
            queryset.save()

            return Response(
                {
                    "message":res_msg.change("Customer Group Status"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        
        except CustomerGroup.DoesNotExist:

            return Response(
                {
                    "message":res_msg.not_exists("Customer Group"),
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
class ShopListView(APIView):
    def get(self,request,customer_group=None):
        
        filter_condition={}
        
        if request.user.role.is_admin == False:    
            filter_condition['branch'] = int(request.user.branch.pk)
           
        filter_condition['is_active'] = True

        if customer_group != None:
            queryset = list(Customer.objects.filter(**filter_condition,customer_group=customer_group).order_by('id'))
        else:
            queryset = list(Customer.objects.filter(**filter_condition).exclude(customer_group=settings.SHOP).order_by('id'))
            
        serializer = CustomerSerializer(queryset, many=True)

        return Response({
            "data": {
                "list": serializer.data,
            },
            "message": res_msg.retrieve('Customer'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)



@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class CustomerLedgerListView(APIView):
    
    def post(self,request):
                
        filter_condition = {}
        
        if request.user.role.is_admin == False:
            branch = request.user.branch.pk
        else:
            branch = request.data.get('branch')
            
        if branch != None:
            
            filter_condition['branch'] = branch
                
        customer_details = request.data.get('customer_details',None)
        from_date = request.data.get('from_date',None)
        to_date = request.data.get('to_date',None)
        entry_type = request.data.get('entry_type',None)
        transaction_type = request.data.get('transaction_type',None)
        cancel_status = request.data.get('cancel_status',None)
        search = request.data.get('search',"")
        page = request.data.get('page',1)
        items_per_page = request.data.get('items_per_page',10)
        
        if customer_details != None:
            
            filter_condition['customer_details'] = customer_details
            
        if from_date != None and to_date != None:
            
            date_range = (from_date,to_date)
            
            filter_condition['entry_date__range'] = date_range
            
        if entry_type != None:
            
            filter_condition['entry_type'] = entry_type
            
        if len(filter_condition) !=  0:
            
            calculation_queryset = CustomerLedger.objects.filter(**filter_condition,is_cancelled=False).order_by('-id')
            
        else:
            
            calculation_queryset = CustomerLedger.objects.filter(is_cancelled=False).order_by('-id')
            
        credit_amount = 0.0 
        debit_amount = 0.0
        credit_weight = 0.0
        debit_weight = 0.0
        
        for calculation in calculation_queryset:
            
            if calculation.transaction_type == settings.CREDIT_ENTRY:
                
                credit_amount += calculation.transaction_amount
                credit_weight += calculation.transaction_weight
                
            else:
                debit_amount += calculation.transaction_amount
                debit_weight += calculation.transaction_weight
                
        remaining_amount = credit_amount-debit_amount
        remaining_weight = credit_weight-debit_weight
        
        if transaction_type != None:
            
            filter_condition['transaction_type'] = transaction_type
            
        if cancel_status != None:
            
            filter_condition['is_cancelled'] = cancel_status
            
        combined_conditions = Q()
        
        if search != "":
            or_conditions = []
            or_conditions.append(Q(invoice_number__icontains=search))
            or_conditions.append(Q(reffrence_number__icontains=search))

            for condition in or_conditions:
                combined_conditions |= condition
            
        if len(filter_condition)!= 0 :
            
            queryset = CustomerLedger.objects.filter(combined_conditions,**filter_condition).order_by('-id')
            
        else:
            queryset = CustomerLedger.objects.filter(combined_conditions).order_by('-id')
            
        paginated_data = Paginator(queryset, items_per_page)
        serializer = CustomerLedgerSerializer(paginated_data.get_page(page), many=True)
        total_items = len(queryset)
        
        response_data = []
        
        for data in serializer.data:
            
            res_data = data
            
            customer_ledger_queryset = CustomerLedger.objects.get(id=data['id'])
            
            res_data['customer_name'] = customer_ledger_queryset.customer_details.customer_name
            res_data['branch_name'] = customer_ledger_queryset.branch.branch_name
            res_data['entry_type_name'] = customer_ledger_queryset.entry_type.entry_type_name
            res_data['transaction_type_name'] = customer_ledger_queryset.transaction_type.transaction_type
            
            response_data.append(res_data)
            
        for i in range(len(response_data)):
            
            response_data[i]['s_no'] = i+1
            
        return Response(
            {
                "data":{
                    "list":response_data,
                    "credit_amount":credit_amount,
                    "credit_weight":credit_weight,
                    "debit_amount":debit_amount,
                    "debit_weight":debit_weight,
                    "remaining_amount":remaining_amount,
                    "remaining_weight":remaining_weight,
                    "total_pages": paginated_data.num_pages,
                    "current_page": page,
                    "total_items": total_items,
                    "current_items": len(serializer.data)
                },
                "message":res_msg.retrieve("Customer Ledger Table List"),
                "status":status.HTTP_200_OK
            }
        )
            