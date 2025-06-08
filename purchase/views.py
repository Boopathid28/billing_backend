import random
import uuid
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.response import Response
from backend import settings
from billing.models import BillingDetails, BillingExchangeDetails, EstimationDiamondDetails, EstimationOldGold, EstimationStoneDetails, EstimationTagItems
from billing.serializer import EstimateDetailsSerializer
from books.serializer import AccountHeadDetailsSerailizer
from customer.serializer import CustomerSerializer
from masters.models import MetalRate, PurchaseTaxDetails, SalesTaxDetails, TaxDetails, TaxDetailsAudit
from masters.serializer import PurchaseTaxDetailsSerializer
from organizations.models import Staff
from product.models import SubItemWeightCalculation
from django.db.models import Sum
from django.db.models import Q
from purchase.serializers import  *
from .models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes, authentication_classes
from django.utils import timezone
from django.db.models import ProtectedError
from django.core.paginator import Paginator
from app_lib.response_messages import ResponseMessages
from accounts.serializer import *
from accounts.models import *
from repair_management.models import *
from repair_management.views import *
from order_management.models import *
from order_management.views import *
from vendor_management.models import VendorLedger
from vendor_management.serializer import VendorLedgerSerializer

res_msg = ResponseMessages()

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class PurchaseTypeViewSet(viewsets.ViewSet):

    def create(self, request):

        data = request.data
        data['created_at'] = timezone.now()
        data['created_by'] = request.user.id
        serializer = PurchaseTypeSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": res_msg.create('PurchaseType'),
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
            queryset = PurchaseType.objects.get(id=pk)
        except Exception as err:
            return Response({
                "message": res_msg.not_exists('PurchaseType'),
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_200_OK)
        
        data = request.data
        data['modified_at'] = timezone.now()
        data['modified_by'] = request.user.id
        serializer = PurchaseTypeSerializer(queryset, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": res_msg.update('PurchaseType'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        return Response({
                "data": serializer.errors,
                "message": res_msg.in_valid_fields(),
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_200_OK)
    
    def destroy(self, request, pk):
        try:
            queryset = PurchaseType.objects.get(id=pk)
            queryset.delete()
            return Response({
                "message": res_msg.delete('PurchaseType'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        except PurchaseType.DoesNotExist:
            return Response({
                "message": res_msg.not_exists('PurchaseType'),
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
class PurchaseTypeList(APIView):

    def get(self, request):

        queryset = list(PurchaseType.objects.filter(is_active=True).order_by('id'))
        serializer = PurchaseTypeSerializer(queryset, many=True)

        return Response({
            "data": {
                "list": serializer.data,
            },
            "message": res_msg.retrieve('PurchaseType'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class PurchaseTaxList(APIView):
    def get(self, request, pk):

        try:
            tax_queryset = TaxDetails.objects.get(metal=pk)
            queryset = PurchaseTaxDetails.objects.get(tax_details = tax_queryset.id )
        except:
            return Response({
                "message": res_msg.not_exists('Purchase tax'),
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_200_OK)
        
        serializer = PurchaseTaxDetailsSerializer(queryset)
        res_data = serializer.data
        return Response({
                "data": res_data,
                "message": res_msg.retrieve('Customer'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class PurchaseViewset(viewsets.ViewSet):   
    def create(self,request):

        try:

            data = request.data
            # if request.user.role_id > 2:
            #     branch = request.user.branch_id
            # else:
            #     branch = data.get('branch')

            
          
            res_data={
              
                'bill_no':data.get('bill_no'),
                'po_id':data.get('po_id'),               
                'person_id':data.get('person_id'),
                'sgst':data.get('sgst')if data.get('sgst') else '0',
                'igst':data.get('igst')if data.get('igst') else '0',
                'gst':data.get('gst')if data.get('gst') else '0',
                'total_pieces':data.get('total_pieces'),
                'total_netweight':data.get('total_netweight'),
                'total_grossweight':data.get('total_grossweight'),
                'sub_total':data.get('sub_total'),
                'total_amount':data.get('total_amount'),
                'total_stone_amount':data.get('total_stone_amount'),
                'hallmark_amount':data.get('hallmark_amount'),
                'mc_amount':data.get('mc_amount'),
                'purchase_date' :data.get('purchase_date'),
                # 'branch':branch,
            }
            if request.user.role.is_admin == True :
                res_data['branch'] = data.get('branch')
            else:                
                res_data['branch'] = request.user.branch.pk

            res_data['created_at'] = timezone.now()
            res_data['created_by'] = request.user.id
            # try:
            #     queryset = PurchaseEntry.objects.get(estimation_no=data.get('estimation_no').lower(), branch=branch)
            #     return Response({
            #         "message": res_msg.already_exists('Estimation Number'),
            #         "status": status.HTTP_204_NO_CONTENT
            #     }, status=status.HTTP_200_OK)
            # except:
            #     pass
            serializer = PurchaseEntrySerializer(data=res_data)
            if serializer.is_valid():
                serializer.save()
                estimation_details=serializer.data
                
                items = request.data.get('item_details', []) 
                             
                if len(items) != 0:
                    for item_data in items:                            
                        item_data['purchaseentry']=estimation_details['id']
                        item_data['purchase_metal']=item_data['purchase_metal']
                        if item_data['purchase_purity'] != None:
                            item_data['purchase_purity ']=item_data['purchase_purity']
                        else:
                           item_data['purchase_purity']= "null"
                        

                        if item_data['purchase_item'] != None:
                           item_data['purchase_item']=item_data['purchase_item']
                        else:
                           item_data['purchase_item']=0    

                        if item_data['purchase_subitem'] != None:
                           item_data['purchase_subitem']=item_data['purchase_subitem']
                        else:
                           item_data['purchase_subitem']=0 

                        item_data['pieces']=item_data['pieces']
                        item_data['stone_pieces']=item_data['stone_pieces']
                        item_data['stone_weight']=item_data['stone_weight']
                        item_data['diamond_pieces']=item_data['diamond_pieces']
                        item_data['diamond_weight']=item_data['diamond_weight']
                        item_data['gross_weight']=item_data['gross_weight']
                        item_data['less_weight']=item_data['less_weight']
                        item_data['net_weight']=item_data['net_weight']  
                        item_data['total_amount']=item_data['total_amount'] 
                        item_data['created_at'] = timezone.now()
                        item_data['created_by'] = request.user.id

                        if len(item_data) != 0 :
                            oldgold_serializer = PurchaseItemDetailSerializer(data=item_data)
                            if oldgold_serializer.is_valid():
                                oldgold_serializer.save()
                                oldgold_item_serializer =oldgold_serializer.data
                            else:
                                raise Exception(oldgold_serializer.errors)
                        
                stones = request.data.get('stone_details', [])                
                if len(stones) != 0:
                    for stone_data in stones:
                        stone_data['purchaseentry']=estimation_details['id']
                        stone_data['purchase_item'] = oldgold_item_serializer['id']
                        stone_data['stone_name']=float(stone_data['stone_name'])
                        stone_data['stone_pieces']=float(stone_data['stone_pieces'])
                        stone_data['stone_weight']=float(stone_data['stone_weight'])
                        stone_data['stone_weight_type']=int(stone_data['stone_weight_type'])
                        stone_data['stone_rate']=float(stone_data['stone_rate'])
                        stone_data['stone_rate_type']=int(stone_data['stone_rate_type'])
                        stone_data['include_stone_weight']=stone_data['include_stone_weight']
                        stone_data['created_at'] = timezone.now()
                        stone_data['created_by'] = request.user.id
                        

                        if int(stone_data['stone_weight_type']) == int(settings.CARAT):
                            stone_data['stone_weight']=(float(stone_data['stone_weight'])/5)

                        if int(stone_data['stone_rate_type']) == int(settings.PERGRAM):
                            total_stone_value=float(stone_data['stone_rate']*stone_data['stone_weight'])
                            stone_data['total_stone_value']=total_stone_value
                        
                        if int(stone_data['stone_rate_type']) == int(settings.PERCARAT):
                            stone_rate = float(stone_data['stone_rate'])/5
                            stone_data['stone_rate'] = stone_rate
                            total_stone_value=float(stone_data['stone_rate']*stone_data['stone_weight'])
                            stone_data['total_stone_value']=total_stone_value

                        if int(stone_data['stone_rate_type']) == int(settings.PERPIECE):
                            total_stone_value=float(stone_data['stone_rate']*stone_data['stone_pieces'])
                            stone_data['total_stone_value']=total_stone_value

                        estimation_stone_serializer=PurchaseStoneDetailsSerializer(data=stone_data)
                        if estimation_stone_serializer.is_valid():
                            estimation_stone_serializer.save()
                        else:
                            raise Exception (estimation_stone_serializer.errors)

                diamond_details = request.data.get('diamond_details', [])                
                if len(stones) != 0:
                    for diamond in diamond_details :
                        diamond['purchaseentry']=estimation_details['id']
                        diamond['purchase_item'] = oldgold_item_serializer['id']
                        diamond['diamond_name'] = float(diamond['diamond_name'])
                        diamond['diamond_pieces'] = float(diamond['diamond_pieces'])
                        diamond['diamond_weight'] = float(diamond['diamond_weight'])
                        diamond['diamond_weight_type'] = int(diamond['diamond_weight_type'])
                        diamond['diamond_rate'] = float(diamond['diamond_rate'])
                        diamond['diamond_rate_type'] = int(diamond['diamond_rate_type'])
                        diamond['include_diamond_weight'] = diamond['include_diamond_weight']
                        diamond['created_at'] = timezone.now()
                        diamond['created_by'] = request.user.id

                        if int(diamond['diamond_weight_type']) == settings.CARAT :
                            diamond_weight=float(diamond['diamond_weight'])/5
                            diamond['diamond_weight']=diamond_weight


                        if int(diamond['diamond_rate_type']) ==settings.PERGRAM:
                            total_diamond_value=float(diamond['diamond_rate']*diamond['diamond_weight'])
                            diamond['total_diamond_value'] = total_diamond_value

                        if int(diamond['diamond_rate_type']) == settings.PERCARAT:
                            diamond_rate=float(diamond['diamond_rate'])/5
                            diamond['diamond_rate']=diamond_rate
                            total_diamond_value=float(diamond['diamond_rate']*diamond['diamond_weight'])
                            diamond['total_diamond_value'] = total_diamond_value

                        if int(diamond['diamond_rate_type']) ==settings.PERPIECE:
                            total_diamond_value=float(diamond['diamond_rate']*diamond['diamond_pieces'])
                            diamond['total_diamond_value'] = total_diamond_value

                        estimation_diamond_serializer=PurchaseDiamondDetailsSerializer(data=diamond)
                        if estimation_diamond_serializer.is_valid():
                            estimation_diamond_serializer.save()
                        else:
                            raise Exception(estimation_diamond_serializer.errors)                
                return Response(
                    {
                        "data":serializer.data,
                        "message":res_msg.create("Purchase billing"),
                        "status":status.HTTP_201_CREATED
                    },status=status.HTTP_200_OK)
            
            else:
                raise Exception(serializer.errors)
        
        except Exception as err:            
            return Response(
                {
                    "data":str(err),
                    "message":res_msg.something_else(),
                    "status":status.HTTP_204_NO_CONTENT
                },status=status.HTTP_200_OK
            )
        

    def update(self,request,pk):

        try:

            data = request.data
            # if request.user.role_id > 2:
            #     branch = request.user.branch_id
            # else:
            #     branch = data.get('branch')
            try:
                purchase_queryset = PurchaseEntry.objects.get(id=pk)
                purchaseitem_queryset = PurchaseItemDetail.objects.filter(purchaseentry_id=pk)          
                purchastone_queryset = PurchaseStoneDetails.objects.filter(purchaseentry_id=pk)
                purchasediamond_queryset = PurchaseDiamondDetails.objects.filter(purchaseentry_id=pk)

                if purchasediamond_queryset is not None:
                    purchasediamond_queryset.delete()

                if purchastone_queryset is not None:
                    purchastone_queryset.delete()

                if purchaseitem_queryset is not None:
                    purchaseitem_queryset.delete()

                
                
             


                
                res_data={
        
                    'bill_no':data.get('bill_no'),
                    'po_id':data.get('po_id'),                 
                    'person_id':data.get('person_id'),
                    'sgst':data.get('sgst'),
                    'igst':data.get('igst'),
                    'gst':data.get('gst'),
                    'total_pieces':data.get('total_pieces'),
                    'total_netweight':data.get('total_netweight'),
                    'total_grossweight':data.get('total_grossweight'),
                    'sub_total':data.get('sub_total'),
                    'total_amount':data.get('total_amount'),
                    'total_stone_amount':data.get('total_stone_amount'),
                    'hallmark_amount':data.get('hallmark_amount'),
                    'mc_amount':data.get('mc_amount'),
                    'purchase_date' :data.get('purchase_date'),
                    # 'branch':branch,
                }
                if request.user.role.is_admin == True :
                    res_data['branch'] = data.get('branch')
                else:                
                    res_data['branch'] = request.user.branch.pk
              
                res_data['created_at'] = purchase_queryset.created_at
                res_data['created_by'] = purchase_queryset.created_by.pk
                res_data['modified_at'] = timezone.now()
                res_data['modified_by'] = request.user.id

                serializer = PurchaseEntrySerializer(purchase_queryset,data=res_data)
                if serializer.is_valid():
                    serializer.save()
                    estimation_details=serializer.data
                    
                    items = request.data.get('item_details', []) 
                                
                    if len(items) != 0:
                        for item_data in items:                            
                            item_data['purchaseentry']=estimation_details['id']
                            item_data['purchase_metal']=item_data['purchase_metal']
                            if item_data['purchase_purity'] != None:
                                item_data['purchase_purity ']=item_data['purchase_purity']
                            else:
                                item_data['purchase_purity']= "null"
                                
                            if item_data['purchase_item'] != None:
                                item_data['purchase_item']=item_data['purchase_item']
                            else:
                                item_data['purchase_item']=0    

                            if item_data['purchase_subitem'] != None:
                                item_data['purchase_subitem']=item_data['purchase_subitem']
                            else:
                                item_data['purchase_subitem']=0 
                                
                            item_data['pieces']=item_data['pieces']
                            item_data['stone_pieces']=item_data['stone_pieces']
                            item_data['stone_weight']=item_data['stone_weight']
                            item_data['diamond_pieces']=item_data['diamond_pieces']
                            item_data['diamond_weight']=item_data['diamond_weight']
                            item_data['gross_weight']=item_data['gross_weight']
                            item_data['less_weight']=item_data['less_weight']
                            item_data['net_weight']=item_data['net_weight']  
                            item_data['total_amount']=item_data['total_amount']
                            if len(item_data) != 0 :
                                oldgold_serializer = PurchaseItemDetailSerializer(data=item_data)
                                if oldgold_serializer.is_valid():
                                    oldgold_serializer.save()
                                    oldgold_item_serializer =oldgold_serializer.data
                                else:
                                    raise Exception(oldgold_serializer.errors)
                            
                    stones = request.data.get('stone_details', [])                
                    if len(stones) != 0:
                        for stone_data in stones:
                            stone_data['purchaseentry']=estimation_details['id']
                            stone_data['purchase_item'] = oldgold_item_serializer['id']
                            stone_data['stone_name']=float(stone_data['stone_name'])
                            stone_data['stone_pieces']=float(stone_data['stone_pieces'])
                            stone_data['stone_weight']=float(stone_data['stone_weight'])
                            stone_data['stone_weight_type']=int(stone_data['stone_weight_type'])
                            stone_data['stone_rate']=float(stone_data['stone_rate'])
                            stone_data['stone_rate_type']=int(stone_data['stone_rate_type'])
                            stone_data['include_stone_weight']=stone_data['include_stone_weight']
                            

                            if int(stone_data['stone_weight_type']) == int(settings.CARAT):
                                stone_data['stone_weight']=(float(stone_data['stone_weight'])/5)

                            if int(stone_data['stone_rate_type']) == int(settings.PERGRAM):
                                total_stone_value=float(stone_data['stone_rate']*stone_data['stone_weight'])
                                stone_data['total_stone_value']=total_stone_value
                            
                            if int(stone_data['stone_rate_type']) == int(settings.PERCARAT):
                                stone_rate = float(stone_data['stone_rate'])/5
                                stone_data['stone_rate'] = stone_rate
                                total_stone_value=float(stone_data['stone_rate']*stone_data['stone_weight'])
                                stone_data['total_stone_value']=total_stone_value

                            if int(stone_data['stone_rate_type']) == int(settings.PERPIECE):
                                total_stone_value=float(stone_data['stone_rate']*stone_data['stone_pieces'])
                                stone_data['total_stone_value']=total_stone_value

                            estimation_stone_serializer=PurchaseStoneDetailsSerializer(data=stone_data)
                            if estimation_stone_serializer.is_valid():
                                estimation_stone_serializer.save()
                            else:
                                raise Exception (estimation_stone_serializer.errors)

                    diamond_details = request.data.get('diamond_details', [])                
                    if len(stones) != 0:
                        for diamond in diamond_details :
                            diamond['purchaseentry']=estimation_details['id']
                            diamond['purchase_item'] = oldgold_item_serializer['id']
                            diamond['diamond_name'] = float(diamond['diamond_name'])
                            diamond['diamond_pieces'] = float(diamond['diamond_pieces'])
                            diamond['diamond_weight'] = float(diamond['diamond_weight'])
                            diamond['diamond_weight_type'] = int(diamond['diamond_weight_type'])
                            diamond['diamond_rate'] = float(diamond['diamond_rate'])
                            diamond['diamond_rate_type'] = int(diamond['diamond_rate_type'])
                            diamond['include_diamond_weight'] = diamond['include_diamond_weight']

                            if int(diamond['diamond_weight_type']) == settings.CARAT :
                                diamond_weight=float(diamond['diamond_weight'])/5
                                diamond['diamond_weight']=diamond_weight


                            if int(diamond['diamond_rate_type']) ==settings.PERGRAM:
                                total_diamond_value=float(diamond['diamond_rate']*diamond['diamond_weight'])
                                diamond['total_diamond_value'] = total_diamond_value

                            if int(diamond['diamond_rate_type']) == settings.PERCARAT:
                                diamond_rate=float(diamond['diamond_rate'])/5
                                diamond['diamond_rate']=diamond_rate
                                total_diamond_value=float(diamond['diamond_rate']*diamond['diamond_weight'])
                                diamond['total_diamond_value'] = total_diamond_value

                            if int(diamond['diamond_rate_type']) ==settings.PERPIECE:
                                total_diamond_value=float(diamond['diamond_rate']*diamond['diamond_pieces'])
                                diamond['total_diamond_value'] = total_diamond_value

                            estimation_diamond_serializer=PurchaseDiamondDetailsSerializer(data=diamond)
                            if estimation_diamond_serializer.is_valid():
                                estimation_diamond_serializer.save()
                            else:
                                raise Exception(estimation_diamond_serializer.errors)
                    return Response(
                        {
                            "data":serializer.data,
                            "message":res_msg.update("Purchase Entry"),
                            "status": status.HTTP_200_OK
                        }, status=status.HTTP_200_OK)
                
                else:
                    raise Exception(serializer.errors)
                
            except PurchaseEntry.DoesNotExist:
                return Response(
                    {
                        "message":res_msg.not_exists("Purchase Entry"),
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
        
    def destroy(self, request, pk):
        try:
            purchase_queryset = PurchaseEntry.objects.get(id=pk)
            purchaseitem_queryset = PurchaseItemDetail.objects.filter(purchaseentry=pk)          
            purchastone_queryset = PurchaseStoneDetails.objects.filter(purchaseentry=pk)
            purchasediamond_queryset = PurchaseDiamondDetails.objects.filter(purchaseentry=pk)

            if purchasediamond_queryset :
                purchasediamond_queryset.delete()                

            if purchastone_queryset :
                purchastone_queryset.delete()

            if purchaseitem_queryset :
                purchaseitem_queryset.delete()

            if purchase_queryset :
                purchase_queryset.delete()

            return Response({
                "message": res_msg.delete('Purchase Entry'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        except PurchaseEntry.DoesNotExist:
            return Response({
                "message": res_msg.not_exists('PurchaseEntry'),
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
           
    def get(self,request,pk):
 
        try:
            listqueryset=PurchaseEntry.objects.get(id=pk)
            serializer = PurchaseEntrySerializer(listqueryset)
            person_name =''
        
            person = Customer.objects.get(pk =listqueryset.person_id)
            if person :
                person_name = person.customer_name
            else:
                person_name = None

           
            serialized = {}
            serialized = serializer.data
            serialized['person_name'] = person_name

            purchaseitem = PurchaseItemDetail.objects.filter(purchaseentry=pk).values('id','purchaseentry','purchase_metal','purchase_purity','purchase_item','purchase_subitem','purchase_metal__metal_name','purchase_purity__purity_name','pieces','stone_pieces','stone_weight','diamond_pieces','diamond_weight','gross_weight','less_weight','net_weight','total_amount')
            purchaseitem_serialized =[]
            
            for i in purchaseitem:
                if i['purchase_item'] != 0:
                    item = Item.objects.get(pk=i['purchase_item'])             
                    item_name = item.item_name
                else:
                    item_name = None

                if i['purchase_subitem'] != 0:
                    subitem = SubItem.objects.get(pk =i['purchase_subitem'])                
                    subitem_name = subitem.sub_item_name
                else:
                    subitem_name = None
                
                item_dict = dict(i)
                item_dict['purchase_item__item_name'] = item_name
                item_dict['purchase_subitem__sub_item_name'] = subitem_name
                purchaseitem_serialized.append(item_dict)
      
            stoneitem = PurchaseStoneDetails.objects.filter(purchaseentry=pk).values('id','purchaseentry','purchase_item','stone_name','stone_name__stone_name','stone_pieces','stone_weight','stone_weight_type','stone_weight_type__weight_name','stone_rate','stone_rate_type','stone_rate_type__type_name','include_stone_weight','total_stone_value')
            diamonditem = PurchaseDiamondDetails.objects.filter(purchaseentry=pk).values('id','purchaseentry','purchase_item','diamond_name','diamond_name__stone_name','diamond_pieces','diamond_weight','diamond_weight_type','diamond_weight_type__weight_name','diamond_rate','diamond_rate_type','diamond_rate_type__type_name','include_diamond_weight','total_diamond_value')
        
        
            return Response(
                {
                    "data":{
                        "purchase_list": serialized,
                        "iteam_details":purchaseitem_serialized,
                        "stoneitem":stoneitem,    
                        "diamonditem":diamonditem,            
                        },
                    "message":res_msg.retrieve("Transfer Item"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )

        except PurchaseEntry.DoesNotExist:
            
            return Response(
                {
                    "message":res_msg.not_exists("Purachse Entry List"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class PurchaseEntryListView(APIView):
   
    def post(self, request):

        search = request.data.get('search') if request.data.get('search')  else ''
        from_date = request.data.get('from_date') if request.data.get('from_date') else None
        to_date = request.data.get('to_date') if request.data.get('to_date')  else None        
        page = request.data.get('page') if request.data.get('page') else 1
        items_per_page = request.data.get('items_per_page') if request.data.get('items_per_page') else 10        
        branch = request.data.get('branch') if request.data.get('branch')  else None
    
        filter_condition={}
    
        if from_date != None and to_date != None :
            date_range=(from_date,to_date)

            filter_condition['purchase_date__range'] = date_range
        
        if request.user.role.is_admin == True :
            if request.data.get('branch') != None:
                filter_condition['branch'] = branch
        else:                
            filter_condition['branch'] = request.user.branch.pk
    
        if len(filter_condition) != 0 : 
            queryset = list(PurchaseEntry.objects.filter(Q(bill_no__icontains=search),**filter_condition).order_by('id'))
        elif search != '':
            queryset = list(PurchaseEntry.objects.filter(Q(bill_no__icontains=search)).order_by('id'))
        else :
            queryset = list(PurchaseEntry.objects.all().order_by('id'))

        paginated_data = Paginator(queryset, items_per_page)
        serializer = PurchaseEntrySerializer(paginated_data.get_page(page),many=True)

        res_data = []
        for i in range(0, len(serializer.data)):

            custom = serializer.data[i]  
            custom['purchase_typename'] = 'Old purchase'
            custom['branch_name'] = queryset[i].branch.branch_name
            custom['purchase_person_name'] = 'Customer'
            advance_amount = 0
            balance_amount = 0
            total_amount = queryset[i].total_amount

            payment = Purchasepayment.objects.aggregate(total=Sum('paid_amount'))
        
            if payment != None:
                # advance_amount = payment.total

                balance_amount = int(total_amount)-(advance_amount)
            custom['advance_amount'] = advance_amount
            custom['balance_amount'] = balance_amount
            person_name = ''

            person = Customer.objects.get(id =queryset[i].person_id)
            if person :
                person_name = person.customer_name
            else:
                person_name = None
            
            custom['person_name'] = person_name

            item = PurchaseItemDetail.objects.filter(purchaseentry = queryset[i].pk).count()
            custom['item'] =item
            
            res_data.append(custom)
        
        return Response({
            "data": {
                "list": res_data,
                "total_pages": paginated_data.num_pages,
                "current_page": page,
                "total_items": len(queryset),
                "current_items": len(res_data)
            },
            "message": res_msg.retrieve('Purchase List'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
        
       

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class PurchaseorderIDView(APIView):
 
    def get(self,request):
        try:
            queryset=PurchaseEntry.objects.all().order_by('-id')[0]
            new_id=int(queryset.pk)+1
            prefix = 'OGP-00'  # Prefix for the purchase bill number
            purchase_id = f'{prefix}{new_id}'
          
            return Response(
                {
                    "po_id":purchase_id,
                    "message":res_msg.retrieve("Purchase"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        except Exception as err:
            return Response(
                {
                    "po_id":"OGP-001",
                    "message":res_msg.retrieve("Purchase"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class BillingAPIView(APIView):
    def get(self,request,billno):
        if billno != None :
           
            try:                
                queryset = BillingDetails.objects.get(bill_no = billno)  
                old_gold_details=[]
                old_gold_queryset = BillingOldGold.objects.filter(billing_details=queryset.pk)
                pieces = 0
                net_weight =0
                gross_weight =0
                totalitem =0
                totalamount =0
                bill=queryset.bill_date
                bill_date = bill.strftime('%Y-%m-%d')
                
                for old_gold in old_gold_queryset:
                    old_details={
                        'id':old_gold.pk,                        
                        'gross_weight':old_gold.old_gross_weight,
                        'metal':old_gold.old_metal.pk,
                        'metal_name':old_gold.old_metal.metal_name,
                        'metal_rate':old_gold.metal_rate,
                        'net_weight':old_gold.old_net_weight,
                        'old_rate':old_gold.old_metal_rate,                        
                        # 'purchase_purity':old_gold.purity.purity_name,
                        # 'purchase_purity_id':old_gold.purity.pk,
                        'today_rate':old_gold.today_metal_rate,
                        'total_amount':old_gold.total_old_gold_value,
                    }
                    # pieces = pieces + 1
                    totalitem = totalitem +1
                    totalamount = old_gold.total_old_gold_value+totalamount
                    net_weight  = old_gold.old_net_weight + net_weight
                    gross_weight  = old_gold.old_gross_weight + gross_weight
                    bill_date = bill_date
                    old_gold_details.append(old_details)
                    
            except Exception as err:
                return Response(
                    {
                   
                        "message" : res_msg.not_exists('Bill Number'),
                        "status": status.HTTP_204_NO_CONTENT,                        
                    }, status=status.HTTP_200_OK
            )  

            return Response(
                {
                    "data":{
                        "old_gold_details" : old_gold_details,
                        # "pieces":pieces,
                        "netweight":net_weight,
                        "gross_weight":gross_weight,
                        "totalitem":totalitem,
                        "gst_amount": 0,  
                        "others": 0,      
                        "totalamount":totalamount,           
                        "bill_id": queryset.pk,                        
                        "bill_no": queryset.bill_no,                       
                        "customer_mobile":queryset.customer_mobile,
                        "customer_id":queryset.customer_details.pk,
                        "customer_name":queryset.customer_details.customer_name,
                        "bill_date":bill_date
                        
                    },
                    "message" : res_msg.retrieve("Bill details"),
                    "status": status.HTTP_200_OK
                }, status=status.HTTP_200_OK
            )  
        else:
            return Response(
                {
                    "message" : "Invalid Bill Number",
                    "status": status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_200_OK
            )  
        

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class BillingListView(APIView):
    def get(self,request,branch=None):
        
        try:
            # if request.user.role_id <= 2:
            #     if branch == None:            
            #         branch = 0
            #     else:
            #         branch = branch
            # else:
            #     branch = request.user.branch_id
                
            filter_dict={}
            if request.user.role.is_admin == True :
                branch = branch               
            else:                
               branch = request.user.branch.pk
          
            filter_dict['branch'] = branch   
         
            queryset = list(BillingDetails.objects.filter(**filter_dict).values('id','bill_no','customer_mobile','customer_details__id','customer_details__customer_name'))
            # queryset = list(BillingDetails.objects.all().values('id','bill_no','customer_mobile','customer_details__id','customer_details__customer_name'))

            return Response(
                {
                    "data":{
                        'list':queryset
                    },
                    "message":res_msg.retrieve("Billing Details"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        except EstimateDetails.DoesNotExist:

            return Response(
                {
                    "message":res_msg.not_exists("Billing Details"),
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
class CalculateView(APIView):
    def post(self, request):        
        detail = request.data.get('detail', [])

        total_item = 0
        total_amount = 0.0
        net_weight_total = 0.0
        gross_weight_total = 0.0
        pieces = 0

        #Getting data from user
        for item in detail:
            total_item = total_item + 1
            if item.get('total_amount') != "":
                total_amount = total_amount + float(item.get('total_amount'))
            if item.get('net_weight') != "":
                net_weight_total = net_weight_total + float(item.get('net_weight'))
            if item.get('gross_weight') != "":
                gross_weight_total = gross_weight_total + float(item.get('gross_weight'))
            if item.get('pieces') != "":
                pieces = pieces + int(item.get('pieces'))

        return Response({
            "data": {
                "netweight": net_weight_total,
                "gross_weight": gross_weight_total,
                "totalitem": total_item,
                "gst_amount": 0,  
                "others": 0,      
                "totalamount": total_amount,   
                "pieces":pieces
            },
            "message": "Purchase entry calculation",
            "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)

        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class NewPurchaseViewset(viewsets.ViewSet):   
    @transaction.atomic
    def create(self,request):

        try:
            data = request.data            
            res_data={               
                'total_pieces':data.get('total_pieces'),
                'purchase_order_id':data.get('purchase_order_id'),
                'due_date':data.get('due_date'),
                'order_date':data.get('order_date'),
                'total_net_weight':data.get('total_net_weight'),
                'total_gross_weight':data.get('total_gross_weight'),
                'total_pure_weight':data.get('total_pure_weight'),
                'total_amount':data.get('total_amount'),
                'designer_name':data.get('designer_name'),
                'branch':data.get('branch'),
                'no_of_days':data.get('no_of_days'),
                'is_billed':False,
                'paid_amount':"0.00",
                'paid_weight':"0.00"
            }
            if request.user.role.is_admin == True :
                branch = data.get('branch')
            else:                
                branch = request.user.branch.pk

            res_data['branch'] = branch
            res_data['created_at'] = timezone.now()
            res_data['created_by'] = request.user.id
          
            serializer = NewPurchaseSerializer(data=res_data)
            if serializer.is_valid():
                serializer.save()
                new_purchase=serializer.data     

                items = request.data.get('item_details', []) 

                if len(items) != 0:
                    for item in items:       
                        item_data = {}

                        fixed_rate = item.get('fixed_rate',None)
                        per_gram_rate = item.get('per_gram_rate',None)
                        per_piece_rate = item.get('per_piece_rate',None)
                        wastage = item.get('wastage',None)
                        flat_wastage = item.get('flat_wastage',None)
                        making_charge_pergram = item.get('making_charge_pergram',None)
                        flat_makingcharge = item.get('flat_makingcharge',None)
                        touch = item.get('touch',None)

                        item_data['purchase_order']=new_purchase['id']
                        item_data['item'] = item['item']
                        item_data['sub_item'] = item['sub_item']
                        item_data['pieces'] = item.get('pieces',0)
                        item_data['gross_weight'] = item.get('gross_weight',0.0)
                        item_data['less_weight'] = item.get('less_weight',0.0)
                        item_data['net_weight'] = item.get('net_weight',0.0)
                        item_data['pure_weight']=item.get('pure_weight',0.0)

                        item_data['fixed_rate']=fixed_rate if fixed_rate != None else 0
                        item_data['per_gram_rate']=per_gram_rate if per_gram_rate != None else 0
                        item_data['per_piece_rate']=per_piece_rate if per_piece_rate != None else 0
                        item_data['wastage']=wastage if wastage != None else 0
                        item_data['flat_wastage']=flat_wastage if flat_wastage != None else 0
                        item_data['making_charge_pergram']=making_charge_pergram if making_charge_pergram != None else 0
                        item_data['flat_makingcharge']=flat_makingcharge if flat_makingcharge != None else 0
                        item_data['calculation_type']=item.get('calculation_type')

                        item_data['touch']= touch if touch !=None else 0
                        item_data['metal']=item.get('metal')
                        item_data['itemid']=item.get('item_id')
                        item_data['stone_pieces'] = item.get('stone_pieces',0)
                        item_data['stone_weight'] = item.get('stone_weight',0.0)
                        item_data['stone_amount'] = item.get('stone_amount',0.0)
                        item_data['diamond_pieces'] = item.get('diamond_pieces',0)
                        item_data['diamond_weight'] = item.get('diamond_weight',0.0)
                        item_data['diamond_amount'] = item.get('diamond_amount',0.0)
                        item_data['hallmark_charges'] = item.get('hallmark_charges',0.0)
                        item_data['other_charges'] = item.get('other_charges',0.0)
                        item_data['gst_amount'] = item.get('gst_amount',0.0)
                        item_data['total_amount'] = item.get('total_amount',0.0)
                        item_data['created_at'] = timezone.now()
                        item_data['created_by'] = request.user.id
                       
                        if len(item_data) != 0 :
                            item_serializer = NewPurchaseItemdetailSerializer(data=item_data)
                            if item_serializer.is_valid():
                                item_serializer.save()
                                new_purchase_item =item_serializer.data
                            else:
                                raise Exception(item_serializer.errors)
                            
                        ledger_data = {}
                        ledger_data['vendor_details'] = serializer.data['designer_name']
                        ledger_data['transaction_date'] = timezone.now()
                        ledger_data['refference_number'] = serializer.data['purchase_order_id']
                        ledger_data['transaction_type'] = settings.PURCHASE_VENDOR_LEDGER
                        ledger_data['transaction_weight'] = serializer.data['total_gross_weight']
                        ledger_data['transaction_amount'] = serializer.data['total_amount']
                        ledger_data['branch'] = branch
                                
                        ledger_serializer = VendorLedgerSerializer(data=ledger_data)
                        if ledger_serializer.is_valid():
                            ledger_serializer.save()
                        else:
                            transaction.set_rollback(True)
                            return Response(
                                {
                                    "data":ledger_serializer.errors,
                                    "message":res_msg.not_create("New Purchase"),
                                    "status":status.HTTP_400_BAD_REQUEST
                                },status=status.HTTP_200_OK
                            )
                                
                    return Response(
                        {
                            "data":serializer.data,
                            "message":res_msg.create("New Purchase Order"),
                            "status":status.HTTP_201_CREATED
                        },status=status.HTTP_200_OK)
                else:
                    return Response(
                        {
                            "message":res_msg.not_exists("Item Details"),
                            "status":status.HTTP_201_CREATED
                        },status=status.HTTP_200_OK)
            else:
                raise Exception(serializer.errors)
        
        except Exception as err:   
            transaction.set_rollback(True)         
            return Response(
                {
                    "data":str(err),
                    "message":res_msg.something_else(),
                    "status":status.HTTP_204_NO_CONTENT
                },status=status.HTTP_200_OK
            )
        
    @transaction.atomic
    def update(self,request,pk):

        try:
            queryset = NewPurchase.objects.get(id = pk)

            data = request.data
            if request.user.role.is_admin == True :
                branch = data.get('branch')
            else:                
                branch = request.user.branch.pk
           
            res_data={

                'total_pieces':data.get('total_pieces'),
                'purchase_order_id':data.get('purchase_order_id'),
                'due_date':data.get('due_date'),
                'order_date':data.get('order_date'),
                'total_net_weight':data.get('total_net_weight'),
                'total_gross_weight':data.get('total_gross_weight'),
                'total_item':data.get('total_item'),
                'others':data.get('others')if data.get('others') else '0',
                'hallmark':data.get('hallmark')if data.get('hallmark') else '0',
                'total_amount':data.get('total_amount'),
                'total_pure_weight':data.get('total_pure_weight'),
                'designer_name':data.get('designer_name'),
                'branch':data.get('branch'),
                'no_of_days':data.get('no_of_days'),
                # 'is_billed':queryset.is_billed,
                'paid_amount':queryset.paid_amount,
                'paid_weight':queryset.paid_weight
            }
            if data.get('total_amount') == queryset.paid_amount and data.get('total_pure_weight') == queryset.paid_weight:
                res_data['is_billed'] = True
            else:
                res_data['is_billed'] = False

            if request.user.role.is_admin == True :
                res_data['branch'] = data.get('branch')
            else:                
                res_data['branch'] = request.user.branch.pk

            res_data['modified_at'] = timezone.now()
            res_data['modified_by'] = request.user.id
          
            serializer = NewPurchaseSerializer(queryset,data=res_data,partial=True)
            if serializer.is_valid():
                serializer.save()
                new_purchase=serializer.data 

                # purchaseorder_item_queryset  = NewPurchaseItemdetail.objects.filter(purchase_order=pk)             
                # if purchaseorder_item_queryset: 
                #     purchaseorder_item_queryset.delete()

                items = request.data.get('item_details', []) 
                if len(items) != 0:
                    for item in items: 
                        item_data = {}   
                        try:
                            purchase_item_id = item.get('id') if item.get('id') else 0
                            purchaseorder_item_queryset  = NewPurchaseItemdetail.objects.get(id=purchase_item_id) 

                            if len(purchaseorder_item_queryset) != 0:
                                fixed_rate = item.get('fixed_rate',None)
                                per_gram_rate = item.get('per_gram_rate',None)
                                per_piece_rate = item.get('per_piece_rate',None)
                                wastage = item.get('wastage',None)
                                flat_wastage = item.get('flat_wastage',None)
                                making_charge_pergram = item.get('making_charge_pergram',None)
                                flat_makingcharge = item.get('flat_makingcharge',None)
                                touch = item.get('touch',None)

                                item_data['purchase_order']=new_purchase['id']
                                item_data['item'] = item['item']
                                item_data['sub_item'] = item['sub_item']
                                item_data['pieces'] = item.get('pieces',0)
                                item_data['gross_weight'] = item.get('gross_weight',0.0)
                                item_data['less_weight'] = item.get('less_weight',0.0)
                                item_data['net_weight'] = item.get('net_weight',0.0)
                                item_data['pure_weight']=item.get('pure_weight',0.0)

                                item_data['fixed_rate']=fixed_rate if fixed_rate != None else 0
                                item_data['per_gram_rate']=per_gram_rate if per_gram_rate != None else 0
                                item_data['per_piece_rate']=per_piece_rate if per_piece_rate != None else 0
                                item_data['wastage']=wastage if wastage != None else 0
                                item_data['flat_wastage']=flat_wastage if flat_wastage != None else 0
                                item_data['making_charge_pergram']=making_charge_pergram if making_charge_pergram != None else 0
                                item_data['flat_makingcharge']=flat_makingcharge if flat_makingcharge != None else 0
                                item_data['calculation_type']=item.get('calculation_type')

                                item_data['touch']= touch if touch !=None else 0
                                item_data['metal']=item.get('metal')
                                item_data['itemid']=item.get('item_id')
                                item_data['stone_pieces'] = item.get('stone_pieces',0)
                                item_data['stone_weight'] = item.get('stone_weight',0.0)
                                item_data['stone_amount'] = item.get('stone_amount',0.0)
                                item_data['diamond_pieces'] = item.get('diamond_pieces',0)
                                item_data['diamond_weight'] = item.get('diamond_weight',0.0)
                                item_data['diamond_amount'] = item.get('diamond_amount',0.0)
                                item_data['hallmark_charges'] = item.get('hallmark_charges',0.0)
                                item_data['other_charges'] = item.get('other_charges',0.0)
                                item_data['gst_amount'] = item.get('gst_amount',0.0)
                                item_data['total_amount'] = item.get('total_amount',0.0)
                                item_data['modified_at'] = timezone.now()
                                item_data['modified_by'] = request.user.id
                                
                                item_serializer = NewPurchaseItemdetailSerializer(purchaseorder_item_queryset,data=item_data,partial=True)
                                if item_serializer.is_valid():
                                    item_serializer.save()
                                    new_purchase_item =item_serializer.data
                                else:
                                    raise Exception(item_serializer.errors)
                                    
                        except NewPurchaseItemdetail.DoesNotExist:

                            fixed_rate = item.get('fixed_rate',None)
                            per_gram_rate = item.get('per_gram_rate',None)
                            per_piece_rate = item.get('per_piece_rate',None)
                            wastage = item.get('wastage',None)
                            flat_wastage = item.get('flat_wastage',None)
                            making_charge_pergram = item.get('making_charge_pergram',None)
                            flat_makingcharge = item.get('flat_makingcharge',None)
                            touch = item.get('touch',None)

                            item_data['purchase_order']=new_purchase['id']
                            item_data['item'] = item['item']
                            item_data['sub_item'] = item['sub_item']
                            item_data['pieces'] = item.get('pieces',0)
                            item_data['gross_weight'] = item.get('gross_weight',0.0)
                            item_data['less_weight'] = item.get('less_weight',0.0)
                            item_data['net_weight'] = item.get('net_weight',0.0)
                            item_data['pure_weight']=item.get('pure_weight',0.0)

                            item_data['fixed_rate']=fixed_rate if fixed_rate != None else 0
                            item_data['per_gram_rate']=per_gram_rate if per_gram_rate != None else 0
                            item_data['per_piece_rate']=per_piece_rate if per_piece_rate != None else 0
                            item_data['wastage']=wastage if wastage != None else 0
                            item_data['flat_wastage']=flat_wastage if flat_wastage != None else 0
                            item_data['making_charge_pergram']=making_charge_pergram if making_charge_pergram != None else 0
                            item_data['flat_makingcharge']=flat_makingcharge if flat_makingcharge != None else 0
                            item_data['calculation_type']=item.get('calculation_type')

                            item_data['touch']= touch if touch !=None else 0
                            item_data['metal']=item.get('metal')
                            item_data['itemid']=item.get('item_id')
                            item_data['stone_pieces'] = item.get('stone_pieces',0)
                            item_data['stone_weight'] = item.get('stone_weight',0.0)
                            item_data['stone_amount'] = item.get('stone_amount',0.0)
                            item_data['diamond_pieces'] = item.get('diamond_pieces',0)
                            item_data['diamond_weight'] = item.get('diamond_weight',0.0)
                            item_data['diamond_amount'] = item.get('diamond_amount',0.0)
                            item_data['hallmark_charges'] = item.get('hallmark_charges',0.0)
                            item_data['other_charges'] = item.get('other_charges',0.0)
                            item_data['gst_amount'] = item.get('gst_amount',0.0)
                            item_data['total_amount'] = item.get('total_amount',0.0)
                            item_data['modified_at'] = timezone.now()
                            item_data['modified_by'] = request.user.id

                            item_serializer = NewPurchaseItemdetailSerializer(data=item_data)
                            if item_serializer.is_valid():
                                item_serializer.save()
                                new_purchase_item =item_serializer.data
                            else:
                                raise Exception(item_serializer.errors)
                        
                return Response(
                    {
                        "message":res_msg.update("New Purchase"),
                        "status":status.HTTP_200_OK
                    },status=status.HTTP_200_OK) 
            else:
                raise Exception(serializer.errors)
        
        except NewPurchase.DoesNotExist:
            return Response(
                {
                    "message":res_msg.not_exists("New Purchase "),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        
        except Exception as err:
            transaction.set_rollback(True)
            return Response(
                {
                    "data" : str(err),
                    "message":res_msg.something_else(),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        
    def destroy(self, request, pk):
        try:
            queryset = NewPurchase.objects.get(id = pk)

            purchaseorder_item_queryset  = NewPurchaseItemdetail.objects.filter(purchase_order=pk)  
           
            if queryset.is_canceled == True:
                
                return Response(
                    {
                        "message":"The Purchase Bill is already canceled",
                        "status":status.HTTP_204_NO_CONTENT
                    },status=status.HTTP_200_OK
                )
            
            queryset.is_canceled = True
            queryset.save()
            
            ledger_queryset = VendorLedger.objects.get(refference_number=queryset.purchase_order_id,transaction_type= settings.PURCHASE_VENDOR_LEDGER)
            
            ledger_queryset.is_canceled = True
            ledger_queryset.save()

            queryset.delete()

            return Response({
                "message": res_msg.delete('New Purchase'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        except NewPurchase.DoesNotExist:
            return Response({
                "message": res_msg.not_exists('New Purchase'),
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
        
    def get(self,request,pk): 
        try:
            listqueryset = NewPurchase.objects.get(id=pk)
            serializer = NewPurchaseSerializer(listqueryset)
            
            serialized = serializer.data
            serialized['person_name'] = listqueryset.designer_name.account_head_name

            purchase_orderitem_queryset = NewPurchaseItemdetail.objects.filter(purchase_order=pk)
            purchaseitem_serializer = NewPurchaseItemdetailSerializer(purchase_orderitem_queryset,many=True)
            
            detail = []
            for i in range(0, len(purchaseitem_serializer.data)):
                dict_data = purchaseitem_serializer.data[i]
                dict_data['metal_name'] = purchase_orderitem_queryset[i].metal.metal_name
                dict_data['item_name'] = purchase_orderitem_queryset[i].item.item_name
                dict_data['sub_item_name'] = purchase_orderitem_queryset[i].sub_item.sub_item_name
                dict_data['from_db'] = True
            
                stone_item_queryset  = NewPurchaseStoneDetails.objects.filter(purchase_order=pk)
                # stone_item_serializer = NewPurchaseStoneDetailsSerializer(stone_item_queryset,many=True)
               
                stone_details=[]
                for stone in stone_item_queryset:
                    stone_data={
                        'id':stone.pk,
                        'stone_name':stone.stone_name.pk,
                        'stone_pieces':stone.stone_pieces,
                        'stone_weight':stone.stone_weight,
                        'stone_weight_type':stone.stone_weight_type.pk,
                        'stone_rate':stone.stone_rate,
                        'stone_rate_type':stone.stone_rate_type.pk,
                        'include_stone_weight':stone.include_stone_weight,
                        'from_db':True
                    }
                    stone_details.append(stone_data)

                diamond_item_queryset  = NewPurchaseDiamondDetails.objects.filter(purchase_order=pk)
                # diamond_item_serializer = NewPurchaseDiamondDetailsSerializer(diamond_item_queryset,many=True)
             
                diamond_details = []           
                for diamond in diamond_item_queryset:
                    diamond_data={
                        'id':diamond.pk,
                        'diamond_name':diamond.diamond_name.pk,
                        'diamond_pieces':diamond.diamond_pieces,
                        'diamond_weight':diamond.diamond_weight,
                        'diamond_weight_type':diamond.diamond_weight_type.pk,
                        'diamond_rate':diamond.diamond_rate,
                        'diamond_rate_type':diamond.diamond_rate_type.pk,
                        'include_diamond_weight':diamond.include_diamond_weight,
                        'from_db':True
                    }
                    diamond_details.append(diamond_data)

                dict_data['stone_details'] = stone_details
                dict_data['diamond_details'] = diamond_details
                
                detail.append(dict_data)

            serialized['new_purchase_item']=detail
           
            return Response(
                {
                    "data":serialized,
                  
                    "message":res_msg.retrieve("New Purchase"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )

        except NewPurchase.DoesNotExist:            
            return Response(
                {
                    "message":res_msg.not_exists("New Purchase List"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class NewPurchaseorderIDView(APIView):
 
    def get(self,request):
        try:
            queryset=NewPurchase.objects.all().order_by('-id')[0]
            new_id=int(queryset.pk)+1
            prefix = 'NWP-00'  # Prefix for the purchase bill number
            purchase_id = f'{prefix}{new_id}'
          
            return Response(
                {
                    "po_id":purchase_id,
                    "message":res_msg.retrieve("New Purchase"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        except Exception as err:
            return Response(
                {
                    "po_id":"NWP-001",
                    "message":res_msg.retrieve("New Purchase"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class NewPurchaseListView(APIView):
   
    def post(self, request):
        
        search = request.data.get('search') if request.data.get('search')  else ''
        from_date = request.data.get('from_date') if request.data.get('from_date') else None
        to_date = request.data.get('to_date') if request.data.get('to_date')  else None        
        page = request.data.get('page') if request.data.get('page') else 1
        items_per_page = request.data.get('items_per_page') if request.data.get('items_per_page') else 10
        branch = request.data.get('branch') if request.data.get('branch') else None
   
        filter_condition={}

        if request.user.role.is_admin == True :
            if branch != None:
                filter_condition['branch'] = branch
        else:                
            filter_condition['branch'] = request.user.branch.pk
       
        if from_date != None and to_date != None:
            date_range=(from_date,to_date)
            filter_condition['order_date__range'] = date_range

        if len(filter_condition) != 0 : 
            queryset = list(NewPurchase.objects.filter(Q(purchase_order_id__icontains=search | Q(designer_name__icontains=search)),**filter_condition).order_by('id'))
        elif search != '':
            queryset = list(NewPurchase.objects.filter(Q(purchase_order_id__icontains=search) | Q(designer_name__icontains=search)).order_by('id'))
        else :
            queryset = list(NewPurchase.objects.all().order_by('id'))

        paginated_data = Paginator(queryset, items_per_page)

        serializer = NewPurchaseSerializer(paginated_data.get_page(page),many=True)

        res_data = []
        for i in range(0, len(serializer.data)):
            custom = serializer.data[i]  

            if queryset[i].is_billed == True:
                custom['status'] = "Received"
            else:
                custom['status'] = "Pending"
            custom['designer_name_id'] = queryset[i].designer_name.pk 
            custom['designer_name'] = queryset[i].designer_name.account_head_name    
            custom['purchase_typename'] = 'New purchase'
            custom['branch_name'] = queryset[i].branch.branch_name
            custom['customer_name'] = queryset[i].designer_name.account_head_name
            res_data.append(custom)
    
        return Response({
            "data": {
                "list": res_data,
                "total_pages": paginated_data.num_pages,
                "current_page": page,
                "total_items": len(queryset),
                "current_items": len(res_data)
            },
            "message": res_msg.retrieve('New Purchase List'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class VendorDetailView(APIView):
    def get(self, request,pk,type):
        
        branch = request.data.get('branch') if request.data.get('branch') else None
        filter_condition={}

        if request.user.role.is_admin == True:
            if branch != None:    
                if type == 1:        
                    filter_condition['branch'] = branch
                elif type == 2:
                    filter_condition['repair_details__branch'] = branch
        else:
            if type == 1:
                filter_condition['branch'] = request.user.branch.pk
            elif type == 2:
                filter_condition['repair_details__branch'] = branch

        vendor_queryset=AccountHeadDetails.objects.get(id=pk)

        if type == settings.NEWPURCHASE_VENDOR_PAYMENT:
            queryset = list(NewPurchase.objects.filter(designer_name = pk,is_billed = False,**filter_condition).order_by('-id'))

            serializer = NewPurchaseSerializer(queryset, many=True)
            res_data = []
            total_unpaid_weight = 0
            total_unpaid_amount = 0
            for i in range(0, len(serializer.data)):
                dict_data = serializer.data[i]
                dict_data['pending_amount']=(queryset[i].total_amount)-(queryset[i].paid_amount)
                dict_data['pending_weight']=(queryset[i].total_pure_weight)-(queryset[i].paid_weight)
                dict_data['branch_name'] = queryset[i].branch.branch_name    
                dict_data['designer_name'] = queryset[i].designer_name.account_head_name                
                res_data.append(dict_data)

                total_unpaid_weight = total_unpaid_weight + dict_data['pending_weight']
                total_unpaid_amount = total_unpaid_amount + dict_data['pending_amount']

        elif type == settings.REPAIR_VENDOR_PAYMENT:
            repair_queryset = RepairOrderIssued.objects.filter(vendor_name = pk, **filter_condition).order_by('-id')
            repair_serializer = RepairOrderIssuedSerializer(repair_queryset, many=True)
            res_data = []
            total_unpaid_weight = 0
            total_unpaid_amount = 0
            for j in range(0, len(repair_serializer.data)):
                dict_data = repair_serializer.data[j]
                dict_data['pending_amount']=(repair_queryset[j].repair_details.total_vendor_charges)-(repair_queryset[j].paid_amount)
                dict_data['pending_weight']=(repair_queryset[j].repair_details.total_issued_weight)-(repair_queryset[j].paid_weight)
                dict_data['branch_name'] = repair_queryset[j].repair_details.branch.branch_name    
                dict_data['designer_name'] = repair_queryset[j].vendor_name.account_head_name                
                res_data.append(dict_data)

                total_unpaid_weight = total_unpaid_weight + dict_data['pending_weight']
                total_unpaid_amount = total_unpaid_amount + dict_data['pending_amount']

        elif type == settings.ORDER_VENDOR_PAYMENT:
            orderissue_queryset = list(OrderIssue.objects.filter(vendor = pk).order_by('-id'))
            order_serializer = OrderIssueSerializer(orderissue_queryset, many=True)
            res_data = []
            total_unpaid_weight = 0
            total_unpaid_amount = 0
            for order_issue in range(0, len(order_serializer.data)):
                dict_data = order_serializer.data[order_issue]
                try:
                    if branch != None:
                        order_details = OrderDetails.objects.get(id=orderissue_queryset[order_issue].order_id.pk,branch=branch)
                        dict_data['pending_amount']=(order_details.approximate_amount)-(orderissue_queryset[order_issue].paid_amount)
                        dict_data['pending_weight']=(order_details.total_weight)-(orderissue_queryset[order_issue].paid_weight)
                        dict_data['branch_name'] = order_details.branch.branch_name    
                        dict_data['designer_name'] = orderissue_queryset[order_issue].vendor.account_head_name  
                    else:
                        order_details = OrderDetails.objects.get(id=orderissue_queryset[order_issue].order_id.pk)
                        dict_data['pending_amount']=(order_details.approximate_amount)-(orderissue_queryset[order_issue].paid_amount)
                        dict_data['pending_weight']=(order_details.total_weight)-(orderissue_queryset[order_issue].paid_weight)
                        dict_data['branch_name'] = order_details.branch.branch_name    
                        dict_data['designer_name'] = orderissue_queryset[order_issue].vendor.account_head_name  

                    res_data.append(dict_data)
                    total_unpaid_weight = total_unpaid_weight + dict_data['pending_weight']
                    total_unpaid_amount = total_unpaid_amount + dict_data['pending_amount']
                except OrderDetails.DoesNotExist:
                    pass

        return Response({
            "data": {
                "list": res_data,
                "credit_balance_gm":vendor_queryset.credit_balance_gm,
                "credit_balance_rupee":vendor_queryset.credit_balance_rupee,
                "total_unpaid_weight":total_unpaid_weight,
                "total_unpaid_amount":total_unpaid_amount
            },
            "message": res_msg.retrieve('New Purchase'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
        
        # except NewPurchase.DoesNotExist:            
        #         return Response(
        #             {
        #                 "message":res_msg.not_exists("New Purchase List"),
        #                 "status":status.HTTP_404_NOT_FOUND
        #             },status=status.HTTP_200_OK
        #         )
 
        
        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class MetalRatecutView(APIView):
    def post(self, request):        
        
        metal_details = request.data.get('details', [])
        if len(metal_details) != 0:
            metal_data_list = []
            for metal_data in metal_details:
                metal_data['created_at'] = timezone.now()
                metal_data['created_by'] = request.user.id
                metal_data['metal'] = metal_data['metal']
                metal_data['metal_weight'] = float(metal_data['metal_weight'])
                metal_data['pure_calculation'] = float(metal_data['pure_calculation'])
                metal_data['pure_weight'] = float(metal_data['pure_weight'])
                metal_data['payment_bill_no'] = metal_data['payment_bill_no']
                metal_data['date'] = metal_data['date']
                metal_data['designer_name'] = metal_data['designer_name']
                metal_data['purchase_order'] = metal_data['purchase_order']
                metal_data_list.append(metal_data)

            serializer = MetalRateCutSerializer(data=metal_data_list, many=True)
            
            for metal_data in metal_details:
                purchase_order_ids = metal_data['purchase_order'].split(',')
                remaining_amount = metal_data['pure_weight']  # Initialize remaining amount with the total pure weight

                vendor_queryset=AccountHeadDetails.objects.get(id=metal_data['designer_name'])   

                if request.data.get('type') == settings.NEWPURCHASE_VENDOR_PAYMENT:       # Purchase Vendor Payment
                    for purchase_order_id in purchase_order_ids:
                        
                        queryset = NewPurchase.objects.get(id=purchase_order_id)

                        #checking given weight and total weight is equal or greater
                        if float(remaining_amount) == float(queryset.total_pure_weight) or  float(remaining_amount) > float(queryset.total_pure_weight):
                            #Calculating the pending weight
                            pending_amount = float(queryset.total_pure_weight) - float(queryset.paid_weight) 
                            #From given weight calculate how much weight should pay
                            remaining_amount = float(remaining_amount) - pending_amount
                            #given weight is greater than total weight so we are updatimg total weight to paid weight
                            data={}
                            data['paid_weight'] = queryset.total_pure_weight
                            new_purchase_serializer =NewPurchaseSerializer(queryset,data=data)
                            if new_purchase_serializer.is_valid():
                                new_purchase_serializer.save()

                        else:
                            #Intialising given weight
                            intial_amount = float(remaining_amount)

                            pending_amount = float(queryset.total_pure_weight) - float(queryset.paid_weight) 

                            #checking given weight is greater than pending weight
                            if float(remaining_amount) >= pending_amount :
                                remaining_amount = float(remaining_amount) - pending_amount
                            else:
                                remaining_amount = 0

                            #Adding already paid weight with initial weight
                            amount = queryset.paid_weight+intial_amount
                        
                            #checking given weight greater or equal to total weight
                            if float(amount) >= float(queryset.total_pure_weight):  
                                #updating paid weight with total weight value                                               
                                pay_amount = queryset.total_pure_weight

                            else: 
                                pay_amount = amount
                            #saving data      
                            data={}
                            data['paid_weight'] = pay_amount
                            new_purchase_serializer =NewPurchaseSerializer(queryset,data=data)
                            if new_purchase_serializer.is_valid():
                                new_purchase_serializer.save()

                        #Checking paid weight,paid amount is equal to total pure weight and amount       
                        if queryset.total_amount == queryset.paid_amount and queryset.total_pure_weight == queryset.paid_weight:            
                            res_data={'is_billed':True}
                            
                        else:
                            res_data={'is_billed':False}
            
                        new_purchase_serializer =NewPurchaseSerializer(queryset,data=res_data)
                        if new_purchase_serializer.is_valid():
                            new_purchase_serializer.save()

                elif request.data.get('type') == settings.REPAIR_VENDOR_PAYMENT:            #Repair Order Vendor Payment
                    for repair_id in purchase_order_ids:

                        repair_queryset = RepairOrderIssued.objects.get(id=repair_id)

                        if float(remaining_amount) == float(repair_queryset.repair_details.total_issued_weight) or  float(remaining_amount) > float(repair_queryset.repair_details.total_vendor_charges):
                            
                            pending_amount = float(repair_queryset.repair_details.total_issued_weight) - float(repair_queryset.paid_weight) 
                            
                            remaining_amount = float(remaining_amount) - pending_amount
                            data={}
                            data['paid_weight'] = repair_queryset.repair_details.total_issued_weight
                            repair_serializer =RepairOrderIssuedSerializer(repair_queryset,data=data)
                            if repair_serializer.is_valid():
                                repair_serializer.save()

                        else:
                            intial_amount = float(remaining_amount)

                            pending_amount = float(repair_queryset.repair_details.total_issued_weight) - float(repair_queryset.paid_weight) 

                            if float(remaining_amount) >= pending_amount :
                                remaining_amount = float(remaining_amount) - pending_amount
                            else:
                                remaining_amount = 0

                            amount = repair_queryset.paid_weight+intial_amount

                            if float(amount) >= float(repair_queryset.repair_details.total_issued_weight):                                           
                                pay_amount = repair_queryset.repair_details.total_issued_weight
                            else: 
                                pay_amount = amount

                            data={}
                            data['paid_weight'] = pay_amount
                            repair_serializer =RepairOrderIssuedSerializer(repair_queryset,data=data)
                            if repair_serializer.is_valid():
                                repair_serializer.save()

                elif request.data.get('type') == settings.ORDER_VENDOR_PAYMENT:            #Repair Order Vendor Payment
                    for order_id in purchase_order_ids:

                        order_issue_queryset = OrderIssue.objects.get(id=order_id)

                        order_queryset = OrderDetails.objects.get(id=order_issue_queryset.order_id.pk)

                        if float(remaining_amount) == float(order_queryset.total_weight) or  float(remaining_amount) > float(order_queryset.approximate_amount):
                            
                            pending_amount = float(order_queryset.total_weight) - float(order_issue_queryset.paid_weight) 
                            
                            remaining_amount = float(remaining_amount) - pending_amount
                            data={}
                            data['paid_weight'] = order_queryset.total_weight
                            repair_serializer =RepairOrderIssuedSerializer(repair_queryset,data=data)
                            if repair_serializer.is_valid():
                                repair_serializer.save()

                        else:
                            intial_amount = float(remaining_amount)

                            pending_amount = float(order_queryset.total_weight) - float(order_issue_queryset.paid_weight) 

                            if float(remaining_amount) >= pending_amount :
                                remaining_amount = float(remaining_amount) - pending_amount
                            else:
                                remaining_amount = 0

                            amount = order_issue_queryset.paid_weight+intial_amount

                            if float(amount) >= float(order_queryset.total_weight):                                           
                                pay_amount = order_queryset.total_weight
                            else: 
                                pay_amount = amount

                            data={}
                            data['paid_weight'] = pay_amount
                            order_serializer =OrderIssueSerializer(order_issue_queryset,data=data)
                            if order_serializer.is_valid():
                                order_serializer.save()

            #if there is any remaining weight it will be added to vendor account 
            if remaining_amount != 0:               
                vendor_remain_amount = float(vendor_queryset.credit_balance_gm) +float(remaining_amount)                
                AccountHeadDetails.objects.filter(id=vendor_queryset.pk).update(credit_balance_gm=vendor_remain_amount)  

            if serializer.is_valid():
                serializer.save()
                return Response({
                    "message": res_msg.create('Metal rate cut'),
                    "status": status.HTTP_201_CREATED
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "data": serializer.errors,
                    "message": res_msg.in_valid_fields(),
                    "status": status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_200_OK)

        else:
            return Response({
                "message": res_msg.something_else(),
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_200_OK)
        

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class CashRatecutView(APIView):
    def post(self, request):    

        metal_details = request.data.get('details', [])
        if len(metal_details) != 0:
            metal_data_list = []
            for metal_data in metal_details:
                metal_data['created_at'] = timezone.now()
                metal_data['created_by'] = request.user.id
                metal_data['pure_weight'] = float(metal_data['pure_weight'])
                metal_data['rate'] = float(metal_data['rate'])
                metal_data['rate_cut'] = float(metal_data['rate_cut'])
                metal_data['payment_bill_no'] = metal_data['payment_bill_no']
                metal_data['date'] = metal_data['date']
                metal_data['designer_name'] = metal_data['designer_name']
                metal_data['purchase_order'] = metal_data['purchase_order']
                metal_data_list.append(metal_data)

            serializer = CashRateCutSerializer(data=metal_data_list, many=True)
         
            for metal_data in metal_details:
                purchase_order_ids = metal_data['purchase_order'].split(',')
                remaining_amount = metal_data['rate_cut']  # Initialize remaining amount with the total pure weight

                vendor_queryset=AccountHeadDetails.objects.get(id=metal_data['designer_name'])

                if request.data.get('type') == settings.NEWPURCHASE_VENDOR_PAYMENT:
                    for purchase_order_id in purchase_order_ids:
                    
                        queryset = NewPurchase.objects.get(id=purchase_order_id)

                        #Check given weight is equal or greater to totalpure weight
                        if float(remaining_amount) == float(queryset.total_pure_weight) or  float(remaining_amount) > float(queryset.total_pure_weight):
                            #calculating pending weight
                            pending_amount = float(queryset.total_pure_weight) - float(queryset.paid_weight) 
                            #Calculating how much weight should be paid with given weight
                            remaining_amount = float(remaining_amount) - pending_amount
                            #Updating the value as total pure weight because given weight is greater
                            data={}
                            data['paid_weight'] = queryset.total_pure_weight
                            new_purchase_serializer =NewPurchaseSerializer(queryset,data=data)
                            if new_purchase_serializer.is_valid():
                                new_purchase_serializer.save()

                        else:
                            #Intializing given weight
                            intial_amount = float(remaining_amount)
                            #calculatimg pending amount
                            pending_amount = float(queryset.total_pure_weight) - float(queryset.paid_weight) 

                            #Check the given weight greater or equal
                            if float(remaining_amount) >= pending_amount :
                                #if greater remaing amount is calculated from paid amount
                                remaining_amount = float(remaining_amount) - pending_amount
                            else:
                                remaining_amount = 0
                            #Calculate total amount with already paid weight and given weight
                            amount = queryset.paid_weight+intial_amount
                            
                            #Checking the amount is greater than total pure weight
                            if float(amount) >= float(queryset.total_pure_weight)  :
                                #Updating paid amount with total weight
                                pay_amount = queryset.total_pure_weight
                            else:          
                                #updating calculated amount     
                                pay_amount = amount
                                        
                            data={}
                            data['paid_weight'] = pay_amount
                            new_purchase_serializer =NewPurchaseSerializer(queryset,data=data)
                            if new_purchase_serializer.is_valid():
                                new_purchase_serializer.save()

                        #Checking and updating total weight,total amount with paid weight,paid amount       
                        if queryset.total_amount == queryset.paid_amount and queryset.total_pure_weight == queryset.paid_weight:            
                            res_data={'is_billed':True}                        
                        else:
                            res_data={'is_billed':False}
            
                        new_purchase_serializer =NewPurchaseSerializer(queryset,data=res_data)
                        if new_purchase_serializer.is_valid():
                            new_purchase_serializer.save()

                elif request.data.get('type') == settings.REPAIR_VENDOR_PAYMENT:
                    for repair_id in purchase_order_ids:
                    
                        repair_queryset = RepairOrderIssued.objects.get(id=repair_id)

                        #Check given weight is equal or greater to totalpure weight
                        if float(remaining_amount) == float(repair_queryset.repair_details.total_issued_weight) or  float(remaining_amount) > float(repair_queryset.repair_details.total_issued_weight):
                            #calculating pending weight
                            pending_amount = float(repair_queryset.repair_details.total_issued_weight) - float(repair_queryset.paid_weight) 
                            #Calculating how much weight should be paid with given weight
                            remaining_amount = float(remaining_amount) - pending_amount
                            #Updating the value as total pure weight because given weight is greater
                            data={}
                            data['paid_weight'] = repair_queryset.repair_details.total_issued_weight
                            repair_serializer =RepairOrderIssuedSerializer(repair_queryset,data=data)
                            if repair_serializer.is_valid():
                                repair_serializer.save()

                        else:
                            #Intializing given weight
                            intial_amount = float(remaining_amount)
                            #calculatimg pending amount
                            pending_amount = float(repair_queryset.repair_details.total_issued_weight) - float(repair_queryset.paid_weight) 

                            #Check the given weight greater or equal
                            if float(remaining_amount) >= pending_amount :
                                #if greater remaing amount is calculated from paid amount
                                remaining_amount = float(remaining_amount) - pending_amount
                            else:
                                remaining_amount = 0
                            #Calculate total amount with already paid weight and given weight
                            amount = repair_queryset.paid_weight+intial_amount
                            
                            #Checking the amount is greater than total pure weight
                            if float(amount) >= float(repair_queryset.repair_details.total_issued_weight)  :
                                #Updating paid amount with total weight
                                pay_amount = repair_queryset.repair_details.total_issued_weight
                            else:          
                                #updating calculated amount     
                                pay_amount = amount
                                        
                            data={}
                            data['paid_weight'] = pay_amount
                            repair_serializer =RepairOrderIssuedSerializer(repair_queryset,data=data)
                            if repair_serializer.is_valid():
                                repair_serializer.save()

                elif request.data.get('type') == settings.ORDER_VENDOR_PAYMENT:
                    for order_id in purchase_order_ids:
                    
                        order_issue_queryset = OrderIssue.objects.get(id=order_id)

                        order_queryset = OrderDetails.objects.get(id=order_issue_queryset.order_id.pk)

                        #Check given weight is equal or greater to totalpure weight
                        if float(remaining_amount) == float(order_queryset.total_weight) or  float(remaining_amount) > float(order_queryset.total_weight):
                            #calculating pending weight
                            pending_amount = float(order_queryset.total_weight) - float(order_issue_queryset.paid_weight) 
                            #Calculating how much weight should be paid with given weight
                            remaining_amount = float(remaining_amount) - pending_amount
                            #Updating the value as total pure weight because given weight is greater
                            data={}
                            data['paid_weight'] = order_queryset.total_weight
                            order_serializer =OrderIssueSerializer(order_issue_queryset,data=data)
                            if order_serializer.is_valid():
                                order_serializer.save()

                        else:
                            #Intializing given weight
                            intial_amount = float(remaining_amount)
                            #calculatimg pending amount
                            pending_amount = float(repair_queryset.repair_details.total_issued_weight) - float(queryset.paid_weight) 

                            #Check the given weight greater or equal
                            if float(remaining_amount) >= pending_amount :
                                #if greater remaing amount is calculated from paid amount
                                remaining_amount = float(remaining_amount) - pending_amount
                            else:
                                remaining_amount = 0
                            #Calculate total amount with already paid weight and given weight
                            amount = queryset.paid_weight+intial_amount
                            
                            #Checking the amount is greater than total pure weight
                            if float(amount) >= float(repair_queryset.repair_details.total_issued_weight)  :
                                #Updating paid amount with total weight
                                pay_amount = repair_queryset.repair_details.total_issued_weight
                            else:          
                                #updating calculated amount     
                                pay_amount = amount
                                        
                            data={}
                            data['paid_weight'] = pay_amount
                            repair_serializer =RepairOrderIssuedSerializer(repair_queryset,data=data)
                            if repair_serializer.is_valid():
                                repair_serializer.save()

            if remaining_amount != 0:
                #adding already credit balance gram with remaining weight and update value
                vendor_remain_amount = float(vendor_queryset.credit_balance_gm) +float(remaining_amount)                
                AccountHeadDetails.objects.filter(id=vendor_queryset.pk).update(credit_balance_gm=vendor_remain_amount)   

            if serializer.is_valid():
                serializer.save()
                return Response({
                    "message": res_msg.create('Cash rate cut'),
                    "status": status.HTTP_201_CREATED
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "data": serializer.errors,
                    "message": res_msg.in_valid_fields(),
                    "status": status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": res_msg.something_else(),
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_200_OK)
        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class AmountsettleView(APIView):
   
    def post(self, request):        
        data = request.data
        data['payment_bill_no'] = data.get('payment_bill_no')
        data['purchase_order'] = data.get('purchase_order')
        data['date'] = data.get('date')
        data['designer_name'] = data.get('designer_name')
        data['amount'] = float(data.get('amount'))    
        if data.get('discount') != None:
            data['discount']=float(data.get('discount'))

        data['created_at'] = timezone.now()
        data['created_by'] = request.user.id
        serializer = AmountSettleSerializer(data=data)

        vendor_queryset=AccountHeadDetails.objects.get(id=data.get('designer_name'))

        if serializer.is_valid():
            serializer.save()
            
            remaining_amount = data.get('amount')
            purchase_order_ids = data.get('purchase_order').split(',')
            if data.get('type') == settings.NEWPURCHASE_VENDOR_PAYMENT:
                for purchase_order_id in purchase_order_ids:
                    # Initialize remaining amount with the total pure weight
                
                    queryset = NewPurchase.objects.get(id=purchase_order_id)

                    if data.get('cash_receivable') == True:
                        # if queryset.total_amount == queryset.paid_amount:
                        #     exit
                        
                        #check given amount is greater than credit balance
                        if  float(data.get('amount'))  > float(vendor_queryset.credit_balance_rupee) or float(data.get('amount'))  == float(vendor_queryset.credit_balance_rupee):
                            #Calculating amount to be paid from vendor account balance and amount
                            rupee = float(data.get('amount')) - float(vendor_queryset.credit_balance_rupee)                            
                            ven_data={'credit_balance_rupee':"0.00"}
                            
                        else:
                            #Calculating amount to be paid from vendor account balance and amount
                            rupee = float(vendor_queryset.credit_balance_rupee) - float(data.get('amount'))  
                            if  float(data.get('amount')) > 0: 
                                ven_data={'credit_balance_rupee':rupee}                   
                                
                            else:
                                ven_data={'credit_balance_rupee':"0.00"}
                                
                        
                        ven_serializer = AccountHeadDetailsSerailizer(vendor_queryset,data=ven_data,partial=True)
                        if ven_serializer.is_valid():
                            ven_serializer.save()
                        else:
                            raise Exception(ven_serializer.errors)
                            
                        #Check given amount is greater or equal to total amount                    
                        if float(rupee) == float(queryset.total_amount) or  float(rupee) > float(queryset.total_amount):
                            #Calculate pending amount
                            pending_amount = float(queryset.total_amount) - float(queryset.paid_amount) 
                            #Calculate amount to be paid 
                            remaining_amount = float(rupee) - pending_amount  
                        
                            data={}
                            data['paid_amount'] = queryset.total_amount
                            new_purchase_serializer =NewPurchaseSerializer(queryset,data=data)
                            if new_purchase_serializer.is_valid():
                                new_purchase_serializer.save()
                            else:
                                #Initialize given amount
                                intial_amount = float(rupee)                        
                                #Calculate pending amount
                                pending_amount = float(queryset.total_amount) - float(queryset.paid_amount)                         
                                #Check given amount greater than pending amount
                            
                                if float(rupee) >= pending_amount :
                                    remaining_amount = float(rupee) - pending_amount
                                                            
                                else:
                                    remaining_amount = 0
                                
                                #Calcuate already paid amount with initial amount
                                amount = queryset.paid_amount+intial_amount

                                if float(amount) >= float(queryset.total_amount):
                                    #Update amount as totalamount
                                    pay_amount = queryset.total_amount
                                else:     
                                    #update calculate amount                       
                                    pay_amount = amount
                                            
                                data={}
                                data['paid_amount'] = pay_amount
                                new_purchase_serializer =NewPurchaseSerializer(queryset,data=data)
                                if new_purchase_serializer.is_valid():
                                    new_purchase_serializer.save()
                            
                            if remaining_amount != 0:
                                #Update remaing amount with already balance rupee                         
                                vendor_remain_amount = float(vendor_queryset.credit_balance_rupee) + float(remaining_amount)                          
                                AccountHeadDetails.objects.filter(id=vendor_queryset.pk).update(credit_balance_rupee=vendor_remain_amount)       
                        
                    else:
                        #Check given amount is greater or equal to total amount                    
                        if float(remaining_amount) == float(queryset.total_amount) or  float(remaining_amount) > float(queryset.total_amount):
                            #Calculate pending amount
                            pending_amount = float(queryset.total_amount) - float(queryset.paid_amount) 
                            #Calculate amount to be paid 
                            remaining_amount = float(remaining_amount) - pending_amount                    
                        
                            data={}
                            data['paid_amount'] = queryset.total_amount
                            new_purchase_serializer =NewPurchaseSerializer(queryset,data=data)
                            if new_purchase_serializer.is_valid():
                                new_purchase_serializer.save()

                            
                        else:
                            #Initialize given amount
                            intial_amount = float(remaining_amount)
                            #Calculate pending amount
                            pending_amount = float(queryset.total_amount) - float(queryset.paid_amount)                         
                            #Checkgiven amount greater than pending amount
                            if float(remaining_amount) >= pending_amount :
                                remaining_amount = float(remaining_amount) - pending_amount
                            else:
                                remaining_amount = 0
                        
                            #Calcuate already paid amount with initial amount
                            amount = queryset.paid_amount+intial_amount

                            if float(amount) >= float(queryset.total_amount):
                                #Update amount as totalamount
                                pay_amount = queryset.total_amount
                            else:     
                                #update calculate amount                       
                                pay_amount = amount
                                        
                            data={}
                            data['paid_amount'] = pay_amount
                            new_purchase_serializer =NewPurchaseSerializer(queryset,data=data)
                            if new_purchase_serializer.is_valid():
                                new_purchase_serializer.save()

                        if remaining_amount != 0:
                            #Update remaing amount with already balance rupee                         
                            vendor_remain_amount = float(vendor_queryset.credit_balance_rupee) + float(remaining_amount)
                            AccountHeadDetails.objects.filter(id=vendor_queryset.pk).update(credit_balance_rupee=vendor_remain_amount)

                    if data.get('metal_receivable') == True:
                    
                        #Calculate balance gram
                        balance = float(queryset.total_pure_weight) - float(queryset.paid_weight)
                        #Check if vendor gram is greater than balance
                        if float(vendor_queryset.credit_balance_gm) > float(balance) or float(vendor_queryset.credit_balance_gm) == float(balance):                    
                            amount = float(vendor_queryset.credit_balance_gm) - float(balance)   
                            ven_data={'credit_balance_gm':amount}

                        else:
                            amount =   float(balance) - float(vendor_queryset.credit_balance_gm)
                            ven_data={'credit_balance_gm':"0.00"}
                                
                        #Update the balance credit balance gram
                        ven_serializer = AccountHeadDetailsSerailizer(vendor_queryset,data=ven_data,partial=True)
                        if ven_serializer.is_valid():
                            ven_serializer.save()
                        else:
                            raise Exception(ven_serializer.errors)

                    
                        #Check Balance gram greater than total weight
                        if  float(vendor_queryset.credit_balance_gm) >= float(queryset.total_pure_weight) :                   
                            pay_weight = queryset.total_pure_weight
                        
                        else:
                            #Calculate  total weight with already paid weight
                            weight = float(queryset.paid_weight) + balance
                            #Check weight greater than total weight
                            if weight >= float(queryset.total_pure_weight):
                                #update value with totalweight
                                pay_weight = queryset.total_pure_weight
                            else:
                                pay_weight = float(queryset.paid_weight) + balance
                        
                        data = {}
                        data['paid_weight']= pay_weight                
                        new_purchase_serializer = NewPurchaseSerializer(queryset, data=data)
                        if new_purchase_serializer.is_valid():
                            new_purchase_serializer.save()
                    #Update if totalweight,total amount is equal to paid weight ,paid amount       
                    if queryset.total_amount == queryset.paid_amount and queryset.total_pure_weight == queryset.paid_weight:                     
                        res_data={'is_billed':True}
                    else:
                        res_data={'is_billed':False}  

                    new_purchase_serializer = NewPurchaseSerializer(queryset,data=res_data)
                    if new_purchase_serializer.is_valid():
                        new_purchase_serializer.save()
                    else:
                        new_purchase_serializer.errors 

                    #Final remaining amount update
                    if remaining_amount != 0:
                        #Update remaing amount with alreday balance rupee                         
                        vendor_remain_amount = float(vendor_queryset.credit_balance_rupee) + float(remaining_amount)
                        AccountHeadDetails.objects.filter(id=vendor_queryset.pk).update(credit_balance_rupee=vendor_remain_amount)

            elif data.get('type') == settings.REPAIR_VENDOR_PAYMENT:
                for repair_id in purchase_order_ids:
                
                    repair_queryset = RepairOrderIssued.objects.get(id=repair_id)

                    if data.get('cash_receivable') == True:
                        # if queryset.total_amount == queryset.paid_amount:
                        #     exit
                        
                        #check given amount is greater than credit balance
                        if  float(data.get('amount'))  > float(vendor_queryset.credit_balance_rupee) or float(data.get('amount'))  == float(vendor_queryset.credit_balance_rupee):
                            #Calculating amount to be paid from vendor account balance and amount
                            rupee = float(data.get('amount')) - float(vendor_queryset.credit_balance_rupee)                            
                            ven_data={'credit_balance_rupee':"0.00"}
                            
                        else:
                            #Calculating amount to be paid from vendor account balance and amount
                            rupee = float(vendor_queryset.credit_balance_rupee) - float(data.get('amount'))  
                            if  float(data.get('amount')) > 0: 
                                ven_data={'credit_balance_rupee':rupee}                   
                                
                            else:
                                ven_data={'credit_balance_rupee':"0.00"}
                        
                        ven_serializer = AccountHeadDetailsSerailizer(vendor_queryset,data=ven_data,partial=True)
                        if ven_serializer.is_valid():
                            ven_serializer.save()
                        else:
                            raise Exception(ven_serializer.errors)
                            
                        #Check given amount is greater or equal to total amount                    
                        if float(rupee) == float(repair_queryset.repair_details.total_vendor_charges) or  float(rupee) > float(repair_queryset.repair_details.total_vendor_charges):
                            #Calculate pending amount
                            pending_amount = float(repair_queryset.repair_details.total_vendor_charges) - float(repair_queryset.paid_amount) 
                            #Calculate amount to be paid 
                            remaining_amount = float(rupee) - pending_amount  
                        
                            data={}
                            data['paid_amount'] = repair_queryset.repair_details.total_vendor_charges
                            repair_serializer =RepairOrderIssuedSerializer(repair_queryset,data=data)
                            if repair_serializer.is_valid():
                                repair_serializer.save()
                            else:
                                #Initialize given amount
                                intial_amount = float(rupee)                        
                                #Calculate pending amount
                                pending_amount = float(repair_queryset.repair_details.total_vendor_charges) - float(repair_queryset.paid_amount)                         
                                #Check given amount greater than pending amount
                            
                                if float(rupee) >= pending_amount :
                                    remaining_amount = float(rupee) - pending_amount
                                                            
                                else:
                                    remaining_amount = 0
                                
                                #Calcuate already paid amount with initial amount
                                amount = repair_queryset.paid_amount+intial_amount

                                if float(amount) >= float(repair_queryset.repair_details.total_issued_weight):
                                    #Update amount as totalamount
                                    pay_amount = repair_queryset.repair_details.total_issued_weight
                                else:     
                                    #update calculate amount                       
                                    pay_amount = amount
                                            
                                data={}
                                data['paid_amount'] = pay_amount
                                repair_serializer =RepairOrderIssuedSerializer(repair_queryset,data=data)
                                if repair_serializer.is_valid():
                                    repair_serializer.save()
                            
                            if remaining_amount != 0:
                                #Update remaing amount with already balance rupee                         
                                vendor_remain_amount = float(vendor_queryset.credit_balance_rupee) + float(remaining_amount)                          
                                AccountHeadDetails.objects.filter(id=vendor_queryset.pk).update(credit_balance_rupee=vendor_remain_amount)       
                        
                    else:
                        #Check given amount is greater or equal to total amount                    
                        if float(remaining_amount) == float(repair_queryset.repair_details.total_vendor_charges) or  float(remaining_amount) > float(repair_queryset.repair_details.total_vendor_charges):
                            #Calculate pending amount
                            pending_amount = float(repair_queryset.repair_details.total_vendor_charges) - float(repair_queryset.paid_amount) 
                            #Calculate amount to be paid 
                            remaining_amount = float(remaining_amount) - pending_amount                    
                        
                            data={}
                            data['paid_amount'] = repair_queryset.repair_details.total_vendor_charges
                            repair_serializer =RepairOrderIssuedSerializer(repair_queryset,data=data)
                            if repair_serializer.is_valid():
                                repair_serializer.save()
                        else:
                            #Initialize given amount
                            intial_amount = float(remaining_amount)
                            #Calculate pending amount
                            pending_amount = float(repair_queryset.repair_details.total_vendor_charges) - float(repair_queryset.paid_amount)                         
                            #Checkgiven amount greater than pending amount
                            if float(remaining_amount) >= pending_amount :
                                remaining_amount = float(remaining_amount) - pending_amount
                            else:
                                remaining_amount = 0
                        
                            #Calcuate already paid amount with initial amount
                            amount = repair_queryset.paid_amount+intial_amount

                            if float(amount) >= float(repair_queryset.repair_details.total_vendor_charges):
                                #Update amount as totalamount
                                pay_amount = repair_queryset.repair_details.total_vendor_charges
                            else:     
                                #update calculate amount                       
                                pay_amount = amount
                                        
                            data={}
                            data['paid_amount'] = pay_amount
                            repair_serializer =RepairOrderIssuedSerializer(repair_queryset,data=data)
                            if repair_serializer.is_valid():
                                repair_serializer.save()

                        if remaining_amount != 0:
                            #Update remaing amount with already balance rupee                         
                            vendor_remain_amount = float(vendor_queryset.credit_balance_rupee) + float(remaining_amount)
                            AccountHeadDetails.objects.filter(id=vendor_queryset.pk).update(credit_balance_rupee=vendor_remain_amount)

                    if data.get('metal_receivable') == True:
                    
                        #Calculate balance gram
                        balance = float(repair_queryset.repair_details.total_issued_weight) - float(repair_queryset.paid_weight)
                        #Check if vendor gram is greater than balance
                        if float(vendor_queryset.credit_balance_gm) > float(balance) or float(vendor_queryset.credit_balance_gm) == float(balance):                    
                            amount = float(vendor_queryset.credit_balance_gm) - float(balance)   
                            ven_data={'credit_balance_gm':amount}

                        else:
                            amount =   float(balance) - float(vendor_queryset.credit_balance_gm)
                            ven_data={'credit_balance_gm':"0.00"}
                                
                        #Update the balance credit balance gram
                        ven_serializer = AccountHeadDetailsSerailizer(vendor_queryset,data=ven_data,partial=True)
                        if ven_serializer.is_valid():
                            ven_serializer.save()
                        else:
                            raise Exception(ven_serializer.errors)
                    
                        #Check Balance gram greater than total weight
                        if  float(vendor_queryset.credit_balance_gm) >= float(repair_queryset.repair_details.total_issued_weight) :                   
                            pay_weight = repair_queryset.repair_details.total_issued_weight
                        
                        else:
                            #Calculate  total weight with already paid weight
                            weight = float(repair_queryset.paid_weight) + balance
                            #Check weight greater than total weight
                            if weight >= float(repair_queryset.repair_details.total_issued_weight):
                                #update value with totalweight
                                pay_weight = repair_queryset.repair_details.total_issued_weight
                            else:
                                pay_weight = float(repair_queryset.paid_weight) + balance
                        
                        data = {}
                        data['paid_weight']= pay_weight                
                        repair_serializer =RepairOrderIssuedSerializer(repair_queryset,data=data)
                        if repair_serializer.is_valid():
                            repair_serializer.save()

                    #Final remaining amount update
                    if remaining_amount != 0:
                        #Update remaing amount with alreday balance rupee                         
                        vendor_remain_amount = float(vendor_queryset.credit_balance_rupee) + float(remaining_amount)
                        AccountHeadDetails.objects.filter(id=vendor_queryset.pk).update(credit_balance_rupee=vendor_remain_amount)

            elif data.get('type') == settings.ORDER_VENDOR_PAYMENT:
                for order_id in purchase_order_ids:
                
                    order_issue_queryset = OrderIssue.objects.get(id=order_id)

                    order_queryset = OrderDetails.objects.get(id=order_issue_queryset.order_id.pk)

                    if data.get('cash_receivable') == True:
                        # if queryset.total_amount == queryset.paid_amount:
                        #     exit
                        
                        #check given amount is greater than credit balance
                        if  float(data.get('amount'))  > float(vendor_queryset.credit_balance_rupee) or float(data.get('amount'))  == float(vendor_queryset.credit_balance_rupee):
                            #Calculating amount to be paid from vendor account balance and amount
                            rupee = float(data.get('amount')) - float(vendor_queryset.credit_balance_rupee)                            
                            ven_data={'credit_balance_rupee':"0.00"}
                            
                        else:
                            #Calculating amount to be paid from vendor account balance and amount
                            rupee = float(vendor_queryset.credit_balance_rupee) - float(data.get('amount'))  
                            if  float(data.get('amount')) > 0: 
                                ven_data={'credit_balance_rupee':rupee}                   
                                
                            else:
                                ven_data={'credit_balance_rupee':"0.00"}
                        
                        ven_serializer = AccountHeadDetailsSerailizer(vendor_queryset,data=ven_data,partial=True)
                        if ven_serializer.is_valid():
                            ven_serializer.save()
                        else:
                            raise Exception(ven_serializer.errors)
                            
                        #Check given amount is greater or equal to total amount                    
                        if float(rupee) == float(order_queryset.approximate_amount) or  float(rupee) > float(order_queryset.approximate_amount):
                            #Calculate pending amount
                            pending_amount = float(order_queryset.approximate_amount) - float(order_issue_queryset.paid_amount) 
                            #Calculate amount to be paid 
                            remaining_amount = float(rupee) - pending_amount  
                        
                            data={}
                            data['paid_amount'] = order_queryset.approximate_amount
                            order_serializer =OrderIssueSerializer(order_issue_queryset,data=data)
                            if order_serializer.is_valid():
                                order_serializer.save()
                            else:
                                #Initialize given amount
                                intial_amount = float(rupee)                        
                                #Calculate pending amount
                                pending_amount = float(order_queryset.approximate_amount) - float(order_issue_queryset.paid_amount)                         
                                #Check given amount greater than pending amount
                            
                                if float(rupee) >= pending_amount :
                                    remaining_amount = float(rupee) - pending_amount
                                                            
                                else:
                                    remaining_amount = 0
                                
                                #Calcuate already paid amount with initial amount
                                amount = order_issue_queryset.paid_amount+intial_amount

                                if float(amount) >= float(order_queryset.total_weight):
                                    #Update amount as totalamount
                                    pay_amount = order_queryset.total_weight
                                else:     
                                    #update calculate amount                       
                                    pay_amount = amount
                                            
                                data={}
                                data['paid_amount'] = pay_amount
                                order_serializer =OrderIssueSerializer(order_issue_queryset,data=data)
                                if order_serializer.is_valid():
                                    order_serializer.save()
                            
                            if remaining_amount != 0:
                                #Update remaing amount with already balance rupee                         
                                vendor_remain_amount = float(vendor_queryset.credit_balance_rupee) + float(remaining_amount)                          
                                AccountHeadDetails.objects.filter(id=vendor_queryset.pk).update(credit_balance_rupee=vendor_remain_amount)       
                        
                    else:
                        #Check given amount is greater or equal to total amount                    
                        if float(remaining_amount) == float(order_queryset.approximate_amount) or  float(remaining_amount) > float(order_queryset.approximate_amount):
                            #Calculate pending amount
                            pending_amount = float(order_queryset.approximate_amount) - float(order_issue_queryset.paid_amount) 
                            #Calculate amount to be paid 
                            remaining_amount = float(remaining_amount) - pending_amount                    
                        
                            data={}
                            data['paid_amount'] = order_queryset.approximate_amount
                            repair_serializer =RepairOrderIssuedSerializer(repair_queryset,data=data)
                            if repair_serializer.is_valid():
                                repair_serializer.save()
                        else:
                            #Initialize given amount
                            intial_amount = float(remaining_amount)
                            #Calculate pending amount
                            pending_amount = float(order_queryset.approximate_amount) - float(order_issue_queryset.paid_amount)                         
                            #Checkgiven amount greater than pending amount
                            if float(remaining_amount) >= pending_amount :
                                remaining_amount = float(remaining_amount) - pending_amount
                            else:
                                remaining_amount = 0
                        
                            #Calcuate already paid amount with initial amount
                            amount = order_issue_queryset.paid_amount+intial_amount

                            if float(amount) >= float(order_queryset.approximate_amount):
                                #Update amount as totalamount
                                pay_amount = order_queryset.approximate_amount
                            else:     
                                #update calculate amount                       
                                pay_amount = amount
                                        
                            data={}
                            data['paid_amount'] = pay_amount
                            order_serializer =OrderIssueSerializer(order_issue_queryset,data=data)
                            if order_serializer.is_valid():
                                order_serializer.save()

                        if remaining_amount != 0:
                            #Update remaing amount with already balance rupee                         
                            vendor_remain_amount = float(vendor_queryset.credit_balance_rupee) + float(remaining_amount)
                            AccountHeadDetails.objects.filter(id=vendor_queryset.pk).update(credit_balance_rupee=vendor_remain_amount)

                    if data.get('metal_receivable') == True:
                    
                        #Calculate balance gram
                        balance = float(repair_queryset.repair_details.total_issued_weight) - float(repair_queryset.paid_weight)
                        #Check if vendor gram is greater than balance
                        if float(vendor_queryset.credit_balance_gm) > float(balance) or float(vendor_queryset.credit_balance_gm) == float(balance):                    
                            amount = float(vendor_queryset.credit_balance_gm) - float(balance)   
                            ven_data={'credit_balance_gm':amount}

                        else:
                            amount =   float(balance) - float(vendor_queryset.credit_balance_gm)
                            ven_data={'credit_balance_gm':"0.00"}
                                
                        #Update the balance credit balance gram
                        ven_serializer = AccountHeadDetailsSerailizer(vendor_queryset,data=ven_data,partial=True)
                        if ven_serializer.is_valid():
                            ven_serializer.save()
                        else:
                            raise Exception(ven_serializer.errors)
                    
                        #Check Balance gram greater than total weight
                        if  float(vendor_queryset.credit_balance_gm) >= float(order_queryset.total_weight) :                   
                            pay_weight = order_queryset.total_weight
                        
                        else:
                            #Calculate  total weight with already paid weight
                            weight = float(order_issue_queryset.paid_weight) + balance
                            #Check weight greater than total weight
                            if weight >= float(order_queryset.total_weight):
                                #update value with totalweight
                                pay_weight = order_queryset.total_weight
                            else:
                                pay_weight = float(order_issue_queryset.paid_weight) + balance
                        
                        data = {}
                        data['paid_weight']= pay_weight                
                        order_serializer =OrderIssueSerializer(order_issue_queryset,data=data)
                        if order_serializer.is_valid():
                            order_serializer.save()

                    #Final remaining amount update
                    if remaining_amount != 0:
                        #Update remaing amount with alreday balance rupee                         
                        vendor_remain_amount = float(vendor_queryset.credit_balance_rupee) + float(remaining_amount)
                        AccountHeadDetails.objects.filter(id=vendor_queryset.pk).update(credit_balance_rupee=vendor_remain_amount)
            

            return Response({        
                "message": res_msg.create('Amount rate cut '),
                "status": status.HTTP_201_CREATED
            }, status=status.HTTP_200_OK)
        
        else:
            return Response({
                "data": serializer.errors,
                "message": res_msg.in_valid_fields(),
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_200_OK)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class NewPurchaseTransactionIDView(APIView):
 
    def get(self,request):
        try:
            # queryset=NewPurchaseTransactionDetail.objects.all().order_by('-id')[0]
            # new_id=int(queryset.pk)+1
            random_id =random.randrange(0,100)
            prefix = 'VDP-00'  # Prefix for the vendor payment bill number
            id = f'{prefix}{random_id}'
          
            return Response(
                {
                    "vendor_id":id,                    
                    "message":res_msg.retrieve("Vendor payment"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        except Exception as err:
            return Response(
                {
                    "vendor_id":"VDP-001",
                    "id":1,
                    "message":res_msg.retrieve("Vendor payment"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )

        
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# class VendorpaymentView(APIView):
#     def post(self, request):        
#         data = request.data
#         data['payment_bill_no'] = data.get('payment_bill_no')
#         data['designer_name'] = data.get('designer_name')
#         data['date'] = data.get('date')
#         data['created_at'] = timezone.now()
#         data['created_by'] = request.user.id
#         serializer = NewPurchaseBillDetailSerializer(data=data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response({        
#                 "message": res_msg.create('Vendor payment'),
#                 "status": status.HTTP_201_CREATED
#             }, status=status.HTTP_200_OK)
        
#         else:
#             return Response({
#                 "data": serializer.errors,
#                 "message": res_msg.in_valid_fields(),
#                 "status": status.HTTP_400_BAD_REQUEST
#             }, status=status.HTTP_200_OK)

        
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# class VendorPaymentListView(APIView):
   
#     def post(self, request):
             
#         page = request.data.get('page') if request.data.get('page') else 1
#         items_per_page = request.data.get('items_per_page') if request.data.get('items_per_page') else 10       

#         queryset = AccountHeadDetails.objects.all().order_by('-id')

#         paginated_data = Paginator(queryset, items_per_page)
#         serializer = AccountHeadDetailsSerailizer(paginated_data.get_page(page),many=True)
#         res_data = []
#         for i in serializer.data:
        
#             total_pure_weight = 0
#             total_amount = 0
#             paid_amount = 0
#             paid_weight = 0

#             newpurchase_queryset = NewPurchase.objects.filter(designer_name=i['id'])

#             for newpurchase in newpurchase_queryset:
#                 total_pure_weight += newpurchase.total_pure_weight
#                 total_amount += newpurchase.total_amount
#                 paid_amount += newpurchase.paid_amount
#                 paid_weight += newpurchase.paid_weight
#             pending_amount = (total_amount) - (paid_amount)
#             pending_weight = (total_pure_weight) - (paid_weight)
           
#             if total_pure_weight == paid_weight and total_amount == paid_amount:
#                 pay_status = 'Received'
#                 color = '#FFBFBF'
#                 payment_history ={
#                 'id': i['id'],
#                 'designer_name': i['account_head_name'],
#                 'total_pure_weight': total_pure_weight,
#                 'total_amount': total_amount,
#                 'paid_amount': paid_amount,
#                 'paid_weight': paid_weight,
#                 'pending_amount': pending_amount,
#                 'pending_weight': pending_weight,                     
#                 'credit_balance_rupee': i['credit_balance_rupee'],
#                 'credit_balance_gm': i['credit_balance_gm'],
#             }

#             else:
#                 pay_status = 'Pending'
#                 color='#7BFFA4'
#                 payment_history =[]

#             res_data.append({
#                 'id':i['id'],
#                 'designer_name': i['account_head_name'],
#                 'total_pure_weight': total_pure_weight,
#                 'total_amount': total_amount,
#                 'paid_amount': paid_amount,
#                 'paid_weight': paid_weight,
#                 'pending_amount':pending_amount,
#                 'pending_weight':pending_weight,
#                 'status':pay_status,
#                 'color':color,
#                 'payment_history':payment_history,
#                 'credit_balance_rupee':i['credit_balance_rupee'],
#                 'credit_balance_gm':i['credit_balance_gm'],
#             })


#         return Response({
#             "data": {
#                 "list": res_data,
#                 "total_pages": paginated_data.num_pages,
#                 "current_page": page,
#                 "total_items": len(queryset),
#                 "current_items": len(res_data)
#             },
#             "message": res_msg.retrieve('New Purchase List'),
#             "status": status.HTTP_200_OK
#         }, status=status.HTTP_200_OK)


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class VendorPaymentListView(APIView):
   
    def post(self, request):
             
        page = request.data.get('page') if request.data.get('page') else 1
        items_per_page = request.data.get('items_per_page') if request.data.get('items_per_page') else 10       
        response_data = []
        dict_data = {}
        queryset = AccountHeadDetails.objects.all().order_by('-id')

        paginated_data = Paginator(queryset, items_per_page)
        serializer = AccountHeadDetailsSerailizer(paginated_data.get_page(page),many=True)
        for account_detail in serializer.data:
            dict_data = {}
            dict_data['id'] = account_detail['id']
            dict_data['designer_name'] = account_detail['account_head_name']

            # Aggregate purchase data
            purchase_aggregates = NewPurchase.objects.filter(designer_name=account_detail['id']).aggregate(
                total_weight=Sum('total_pure_weight'),
                total_amount=Sum('total_amount'),
                paid_amount=Sum('paid_amount'),
                paid_weight=Sum('paid_weight')
            )

            total_weight = purchase_aggregates['total_weight'] or 0
            total_amount = purchase_aggregates['total_amount'] or 0
            paid_amount = purchase_aggregates['paid_amount'] or 0
            paid_weight = purchase_aggregates['paid_weight'] or 0

            dict_data['total_pure_weight'] = total_weight
            dict_data['total_amount'] = total_amount
            dict_data['paid_amount'] = paid_amount
            dict_data['paid_weight'] = paid_weight
            dict_data['pending_amount'] = total_amount - paid_amount
            dict_data['pending_weight'] = total_weight - paid_weight
            dict_data['type'] = 1

            if total_weight == paid_weight and total_amount == paid_amount:
                dict_data['pay_status'] = "Paid"
                dict_data['color'] = '#FFBFBF'
            elif (paid_weight > 0 and paid_weight < total_weight) and (paid_amount > 0 and paid_amount < total_amount):
                dict_data['pay_status'] = "Partially Paid"
                dict_data['color'] = '#FFBFBF'
            else:
                dict_data['pay_status'] = "Pending"
                dict_data['color'] = '#7BFFA4'

            account_detail_instance = AccountHeadDetails.objects.get(pk=account_detail['id'])
            dict_data['credit_balance_rupee'] = account_detail_instance.credit_balance_rupee
            dict_data['credit_balance_gm'] = account_detail_instance.credit_balance_gm

            response_data.append(dict_data)

            # # Aggregate repair issue data
            repair_aggregates = RepairOrderIssued.objects.filter(vendor_name=account_detail['id']).aggregate(
                total_weight=Sum('repair_details__total_issued_weight'),
                total_amount=Sum('repair_details__total_vendor_charges'),
                paid_amount=Sum('paid_amount'),
                paid_weight=Sum('paid_weight')
            )

            total_weight = repair_aggregates['total_weight'] or 0
            total_amount = repair_aggregates['total_amount'] or 0
            paid_amount = repair_aggregates['paid_amount'] or 0
            paid_weight = repair_aggregates['paid_weight'] or 0
            
            repair_data = {
                'total_pure_weight': total_weight,
                'total_amount': total_amount,
                'paid_amount': paid_amount,
                'paid_weight': paid_weight,
                'pending_amount': total_amount - paid_amount,
                'pending_weight': total_weight - paid_weight
            }
            repair_data['id'] = account_detail['id']
            repair_data['designer_name'] = account_detail['account_head_name']
            
            # if total_weight == paid_weight and total_amount == paid_amount:
            #     repair_data['pay_status'] = 'Received'
            #     repair_data['color'] = '#FFBFBF'
            # else:
            #     repair_data['pay_status'] = 'Pending'
            #     repair_data['color'] = '#7BFFA4'

            if total_weight == paid_weight and total_amount == paid_amount:
                dict_data['pay_status'] = "Paid"
                dict_data['color'] = '#FFBFBF'
            elif (paid_weight > 0 and paid_weight < total_weight) and (paid_amount > 0 and paid_amount < total_amount):
                dict_data['pay_status'] = "Partially Paid"
                dict_data['color'] = '#FFBFBF'
            else:
                dict_data['pay_status'] = "Pending"
                dict_data['color'] = '#7BFFA4'

            repair_data['type'] = 2
            repair_data['credit_balance_rupee'] = account_detail_instance.credit_balance_rupee
            repair_data['credit_balance_gm'] = account_detail_instance.credit_balance_gm
            
            response_data.append(repair_data)
            
            orderissue_queryset = OrderIssue.objects.filter(vendor=account_detail['id'])
            total_pure_weight = 0
            total_amount = 0
            paid_amount = 0
            paid_weight = 0
            for order_issue in orderissue_queryset:
                
                try:
                    order_details = OrderDetails.objects.get(id=order_issue.order_id.pk)
                    total_pure_weight += order_details.total_weight
                    total_amount += order_details.approximate_amount
                    paid_amount += order_issue.paid_amount
                    paid_weight += order_issue.paid_weight
                except OrderDetails.DoesNotExist:
                    pass
            
            order_data = {
                'total_pure_weight': total_weight,
                'total_amount': total_amount,
                'paid_amount': paid_amount,
                'paid_weight': paid_weight,
                'pending_amount': total_amount - paid_amount,
                'pending_weight': total_weight - paid_weight
            }
            
            order_data['id'] = account_detail['id']
            order_data['designer_name'] = account_detail['account_head_name']
            # if total_pure_weight == paid_weight and total_amount == paid_amount:
            #     order_data['pay_status'] = 'Received'
            #     order_data['color'] = '#FFBFBF'
            # else:
            #     order_data['pay_status'] = 'Pending'
            #     order_data['color']='#7BFFA4'

            if total_pure_weight == paid_weight and total_amount == paid_amount:
                dict_data['pay_status'] = "Paid"
                dict_data['color'] = '#FFBFBF'
            elif (paid_weight > 0 and paid_weight < total_pure_weight) and (paid_amount > 0 and paid_amount < total_amount):
                dict_data['pay_status'] = "Partially Paid"
                dict_data['color'] = '#FFBFBF'
            else:
                dict_data['pay_status'] = "Pending"
                dict_data['color'] = '#7BFFA4'

            order_data['type'] = 3
            order_data['credit_balance_rupee'] = account_detail_instance.credit_balance_rupee
            order_data['credit_balance_gm'] = account_detail_instance.credit_balance_gm
            response_data.append(order_data)
            
        return Response({
            "data": {
                "list": response_data,
                "total_pages": paginated_data.num_pages,
                "current_page": page,
                "total_items": len(queryset),
                "current_items": len(response_data)
            },
            "message": res_msg.retrieve('New Purchase List'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)



@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ItemListView(APIView):
    def get(self, request):
        queryset = Item.objects.filter(is_active=True).values(
            'huid_rate', 'id', 'item_id', 'item_name', 'purity__id','hsn_code', 'stock_type', 'stock_type__stock_type_name', 'metal__metal_name', 'purity__purity_name'
        )

        # # Fetch association rates from the database
        # association_rates = MetalRate.objects.all().values_list('association_rate', 'rate')
      

        # # Flatten the association rates to a single dictionary
        # association_rate_dict = {}
        # for rates in association_rates:
        #     for rate_key, rate_value in rates[0].items():
        #         association_rate_dict[rate_key] = rate_value


        for item in queryset:

            try:
                rate_queryset = MetalRate.objects.filter(purity = item['purity__id']).order_by('-id')[0]  
                item['rate'] = rate_queryset.rate

            except Exception as err:
                item['rate'] = 0
            # metal = item['metal__metal_name']
            # purity = item['purity__purity_name']
            # rate_key = f'{metal}_{purity}'

            # # Get the rate value from association_rate_dict based on the rate key
            # rate_value = association_rate_dict.get(rate_key, None)

            # # Assign the rate value to the item dictionary
            # item['rate'] = rate_value

        return Response(
            {
                "data": queryset,
                "message": res_msg.retrieve("Item Details"),
                "status": status.HTTP_200_OK
            },
            status=status.HTTP_200_OK
        )

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class StoneDeleteView(APIView):
    def delete(self, request, pk):
        try:
            queryset  = NewPurchaseStoneDetails.objects.get(id=pk)
            queryset.delete()
            return Response({
                "message": res_msg.delete('New Purchase Stone detail'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        except NewPurchaseStoneDetails.DoesNotExist:
            return Response({
                "message": res_msg.not_exists('New Purchase Stone detail'),
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
class DiamondDeleteView(APIView):
    def delete(self, request, pk):
        try:
            queryset  = NewPurchaseDiamondDetails.objects.get(id=pk)
            queryset.delete()
            return Response({
                "message": res_msg.delete('New Purchase Diamond detail'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        except NewPurchaseDiamondDetails.DoesNotExist:
            return Response({
                "message": res_msg.not_exists('New Purchase Diamond detail'),
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
class ItemDeleteView(APIView):
    def delete(self, request, pk):
        try:
            queryset  = NewPurchaseItemdetail.objects.get(id=pk)

            stone_item_queryset  = NewPurchaseStoneDetails.objects.filter(purchase_order=pk)
            diamond_item_queryset  = NewPurchaseDiamondDetails.objects.filter(purchase_order=pk) 

            if diamond_item_queryset:
                diamond_item_queryset.delete()
    
            if stone_item_queryset:
                stone_item_queryset.delete()

            queryset.delete()
            return Response({
                "message": res_msg.delete('New Purchase Item detail'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        except NewPurchaseItemdetail.DoesNotExist:
            return Response({
                "message": res_msg.not_exists('New Purchase Item detail'),
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
class NewPurchaseEntryListView(APIView):
   
    def post(self, request):

        search = request.data.get('search') if request.data.get('search')  else ''
        from_date = request.data.get('from_date') if request.data.get('from_date') else None
        to_date = request.data.get('to_date') if request.data.get('to_date')  else None        
        page = request.data.get('page') if request.data.get('page') else 1
        items_per_page = request.data.get('items_per_page') if request.data.get('items_per_page') else 10
        branch = request.data.get('branch') if request.data.get('branch')  else None
        
        filter_condition={}       
        if from_date != None and to_date != None:
            date_range=(from_date,to_date)
            filter_condition['order_date__range'] = date_range
        
        if request.user.role.is_admin == True :
            if request.data.get('branch') != None:
                filter_condition['branch'] = request.data.get('branch')
        else:                
            filter_condition['branch'] = request.user.branch.pk

        if len(filter_condition) != 0 : 
            queryset = list(NewPurchase.objects.filter(Q(purchase_order_id__icontains=search),**filter_condition).order_by('id'))
        elif search != '':
            queryset = list(NewPurchase.objects.filter(Q(purchase_order_id__icontains=search)).order_by('id'))
        else :
            queryset = list(NewPurchase.objects.all().order_by('id'))

        paginated_data = Paginator(queryset, items_per_page)
        serializer = NewPurchaseSerializer(paginated_data.get_page(page),many=True)

        res_data = []
        for i in range(0, len(serializer.data)):
            custom = serializer.data[i] 
            balance_amount =(queryset[i].total_amount) - (queryset[i].paid_amount)
            custom['advance_amount'] = '0.00'
            custom['balance_amount'] = balance_amount
            custom['purchase_typename'] = 'New Purchase'
            custom['branch_name'] = queryset[i].branch.branch_name
            custom['person_name'] = queryset[i].designer_name.account_head_name
            custom['item'] = queryset[i].total_pieces
            custom['po_id'] = queryset[i].purchase_order_id
            custom['purchase_person_name'] ="Vendor"
            custom['purchase_date'] =queryset[i].due_date
            res_data.append(custom)
    
        return Response({
            "data": {
                "list": res_data,
                "total_pages": paginated_data.num_pages,
                "current_page": page,
                "total_items": len(queryset),
                "current_items": len(res_data)
            },
            "message": res_msg.retrieve('New Purchase List'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
