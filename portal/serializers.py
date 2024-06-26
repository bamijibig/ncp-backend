
from datetime import date, datetime, timedelta
from portal.models import contract_application,ContractorUser, Region, BusinessHub
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
    
        #print(email)
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            email,
            fail_silently=False,
        )
        
        
        # call super to now save modified instance along with the validated data
        return super().update(instance, validated_data)  


# class ContractorUserPlusEmailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ContractorUser
#         fields = "__all__"

#     def update(self, instance, validated_data):
#         subject = 'Contractor Updated Profile and Awaiting Approval'
#         message = '''Hi CTO, 
# A Contractor, {} has just submitted his profile for approval. Kindly login to the platform to review pending approvals on the Awaiting Approval tab for Contractors. Click "https://ncp.ibedc.com" to visit the platform.'''.format(validated_data.get('contractor_name', ''))
        
#         # Fetch CTO emails
#         cto_emails = EmailSerializer(ContractorUser.objects.filter(is_cto=True), many=True).data
#         email = [val['email'] for val in cto_emails]
        
#         send_mail(
#             subject,
#             message,
#             settings.DEFAULT_FROM_EMAIL,
#             email,
#             fail_silently=False,
#         )

#         if validated_data.get('in_approval_workflow') and not validated_data.get('cto_is_contractor_approved') and validated_data.get('action') != 'decline':
#             reg_date = validated_data['date_joined']
#             if date.today() >= reg_date + timedelta(days=2):
#                 subject = 'A Reminder Contractor Updated Profile and Awaiting Approval'
#                 message = '''Hi CTO, 
# A Reminder Contractor, {} has just submitted his profile for approval. Kindly login to the platform to review pending approvals on the Awaiting Approval tab for Contractors. Click "https://ncp.ibedc.com" to visit the platform.'''.format(validated_data.get('contractor_name', ''))
                
#                 send_mail(
#                     subject,
#                     message,
#                     settings.DEFAULT_FROM_EMAIL,
#                     email,
#                     fail_silently=False,
#                 )

#         # Call super to now save modified instance along with the validated data
#         return super().update(instance, validated_data)

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


class contract_applicationEvalSerializer(serializers.ModelSerializer):
    class Meta:
        model=contract_application
        fields="__all__"
    def update(self, instance, validated_data):
        # instance.model_method() # call model method for instance level computation
        subject='npd has approved waiting for '
        message='''Hi N, 
        A Contractor, {} has just submitted his profile for approval. Kindly login to the platform to review pending approvals on the Awaiting Approval tab for Contractors.Click "https://ncp.ibedc.com" to visit the platform.'''.format(self.data.get('contractor_name'))
        npdmail = []
        npd_emails = EmailSerializer(ContractorUser.objects.filter(is_npd=True), many=True).data
        # print(cto_emails)
        
        for val in npd_emails:
            npdmail.append(list(val.items())[0][1])
    
        #print(email)
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            npdmail,
            fail_silently=False,
        )
        
        
        # call super to now save modified instance along with the validated data
        return super().update(instance, validated_data)

class contract_applicationPrecomSerializer(serializers.ModelSerializer):
    class Meta:
        model=contract_application
        fields="__all__"

    def update(self, instance, validated_data):
        # instance.model_method() # call model method for instance level computation
        subject='bhm has approved waiting for '
        message='''Hi N, 
        A Contractor, {} has just submitted his profile for approval. Kindly login to the platform to review pending approvals on the Awaiting Approval tab for Contractors.Click "https://ncp.ibedc.com" to visit the platform.'''.format(self.data.get('contractor_name'))
        temail = []
        te_emails = EmailSerializer(ContractorUser.objects.filter(is_te=True), many=True).data
        # print(cto_emails)
        
        for val in te_emails:
            temail.append(list(val.items())[0][1])
    
        #print(email)
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            temail,
            fail_silently=False,
        )
        
        
        # call super to now save modified instance along with the validated data
        return super().update(instance, validated_data)
