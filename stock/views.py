from django.shortcuts import render

from tagging.serializer import TaggedItemsSerializer
from .models import *
from rest_framework.views import APIView
from rest_framework import status,viewsets
from django.utils import timezone
from app_lib.response_messages import ResponseMessages
from .serializer import *
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.db.models import ProtectedError
from masters.models import StoneDetails
from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework import filters
from django.core.paginator import Paginator
from books.models import *
import random
from django.conf import settings
from masters.models import MetalRate
from billing.models import *
from dateutil.relativedelta import relativedelta
from product.models import *
from value_addition.models import *
from organizations.models import *
from accounts.models import *
from customer.serializer import *
from tagging.serializer import *
from tagging.models import *
from django.db import transaction

res_msg = ResponseMessages()

# Transfer Item        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class TransferItemViewset(viewsets.ViewSet):
    def create(self,request):
        resdata=request.data
        request_data = {}
        request_data['transfer_date'] = resdata.get('transfer_date')
        request_data['required_date'] = resdata.get('required_date')
        request_data['transfer_to'] = resdata.get('transfer_to')
        request_data['stock_authority'] = resdata.get('stock_authority')
        request_data['transfer_status'] = 1
        request_data['created_at']=timezone.now()
        request_data['created_by']=request.user.id
        if request.user.role.is_admin == False:
          transfer_from = request.user.branch.pk
        else:
           transfer_from= resdata.get('transfer_from')
        request_data['transfer_from'] = transfer_from   
        item_serializer=TransferItemSerializer(data=request_data)    
        if item_serializer.is_valid():
            item_serializer.save()
            tag_item_details=resdata.get('tag_item_details') if resdata.get('tag_item_details') else {}
            
            itemdetails ={}
            for itemrow in tag_item_details:
                
                itemdetails['transfer_itemid']=str(item_serializer.data['id'])
      
                tagitems=TaggedItems.objects.get(tag_number=itemrow['tag_number'])
                TaggedItems.objects.filter(id=tagitems.id).update(transfer=1)
                
                itemdetails['tagitems_id']=tagitems.id
                itemdetails['tag_number']=itemrow['tag_number']
                itemdetails['created_at']=timezone.now()
                itemdetails['created_by']=request.user.id
                itemdetails_serializer=TransferItemDetailsSerializer(data=itemdetails)
                itemtags = {}
                if itemdetails_serializer.is_valid():
                    itemdetails_serializer.save()
                    itemtags['transfer'] = 1
                    
                  
                else:
                    raise Exception(itemdetails_serializer.errors)
            return Response(
                {
                    "data":item_serializer.data,
                    "message":res_msg.create("Transfer Item"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )                    
        else:
            return Response(
                {
                    "data":item_serializer.errors,
                    "message":res_msg.something_else(),
                    "status":status.HTTP_204_NO_CONTENT
                },status=status.HTTP_200_OK
                )
        
    def update(self,request,pk):
   
        try:
            item_querset=TransferItem.objects.get(id=pk)
            resdata=request.data
        
            request_data = {}
            request_data['transfer_date'] = resdata.get('transfer_date')
            request_data['required_date'] = resdata.get('required_date')
            request_data['transfer_to'] = resdata.get('transfer_to')
            request_data['stock_authority'] = resdata.get('stock_authority')
            if request.user.role.is_admin == False:
                transfer_from = request.user.branch.pk
            else:
                transfer_from= resdata.get('transfer_from')
            request_data['transfer_from'] = transfer_from   
            request_data['modified_at']=timezone.now()
            request_data['modified_by']=request.user.id
            
            item_serializer=TransferItemSerializer(item_querset,data=request_data,partial=True)
            
            if item_serializer.is_valid():
                item_serializer.save()
             
                itemdetails ={}
                tag_item_details=resdata.get('tag_item_details') if resdata.get('tag_item_details') else {}

                
                transfer_queryset=list(TransferItemDetails.objects.filter(transfer_itemid=pk))
                for itrow in transfer_queryset:   
                    TaggedItems.objects.filter(id=itrow.tagitems_id.pk).update(transfer=0)
                    itrow.delete()

                for itemrow in tag_item_details:
                
                    itemdetails['transfer_itemid']=str(item_serializer.data['id'])
                    tagitems=TaggedItems.objects.get(tag_number=itemrow['tag_number'])
                    TaggedItems.objects.filter(id=tagitems.id).update(transfer=1)
                    itemdetails['tagitems_id']=tagitems.id
                    itemdetails['tag_number']=itemrow['tag_number']
                    itemdetails['created_at']=timezone.now()
                    itemdetails['created_by']=request.user.id
                    itemdetails_serializer=TransferItemDetailsSerializer(data=itemdetails)
               
                    if itemdetails_serializer.is_valid():
                        itemdetails_serializer.save()
                       
                    
                    else:
                        raise Exception(itemdetails_serializer.errors)


                return Response(
                    {
                        "data":item_serializer.data ,
                        "message":res_msg.update("Tansfer Item Details"),
                        "status":status.HTTP_200_OK
                    },status=status.HTTP_200_OK
                )

            else:

                return Response(
                    {
                        "data":item_serializer.errors,
                        "message":res_msg.not_update("Transfer Item Detials"),
                        "status":status.HTTP_400_BAD_REQUEST
                    },status=status.HTTP_200_OK
                )
        except TransferItem.DoesNotExist:

            return Response(
                {
                    "message":res_msg.not_exists("Tansfer item"),
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

    def destroy(self,request,pk):
        try:
            transfer = TransferItem.objects.get(id=pk)
            if transfer.transfer_status == 1 or transfer.transfer_status == 3:
                TransferItemDetails.objects.get(transfer_itemid=pk).delete()
                TransferItem.objects.get(id=pk).delete()
                return Response({
                    "message": res_msg.delete('Transfer Item'),
                    "status": status.HTTP_200_OK
                }, status=status.HTTP_200_OK)
            else:
                received = ReceivedItem.objects.get(transfer_itemid=pk)
               
                if received.transfer_status_id == 4:
                    ReceivedItemDetails.objects.get(transfer_itemid=pk).delete()
                    ReceivedItem.objects.get(transfer_itemid=pk).delete()
                    TransferItemDetails.objects.get(transfer_itemid=pk).delete()
                    TransferItem.objects.get(id=pk).delete()
                    return Response({
                        "message": res_msg.delete('Transfer Item'),
                        "status": status.HTTP_200_OK
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        "message":"Cannot delete transfer because item has received",
                        "status": status.HTTP_404_NOT_FOUND
                    }, status=status.HTTP_200_OK)
        except TransferItem.DoesNotExist:
            return Response(
                {
                    "message":res_msg.not_exists("Tansfer item"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        except Exception as err:
            return Response(    
                {
                    "data":str(err),
                    "message":res_msg.something_else(),
                    "status":status.HTTP_204_NO_CONTENT
                },status=status.HTTP_200_OK)


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class TransferItemListView(APIView):
    def get(self,request,pk):
 
        try:
 
            queryset=TransferItem.objects.filter(id=pk).values('id','transfer_date','required_date','stock_authority','stock_authority__first_name','transfer_from','transfer_from__branch_name','transfer_to','transfer_to__branch_name','transfer_status','transfer_status__status_name')
           
            transfer_itemqueryset = TransferItemDetails.objects.filter(transfer_itemid=pk)
            res_data = []          
 
            for item in transfer_itemqueryset:
                tag_item = TaggedItems.objects.filter(tag_number=item.tag_number).values('id','tag_number','sub_item_details__sub_item_name','net_weight','gross_weight','item_details__item_details__item_name')
                
                if len(tag_item) > 0:
                    res_data.append(tag_item[0])
 
            transfer_item = {}
            if len(queryset) > 0:
                transfer_item = queryset[0]

            data={
               "transfer_item": transfer_item,
               "tagged_item":res_data,
 
            }
            return Response(
                {
                    "data":data,
                    "message":res_msg.retrieve("Transfer Item"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
       
        except TransferItem.DoesNotExist:
            return Response(
                {
                    "message":res_msg.not_exists("Transfer Item"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
       
 
    def post(self, request):
        search = request.data.get('search') if request.data.get('search')  else ''
        from_date = request.data.get('from_date') if request.data.get('from_date') != None else None
        to_date = request.data.get('to_date') if request.data.get('to_date') != None else None
        transfer_status = request.data.get('transfer_status') if request.data.get('transfer_status') != None else None 
        tag_status = request.data.get('tag_status') if request.data.get('tag_status') != None else None 
        page = request.data.get('page') if request.data.get('page') else 1
        branch = request.data.get('branch') if request.data.get('branch') else None
        # items_per_page = request.data.get('items_per_page') if request.data.get('items_per_page') else 10
        try:
            items_per_page = int(request.data.get('items_per_page', TransferItem.objects.all().count()))
            if items_per_page == 0:
                items_per_page = 10 
        except Exception as err:
            items_per_page = 10 

        filter_condition={}
        
        if request.user.role.is_admin ==True:
            if branch != None:            
               filter_condition['transfer_from'] = branch
        else:
            filter_condition['transfer_from'] = request.user.branch_id
   
        
       
        if from_date != None and to_date != None :
            date_range=(from_date,to_date)
            filter_condition['transfer_date__range'] = date_range
        
        if int(transfer_status) ==2:           
           filter_condition['transfer_status__in'] = [1]  

        else:
           if tag_status != None:
             filter_condition['transfer_status'] = tag_status 
      

        if len(filter_condition) != 0:
           queryset = list(TransferItem.objects.filter(Q(stock_authority__first_name__icontains=search),**filter_condition).order_by('id'))
        elif search != '':
           queryset = list(TransferItem.objects.filter(Q(stock_authority__first_name__icontains=search)).order_by('id'))
        else:
           queryset=list(TransferItem.objects.all().order_by('id'))

        paginated_data = Paginator(queryset, items_per_page)
        serializer = TransferItemSerializer(paginated_data.get_page(page),many=True)
 
        res_data = []
        
        for i in range(0, len(serializer.data)):
            
            custom = serializer.data[i]  
            custom['status'] = queryset[i].transfer_status.status_name
            custom['color'] = queryset[i].transfer_status.status_color
            custom['bgcolor'] = queryset[i].transfer_status.status_bgcolor
            custom['transfer_from'] = queryset[i].transfer_from.branch_name           
            custom['transfer_to'] = queryset[i].transfer_to.branch_name
            custom['authority_name'] = queryset[i].stock_authority.first_name
            custom['transfer_date'] = queryset[i].transfer_date
            total=TransferItemDetails.objects.filter(transfer_itemid=queryset[i].pk)
            count=total.count()
            custom['no_of_item'] = count
            reveive=ReturnItemDetails.objects.filter(transfer_itemid=queryset[i].pk)
            reveivecount=reveive.count()
            custom['no_of_receive'] = reveivecount            
            returnitem=ReturnItemDetails.objects.filter(transfer_itemid=queryset[i].pk) 
            returnitemcount=returnitem.count()
            custom['no_of_return'] = returnitemcount 
            res_data.append(custom)
       
        return Response({
            "data": {
                "list": res_data,
                "total_pages": paginated_data.num_pages,
                "current_page": page,
                "total_items": len(queryset),
                "current_items": len(res_data)
            },
            "message": res_msg.retrieve('Transfer Item'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)

#Received Item
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ReceiveitemViewset(viewsets.ViewSet):    
   def create(self,request):
        resdata=request.data
        request_data = {}
        request_data['received_date'] = resdata.get('received_date')
        request_data['transfer_itemid'] = resdata.get('transfer_itemid')
        request_data['created_at']=timezone.now()
        request_data['created_by']=request.user.id
        request_data['transfer_status']=5
        item_serializer=ReceivedItemSerializer(data=request_data)    
        if item_serializer.is_valid():
            item_serializer.save()
            tag_item_details=resdata.get('tag_item_details') if resdata.get('tag_item_details') else {}
           
            itemdetails ={}
            for itemrow in tag_item_details:
               
                itemdetails['received_itemid'] = str(item_serializer.data['id'])
                itemdetails['transfer_itemid'] =resdata.get('transfer_itemid')
                tagitems=TaggedItems.objects.get(tag_number=itemrow['tag_number'])
                TaggedItems.objects.filter(id=tagitems.id).update(branch=item_serializer.data['transfer_to'],transfer=0)
               
                itemdetails['tagitems_id']=tagitems.id
                itemdetails['tag_number']=itemrow['tag_number']
                itemdetails['created_at']=timezone.now()
                itemdetails['created_by']=request.user.id
                itemdetails_serializer=ReceivedItemDetailsSerializer(data=itemdetails)
                itemtags = {}
                if itemdetails_serializer.is_valid():
                    itemdetails_serializer.save()
                    itemtags['transfer'] = 1
                   
                 
                else:
                    raise Exception(itemdetails_serializer.errors)
            return Response(
                {
                    "data":item_serializer.data,
                    "message":res_msg.create("Received Item"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )                    
        else:
            return Response(
                {
                    "data":item_serializer.errors,
                    "message":res_msg.something_else(),
                    "status":status.HTTP_204_NO_CONTENT
                },status=status.HTTP_200_OK
                )
       
       
       
   def update(self,request,pk):
   
        try:
            item_querset=ReceivedItem.objects.get(id=pk)
            resdata=request.data
       
            request_data = {}
            request_data['received_date'] = resdata.get('received_date')
            request_data['created_at']=timezone.now()
            request_data['created_by']=request.user.id
            request_data['modified_at']=timezone.now()
            request_data['modified_by']=request.user.id
            request_data['transfer_status']=5
            item_serializer=ReceivedItemSerializer(item_querset,data=request_data,partial=True)
           
            if item_serializer.is_valid():
                item_serializer.save()
                recedata = item_serializer.data
                itemdetails ={}
                tag_item_details=resdata.get('tag_item_details') if resdata.get('tag_item_details') else {}
                ReceivedItemDetails.objects.filter(received_itemid=pk).delete()
                for itemrow in tag_item_details:
                  
                    itemdetails['received_itemid'] = pk
                    itemdetails['transfer_itemid'] =recedata['transfer_itemid']
                 
                    tagitems=TaggedItems.objects.get(tag_number=itemrow['tag_number'])
                    transfertems=TransferItem.objects.get(id=recedata['transfer_itemid'])
             
                    TaggedItems.objects.filter(id=tagitems.id).update(branch=transfertems.transfer_to.pk,transfer=0)
                    itemdetails['tagitems_id']=tagitems.id
                    itemdetails['tag_number']=itemrow['tag_number']
                    itemdetails['created_at']=timezone.now()
                    itemdetails['created_by']=request.user.id
                    itemdetails_serializer=ReceivedItemDetailsSerializer(data=itemdetails)
               
                    if itemdetails_serializer.is_valid():
                        itemdetails_serializer.save()
                       
                   
                    else:
                        raise Exception(itemdetails_serializer.errors)
 
 
                return Response(
                    {
                        "data":item_serializer.data ,
                        "message":res_msg.update("Received Item Details"),
                        "status":status.HTTP_200_OK
                    },status=status.HTTP_200_OK
                )
 
            else:
 
                return Response(
                    {
                        "data":item_serializer.errors,
                        "message":res_msg.not_update("Received Item Detials"),
                        "status":status.HTTP_400_BAD_REQUEST
                    },status=status.HTTP_200_OK
                )
        except ReceivedItem.DoesNotExist:
 
            return Response(
                {
                    "message":res_msg.not_exists("Received item"),
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
class ReceivedItemListView(APIView):
    def get(self,request,pk):
 
        try:
 
            queryset=ReceivedItem.objects.filter(id=pk).values('id','received_date','transfer_itemid','transfer_itemid__transfer_date','transfer_itemid__required_date','transfer_itemid__stock_authority','transfer_itemid__stock_authority__first_name','transfer_itemid__transfer_from','transfer_itemid__transfer_from__branch_name','transfer_itemid__transfer_to','transfer_itemid__transfer_to__branch_name','transfer_itemid__transfer_status','transfer_itemid__transfer_status__status_name')
           
            transfer_itemqueryset = ReceivedItemDetails.objects.filter(received_itemid=pk)
            res_data = []          
 
            for item in transfer_itemqueryset:
                tag_item = TaggedItems.objects.filter(tag_number=item.tag_number).values('id','tag_number','sub_item_details__sub_item_name','net_weight','gross_weight','item_details__item_details__item_name')
                if len(tag_item) > 0:
                    res_data.append(tag_item[0])
                    
            transfer_item = {}
            if len(queryset) > 0:
                transfer_item = queryset[0]
           
            data={
               "received_item": transfer_item,
               "tagged_item":res_data,
 
            }
            return Response(
                {
                    "data":data,
                    "message":res_msg.retrieve("Received Item"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
       
        except ReceivedItem.DoesNotExist:
            return Response(
                {
                    "message":res_msg.not_exists("Received Item"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
       
 
    def post(self, request):
 
        search = request.data.get('search') if request.data.get('search') else ""
        from_date = request.data.get('from_date') if request.data.get('from_date') != None else None
        to_date = request.data.get('to_date') if request.data.get('to_date') != None else None
        page = request.data.get('page') if request.data.get('page') else 1
        tag_status = request.data.get('tag_status') if request.data.get('tag_status') != None else None 
        branch = request.data.get('branch') if request.data.get('branch') else None
        try:
            items_per_page = int(request.data.get('items_per_page', ReceivedItem.objects.all().count()))
            if items_per_page == 0:
                items_per_page = 10 
        except Exception as err:
            items_per_page = 10 

        filter_condition={}

        if request.user.role.is_admin == True:
            if branch != None:            
                filter_condition['transfer_itemid__transfer_to'] = branch
        else:
            filter_condition['transfer_itemid__transfer_to'] = request.user.branch_id


        if tag_status != None:
           filter_condition['transfer_status'] = tag_status
          
             

        if from_date != None and to_date!= None:
            fdate =from_date+'T00:00:00.899010+05:30'
            tdate =to_date+'T23:59:59.899010+05:30'
            date_range=(fdate,tdate)
            filter_condition['created_at__range']=date_range

        if len(filter_condition) != 0:
           queryset = list(ReceivedItem.objects.filter(Q(transfer_itemid__stock_authority__first_name__icontains=search),**filter_condition).order_by('id'))
        elif search != '':
           queryset = list(ReceivedItem.objects.filter(Q(transfer_itemid__stock_authority__first_name__icontains=search)).order_by('id'))
        else:
           queryset=list(ReceivedItem.objects.all().order_by('id'))
        
        paginated_data = Paginator(queryset, items_per_page)
        serializer = ReceivedItemSerializer(paginated_data.get_page(page), many=True)
 
        res_data = []
        
        for i in range(0, len(serializer.data)):
            
            custom = serializer.data[i]
            custom['status'] = queryset[i].transfer_status.status_name
            custom['color'] = queryset[i].transfer_status.status_color
            custom['bgcolor'] = queryset[i].transfer_status.status_bgcolor
            custom['transfer_from'] = queryset[i].transfer_itemid.transfer_from.branch_name
            custom['transfer_to'] = queryset[i].transfer_itemid.transfer_to.branch_name
            custom['authority_name'] = queryset[i].transfer_itemid.stock_authority.first_name
            custom['received_date'] = queryset[i].received_date
            total=TransferItemDetails.objects.filter(transfer_itemid=queryset[i].transfer_itemid)
            count=total.count()
            custom['no_of_item'] = count
            reveive=ReceivedItemDetails.objects.filter(transfer_itemid=queryset[i].transfer_itemid)
            reveivecount=reveive.count()
            custom['no_of_receive'] = reveivecount
            
            returnitem=ReturnItemDetails.objects.filter(transfer_itemid=queryset[i].transfer_itemid) 
            returnitemcount=returnitem.count()
            custom['no_of_return'] = returnitemcount
 
            res_data.append(custom)
       
        return Response({
            "data": {
                "list": res_data,
                "total_pages": paginated_data.num_pages,
                "current_page": page,
                "total_items": len(queryset),
                "current_items": len(res_data)
           
            },
            "message": res_msg.retrieve('Received Item'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)

#Return Item
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ReturnItemViewset(viewsets.ViewSet):
    
   def create(self,request):
        resdata=request.data
      
        request_data = {}
        request_data['return_date'] = resdata.get('return_date')
        request_data['transfer_itemid'] = resdata.get('transfer_itemid')
        request_data['reason'] = resdata.get('reason')        
        request_data['transfer_status'] = 6
        request_data['created_at']=timezone.now()
        request_data['created_by']=request.user.id

        item_serializer=ReturnItemSerializer(data=request_data)    
        if item_serializer.is_valid():
            item_serializer.save()
            tag_item_details=resdata.get('tag_item_details') if resdata.get('tag_item_details') else {}
           
            itemdetails ={}
            for itemrow in tag_item_details:
                ReceivedItemDetails.objects.get(transfer_itemid=resdata.get('transfer_itemid')).delete()
                ReceivedItem.objects.get(transfer_itemid=resdata.get('transfer_itemid')).delete()
                itemdetails['return_itemid'] = str(item_serializer.data['id'])
                itemdetails['transfer_itemid'] =resdata.get('transfer_itemid')
                tagitems=TaggedItems.objects.get(tag_number=itemrow['tag_number'])
              
                transfertems=TransferItem.objects.get(id=resdata.get('transfer_itemid'))

                TaggedItems.objects.filter(id=tagitems.id).update(branch=transfertems.transfer_to.pk,transfer=0)
               
                itemdetails['tagitems_id']=tagitems.id
                itemdetails['tag_number']=itemrow['tag_number']
                itemdetails['created_at']=timezone.now()
                itemdetails['created_by']=request.user.id
                itemdetails_serializer=ReturnItemDetailsSerializer(data=itemdetails)
                itemtags = {}
                if itemdetails_serializer.is_valid():
                    itemdetails_serializer.save()
                    itemtags['transfer'] = 1
                   
                 
                else:
                    raise Exception(itemdetails_serializer.errors)
            return Response(
                {
                    "data":item_serializer.data,
                    "message":res_msg.create("Return Item"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )                    
        else:
            return Response(
                {
                    "data":item_serializer.errors,
                    "message":res_msg.something_else(),
                    "status":status.HTTP_204_NO_CONTENT
                },status=status.HTTP_200_OK
                )
       
       
       
   def update(self,request,pk):
   
        try:
            item_querset=ReturnItem.objects.get(id=pk)
            resdata=request.data
       
            request_data = {}
            request_data['return_date'] = resdata.get('return_date')
            request_data['transfer_itemid'] = resdata.get('transfer_itemid')
            request_data['reason'] = resdata.get('reason')  
            request_data['created_at']=timezone.now()
            request_data['created_by']=request.user.id
            request_data['modified_at']=timezone.now()
            request_data['modified_by']=request.user.id
           
            item_serializer=ReturnItemSerializer(item_querset,data=request_data,partial=True)
           
            if item_serializer.is_valid():
                item_serializer.save()
             
                itemdetails ={}
                tag_item_details=resdata.get('tag_item_details') if resdata.get('tag_item_details') else {}
                
                ReturnItemDetails.objects.filter(return_itemid=pk).delete()
 
                for itemrow in tag_item_details:
               
                    itemdetails['return_itemid'] = str(item_serializer.data['id'])
                    itemdetails['transfer_itemid'] =resdata.get('transfer_itemid')
                    tagitems=TaggedItems.objects.get(tag_number=itemrow['tag_number'])
                    TaggedItems.objects.filter(id=tagitems.id).update(transfer=1)
                    itemdetails['tagitems_id']=tagitems.id
                    itemdetails['tag_number']=itemrow['tag_number']
                    itemdetails['created_at']=timezone.now()
                    itemdetails['created_by']=request.user.id
                    itemdetails_serializer=ReturnItemDetailsSerializer(data=itemdetails)
               
                    if itemdetails_serializer.is_valid():
                        itemdetails_serializer.save()
                    else:
                        raise Exception(itemdetails_serializer.errors)
 
                return Response(
                    {
                        "data":item_serializer.data ,
                        "message":res_msg.update("Return Item Details"),
                        "status":status.HTTP_200_OK
                    },status=status.HTTP_200_OK
                )
 
            else:
 
                return Response(
                    {
                        "data":item_serializer.errors,
                        "message":res_msg.not_update("Return Item Detials"),
                        "status":status.HTTP_400_BAD_REQUEST
                    },status=status.HTTP_200_OK
                )
        except ReturnItem.DoesNotExist:
 
            return Response(
                {
                    "message":res_msg.not_exists("Return Item  item"),
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
class ReturnItemListView(APIView):
    def get(self,request,pk):
 
        try:
 
            queryset=ReturnItem.objects.filter(id=pk).values('id','reason','return_date','transfer_itemid','transfer_itemid__transfer_date','transfer_itemid__required_date','transfer_itemid__stock_authority','transfer_itemid__stock_authority__first_name','transfer_itemid__transfer_from','transfer_itemid__transfer_from__branch_name','transfer_itemid__transfer_to','transfer_itemid__transfer_to__branch_name','transfer_itemid__transfer_status','transfer_itemid__transfer_status__status_name')
           
            transfer_itemqueryset = ReturnItemDetails.objects.filter(return_itemid=pk)
            res_data = []          
 
            for item in transfer_itemqueryset:
                tag_item = TaggedItems.objects.filter(tag_number=item.tag_number).values('id','tag_number','sub_item_details__sub_item_name','net_weight','gross_weight','item_details__item_details__item_name')
                if len(tag_item) > 0:
                    res_data.append(tag_item[0])
 
            transfer_item = {}
            if len(queryset) > 0:
                transfer_item = queryset[0]
           
            data={
               "return_item": transfer_item,
               "tagged_item":res_data,
 
            }
           
            return Response(
                {
                    "data":data,
                    "message":res_msg.retrieve("Return Item"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
       
        except ReturnItem.DoesNotExist:
            return Response(
                {
                    "message":res_msg.not_exists("Return Item"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
       
 
    def post(self, request):

        search = request.data.get('search') if request.data.get('search') else ""
        from_date = request.data.get('from_date') if request.data.get('from_date') != None else None
        to_date = request.data.get('to_date') if request.data.get('to_date') != None else None
        page = request.data.get('page') if request.data.get('page') else 1
        tag_status = request.data.get('tag_status') if request.data.get('tag_status') != None else None
        branch = request.data.get('branch') if request.data.get('branch') else None
        try:
            items_per_page = int(request.data.get('items_per_page', ReturnItem.objects.all().count()))
            if items_per_page == 0:
                items_per_page = 10 
        except Exception as err:
            items_per_page = 10 
 
        if request.user.role.is_admin == True:
            if branch != None:            
                filter_condition['transfer_itemid__transfer_to'] = branch
        else:
            filter_condition['transfer_itemid__transfer_to'] = request.user.branch.pk
     
   
        filter_condition={}

        if tag_status != None:
           filter_condition['transfer_status'] = tag_status

        if from_date != None and to_date!= None:
            fdate =from_date+'T00:00:00.899010+05:30'
            tdate =to_date+'T23:59:59.899010+05:30'
            date_range=(fdate,tdate)
            filter_condition['created_at__range']=date_range

        if len(filter_condition) != 0:
           queryset = list(ReturnItem.objects.filter(Q(transfer_itemid__stock_authority__first_name__icontains=search),**filter_condition).order_by('id'))
        elif search != '':
           queryset = list(ReturnItem.objects.filter(Q(transfer_itemid__stock_authority__first_name__icontains=search)).order_by('id'))
        else:
           queryset=list(ReturnItem.objects.all().order_by('id'))
        
        paginated_data = Paginator(queryset, items_per_page)
        serializer = ReturnItemSerializer(paginated_data.get_page(page), many=True)
 
        res_data = []
        for i in range(0, len(serializer.data)):
            
            custom = serializer.data[i]
            custom['status'] = queryset[i].transfer_status.status_name
            custom['color'] = queryset[i].transfer_status.status_color
            custom['bgcolor'] = queryset[i].transfer_status.status_bgcolor
            custom['transfer_from'] = queryset[i].transfer_itemid.transfer_from.branch_name
            custom['transfer_to'] = queryset[i].transfer_itemid.transfer_to.branch_name
            custom['authority_name'] = queryset[i].transfer_itemid.stock_authority.first_name
            custom['return_date'] = queryset[i].return_date
            total=TransferItemDetails.objects.filter(transfer_itemid=queryset[i].transfer_itemid)
            count=total.count()
            custom['no_of_item'] = count
            reveive=ReceivedItemDetails.objects.filter(transfer_itemid=queryset[i].transfer_itemid)
            reveivecount=reveive.count()
            custom['no_of_receive'] = reveivecount
            
            returnitem=ReturnItemDetails.objects.filter(transfer_itemid=queryset[i].transfer_itemid) 
            returnitemcount=returnitem.count()
            custom['no_of_return'] = returnitemcount
 
            res_data.append(custom)
       
        return Response({
            "data": {
                "list": res_data,
                "total_pages": paginated_data.num_pages,
                "current_page": page,
                "total_items": len(queryset),
                "current_items": len(res_data)
            },
            "message": res_msg.retrieve('Return Item'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)



@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ApproveTransferItemViewset(viewsets.ViewSet):
    
    def update(self,request,pk):
   
        try:
            item_querset=TransferItem.objects.get(id=pk)
            resdata=request.data
        
            request_data = {}
            request_data['transfer_status'] = resdata.get('transfer_status') #Received
            
            item_serializer=TransferItemSerializer(item_querset,data=request_data,partial=True)
            
            if item_serializer.is_valid():
                item_serializer.save()   

                receivedata = item_serializer.data 
                
                if int(resdata.get('transfer_status')) == 2:
                    receive_data = {}
                    receive_data['transfer_status'] = 4
                    receive_data['transfer_itemid'] = pk
                    receive_data['created_at']=timezone.now()
                    receive_data['created_by']=request.user.id
                
                    receive_serializer=ReceivedItemSerializer(data=receive_data) 
                       
                    if receive_serializer.is_valid():
                        receive_serializer.save() 
                        recedata = receive_serializer.data
                        
                        transfer_queryset=list(TransferItemDetails.objects.filter(transfer_itemid=pk))
                        itemdetails = {}
                        
                        for itemrow in transfer_queryset:
                          
                            itemdetails['received_itemid']= recedata['id']
                            
                            itemdetails['transfer_itemid']= pk

                            tagitems=TaggedItems.objects.get(tag_number=itemrow.tag_number)
                            
                            TaggedItems.objects.filter(id=tagitems.id).update(transfer=1)
                            
                            itemdetails['tagitems_id']=tagitems.id
                            itemdetails['tag_number']=itemrow.tag_number
                            itemdetails['created_at']=timezone.now()
                            itemdetails['created_by']=request.user.id

                            itemdetails_serializer=ReceivedItemDetailsSerializer(data=itemdetails)
                    
                            if itemdetails_serializer.is_valid():
                                itemdetails_serializer.save()
                            
                            
                            else:
                                raise Exception(itemdetails_serializer.errors)   
                    message = 'Approved'
                else:
                    ReceivedItemDetails.objects.filter(transfer_itemid=pk).delete()
                    ReceivedItem.objects.filter(transfer_itemid=pk).delete()
                    message = 'Rejected'
                return Response(
                {
                    "data":item_serializer.data ,
                    "message":res_msg.update(message),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
                )

            else:

                return Response(
                    {
                        "data":item_serializer.errors,
                        "message":res_msg.not_update("Transfer Item Detials"),
                        "status":status.HTTP_400_BAD_REQUEST
                    },status=status.HTTP_200_OK
                )
        except TransferItem.DoesNotExist:

            return Response(
                {
                    "message":res_msg.not_exists("Tansfer item"),
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
class ApproveReturnItemViewset(viewsets.ViewSet):
    
    def update(self,request,pk):
   
        try:
            item_querset=ReturnItem.objects.get(id=pk)
            resdata=request.data
        
            request_data = {}
            request_data['transfer_status'] = resdata.get('transfer_status') #Received
            
            item_serializer=ReturnItemSerializer(item_querset,data=request_data,partial=True)
            
            if item_serializer.is_valid():
                item_serializer.save()   

                receivedata = item_serializer.data 
               
                if int(resdata.get('transfer_status')) == 7:
                    
                    message = 'Approved'
                else:


                    receive_data = {}
                    receive_data['transfer_status'] = 4
                    receive_data['transfer_itemid'] = receivedata['transfer_itemid']
                    receive_data['created_at']=timezone.now()
                    receive_data['created_by']=request.user.id
                
                    receive_serializer=ReceivedItemSerializer(data=receive_data) 
                    
                    if receive_serializer.is_valid():
                        receive_serializer.save() 
                        recedata = receive_serializer.data
                        
                        transfer_queryset=list(TransferItemDetails.objects.filter(transfer_itemid=receivedata['transfer_itemid']))
                        itemdetails = {}
                        
                        for itemrow in transfer_queryset:
                        
                            itemdetails['received_itemid']= recedata['id']
                            
                            itemdetails['transfer_itemid']= receivedata['transfer_itemid']

                            tagitems=TaggedItems.objects.get(tag_number=itemrow.tag_number)
                            
                            TaggedItems.objects.filter(id=tagitems.id).update(transfer=1)
                            
                            itemdetails['tagitems_id']=tagitems.id
                            itemdetails['tag_number']=itemrow.tag_number
                            itemdetails['created_at']=timezone.now()
                            itemdetails['created_by']=request.user.id
                            itemdetails_serializer=ReceivedItemDetailsSerializer(data=itemdetails)
                    
                            if itemdetails_serializer.is_valid():
                                itemdetails_serializer.save()
                            
                            
                            else:
                                raise Exception(itemdetails_serializer.errors)   
                            
                    ReturnItemDetails.objects.get(transfer_itemid=receivedata['transfer_itemid']).delete()
                    ReturnItem.objects.get(transfer_itemid=receivedata['transfer_itemid']).delete()
                    message = 'Rejected'




                return Response(
                {
                    "data":item_serializer.data ,
                    "message":res_msg.update(message),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
                )

            else:

                return Response(
                    {
                        "data":item_serializer.errors,
                        "message":res_msg.not_update("Transfer Item Detials"),
                        "status":status.HTTP_400_BAD_REQUEST
                    },status=status.HTTP_200_OK
                )
        except TransferItem.DoesNotExist:

            return Response(
                {
                    "message":res_msg.not_exists("Tansfer item"),
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
class TransferStatusLiView(APIView):

    def get(self,request,type=None):

        if int(type)< 4:
            queryset=list(TransferStatus.objects.filter().exclude(id__in=[4,5,6,7,8]))
        elif int(type) > 5:
            queryset=list(TransferStatus.objects.filter().exclude(id__in=[1,2,3,4,5]))
        else:
            queryset=list(TransferStatus.objects.all().exclude(id__in=[4,5]))
        serializer = TransferStatusSerializer(queryset, many=True)

        return Response(
            {
                "data":{
                    "list":serializer.data,
                },
                "message":res_msg.retrieve("Status"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class TransferFilterStatusLiView(APIView):

    def get(self,request,type=None):

        if int(type)== 1:
            queryset=list(TransferStatus.objects.filter().exclude(id__in=[4,5,6,7,8]))
        elif int(type) == 2:
            queryset=list(TransferStatus.objects.filter().exclude(id__in=[2,3,4,5,6,7,8]))
        elif int(type) == 3:
            queryset=list(TransferStatus.objects.filter().exclude(id__in=[1,2,3,6,7,8]))
        else:
            queryset=list(TransferStatus.objects.all().exclude(id__in=[1,2,3,4,5]))
        serializer = TransferStatusSerializer(queryset, many=True)
        
        return Response(
            {
                "data":{
                    "list":serializer.data,
                },
                "message":res_msg.retrieve("Status"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class TaggedItemListView(APIView):
    def get(self,request,tag_number=None):
 
        try:
            filter_condition={}
            if tag_number != None:
                filter_condition['tag_number'] = tag_number
      
            queryset = list(TaggedItems.objects.filter(**filter_condition).values('id','tag_number','sub_item_details__sub_item_name','net_weight','gross_weight','item_details__item_details__item_name'))
            rowdata = {}
            if len(queryset) > 0:
                rowdata = queryset[0]
            return Response(
                    {
                    "data":{
                        "list":rowdata,
                        },
                        "message":res_msg.retrieve("Tagged Item"),
                        "status":status.HTTP_200_OK
                    },status=status.HTTP_200_OK
            )
       
        except TransferItem.DoesNotExist:
            return Response(
                {
                    "message":res_msg.not_exists("Transfer Item"),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
       


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class TaggedBranchItemListView(APIView):
    def get(self,request,tag_number=None,branch=None):
 
        try:
            if request.user.role.is_admin == False:
                branch_filter = request.user.branch.pk
            else:
                if branch!= None:
                    branch_filter=branch

                else:
                    return Response(
                        {
                            "message":"branch is required",
                            "status":status.HTTP_204_NO_CONTENT
                        },status=status.HTTP_200_OK
                    )
                
            if tag_number != None:
                tag_number_filter = tag_number

            else:
                return Response(
                    {
                        "message":"Tag Number is Required",
                        "stauts":status.HTTP_204_NO_CONTENT
                    },status=status.HTTP_200_OK
                )
            
            queryset = TaggedItems.objects.get(tag_number=tag_number_filter,branch = branch_filter)

            if queryset.is_billed == True:

                return Response(
                    {
                        "message":"The Tag is Already Billed",
                        "status":status.HTTP_404_NOT_FOUND
                    },status=status.HTTP_200_OK
                )
            
            else:

                res_data ={
                    "id":queryset.pk,
                    "branch":queryset.branch.branch_name,
                    "tag_number":queryset.tag_number,
                    "item_name":queryset.item_details.item_details.item_name,
                    "sub_item_name":queryset.sub_item_details.sub_item_name,
                    "gross_weight":queryset.gross_weight,
                    "net_weight":queryset.net_weight
                }

                return Response(
                    {
                        "data":res_data,
                        "message":res_msg.retrieve("Tag Details"),
                        "status":status.HTTP_200_OK
                    },status=status.HTTP_200_OK
                )
            
        except TaggedItems.DoesNotExist:

            return Response(
                {
                    "message":res_msg.not_exists("Tag Details"),
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
class TransferTypeView(APIView):

    def get(self,request):

        queryset=list(TransferType.objects.all())
        serializer = TransferTypeSerializer(queryset, many=True)
        return Response(
            {
                "data":{
                    "list":serializer.data,
                },
                "message":res_msg.retrieve("Status"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ApprovalIssueNumberView(APIView):  
    def get(self, request):  
        try:
            
            user_id = request.user.id
            user_instance = User.object.get(id=user_id)
            try:
                approval_issue_number = ApprovalIssueNumber.objects.get(user=user_instance)
                return Response(
                    {
                        "data": approval_issue_number.approval_issue_number,
                        "message": "Approval Issue Number found",
                        "status": status.HTTP_200_OK
                    },
                    status=status.HTTP_200_OK
                )
            except ApprovalIssueNumber.DoesNotExist:
                next_approval_issue_number = self.generateapprovalissuenumber()
                
                ApprovalIssueNumber.objects.create(user=user_instance, approval_issue_number=next_approval_issue_number)

                return Response(
                    {
                        "data": next_approval_issue_number,
                        "message": "New Approval Issue Number generated",
                        "status": status.HTTP_200_OK
                    },
                    status=status.HTTP_200_OK
                )

        except Exception as err:
            return Response(
                {
                    "data": str(err),
                    "message": res_msg.something_else(),
                    "status": status.HTTP_204_NO_CONTENT
                },
                status=status.HTTP_200_OK
            )

        
    def generateapprovalissuenumber(self):
        try:
            approval_issue_queryset = ApprovalIssueID.objects.all().order_by('-id').first()
            
            if approval_issue_queryset:
                number = int(approval_issue_queryset.pk) + 1
            else:
                number = 1
            prefix = 'APP-ISS-00'
            approval_issue = f'{prefix}{number}'
            ApprovalIssueID.objects.create(approval_issue_id=approval_issue)
            return approval_issue
        except Exception as err:
            ApprovalIssueID.objects.create(approval_issue_id='APP-ISS-001')
            return 'APP-ISS-001'
        

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ApprovalIssueView(viewsets.ViewSet): 
    
    @transaction.atomic
    def create(self,request):
        
        try:
            
            request_data = request.data 
            
            request_data['created_at'] = timezone.now()
            request_data['created_by'] = request.user.id
            request_data['status'] = settings.APPROVAL_ISSUED
            request_data['bill_type'] = request_data.get('bill_type')

            
            if request.user.role.is_admin == False:
                request_data['branch'] = request.user.branch.pk
                
            issue_details_serializer = ApprovalIssueSerializer(data=request_data)
            
            if issue_details_serializer.is_valid():
                issue_details_serializer.save()
                
                try:
                    approval_issue_number = ApprovalIssueNumber.objects.get(user=request.user.pk)
                    approval_issue_number.delete()
                    
                except Exception as err:
                    raise Exception(err)
                
                issue_tag_details = request_data.get('issue_tag_details')
                
                for tag in issue_tag_details:
                    
                    tag_details ={}
                    
                    tag_number=tag
                    
                    tag_queryset = TaggedItems.objects.get(tag_number=tag_number)
                    
                    tag_details['approval_issue_details'] = issue_details_serializer.data['id']
                    tag_details['tag_details'] = tag_queryset.pk
                    
                    issue_tag_serializer = ApprovalIssueTagItemsSerializer(data=tag_details)
                    
                    if issue_tag_serializer.is_valid():
                        issue_tag_serializer.save()
                        
                        tag_queryset.transfer = True
                        tag_queryset.save()
                        
                    else:
                        raise Exception(issue_tag_serializer.errors)
                    
                return Response(
                    {
                        "data":issue_details_serializer.data,
                        "message":res_msg.create("Approval Issue"),
                        "status":status.HTTP_200_OK
                    },status=status.HTTP_200_OK
                )
                    
            else:
                raise Exception(issue_details_serializer.errors)
                        
        except Exception as err:
            transaction.rollback(True)
            return Response(
                {
                    "data":str(err),
                    "message":res_msg.something_else(),
                    "status":status.HTTP_204_NO_CONTENT
                },status=status.HTTP_200_OK
            )
            
    def retrieve(self,request,pk):
        
        try:
            
            issue_details_queryset = ApprovalIssue.objects.get(id=pk)
            
            res_data = {}
            
            res_data['id'] = issue_details_queryset.pk
            res_data['approval_issue_id'] = issue_details_queryset.approval_issue_id
            res_data['bill_type'] = issue_details_queryset.bill_type.pk
            res_data['issue_date'] = issue_details_queryset.issue_date
            res_data['issued_by'] = issue_details_queryset.issued_by
            res_data['receiver_name'] = issue_details_queryset.receiver_name
            res_data['shop_name'] = issue_details_queryset.shop_name.pk
            res_data['shop_name_details'] = issue_details_queryset.shop_name.customer_name
            res_data['branch'] = issue_details_queryset.branch.pk
            res_data['branch_name'] = issue_details_queryset.branch.branch_name
            res_data['notes'] = issue_details_queryset.notes
            res_data['shop_address'] = {
                "door_no":issue_details_queryset.shop_name.door_no,
                "street_name":issue_details_queryset.shop_name.street_name,
                "area":issue_details_queryset.shop_name.area,
                "taluk":issue_details_queryset.shop_name.taluk,
                "postal":issue_details_queryset.shop_name.postal,
                "district":issue_details_queryset.shop_name.district,
                "state":issue_details_queryset.shop_name.state,
                "country":issue_details_queryset.shop_name.country,
                "pincode":issue_details_queryset.shop_name.pincode
            }
            
            issued_tag_item_queryset = ApprovalIssueTagItems.objects.filter(approval_issue_details=issue_details_queryset.pk)
            
            issued_tag_details= []
            
            for tag in issued_tag_item_queryset:
                
                tag_details={}
                tag_details['id'] = tag.pk
                tag_details['tag_number'] = tag.tag_details.tag_number
                tag_details['metal'] = tag.tag_details.sub_item_details.metal.metal_name
                tag_details['item_name'] = tag.tag_details.sub_item_details.item_details.item_name
                tag_details['sub_item_name'] = tag.tag_details.sub_item_details.sub_item_name
                tag_details['gross_weight'] = tag.tag_details.gross_weight
                tag_details['net_weight'] = tag.tag_details.net_weight
                tag_details['pieces'] = tag.tag_details.tag_pieces
                tag_details['from_db'] = True
                
                issued_tag_details.append(tag_details)
                
            res_data['issued_tag_details'] =issued_tag_details
            
            return Response(
                {
                    "data":res_data,
                    "message":res_msg.retrieve("Approval Issue Details"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
            
        except ApprovalIssue.DoesNotExist:
            
            return Response(
                {
                    "message":res_msg.not_exists("Approval Issue Details"),
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
            
    
    @transaction.atomic        
    def update(self,request,pk):
        
        try:
            
            with transaction.atomic():
            
                queryset = ApprovalIssue.objects.get(id=pk)
                request_data = request.data
                
                request_data['modified_at'] = timezone.now()
                request_data['modified_by'] = request.user.pk
                
                serializer = ApprovalIssueSerializer(queryset,data=request_data,partial=True)
                
                if serializer.is_valid():
                    serializer.save()
                
                    new_tag_items = request_data.get('new_tag_items') if request_data.get('new_tag_items') else []
                    
                    for new_tag in new_tag_items:
                        req_data = {}
                        req_data['approval_issue_details'] = queryset.pk
                        
                        tag_queryset = TaggedItems.objects.get(tag_number=new_tag)
                        req_data['tag_details'] = tag_queryset.pk
                        
                        issued_tag_serializer = ApprovalIssueTagItemsSerializer(data=req_data)
                        
                        if issued_tag_serializer.is_valid():
                            issued_tag_serializer.save()
                        
                        else:
                            raise Exception(issued_tag_serializer.errors)
                        
                    return Response(
                        {
                            "data":serializer.data,
                            "message":res_msg.update("Approval Issue Details"),
                            "status":status.HTTP_200_OK
                        },status=status.HTTP_200_OK
                    )
                        
                else:
                    raise Exception(serializer.errors)
                        
        except ApprovalIssue.DoesNotExist:
            return Response(
                {
                    "message":res_msg.not_exists("Approval Issue"),
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
            
    def delete(self,request,pk):
        
        try:
            
            queryset = ApprovalIssue.objects.get(id=pk)
            
            if queryset.status.pk == int(settings.APPROVAL_RECEIVED):
                return Response(
                    {
                        "Message":"Cannot Cancel the Approval After Receiving",
                        "status":status.HTTP_204_NO_CONTENT
                    },status=status.HTTP_200_OK
                )
                
            status_queryset = StatusTable.objects.get(id=settings.CANCELLED)
            
            queryset.status = status_queryset.pk
            queryset.save()
            
            return Response(
                {
                    "message":res_msg.change("Approval Issue status"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
            
        except ApprovalIssue.DoesNotExist:
            
            return Response(
                {
                    "message":res_msg.not_exists('Approval Issue'),
                    "status":status.HTTP_404_NOT_FOUND
                },status=status.HTTP_200_OK
            )
        
        except ProtectedError:
            return Response(
                {
                    "message":res_msg.related_item("Please"),
                    "status":status.HTTP_204_NO_CONTENT
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
                    
def deleteapprovalissue(pk):
    
    try:
        approval_issue_delete_queryset = ApprovalIssue.objects.get(id=pk)
        approval_issue_delete_queryset.delete() 
    except:
        pass
            
            
            
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ApprovalIssueListView(APIView):
    def get(self, request):
 
        queryset = list(ApprovalIssue.objects.all().order_by('id'))
        serializer = ApprovalIssueSerializer(queryset,many=True)

        res_data = []
        for i in range(0, len(serializer.data)):
            res_dict = serializer.data[i]
            res_dict['shop'] = queryset[i].shop_name.customer_name
            res_dict['branch_name'] = queryset[i].branch.branch_name
            res_dict['status_name'] = queryset[i].status.status_name
            res_dict['status_color'] = queryset[i].status.color
            
            res_data.append(res_dict)

        return Response({
            "data": res_data,
            "message":res_msg.retrieve("Approval Issue List"),
            "status":status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
        

    def post(self, request):
        search = request.data.get('search') if request.data.get('search') else ""
        from_date = request.data.get('from_date') if request.data.get('from_date') != None else None
        to_date = request.data.get('to_date') if request.data.get('to_date') != None else None
        page = request.data.get('page') if request.data.get('page') else 1
        branch = request.data.get('branch', None)
        
        try:
            items_per_page = int(request.data.get('items_per_page', ApprovalIssue.objects.all().count()))
            if items_per_page == 0:
                items_per_page = 10 
        except Exception as err:
            items_per_page = 10 

        filter_condition={}
        
        if from_date != None and to_date!= None:
           date_range=(from_date,from_date)
           filter_condition['created_at__range']=date_range
 
        if request.user.role.is_admin == True:
            if branch != None:            
                filter_condition['branch'] = branch
        else:
            filter_condition['branch'] = request.user.branch.pk
            
        if len(filter_condition) != 0:
            queryset = list(ApprovalIssue.objects.filter(Q(approval_issue_id__icontains=search) | Q(shop_name__customer_name__icontains=search) | Q(receiver_name__icontains=search), **filter_condition).order_by('id'))
        else:
            queryset = list(ApprovalIssue.objects.filter(Q(approval_issue_id__icontains=search) | Q(shop_name__customer_name__icontains=search) | Q(receiver_name__icontains=search)).order_by('id'))
        
        res_data = []

        paginated_data = Paginator(queryset, items_per_page)


        for i in list(paginated_data.get_page(page)):
            serializer = ApprovalIssueSerializer(i)
            res_dict = serializer.data
            res_dict['shop'] = i.shop_name.customer_name
            res_dict['branch_name'] = i.branch.branch_name
            res_dict['status_name'] = i.status.status_name
            res_dict['status_color'] = i.status.color
            
            res_data.append(res_dict)

        return Response({
            "data": {
                "list": res_data,
                "total_pages": paginated_data.num_pages,
                "current_page": page,
                "total_items": len(queryset),
                "current_items": len(list(paginated_data.get_page(page)))
            },
            "message":res_msg.retrieve("Approval Issue List"),
            "status":status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
        

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ApprovalReciptView(APIView):
    @transaction.atomic 
    def post(self,reqeuest,pk):
        
        try:
            
            with transaction.atomic():
            
                reqeuest_data=reqeuest.data
                
                approval_issue_queryset = ApprovalIssue.objects.get(id=pk)
                
                received_tag_details=reqeuest_data['received_tag_details']
                
                for received_tag in received_tag_details:
                    
                    received_tag_queryset = ApprovalIssueTagItems.objects.get(id=received_tag)
                    received_tag_queryset.is_received = True
                    received_tag_queryset.save()
                    
                    tag_queryset = TaggedItems.objects.get(id=received_tag_queryset.tag_details.pk)
                    tag_queryset.transfer = False
                    tag_queryset.save()
                    
                sold_tag_details = reqeuest_data['sold_tag_details']
                
                for sold_tag in sold_tag_details:
                    
                    sold_tag_queryset = ApprovalIssueTagItems.objects.get(id=sold_tag)
                    sold_tag_queryset.is_sold = True
                    sold_tag_queryset.save()
                    
                status_queryset = StatusTable.objects.get(id=int(settings.APPROVAL_RECEIVED))
                
                approval_issue_queryset.status = status_queryset
                approval_issue_queryset.save()
                
                return Response(
                    {
                        "message":res_msg.create("Approval Recipt"),
                        "status":status.HTTP_200_OK
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
class GetApprovalIssueDetails(APIView):    
    def get(self,request,pk,gst_type):
        try:
            if pk != None:
                approval_details = {}
                res_data = []
                approval_issue_details = []
                try:
                    queryset = ApprovalIssue.objects.get(id=pk)
                    serializer = ApprovalIssueSerializer(queryset)
                    approval_details.update(serializer.data)
                    approval_details['phone'] = queryset.shop_name.phone
                except ApprovalIssue.DoesNotExist:
                    return Response(
                    {
                        "message" : res_msg.not_exists('Approval Issue Details'),
                        "status": status.HTTP_204_NO_CONTENT,                        
                    }, status=status.HTTP_200_OK
                )  

                particulars = []
                tag_item_queryset = ApprovalIssueTagItems.objects.filter(approval_issue_details=pk)
                
                for item in tag_item_queryset:
                    tagged_item = TaggedItems.objects.get(id=item.tag_details.pk)
                    tag_details={
                        'id':tagged_item.pk,
                        'tag_number':tagged_item.tag_number,
                        'gross_weight':tagged_item.gross_weight,
                        'item_details':tagged_item.item_details.pk,
                        'item':tagged_item.item_details.item_details.item_name,
                        'jewel_type':tagged_item.sub_item_details.metal.metal_name,
                        'loop_weight':tagged_item.loop_weight,
                        'cover_weight':tagged_item.cover_weight,
                        'metal':tagged_item.sub_item_details.metal.pk,
                        'net_weight':tagged_item.net_weight,
                        'other_weight':tagged_item.other_weight,
                        "calculation_type":tagged_item.calculation_type.pk,
                        "calculation_type_name":tagged_item.calculation_type.calculation_name,
                        "stock_type":tagged_item.sub_item_details.stock_type.pk,
                        "stock_type_name":tagged_item.sub_item_details.stock_type.stock_type_name,
                        "tag_type":tagged_item.tag_type.tag_name,
                        'calculation_type':tagged_item.calculation_type.pk,
                        'calculation_type_name':tagged_item.calculation_type.calculation_name,
                        'stone_rate':tagged_item.stone_rate,
                        'sub_item_details':tagged_item.sub_item_details.pk,
                        'sub_item_name':tagged_item.sub_item_details.sub_item_name,
                        'tag_weight':tagged_item.tag_weight,
                        "stone_rate":tagged_item.stone_rate,
                        "diamond_rate":tagged_item.diamond_rate,
                        "total_stone_weight":tagged_item.stone_weight,
                        "total_diamond_weight":tagged_item.diamond_weight,
                        'remaining_pieces':tagged_item.remaining_pieces,
                        'remaining_gross_weight':tagged_item.remaining_gross_weight,
                        'remaining_net_weight':tagged_item.remaining_net_weight,
                        'remaining_tag_count':tagged_item.remaining_tag_count,
                        'is_billed':tagged_item.is_billed,
                        "designer_name":tagged_item.tag_entry_details.lot_details.designer_name.account_head_name,
                        "tagged_date":tagged_item.created_at,
                    }
                    if str(tagged_item.calculation_type.pk) == settings.FIXEDRATE:
                        tag_details['min_fixed_rate']=tagged_item.min_fixed_rate 
                        tag_details['max_fixed_rate']=tagged_item.max_fixed_rate

                        tag_details['min_sale_value']=(tagged_item.min_fixed_rate + tagged_item.stone_rate + tagged_item.diamond_rate)
                        tag_details['max_sale_value']=(tagged_item.max_fixed_rate + tagged_item.stone_rate + tagged_item.diamond_rate)

                        tag_details['rate'] = tag_details['max_sale_value'] + tagged_item.item_details.item_details.huid_rate

                    elif str(tagged_item.calculation_type.pk) == settings.WEIGHTCALCULATION:
                        try:
                            metal_rate_queryset = MetalRate.objects.filter(purity=tagged_item.sub_item_details.purity.pk).order_by('-id')[0]
                            metal_rate = metal_rate_queryset.rate
                        except Exception as err:
                            metal_rate=0
                    
                        metal_value=(float(metal_rate)*float(tagged_item.net_weight))

                        subitem_weight_queryset=SubItemWeightCalculation.objects.get(sub_item_details=tagged_item.sub_item_details.pk)

                        if str(subitem_weight_queryset.wastage_calculation.pk) == settings.GROSSWEIGHT :

                            min_wastage_value=((tagged_item.gross_weight*tagged_item.min_wastage_percent)/100)*metal_rate

                        else:

                            min_wastage_value=((tagged_item.net_weight*tagged_item.min_wastage_percent)/100)*metal_rate

                        min_flat_wastage=tagged_item.min_flat_wastage

                        if str(subitem_weight_queryset.making_charge_calculation.pk) == settings.GROSSWEIGHT :

                            min_making_Charge=(tagged_item.min_making_charge_gram*tagged_item.gross_weight)

                        else:

                            min_making_Charge=(tagged_item.min_making_charge_gram*tagged_item.net_weight)


                        min_flat_making_charge=tagged_item.min_flat_making_charge

                        min_sale_value = metal_value + min_wastage_value + min_flat_wastage + min_making_Charge + min_flat_making_charge + tagged_item.stone_rate + tagged_item.diamond_rate

                        #max sale value calculation

                        if str(subitem_weight_queryset.wastage_calculation.pk) == settings.GROSSWEIGHT :

                            max_wastage_value=((tagged_item.gross_weight * tagged_item.max_wastage_percent)/100)*metal_rate

                        else:

                            max_wastage_value=((tagged_item.net_weight * tagged_item.max_wastage_percent)/100)*metal_rate


                        max_flat_wastage=tagged_item.max_flat_wastage

                        if str(subitem_weight_queryset.making_charge_calculation.pk) == settings.GROSSWEIGHT :

                            max_making_Charge=(tagged_item.max_making_charge_gram * tagged_item.gross_weight)
                        
                        else:

                            max_making_Charge=(tagged_item.max_making_charge_gram * tagged_item.net_weight)

                        
                        max_flat_making_charge = tagged_item.max_flat_making_charge
                        
                        max_sale_value = metal_value + max_wastage_value + max_flat_wastage + max_making_Charge + max_flat_making_charge + tagged_item.stone_rate + tagged_item.diamond_rate
                        
                        tag_details['metal_rate'] = metal_rate
                        tag_details['wastage_calculation_type'] = subitem_weight_queryset.wastage_calculation.pk
                        tag_details['wastage_calculation_name'] = subitem_weight_queryset.wastage_calculation.weight_name
                        tag_details['making_charge_calculation_type'] = subitem_weight_queryset.making_charge_calculation.pk
                        tag_details['making_charge_calculation_name'] = subitem_weight_queryset.making_charge_calculation.weight_name
                        tag_details['min_wastage_percent'] = tagged_item.min_wastage_percent
                        tag_details['min_flat_wastage'] = tagged_item.min_flat_wastage
                        tag_details['wastage_percent'] = tagged_item.max_wastage_percent
                        tag_details['flat_wastage'] = tagged_item.max_flat_wastage
                        tag_details['max_wastage_percent'] = tagged_item.max_wastage_percent
                        tag_details['max_flat_wastage'] = tagged_item.max_flat_wastage
                        tag_details['min_making_charge'] = tagged_item.min_making_charge_gram
                        tag_details['min_flat_making_charge'] = tagged_item.min_flat_making_charge
                        tag_details['making_charge'] = tagged_item.max_making_charge_gram
                        tag_details['flat_making_charge'] = tagged_item.max_flat_making_charge
                        tag_details['max_making_charge'] = tagged_item.max_making_charge_gram
                        tag_details['max_flat_making_charge'] = tagged_item.max_flat_making_charge

                        tag_details['min_sale_value']=min_sale_value
                        tag_details['max_sale_value']=max_sale_value

                        tag_details['rate'] = tag_details['max_sale_value'] + tagged_item.item_details.item_details.huid_rate

                    elif str(tagged_item.calculation_type.pk) == settings.PERGRAMRATE:

                        tag_details['min_pergram_rate']=tagged_item.min_pergram_rate
                        tag_details['max_pergram_rate']=tagged_item.max_pergram_rate
                        tag_details['per_gram_weight_type'] = tagged_item.per_gram_weight_type.pk
                        tag_details['per_gram_weight_type_name'] = tagged_item.per_gram_weight_type.weight_name

                        if str(tagged_item.per_gram_weight_type.pk) == settings.GROSSWEIGHT :

                            min_per_gram_value=float(tagged_item.gross_weight) * float(tagged_item.min_pergram_rate)
                            max_per_gram_value=float(tagged_item.gross_weight) * float(tagged_item.max_pergram_rate)

                        else:

                            min_per_gram_value=float(tagged_item.net_weight) * float(tagged_item.min_pergram_rate)
                            max_per_gram_value=float(tagged_item.net_weight) * float(tagged_item.max_pergram_rate)

                        tag_details['min_sale_value']=(min_per_gram_value + tagged_item.stone_rate + tagged_item.diamond_rate)
                        tag_details['max_sale_value']=(max_per_gram_value + tagged_item.stone_rate + tagged_item.diamond_rate)

                        tag_details['rate'] = tag_details['max_sale_value'] + tagged_item.item_details.item_details.huid_rate

                    elif str(tagged_item.calculation_type.pk) == settings.PERPIECERATE:
                        tag_details['min_per_piece_rate'] = tagged_item.min_per_piece_rate
                        tag_details['per_piece_rate'] = tagged_item.per_piece_rate

                        tag_details['min_per_piece_rate']=tagged_item.min_per_piece_rate  
                        tag_details['max_per_piece_rate']=tagged_item.max_per_piece_rate  
                        min_rate =  tagged_item.tag_pieces * tagged_item.min_per_piece_rate
                        max_rate =  tagged_item.tag_pieces * tagged_item.max_per_piece_rate
                        tag_details['min_sale_value']=(min_rate + tagged_item.stone_rate + tagged_item.diamond_rate)
                        tag_details['max_sale_value']=(max_rate + tagged_item.stone_rate + tagged_item.diamond_rate)  

                        tag_details['rate'] = tag_details['max_sale_value'] + tagged_item.item_details.item_details.huid_rate

                    try:
                        tax_queryset = TaxDetailsAudit.objects.filter(metal=tagged_item.item_details.item_details.metal.pk).order_by('-id').first()

                        if tax_queryset:
                            tax_percent_queryset = SalesTaxDetails.objects.get(tax_details=tax_queryset.tax_details)

                            if int(gst_type) == settings.INTRA_STATE_GST:
                                tag_details['gst'] = (((tax_percent_queryset.sales_tax_cgst + tax_percent_queryset.sales_tax_sgst + tax_percent_queryset.sales_surcharge_percent)/100) * tag_details['rate']) + tax_percent_queryset.sales_additional_charges
                                tag_details['sales_tax_cgst']=tax_percent_queryset.sales_tax_cgst
                                tag_details['sales_tax_sgst']=tax_percent_queryset.sales_tax_sgst

                            elif int(gst_type) == settings.INTER_STATE_GST:
                                tag_details['gst'] = (((tax_percent_queryset.sales_tax_igst + tax_percent_queryset.sales_surcharge_percent)/100) * tag_details['rate']) + tax_percent_queryset.sales_additional_charges
                                tag_details['sales_tax_igst']=tax_percent_queryset.sales_tax_igst
                           
                    except Exception as err:
                        tag_details['gst'] = 0
                        tag_details['sales_tax_igst']=0
                        tag_details['sales_tax_cgst']=0
                        tag_details['sales_tax_sgst']=0
                        tag_details['sales_surcharge_percent']=0
                        tag_details['sales_additional_charges'] = 0

                    tag_details['with_gst_rate'] = tag_details['rate'] + tag_details['gst']

                    stone_queryset=TaggedItemStone.objects.filter(tag_details=tagged_item.pk)
                    stone_details=[]
                    
                    for stone in stone_queryset:
                        stone_data={
                            'id' : stone.pk,
                            'stone_name':stone.stone_name.pk,
                            'stone_pieces':stone.stone_pieces,
                            'stone_weight':stone.stone_weight,
                            'stone_weight_type':stone.stone_weight_type.pk,
                            'stone_weight_type_name':stone.stone_weight_type.weight_name,
                            'stone_rate':stone.stone_rate,
                            'stone_rate_type':stone.stone_rate_type.pk,
                            'stone_rate_type_name':stone.stone_rate_type.type_name,
                            'include_stone_weight':stone.include_stone_weight
                        }

                        if str(stone.stone_weight_type.pk) == settings.CARAT:
                            stone_data['stone_weight'] = float(stone.stone_weight)*5

                        else:
                            stone_data['stone_weight'] = float(stone.stone_weight)

                        if str(stone.stone_rate_type.pk) == settings.PERCARAT:
                            stone_data['stone_rate'] = float(stone.stone_rate)/5

                        elif str(stone.stone_rate_type.pk) == settings.PERPIECE:
                            stone_data['stone_rate'] = float(stone.stone_rate)
                        else:
                            stone_data['stone_rate'] = float(stone.stone_rate)

                        stone_details.append(stone_data)
                    tag_details['stone_details']=stone_details
                
                    diamond_queryset=TaggedItemDiamond.objects.filter(tag_details=tagged_item.pk)
                    diamond_details=[]
                    
                    for diamond in diamond_queryset:
                        diamond_data={
                            'id' : diamond.pk,
                            'diamond_name':diamond.diamond_name.pk,
                            'diamond_pieces':diamond.diamond_pieces,
                            'diamond_weight':diamond.diamond_weight,
                            'diamond_weight_type':diamond.diamond_weight_type.pk,
                            'diamond_weight_type_name':diamond.diamond_weight_type.weight_name,
                            'diamond_rate':diamond.diamond_rate,
                            'diamond_rate_type':diamond.diamond_rate_type.pk,
                            'diamond_rate_type_name':diamond.diamond_rate_type.type_name,
                            'include_diamond_weight':diamond.include_diamond_weight
                        }

                        if str(diamond.diamond_weight_type.pk) == settings.CARAT:
                            diamond_data['diamond_weight'] = float(diamond.diamond_weight)*5

                        else:
                            diamond_data['diamond_weight'] = float(diamond.diamond_weight)

                        if str(diamond.diamond_rate_type.pk) == settings.PERCARAT:
                            diamond_data['diamond_rate'] = float(diamond.diamond_rate)/5

                        else:
                            diamond_data['diamond_rate'] = float(diamond.diamond_rate)

                        diamond_details.append(diamond_data)

                    tag_details['diamond_details']=diamond_details

                    particulars.append(tag_details)
               
                approval_details['tag_item_details']=particulars
                
                res_data.append(approval_details)
                return Response(
                {
                    "data":approval_details,
                    "message" : res_msg.retrieve("Approval Issue details"),
                    "status": status.HTTP_200_OK
                }, status=status.HTTP_200_OK
                )  
            else:
                return Response(
                {
                    "message" : res_msg.not_exists("Approval Issue details"),
                    "status": status.HTTP_200_OK
                }, status=status.HTTP_200_OK
            )  
            
        except Exception as err:
            return Response(
                {
                    "data":str(err),
                    "message" : res_msg.something_else(),
                    "status": status.HTTP_204_NO_CONTENT,                        
                }, status=status.HTTP_200_OK
        )  



@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class StockLedgerList(APIView):
    
    def post(self,request):

        filter_condition = {}
        
        if request.user.role.is_admin == True:
            branch = request.data.get('branch')
        else:
            branch = request.user.branch.pk

        stock_type = request.data.get('stock_type',None)
        metal = request.data.get('metal',None)
        purity = request.data.get('purity',None)
        item = request.data.get('item',None)
        sub_item = request.data.get('sub_item',None)
        vendor = request.data.get('vendor',None)
        search = request.data.get('search',"")
        from_date = request.data.get('from_date',None)
        to_date = request.data.get('to_date',None)
        page = request.data.get('page',1)
        items_per_page = request.data.get('items_per_page',10)
        
        if branch != None:
            
            filter_condition['tag_details__branch'] = branch
        
        if metal != None:
            
            filter_condition['tag_details__sub_item_details__item_details__purity__metal'] = metal
        
        if purity != None:
            
            filter_condition['tag_details__sub_item_details__item_details__purity'] = purity
        
        if item != None:
            
            filter_condition['tag_details__sub_item_details__item_details'] = item
        
        if sub_item != None:
            
            filter_condition['tag_details__sub_item_details'] = sub_item
        
        if vendor != None:
            
            filter_condition['tag_details__tag_entry_details__lot_details__designer_name'] = vendor
            
        if from_date != None and to_date != None:
            
            date_range = (from_date,to_date)
            
            filter_condition['entry_date__range'] = date_range
        
        if len(filter_condition) != 0:
            
            calculation_queryset = StockLedger.objects.filter(**filter_condition).order_by('-id')
           
        else:
            calculation_queryset = StockLedger.objects.all().order_by('-id')
            
        in_stock_pieces = 0
        in_stock_gross_weight = 0.0
        
        out_stock_pieces = 0
        out_stock_gross_weight = 0.0
        
        for tags in calculation_queryset:
            
            if tags.stock_type == settings.IN:
                
                in_stock_pieces += tags.pieces
                in_stock_gross_weight += tags.gross_weight
                
            else:
                
                out_stock_pieces += tags.pieces
                out_stock_gross_weight += tags.gross_weight
        
        if search != "":
            
            filter_condition['tag_details__tag_number__icontains'] = search
            
        if stock_type != None:
            
            filter_condition['stock_type'] = stock_type

            
        if len(filter_condition) != 0:
            
            queryset = StockLedger.objects.filter(**filter_condition).order_by('-id')
            
        else:
            queryset = StockLedger.objects.all().order_by('-id')
            
        paginated_data = Paginator(queryset, items_per_page)
        serializer = StockLedgerSerializer(paginated_data.get_page(page), many=True)
        total_items = len(queryset)
        
        response_data = []
        
        for data in serializer.data:
            
            ledger_queryset = StockLedger.objects.get(id=data['id'])
            
            res_data = data
            
            res_data['tag_number'] = ledger_queryset.tag_details.tag_number
            res_data['metal'] = ledger_queryset.tag_details.sub_item_details.item_details.purity.metal.metal_name
            res_data['purity'] = ledger_queryset.tag_details.sub_item_details.item_details.purity.purity_name
            res_data['item'] = ledger_queryset.tag_details.sub_item_details.item_details.item_name
            res_data['sub_item'] = ledger_queryset.tag_details.sub_item_details.sub_item_name
            res_data['vendor'] = ledger_queryset.tag_details.tag_entry_details.lot_details.designer_name.account_head_name
            res_data['stock_ledger_name'] = ledger_queryset.stock_type.stock_ledger_type
            
            response_data.append(res_data)
            
        return Response(
            {
                "data":{
                    "list":response_data,
                    "in_stock_pieces":in_stock_pieces,
                    "in_stock_gross_weight":in_stock_gross_weight,
                    "out_stock_pieces":out_stock_pieces,
                    "out_stock_gross_weight":out_stock_gross_weight,
                    "total_pages": paginated_data.num_pages,
                    "current_page": page,
                    "total_items": total_items,
                    "current_items": len(serializer.data)
                },
                "message":res_msg.retrieve("Stock Ledger Table List"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
        


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class StockLedgerTypeList(APIView):
    
    def get(self,request):

        queryset = StockLedger.objects.all().order_by('-id')

        serializer = StockLedgerSerializer(queryset,many=True)

        return Response(
            {
                "data":{
                    "list":serializer.data
                },
                "message":res_msg.retrieve("Stock Ledger Type List"),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
        


