
from portal.models import ContractorUser, Region, BusinessHub
from .models import contract_applicationpub
from django.contrib.auth.models import Group
from rest_framework import serializers
# from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail
from django.conf import settings

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
    


class UserFieldSerializer(serializers.ModelSerializer):
    class Meta:
       model=ContractorUser
       fields= ("first_name", "last_name","job_title", "role", "tel_no", "email", "region")

class EmailSerializer(serializers.ModelSerializer):
    class Meta:
       model=ContractorUser
       fields= ("email","role")

class ContractorUserSerializer(serializers.ModelSerializer):
    class Meta:
       model=ContractorUser
       fields="__all__"

class ContractorUserPlusEmailSerializer(serializers.ModelSerializer):
    class Meta:
       model=ContractorUser
       fields="__all__"

    def update(self, instance, validated_data):
        # instance.model_method() # call model method for instance level computation
        subject='Contractor Updated Profile and Awaiting Approval'
        message='''Hi CTO, 
        A Contractor, {} has just submitted his profile for approval. Kindly login to the platform to review pending approvals on the Awaiting Approval tab for Contractors.Click "https://ncp.ibedc.com" to visit the platform.'''.format(self.data.get('contractor_name'))
        email = []
        cto_emails = EmailSerializer(ContractorUser.objects.filter(is_cto=True), many=True).data
        # print(cto_emails)
        
        for val in cto_emails:
            email.append(list(val.items())[0][1])
    
        print(email)
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            email,
            fail_silently=False,
        )
        # call super to now save modified instance along with the validated data
        return super().update(instance, validated_data)  

class ContractorUserunsubmitSerializer(serializers.ModelSerializer):
    class Meta:
       model=ContractorUser
       fields="__all__"

    


class ContractorApprovalStatusSerializer(serializers.ModelSerializer):
    class Meta:
       model=ContractorUser
       fields= ("id","registration_approved", "is_contractor", "in_approval_workflow")


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
        model=contract_applicationpub
        fields="__all__"
        

class contract_applicationSerializer(serializers.ModelSerializer):

    class Meta:
        model=contract_applicationpub
        fields="__all__"
    

class contract_applicationListSerializer(serializers.ModelSerializer):
    # letter_of_donation_dss = Base64ImageField(max_length =None, use_url=True, required=False)
    # coren_or_nemsa_competency = Base64ImageField(max_length =None, use_url=True, required=False)
    # nemsa_test_cert = Base64ImageField(max_length =None, use_url=True, required=False)
    # attach_document = Base64ImageField(max_length =None, use_url=True, required=False)
    # attach_document = Base64ImageField(max_length =None, use_url=True, required=False)
    contractor = UserFieldSerializer(read_only=True)
    class Meta:
        model=contract_applicationpub
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
    
    def update(self, instance, validated_data):

        if(validated_data['action'] == 'Approve'):
            if(validated_data['approval_role'] == 'cto'):
                #SEND MESSAGE AFTER CTO APPROVAL. Send to MDs to take next action
                subject='A Contractor ({}) is Awaiting your Approval'.format(self.data.get('contractor_name'))
                message='''Hi MD ,

                A new Contractor, {}  is currently at the MD approval stage and needs your approval. 
                Kindly login to the platform to review pending approvals on the Awaiting Approval tab for Contractors.

                Best Regards'''.format(self.data.get('contractor_name'))
                email = []
                md_emails = EmailSerializer(ContractorUser.objects.filter(is_md=True), many=True).data
                
                
                for val in md_emails:
                    email.append(list(val.items())[0][1])
                send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        email,
                        fail_silently=False,
                            )
            elif(validated_data['approval_role'] == 'md'):
                #SEND MESSAGE AFTER MD APPROVAL. Notify contractor of the approval
                subject='Your profile has been approved'
                message='''Hi {},

                Your profile has been approved. You can now create connections and perform other contractor related activities on the platform. Click "https://ncp.ibedc.com" to visit the platform.
                Best Regards'''.format(self.data.get('contractor_name'))
               
                send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        [self.data.get('email'),],
                        fail_silently=False,
                            )
            else:
                pass
        elif(validated_data['action']=='Decline'):
            #THE MESSAGE TO BE SENT FOR APPLICATION DECLINED
            subject='Your Application as a Contractor has been Decline'
            message='''Hi {},

            Your application as a Contractor has been declined. Action required... 
            Kindly resolve the reason for decline stated below and resubmit for approval. Click "https://ncp.ibedc.com" to visit the platform.

            Comment: {}

            Best Regards'''.format(self.data.get('contractor_name'), validated_data['declined_comment'])
            send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [self.data.get('email'),],
                    fail_silently=False,
                        )
        else:
            pass
        return super().update(instance, validated_data)  
    



