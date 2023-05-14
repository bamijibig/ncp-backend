
# Create your views here.
from django.shortcuts import render
from .models import contract_application, ContractorUser, Region,BusinessHub
from .serializers import (
                    ContractorUserSerializer,
                    ContractorUserunsubmitSerializer, 
                    RegisterSerializer, 
                    RegionListSerializer, 
                    BusinessHubListSerializer, 
                    ActionContractorSerializer, 
                    contract_applicationSerializer,
                    # technicalEvaluationSerializer,
                    contract_applicationListSerializer, 
                    contract_applicationViewSerializer,
                    CreateUserSerializer, 
                    RegionSerializer, 
                    BusinessHubSerializer,
                    ContractorApprovalStatusSerializer,
                    ContractorUserPlusEmailSerializer
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


class contractor_regupdatesubmitview(generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        queryset=ContractorUser.objects.filter(id=self.kwargs["pk"])
        return queryset
    # queryset=ContractorUser.objects.all()
    serializer_class=ContractorUserPlusEmailSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['contractor_name', 'tel_no','email']
    search_fields = '__all__'
    ordering_fields = '__all__'

class contractor_regview(viewsets.ModelViewSet):
    queryset=ContractorUser.objects.all()
    serializer_class=ContractorUserSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['contractor_name', 'tel_no','email']
    search_fields = '__all__'
    ordering_fields = '__all__'

class ConnectionContractorView(generics.ListAPIView):
    def get_queryset(self):
        queryset = contract_application.objects.filter(contractor=self.request.user.id)
        return queryset
    serializer_class=contract_applicationViewSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['connectiontype', 'est_load_of_premises','useofpremises','date_of_application']
    search_fields = '__all__'
    ordering_fields = '__all__'

class ConnectionStaffView(generics.ListAPIView):
    def get_queryset(self):

        if(self.request.user.staff_type == 'regionstaff'):
            queryset = contract_application.objects.filter(bh__region__id = self.request.user.region)
        elif(self.request.user.staff_type == 'businesshubstaff'):
            queryset = contract_application.objects.filter(bh__id = self.request.user.businesshub)
        else:
            queryset = contract_application.objects.all()
        return queryset
    permission_classes = [IsAuthenticated]
    serializer_class=contract_applicationViewSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['connectiontype', 'est_load_of_premises','useofpremises','date_of_application']
    search_fields = '__all__'
    ordering_fields = '__all__'

class ConnectionView(viewsets.ModelViewSet):
    queryset=contract_application.objects.all()
    serializer_class=contract_applicationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['connectiontype', 'est_load_of_premises','useofpremises','date_of_application']
    search_fields = '__all__'
    ordering_fields = '__all__'

class contractStaffListOnlyview(viewsets.ModelViewSet):
    queryset=contract_application.objects.all()
    serializer_class=contract_applicationListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['connectiontype', 'est_load_of_premises','useofpremises','date_of_application']
    search_fields = '__all__'
    ordering_fields = '__all__'

# class technicalview(viewsets.ModelViewSet):
#     queryset=technicalEvaluation.objects.all()
#     serializer_class=technicalEvaluationSerializer
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
#     filterset_fields = ['load_demand', 'equipment_sizing']
#     search_fields = '__all__'
#     ordering_fields = '__all__'

class RegisterView(generics.CreateAPIView):
    queryset = ContractorUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class UserList(generics.ListAPIView):
    queryset = ContractorUser.objects.filter(is_contractor=False)
    permission_classes = []
    serializer_class = CreateUserSerializer

# class ContractorList(generics.ListAPIView):
#     queryset = ContractorUser.objects.filter(is_contractor=True)
#     permission_classes = []
#     serializer_class = ContractorUserSerializer
class ContractorList(generics.ListAPIView):
    queryset = ContractorUser.objects.filter(registration_approved=True,is_contractor=True)
    permission_classes = []
    serializer_class = ContractorUserSerializer

class ContractorListunsubmit(generics.ListAPIView):
    queryset = ContractorUser.objects.filter(registration_approved=False,is_contractor=True, registration_status__isnull=True)
    permission_classes = []
    serializer_class = ContractorUserunsubmitSerializer


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
        # if(self.request.user.is_hsch == True):
        #     queryset = ContractorUser.objects.filter(is_contractor=True, declined = False, hsch_is_contractor_approved=False)
        if(self.request.user.is_cto == True):
            queryset = ContractorUser.objects.filter(is_contractor=True, declined = False,  cto_is_contractor_approved=False)
            # email=self.request.user.is_cto.email
            # subject='CTO has approved this request'
            # message='The request have been approved by CTO and awaiting MD approval'
            # send_mail(
            #     subject,
            #     message,
            #     settings.DEFAULT_FROM_EMAIL,  # Sender email
            #     [email],  # Recipient email(s)
            #     fail_silently=False,
            # )


        elif(self.request.user.is_md == True):
            queryset = ContractorUser.objects.filter(is_contractor=True, declined = False,  cto_is_contractor_approved=True, md_is_contractor_approved=False)
        else:
            queryset = None
        #  for user in queryset:
        #     user_email = user.email
        #     subject = 'Notification Subject'
        #     message = 'Notification Message'
        #     send_mail(
        #         subject,
        #         message,
        #         settings.DEFAULT_FROM_EMAIL,  # Sender email
        #         [user_email],  # Recipient email(s)
        #         fail_silently=False,
        #     )
        return queryset
    permission_classes = [IsAuthenticated]
    serializer_class = ContractorUserSerializer

class ApproveOrDeclineContractor(generics.RetrieveUpdateDestroyAPIView):

    def get_queryset(self):
        queryset = ContractorUser.objects.filter(id=self.kwargs["pk"])
        return queryset
    permission_classes = [IsAuthenticated]
    serializer_class = ActionContractorSerializer
 

class ApproveOrDeclineConnection(generics.RetrieveUpdateDestroyAPIView):

    def get_queryset(self):
        queryset = contract_application.objects.filter(id=self.kwargs["pk"])
        return queryset
    permission_classes = [IsAuthenticated]
    serializer_class = contract_applicationSerializer

class ApprovalStatus(generics.RetrieveAPIView):

    def get_queryset(self):
        queryset = ContractorUser.objects.filter(id=self.kwargs["pk"])
        return queryset
    serializer_class = ContractorApprovalStatusSerializer


class ConnectionMyApprovalList(generics.ListAPIView):

    def get_queryset(self):
        # queryset = ContractorUser.objects.filter(is_contractor=True)
        if(self.request.user.is_tm == True):
            queryset = contract_application.objects.filter(declined = False, tm_is_connection_approved=False, bh__region__technicalManager__id = self.request.user.id)
        elif(self.request.user.is_te == True):
            queryset = contract_application.objects.filter(declined = False, tm_is_connection_approved=True, te_is_connection_approved = False, bh__technicalManager__id = self.request.user.id) | contract_application.objects.filter(declined = False, tm_is_connection_approved=True, te_is_connection_approved = True, cto_is_connection_approved=True, ct_is_pre_requested = True, tept_is_connection_approved = False, bh__technicalManager__id = self.request.user.id)
        elif(self.request.user.is_npd == True):
            queryset = contract_application.objects.filter(declined = False, npd_is_connection_approved=False, te_is_connection_approved = True)
        elif(self.request.user.is_cto == True):
            queryset = contract_application.objects.filter(declined = False, npd_is_connection_approved=True, cto_is_connection_approved = False)
        elif(self.request.user.is_hm == True):
            queryset = contract_application.objects.filter(declined = False, cto_is_connection_approved=True, tept_is_connection_approved = True, hm_is_connection_approved = False)
              
        else:
            queryset = None
        return queryset
    permission_classes = [IsAuthenticated]
    serializer_class = contract_applicationViewSerializer


class ContractorConnectionPrecommision(generics.ListAPIView):
    def get_queryset(self):
        queryset = contract_application.objects.filter(contractor=self.request.user.id, cto_is_connection_approved=True, ct_is_pre_requested = False)
        return queryset
    permission_classes = [IsAuthenticated]
    serializer_class = contract_applicationViewSerializer
