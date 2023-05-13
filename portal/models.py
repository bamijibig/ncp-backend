from django.db import models

from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "PASSWORD RESET TOKEN: {} ".format(reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {}".format(reset_password_token.user.email),
        # message:
        email_plaintext_message,
        # from:
        "No Reply <no_reply@ibedc.com>",
        # to:
        [reset_password_token.user.email]
    )



class ContractorUser(AbstractUser):
    # user=models.ForeignKey(User,blank="True",null="True", on_delete=models.SET_NULL)
    # email=models.EmailField(null=True,blank=True)
    # password=models.CharField(max_length=250,blank=True)
    # businesshub=models.ForeignKey(BusinessHub,on_delete=models.CASCADE, null=True,blank=True)
    contractor_name=models.CharField(max_length=250,blank=True)
    con_address=models.CharField(max_length=250,blank=True)
    licensed_no=models.IntegerField(null=True,blank=True)
    tel_no=models.CharField(max_length=100,null=True,blank=True)
    role=models.CharField(max_length=100,null=True,blank=True)
    job_title=models.CharField(max_length=100,null=True,blank=True)

    stafftype=(
        ('hqstaff','hqstaff'),
        ('regionstaff','regionstaff'),
        ('businesshubstaff','businesshubstaff')
    )

    staff_type=models.CharField(max_length=100, choices=stafftype, default='hqstaff') 
    region=models.CharField(max_length=100,null=True,blank=True) #Send region id as value
    businesshub=models.CharField(max_length=100,null=True,blank=True) #Send business hub id as value
    coren_or_nemsa_competency=models.FileField(null=True,blank=True)
    reg_date=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    is_contractor = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_tm = models.BooleanField(default=False)
    is_te = models.BooleanField(default=False)
    is_npd = models.BooleanField(default=False)
    is_cto = models.BooleanField(default=False)
    is_md = models.BooleanField(default=False)
    is_hsch = models.BooleanField(default=False)
    is_hm = models.BooleanField(default=False)

    in_approval_workflow = models.BooleanField(default=False)
   
 
    registration_status = models.CharField(max_length=200, null=True,blank=True) #in-progress

    # hsch_is_contractor_approved = models.BooleanField(default=False)
    # hsch_is_contractor_approved_date = models.DateField(null = True, blank=True)
    # hsch_approved_by=models.CharField(max_length=200,null=True,blank=True)
    # hsch_memo=models.FileField(null=True,blank=True)

    
    cto_is_contractor_approved = models.BooleanField(default=False)
    cto_is_contractor_approved_date = models.DateField(null = True, blank=True)
    cto_approved_by=models.CharField(max_length=200,null=True,blank=True)
    cto_memo=models.FileField(null=True,blank=True)


    md_is_contractor_approved = models.BooleanField(default=False)
    md_is_contractor_approved_date = models.DateField(null = True, blank=True)
    md_approved_by=models.CharField(max_length=200,null=True,blank=True)
    md_memo=models.FileField(null=True,blank=True)

    declined = models.BooleanField(default=False)
    declined_comment = models.TextField(null=True,blank=True)
    registration_approved = models.BooleanField(default=False)



class Region(models.Model):
    region=models.CharField(max_length=200, null=True, blank=True)
    location=models.CharField(max_length=200,null=True, blank=True)
    regionManager=models.ForeignKey(ContractorUser,on_delete=models.DO_NOTHING, related_name = "region_manager", null=True,blank=True)
    technicalManager=models.ForeignKey(ContractorUser,on_delete=models.DO_NOTHING, related_name = "region_t_manager", null=True,blank=True)
    email=models.EmailField(null=True, blank=True)
    phoneNumber=models.CharField(max_length=200,null=True, blank=True)

class BusinessHub(models.Model):
    region=models.ForeignKey(Region,on_delete=models.CASCADE, null=True,blank=True)
    businesshub=models.CharField(max_length=200, null=True, blank=True)
    location=models.CharField(max_length=200,null=True, blank=True)
    hubManager=models.ForeignKey(ContractorUser,on_delete=models.DO_NOTHING, related_name = "hub_manager", null=True,blank=True)
    technicalManager=models.ForeignKey(ContractorUser,on_delete=models.DO_NOTHING, related_name = "hub_t_manager", null=True,blank=True)
    email=models.EmailField(null=True, blank=True)
    phoneNumber=models.CharField(max_length=200,null=True, blank=True)