class contract_applicationTestSerializer(serializers.ModelSerializer):
    class Meta:
        model=contract_application
        fields="__all__"
    def update(self, instance, validated_data):
        # instance.model_method() # call model method for instance level computation
        subject='bhm has approved waiting for '
        message='''Hi N, 
        A Contractor, {} has just submitted his profile for approval. Kindly login to the platform to review pending approvals on the Awaiting Approval tab for Contractors.Click "https://ncp.ibedc.com" to visit the platform.'''.format(self.data.get('contractor_name'))
        bhmmail = []
        bhm_emails = EmailSerializer(ContractorUser.objects.filter(is_bhm=True), many=True).data
        # print(cto_emails)
        
        for val in bhm_emails:
            bhmmail.append(list(val.items())[0][1])
    
        #print(email)
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            bhmmail,
            fail_silently=False,
        )
        return super().update(instance, validated_data)
class contract_applicationComSerializer(serializers.ModelSerializer):
    class Meta:
        model=contract_application
        fields="__all__"
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
            is_bhm = validated_data['is_bhm'],
            is_hbo = validated_data['is_hbo'],
            is_hse = validated_data['is_hse'],
            job_title = validated_data['job_title'],
            role = validated_data['role'],
            tel_no = validated_data['tel_no'],
            region = validated_data['region'],
            businesshub = validated_data['businesshub']

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
    
    def update(self, instance, validated_data):

        if(validated_data['action'] == 'Approve'):
            if(validated_data['approval_role'] == 'cto'):
                #SEND MESSAGE AFTER CTO APPROVAL. Send to MDs to take next action
                subject='A Notification for a New Contractor Registration ({})'.format(self.data.get('contractor_name'))
                message='''Hi MD ,

                A new Contractor, {}  just register on New Connection Portal 
                Kindly login to the platform to view the Contractor Registration.

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
        model=contract_application
        fields="__all__"

    def update(self, instance, validated_data):
        # print(self.data.get('contractor'))

        contractoremail = EmailSerializer(ContractorUser.objects.filter(id=self.data.get('contractor')), many=True).data
        tm_emails = EmailSerializer(ContractorUser.objects.filter(is_tm=True,region=str(self.data.get('bh__region'))), many=True).data
        # te2_emails = EmailSerializer(ContractorUser.objects.filter(is_te=True), many=True).data
        # hm_emails = EmailSerializer(ContractorUser.objects.filter(is_hm=True), many=True).data
        te_emails = EmailSerializer(ContractorUser.objects.filter(is_te=True, businesshub=str(self.data.get('bh'))), many=True).data
        npd_emails = EmailSerializer(ContractorUser.objects.filter(is_npd=True), many=True).data
        cto_emails = EmailSerializer(ContractorUser.objects.filter(is_cto=True), many=True).data
        hsemail = [val['email'] for val in EmailSerializer(ContractorUser.objects.filter(is_hse=True), many=True).data]
        bhmmail = EmailSerializer(ContractorUser.objects.filter(is_bhm=True, businesshub=str(self.data.get('bh'))), many=True).data
        hboemail = [val['email'] for val in EmailSerializer(ContractorUser.objects.filter(is_hbo=True), many=True).data]
        hmemail = [val['email'] for val in EmailSerializer(ContractorUser.objects.filter(is_hm=True), many=True).data]


        # contractoremail = []
        # for val in contractormail:
        #     contractoremail.append(list(val.items())[0][1])
        if(validated_data['action'] == 'submitconnection'):
            #SEND MESSAGE AFTER CONNECTIONS IS SUBMITTED. Send to TM to take next action
            subject='A Connection Request ({}) is Awaiting your Review'.format(self.data.get('connectiontype'))
            message='''Hi ,

            A new Connection Request, {}  has been submitted and needs your attention. 
            Kindly login to the platform to review pending approvals on the Awaiting Approval tab for Connections.Click "https://ncp.ibedc.com" to visit the platform.

            Best Regards'''.format(self.data.get('connectiontype'))

            

            tmemail = []
            #tm_emails = EmailSerializer(ContractorUser.objects.filter(is_te=True), many=True).data
            # tm_emails = EmailSerializer(ContractorUser.objects.filter(is_tm=True), many=True).data
            
            for val in tm_emails:
                tmemail.append(list(val.items())[0][1])
            
            #Send to tm
            send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    tmemail,
                    fail_silently=False,
                        )
            
            # notify others
            copyemails = []
            for val in cto_emails:
                    copyemails.append(list(val.items())[0][1])
            for val in npd_emails:
                    copyemails.append(list(val.items())[0][1])
            copymessage='''Hi ,

            A new Connection Request, {}  has been submitted and currently awaiting approval from the TM. 
    
            Best Regards'''.format(self.data.get('connectiontype'))
            send_mail(
                    subject,
                    copymessage,
                    settings.DEFAULT_FROM_EMAIL,
                    copyemails,
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
            # te2_emails = EmailSerializer(ContractorUser.objects.filter(is_te=True), many=True).data
            
            
            for val in te_emails:
                te2email.append(list(val.items())[0][1])
            send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    te2email,
                    fail_silently=False,
                        )
            # notify others
            copyemails = []
            for val in cto_emails:
                    copyemails.append(list(val.items())[0][1])
            for val in npd_emails:
                    copyemails.append(list(val.items())[0][1])
            copymessage='''Hi ,

            A new Connection Request, {}  has been submitted and currently awaiting approval from the TM. 
    
            Best Regards'''.format(self.data.get('connectiontype'))
            send_mail(
                    subject,
                    copymessage,
                    settings.DEFAULT_FROM_EMAIL,
                    copyemails,
                    fail_silently=False,
                        )
            # notify bhm
            bhm_emails = []
            for val in bhmmail:
                    bhm_emails.append(list(val.items())[0][1])
            
            copymessage='''Hi ,

            A new Connection Request, {}  has been submitted and currently awaiting your approval. 
    
            Best Regards'''.format(self.data.get('connectiontype'))
            send_mail(
                    subject,
                    copymessage,
                    settings.DEFAULT_FROM_EMAIL,
                    bhm_emails,
                    fail_silently=False,
                        )
        if(validated_data['action'] == 'submitprecomreq'):
            #SEND MESSAGE AFTER COMMISSIONING TEST IS SUBMITTED. Send to BHM to take next action
            subject='A Connection Request ({}) is Awaiting your Review'.format(self.data.get('connectiontype'))
            message='''Hi ,

            A new Connection Request, {}  is currently at the BHM approval stage and needs your attention. 
            Kindly login to the platform to review pending approvals on the Awaiting Approval tab for Connections.Click "https://ncp.ibedc.com" to visit the platform.

            Best Regards'''.format(self.data.get('connectiontype'))


            bhm_emails = []
            for val in bhmmail:
                    bhm_emails.append(list(val.items())[0][1])
            
            send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    bhm_emails,
                    fail_silently=False,
                        )


            # notify others
            copyemails = []
            for val in cto_emails:
                    copyemails.append(list(val.items())[0][1])
            for val in npd_emails:
                    copyemails.append(list(val.items())[0][1])
            copymessage='''Hi ,

            A new Connection Request, {}  has been submitted and currently awaiting approval from the TM. 
    
            Best Regards'''.format(self.data.get('connectiontype'))
            send_mail(
                    subject,
                    copymessage,
                    settings.DEFAULT_FROM_EMAIL,
                    copyemails,
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
                # te_emails = EmailSerializer(ContractorUser.objects.filter(is_te=True), many=True).data
                
                
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
                # npd_emails = EmailSerializer(ContractorUser.objects.filter(is_npd=True), many=True).data
                
                
                for val in npd_emails:
                    npdemail.append(list(val.items())[0][1])
                send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        npdemail,
                        fail_silently=False,
                            )
                # notify others
                copyemails = []
                for val in cto_emails:
                        copyemails.append(list(val.items())[0][1])
                # for val in npd_emails:
                #         copyemails.append(list(val.items())[0][1])
                copymessage='''Hi ,

                A new Connection Request, {}  has been submitted and currently awaiting approval from the TM. 
        
                Best Regards'''.format(self.data.get('connectiontype'))
                send_mail(
                        subject,
                        copymessage,
                        settings.DEFAULT_FROM_EMAIL,
                        copyemails,
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
                # cto_emails = EmailSerializer(ContractorUser.objects.filter(is_cto=True), many=True).data
                
                
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
                # notify others
                copyemails = []
                for val in cto_emails:
                        copyemails.append(list(val.items())[0][1])
                for val in npd_emails:
                        copyemails.append(list(val.items())[0][1])
                for val in bhmmail:
                        copyemails.append(list(val.items())[0][1])
                copymessage='''Hi ,

                A new Connection Request, {}  has been submitted and currently awaiting contractor to request for precomission test. 
        
                Best Regards'''.format(self.data.get('connectiontype'))
                send_mail(
                        subject,
                        copymessage,
                        settings.DEFAULT_FROM_EMAIL,
                        copyemails,
                        fail_silently=False,
                            )
                # notify bhm


                subject = 'A Connection Request ({}) is Awaiting your Approval'.format(self.data.get('connectiontype'))
                message = '''
            Hi,

            A new Connection Request, {} is currently at the CTO approval stage and needs your approval.
            Kindly log in to the platform to review pending approvals on the Awaiting Approval tab for Connections. Click "https://ncp.ibedc.com" to visit the platform.

            Best Regards
            '''.format(self.data.get('connectiontype'))

                # hsemail = [val['email'] for val in EmailSerializer(ContractorUser.objects.filter(is_hse=True), many=True).data]

                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    hsemail,
                    fail_silently=False,
                )
                                # notify contractor
                subject='Your Connection Request ({}) you are to collect an approval form to commence connection'.format(self.data.get('connectiontype'))
                message='''Hi ,

                Your Connection Request, {}  has been tentatively approved by CTO. Kindly visit IBEDC office to collect Approval form to commence connection. Click "https://ncp.ibedc.com" to visit the platform.
                
                Best Regards'''.format(self.data.get('connectiontype'))
                
                send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        contractoremail,
                        fail_silently=False,
                            )
                # notify others
                



                        
               
                
                
                
            elif validated_data['approval_role'] == 'bhm':
                subject = 'A Connection Request ({}) is Awaiting your Approval'.format(self.data.get('connectiontype'))
                message = '''
            Hi,

            A new Connection Request, {} is currently at the HBO approval stage and needs your approval.
            Kindly log in to the platform to review pending approvals on the Awaiting Approval tab for Connections. Click "https://ncp.ibedc.com" to visit the platform.

            Best Regards
            '''.format(self.data.get('connectiontype'))

                # hboemail = [val['email'] for val in EmailSerializer(ContractorUser.objects.filter(is_hbo=True), many=True).data]

                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    hboemail,
                    fail_silently=False,
                )
                copyemails = []
                for val in cto_emails:
                        copyemails.append(list(val.items())[0][1])
                for val in npd_emails:
                        copyemails.append(list(val.items())[0][1])
                copymessage='''Hi ,

                A new Connection Request, {}  has been submitted and currently awaiting approval from the HBO. 
        
                Best Regards'''.format(self.data.get('connectiontype'))
                send_mail(
                        subject,
                        copymessage,
                        settings.DEFAULT_FROM_EMAIL,
                        copyemails,
                        fail_silently=False,
                            )
            elif validated_data['approval_role'] == 'hbo':
                subject = 'A Connection Request ({}) is Awaiting your Approval'.format(self.data.get('connectiontype'))
                message = '''
            Hi,

            A new Connection Request, {} is currently at the HM approval stage and needs your approval.
            Kindly log in to the platform to review pending approvals on the Awaiting Approval tab for Connections. Click "https://ncp.ibedc.com" to visit the platform.

            Best Regards
            '''.format(self.data.get('connectiontype'))

                # hmemail = [val['email'] for val in EmailSerializer(ContractorUser.objects.filter(is_hm=True), many=True).data]

                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    hmemail,
                    fail_silently=False,
                )
                # notify others
                copyemails = []
                for val in cto_emails:
                        copyemails.append(list(val.items())[0][1])
                for val in npd_emails:
                        copyemails.append(list(val.items())[0][1])
                copymessage='''Hi ,

                A new Connection Request, {}  has been submitted and currently awaiting approval from the HBO. 
        
                Best Regards'''.format(self.data.get('connectiontype'))
                send_mail(
                        subject,
                        copymessage,
                        settings.DEFAULT_FROM_EMAIL,
                        copyemails,
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
                # notify others
                copyemails = []
                for val in cto_emails:
                        copyemails.append(list(val.items())[0][1])
                for val in npd_emails:
                        copyemails.append(list(val.items())[0][1])
                for val in tm_emails:
                        copyemails.append(list(val.items())[0][1])
                copymessage='''Hi ,

                A completed Request, {}  A Connection Request, {}  approval has been completed. Click "https://ncp.ibedc.com" to visit the platform. 
        
                Best Regards'''.format(self.data.get('connectiontype'), self.data.get('status'))
                send_mail(
                        subject,
                        copymessage,
                        settings.DEFAULT_FROM_EMAIL,
                        copyemails,
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

            # Best Regards'''.format(self.data.get('connectiontype'), validated_data['declined_comment'])
            # send_mail(
            #         subject,
            #         message,
            #         settings.DEFAULT_FROM_EMAIL,
            #         contractoremail,
            #         fail_silently=False,
            #             )
            # notify others
            copyemails = []
            for val in cto_emails:
                    copyemails.append(list(val.items())[0][1])
            for val in npd_emails:
                    copyemails.append(list(val.items())[0][1])
            copymessage='''Hi ,

            A connection request - {} has been declined. Action required...  
    
            Best Regards'''.format(self.data.get('connectiontype'))
            send_mail(
                    subject,
                    copymessage,
                    settings.DEFAULT_FROM_EMAIL,
                    copyemails,
                    fail_silently=False,
                        )
            
        else:
            pass
        return super().update(instance, validated_data)  
    

