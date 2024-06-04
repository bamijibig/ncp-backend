
# Create your views here.
from django.shortcuts import render
from .models import contract_applicationpub, ContractorUser,BusinessHub
from portal.models import Region
from .serializers import (
                  
                    contract_applicationComSerializer,
                    contract_applicationEvalSerializer,
                    contract_applicationPreSerializer,
                    contract_applicationSerializer,
                    contract_applicationTestSerializer,
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

class ApproveOrDeclineConnectionTE(generics.RetrieveUpdateDestroyAPIView):

    def get_queryset(self):
        queryset = contract_applicationpub.objects.filter(id=self.kwargs["pk"])
        return queryset
    permission_classes = [IsAuthenticated]
    serializer_class = contract_applicationEvalSerializer

class ApproveOrDeclineConnectionTEST(generics.RetrieveUpdateDestroyAPIView):

    def get_queryset(self):
        queryset = contract_applicationpub.objects.filter(id=self.kwargs["pk"])
        return queryset
    permission_classes = [IsAuthenticated]
    serializer_class = contract_applicationTestSerializer

class ApproveOrDeclineConnectionPRE(generics.RetrieveUpdateDestroyAPIView):

    def get_queryset(self):
        queryset = contract_applicationpub.objects.filter(id=self.kwargs["pk"])
        return queryset
    permission_classes = [IsAuthenticated]
    serializer_class = contract_applicationPreSerializer

class ApproveOrDeclineConnectionCOM(generics.RetrieveUpdateDestroyAPIView):

    def get_queryset(self):
        queryset = contract_applicationpub.objects.filter(id=self.kwargs["pk"])
        return queryset
    permission_classes = [IsAuthenticated]
    serializer_class = contract_applicationComSerializer
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

# class ApproveOrDeclineConnectionpub(generics.RetrieveUpdateDestroyAPIView):

#     def get_queryset(self):
#         queryset = contract_applicationpub.objects.filter(id=self.kwargs["pk"])
#         return queryset
#     permission_classes = [IsAuthenticated]
#     serializer_class = actioncontract_applicationSerializer
class ApprovalStatuspub(generics.RetrieveAPIView):

    def get_queryset(self):
        queryset = ContractorUser.objects.filter(id=self.kwargs["pk"])
        return queryset
    serializer_class = ContractorApprovalStatuspubSerializer

class ConnectionMyApprovalListpub(generics.ListAPIView):

    def get_queryset(self):
        if(self.request.user.is_tm == True):
            queryset = contract_applicationpub.objects.filter( tm_is_connection_approved=False, bh__region__technicalManager__id = self.request.user.id)
        elif(self.request.user.is_te == True):
            queryset = contract_applicationpub.objects.filter( tm_is_connection_approved=True, te_is_connection_approved = False, bh__technicalManager__id = self.request.user.id) | contract_applicationpub.objects.filter( tm_is_connection_approved=True, te_is_connection_approved = True, cto_is_connection_approved=True, ct_is_pre_requested = True, tept_is_connection_approved = False, bh__technicalManager__id = self.request.user.id)
        elif(self.request.user.is_npd == True):
            queryset = contract_applicationpub.objects.filter( npd_is_connection_approved=False, te_is_connection_approved = True)
        elif(self.request.user.is_cto == True):
            queryset = contract_applicationpub.objects.filter( npd_is_connection_approved=True, cto_is_connection_approved = False)
        # elif(self.request.user.is_hse == True):
        #     queryset = contract_applicationpub.objects.filter(declined = False, npd_is_connection_approved=True, te_is_connection_approved = True, cto_is_connection_approved = True, hse_is_connection_approved = False, tept_is_connection_approved = False)
        elif(self.request.user.is_bhm == True):
            queryset = contract_applicationpub.objects.filter( npd_is_connection_approved=True, te_is_connection_approved = True, tept_is_connection_approved = True, cto_is_connection_approved = True, bhm_is_connection_approved = False)
            
        elif(self.request.user.is_hbo == True):
            queryset = contract_applicationpub.objects.filter( npd_is_connection_approved=True, te_is_connection_approved = True, tept_is_connection_approved = True, cto_is_connection_approved = True, bhm_is_connection_approved = True, hbo_is_connection_approved = False)
            
        elif(self.request.user.is_hm == True):
            queryset = contract_applicationpub.objects.filter( cto_is_connection_approved=True, tept_is_connection_approved = True, hbo_is_connection_approved = True, hm_is_connection_approved = False)
              
        else:
            queryset = None
        return queryset
    permission_classes = [IsAuthenticated]
    serializer_class = contract_applicationViewSerializer


class ContractorConnectionPrecommisionpub(generics.ListAPIView):
    def get_queryset(self):
        queryset = contract_applicationpub.objects.filter(contractor=self.request.user.id, cto_is_connection_approved=True, ct_is_pre_requested = False)
        return queryset
    permission_classes = [IsAuthenticated]
    serializer_class = contract_applicationViewSerializer
class ContractorConnectioncommisionpub(generics.ListAPIView):
    def get_queryset(self):
        queryset = contract_applicationpub.objects.filter(contractor=self.request.user.id, cto_is_connection_approved=True, ct_is_pre_requested = True, hm_is_connection_approved = True,ct_is_done=False)
        return queryset
    permission_classes = [IsAuthenticated]
    serializer_class = contract_applicationViewSerializer



from django.utils.timezone import now
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import contract_applicationViewSerializer

class ApproveOrDeclineConnectionpub(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = contract_applicationViewSerializer

    def get_queryset(self):
        return contract_applicationpub.objects.filter(id=self.kwargs["pk"])

    def patch(self, request, *args, **kwargs):
        connection = self.get_object()
        data = request.data
        action = data.get('action')
        user = request.user

        if action == 'Approve':
            if user.is_tm:
                connection.approval_role = 'tm'
                connection.tm_is_connection_approved = True
                connection.tm_is_connection_approved_date = now().strftime('%Y-%m-%d')
                connection.tm_is_connection_approved_by = f"{user.first_name} {user.last_name}"
                connection.connection_status = 'Approved By TM. Awaiting TE Evaluation'
                connection.tm_memo = data.get('memo')
            
            if user.is_npd:
                connection.approval_role = 'npd'
                connection.npd_is_connection_approved = True
                connection.npd_is_connection_approved_date = now().strftime('%Y-%m-%d')
                connection.npd_is_connection_approved_by = f"{user.first_name} {user.last_name}"
                connection.connection_status = 'Approved By NP & D. Awaiting Induction & CTO Approval'
                connection.npd_memo = data.get('memo')

            if user.is_cto:
                connection.approval_role = 'cto'
                connection.cto_is_connection_approved = True
                connection.cto_is_connection_approved_date = now().strftime('%Y-%m-%d')
                connection.cto_is_connection_approved_by = f"{user.first_name} {user.last_name}"
                connection.connection_status = 'Awaiting contractor Precomission request'
                connection.in_approval_workflow = False
                connection.connection_approved = True
                connection.cto_memo = data.get('memo')

            if user.is_bhm:
                connection.approval_role = 'bhm'
                connection.bhm_is_connection_approved = True
                connection.bhm_is_contractor_approved_date = now().strftime('%Y-%m-%d')
                connection.bhm_approved_by = f"{user.first_name} {user.last_name}"
                connection.connection_status = 'Awaiting Head Billing Approval'
                connection.in_approval_workflow = False
                connection.connection_approved = True
                connection.bhm_memo = data.get('memo')

            if user.is_hbo:
                connection.approval_role = 'hbo'
                connection.hbo_is_connection_approved = True
                connection.hbo_is_contractor_approved_date = now().strftime('%Y-%m-%d')
                connection.hbo_approved_by = f"{user.first_name} {user.last_name}"
                connection.connection_status = 'Awaiting Head Metering Approval'
                connection.in_approval_workflow = False
                connection.connection_approved = True
                connection.hbo_memo = data.get('memo')

            if user.is_hm:
                connection.approval_role = 'hm'
                connection.hm_is_connection_approved = True
                connection.hm_is_contractor_approved_date = now().strftime('%Y-%m-%d')
                connection.hm_approved_by = f"{user.first_name} {user.last_name}"
                connection.connection_status = 'Connection Approval Completed awaiting document'
                connection.in_approval_workflow = False
                connection.connection_approved = True
                connection.hm_memo = data.get('memo')

        elif action == 'Decline':
            connection.declined = True
            connection.in_approval_workflow = True
            connection.declined_comment = data.get('comment')

            if user.is_tm:
                connection.tm_memo = data.get('memo')

            if user.is_npd:
                connection.npd_memo = data.get('memo')
                connection.connection_status = 'Connection Application Declined by NPD.'
                connection.te_is_connection_approved = False
                connection.te_is_connection_approved_date = None
                connection.te_is_connection_approved_by = ''
                connection.te_memo = ''
                connection.eval_title=''
                connection.eval_applicant=''
                connection.eval_dt=''
                connection.eval_voltage_level=''
                connection.eval_estimated_load=''
                connection.eval_site_visit_date=''
                connection.eval_conworkdone=''
                connection.eval_dtsubname=''
                connection.eval_comentoncon=''
                connection.eval_fdrname=''
                connection.eval_fdrcapacity=''
                connection.eval_fdrpload=''
                connection.eval_tilldate=''
                connection.eval_cumloada=''
                connection.eval_srcfeeder=''
                connection.eval_ptrsf=''
                connection.eval_trsfrating=''
                connection.eval_trendpeak=''
                connection.eval_trendpeak=''
                connection.eval_cumtilldate=''
                connection.eval_permload=''
                connection.eval_maravail=''
                connection.eval_fulspons=''
                connection.eval_estpcost=''
                connection.eval_specoment=''
                connection.eval_preamble=''
                connection.eval_findings=''
                connection.eval_scopework=''
                connection.eval_recom=''
                connection.eval_pcm=''
                connection.eval_sglinediagram=''
                connection.eval_otherdoc=''

            if user.is_cto:
                connection.cto_memo = data.get('memo')
                connection.npd_is_connection_approved = False
                connection.npd_is_connection_approved_date = None
                connection.npd_is_connection_approved_by = ''
                connection.connection_status = 'Declined by CTO. Awaiting NPD to act on it'
                connection.npd_memo = ''

            if user.is_bhm:
                connection.bhm_memo = data.get('memo')
                # Resetting BHM's own approval instead of CTO's
                connection.bhm_is_connection_approved = False
                connection.bhm_is_contractor_approved_date = None
                connection.bhm_approved_by = ''
                connection.connection_status = 'Declined by BHM. Reverting to BHM for further action'
                connection.bhm_memo = ''

            if user.is_hbo:
                connection.hbo_memo = data.get('memo')
                connection.bhm_is_connection_approved = False
                connection.bhm_is_contractor_approved_date = None
                connection.bhm_approved_by = ''
                connection.connection_status = 'Declined by HBO. Awaiting BHM to act on it'
                connection.bhm_memo = ''

            if user.is_hm:
                connection.hm_memo = data.get('memo')
                connection.hbo_is_connection_approved = False
                connection.hbo_is_contractor_approved_date = None
                connection.hbo_approved_by = ''
                connection.connection_status = 'Declined by HM. Awaiting HBO to act on it'
                connection.hbo_memo = ''

        connection.save()
        return JsonResponse({'status': 'success'})

    def handle_invalid_request(self):
        return JsonResponse({'status': 'invalid request'}, status=400)