class actioncontract_applicationSerializer(serializers.ModelSerializer):

    class Meta:
        model=contract_applicationpub
        fields="__all__"

    def update(self, instance, validated_data):
        # print(self.data.get('contractor'))
        contractormail = EmailSerializer(ContractorUser.objects.filter(id=self.data.get('contractor')), many=True).data
        
        
        contractoremail = []
        for val in contractormail:
            contractoremail.append(list(val.items())[0][1])
        if(validated_data['action'] == 'submitconnection'):
            #SEND MESSAGE AFTER CONNECTIONS IS SUBMITTED. Send to TM to take next action
            subject='A Connection Request ({}) is Awaiting your Review'.format(self.data.get('connectiontype'))
            message='''Hi ,

            A new Connection Request, {}  has been submitted and needs your attention. 
            Kindly login to the platform to review pending approvals on the Awaiting Approval tab for Connections.Click "https://ncp.ibedc.com" to visit the platform.

            Best Regards'''.format(self.data.get('connectiontype'))
            tmemail = []
            #tm_emails = EmailSerializer(ContractorUser.objects.filter(is_te=True), many=True).data
            tm_emails = EmailSerializer(ContractorUser.objects.filter(is_tm=True), many=True).data
            
            for val in tm_emails:
                tmemail.append(list(val.items())[0][1])
            send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    tmemail,
                    fail_silently=False,
                        )
        if(validated_data['action'] == 'precomreq'):
            #SEND MESSAGE AFTER REQUEST FOR PRECOMISSIONING. Send to TE to take next action
            subject='A Connection Request ({}) is Awaiting your Review'.format(self.data.get('connectiontype'))
            message='''Hi ,

            A new Connection Request, {}  is currently at the precommissioning stage and needs your attention. 
            Kindly login to the platform to review pending approvals on the Awaiting Approval tab for Connections.Click "https://ncp.ibedc.com" to visit the platform.

            Best Regards'''.format(self.data.get('connectiontype'))
            te2email = []
            te2_emails = EmailSerializer(ContractorUser.objects.filter(is_te=True), many=True).data
            
            
            for val in te2_emails:
                te2email.append(list(val.items())[0][1])
            send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    te2email,
                    fail_silently=False,
                        )
        if(validated_data['action'] == 'submitprecomreq'):
            #SEND MESSAGE AFTER COMMISSIONING TEST IS SUBMITTED. Send to HM to take next action
            subject='A Connection Request ({}) is Awaiting your Review'.format(self.data.get('connectiontype'))
            message='''Hi ,

            A new Connection Request, {}  is currently at the HM approval stage and needs your attention. 
            Kindly login to the platform to review pending approvals on the Awaiting Approval tab for Connections.Click "https://ncp.ibedc.com" to visit the platform.

            Best Regards'''.format(self.data.get('connectiontype'))
            hmemail = []
            hm_emails = EmailSerializer(ContractorUser.objects.filter(is_hm=True), many=True).data
            
            
            for val in hm_emails:
                hmemail.append(list(val.items())[0][1])
            send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    hmemail,
                    fail_silently=False,
                        )
            
        if(validated_data['action'] == 'Approve'):
            if(validated_data['approval_role'] == 'tm'):
                
                #SEND MESSAGE AFTER TM APPROVAL. Send to TE to evaluate
                subject='A Connection Request ({}) is Awaiting your Evaluation'.format(self.data.get('connectiontype'))
                message='''Hi ,

                A new Connection Request, {}  is currently at the NPD approval stage and needs your approval. 
                Kindly login to the platform to review pending approvals on the Awaiting Approval tab for Connections.Click "https://ncp.ibedc.com" to visit the platform.

                Best Regards'''.format(self.data.get('connectiontype'))
                teemail = []
                te_emails = EmailSerializer(ContractorUser.objects.filter(is_te=True), many=True).data
                
                
                for val in te_emails:
                    teemail.append(list(val.items())[0][1])
                send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        teemail,
                        fail_silently=False,
                            )
            elif(validated_data['approval_role'] == 'te'):
                
                #SEND MESSAGE AFTER TE Evaluation. Send to NPD to take next action
                subject='A Connection Request ({}) is Awaiting your Approval'.format(self.data.get('connectiontype'))
                message='''Hi ,

                A new Connection Request, {}  is currently at the NPD approval stage and needs your approval. 
                Kindly login to the platform to review pending approvals on the Awaiting Approval tab for Connections.Click "https://ncp.ibedc.com" to visit the platform.

                Best Regards'''.format(self.data.get('connectiontype'))
                npdemail = []
                npd_emails = EmailSerializer(ContractorUser.objects.filter(is_npd=True), many=True).data
                
                
                for val in npd_emails:
                    npdemail.append(list(val.items())[0][1])
                send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        npdemail,
                        fail_silently=False,
                            )
            elif(validated_data['approval_role'] == 'npd'):
                #SEND MESSAGE AFTER NPD APPROVAL. Send to CTO to take next action
                subject='A Connection Request ({}) is Awaiting your Approval'.format(self.data.get('connectiontype'))
                message='''Hi ,

                A new Connection Request, {}  is currently at the CTO approval stage and needs your approval. 
                Kindly login to the platform to review pending approvals on the Awaiting Approval tab for Connections.Click "https://ncp.ibedc.com" to visit the platform.

                Best Regards'''.format(self.data.get('connectiontype'))
                ctoemail = []
                cto_emails = EmailSerializer(ContractorUser.objects.filter(is_cto=True), many=True).data
                
                
                for val in cto_emails:
                    ctoemail.append(list(val.items())[0][1])
                send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        ctoemail,
                        fail_silently=False,
                            )

            elif(validated_data['approval_role'] == 'cto'):
                subject = 'A Connection Request ({}) is Awaiting your Approval'.format(self.data.get('connectiontype'))
                message = '''
            Hi,

            A new Connection Request, {} is currently at the HSE approval stage and needs your approval.
            Kindly log in to the platform to review pending approvals on the Awaiting Approval tab for Connections. Click "https://ncp.ibedc.com" to visit the platform.

            Best Regards
            '''.format(self.data.get('connectiontype'))

                hsemail = [val['email'] for val in EmailSerializer(ContractorUser.objects.filter(is_hse=True), many=True).data]

                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    hsemail,
                    fail_silently=False,
                )
                
            elif validated_data['approval_role'] == 'hse':
                #SEND MESSAGE AFTER CTO APPROVAL. Send to Contractor to Request Precommissioning
                subject='Your Connection Request ({}) is at Precomissioning Stage. Action required.'.format(self.data.get('connectiontype'))
                message='''Hi ,

                Your Connection Request, {}  is currently at the Precomissioning Stage.
                Kindly login to your dashboard, and request precommissioning test for the connection.Click "https://ncp.ibedc.com" to visit the platform.
                
                Best Regards'''.format(self.data.get('connectiontype'))
                
                
                send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        contractoremail,
                        fail_silently=False,
                            )
            elif validated_data['approval_role'] == 'hbo':
                subject = 'A Connection Request ({}) is Awaiting your Approval'.format(self.data.get('connectiontype'))
                message = '''
            Hi,

            A new Connection Request, {} is currently at the HBO approval stage and needs your approval.
            Kindly log in to the platform to review pending approvals on the Awaiting Approval tab for Connections. Click "https://ncp.ibedc.com" to visit the platform.

            Best Regards
            '''.format(self.data.get('connectiontype'))

                hmemail = [val['email'] for val in EmailSerializer(ContractorUser.objects.filter(is_hm=True), many=True).data]

                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    hmemail,
                    fail_silently=False,
                )
            elif(validated_data['approval_role'] == 'hm'):
                #SEND MESSAGE AFTER HM APPROVAL. Send to Contractor
                subject='Your Connection Request ({}) Approval Process is Completed'.format(self.data.get('connectiontype'))
                message='''Hi ,

                Your Connection Request, {}  approval has been completed. Click "https://ncp.ibedc.com" to visit the platform.
                
                Best Regards'''.format(self.data.get('connectiontype'))
                
                send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        contractoremail,
                        fail_silently=False,
                            )
                
            else:
                pass
        elif(validated_data['action']=='Decline'):
            #THE MESSAGE TO BE SENT FOR APPLICATION DECLINED
            subject='Your Connection Request has been Declined'
            message='''Hi,

            Your connection request - {} has been declined. Action required... 
            Kindly resolve the reason for decline stated below and resubmit for approval. Click "https://ncp.ibedc.com" to visit the platform.

            Comment: {}

            Best Regards'''.format(self.data.get('connectiontype'), validated_data['declined_comment'])
            send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    contractoremail,
                    fail_silently=False,
                        )
        else:
            pass
        return super().update(instance, validated_data)  
