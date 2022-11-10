
from portal.models import contract_application, technicalEvaluation,ContractorUser
from django.contrib.auth.models import Group
from rest_framework import serializers


# class Base64ImageField(serializers.ImageField):
#     """
#     A Django REST framework field for handling image-uploads through raw post data.
#     It uses base64 for encoding and decoding the contents of the file.

#     Heavily based on
#     https://github.com/tomchristie/django-rest-framework/pull/1268

#     Updated for Django REST framework 3.
#     """

#     def to_internal_value(self, data):
#         from django.core.files.base import ContentFile
#         import base64
#         import six
#         import uuid

#         # Check if this is a base64 string
#         if isinstance(data, six.string_types):
#             # Check if the base64 string is in the "data:" format
#             if 'data:' in data and ';base64,' in data:
#                 # Break out the header from the base64 content
#                 header, data = data.split(';base64,')

#             # Try to decode the file. Return validation error if it fails.
#             try:
#                 decoded_file = base64.b64decode(data)
#             except TypeError:
#                 self.fail('invalid_image')

#             # Generate file name:
#             file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
#             # Get the file name extension:
#             file_extension = self.get_file_extension(file_name, decoded_file)

#             complete_file_name = "%s.%s" % (file_name, file_extension, )

#             data = ContentFile(decoded_file, name=complete_file_name)

#         return super(Base64ImageField, self).to_internal_value(data)

#     def get_file_extension(self, file_name, decoded_file):
#         import imghdr

#         extension = imghdr.what(file_name, decoded_file)
#         if(extension == "jpeg" or extension == "jpg"):
#             extension = "jpg"
#         elif(extension == "png"):
#             extension = "png"
#         else:
#             extension = extension
#         extension = "jpg" if  else extension

#         return extension


class ContractorUserSerializer(serializers.ModelSerializer):
    class Meta:
       model=ContractorUser
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
    contractor = ContractorUserSerializer(read_only=True)
    class Meta:
        model=contract_application
        fields="__all__"

class technicalEvaluationSerializer(serializers.ModelSerializer):
    class Meta:
       model=technicalEvaluation
       fields="__all__"


class CreateUserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    group = serializers.ChoiceField(choices=['SUPER-ADMIN','CONTRACTOR', 'PROCUREMENT','TE','TM'], allow_blank=False)# new
    
    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('Passwords must match.')
        return data

    def create(self, validated_data):
        group_data = validated_data.pop('group')
        group, _ = Group.objects.get_or_create(name=group_data)
        data = {
            key: value for key, value in validated_data.items()
            if key not in ('password1', 'password2')
        }
        data['password'] = validated_data['password1']
        user = self.Meta.model.objects.create_user(**data)
        user.groups.add(group)
        user.save()
      
        return user

    class Meta:
        model = ContractorUser
        fields = "__all__"
        
        # extra_kwargs = {"password": {"write_only": True}}
        read_only_fields = ('id',)