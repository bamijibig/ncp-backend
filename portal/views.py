
# Create your views here.
from django.shortcuts import render
from .models import contract_application, ContractorUser, technicalEvaluation
from .serializers import ContractorUserSerializer, contract_applicationSerializer,technicalEvaluationSerializer,contract_applicationListSerializer, CreateUserSerializer
from rest_framework import viewsets, generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from knox.models import AuthToken
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model, login, logout
from rest_framework import status
from rest_framework.response import Response


# Create your views here.
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


class UserCreate(generics.CreateAPIView):
    permission_classes = []
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
			'user': CreateUserSerializer(user).data,
			'token': AuthToken.objects.create(user)[1]
		})

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