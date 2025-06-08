from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.response import Response
from organizations.models import Staff
from .models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes, authentication_classes
from django.utils import timezone
from django.db.models import ProtectedError
from django.db.models import Q
from django.core.paginator import Paginator
from app_lib.response_messages import ResponseMessages
from accounts.serializer import UserSerializer
from accounts.models import *
from .serializer import *
from billing.models import BillingParticularDetails

res_msg = ResponseMessages()

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class FloorViewSet(viewsets.ViewSet):

    def create(self, request):

        data = request.data
        data['floor_name'] = data.get('floor_name').lower()
        data['created_at'] = timezone.now()
        data['created_by'] = request.user.id
        if request.user.role.is_admin == False:
           branch = request.user.branch.pk
        else:
           branch = data.get('branch')
        data['branch'] = branch
        try:
            queryset = Floor.objects.get(floor_name=data.get('floor_name').lower(), branch=branch)
            return Response({
                "message": res_msg.already_exists('Floor'),
                "status": status.HTTP_204_NO_CONTENT
            }, status=status.HTTP_200_OK)
        except:
            pass
        serializer = FloorSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": res_msg.create('Floor'),
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
            queryset = Floor.objects.get(id=pk)
        except Exception as err:
            return Response({
                "message": res_msg.not_exists('Floor'),
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_200_OK)
        
        data = request.data
        data['floor_name'] = data.get('floor_name').lower()
        data['modified_at'] = timezone.now()
        data['modified_by'] = request.user.id
        if request.user.role.is_admin == False:
           branch = request.user.branch.pk
        else:
           branch = data.get('branch')
        data['branch'] = branch
        try:
            queryset = Floor.objects.exclude(id=pk).get(floor_name=data.get('floor_name').lower(), branch=branch)
            return Response({
                "message": res_msg.already_exists('Floor'),
                "status": status.HTTP_204_NO_CONTENT
            }, status=status.HTTP_200_OK)
        except:
            pass

        serializer = FloorSerializer(queryset, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": res_msg.update('Floor'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        return Response({
                "data": serializer.errors,
                "message": res_msg.in_valid_fields(),
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_200_OK)
        
    def destroy(self, request, pk):
        try:
            queryset = Floor.objects.get(id=pk)
            queryset.delete()
            return Response({
                "message": res_msg.delete('Floor'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        except Floor.DoesNotExist:
            return Response({
                "message": res_msg.not_exists('Floor'),
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
class FloorList(APIView):

    def get(self, request, branch=None):

        filter_condition={}
        if request.user.role.is_admin == True:
            if branch != None:            
                filter_condition['branch'] = branch
        else:
            filter_condition['branch'] = request.user.branch.pk
            
        filter_condition['is_active'] = True 

        queryset = list(Floor.objects.filter(**filter_condition).order_by('id'))
      
        serializer = FloorSerializer(queryset, many=True)

        res_data = []

        for i in range(0, len(serializer.data)):
            dict_data = serializer.data[i]
            dict_data['branch_name'] = queryset[i].branch.branch_name

            res_data.append(dict_data)

        return Response({
            "data": {
                "list": res_data,
            },
            "message": res_msg.retrieve('Floor'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
    
    def post(self, request):

        search = request.data.get('search') if request.data.get('search') else ''
        from_date = request.data.get('from_date') if request.data.get('from_date') else None
        to_date = request.data.get('to_date') if request.data.get('to_date') else None
        active_status = request.data.get('active_status') if request.data.get('active_status') != None else None
        page = request.data.get('page') if request.data.get('page') else 1
        items_per_page = request.data.get('items_per_page') if request.data.get('items_per_page') else 10
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
        
        # try:
        #     items_per_page = int(request.data.get('items_per_page', Floor.objects.all().count()))
        #     if items_per_page == 0:
        #         items_per_page = 10 
        # except Exception as err:
        #     items_per_page = 10 

        if len(filter_condition) != 0:
           queryset = list(Floor.objects.filter(Q(floor_name__icontains=search)|Q(branch__branch_name__icontains=search),**filter_condition).order_by('id'))
        elif search != '':
           queryset = list(Floor.objects.filter(Q(floor_name__icontains=search)|Q(branch__branch_name__icontains=search)).order_by('id'))
        else:
           queryset=list(Floor.objects.all().order_by('id'))

        paginated_data = Paginator(queryset, items_per_page)
        serializer = FloorSerializer(paginated_data.get_page(page), many=True)

        res_data = []

        for i in range(0, len(serializer.data)):
            dict_data = serializer.data[i]
            try :
                staff = Staff.objects.get(user =queryset[i].created_by_id)
                username = staff.first_name
            except:
                username = "-"
            dict_data['branch_name'] = queryset[i].branch.branch_name
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
            "message": res_msg.retrieve('Floor'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class FloorStatus(APIView):

    def get(self, request, pk=None, active=None):

        try:

            floor_queryset=Floor.objects.get(id=pk)

            if not(floor_queryset.is_active)==True:

                branch_queryset=Branch.objects.get(id=floor_queryset.branch.pk)

                if branch_queryset.is_active==False:

                    return Response(
                        {
                            "message":"Please activate the "+branch_queryset.branch_name+"branch",
                            "status":status.HTTP_200_OK
                        },status=status.HTTP_200_OK
                    )
                else:
                    floor_queryset.is_active=not(floor_queryset.is_active)
                    floor_queryset.save()

                    counter_queryset=Counter.objects.filter(floor=floor_queryset.pk)

                    for data in counter_queryset:

                        data.is_active=floor_queryset.is_active
                        data.save()

                    serializer=FloorSerializer(floor_queryset)

                    return Response(
                        {
                            "data":serializer.data,
                            "message":res_msg.change("Floor Status"),
                            "status":status.HTTP_200_OK
                        },status=status.HTTP_200_OK
                    )
                
            else:

                floor_queryset.is_active=not(floor_queryset.is_active)
                floor_queryset.save()

                counter_queryset=Counter.objects.filter(floor=floor_queryset.pk)
                for data in counter_queryset:

                    data.is_active=floor_queryset.is_active
                    data.save()

                    serializer=FloorSerializer(floor_queryset)


                serializer=FloorSerializer(floor_queryset)

                return Response(
                    {
                        "data":serializer.data,
                        "message":res_msg.change("Floor Status"),
                        "status":status.HTTP_200_OK
                    },status=status.HTTP_200_OK
                )

        except Floor.DoesNotExist:

            return Response(
                {
                    "message":res_msg.not_exists("Floor"),
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
class CounterViewSet(viewsets.ViewSet):

    def create(self, request):

        data = request.data
        data['counter_name'] = data.get('counter_name').lower()
        data['created_at'] = timezone.now()
        data['created_by'] = request.user.id
   
        if request.user.role.is_admin == False:
           branch = request.user.branch_id
        else:
           branch = data.get('branch')
        data['branch'] = branch

        try:
            queryset = Counter.objects.get(counter_name=data.get('counter_name').lower(), branch=branch, floor=data.get('floor'))
            return Response({
                "message": res_msg.already_exists('Counter'),
                "status": status.HTTP_204_NO_CONTENT
            }, status=status.HTTP_200_OK)
        except:
            pass
        serializer = CounterSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": res_msg.create('Counter'),
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
            queryset = Counter.objects.get(id=pk)
        except Exception as err:
            return Response({
                "message": res_msg.not_exists('Counter'),
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_200_OK)
        
        data = request.data
        data['counter_name'] = data.get('counter_name').lower()
        data['modified_at'] = timezone.now()
        data['modified_by'] = request.user.id
        if request.user.role.is_admin == False:
           branch = request.user.branch.pk
        else:
           branch = data.get('branch')
        data['branch'] = branch
        try:
            queryset = Counter.objects.exclude(id=pk).get(counter_name=data.get('counter_name').lower(), branch=branch, floor=data.get('floor'))
            return Response({
                "message": res_msg.already_exists('Counter'),
                "status": status.HTTP_204_NO_CONTENT
            }, status=status.HTTP_200_OK)
        except:
            pass

        serializer = CounterSerializer(queryset, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": res_msg.update('Counter'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        return Response({
                "data": serializer.errors,
                "message": res_msg.in_valid_fields(),
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_200_OK)
    
    def destroy(self, request, pk):
        try:
            queryset = Counter.objects.get(id=pk)
            queryset.delete()
            return Response({
                "message": res_msg.delete('Counter'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        except Counter.DoesNotExist:
            return Response({
                "message": res_msg.not_exists('Counter'),
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
class CounterList(APIView):

    def get(self, request, branch=None):

        filter_condition={}
        if request.user.role.is_admin ==True:
            if branch != None:            
                filter_condition['branch'] = branch
        else:
            filter_condition['branch'] = request.user.branch_id
        
            
        filter_condition['is_active'] = True 
        queryset = list(Counter.objects.filter(**filter_condition).order_by('id'))
        serializer = CounterSerializer(queryset, many=True)

        res_data = []

        for i in range(0, len(serializer.data)):
            dict_data = serializer.data[i]
            dict_data['branch_name'] = queryset[i].branch.branch_name
            dict_data['floor_name'] = queryset[i].floor.floor_name

            res_data.append(dict_data)

        return Response({
            "data": {
                "list": res_data,
            },
            "message": res_msg.retrieve('Counter'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
    
    def post(self, request):

        search = request.data.get('search') if request.data.get('search') else ''
        from_date = request.data.get('from_date') if request.data.get('from_date') else None
        to_date = request.data.get('to_date') if request.data.get('to_date') else None
        active_status = request.data.get('active_status') if request.data.get('active_status') != None else None
        page = request.data.get('page') if request.data.get('page') else 1
        items_per_page = request.data.get('items_per_page') if request.data.get('items_per_page') else 10
        branch = request.data.get('branch') if request.data.get('branch') else None
        filter_condition={}
        if request.user.role.is_admin == True:
            if branch != None:            
                filter_condition['branch'] = branch
        else:
            filter_condition['branch'] = request.user.branch_id

        if active_status != None:
           filter_condition['is_active'] = active_status 

        if from_date != None and to_date!= None:
           fdate =from_date+'T00:00:00.899010+05:30'
           tdate =to_date+'T23:59:59.899010+05:30'
           date_range=(fdate,tdate)
           filter_condition['created_at__range']=date_range
        
        
        # try:
        #     items_per_page = int(request.data.get('items_per_page', Counter.objects.all().count()))
        #     if items_per_page == 0:
        #         items_per_page = 10 
        # except Exception as err:
        #     items_per_page = 10 
       
        if len(filter_condition) != 0 :
           queryset = list(Counter.objects.filter(Q(counter_name__icontains=search)|Q(floor__floor_name__icontains=search)|Q(branch__branch_name__icontains=search),**filter_condition).order_by('id'))
        elif search != '':
           queryset = list(Counter.objects.filter(Q(counter_name__icontains=search)|Q(floor__floor_name__icontains=search)|Q(branch__branch_name__icontains=search)).order_by('id'))
        else:
           queryset=list(Counter.objects.all().order_by('id'))



        paginated_data = Paginator(queryset, items_per_page)
        serializer = CounterSerializer(paginated_data.get_page(page), many=True)

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
            dict_data['floor_name'] = queryset[i].floor.floor_name

            res_data.append(dict_data)

        return Response({
            "data": {
                "list": res_data,
                "total_pages": paginated_data.num_pages,
                "current_page": page,
                "total_items": len(queryset),
                "current_items": len(serializer.data)
            },
            "message": res_msg.retrieve('Counter'),
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class CounterStatus(APIView):

    def get(self, request, pk=None, active=None):

        if pk != None:
            try:
                queryset = Counter.objects.get(id=pk)
            except Exception as err:
                return Response({
                    "message": res_msg.not_exists('Counter'),
                    "status": status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_200_OK)
            
            if not(queryset.is_active):
                try:
                    branch_queryset = Branch.objects.get(id=queryset.branch.pk, is_active=True)
                    pass
                except Branch.DoesNotExist:
                    return Response({
                        "message": res_msg.activate(queryset.branch.branch_name + ' branch'),
                        "status": status.HTTP_204_NO_CONTENT
                    }, status=status.HTTP_200_OK)
                
                try:
                    floor_queryset = Floor.objects.get(id=queryset.floor.pk, is_active=True)
                    pass
                except Floor.DoesNotExist:
                    return Response({
                        "message": res_msg.activate(queryset.floor.floor_name + ' floor'),
                        "status": status.HTTP_204_NO_CONTENT
                    }, status=status.HTTP_200_OK)
            
        queryset.is_active = active if active != None else not(queryset.is_active)
        queryset.save()

        serializer = CounterSerializer(queryset)


        if active != None:
            return

        return Response({
                "data": serializer.data,
                "message": res_msg.update('Counter status'),
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
    

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class CounterTargetView(viewsets.ViewSet):

    def create(self,request):

        request_data = request.data

        if request.user.role.is_admin == False :
            request_data['branch'] = request.user.branch.pk

        request_data['created_at'] =timezone.now()
        request_data['created_by'] =request.user.id

        serializer = CounterTargetSerializer(data=request_data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "data":serializer.data,
                    "message":res_msg.create("Counter Target"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        
        else:
            return Response(
                {
                    "data":serializer.errors,
                    "message":res_msg.not_create("Counter Target"),
                    "status":status.HTTP_200_OK
                }
            )
        
    def retrieve(self,request,pk):

        try:

            queryset = CounterTarget.objects.get(id=pk)

            serializer = CounterTargetSerializer(queryset)

            return Response(
                {
                    "data":serializer.data,
                    "message":res_msg.retrieve("Counter Target"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        except CounterTarget.DoesNotExist:
            return Response(
                {
                    "message":res_msg.retrieve("Counter Target"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        
    def destroy(self,request,pk):
        try:

            queryset = CounterTarget.objects.get(id=pk)

            queryset.delete()

            
            return Response(
                {
                    "message":res_msg.delete("Counter Target"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        except CounterTarget.DoesNotExist:
            return Response(
                {
                    "message":res_msg.retrieve("Counter Target"),
                    "status":status.HTTP_200_OK
                },status=status.HTTP_200_OK
            )
        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class CounterTargetListView(APIView):

    def get(self,request):

        queryset = list(CounterTarget.objects.all().values('id','counter_details__counter_name','target_from_date','target_to_date','target_pieces','target_weight','target_amount').order_by('id'))

        return Response(
            {
                "data":{
                    "list":queryset
                },
                "message":res_msg.retrieve('Counter Target List'),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )
    
    def post(self,request):

        request_data = request.data

        branch = request_data.get('branch') if request_data.get('branch') else None
        counter = request_data.get('counter') if request_data.get('counter') else None
        page = request.data.get('page') if request.data.get('page') else None
        items_per_page = request.data.get('items_per_page') if request.data.get('items_per_page') else None

        filter_condition = {}

        if request.user.role.is_admin == True:
            if branch != None :
                filter_condition['branch'] = branch

        else:

            filter_condition['branch'] = request.user.branch.pk

        if counter != None :
            filter_condition['counter_details'] = counter

        if len(filter_condition) != 0:

            queryset = CounterTarget.objects.filter(**filter_condition).order_by('id')

        else:

            queryset = CounterTarget.objects.all().order_by('id')

        if page != None and items_per_page != None:
            paginated_data = Paginator(queryset, items_per_page)
            serializer = CounterTargetSerializer(paginated_data.get_page(page), many=True)

        else:
            serializer = CounterTargetSerializer(queryset,many=True)

        
        response_data = []

        for data in serializer.data:
            res_data = {}

            target_queryset = CounterTarget.objects.get(id=data['id'])

            res_data['id'] = target_queryset.pk
            res_data['branch'] = target_queryset.branch.pk
            res_data['branch_name'] = target_queryset.branch.branch_name
            res_data['counter'] = target_queryset.counter_details.pk
            res_data['counter_name'] = target_queryset.counter_details.counter_name
            res_data['target_from_date'] = target_queryset.target_from_date
            res_data['target_to_date'] = target_queryset.target_to_date
            res_data['target_pieces'] = target_queryset.target_pieces
            res_data['target_weight'] = target_queryset.target_weight
            res_data['target_amount'] = target_queryset.target_amount
            res_data['created_at'] = target_queryset.created_at

            date_range = (data['target_from_date'],data['target_to_date'])

            bill_data_queryset = BillingTagItems.objects.filter(billing_tag_item__display_counter = data['counter_details'],billing_details__bill_date__range=date_range)

            achived_pieces = len(bill_data_queryset)
            achived_weight = 0
            achived_amount = 0

            for items in bill_data_queryset :

                achived_weight += items.gross_weight
                achived_amount += items.total_rate

            res_data['achived_pieces'] =achived_pieces
            res_data['achived_weight'] =achived_weight
            res_data['achived_amount'] =achived_amount
            
            remaining_pieces =res_data['target_pieces'] - res_data['achived_pieces']
            if remaining_pieces <= 0:
                res_data['remaining_pieces'] = 0
            else:
                res_data['remaining_pieces'] = remaining_pieces
            remaining_weight =res_data['target_weight'] - res_data['achived_weight']
            if remaining_weight <= 0:
                res_data['remaining_weight'] = 0

            else :
                res_data['remaining_weight'] = remaining_weight
            remaining_amount =res_data['target_amount'] - res_data['achived_amount']
            if remaining_amount <= 0:
                res_data['remaining_amount'] = 0

            else:
                res_data['remaining_amount'] = remaining_amount

           

            if res_data['achived_pieces'] == 0 and res_data['achived_weight'] == 0 and res_data['achived_amount'] == 0 :
                res_data['target_status'] = "Pending"
                res_data['status_colour'] = '#FBA834'

            elif res_data['achived_pieces'] >= 1 or res_data['achived_weight'] >= 1 or res_data['achived_amount'] >= 1 :
                res_data['target_status'] = "Partially Achived"
                res_data['status_colour'] = '#EADFB4'

            elif res_data['achived_pieces'] == res_data['target_pieces'] or res_data['achived_weight'] == res_data['target_weight'] or res_data['achived_amount'] == res_data['target_amount'] :
                res_data['target_status'] = 'Achived'
                res_data['status_colour'] = '#416D19'

            elif res_data['achived_pieces'] > res_data['target_pieces'] or res_data['achived_weight'] > res_data['target_weight'] or res_data['achived_amount'] > res_data['target_amount'] :
                res_data['target_status'] = 'Over Achived' 
                res_data['status_colour'] = '#E72929'

            response_data.append(res_data)

        return Response(
            {
                "data":{
                    "list":response_data
                },
                "message":res_msg.retrieve('Counter Target List'),
                "status":status.HTTP_200_OK
            },status=status.HTTP_200_OK
        )


        







