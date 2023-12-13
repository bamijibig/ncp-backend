
# Create your views here.
from django.shortcuts import render
from .models import contract_applicationpub, ContractorUser,BusinessHub
from portal.models import Region
from .serializers import (
                  
                    contract_applicationSerializer,
                    # technicalEvaluationSerializer,
                     
                    contract_applicationViewSerializer,
                    
                    actioncontract_applicationSerializer,
                    ContractorApprovalStatuspubSerializer

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
from django.core.mail import send_mail
from django.conf import settings


class ConnectionContractorViewpub(generics.ListAPIView):
    def get_queryset(self):
        queryset = contract_applicationpub.objects.filter(contractor=self.request.user.id)
        return queryset
    serializer_class=contract_applicationViewSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # filterset_fields = ['connectiontype', 'est_load_of_premises','useofpremises','date_of_application']
    search_fields = '__all__'
    ordering_fields = '__all__' 
class ConnectionStaffViewpub(generics.ListAPIView):
    def get_queryset(self):

        if(self.request.user.staff_type == 'regionstaff'):
            queryset = contract_applicationpub.objects.filter(bh__region__id = self.request.user.region)
        elif(self.request.user.staff_type == 'businesshubstaff'):
            queryset = contract_applicationpub.objects.filter(bh__id = self.request.user.businesshub)
        else:
            queryset = contract_applicationpub.objects.all()
        return queryset
    permission_classes = [IsAuthenticated]
    serializer_class=contract_applicationViewSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # filterset_fields = ['connectiontype', 'est_load_of_premises','useofpremises','date_of_application']
    search_fields = '__all__'
    ordering_fields = '__all__'


class ConnectionViewpub(viewsets.ModelViewSet):
    queryset=contract_applicationpub.objects.all()
    serializer_class=contract_applicationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # filterset_fields = ['connectiontype', 'est_load_of_premises','useofpremises','date_of_application']
    search_fields = '__all__'
    ordering_fields = '__all__'

class ApproveOrDeclineConnectionpub(generics.RetrieveUpdateDestroyAPIView):

    def get_queryset(self):
        queryset = contract_applicationpub.objects.filter(id=self.kwargs["pk"])
        return queryset
    permission_classes = [IsAuthenticated]
    serializer_class = actioncontract_applicationSerializer
class ApprovalStatuspub(generics.RetrieveAPIView):

    def get_queryset(self):
        queryset = ContractorUser.objects.filter(id=self.kwargs["pk"])
        return queryset
    serializer_class = ContractorApprovalStatuspubSerializer

class ConnectionMyApprovalListpub(generics.ListAPIView):

    def get_queryset(self):
        if(self.request.user.is_tm == True):
            queryset = contract_applicationpub.objects.filter(declined = False, tm_is_connection_approved=False, bh__region__technicalManager__id = self.request.user.id)
        elif(self.request.user.is_te == True):
            queryset = contract_applicationpub.objects.filter(declined = False, tm_is_connection_approved=True, te_is_connection_approved = False, bh__technicalManager__id = self.request.user.id) | contract_applicationpub.objects.filter(declined = False, tm_is_connection_approved=True, te_is_connection_approved = True, cto_is_connection_approved=True, ct_is_pre_requested = True, tept_is_connection_approved = False, bh__technicalManager__id = self.request.user.id)
        elif(self.request.user.is_npd == True):
            queryset = contract_applicationpub.objects.filter(declined = False, npd_is_connection_approved=False, te_is_connection_approved = True)
        elif(self.request.user.is_cto == True):
            queryset = contract_applicationpub.objects.filter(declined = False, npd_is_connection_approved=True, cto_is_connection_approved = False)
        elif(self.request.user.is_hse == True):
            queryset = contract_applicationpub.objects.filter(declined = False, npd_is_connection_approved=True, te_is_connection_approved = True, cto_is_connection_approved = True, hse_is_connection_approved = False, tept_is_connection_approved = False)
        elif(self.request.user.is_hbo == True):
            queryset = contract_applicationpub.objects.filter(declined = False, npd_is_connection_approved=True, te_is_connection_approved = True, tept_is_connection_approved = True, cto_is_connection_approved = True,hse_is_connection_approved = True, hbo_is_connection_approved = False)
            
        elif(self.request.user.is_hm == True):
            queryset = contract_applicationpub.objects.filter(declined = False, cto_is_connection_approved=True, tept_is_connection_approved = True, hbo_is_connection_approved = True, hm_is_connection_approved = False)
              
        else:
            queryset = None
        return queryset
    permission_classes = [IsAuthenticated]
    serializer_class = contract_applicationViewSerializer


class ContractorConnectionPrecommisionpub(generics.ListAPIView):
    def get_queryset(self):
        queryset = contract_applicationpub.objects.filter(contractor=self.request.user.id, cto_is_connection_approved=True, hse_is_connection_approved = True, ct_is_pre_requested = False)
        return queryset
    permission_classes = [IsAuthenticated]
    serializer_class = contract_applicationViewSerializer
