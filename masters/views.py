from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.response import Response
from .models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes, authentication_classes
from django.utils import timezone
from django.db.models import ProtectedError
from django.core.paginator import Paginator
from app_lib.response_messages import ResponseMessages
from accounts.serializer import UserSerializer
from accounts.models import *
from .serializer import *
from django.db.models import Q
from product.models import RangeStock
from django.conf import settings
from tagging.models import TaggedItems
from django.db import transaction
from billing.models import BillingType
from billing.serializer import BillingTypeSerializer
from django.contrib.auth.hashers import make_password,check_password

res_msg = ResponseMessages()

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class MetalViewSet(viewsets.ViewSet):

    def create(self, request):

        data = request.data
        data['metal_name'] = data.get('metal_name').lower()
        data['created_at'] = timezone.now()
        data['created_by'] = request.user.id
        serializer = MetalSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            bill_type_data = {}
            bill_type_data['bill_type'] = data.get('metal_name').lower()
            billtype_serializer = BillingTypeSerializer(data=bill_type_data)
            if billtype_serializer.is_valid():
                billtype_serializer.save()
            else:
                return Response({
                "data": billtype_serializer.errors,
                "message": res_msg.not_create('Bill Type'),
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_200_OK)

            return Response({
                "data": serializer.data,
                "message": res_msg.create('Metal'),
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
            queryset = Metal.objects.get(id=pk)
        except Exception as err:
            return Response({
                "message": res_msg.not_exists('Metal'),
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_200_OK)
        
        data = request.data
        data['metal_name'] = data.get('metal_name').lower()
        data['modified_at'] = timezone.now()
        data['modified_by'] = request.user.id
        serializer = MetalSerializer(queryset, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": res_msg.update('Metal'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        return Response({
                "data": serializer.errors,
                "message": res_msg.in_valid_fields(),
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_200_OK)
    
    def destroy(self, request, pk):
        try:
            queryset = Metal.objects.get(id=pk)
            queryset.delete()
            return Response({
                "message": res_msg.delete('Metal'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        except Metal.DoesNotExist:
            return Response({
                "message": res_msg.not_exists('Metal'),
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
class MetalList(APIView):

    def get(self, request):

        queryset = list(Metal.objects.filter(is_active=True).order_by('id'))
        
        res_data = []
        for data in queryset:
            dict_data = {}
            dict_data['id']=data.pk
            dict_data['metal_name']=data.metal_name
            dict_data['metal_code']=data.metal_code

            old_metal_rate_queryset = MetalOldRate.objects.filter(metal=data.pk).order_by('id').first()

            try:

                dict_data['old_metal_rate'] = old_metal_rate_queryset.old_metal_rate
            except:
                dict_data['old_metal_rate']=0
            
            res_data.append(dict_data)
           
        return Response({
            "data": {
                "list": res_data,
            },
            "message": res_msg.retrieve('Metal'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
    
    def post(self, request):

        search = request.data.get('search') if request.data.get('search') else ''
        from_date = request.data.get('from_date') if request.data.get('from_date') else None
        to_date = request.data.get('to_date') if request.data.get('to_date') else None
        active_status = request.data.get('active_status') if request.data.get('active_status') != None else None
        page = request.data.get('page') if request.data.get('page') else 1
        try:
            items_per_page = int(request.data.get('items_per_page', Metal.objects.all().count()))
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
                queryset = list(Metal.objects.filter(Q(metal_name__icontains=search) | Q(metal_code__icontains=search),**filter_condition).order_by('id'))
        elif search != '':
                queryset = list(Metal.objects.filter(Q(metal_name__icontains=search) | Q(metal_code__icontains=search)).order_by('id'))
        else:
            queryset = list(Metal.objects.filter(Q(metal_name__icontains=search) | Q(metal_code__icontains=search)).order_by('id'))
        
        paginated_data = Paginator(queryset, items_per_page)
        serializer = MetalSerializer(paginated_data.get_page(page), many=True)

        return Response({
            "data": {
                "list": serializer.data,
                "total_pages": paginated_data.num_pages,
                "current_page": page,
                "total_items": len(queryset),
                "current_items": len(serializer.data)
            },
            "message": res_msg.retrieve('Metal'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
    

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class MetalStatus(APIView):

    def get(self, request, pk=None):

        if pk != None:
            try:
                queryset = Metal.objects.get(id=pk)
            except Exception as err:
                return Response({
                    "message": res_msg.not_exists('Metal'),
                    "status": status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_200_OK)

            if not(queryset.is_active) == False:
                try:
                    purity_queryset = list(Purity.objects.filter(metal=pk))

                    for i in purity_queryset:
                        PurityStatus().get(request, i.pk, not(queryset.is_active))
                except:
                    pass

                try:
                    tag_queryset = list(TagTypes.objects.filter(metal=pk))

                    for i in tag_queryset:
                        TagTypeStatusView().get(request, i.pk, not(queryset.is_active))
                except:
                    pass
            
        queryset.is_active = not(queryset.is_active)
        queryset.save()

        serializer = MetalSerializer(queryset)

        return Response({
                "data": serializer.data,
                "message": res_msg.update('Metal status'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
  
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class PurityViewSet(viewsets.ViewSet):

    def create(self, request):

        data = request.data
        data['created_at'] = timezone.now()
        data['created_by'] = request.user.id
        serializer = PuritySerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": res_msg.create('Purity'),
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
            queryset = Purity.objects.get(id=pk)
        except Exception as err:
            return Response({
                "message": res_msg.not_exists('Purity'),
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_200_OK)
        
        data = request.data
        data['purity_name'] = data.get('purity_name')
        data['modified_at'] = timezone.now()
        data['modified_by'] = request.user.id
        serializer = PuritySerializer(queryset, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            
            return Response({
                "data": serializer.data,
                "message": res_msg.update('Purity'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        
        return Response({
                "data": serializer.errors,
                "message": res_msg.in_valid_fields(),
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_200_OK)
    
    def destroy(self, request, pk):
        try:
            queryset = Purity.objects.get(id=pk)
            queryset.delete()
            return Response({
                "message": res_msg.delete('Purity'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        except Purity.DoesNotExist:
            return Response({
                "message": res_msg.not_exists('Purity'),
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
class PurityList(APIView):  

    def get(self, request,pk=None):

        if pk != None:
            queryset=list(Purity.objects.filter(is_active=True,metal=pk).order_by('id').values('id','purity_name','purity_code','metal__metal_name'))
        else:
            queryset = list(Purity.objects.filter(is_active=True).order_by('id').values('id','purity_name','purity_code','metal__metal_name'))

        return Response({
            "data": {
                "list": queryset,
            },
            "message": res_msg.retrieve('Purity'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
    
    def post(self, request):

        search = request.data.get('search') if request.data.get('search') else ''
        from_date = request.data.get('from_date') if request.data.get('from_date') else None
        to_date = request.data.get('to_date') if request.data.get('to_date') else None
        active_status = request.data.get('active_status') if request.data.get('active_status') != None else None
        page = request.data.get('page') if request.data.get('page') else 1
        try:
            items_per_page = int(request.data.get('items_per_page', Purity.objects.all().count()))
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
            queryset = list(Purity.objects.filter(Q(purity_name__icontains=search) | Q(metal__metal_name__icontains=search) | Q(purity_code__icontains=search),**filter_condition).order_by('id'))
        elif search != '':
            queryset = list(Purity.objects.filter(Q(purity_name__icontains=search) | Q(metal__metal_name__icontains=search) | Q(purity_code__icontains=search)).order_by('id'))
        else:
            queryset = list(Purity.objects.filter(Q(purity_name__icontains=search) | Q(metal__metal_name__icontains=search) | Q(purity_code__icontains=search)).order_by('id'))

        paginated_data = Paginator(queryset, items_per_page)
        serializer = PuritySerializer(paginated_data.get_page(page), many=True)
        
        res_data = []
        for i in range(0, len(serializer.data)):
            dict_data = serializer.data[i]
            dict_data['metal_name'] = queryset[i].metal.metal_name

            res_data.append(dict_data)

        return Response({
            "data": {
                "list": serializer.data,
                "total_pages": paginated_data.num_pages,
                "current_page": page,
                "total_items": len(queryset),
                "current_items": len(serializer.data)
            },
            "message": res_msg.retrieve('Purity'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class PurityStatus(APIView):

    def get(self, request, pk=None, active=None):

        if pk != None:
            try:
                queryset = Purity.objects.get(id=pk)
            except Exception as err:
                return Response({
                    "message": res_msg.not_exists('Purity'),
                    "status": status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_200_OK)
            
            if not(queryset.is_active):
                try:
                    metal_queryset = Metal.objects.get(id=queryset.metal.pk, is_active=True)
                    pass
                except Metal.DoesNotExist:
                    return Response({
                        "message": res_msg.activate(queryset.metal.metal_name + ' metal'),
                        "status": status.HTTP_204_NO_CONTENT
                    }, status=status.HTTP_200_OK)
            
        queryset.is_active = active if active != None else not(queryset.is_active)
        queryset.save()

        serializer = PuritySerializer(queryset)

        if active != None:
            return

        return Response({
                "data": serializer.data,
                "message": res_msg.update('Purity status'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
    
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# class PurityVisible(APIView):

#     def get(self, request, pk=None):
#         if pk != None:
#             try:
#                 queryset = Purity.objects.get(id=pk)
#             except Exception as err:
#                 return Response({
#                     "message": res_msg.not_exists('Purity'),
#                     "status": status.HTTP_400_BAD_REQUEST
#                 }, status=status.HTTP_200_OK)
           
#         all_queryset = list(Purity.objects.filter(is_visible=True))
        
#         if not(queryset.is_visible):
            
#             for i in all_queryset:
#                 if i.metal.pk == queryset.metal.pk:
#                     i.is_visible = False
#                     i.save()
#                     queryset.is_visible = not(queryset.is_visible)
#                     queryset.save()
#                     serializer = PuritySerializer(queryset)

#                     return Response({
#                         "data": serializer.data,
#                         "message": res_msg.update('Purity visible'),
#                         "status": status.HTTP_200_OK
#                     }, status=status.HTTP_200_OK)
                    
#         else:
#             for i in all_queryset:
#                 if i.metal.pk != queryset.metal.pk:
#                     return Response({
#                         "message": "Any one of the gold value is visible for display value",
#                         "status": status.HTTP_200_OK
#                     }, status=status.HTTP_200_OK)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class PurityVisible(APIView):
 
    def get(self, request, pk=None):
        if pk != None:
            try:
                queryset = Purity.objects.get(id=pk)
                if queryset.is_visible == False:                    
                   Purity.objects.filter(metal=queryset.metal).update(is_visible=False)
                   Purity.objects.filter(id=pk).update(is_visible=True)
 
                else:
                   
                    Purity.objects.filter(id=pk).update(is_visible=False)
                return Response({
                    "message": res_msg.update('Purity visible'),
                    "status": status.HTTP_200_OK
                }, status=status.HTTP_200_OK)
            except Exception as err:
                return Response({
                    "message": res_msg.not_exists('Purity'),
                    "status": status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_200_OK)  
   
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class MetalRateViewSet(viewsets.ViewSet):

    def create(self, request):

        data = request.data
        data['created_at'] = timezone.now()
        data['created_by'] = request.user.id
        serializer = MetalRateSerializer(data=data)


        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": res_msg.create('MetalRate'),
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
            queryset = MetalRate.objects.get(id=pk)
        except Exception as err:
            return Response({
                "message": res_msg.not_exists('MetalRate'),
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_200_OK)
        
        data = request.data
        data['modified_at'] = timezone.now()
        data['modified_by'] = request.user.id
        serializer = MetalRateSerializer(queryset, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": res_msg.update('MetalRate'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        return Response({
                "data": serializer.errors,
                "message": res_msg.in_valid_fields(),
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_200_OK)
    
    def destroy(self, request, pk):
        try:
            queryset = MetalRate.objects.get(id=pk)
            queryset.delete()
            return Response({
                "message": res_msg.delete('MetalRate'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        except MetalRate.DoesNotExist:
            return Response({
                "message": res_msg.not_exists('MetalRate'),
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
class MetalRateList(APIView):

    def get(self, request):

        queryset = MetalRate.objects.all().order_by('id')
        serializer = MetalRateSerializer(queryset, many=True)

        return Response({
            "data": {
                "list": serializer.data,
            },
            "message": res_msg.retrieve('MetalRate'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
    
    def post(self, request):

        search = request.data.get('search') if request.data.get('search') else ''
        from_date = request.data.get('from_date') if request.data.get('from_date') else None
        to_date = request.data.get('to_date') if request.data.get('to_date') else None
        active_status = request.data.get('active_status') if request.data.get('active_status') != None else None
        page = request.data.get('page') if request.data.get('page') else 1
        try:
            items_per_page = int(request.data.get('items_per_page', MetalRate.objects.all().count()))
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
                queryset = list(MetalRate.objects.filter(**filter_condition).order_by('id'))
        elif search != '':
                queryset = list(MetalRate.objects.filter(**filter_condition).order_by('id'))
        else:
            queryset = list(MetalRate.objects.all().order_by('id'))

        paginated_data = Paginator(queryset, items_per_page)
        serializer = MetalRateSerializer(paginated_data.get_page(page), many=True)

        return Response({
            "data": {
                "list": serializer.data,
                "total_pages": paginated_data.num_pages,
                "current_page": page,
                "total_items": len(queryset),
                "current_items": len(serializer.data)
            },
            "message": res_msg.retrieve('Metal Rate'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
    
def DeleteTax(pk):

    try:

        tax_queryset=TaxDetails.objects.get(id=pk)
        tax_queryset.delete()

    except:
        pass


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class TaxDetailsViewset(viewsets.ViewSet):

    def create(self,request):
        try:
            
            request_data=request.data
            response_data={}

            tax_details=request_data.get('tax_details')
            tax_details['created_at']=timezone.now()
            tax_details['created_by']=request.user.id

            serializer=TaxDetailsSerializer(data=tax_details)

            if serializer.is_valid():
                serializer.save()
                tax_id=serializer.data['id']
                response_data['tax_details']=serializer.data

                purchase_details=request_data.get('purchase_details')

                purchase_details['tax_details']=serializer.data['id']
                purchase_details['created_at']=timezone.now()
                purchase_details['created_by']=request.user.id

                purchase_serializer=PurchaseTaxDetailsSerializer(data=purchase_details)



                if purchase_serializer.is_valid():
                    purchase_serializer.save()
                    response_data['purchase_details']=purchase_serializer.data

                    
                    sales_details=request_data.get('sales_details')

                    sales_details['tax_details']=serializer.data['id']
                    sales_details['created_at']=timezone.now()
                    sales_details['created_by']=request.user.id

                    sales_serializer=SalesTaxDetailsSerializer(data=sales_details)

                    if sales_serializer.is_valid():
                        sales_serializer.save()
                        response_data['sales_details']=sales_serializer.data
                    else:
                       raise Exception(sales_serializer.errors)
                else:
                    raise Exception(purchase_serializer.errors)
                return Response(
                {
                    "data":response_data,
                    "message":res_msg.create("Tax Details"),
                    "status":status.HTTP_201_CREATED
                },status=status.HTTP_200_OK
            )
            else:
                raise Exception(serializer.errors)
        except Exception as err:
            try:
                DeleteTax(tax_id)
            except:
                pass

            return Response(
                {
                    "data":str(err),
                    "message":res_msg.not_create("Tax Details"),
                    "status":status.HTTP_204_NO_CONTENT
                },status=status.HTTP_200_OK
            )

    def retrieve(self,request,pk):
        try:
            response_data={}

            queryset=TaxDetails.objects.get(id=pk)

            serializer=TaxDetailsSerializer(queryset)
            response_data['tax_details']=serializer.data

            try:

                purcahse_queryset=PurchaseTaxDetails.objects.get(tax_details=queryset.pk)

                purchase_serializer=PurchaseTaxDetailsSerializer(purcahse_queryset)
                response_data['purchase_details']=purchase_serializer.data

                try:
                    sales_queryset=SalesTaxDetails.objects.get(tax_details=queryset.pk)

                    sales_serailizer=SalesTaxDetailsSerializer(sales_queryset)
                    response_data['sales_details']=sales_serailizer.data

                    return Response(
                        {
                            "data":response_data,
                            "message":res_msg.retrieve("Tax Details"),
                            "status":status.HTTP_200_OK
                        },status=status.HTTP_200_OK
                    )

                except Exception as err:
                    return Response(
                        {
                           "data":response_data,
                           "message":res_msg.retrieve("Tax Details"),
                           "status":status.HTTP_200_OK
                        },status=status.HTTP_200_OK
                    )

            except Exception as err:
                return Response(
                    {
                        "data":response_data,
                        "messsage":res_msg.retrieve("Tax Details"),
                        "status":status.HTTP_200_OK
                    },status=status.HTTP_200_OK
                )

        except Exception as err:
            return Response(
                {
                    "message":res_msg.not_exists("Tax Details"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        
    def update(self,request,pk):
        try:
            queryset=TaxDetails.objects.get(id=pk)

        except Exception as err:
            return Response(
                {
                    "message":res_msg.not_exists("Tax Details"),
                    "status":status.HTTP_404_NOT_FOUND,
                },status=status.HTTP_200_OK
            )
        request_data=request.data

        response_data={}

        tax_details=request_data.get('tax_details') if request_data.get('tax_details') else []
        tax_details['modified_at']=timezone.now()
        tax_details['modified_by']=request.user.id

        serializer=TaxDetailsSerializer(queryset,data=tax_details,partial=True)

        if serializer.is_valid():
            serializer.save()
            response_data['tax_details']=serializer.data

        purchase_queryset=PurchaseTaxDetails.objects.get(tax_details=queryset.pk)

        purchase_details=request_data.get('purchase_details') if request_data.get('purchase_details') else []
        purchase_details['modified_at']=timezone.now()
        purchase_details['modified_by']=request.user.id

        purchase_serializer=PurchaseTaxDetailsSerializer(purchase_queryset,data=purchase_details,partial=True)

        if purchase_serializer.is_valid():
            purchase_serializer.save()
            response_data['purchase_details']=purchase_serializer.data

        sales_queryset=SalesTaxDetails.objects.get(tax_details=queryset.pk)

        sales_details=request_data.get("sales_details")
        sales_details['modified_at']=timezone.now()
        sales_details['modified_by']=request.user.id

        sales_serializer=SalesTaxDetailsSerializer(sales_queryset,data=sales_details,partial=True)

        if sales_serializer.is_valid():
            sales_serializer.save()
            response_data['sales_details']=sales_serializer.data

        return Response(
            {
                "data":response_data,
                "message":res_msg.update("Tax Details"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
    
    def destroy(self,request,pk):
        try:
            queryset=TaxDetails.objects.get(id=pk)
            queryset.delete()

        except TaxDetails.DoesNotExist:
            return Response(
                {
                    "message":res_msg.not_exists("Tax Details"),
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
        
        return Response(
            {
                "message":res_msg.delete("Tax Details"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class TaxDetailList(APIView):

    def post(self,request):

        search = request.data.get('search') if request.data.get('search') else ''
        active_status = request.data.get('active_status') if request.data.get('active_status') != None else None
        from_date = request.data.get('from_date') if request.data.get('from_date') else None
        to_date = request.data.get('to_date') if request.data.get('to_date') else None
        page = request.data.get('page') if request.data.get('page') else 1
        try:
            items_per_page = int(request.data.get('items_per_page', TaxDetails.objects.all().count()))
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
            queryset=list(TaxDetails.objects.filter(Q(tax_name__icontains=search) | Q(metal__metal_name__icontains=search) | Q(tax_code__icontains=search),**filter_condition).order_by('id'))
        elif search != '':
            queryset=list(TaxDetails.objects.filter(Q(tax_name__icontains=search)  | Q(metal__metal_name__icontains=search) | Q(tax_code__icontains=search)).order_by('id'))
        else:
            queryset=list(TaxDetails.objects.all().order_by('id'))

        paginated_data = Paginator(queryset, items_per_page)
        serializer = TaxDetailsSerializer(paginated_data.get_page(page), many=True)
        
        response_data=[]

        for i in range(0, len(serializer.data)):
            
            # purchase_queryset=PurchaseTaxDetails.objects.get(tax_details=queryset[i].pk)

            # sales_queryset=SalesTaxDetails.objects.get(tax_details=queryset[i].pk)

            # purchase_serializer=PurchaseTaxDetailsSerializer(purchase_queryset)
            # sales_serializer=SalesTaxDetailsSerializer(sales_queryset)
            
            res_data={}
            res_data['id']=queryset[i].pk
            res_data['metal_name']=queryset[i].metal.metal_name
            res_data['tax_code']=queryset[i].tax_code
            res_data['tax_name']=queryset[i].tax_name
            res_data['is_active']=queryset[i].is_active

            response_data.append(res_data)
            
        return Response(
            {
                "data": {
                    "list": response_data,
                    "total_pages": paginated_data.num_pages,
                    "current_page": page,
                    "total_items": len(queryset),
                    "current_items": len(serializer.data)
                },
                "message":res_msg.retrieve("Tax Details"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
       
    
    def get(self,request):

        try:
            queryset=list(TaxDetails.objects.filter(is_active=True).values('id','tax_name','tax_code').order_by('id'))

            return Response(
                {
                    "data":{
                        "list":queryset
                    },
                    "message":res_msg.retrieve("Tax Details"),
                    "status":status.HTTP_200_OK
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
class TaxDetailStatusView(APIView):
    
    def get(self,request,pk):

        try:

            queryset=TaxDetails.objects.get(id=pk)

            queryset.is_active=not(queryset.is_active)
            queryset.save()

        except Exception as err:
            return Response(
                {
                    "message":res_msg.not_update("Tax Detail Status"),
                    "status":status.HTTP_400_BAD_REQUEST
                },status=status.HTTP_200_OK
            )
        serializer=TaxDetailsSerializer(queryset)
        return Response(
                {
                    "data":serializer.data,
                    "message":res_msg.change("Tax Detail status"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ShapeDetailsviewset(viewsets.ViewSet):
    
    def create(self,request):
        request_data=request.data


        request_data['created_at']=timezone.now()
        request_data['created_by']=request.user.id


        serializer=ShapeDetailsSerializer(data=request_data)


        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "data":serializer.data,
                    "message":res_msg.create("Shape"),
                    "status":status.HTTP_201_CREATED
                },status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    "data":serializer.errors,
                    "message":res_msg.not_create("Shape"),
                    "status":status.HTTP_400_BAD_REQUEST
                },status=status.HTTP_200_OK
            )
    
    def update(self,request,pk):
        
        try:
            queryset=ShapeDetails.objects.get(id=pk)

            request_data=request.data
            request_data['modified_at']=timezone.now()
            request_data['modified_by']=request.user.id

            serializer=ShapeDetailsSerializer(queryset,data=request_data,partial=True)

            if serializer.is_valid():
                serializer.save()

                return Response(
                    {
                        "data":serializer.data,
                        "message":res_msg.update("Shape Details"),
                        "status":status.HTTP_200_OK
                    },status=status.HTTP_200_OK
                )


        except Exception as err:

            return Response(
                {
                    "message":res_msg.not_exists("Shape Details"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        
    def retrieve(self,request,pk):

        try:
            queryset=ShapeDetails.objects.get(id=pk)

            serializer=ShapeDetailsSerializer(queryset)

            return Response(
                {
                    "data":serializer.data,
                    "message":res_msg.retrieve("Shape Details"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        
        except Exception as err:
            return Response(
                {
                    "message":res_msg.not_exists("Shape Details"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        
    def destroy(self,request,pk):
        try:
            queryset=ShapeDetails.objects.get(id=pk)

            queryset.delete()

            return Response(
                {
                    "message":res_msg.delete("Shape Details"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        except ProtectedError:
            return Response(
                {
                    "message":res_msg.related_item("Please Delete "),
                    "status":status.HTTP_400_BAD_REQUEST
                },status=status.HTTP_200_OK
            )
        except Exception as err:
            return Response(
                {
                    "message":res_msg.not_exists("Shape Details"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ShapeDetailListView(APIView):
    
    def get(self,request):

        try:
            
            queryset=ShapeDetails.objects.all().values('id','shape_name').order_by('id')

            return Response(
                {
                    "data":{
                        "list":queryset
                    },
                    "message":res_msg.retrieve("Shape Details"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        except Exception as err:
            return Response(
                {
                    "message":res_msg.something_else(),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        
    def post(self,request):
        
        search = request.data.get('search') if request.data.get('search') else ''
        active_status=request.data.get('active_status') if request.data.get('active_status') != None else None
        from_date=request.data.get('from_date') if request.data.get('from_date') else None
        to_date=request.data.get('to_date') if request.data.get('to_date') else None
        page = request.data.get('page') if request.data.get('page') else 1
        try:
            items_per_page = int(request.data.get('items_per_page', ShapeDetails.objects.all().count()))
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
            queryset=list(ShapeDetails.objects.filter(shape_name__icontains=search,**filter_condition).order_by('id'))
        elif search != '':
            queryset=list(ShapeDetails.objects.filter(shape_name__icontains=search).order_by('id'))
        else:
            queryset=list(ShapeDetails.objects.all().order_by('id'))
        
        paginated_data = Paginator(queryset, items_per_page)
        serializer = ShapeDetailsSerializer(paginated_data.get_page(page), many=True)
      
        return Response(
            {
                "data": {
                    "list": serializer.data,
                    "total_pages": paginated_data.num_pages,
                    "current_page": page,
                    "total_items": len(queryset),
                    "current_items": len(serializer.data)
                },
                "message":res_msg.retrieve("Shape Details"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ShapeStatusView(APIView):
    def get(self,request,pk):

        try:
            queryset=ShapeDetails.objects.get(id=pk)

            queryset.is_active=not(queryset.is_active)
            queryset.save()
            serializer=ShapeDetailsSerializer(queryset)

            try:
                caratrate_queryset=list(CaratRate.objects.filter(shape=pk))

                for data in caratrate_queryset:
                    if queryset.is_active==True:
                        if data.cut.is_active==True:
                            if data.color.is_active==True:
                                if data.clarity.is_active==True:
                                    if data.cent_group.is_active==True:
                                        if data.stone.is_active==True:
                                            data.is_active=queryset.is_active
                                            data.save()
                                        else:
                                            pass
                                    else:
                                        pass
                                else:
                                    pass
                            else:
                                pass
                        else:
                            pass
                    else:
                        data.is_active=queryset.is_active
                        data.save()
                return Response(
                    {
                        "data":serializer.data,
                        "message":res_msg.change("Shape Detail Status"),
                        "status":status.HTTP_200_OK
                    },status=status.HTTP_200_OK
                )
                        
            except Exception as err:
                return Response(
                {
                    "message":res_msg.not_update("Shape Detail Status"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )

            
        except ShapeDetails.DoesNotExist:
            return Response(
                {
                    "message":res_msg.not_update("Shape Detail Status"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )

        except Exception as err:
            return Response(
                {
                    "message":res_msg.not_update("Shape Detail Status"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class CutDetailsViewset(viewsets.ViewSet):
    def create(self,request):

        request_data=request.data

        request_data['created_at']=timezone.now()
        request_data['created_by']=request.user.id

        serializer=CutDetailsSerializer(data=request_data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "data":serializer.data,
                    "message":res_msg.create("Cut Details"),
                    "status":status.HTTP_201_CREATED
                },status=status.HTTP_200_OK
            )
        
        else:
            return Response(
                {
                    "data":serializer.errors,
                    "message":res_msg.not_create("Cut Details"),
                    "status":status.HTTP_400_BAD_REQUEST
                },status=status.HTTP_200_OK
            )
        
    def update(self,request,pk):

        request_data=request.data
        try:
            queryset=CutDetails.objects.get(id=pk)

            request_data['modified_at']=timezone.now()
            request_data['modified_by']=request.user.id

            serializer=CutDetailsSerializer(queryset,data=request_data,partial=True)

            if serializer.is_valid():
                serializer.save()

                return Response(
                    {
                        "data":serializer.data,
                        "message":res_msg.update("Cut Details"),
                        "status":status.HTTP_200_OK
                    },status=status.HTTP_200_OK
                )
            
            else:
                return Response(
                    {
                        "data":serializer.errors,
                        "message":res_msg.not_update("Cut Details"),
                        "status":status.HTTP_400_BAD_REQUEST
                    },status=status.HTTP_200_OK
                )
        except Exception as err:
            return Response(
                {
                    "message":res_msg.not_exists("Cut Details"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        
    def retrieve(self,request,pk):

        try:
            queryset=CutDetails.objects.get(id=pk)

            serializer=CutDetailsSerializer(queryset)

            return Response(
                {
                    "data":serializer.data,
                    "message":res_msg.retrieve("Cut Details"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        except Exception as err:
            return Response(
                {
                    "message":res_msg.not_exists("Cut Details"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
    
    def destroy(self,request,pk):

        try:
            queryset=CutDetails.objects.get(id=pk)

            queryset.delete()

            return Response(
                {
                    "message":res_msg.delete("Cut Details"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        except ProtectedError:
            return Response(
                {
                    "message":res_msg.related_item("Please Delete "),
                    "status":status.HTTP_400_BAD_REQUEST
                },status=status.HTTP_200_OK
            )
        except Exception as err:
            return Response(
                {
                    "message":res_msg.not_exists("Cut Details"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class CutStatusView(APIView):
    def get(self,request,pk):

        try:
            queryset=CutDetails.objects.get(id=pk)

            queryset.is_active=not(queryset.is_active)
            queryset.save()

            serializer=CutDetailsSerializer(queryset)

            try:
                caratrate_queryset=list(CaratRate.objects.filter(cut=pk))

                for data in caratrate_queryset:
                    if queryset.is_active==True:
                        if data.shape.is_active==True:
                            if data.color.is_active==True:
                                if data.clarity.is_active==True:
                                    if data.cent_group.is_active==True:
                                        if data.stone.is_active==True:
                                            data.is_active=queryset.is_active
                                            data.save()
                                        else:
                                            pass
                                    else:
                                        pass
                                else:
                                    pass
                            else:
                                pass
                        else:
                            pass
                    else:
                        data.is_active=queryset.is_active
                        data.save()
                return Response(
                    {
                        "data":serializer.data,
                        "message":res_msg.change("Cut Detail Status"),
                        "status":status.HTTP_200_OK
                    },status=status.HTTP_200_OK
                )
            except Exception as err:
                return Response(
                {
                    "message":res_msg.not_update("Cut Details"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        except Exception as err:
            return Response(
                {
                    "message":res_msg.not_exists("Cut Details"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class CutListView(APIView):
    
    def get(self,request):

        queryset=list(CutDetails.objects.filter(is_active=True).values('id','cut_name').order_by('id'))

        return Response(
            {
                "data": {
                    "list": queryset
                },
                "message":res_msg.retrieve("Cut Details"),
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
            items_per_page = int(request.data.get('items_per_page', CutDetails.objects.all().count()))
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
            queryset=list(CutDetails.objects.filter(cut_name__icontains=search,**filter_condition).order_by('id'))
        elif search != '':
            queryset=list(CutDetails.objects.filter(cut_name__icontains=search).order_by('id'))
        else:
            queryset=list(CutDetails.objects.all().order_by('id'))

        paginated_data = Paginator(queryset, items_per_page)
        serializer = CutDetailsSerializer(paginated_data.get_page(page), many=True)

        return Response(
            {
                "data": {
                    "list": serializer.data,
                    "total_pages": paginated_data.num_pages,
                    "current_page": page,
                    "total_items": len(queryset),
                    "current_items": len(serializer.data)
                },
                "message":res_msg.retrieve("Cut Details"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ColourDetailViewset(viewsets.ViewSet):
    def create(self,request):

        request_data=request.data

        request_data['created_at']=timezone.now()
        request_data['created_by']=request.user.id

        serializer=ColorDetailsSerializer(data=request_data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "data":serializer.data,
                    "message":res_msg.retrieve("Colour Details"),
                    "status":status.HTTP_201_CREATED
                },status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    "data":serializer.errors,
                    "message":res_msg.not_create("Colour Details"),
                    "status":status.HTTP_400_BAD_REQUEST
                },status=status.HTTP_200_OK
            )
    
    def retrieve(self,request,pk):

        try:
            queryset=ColorDetails.objects.get(id=pk)

            serializer=ColorDetailsSerializer(queryset)

            return Response(
                {
                    "data":serializer.data,
                    "message":res_msg.retrieve("Colour Details"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )

        except Exception as err:
            return Response(
                {
                    "message":res_msg.not_exists("Colour Details"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        
    def update(self,request,pk):

        try:

            request_data=request.data
            request_data['modified_at']=timezone.now()
            request_data['modified_by']=request.user.id

            queryset=ColorDetails.objects.get(id=pk)

            serializer=ColorDetailsSerializer(queryset,data=request_data,partial=True)

            if serializer.is_valid():
                serializer.save()

                return Response(
                    {
                        "data":serializer.data,
                        "message":res_msg.update("Colour Details"),
                        "status":status.HTTP_200_OK
                    },status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        "data":serializer.errors,
                        "message":res_msg.not_update("Colour Details"),
                        "status":status.HTTP_400_BAD_REQUEST
                    },status=status.HTTP_200_OK
                )
            
        except Exception as err:
            return Response(
                {
                    "message":res_msg.not_exists("Colour Details"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        
    def destroy(self,request,pk):

        try:
            queryset=ColorDetails.objects.get(id=pk)

            queryset.delete()

            return Response(
                {
                    "message":res_msg.delete("Colour Details"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        except ProtectedError:
            return Response(
                {
                    "message":res_msg.related_item("Please Delete "),
                    "status":status.HTTP_400_BAD_REQUEST
                },status=status.HTTP_200_OK
            )
        except Exception as err:
            return Response(
                {
                    "message":res_msg.not_exists("Colour Details"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ColourStatusView(APIView):
    
    def get(self,request,pk):
        try:
            queryset=ColorDetails.objects.get(id=pk)

            queryset.is_active=not(queryset.is_active)
            queryset.save()

            serializer=ColorDetailsSerializer(queryset)

            try:
                caratrate_queryset=list(CaratRate.objects.filter(color=pk))

                for data in caratrate_queryset:
                    if queryset.is_active==True:
                        if data.shape.is_active==True:
                            if data.cut.is_active==True:
                                if data.clarity.is_active==True:
                                    if data.cent_group.is_active==True:
                                        if data.stone.is_active==True:
                                            data.is_active=queryset.is_active
                                            data.save()
                                        else:
                                            pass
                                    else:
                                        pass
                                else:
                                    pass
                            else:
                                pass
                        else:
                            pass
                    else:
                        data.is_active=queryset.is_active
                        data.save()

                return Response(
                    {
                        "data":serializer.data,
                        "message":res_msg.change("Colour Details Status"),
                        "status":status.HTTP_200_OK
                    },status=status.HTTP_200_OK
                )
            except Exception as err:
                return Response(
                {
                    "message":res_msg.not_update("Colour Details"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        except Exception as err:
            return Response(
                {
                    "message":res_msg.not_exists("Colour Details"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ColourListView(APIView):

    def get(self,request):

        queryset=list(ColorDetails.objects.filter(is_active=True).values('id','color_name').order_by('id'))

        return Response(
            {
                "data": {
                    "list": queryset
                },
                "message":res_msg.retrieve("Color Details"),
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
            items_per_page = int(request.data.get('items_per_page', ColorDetails.objects.all().count()))
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
            queryset=list(ColorDetails.objects.filter(color_name__icontains=search,**filter_condition).order_by('id'))
        elif search != '':
            queryset=list(ColorDetails.objects.filter(color_name__icontains=search).order_by('id'))
        else:
            queryset=list(ColorDetails.objects.all().order_by('id'))
        
        paginated_data = Paginator(queryset, items_per_page)
        serializer = ColorDetailsSerializer(paginated_data.get_page(page), many=True)
           
        return Response(
            {
                "data": {
                    "list": serializer.data,
                    "total_pages": paginated_data.num_pages,
                    "current_page": page,
                    "total_items": len(queryset),
                    "current_items": len(serializer.data)
                },
                "message":res_msg.retrieve("Colour Details"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ClarityDetailsViewset(viewsets.ViewSet):
    def create(self,request):
         
        request_data=request.data
        request_data['created_at']=timezone.now()
        request_data['created_by']=request.user.id

        serializer=ClarityDetailsSerializer(data=request_data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "data":serializer.data,
                    "message":res_msg.create("Clarity Details"),
                    "status":status.HTTP_201_CREATED
                },status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    "data":serializer.errors,
                    "message":res_msg.not_create("Clarity Details"),
                    "status":status.HTTP_400_BAD_REQUEST
                },status=status.HTTP_200_OK
            )
    def retrieve(self,request,pk):

        try:
            queryset=ClarityDetails.objects.get(id=pk)

            serializer=ClarityDetailsSerializer(queryset)
            return Response(
                {
                    "data":serializer.data,
                    "message":res_msg.retrieve("Clarity Details"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        except Exception as err:
            return Response(
                {
                    "message":res_msg.not_exists("Clarity Details"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
    def update(self,request,pk):

        try:
            request_data=request.data
            request_data['modified_at']=timezone.now()
            request_data['modified_by']=request.user.id

            queryset=ClarityDetails.objects.get(id=pk)

            serializer=ClarityDetailsSerializer(queryset,data=request_data,partial=True)

            if serializer.is_valid():
                serializer.save()

                return Response(
                    {
                        "data":serializer.data,
                        "message":res_msg.update("Clarity Details"),
                        "status":status.HTTP_200_OK
                    },status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        "data":serializer.errors,
                        "message":res_msg.not_update("Clarity Details"),
                        "status":status.HTTP_400_BAD_REQUEST
                    },status=status.HTTP_200_OK)
        except Exception as err:
            return Response(
                {
                    "message":res_msg.not_exists("Clarity Details"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        
    def destroy(self,request,pk):
        try:
            queryset = ClarityDetails.objects.get(id=pk)

            queryset.delete()

            return Response(
                {
                    "message":res_msg.delete("Clarity Detail"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        except ProtectedError:
            return Response(
                {
                    "message":res_msg.related_item("Please Delete "),
                    "status":status.HTTP_400_BAD_REQUEST
                },status=status.HTTP_200_OK
            )
        except Exception as err:
            return Response(
                {
                    "message":res_msg.not_exists("Clarity Details"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
    

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ClarityStatusView(APIView):

    def get(self,request,pk):
        try:
            queryset=ClarityDetails.objects.get(id=pk)

            queryset.is_active=not(queryset.is_active)
            queryset.save()

            serializer=ClarityDetailsSerializer(queryset)

            try:
                caratrate_queryset=list(CaratRate.objects.filter(clarity=pk))

                for data in caratrate_queryset:
                    if queryset.is_active==True:
                        if data.shape.is_active==True:
                            if data.cut.is_active==True:
                                if data.color.is_active==True:
                                    if data.cent_group.is_active==True:
                                        data.is_active=queryset.is_active
                                        data.save()
                                    else:
                                        pass
                                else:
                                    pass
                            else:
                                pass
                        else:
                            pass
                    else:
                        data.is_active=queryset.is_active
                        data.save()

                return Response(
                    {
                        "data":serializer.data,
                        "message":res_msg.change("Clarity Detail Status"),
                        "status":status.HTTP_200_OK
                    },status=status.HTTP_200_OK
                )
            except Exception as err:
                return Response(
                {
                    "message":res_msg.not_update("Clarity Details"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        except Exception as err:
            return Response(
                {
                    "message":res_msg.not_exists("Clarity Details"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ClarityListView(APIView):
    def get(self,request):

        queryset=list(ClarityDetails.objects.filter(is_active=True).values('id','clarity_name').order_by('id'))

        return Response(
            {
                "data": {
                    "list": queryset
                },
                "message":res_msg.retrieve("Clarity Details"),
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
            items_per_page = int(request.data.get('items_per_page', ClarityDetails.objects.all().count()))
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
            queryset=list(ClarityDetails.objects.filter(clarity_name__icontains=search,**filter_condition).order_by('id'))
        elif search != '':
            queryset=list(ClarityDetails.objects.filter(clarity_name__icontains=search).order_by('id'))
        else:
            queryset=list(ClarityDetails.objects.all().order_by('id'))

        paginated_data = Paginator(queryset, items_per_page)
        serializer = ClarityDetailsSerializer(paginated_data.get_page(page), many=True)

        return Response(
            {
                "data": {
                    "list": serializer.data,
                    "total_pages": paginated_data.num_pages,
                    "current_page": page,
                    "total_items": len(queryset),
                    "current_items": len(serializer.data)
                },
                "message":res_msg.retrieve('Clarity Details'),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class CentGroupViewset(viewsets.ViewSet):
    def create(self,request):

        request_data=request.data

        request_data['created_at']=timezone.now()
        request_data['created_by']=request.user.id

        serializer=CentGroupSerializer(data=request_data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "data":serializer.data,
                    "message":res_msg.create("Cent Group"),
                    "status":status.HTTP_201_CREATED
                },status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    "data":serializer.errors,
                    "message":res_msg.not_create("Cent Group"),
                    "status":status.HTTP_400_BAD_REQUEST
                },status=status.HTTP_200_OK
            )
    def update(self,request,pk):
        
        try:
            queryset=CentGroup.objects.get(id=pk)
            request_data=request.data
            request_data['modified_at']=timezone.now()
            request_data['modified_by']=request.user.id

            serializer=CentGroupSerializer(queryset,data=request_data,partial=True)

            if serializer.is_valid():
                serializer.save()

                return Response(
                    {
                        "data":serializer.data,
                        "message":res_msg.update("Cent Group"),
                        "status":status.HTTP_200_OK
                    },status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        "data":serializer.errors,
                        "message":res_msg.not_update("Cent Group"),
                        "status":status.HTTP_404_NOT_FOUND
                    },status=status.HTTP_200_OK
                )


        except Exception as err:
            return Response(
                {
                    "message":res_msg.not_exists("Cent Group"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
    def retrieve(self,request,pk):

        try:
            queryset=CentGroup.objects.get(id=pk)

            serializer=CentGroupSerializer(queryset)

            return Response(
                {
                    "data":serializer.data,
                    "message":res_msg.retrieve("Cent Group"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        except Exception as err:
            return Response(
                {
                    "message":res_msg.not_exists,
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
    
    def destroy(self,request,pk):
        try:
            queryset=CentGroup.objects.get(id=pk)

            queryset.delete()

            return Response(
                {
                    "message":res_msg.delete("Cent Group"),
                    "status":status.HTTP_200_OK         
                },status=status.HTTP_200_OK
            )
        except ProtectedError:
            return Response(
                {
                    "message":res_msg.related_item("Please Delete "),
                    "status":status.HTTP_400_BAD_REQUEST
                },status=status.HTTP_200_OK
            )
        except Exception as err:

            return Response(
                {
                    "message":res_msg.not_exists("Cent Group"),
                    "status":status.HTTP_404_NOT_FOUND
                }
            )
        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class CentGroupStatusView(APIView):
    def get(self,request,pk):

        try:
            queryset=CentGroup.objects.get(id=pk)

            queryset.is_active=not(queryset.is_active)
            queryset.save()

            serializer=CentGroupSerializer(queryset)

            try:
                caratrate_queryset=list(CaratRate.objects.filter(cent_group=pk))

                for data in caratrate_queryset:
                    if queryset.is_active==True:
                        if data.shape.is_active==True:
                            if data.cut.is_active==True:
                                if data.color.is_active==True:
                                    if data.clarity.is_active==True:
                                        if data.stone.is_active==True:
                                            data.is_active=queryset.is_active
                                            data.save()
                                        else:
                                            pass
                                    else:
                                        pass
                                else:
                                    pass
                            else:
                                pass
                        else:
                            pass
                    else:
                        data.is_active=queryset.is_active
                        data.save()

                return Response(
                    {
                        "data":serializer.data,
                        "message":res_msg.change("Cent Group Status"),
                        "status":status.HTTP_200_OK
                    },status=status.HTTP_200_OK
                )
            except Exception as err:
                return Response(
                {
                    "message":res_msg.not_update("Cent Group"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        except Exception as err:
            return Response(
                {
                    "message":res_msg.not_exists("Cent Group"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])  
class CentGroupListView(APIView):
    def get(self,request):

        queryset=list(CentGroup.objects.filter(is_active=True).values('id','centgroup_name').order_by('id'))

        return Response(
            {
                "data":{
                    "list":queryset
                },
                "message":res_msg.retrieve("Cent Group"),
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
            items_per_page = int(request.data.get('items_per_page', CentGroup.objects.all().count()))
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
            queryset=list(CentGroup.objects.filter(centgroup_name__icontains=search,**filter_condition).order_by('id'))
        elif search != '':
            queryset=list(CentGroup.objects.filter(centgroup_name__icontains=search).order_by('id'))
        else:
           queryset=list(CentGroup.objects.all().order_by('id'))

        paginated_data = Paginator(queryset, items_per_page)
        serializer = CentGroupSerializer(paginated_data.get_page(page), many=True)
        
        return Response(
            {
                "data" : {   
                    "list": serializer.data,
                    "total_pages": paginated_data.num_pages,
                    "current_page": page,
                    "total_items": len(queryset),
                    "current_items": len(serializer.data)
                },
                "message":res_msg.retrieve("Cent Group"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])  
class TagTypeViewset(viewsets.ViewSet):
    
    def create(self,request):
         
        requset_data=request.data
        requset_data['created_at']=timezone.now()
        requset_data['created_by']=request.user.id

        serializer=TagTypeSerializer(data=requset_data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "data":serializer.data,
                    "message":res_msg.create("Tag Type"),
                    "status":status.HTTP_201_CREATED
                },status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    "data":serializer.errors,
                    "message":res_msg.not_create("Tag Type"),
                    "status":status.HTTP_400_BAD_REQUEST
                },status=status.HTTP_200_OK
            )
    
    def retrieve(self,request,pk):

        try:
            queryset=TagTypes.objects.get(id=pk)

            serializer=TagTypeSerializer(queryset)

            return Response(
                {
                    "data":serializer.data,
                    "message":res_msg.retrieve("Tag Type"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )

        except Exception as err:
            return Response(
                {
                    "message":res_msg.not_exists("Tag Type"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        
    def update(self,request,pk):

        try:
            queryset=TagTypes.objects.get(id=pk)

            request_data=request.data
            request_data['modified_at']=timezone.now()
            request_data['modified_by']=request.user.id

            serializer=TagTypeSerializer(queryset,data=request_data,partial=True)

            if serializer.is_valid():
                serializer.save()

                return Response(
                    {
                        "data":serializer.data,
                        "message":res_msg.update("Tag Type"),
                        "status":status.HTTP_200_OK
                    },status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        "data":serializer.errors,
                        "message":res_msg.not_update("Tag Type"),
                        "status":status.HTTP_400_BAD_REQUEST
                    },status=status.HTTP_200_OK
                )
        except Exception as err:
            return Response(
                {
                    'message':res_msg.not_exists("Tag Type"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
    
    def destroy(self,request,pk):

        try:
            queryset=TagTypes.objects.get(id=pk)

            queryset.delete()

            return Response(
                {
                    "message":res_msg.delete("Tag Type"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        except Exception as err:
            return Response(
                {
                    "message":res_msg.not_exists("Tag Type"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])  
class TagTypeStatusView(APIView):

    def get(self, request, pk, active=None):

        try:
            queryset=TagTypes.objects.get(id=pk)
        except Exception as err:
            return Response(
                {
                    "message":res_msg.not_exists("Tag Type"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )

        if not(queryset.is_active):
            try:
                metal_queryset = Metal.objects.get(id=queryset.metal.pk, is_active=True)
                pass
            except Metal.DoesNotExist:
                return Response({
                    "message": res_msg.activate(queryset.metal.metal_name + ' metal'),
                    "status": status.HTTP_204_NO_CONTENT
                }, status=status.HTTP_200_OK)

        queryset.is_active=not(queryset.is_active)
        queryset.save()

        serializer=TagTypeSerializer(queryset)

        if active:
            return
        
        return Response(
                {
                    "data":serializer.data,
                    "message":res_msg.change("Tag Type Status"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class TagTypeListView(APIView):
    
    def get(self,request):

        queryset=list(TagTypes.objects.filter(is_active=True).values('id','tag_name','metal_id__metal_name'))

        return Response(
            {
                "data": {
                    "list": queryset
                },
                "message":res_msg.retrieve("Tag Type"),
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
            items_per_page = int(request.data.get('items_per_page', TagTypes.objects.all().count()))
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
                queryset=TagTypes.objects.filter(Q(tag_name__icontains=search)  | Q(metal__metal_name__icontains=search) | Q(tag_code__icontains=search),**filter_condition).order_by('id')
        elif search != '':
                queryset=TagTypes.objects.filter(Q(tag_name__icontains=search)  | Q(metal__metal_name__icontains=search) | Q(tag_code__icontains=search)).order_by('id')
        else:
            queryset=TagTypes.objects.all().order_by('id')
        
        paginated_data = Paginator(queryset, items_per_page)
        serializer = TagTypeSerializer(paginated_data.get_page(page), many=True)
        res_data = []

        for i in range(0, len(serializer.data)):
            dict_data = serializer.data[i]
            dict_data['metal_name'] = queryset[i].metal.metal_name

            res_data.append(dict_data)

        return Response(
            {
                "data": {
                    "list": res_data,
                    "total_pages": paginated_data.num_pages,
                    "current_page": page,
                    "total_items": len(queryset),
                    "current_items": len(serializer.data)
                },
                "message":res_msg.retrieve("Tag Type"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
    

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class StoneDetailsViewset(viewsets.ViewSet):

    def create(self,request):
        request_data=request.data
        request_data['created_at']=timezone.now()
        request_data['created_by']=request.user.id

        serializer=StoneSerializer(data=request_data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "data":serializer.data,
                    "message":res_msg.create("Stone Details"),
                    "status":status.HTTP_201_CREATED
                },status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    "data":serializer.errors,
                    "message":res_msg.in_valid_fields(),
                    "status":status.HTTP_400_BAD_REQUEST
                },status=status.HTTP_200_OK
            )
        
    def retrieve(self,request,pk):
        try:
            queryset=StoneDetails.objects.get(id=pk)

            serializer=StoneSerializer(queryset)

            return Response(
                {
                    "data":serializer.data,
                    "message":res_msg.retrieve("Stone Details"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        except Exception as err:
            return Response(
                {
                    "message":res_msg.not_exists("Stone Details"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        
    def update(self,request,pk):

        try:
            queryset=StoneDetails.objects.get(id=pk)

            request_data=request.data
            request_data['modified_at']=timezone.now()
            request_data['modified_by']=request.user.id

            serializer=StoneSerializer(queryset,data=request_data,partial=True)

            if serializer.is_valid():
                
                serializer.save()

                return Response(
                    {
                        "data":serializer.data,
                        "message":res_msg.update("Stone Details"),
                        "status":status.HTTP_200_OK
                    },status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        "data":serializer.errors,
                        "message":res_msg.in_valid_fields(),
                        "status":status.HTTP_400_BAD_REQUEST
                    },status=status.HTTP_200_OK
                )
            
        except Exception as err:
            return Response(
                {
                    "message":res_msg.not_exists("Stone Details"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        
    def destroy(self,request,pk):
        try:
            queryset=StoneDetails.objects.get(id=pk)

            queryset.delete()
            return Response(
                {
                    "message":res_msg.delete("Stone Details"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )

        except StoneDetails.DoesNotExist:
            return Response(
                {
                    "message":res_msg.not_exists("Stone Details"),
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
        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class StoneStatusView(APIView):

    def get(self,request,pk):

        try:
            queryset=StoneDetails.objects.get(id=pk)

            queryset.is_active=not(queryset.is_active)
            queryset.save()

            serializer=StoneSerializer(queryset)

            try:
                caratrate_queryset=list(CaratRate.objects.filter(stone=pk))

                for data in caratrate_queryset:
                    if queryset.is_active==True:
                        if data.shape.is_active==True:
                            if data.cut.is_active==True:
                                if data.color.is_active==True:
                                    if data.clarity.is_active==True:
                                        if data.cent_group.is_active==True:
                                            data.is_active=queryset.is_active
                                            data.save()
                                        else:
                                            pass
                                    else:
                                        pass
                                else:
                                    pass
                            else:
                                pass
                        else:
                            pass
                    else:
                        data.is_active=queryset.is_active
                        data.save()

                return Response(
                    {
                        "data":serializer.data,
                        "message":res_msg.change("Stone Detail Status"),
                        "status":status.HTTP_200_OK
                    },status=status.HTTP_200_OK
                )
            except Exception as err:
                return Response(
                {
                    "message":res_msg.not_update("Stone Detail"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        except Exception as err:
            return Response(
                {
                    "message":res_msg.not_exists("Stone Detail"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class StoneListView(APIView):
    
    def get(self,request):

        queryset=list(StoneDetails.objects.filter(is_active=True).values('id','stone_name','stone_code').order_by('id'))

        return Response(
            {
                "data": {
                    "list": queryset
                },
                "message":res_msg.retrieve("Stone Details"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
    
    def post(self,request):

        search = request.data.get('search') if request.data.get('search') else ''
        active_status = request.data.get('active_status') if request.data.get('active_status') !=None else None
        from_date = request.data.get('from_date') if request.data.get('from_date') else None
        to_date = request.data.get('to_date') if request.data.get('to_date') else None
        page = request.data.get('page') if request.data.get('page') else 1
        try:
            items_per_page = int(request.data.get('items_per_page', StoneDetails.objects.all().count()))
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
            queryset=list(StoneDetails.objects.filter(Q(stone_name__icontains=search) | Q(stone_code__icontains=search),**filter_condition).order_by('id'))
        elif search != '':
            queryset=list(StoneDetails.objects.filter(Q(stone_name__icontains=search) | Q(stone_code__icontains=search)).order_by('id'))
        else:
            queryset=list(StoneDetails.objects.all().order_by('id'))
        
        paginated_data = Paginator(queryset, items_per_page)
        serializer = StoneSerializer(paginated_data.get_page(page), many=True)
        
        return Response(
            {
                "data": {
                    "list": serializer.data,
                    "total_pages": paginated_data.num_pages,
                    "current_page": page,
                    "total_items": len(queryset),
                    "current_items": len(serializer.data)
                },
                "message":res_msg.retrieve("Stone Details"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class CaratRateViewset(viewsets.ViewSet):

    def create(self,request):

        request_data=request.data
        designer_ids = request.data.get('designer', [])
        request_data = request.data.copy()
        request_data['created_at']=timezone.now()
        request_data['created_by']=request.user.id

        designer = []
        for designer_id in designer_ids:
            designer_data = request_data.copy()
            designer_data['designer'] = designer_id
            designer.append(designer_data)
     
        serializer=CaratRateSerializer(data=designer, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "data":serializer.data,
                    "message":res_msg.create("Carat Rate"),
                    "status":status.HTTP_201_CREATED
                },status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    "data":serializer.errors,
                    "message":res_msg.not_create("Carat Rate"),
                    "status":status.HTTP_400_BAD_REQUEST
                },status=status.HTTP_200_OK
            )
        
    def retrieve(self,reuqest,pk):

        try:

            queryset=CaratRate.objects.get(id=pk)

            serializer=CaratRateSerializer(queryset)

            response_data=serializer.data
            response_data['designer_name']=queryset.designer.account_head_name
            response_data['stone_name']=queryset.stone.stone_name
            response_data['shape_name']=queryset.shape.shape_name
            response_data['cut_name']=queryset.cut.cut_name
            response_data['color_name']=queryset.color.color_name
            response_data['clarity_name']=queryset.clarity.clarity_name
            response_data['cent_group_name']=queryset.cent_group.centgroup_name

            return Response(
                {
                    "data":response_data,
                    "message":res_msg.retrieve("Carat Rate"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        except Exception as err:
            return Response(
                {
                    "message":res_msg.not_exists("Carat Rate"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
    
    def update(self,request,pk):

        try:
            queryset=CaratRate.objects.get(id=pk)

            request_data=request.data
            request_data['modified_at']=timezone.now()
            request_data['modified_by']=request.user.id

            serializer=CaratRateSerializer(queryset,data=request_data,partial=True)

            if serializer.is_valid():
                serializer.save()
                response_data=serializer.data
                response_data['designer_name']=queryset.designer.account_head_name
                response_data['stone_name']=queryset.stone.stone_name
                response_data['shape_name']=queryset.shape.shape_name
                response_data['cut_name']=queryset.cut.cut_name
                response_data['color_name']=queryset.color.color_name
                response_data['clarity_name']=queryset.clarity.clarity_name
                response_data['cent_group_name']=queryset.cent_group.centgroup_name
                return Response(
                    {
                        "data":response_data,
                        "message":res_msg.update("Carat Rate"),
                        "status":status.HTTP_200_OK
                    },status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        "data":serializer.errors,
                        "message":res_msg.not_update("Carat Rate"),
                        "status":status.HTTP_404_NOT_FOUND
                    },status=status.HTTP_200_OK
                )
        except Exception as err:
            return Response(
                {
                    "message":res_msg.not_exists("Carat Rate"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        
    def destroy(self,request,pk):

        try:
            queryset=CaratRate.objects.get(id=pk)

            queryset.delete()

            return Response(
                {
                    "message":res_msg.delete("Carat Rate"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        except CaratRate.DoesNotExist:
            return Response(
                {
                    "message":res_msg.not_exists("Carat Rate"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        except ProtectedError:
            return Response(
                {
                    "message":res_msg.related_item("Please Delete the "),
                    "status":status.HTTP_400_BAD_REQUEST
                },status=status.HTTP_200_OK
            )
        

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class CaratRateStatusView(APIView):
    def get(self,request,pk):

        try:
            queryset=CaratRate.objects.get(id=pk)

            if queryset.is_active==False:
                if queryset.shape.is_active==True:
                    if queryset.cut.is_active==True:
                        if queryset.color.is_active==True: 
                            if queryset.clarity.is_active==True:
                                if queryset.cent_group.is_active==True:
                                    if queryset.stone.is_active==True:
                                        queryset.is_active=not(queryset.is_active)
                                        queryset.save()
                                        serializer=CaratRateSerializer(queryset)
                                        return Response(
                                            {
                                                "data":serializer.data,
                                                "message":res_msg.change("Carat Rate Status"),
                                                "status":status.HTTP_200_OK
                                            },status=status.HTTP_200_OK
                                        )
                                    else:
                                        return Response({"message":"Please Activate the Stone",
                                                         "status":status.HTTP_400_BAD_REQUEST
                                                         },status=status.HTTP_200_OK)
                                else:
                                    return Response({"message":"Please Activate the Cent Group",
                                                     "status":status.HTTP_400_BAD_REQUEST
                                                     },status=status.HTTP_200_OK)
                            else:
                                return Response({"message":"Please Activate the Clarity",
                                                     "status":status.HTTP_400_BAD_REQUEST
                                                     },status=status.HTTP_200_OK)
                        else:
                            return Response({"message":"Please Activate the Color",
                                                     "status":status.HTTP_400_BAD_REQUEST
                                                     },status=status.HTTP_200_OK)
                    else:
                        return Response({"message":"Please Activate the Cut",
                                                     "status":status.HTTP_400_BAD_REQUEST
                                                     },status=status.HTTP_200_OK)
                else:
                    return Response({"message":"Please Activate the Shape",
                                                     "status":status.HTTP_200_OK
                                                     },status=status.HTTP_200_OK)
            else:
                queryset.is_active=not(queryset.is_active)
                queryset.save()
                serializer=CaratRateSerializer(queryset)
                return Response(
                        {
                            "data":serializer.data,
                            "message":res_msg.change("Carat Rate Status"),
                            "status":status.HTTP_200_OK
                        },status=status.HTTP_200_OK
                    )

        except CaratRate.DoesNotExist:
            return Response(
                {
                    "message":res_msg.not_exists("Carat Rate"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        except Exception as err:
            return Response(
                {
                    "message":res_msg.not_update("Carat Rate"),
                    "status":status.HTTP_400_BAD_REQUEST
                },status=status.HTTP_200_OK
            )
        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class CaratRateListView(APIView):

    def post(self,request):

        search = request.data.get('search') if request.data.get('search') else ''
        active_status = request.data.get('active_status') if request.data.get('active_status') != None else None
        from_date = request.data.get('from_date') if request.data.get('from_date') else None
        to_date = request.data.get('to_date') if request.data.get('to_date') else None
        page = request.data.get('page') if request.data.get('page') else 1
        try:
            items_per_page = int(request.data.get('items_per_page', CaratRate.objects.all().count()))
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
            queryset=list(CaratRate.objects.filter(Q(designer__account_head_name__icontains=search)|Q(shape__shape_name__icontains=search)|Q(stone__stone_name__icontains=search)|Q(cut__cut_name__icontains=search)|Q(color__color_name__icontains=search)|Q(clarity__clarity_name__icontains=search)|Q(cent_group__centgroup_name__icontains=search),**filter_condition).order_by('id'))
        elif search != '':
            queryset=list(CaratRate.objects.filter(Q(designer__account_head_name__icontains=search)|Q(shape__shape_name__icontains=search)|Q(stone__stone_name__icontains=search)|Q(cut__cut_name__icontains=search)|Q(color__color_name__icontains=search)|Q(clarity__clarity_name__icontains=search)|Q(cent_group__centgroup_name__icontains=search)).order_by('id'))
        else:
            queryset=list(CaratRate.objects.all().order_by('id'))

        paginated_data = Paginator(queryset, items_per_page)
        serializer = CaratRateSerializer(paginated_data.get_page(page), many=True)
        
        response_data=[]

        for data in queryset:

            res_data={}
            res_data['id']=data.pk
            res_data['designer']=data.designer.account_head_name
            res_data['stone']=data.stone.stone_name
            res_data['shape']=data.shape.shape_name
            res_data['cut']=data.cut.cut_name
            res_data['color']=data.color.color_name
            res_data['clarity']=data.clarity.clarity_name
            res_data['cent_group']=data.cent_group.centgroup_name
            res_data['purchase_rate']=data.purchase_rate
            res_data['selling_rate']=data.selling_rate
            res_data['is_active']=data.is_active

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
                "message":res_msg.retrieve("Carat Rate"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
    

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class RangeStockViewset(viewsets.ViewSet):

    def create(self,request):

        request_data=request.data
        request_data['created_at']=timezone.now()
        request_data['created_by']=request.user.id  

        serializer=RangeStockSerializer(data=request_data)

        if serializer.is_valid():

            serializer.save()

            return Response(
                {
                    "data":serializer.data,
                    "message":res_msg.create("Range Stock"),
                    "status":status.HTTP_201_CREATED
                },status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    "data":serializer.errors,
                    "message":res_msg.not_create("Range Stock"),
                    "status":status.HTTP_400_BAD_REQUEST 
                },status=status.HTTP_200_OK
            )
        
    def retrieve(self,request,pk):

        try:
            queryset=RangeStock.objects.get(id=pk)

            serializer=RangeStockSerializer(queryset)

            return Response(
                {
                    "data":serializer.data,
                    "message":res_msg.retrieve("Range Stock Details"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        except Exception as err:
            return Response(
                {
                    "message":res_msg.not_exists("Range Stock Details"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
    
    def update(self,request,pk):

        try:

            queryset=RangeStock.objects.get(id=pk)

            request_data=request.data
            request_data['modified_at']=timezone.now()
            request_data['modified_by']=request.user.id

            serializer=RangeStockSerializer(queryset,data=request_data,partial=True)

            if serializer.is_valid():
                serializer.save()

                return Response(
                    {
                        "data":serializer.data,
                        "message":res_msg.update("Range Stock"),
                        "status":status.HTTP_200_OK
                    },status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        "data":serializer.errors,
                        "message":res_msg.not_update("Range Stock"),
                        "status":status.HTTP_400_BAD_REQUEST
                    },status=status.HTTP_200_OK
                )
        except Exception as err:
            return Response(
                {
                    "message":res_msg.not_exists("Range Stock"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        
    def destroy(self,request,pk):

        try:
            queryset=RangeStock.objects.get(id=pk)

            queryset.delete()

            return Response(
                {
                    "message":res_msg.delete("Range Stock"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        except RangeStock.DoesNotExist:
            return Response(
                {
                    "message":res_msg.not_exists("Range Stock"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        except ProtectedError:
            return Response(
                {
                    "message":res_msg.related_item("Please Delete the"),
                    "status":status.HTTP_400_BAD_REQUEST
                },status=status.HTTP_200_OK
            )


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class RangeStockStatusView(APIView):

    def get(self,request,pk):
        try:
            queryset=RangeStock.objects.get(id=pk)

            queryset.is_active=not(queryset.is_active)
            queryset.save()

            serializer=RangeStockSerializer(queryset)

            return Response(
                {
                    "data":serializer.data,
                    "message":res_msg.change("Range Stock Status"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        except Exception as err:
            return Response(
                {
                    "message":res_msg.not_exists("Range Stock"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class RangeStockListView(APIView):

    def get(self,request):

        queryset=list(RangeStock.objects.filter(is_active=True).values('id','range_value').order_by('-id'))

        return Response(
            {
                "data":{
                    "list":queryset
                    },
                "message":res_msg.retrieve("Range Stock"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
    
    def post(self,request):

        search = request.data.get('search') if request.data.get('search') else ''
        active_status = request.data.get('active_status') if request.data.get('active_status') else None
        from_date = request.data.get('from_date') if request.data.get('from_date') else None
        to_date = request.data.get('to_date') if request.data.get('to_date') else None
        page = request.data.get('page') if request.data.get('page') else 1

        try:
            items_per_page = int(request.data.get('items_per_page', RangeStock.objects.all().count()))
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
            queryset=list(RangeStock.objects.filter(**filter_condition).order_by('id'))
        elif search != '':
            queryset=list(RangeStock.objects.filter(**filter_condition).order_by('id'))
        else:
            queryset=list(RangeStock.objects.all().order_by('id'))

        paginated_data = Paginator(queryset, items_per_page)
        serializer = RangeStockSerializer(paginated_data.get_page(page), many=True)

        response_data = []
        for i in range(0,len(serializer.data)):
            dict_data = serializer.data[i]
            response_data.append(dict_data)
        return Response(
            {
                "data":{
                    "list": response_data,
                    "total_pages": paginated_data.num_pages,
                    "current_page": page,
                    "total_items": len(queryset),
                    "current_items": len(serializer.data)
                },
                "message":res_msg.retrieve("Range Stock"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
    
   

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class TodayMetalrate(APIView):
    def get(self, request):
        data = {
                'gold': 0,
                'silver': 0,
                "gold_purity": ".22kt",
                "silver_purity": "1gram"
            }
        
        try:
            metal_rate_queryset=MetalRate.objects.all().order_by('-id')

            if len(metal_rate_queryset) > 0:
                first_data = metal_rate_queryset.first()

                try:
                    purity_queryset = list(Purity.objects.filter(is_visible=True))
                except:
                    return Response({
                        "message": "Visible is not selected",
                        "status": status.HTTP_200_OK
                    }, status=status.HTTP_200_OK)
                
                for i in purity_queryset:
                    if i.metal.pk == 1:
                        data["gold"] = first_data.rate[i.metal.metal_name.replace(' ', '_').replace('-', '_') + "_" + i.purity_name.replace(' ', '_').replace('-', '_')]
                        data["gold_purity"] = i.purity_name
                    elif i.metal.pk == 2:
                        data["silver"] = first_data.rate[i.metal.metal_name.replace(' ', '_').replace('-', '_') + "_" + i.purity_name.replace(' ', '_').replace('-', '_')]
                        data["silver_purity"] = i.purity_name
                    else:
                        pass
        except Exception as err:
            pass

        return Response({
            "data":data,
            "message": res_msg.retrieve('Metal Rate'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
       
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class DisplayMetalrate(APIView):
    def get(self, request):

        metal_rate_queryset=MetalRate.objects.last()
       
        datalist = {}
        datalist['Goldrate'] = ''
        datalist['silverrate']= ''
        datalist['Goldgram'] = ''
        datalist['silvergram']= ''
        if metal_rate_queryset.gold_24ktvisible == True:
            datalist['Goldrate'] = metal_rate_queryset.gold_24kt_rate
            datalist['Goldgram'] ="(Gram 24CT)"

        elif metal_rate_queryset.gold_22kt_visible == True:
            datalist['Goldrate'] = metal_rate_queryset.gold_22kt_rate 
            datalist['Goldgram'] ="(Gram 22CT)"
        
        if metal_rate_queryset.silver_1gm_visible == True:
            datalist['silverrate']=metal_rate_queryset.silver_1gm_rate
            datalist['silvergram'] = '(Gram) '   
       
        return Response({
            "data":datalist,
            "message": res_msg.retrieve('Metal Rate'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)


       
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class MetalbasedPurityView(APIView):
 
    def get(self, request, pk):

 
        try:
            queryset = Purity.objects.filter(metal=pk)
           
        except:
            return Response({
                "message": res_msg.not_exists('Purity'),
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_200_OK)
       
        serializer = PuritySerializer(queryset,many=True)
        return Response({
                "data": serializer.data,
                "message": res_msg.retrieve('Purity'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
    

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class RepairTypeView(viewsets.ViewSet):

    def create(self, request):
        data = request.data
        data['repair_type_name'] = data.get('repair_type_name').lower()
        data['created_at'] = timezone.now()
        data['created_by'] = request.user.id

        serializer = RepairTypeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": res_msg.create('Repair Type'),
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
            queryset = RepairType.objects.get(id=pk)
        except Exception as err:
            return Response({
                "message": res_msg.not_exists('Repair Type'),
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_200_OK)
        
        data = request.data
        data['repair_type_name'] = data.get('repair_type_name').lower()
        data['modified_at'] = timezone.now()
        data['modified_by'] = request.user.id

        serializer = RepairTypeSerializer(queryset, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": res_msg.update('Repair Type'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        return Response({
                "data": serializer.errors,
                "message": res_msg.in_valid_fields(),
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_200_OK)
    

    def retrieve(self, request, pk):
        try:
            queryset = RepairType.objects.get(id=pk)
            serializer = RepairTypeSerializer(queryset)

            return Response({
                "data": serializer.data,
                "message": res_msg.retrieve('Repair Type'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        except RepairType.DoesNotExist:
            return Response({
                "message": res_msg.not_exists('Repair Type'),
                "status": status.HTTP_204_NO_CONTENT
            }, status=status.HTTP_200_OK)
        

    def destroy(self, request, pk):
        try:
            queryset = RepairType.objects.get(id=pk)
            queryset.delete()
            return Response({
                "message": res_msg.delete('Repair Type'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        except RepairType.DoesNotExist:
            return Response({
                "message": res_msg.not_exists('Repair Type'),
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
class RepairTypeStatusView(APIView):

    def get(self,request,pk):
        try:
            queryset = RepairType.objects.get(id=pk)

            queryset.is_active=not(queryset.is_active)
            queryset.save()

            return Response(
                {
                    "message":res_msg.change("Repair Type Status"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        except RepairType.DoesNotExist:
            return Response(
                {
                    "message":res_msg.not_exists("Repair Type"),
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
class RepairTypeListView(APIView):

    def get(self, request):

        queryset = RepairType.objects.all().order_by('id')
        serializer = RepairTypeSerializer(queryset,many=True)
           
        return Response({
            "data": {
                "list": serializer.data,
            },
            "message": res_msg.retrieve('Repair Type'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
    
    def post(self, request):
        search = request.data.get('search') if request.data.get('search') else ''
        from_date = request.data.get('from_date') if request.data.get('from_date') else None
        to_date = request.data.get('to_date') if request.data.get('to_date') else None
        active_status = request.data.get('active_status') if request.data.get('active_status') != None else None
        page = request.data.get('page') if request.data.get('page') else 1
        try:
            items_per_page = int(request.data.get('items_per_page', RepairType.objects.all().count()))
            if items_per_page == 0:
                items_per_page = 10 
        except Exception as err:
            items_per_page = 10 

        filter_condition={}

        if active_status != None:
            filter_condition['is_active']=active_status

        if from_date != None and to_date!= None:
           fdate =from_date+'T00:00:00.899010+05:30'
           tdate =to_date+'T23:59:59.899010+05:30'
           date_range=(fdate,tdate)
           filter_condition['created_at__range']=date_range

        if len(filter_condition) != 0:
                queryset = list(RepairType.objects.filter(Q(repair_type_name__icontains=search),**filter_condition).order_by('id'))
        elif search != '':
                queryset = list(RepairType.objects.filter(Q(repair_type_name__icontains=search)).order_by('id'))
        else:
            queryset = list(RepairType.objects.filter(Q(repair_type_name__icontains=search)).order_by('id'))
        
        paginated_data = Paginator(queryset, items_per_page)
        serializer = RepairTypeSerializer(paginated_data.get_page(page), many=True)

        return Response({
            "data": {
                "list": serializer.data,
                "total_pages": paginated_data.num_pages,
                "current_page": page,
                "total_items": len(queryset),
                "current_items": len(serializer.data)
            },
            "message": res_msg.retrieve('Repair Type'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
    

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class RangeStockReport(APIView):
    def get(self,request,pk):
        try:

            range_queryset = RangeStock.objects.get(id = pk)

            weight_range =(range_queryset.from_weight,range_queryset.to_weight)


            tag_list_queryset = list(TaggedItems.objects.filter(item_details__item_details = range_queryset.item_details.pk,gross_weight__range=weight_range))

            response_data = []

            for tags in tag_list_queryset :
                res_data={
                    'tag_number':tags.tag_number,
                    'item_details':tags.item_details.item_details.item_name,
                    'sub_item_details':tags.sub_item_details.sub_item_name,
                    'size_value':tags.size_value,
                    'tag_number':tags.tag_number,
                    'tag_pieces':tags.tag_pieces,
                    'gross_weight':tags.gross_weight,
                    'net_weight':tags.net_weight,
                    'halmark_huid':tags.halmark_huid,
                }
                response_data.append(res_data)

            return Response(
                {
                    "data":{
                        "list":response_data
                    },
                    "message":res_msg.retrieve("Range Stock Report"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )

        except :

            return Response(
                {
                    "message":res_msg.not_exists("Range Stock"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class VoucherTypeViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk):

        try:
            queryset = VoucherType.objects.get(id=pk)
       
            serializer = VoucherTypeSerializer(queryset)

            return Response({
                "data": serializer.data,
                "message": res_msg.retrieve('Voucher Type'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({
                "message": res_msg.not_exists('Voucher Type'),
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_200_OK)

    def create(self, request):

        data = request.data
        data['voucher_name'] = data.get('voucher_name').lower()
        data['created_at'] = timezone.now()
        data['created_by'] = request.user.id
        serializer = VoucherTypeSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": res_msg.create('Voucher Type'),
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
            queryset = VoucherType.objects.get(id=pk)
        except Exception as err:
            return Response({
                "message": res_msg.not_exists('Voucher Type'),
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_200_OK)
        
        data = request.data
        data['voucher_name'] = data.get('voucher_name').lower()
        data['modified_at'] = timezone.now()
        data['modified_by'] = request.user.id
        serializer = VoucherTypeSerializer(queryset, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": res_msg.update('Voucher Type'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        return Response({
                "data": serializer.errors,
                "message": res_msg.in_valid_fields(),
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_200_OK)
    
    def destroy(self, request, pk):
        try:
            queryset = VoucherType.objects.get(id=pk)
            queryset.delete()
            return Response({
                "message": res_msg.delete('Voucher Type'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        except Metal.DoesNotExist:
            return Response({
                "message": res_msg.not_exists('Voucher Type'),
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
class VoucherTypeListView(APIView):

    def get(self,request):

        queryset=list(VoucherType.objects.filter(is_active=True).values('id','voucher_name'))

        return Response(
            {
                "data":{
                    "list":queryset
                },
                "message":res_msg.retrieve("Voucher Type"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
    
    def post(self,request):

        search = request.data.get('search') if request.data.get('search') else None
        active_status = request.data.get('active_status') if request.data.get('active_status') else None
        from_date = request.data.get('from_date') if request.data.get('from_date') else None
        to_date = request.data.get('to_date') if request.data.get('to_date') else None
        page = request.data.get('page') if request.data.get('page') else 1

        try:
            items_per_page = int(request.data.get('items_per_page'))
            if items_per_page == 0:
                items_per_page = 10 
        except Exception as err:
            items_per_page = 10

        filter_condition={}

        if search!= None:
            filter_condition['voucher_name__icontains'] = search

        if active_status!= None:
            filter_condition['is_active'] = active_status

        if from_date != None and to_date != None:
            date_range=(from_date,to_date)
            filter_condition['created_at__range'] = date_range


        if len(filter_condition) != 0:
            queryset = VoucherType.objects.filter(**filter_condition)

        else:

            queryset = VoucherType.objects.all()

        paginated_data = Paginator(queryset, items_per_page)
        serializer = VoucherTypeSerializer(paginated_data.get_page(page), many=True)

        return Response(
            {
                "data":{
                    "list":serializer.data
                },
                "message":res_msg.retrieve("Voucher Type"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
    

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class VoucherTypeStatusView(APIView):

    def get(self,request,pk):

        try:

            queryset = VoucherType.objects.get(id=pk)

            queryset.is_active=not(queryset.is_active)
            queryset.save()

            return Response(
                {
                    "message":res_msg.change("Voucher Type Status"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        
        except VoucherType.DoesNotExist:

            return Response(
                {
                    "message":res_msg.not_exists("Voucher Type"),
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
class GiftVoucherViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk):

        try:
            queryset = GiftVoucher.objects.get(id=pk)
       
            serializer = GiftVoucherSerializer(queryset)

            return Response({
                "data": serializer.data,
                "message": res_msg.retrieve('Gift Voucher'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({
                "message": res_msg.not_exists('Gift Voucher'),
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_200_OK)

    def create(self, request):

        data = request.data
        data['created_at'] = timezone.now()
        data['created_by'] = request.user.id
        serializer = GiftVoucherSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": res_msg.create('Gift Voucher'),
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
            queryset = GiftVoucher.objects.get(id=pk)
        except Exception as err:
            return Response({
                "message": res_msg.not_exists('Gift Voucher'),
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_200_OK)
        
        data = request.data
        data['modified_at'] = timezone.now()
        data['modified_by'] = request.user.id
        serializer = GiftVoucherSerializer(queryset, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": res_msg.update('Gift Voucher'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        return Response({
                "data": serializer.errors,
                "message": res_msg.in_valid_fields(),
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_200_OK)
    
    def destroy(self, request, pk):
        try:
            queryset = GiftVoucher.objects.get(id=pk)
            queryset.delete()
            return Response({
                "message": res_msg.delete('Gift Voucher'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        except GiftVoucher.DoesNotExist:
            return Response({
                "message": res_msg.not_exists('Gift Voucher'),
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
class GiftVoucherListView(APIView):

    def get(self,request):
        
        queryset=list(GiftVoucher.objects.all())

        for data in queryset:
            dict_data ={}
            dict_data['id'] = data.pk
            dict_data['voucher_type'] = data.voucher_type.pk
            dict_data['voucher_no'] = data.voucher_no
            dict_data['is_active'] = data.is_active
            dict_data['is_redeemed'] = data.is_redeemed
            dict_data['from_date'] = data.from_date
            dict_data['to_date'] = data.to_date

        return Response(
            {
                "data":{
                    "list":dict_data
                },
                "message":res_msg.retrieve("Gift Voucher"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
    
    def post(self,request):

        search = request.data.get('search') if request.data.get('search') else None
        active_status = request.data.get('active_status') if request.data.get('active_status') else None
        from_date = request.data.get('from_date') if request.data.get('from_date') else None
        to_date = request.data.get('to_date') if request.data.get('to_date') else None
        page = request.data.get('page') if request.data.get('page') else 1

        try:
            items_per_page = int(request.data.get('items_per_page'))
            if items_per_page == 0:
                items_per_page = 10 
        except Exception as err:
            items_per_page = 10

        filter_condition={}

        if search!= None:
            filter_condition['voucher_no__icontains'] = search

        if active_status!= None:
            filter_condition['is_active'] = active_status

        if from_date != None and to_date != None:
            date_range=(from_date,to_date)
            filter_condition['created_at__range'] = date_range


        if len(filter_condition) != 0:
            queryset = GiftVoucher.objects.filter(**filter_condition)

        else:

            queryset = GiftVoucher.objects.all()

        paginated_data = Paginator(queryset, items_per_page)
        serializer = GiftVoucherSerializer(paginated_data.get_page(page), many=True)

        return Response(
            {
                "data":{
                    "list":serializer.data
                },
                "message":res_msg.retrieve("Gift Voucher"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
    

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class GiftVoucherStatusView(APIView):

    def get(self,request,pk):

        try:

            queryset = GiftVoucher.objects.get(id=pk)

            queryset.is_active=not(queryset.is_active)
            queryset.save()

            return Response(
                {
                    "message":res_msg.change("Gift Voucher Status"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        
        except GiftVoucher.DoesNotExist:

            return Response(
                {
                    "message":res_msg.not_exists("Gift Voucher"),
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
class GiftVoucherDetailsView(APIView):

    def get(self,request,voucher_no):
        
        try:
            queryset=GiftVoucher.objects.filter(voucher_no=voucher_no,is_active=True,is_redeemed=False)
            if queryset.exists():
                for data in queryset:
                    dict_data ={}
                    dict_data['id'] = data.pk
                    dict_data['voucher_type'] = data.voucher_type.pk
                    dict_data['voucher_no'] = data.voucher_no
                    dict_data['is_active'] = data.is_active
                    dict_data['is_redeemed'] = data.is_redeemed
                    dict_data['from_date'] = data.from_date
                    dict_data['to_date'] = data.to_date

                return Response(
                {
                    "data" : {
                        "list" : dict_data
                    },
                    "message":res_msg.retrieve("Gift Voucher"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
                )   
            else:
                return Response(
                {
                    "message":"Voucher already redeemed",
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )

           
        except GiftVoucher.DoesNotExist:
            return Response(
                {
                    "message":res_msg.not_exists("Gift Voucher"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        except Exception as err:
            return Response(
                {
                    "data" : err,
                    "message":res_msg.something_else(),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )

        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class GSTListView(APIView):

    def get(self,request):
        
        queryset=list(GSTType.objects.all())

        serializer = GSTTypeSerializer(queryset,many=True)

        return Response(
            {
                "data":{
                    "list":serializer.data
                },
                "message":res_msg.retrieve("GST List"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
    

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class NewMetalRateListView(APIView):
    @transaction.atomic
    def post(self,request):
        request_data = request.data
 
        time= timezone.now()
        user = request.user.id
        metal_rates = request_data.get('metal_rates',[])
       
        for data in metal_rates:
           
            data['created_at'] = time
            data['created_by'] = user

            rate = data['rate'] if data['rate'] != "" else None

            if rate != None:
                data['purity'] = data['purity']
                data['rate'] = rate
            else:
                rate_queryset = MetalRate.objects.filter(purity=data['purity']).order_by('-id').first()
                data['purity'] = data['purity']
                data['rate'] = rate_queryset.rate
           
            serializer = MetalRateSerializer(data=data)
           
            if serializer.is_valid():
                serializer.save()
            else:
                transaction.set_rollback(True)
                return Response(
                    {
                        "data":serializer.errors,
                        "message":res_msg.not_create("Metal Rate"),
                        "status":status.HTTP_400_BAD_REQUEST
                    },status=status.HTTP_200_OK
                )
               
        return Response(
            {
                "message":res_msg.create("Metal Rate"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class NewMetalRateList(APIView):
   
    def post(self,request):
       
       
        distinct_created_at_dates = MetalRate.objects.values('created_at').distinct().order_by('-created_at')
       
        page = request.data.get('page', 1)
        items_per_page = request.data.get('items_per_page', 10)
       
        response_data =[]
       
        for dates in distinct_created_at_dates:
 
 
            queryset = MetalRate.objects.filter(created_at=dates['created_at'])
           
            res_data = {}
            res_data['date'] = dates['created_at']
                       
            rate_data = []
           
            for data in queryset:
               
                value = {}
               
                value['id'] = data.pk
                value['metal'] = data.purity.metal.pk
                value['metal_name'] = data.purity.metal.metal_name
                value['purity'] = data.purity.pk
                value['purity_name'] = data.purity.purity_name
                value['display_name'] = str(data.purity.metal.metal_name)+" "+str(data.purity.purity_name)
                value['rate'] = data.rate
               
                rate_data.append(value)
               
            res_data['rates'] = rate_data            
            response_data.append(res_data)
           
        paginator = Paginator(response_data, items_per_page)
        paginated_data = paginator.get_page(page)
       
        for i in range(len(paginated_data)):
           
            paginated_data[i]['s_no'] = i+1
 
           
        serialized_data = {
            "data": {
                "list": list(paginated_data),
                "total_items": paginator.count,
                "total_pages": paginator.num_pages,
                "current_page": paginated_data.number,
                "items_per_page": items_per_page
            },
            "message": res_msg.retrieve("Metal Rate List"),
            "status": status.HTTP_200_OK
        }
       
        return Response(serialized_data, status=status.HTTP_200_OK)
   

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class NewDisplayMetalRate(APIView):
   
    def get(self,request):
       
        res_data = {}
       
        purity_queryset = Purity.objects.filter(is_active=True,is_visible=True)
       
        for purity in purity_queryset:
               
            Metal_rate_queryset = MetalRate.objects.filter(purity=purity.pk).last()
           
            if Metal_rate_queryset:
           
                display_name = str(Metal_rate_queryset.purity.metal.metal_name)+"_"+str(Metal_rate_queryset.purity.purity_name)
               
                res_data[display_name] = Metal_rate_queryset.rate
               
        return Response(
            {
                "data":res_data,
                "message":res_msg.retrieve("Display Metal Rate"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
      

####### OLD METAL RATE CRUD API #######
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class OldMetalRateViewSet(viewsets.ViewSet):

    def create(self, request):
        data = request.data
        data['metal'] = data.get('metal')
        data['created_at'] = timezone.now()
        data['created_by'] = request.user.id

        serializer = OldMetalRateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": res_msg.create('Old Metal Rate'),
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
            queryset = MetalOldRate.objects.get(id=pk)
        except Exception as err:
            return Response({
                "message": res_msg.not_exists('Old Metal Rate'),
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_200_OK)
        
        data = request.data
        data['metal'] = data.get('metal')
        data['modified_at'] = timezone.now()
        data['modified_by'] = request.user.id

        serializer = OldMetalRateSerializer(queryset, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": res_msg.update('Old Metal Rate'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        return Response({
                "data": serializer.errors,
                "message": res_msg.in_valid_fields(),
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_200_OK)
    

    def destroy(self, request, pk):
        try:
            queryset = MetalOldRate.objects.get(id=pk)
            queryset.delete()
            return Response({
                "message": res_msg.delete('Old Metal Rate'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        except MetalOldRate.DoesNotExist:
            return Response({
                "message": res_msg.not_exists('Old Metal Rate'),
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
        

####### OLD METAL RATE LIST API #######
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class OldMetalRateList(APIView):

    def get(self, request,metal=None):

        if metal != None:
            queryset = MetalOldRate.objects.get(metal=metal)

            list = {
                'old_metal_rate' : queryset.old_metal_rate
            }

            try:
                tax_queryset = TaxDetailsAudit.objects.filter(metal=metal).order_by('-id').first()

                if tax_queryset:
                    tax_percent_queryset = PurchaseTaxDetails.objects.get(tax_details=tax_queryset.tax_details)

                    list['inter_gst'] = (tax_percent_queryset.purchase_tax_igst + tax_percent_queryset.purchase_surcharge_percent)
                    list['intra_gst'] = (tax_percent_queryset.purchase_tax_sgst + tax_percent_queryset.purchase_tax_cgst + tax_percent_queryset.purchase_surcharge_percent)
                    list['additional_charges'] = tax_percent_queryset.purchase_additional_charges
            except Exception as err:
                list['inter_gst'] = 0
                list['intra_gst']=0
                list['additional_charges'] = 0
           
            return Response({
                "data": list,
                "message": res_msg.retrieve('Old Metal Rate'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        
        else:
            queryset = MetalOldRate.objects.all().order_by('id')
            
            serializer = OldMetalRateSerializer(queryset,many=True)
            
            return Response({
                "data": {
                    "list": serializer.data,
                },
                "message": res_msg.retrieve('Old Metal Rate'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
    

    def post(self, request):

        search = request.data.get('search') if request.data.get('search') else ''
        from_date = request.data.get('from_date') if request.data.get('from_date') else None
        to_date = request.data.get('to_date') if request.data.get('to_date') else None
        page = request.data.get('page') if request.data.get('page') else 1
        try:
            items_per_page = int(request.data.get('items_per_page', MetalOldRate.objects.all().count()))
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
                queryset = list(MetalOldRate.objects.filter(Q(metal__metal_name__icontains=search) | Q(metal__metal_code__icontains=search),**filter_condition).order_by('id'))
        elif search != '':
                queryset = list(MetalOldRate.objects.filter(Q(metal__metal_name__icontains=search) | Q(metal__metal_code__icontains=search)).order_by('id'))
        else:
            queryset = list(MetalOldRate.objects.filter(Q(metal__metal_name__icontains=search) | Q(metal__metal_code__icontains=search)).order_by('id'))
        
        paginated_data = Paginator(queryset, items_per_page)
        serializer = OldMetalRateSerializer(paginated_data.get_page(page), many=True)

        res_data = []
        for i in range(0,len(serializer.data)):
            dict_data = serializer.data[i]
            dict_data['metal_name'] = queryset[i].metal.metal_name

            res_data.append(dict_data)

        return Response({
            "data": {
                "list": res_data,
                "total_pages": paginated_data.num_pages,
                "current_page": page,
                "total_items": len(queryset),
                "current_items": len(serializer.data)
            },
            "message": res_msg.retrieve('Metal'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)


####### TAX DETAILS AUDIT CRUD API #######
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class TaxDetailsAuditViewSet(viewsets.ViewSet):

    def create(self, request):
        data = request.data
        data['created_at'] = timezone.now()
        data['created_by'] = request.user.id

        serializer = TaxDetailsAuditSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": res_msg.create('Tax Details Audit'),
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
            queryset = TaxDetailsAudit.objects.get(id=pk)
        except Exception as err:
            return Response({
                "message": res_msg.not_exists('Tax Details Audit'),
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_200_OK)
        
        data = request.data
        data['modified_at'] = timezone.now()
        data['modified_by'] = request.user.id

        serializer = TaxDetailsAuditSerializer(queryset, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": res_msg.update('Tax Details Audit'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        return Response({
                "data": serializer.errors,
                "message": res_msg.in_valid_fields(),
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_200_OK)
    

    def retrieve(self, request, pk):
        try:
            queryset = TaxDetailsAudit.objects.get(id=pk)
            serializer = TaxDetailsAuditSerializer(queryset)

            return Response({
                "data": serializer.data,
                "message": res_msg.retrieve('Tax Details Audit'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        except TaxDetailsAudit.DoesNotExist:
            return Response({
                "message": res_msg.not_exists('Tax Details Audit'),
                "status": status.HTTP_204_NO_CONTENT
            }, status=status.HTTP_200_OK)
        

    def destroy(self, request, pk):
        try:
            queryset = TaxDetailsAudit.objects.get(id=pk)
            queryset.delete()
            return Response({
                "message": res_msg.delete('Tax Details Audit'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        except TaxDetailsAudit.DoesNotExist:
            return Response({
                "message": res_msg.not_exists('Tax Details Audit'),
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
        

####### TAX DETAILS AUDIT LIST API #######
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class TaxAuditDetailsList(APIView):
    def get(self, request):

        queryset = TaxDetailsAudit.objects.all().order_by('id')
        serializer = TaxDetailsAuditSerializer(queryset,many=True)
           
        return Response({
            "data": {
                "list": serializer.data,
            },
            "message": res_msg.retrieve('Tax Audit Details'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
    
    def post(self, request):
        search = request.data.get('search') if request.data.get('search') else ''
        from_date = request.data.get('from_date') if request.data.get('from_date') else None
        to_date = request.data.get('to_date') if request.data.get('to_date') else None
        page = request.data.get('page') if request.data.get('page') else 1
        try:
            items_per_page = int(request.data.get('items_per_page', TaxDetailsAudit.objects.all().count()))
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
                queryset = list(TaxDetailsAudit.objects.filter(Q(metal__metal_name__icontains=search),**filter_condition).order_by('id'))
        elif search != '':
                queryset = list(TaxDetailsAudit.objects.filter(Q(metal__metal_name__icontains=search)).order_by('id'))
        else:
            queryset = list(TaxDetailsAudit.objects.filter(Q(metal__metal_name__icontains=search)).order_by('id'))
        
        paginated_data = Paginator(queryset, items_per_page)
        serializer = TaxDetailsAuditSerializer(paginated_data.get_page(page), many=True)

        res_data = []
        for i in range(0,len(serializer.data)):
            dict_data = serializer.data[i]
            dict_data['metal_name'] = queryset[i].metal.metal_name
            dict_data['tax_name'] = queryset[i].tax_details.tax_name

            res_data.append(dict_data)

        return Response({
            "data": {
                "list": res_data,
                "total_pages": paginated_data.num_pages,
                "current_page": page,
                "total_items": len(queryset),
                "current_items": len(serializer.data)
            },
            "message": res_msg.retrieve('Tax Audit Details'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
    

###### REPAIR TYPE STATUS CHANGE API VIEW ######
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class RepairTypeStatusView(APIView):
    def get(self,request,pk):
        try:
            queryset = RepairType.objects.get(id=pk)

            queryset.is_active=not(queryset.is_active)
            queryset.save()

            serializer = RepairTypeSerializer(queryset)
            return Response(
                {
                    "data" : serializer.data,
                    "message":res_msg.change("Repair Type Status"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        except RepairType.DoesNotExist:
            return Response(
                {
                    "message":res_msg.not_exists("Repair Type"),
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
        

####### TAX DETAILS AUDIT CRUD API #######
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class CashCounterViewSet(viewsets.ViewSet):

    def create(self, request):
        data = request.data
        data['created_at'] = timezone.now()
        data['created_by'] = request.user.id

        serializer = CashCounterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            queryset = CashCounter.objects.get(id=serializer.data['id'])
            password = make_password(queryset.password)
            update_data = {
                "password" : password
            }
            update_serializer = CashCounterSerializer(queryset,data=update_data,partial=True)
            if update_serializer.is_valid():
                update_serializer.save()
            else:
                return Response({
                    "data": serializer.errors,
                    "message": res_msg.in_valid_fields(),
                    "status": status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_200_OK)

            return Response({
                "data": serializer.data,
                "message": res_msg.create('Cash Counter'),
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
            queryset = CashCounter.objects.get(id=pk)
        except Exception as err:
            return Response({
                "message": res_msg.not_exists('Cash Counter'),
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_200_OK)
        
        data = request.data
        password = make_password(data.get('password'))
        data['password'] = password
        data['modified_at'] = timezone.now()
        data['modified_by'] = request.user.id

        serializer = CashCounterSerializer(queryset, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": res_msg.update('Cash Counter'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        return Response({
                "data": serializer.errors,
                "message": res_msg.in_valid_fields(),
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_200_OK)
    

    def retrieve(self, request, pk):
        try:
            queryset = CashCounter.objects.get(id=pk)
            serializer = CashCounterSerializer(queryset)

            return Response({
                "data": serializer.data,
                "message": res_msg.retrieve('Cash Counter'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        except CashCounter.DoesNotExist:
            return Response({
                "message": res_msg.not_exists('Cash Counter'),
                "status": status.HTTP_204_NO_CONTENT
            }, status=status.HTTP_200_OK)
        

    def destroy(self, request, pk):
        try:
            queryset = CashCounter.objects.get(id=pk)
            queryset.delete()
            return Response({
                "message": res_msg.delete('Cash Counter'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        except CashCounter.DoesNotExist:
            return Response({
                "message": res_msg.not_exists('Cash Counter'),
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
        

####### CASH COUNTER LIST API #######
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class CashCounterList(APIView):
    def get(self, request):

        queryset = CashCounter.objects.filter(is_active=True).order_by('id')
        serializer = CashCounterSerializer(queryset,many=True)
           
        return Response({
            "data": {
                "list": serializer.data,
            },
            "message": res_msg.retrieve('Cash Counter'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
    
    def post(self, request):
        search = request.data.get('search') if request.data.get('search') else ''
        active_status = request.data.get('active_status') if request.data.get('active_status') != None else None
        from_date = request.data.get('from_date') if request.data.get('from_date') else None
        to_date = request.data.get('to_date') if request.data.get('to_date') else None
        page = request.data.get('page') if request.data.get('page') else 1
        try:
            items_per_page = int(request.data.get('items_per_page', CashCounter.objects.all().count()))
            if items_per_page == 0:
                items_per_page = 10 
        except Exception as err:
            items_per_page = 10 

        filter_condition={}
        if search != "":
            filter_condition['counter_name__icontains']=search

        if from_date != None and to_date!= None:
           fdate =from_date+'T00:00:00.899010+05:30'
           tdate =to_date+'T23:59:59.899010+05:30'
           date_range=(fdate,tdate)
           filter_condition['created_at__range']=date_range

        if active_status != None:
            filter_condition['is_active']=active_status

        if len(filter_condition) != 0:
                queryset = list(CashCounter.objects.filter(**filter_condition).order_by('id'))
        else:
            queryset = list(CashCounter.objects.all().order_by('id'))
        
        paginated_data = Paginator(queryset, items_per_page)
        serializer = CashCounterSerializer(paginated_data.get_page(page), many=True)

        res_data = []
        for i in range(0,len(serializer.data)):
            dict_data = serializer.data[i]

            res_data.append(dict_data)

        return Response({
            "data": {
                "list": res_data,
                "total_pages": paginated_data.num_pages,
                "current_page": page,
                "total_items": len(queryset),
                "current_items": len(serializer.data)
            },
            "message": res_msg.retrieve('Cash counter Details'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
    

###### CASH COUNTER STATUS CHANGE API VIEW ######
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class CashCounterStatusView(APIView):
    def get(self,request,pk):
        try:
            queryset = CashCounter.objects.get(id=pk)

            queryset.is_active=not(queryset.is_active)
            queryset.save()

            serializer = CashCounterSerializer(queryset)
            return Response(
                {
                    "data" : serializer.data,
                    "message":res_msg.change("Cash counter Status"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        except CashCounter.DoesNotExist:
            return Response(
                {
                    "message":res_msg.not_exists("Cash Counter"),
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
        

###### CASH COUNTER CHECKING API VIEW ######
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class CashCounterCheckView(APIView):
    def post(self,request):
        try:
            data = request.data
            queryset = CashCounter.objects.get(id=data.get('counter_name'))

            if check_password(data.get('password'), queryset.password):
                return Response(
                    {
                        "message": "Successful",
                        "status" : status.HTTP_200_OK
                    }, status=status.HTTP_200_OK)
            else:
                return Response(
                    {
                        "message": "Failed to open, Password is Incorrect",
                        "status" : status.HTTP_204_NO_CONTENT
                    }, status=status.HTTP_200_OK)
        except Exception as err:
            return Response(
                {
                    "data":str(err),
                    "message":res_msg.something_else(),
                    "status":status.HTTP_400_BAD_REQUEST
                },status=status.HTTP_200_OK
            )