class contract_application(models.Model):
    contractor=models.ForeignKey(ContractorUser, null=True,  on_delete=models.CASCADE, related_name="usercontractor")
    bh=models.ForeignKey(BusinessHub,on_delete=models.CASCADE, null=True,blank=True) 
    company_name= models.CharField(max_length=100,null=True,blank=True)
    connection_type = (
        ('transformer installation', 'transformer installation'),
        ('transformer uprating', 'transformer uprating'),
        ('relocation', 'relocation'),
        ('change of transformer source', 'change of transformer source'),
        ('others', 'others')
    )
    connectiontype = models.CharField(max_length=100, choices=connection_type,default='transformer installation')


    capacity_type = (
        ('catd_50kva', 'catd_50kva'),
        ('catc_100kva', 'catc_100kva'),
        ('catb_1000kva', 'catb_1000kva'),
        ('cata_all', 'cata_all'),
        
    )
    capacity = models.CharField(max_length=100, choices=capacity_type, default='catd_50kva')

    voltageratio_type = (
        ('elevenby400', 'elevenby400'),
        ('thirtythreeby400', 'thirtythreeby400'),
        
    )
    voltage_ratio = models.CharField(max_length=100, choices=voltageratio_type, default='elevenby400')

    # capacity=  models.CharField(max_length=250,blank=True)
    # voltage_ratio=models.CharField(max_length=250,blank=True)
    route_length_km=models.CharField(max_length=250,blank=True)

    add_house_no=models.CharField(max_length=250,blank=True)
    add_street=models.CharField(max_length=250,blank=True)
    add_town_or_city=models.CharField(max_length=250,blank=True)
    add_lga=models.CharField(max_length=250,blank=True)
    add_state=models.CharField(max_length=250,blank=True)

    est_load_of_premises=models.CharField(max_length=250,blank=True)



    use_of_premises = (
        ('residential', 'residential'),
        ('commercial', 'commercial'),
        ('industrial', 'industrial'),
       
    )
    useofpremises = models.CharField(max_length=100, choices=use_of_premises,default='residential')
    #contracter information
    security_receipt = models.FileField(null=True,blank=True)
    

    #user= models.ForeignKey(user)
    letter_of_donation_dss=models.FileField(null=True,blank=True)
    nemsa_test_cert=models.FileField(null=True,blank=True)
    transformer_waranty=models.FileField(null=True,blank=True)
    transformer_test_cert=models.FileField(null=True,blank=True)
   
    date_of_application=models.DateTimeField(auto_now_add=True,null=True,blank=True)

    in_approval_workflow = models.BooleanField(default=False)
   
 
    connection_status = models.CharField(max_length=200, null=True,blank=True) #in-progress
    # TM
    tm_is_connection_approved = models.BooleanField(default=False)
    tm_is_connection_approved_date = models.DateField(null = True, blank=True)
    tm_is_connection_approved_by=models.CharField(max_length=200,null=True,blank=True)
    tm_memo=models.FileField(null=True,blank=True)

    # TE
    te_is_connection_approved = models.BooleanField(default=False)
    te_is_connection_approved_date = models.DateField(null = True, blank=True)
    te_is_connection_approved_by=models.CharField(max_length=200,null=True,blank=True)
    te_memo=models.FileField(null=True,blank=True)

    # NPD
    npd_is_connection_approved = models.BooleanField(default=False)
    npd_is_connection_approved_date = models.DateField(null = True, blank=True)
    npd_is_connection_approved_by=models.CharField(max_length=200,null=True,blank=True)
    npd_memo=models.FileField(null=True,blank=True)

    # CTO
    cto_is_connection_approved = models.BooleanField(default=False)
    cto_is_connection_approved_date = models.DateField(null = True, blank=True)
    cto_approved_by=models.CharField(max_length=200,null=True,blank=True)
    cto_memo=models.FileField(null=True,blank=True)

    # Contractor precommissioning
    ct_is_pre_requested = models.BooleanField(default=False)
    ct_is_pre_requested_date = models.DateField(null = True, blank=True)

    # TE precommissioning
    tept_is_connection_approved = models.BooleanField(default=False)
    tept_is_connection_approved_date = models.DateField(null = True, blank=True)
    tept_is_connection_approved_by=models.CharField(max_length=200,null=True,blank=True)

    # HM
    hm_is_connection_approved = models.BooleanField(default=False)
    hm_is_contractor_approved_date = models.DateField(null = True, blank=True)
    hm_approved_by=models.CharField(max_length=200,null=True,blank=True)
    hm_memo=models.FileField(null=True,blank=True)

    declined = models.BooleanField(default=False)
    declined_comment = models.TextField(null=True,blank=True)
    connection_approved = models.BooleanField(default=False)

    # Evaluation Form Data

    eval_title=models.CharField(max_length=250, null=True, blank=True)
    eval_applicant=models.CharField(max_length=250, null=True, blank=True)

    voltagelevel_type = (
        ('elevenkv', 'elevenkv'),
        ('thirtythreekv', 'thirtythreekv'),
        ('fourhundred', 'fourhundred'),
    )
    eval_voltage_level = models.CharField(max_length=100, choices=voltagelevel_type, default='elevenkv')


    
    # eval_voltage_level=models.CharField(max_length=250, null=True, blank=True)
    eval_dt=models.CharField(max_length=250, null=True, blank=True)
    eval_estimated_load=models.CharField(max_length=250, null=True, blank=True)
    eval_site_visit_date=models.CharField(max_length=250, null = True, blank=True)
    eval_new4upgrade=models.CharField(max_length=50,null=True,blank=True)
    eval_conworkdone=models.CharField(max_length=50,null=True,blank=True)
    eval_dtsubname=models.CharField(max_length=200,null=True,blank=True)
    eval_region=models.CharField(max_length=200,null=True,blank=True) 
    eval_bhub=models.CharField(max_length=200,null=True,blank=True)
    eval_comentoncon=models.TextField(null=True,blank=True)
    eval_fdrname=models.CharField(max_length=200,null=True,blank=True)
    eval_fdrcapacity=models.CharField(max_length=200,null=True,blank=True)
    eval_fdrpload=models.CharField(max_length=200,null=True,blank=True)
    eval_tilldate=models.CharField(max_length=250, null = True, blank=True)
    eval_cumloada=models.CharField(max_length=200,null=True,blank=True)
    # Details of source substation
    eval_srcfeeder=models.CharField(max_length=200,null=True,blank=True)
    eval_ptrsf=models.CharField(max_length=200,null=True,blank=True)
    eval_trsfrating=models.CharField(max_length=200,null=True,blank=True)
    eval_trendpeak=models.CharField(max_length=200,null=True,blank=True)
    eval_cumtilldate=models.CharField(max_length=250, null = True, blank=True)
    eval_cummwithload=models.CharField(max_length=200,null=True,blank=True)
    eval_permload=models.CharField(max_length=200,null=True,blank=True)
    eval_maravail=models.CharField(max_length=200,null=True,blank=True)
    # Approval
    eval_fulspons=models.CharField(max_length=200,null=True,blank=True)
    eval_estpcost=models.CharField(max_length=200,null=True,blank=True)
    eval_specoment=models.TextField(null=True, blank=True)
    # Detailed project report
    eval_title2=models.CharField(max_length=200,null=True,blank=True)
    eval_preamble=models.TextField(null=True, blank=True)
    eval_findings=models.TextField(null=True, blank=True)
    eval_scopework=models.TextField(null=True, blank=True)
    eval_recom=models.TextField(null=True,blank=True)
    eval_pcm=models.FileField(null=True,blank=True)   
    eval_otherdoc=models.FileField(null=True,blank=True)

    # # Summary report for relief dss
    # #    Project details
    # eval_titlepro=models.CharField(max_length=200,null=True,blank=True)
    # eval_usercom=models.CharField(max_length=200,null=True,blank=True)
    # eval_projmaincat=models.CharField(max_length=200,null=True,blank=True)
    # eval_dtrating=models.CharField(max_length=200,null=True,blank=True)
    # eval_voltlevel=models.CharField(max_length=200,null=True,blank=True)
    # eval_subhead=models.CharField(max_length=200,null=True,blank=True)
    # eval_title=models.CharField(max_length=200,null=True,blank=True)
    # # Finding from site visit
    # eval_datevisit=models.CharField(max_length=250, null = True, blank=True)
    # eval_specloc=models.CharField(max_length=200,null=True,blank=True)
    # eval_majchaexidss=models.CharField(max_length=200,null=True,blank=True)
    
    # # SUBSTATION ANALYSIS
    # nameofsubstation = (
    #         ('existing substation', 'existing substation'),
    #         ('proposed substation', 'proposed substation'),
    #         ('existing substation after relieve', 'existing substation after relieve'),
        
    #     )
    # eval_nameofsub = models.CharField(max_length=100, choices=nameofsubstation, default='existing substation')
    # eval_rating=models.CharField(max_length=200,null=True,blank=True)
    # eval_loading=models.CharField(max_length=200,null=True,blank=True)
    # eval_loadpercent=models.CharField(max_length=200,null=True,blank=True)
    # eval_2yrsloadproj=models.CharField(max_length=200,null=True,blank=True)
    # eval_2yrsloadprojpercent=models.CharField(max_length=200,null=True,blank=True)
    # eval_amtbillkwh=models.CharField(max_length=200,null=True,blank=True)
    # eval_amtbillnaira=models.CharField(max_length=200,null=True,blank=True)
    # eval_collection=models.CharField(max_length=200,null=True,blank=True)
    # eval_collectioneff=models.CharField(max_length=200,null=True,blank=True)
    # #     # RECOMMENDED FEEDER/ASSETS FOR CONNECTION
    # eval_fdrname2=models.CharField(max_length=200,null=True,blank=True)
    # eval_fdravail=models.CharField(max_length=200,null=True,blank=True)
    # eval_fdrcapacity2=models.CharField(max_length=200,null=True,blank=True)
    # eval_fdrtrendpeak=models.CharField(max_length=200,null=True,blank=True)
    # eval_fdrdate=models.CharField(max_length=250, null = True, blank=True)
    # eval_cumload2=models.CharField(max_length=200,null=True,blank=True)
    # eval_srcfeeder2=models.CharField(max_length=200,null=True,blank=True)

    # #     # PROJECT COST ANALYSIS
    # eval_projcost=models.CharField(max_length=200,null=True,blank=True)
    # eval_sanctioncost=models.CharField(max_length=200,null=True,blank=True)
    # eval_capcontribproj=models.CharField(max_length=200,null=True,blank=True)
    # eval_donor=models.CharField(max_length=200,null=True,blank=True)
    # eval_ibedc=models.CharField(max_length=200,null=True,blank=True)
    # #     # APPROVAL
    # eval_aprovmbgrant=models.CharField(max_length=200,null=True,blank=True)
    # eval_recmetertyp=models.CharField(max_length=200,null=True,blank=True)
    # eval_statmeter=models.CharField(max_length=200,null=True,blank=True)
    # eval_specoment2=models.TextField(null=True,blank=True)
    # #     # ATTACHMENT BY TE
    # eval_custreq=models.CharField(max_length=200,null=True,blank=True)
    # eval_condiag=models.FileField(null=True,blank=True)
    # eval_schdiag=models.FileField(null=True,blank=True)
    # eval_sitevform=models.FileField(null=True,blank=True)
    # eval_projplanby=models.CharField(max_length=200,null=True,blank=True)




    # Precomissioning Form
    precom_project_title=models.CharField(max_length=250, null=True, blank=True)
    precom_last_inspection_date=models.CharField(max_length=250, null = True, blank=True)
    precom_project_objectives=models.TextField(null=True, blank=True)

    precom_supplysrc=models.CharField(max_length=200,null=True,blank=True)
    precom_fdrname3=models.CharField(max_length=200,null=True,blank=True)
    precom_peakload=models.CharField(max_length=200,null=True,blank=True)
    precom_dwndrpcon=models.BooleanField(default=False)
    precom_distofnss=models.CharField(max_length=200,null=True,blank=True)
    precom_nopoleht=models.CharField(max_length=200,null=True,blank=True)
    precom_nopolelt=models.CharField(max_length=200,null=True,blank=True)
    precom_podeptht=models.CharField(max_length=200,null=True,blank=True)
    precom_podepthlh=models.CharField(max_length=200,null=True,blank=True)
    precom_sizeconduct=models.CharField(max_length=200,null=True,blank=True)
    precom_qtyused=models.CharField(max_length=200,null=True,blank=True)
    precom_wellallmetalprt=models.BooleanField(default=False)
    precom_ssfencedibedc=models.BooleanField(default=False)
    precom_wellgraveled=models.BooleanField(default=False)
    precom_typfence=models.CharField(max_length=200,null=True,blank=True)
    precom_nemsavail=models.BooleanField(default=False)
        # Substation Details
    precom_trsfcap=models.CharField(max_length=200,null=True,blank=True)
    precom_voltratio=models.CharField(max_length=200,null=True,blank=True)
    precom_make=models.CharField(max_length=200,null=True,blank=True)
    precom_sn=models.CharField(max_length=200,null=True,blank=True)
    precom_current=models.CharField(max_length=200,null=True,blank=True)
    precom_vectorgrp=models.CharField(max_length=200,null=True,blank=True)
    precom_impedance=models.CharField(max_length=200,null=True,blank=True)
    precom_yrsofman=models.CharField(max_length=200,null=True,blank=True)
    precom_cooling=models.CharField(max_length=200,null=True,blank=True)
    precom_cabletypsiz=models.CharField(max_length=200,null=True,blank=True)
    precom_fdrpillarcurr=models.CharField(max_length=200,null=True,blank=True)
    precom_icomcablesiz=models.CharField(max_length=200,null=True,blank=True)
    precom_uprizercable=models.CharField(max_length=200,null=True,blank=True)
    precom_nouprizercable=models.CharField(max_length=200,null=True,blank=True)
    precom_earthresv=models.CharField(max_length=200,null=True,blank=True)
    precom_pcm=models.FileField(null=True,blank=True)
    precom_others=models.FileField(null=True,blank=True)



    def __str__(self):
        return self.company_name