class actioncontract_applicationReminderSerializer(serializers.ModelSerializer):

    class Meta:
        model=contract_application
        fields="__all__"

    def update(self, instance, validated_data):
        # print(self.data.get('contractor'))

        contractormail = EmailSerializer(ContractorUser.objects.filter(id=self.data.get('contractor')), many=True).data
        tm_emails = EmailSerializer(ContractorUser.objects.filter(is_tm=True), many=True,region=str(self.data.get('bh__region'))).data
        # te2_emails = EmailSerializer(ContractorUser.objects.filter(is_te=True), many=True).data
        hm_emails = EmailSerializer(ContractorUser.objects.filter(is_hm=True), many=True).data
        te_emails = EmailSerializer(ContractorUser.objects.filter(is_te=True, businesshub=str(self.data.get('bh'))), many=True).data
        npd_emails = EmailSerializer(ContractorUser.objects.filter(is_npd=True), many=True).data
        cto_emails = EmailSerializer(ContractorUser.objects.filter(is_cto=True), many=True).data
        hsemail = [val['email'] for val in EmailSerializer(ContractorUser.objects.filter(is_hse=True), many=True).data]
        bhmmail = EmailSerializer(ContractorUser.objects.filter(is_bhm=True, businesshub=str(self.data.get('bh'))), many=True).data
        hboemail = [val['email'] for val in EmailSerializer(ContractorUser.objects.filter(is_hbo=True), many=True).data]
        hmemail = [val['email'] for val in EmailSerializer(ContractorUser.objects.filter(is_hm=True), many=True).data]
 # REMINDER START HERE
               #  REMINDER FOR TE

        if(validated_data['approval_role']=='tm' and validated_data['approval_role'] != 'te' and validated_data['action'] != 'decline'):
            te_approved_date=validated_data['te_is_connection_approved_date']
            if date.today() >= te_approved_date + timedelta(days=2):
                
                #SEND MESSAGE AFTER TM APPROVAL. Send to TE to evaluate
                subject='A Reminder that a Connection Request ({}) is Awaiting your Evaluation'.format(self.data.get('connectiontype'))
                message='''Hi ,

                A new Connection Request, {}  is currently at the Technical evaluation stage and needs your approval. 
                Kindly login to the platform to review pending approvals on the Awaiting Approval tab for Connections.Click "https://ncp.ibedc.com" to visit the platform.

                Best Regards'''.format(self.data.get('connectiontype'))
                teemail = []
                # te_emails = EmailSerializer(ContractorUser.objects.filter(is_te=True), many=True).data
                
                
                for val in te_emails:
                    teemail.append(list(val.items())[0][1])
                send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        teemail,
                        fail_silently=False,
                            )
                
        # REMINDER FOR NPD
        if(validated_data['approval_role']=='te' and validated_data['approval_role'] != 'npd' and validated_data['action'] != 'decline'):
            npd_approved_date=validated_data['npd_is_connection_approved_date']
            if date.today() >= npd_approved_date + timedelta(days=2):
                
                #SEND MESSAGE AFTER TM APPROVAL. Send to TE to evaluate
                subject='A Reminder that a Connection Request ({}) is Awaiting your Approval'.format(self.data.get('connectiontype'))
                message='''Hi ,

                A new Connection Request, {}  is currently at the Network Administration stage and needs your approval. 
                Kindly login to the platform to review pending approvals on the Awaiting Approval tab for Connections.Click "https://ncp.ibedc.com" to visit the platform.

                Best Regards'''.format(self.data.get('connectiontype'))
                npdmail = []
                # te_emails = EmailSerializer(ContractorUser.objects.filter(is_te=True), many=True).data
                
                
                for val in npd_emails:
                    npdmail.append(list(val.items())[0][1])
                send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        npdmail,
                        fail_silently=False,
                            )
        # REMINDER FOR CTO
        if(validated_data['approval_role']=='npd' and validated_data['approval_role'] != 'cto' and validated_data['action'] != 'decline'):
            te_approved_date=validated_data['te_is_connection_approved_date']
            if date.today() >= te_approved_date + timedelta(days=2):
                
                #SEND MESSAGE AFTER TM APPROVAL. Send to TE to evaluate
                subject='A Reminder that a Connection Request ({}) is Awaiting your Approval'.format(self.data.get('connectiontype'))
                message='''Hi ,

                A new Connection Request, {}  is currently at the Network Administration stage and needs your approval. 
                Kindly login to the platform to review pending approvals on the Awaiting Approval tab for Connections.Click "https://ncp.ibedc.com" to visit the platform.

                Best Regards'''.format(self.data.get('connectiontype'))
                ctomail = []
                # te_emails = EmailSerializer(ContractorUser.objects.filter(is_te=True), many=True).data
                
                
                for val in cto_emails:
                    ctomail.append(list(val.items())[0][1])
                send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        ctomail,
                        fail_silently=False,
                            )

        # REMINDER FOR CONTRACTOR
        if(validated_data['approval_role']=='cto' and validated_data['ct_is_pre_requested'] == False and validated_data['action'] != 'decline'):
            cto_approved_date=validated_data['cto_is_connection_approved_date']
            if date.today() >= cto_approved_date + timedelta(days=2):
                
                #SEND MESSAGE AFTER TM APPROVAL. Send to TE to evaluate
                subject='Your Connection Request ({}) is at Precomissioning Stage. Action required.'.format(self.data.get('connectiontype'))
                message='''Hi ,

                Your Connection Request, {}  is currently at the Precomissioning Stage.
                Kindly login to your dashboard, and request precommissioning test for the connection.Click "https://ncp.ibedc.com" to visit the platform.
                
                Best Regards'''.format(self.data.get('connectiontype'))
                
                
            
                # te_emails = EmailSerializer(ContractorUser.objects.filter(is_te=True), many=True).data
                
                
                # for val in te_emails:
                #     teemail.append(list(val.items())[0][1])
                send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        contractormail,
                        fail_silently=False,
                            )        
        # REMINDER FOR TE PRECOM
        if(validated_data['action'] == 'precomreq' and validated_data['tept_is_connection_approved'] == False and validated_data['action'] != 'decline'):
            request_approved_date=validated_data['ct_is_pre_requested_date']
            if date.today() >= request_approved_date + timedelta(days=2):
                
                #SEND MESSAGE AFTER TM APPROVAL. Send to TE to evaluate
                subject='A Reminder that a Connection Request ({}) is Awaiting your Approval'.format(self.data.get('connectiontype'))
                message='''Hi ,

                A new Connection Request, {}  is currently at the Network Administration stage and needs your approval. 
                Kindly login to the platform to review pending approvals on the Awaiting Approval tab for Connections.Click "https://ncp.ibedc.com" to visit the platform.

                Best Regards'''.format(self.data.get('connectiontype'))
                teemail = []
                # te_emails = EmailSerializer(ContractorUser.objects.filter(is_te=True), many=True).data
                
                
                for val in te_emails:
                    teemail.append(list(val.items())[0][1])
                send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        teemail,
                        fail_silently=False,
                            )  


        # REMINDER FOR BHM
        if(validated_data['tept_is_connection_approved']==True and validated_data['bhm_is_connection_approved']==False and validated_data['action'] != 'decline'):
            tept_approved_date=validated_data['tept_is_connection_approved_date']
            if date.today() >= tept_approved_date + timedelta(days=2):
                
                #SEND MESSAGE AFTER TM APPROVAL. Send to TE to evaluate
                subject='A Reminder that a Connection Request ({}) is Awaiting your Approval'.format(self.data.get('connectiontype'))
                message='''Hi ,

                A new Connection Request, {}  is currently at the Network Administration stage and needs your approval. 
                Kindly login to the platform to review pending approvals on the Awaiting Approval tab for Connections.Click "https://ncp.ibedc.com" to visit the platform.

                Best Regards'''.format(self.data.get('connectiontype'))
                bhmmail = []
                # te_emails = EmailSerializer(ContractorUser.objects.filter(is_te=True), many=True).data
                
                
                for val in bhmmail:
                    bhmmail.append(list(val.items())[0][1])
                send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        bhmmail,
                        fail_silently=False,
                            )     
                
        # REMINDER FOR HBO
        if(validated_data['bhm_is_connection_approved']==True and validated_data['hbo_is_connection_approved']==False and validated_data['action'] != 'decline'):
            bhm_approved_date=validated_data['bhm_is_contractor_approved_date']
            if date.today() >= bhm_approved_date + timedelta(days=2):
                
                #SEND MESSAGE AFTER TM APPROVAL. Send to TE to evaluate
                subject = 'A Connection Request ({}) is Awaiting your Approval'.format(self.data.get('connectiontype'))
                message = '''
            Hi,

            A new Connection Request, {} is currently at the HBO approval stage and needs your approval.
            Kindly log in to the platform to review pending approvals on the Awaiting Approval tab for Connections. Click "https://ncp.ibedc.com" to visit the platform.

            Best Regards
            '''.format(self.data.get('connectiontype'))
                # te_emails = EmailSerializer(ContractorUser.objects.filter(is_te=True), many=True).data
                
                

                send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        hboemail,
                        fail_silently=False,
                            )     
        # REMINDER FOR HM
        if(validated_data['hbo_is_connection_approved']==True and validated_data['hm_is_connection_approved'] ==False and validated_data['action'] != 'decline'):
            hbo_approved_date=validated_data['hbo_is_contractor_approved_date']
            if date.today() >= hbo_approved_date + timedelta(days=2):
                
                #SEND MESSAGE AFTER TM APPROVAL. Send to TE to evaluate
                subject = 'A Connection Request ({}) is Awaiting your Approval'.format(self.data.get('connectiontype'))
                message = '''
            Hi,

            A new Connection Request, {} is currently at the HM approval stage and needs your approval.
            Kindly log in to the platform to review pending approvals on the Awaiting Approval tab for Connections. Click "https://ncp.ibedc.com" to visit the platform.

            Best Regards
            '''.format(self.data.get('connectiontype'))

                # hmemail = [val['email'] for val in EmailSerializer(ContractorUser.objects.filter(is_hm=True), many=True).data]

                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    hmemail,
                    fail_silently=False,
                )


        # REMINDER FOR CONTRACTOR FOR COMMISSIONING
        if(validated_data['hm_is_connection_approved']==True and validated_data['ct_is_done'] ==False and validated_data['action'] != 'decline'):
            hm_approved_date=validated_data['hm_is_contractor_approved_date']
            if date.today() >= hm_approved_date + timedelta(days=2):
                
                #SEND MESSAGE AFTER TM APPROVAL. Send to TE to evaluate
                subject='A Reminder that your commisioning document ({}) are yet to uploaded '.format(self.data.get('connectiontype'))
                message='''Hi ,

                A new Connection Request, {}  is currently at the Network Administration stage and needs your approval. 
                Kindly login to the platform to review pending approvals on the Awaiting Approval tab for Connections.Click "https://ncp.ibedc.com" to visit the platform.

                Best Regards'''.format(self.data.get('connectiontype'))
                
                send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        contractormail,
                        fail_silently=False,
                            )         
                 # notify others
                copyemails = []
                for val in cto_emails:
                        copyemails.append(list(val.items())[0][1])
                for val in npd_emails:
                        copyemails.append(list(val.items())[0][1])
                copymessage='''Hi ,

                A new Connection Request, {}  has been submitted and currently awaiting approval from the TM. 
        
                Best Regards'''.format(self.data.get('connectiontype'))
                send_mail(
                        subject,
                        copymessage,
                        settings.DEFAULT_FROM_EMAIL,
                        copyemails,
                        fail_silently=False,
                            )

            # REMINDER END HERE    
     
