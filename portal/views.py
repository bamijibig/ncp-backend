
# Create your views here.
from django.shortcuts import render
from .models import contract_application, ContractorUser, technicalEvaluation, Region,BusinessHub
from .serializers import (
                    ContractorUserSerializer, 
                    RegisterSerializer, 
                    RegionListSerializer, 
                    BusinessHubListSerializer, 
                    ActionContractorSerializer, 
                    contract_applicationSerializer,
                    technicalEvaluationSerializer,
                    contract_applicationListSerializer, 
                    CreateUserSerializer, 
                    RegionSerializer, 
                    BusinessHubSerializer,
                    ContractorApprovalStatusSerializer
                    )
from rest_framework import viewsets, generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from knox.models import AuthToken
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model, login, logout
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly

# from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
# Create your views here.

class regionview(viewsets.ModelViewSet):
    queryset=Region.objects.all()
    serializer_class=RegionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = '__all__'
    search_fields = '__all__'
    ordering_fields = '__all__'

class regionlistview(viewsets.ModelViewSet):
    queryset=Region.objects.all()
    serializer_class=RegionListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = '__all__'
    search_fields = '__all__'
    ordering_fields = '__all__'
    http_method_names = ['get', 'options', 'head']

class businesshubview(viewsets.ModelViewSet):
    queryset=BusinessHub.objects.all()
    serializer_class=BusinessHubSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = '__all__'
    search_fields = '__all__'
    ordering_fields = '__all__'


class businesshublistview(viewsets.ModelViewSet):
    queryset=BusinessHub.objects.all()
    serializer_class=BusinessHubListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = '__all__'
    search_fields = '__all__'
    ordering_fields = '__all__'
    http_method_names = ['get', 'options', 'head']

class contractor_regview(viewsets.ModelViewSet):
    queryset=ContractorUser.objects.all()
    serializer_class=ContractorUserSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['contractor_name', 'tel_no','email']
    search_fields = '__all__'
    ordering_fields = '__all__'


class contractview(viewsets.ModelViewSet):
    queryset=contract_application.objects.all()
    serializer_class=contract_applicationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['connectiontype', 'est_load_of_premises','useofpremises','date_of_application']
    search_fields = '__all__'
    ordering_fields = '__all__'

class contractListOnlyview(viewsets.ModelViewSet):
    queryset=contract_application.objects.all()
    serializer_class=contract_applicationListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['connectiontype', 'est_load_of_premises','useofpremises','date_of_application']
    search_fields = '__all__'
    ordering_fields = '__all__'

class technicalview(viewsets.ModelViewSet):
    queryset=technicalEvaluation.objects.all()
    serializer_class=technicalEvaluationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['load_demand', 'equipment_sizing']
    search_fields = '__all__'
    ordering_fields = '__all__'

class RegisterView(generics.CreateAPIView):
    queryset = ContractorUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class UserList(generics.ListAPIView):
    queryset = ContractorUser.objects.filter(is_contractor=False)
    permission_classes = []
    serializer_class = CreateUserSerializer

class ContractorList(generics.ListAPIView):
    queryset = ContractorUser.objects.filter(is_contractor=True)
    permission_classes = []
    serializer_class = ContractorUserSerializer


# class ListUsers(APIView):

#     permission_classes = [IsAuthenticated]
#     serializer_class = ContractorUserSerializer

#     def get(self, request, format=None):
       
#         usernames = [user.username for user in User.objects.all()]
#         return Response(usernames)


class LoginView(APIView):
    permission_classes = []
    def post(self, request):
        form = AuthenticationForm(data=request.data)
        if form.is_valid():
            user = form.get_user()
            login(request, user=form.get_user())
            response = {"status_code": status.HTTP_200_OK,
                        "success": "true",
                        "message": "Successfully logged in",
                        "data": ContractorUserSerializer(user).data,
                        "token": AuthToken.objects.create(user)[1]
                        }
            return Response(response)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
            



#logout
class LogoutView(APIView):
    # permission_classes = (IsAuthenticated,)

    def post(self, *args, **kwargs):
        logout(self.request)
        response = {"status_code": status.HTTP_204_NO_CONTENT,
                        "success": "true",
                        "message": "Successfully logged out",
                        "data": ""}
        return Response(response)


class ContractorMyApprovalList(generics.ListAPIView):

    def get_queryset(self):
        # queryset = ContractorUser.objects.filter(is_contractor=True)
        if(self.request.user.is_hsch == True):
            queryset = ContractorUser.objects.filter(is_contractor=True, declined = False, hsch_is_contractor_approved=False)
        elif(self.request.user.is_cto == True):
            queryset = ContractorUser.objects.filter(is_contractor=True, declined = False, hsch_is_contractor_approved=True, cto_is_contractor_approved=False)
        elif(self.request.user.is_md == True):
            queryset = ContractorUser.objects.filter(is_contractor=True, declined = False, hsch_is_contractor_approved=True, cto_is_contractor_approved=True, md_is_contractor_approved=False)
        else:
            queryset = None
        return queryset
    permission_classes = [IsAuthenticated]
    serializer_class = ContractorUserSerializer


class ApproveOrDeclineContractor(generics.RetrieveUpdateDestroyAPIView):

    def get_queryset(self):
        queryset = ContractorUser.objects.filter(id=self.kwargs["pk"])
        return queryset
    permission_classes = [IsAuthenticated]
    serializer_class = ActionContractorSerializer

class ApprovalStatus(generics.RetrieveAPIView):

    def get_queryset(self):
        queryset = ContractorUser.objects.filter(id=self.kwargs["pk"])
        return queryset
    serializer_class = ContractorApprovalStatusSerializer
