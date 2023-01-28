
from portal.models import contract_application,ContractorUser, Region, BusinessHub
from django.contrib.auth.models import Group
from rest_framework import serializers
# from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        if(extension == "jpeg" or extension == "jpg"):
            extension = "jpg"
        elif(extension == "png"):
            extension = "png"
        else:
            extension = extension
        # extension = "jpg" if  else extension

        return extension

class ContractorUserSerializer(serializers.ModelSerializer):
    class Meta:
       model=ContractorUser
       fields="__all__"

class ContractorUserunsubmitSerializer(serializers.ModelSerializer):
    class Meta:
       model=ContractorUser
       fields="__all__"

    


class ContractorApprovalStatusSerializer(serializers.ModelSerializer):
    class Meta:
       model=ContractorUser
       fields= ("id","registration_approved", "is_contractor", "in_approval_workflow")

class UserFieldSerializer(serializers.ModelSerializer):
    class Meta:
       model=ContractorUser
       fields= ("first_name", "last_name","job_title", "role", "tel_no", "email")

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
       model=Region
       fields="__all__"

class RegionListSerializer(serializers.ModelSerializer):
    regionManager = UserFieldSerializer()
    technicalManager = UserFieldSerializer()
    class Meta:
       model=Region
       fields="__all__"

class BusinessHubSerializer(serializers.ModelSerializer):
    class Meta:
       model=BusinessHub
       fields="__all__"

class BusinessHubListSerializer(serializers.ModelSerializer):
    region = RegionSerializer()
    hubManager = UserFieldSerializer()
    technicalManager = UserFieldSerializer()
    class Meta:
       model=BusinessHub
       fields="__all__"



class contract_applicationViewSerializer(serializers.ModelSerializer):
    bh = BusinessHubListSerializer()
    contractor = ContractorUserSerializer()
    class Meta:
        model=contract_application
        fields="__all__"
        

class contract_applicationSerializer(serializers.ModelSerializer):

    class Meta:
        model=contract_application
        fields="__all__"
        

class contract_applicationListSerializer(serializers.ModelSerializer):
    # letter_of_donation_dss = Base64ImageField(max_length =None, use_url=True, required=False)
    # coren_or_nemsa_competency = Base64ImageField(max_length =None, use_url=True, required=False)
    # nemsa_test_cert = Base64ImageField(max_length =None, use_url=True, required=False)
    # attach_document = Base64ImageField(max_length =None, use_url=True, required=False)
    # attach_document = Base64ImageField(max_length =None, use_url=True, required=False)
    contractor = UserFieldSerializer(read_only=True)
    class Meta:
        model=contract_application
        fields="__all__"

# class technicalEvaluationSerializer(serializers.ModelSerializer):
#     class Meta:
#        model=technicalEvaluation
#        fields="__all__"


class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContractorUser
        fields = "__all__"
        read_only_fields = ('id',)


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=ContractorUser.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = ContractorUser
        fields = "__all__"
        # extra_kwargs = {
        #     'first_name': {'required': True},
        #     'last_name': {'required': True}
        # }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = ContractorUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_contractor=validated_data['is_contractor'],
            is_admin=validated_data['is_admin'],
            is_tm = validated_data['is_tm'],
            is_te = validated_data['is_te'],
            is_hm = validated_data['is_hm'],
            is_npd = validated_data['is_npd'],
            is_cto = validated_data['is_cto'],
            is_md = validated_data['is_md'],
            is_hsch = validated_data['is_hsch'],
            job_title = validated_data['job_title'],
            role = validated_data['role'],
            tel_no = validated_data['tel_no']

        )

        
        user.set_password(validated_data['password'])
        user.save()

        return user

class updateContractorSerializers(serializers.ModelSerializer):
    # coren_or_nemsa_competency = Base64ImageField(max_length=None, use_url=True, required=False)
    class Meta:
        model = ContractorUser
        fields = "__all__"
        read_only_fields = ('id',)

class ActionContractorSerializer(serializers.ModelSerializer):
    class Meta:
       model=ContractorUser
       fields="__all__"
    