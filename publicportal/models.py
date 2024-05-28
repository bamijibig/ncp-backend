from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail

from portal.models import BusinessHub, ContractorUser
class contract_applicationpub(models.Model):
    contractor=models.ForeignKey(ContractorUser, null=True,  on_delete=models.CASCADE, related_name="usercontractoruser")
    # servicecentre=models.ForeignKey(Servicecentre,on_delete=models.CASCADE, null=True,blank=True) 
    bh=models.ForeignKey(BusinessHub, on_delete=models.CASCADE, null=True,blank=True, related_name="bhuser")
  
    # PUBLIC CONTRACTOR DSS-RELIEF DT

    name_sponsor=models.CharField(max_length=200, null=True,blank=True)
    community_name=models.CharField(max_length=200, null=True,blank=True)

    # PROJECT DETAILS
    title=models.CharField(max_length=200, null=True,blank=True)
    chairman_comm_name=models.CharField(max_length=200, null=True,blank=True)
    chairman_comm_number=models.CharField(max_length=200, null=True,blank=True)
    dt_capacity=models.CharField(max_length=200, null=True,blank=True)
    voltage_level=models.CharField(max_length=200, null=True,blank=True)

    # FINDINGS FROM THE SITE VISIT
    # date_of_visit=models.CharField(max_length=200, null=True,blank=True)
   

    # date_of_visit = models.DateField(auto_now_add=True)

    # no_of_customers=models.CharField(max_length=200, null=True,blank=True)
    estimated_load=models.CharField(max_length=200, null=True,blank=True)
    estimated_cost=models.CharField(max_length=200, null=True,blank=True)
    no_of_spans=models.CharField(max_length=200, null=True,blank=True) 
    relief_type = (
        ('relief', 'relief'),
        ('up rating', 'up rating'),
        ('replacement', 'replacement'),
        ('new extension', 'new extension'),
        ('realignment', 'realignment'),
        ('relocation', 'relocation'),
    )
    relieftype = models.CharField(max_length=100, choices=relief_type,default='relief')

    # RECOMMENDED FEEDER/ASSETS FOR CONNECTION
    # feeder_name= models.CharField(max_length=200, null=True,blank=True) 
    # feeder_capacity=models.CharField(max_length=200, null=True,blank=True) 
    # fdr_peakload=models.CharField(max_length=200, null=True,blank=True) 
    # load_tilldate=models.CharField(max_length=200, null=True,blank=True) 

    # DETAIL OF SOURCE SUBSTATION(INJECTION ISS/TRANSMISSION STATION)
    # source_fdr=models.CharField(max_length=200, null=True,blank=True) 
    # powertrans=models.CharField(max_length=200, null=True,blank=True) 
    # trans_rating=models.CharField(max_length=200, null=True,blank=True) 
     
    #  APPROVAL
    # expected_billing=models.CharField(max_length=200, null=True,blank=True) 
    # expected_gain=models.CharField(max_length=200, null=True,blank=True) 
    # letter_of_donation_dss=models.FileField(null=True,blank=True)
    nemsa_comp_cert=models.FileField(null=True,blank=True)
    coren_cert=models.FileField(null=True,blank=True)
    intro_letter_client=models.FileField(null=True,blank=True)

    # RELIEF CONTRACTOR FORM END
    #contracter information
    security_receipt = models.FileField(null=True,blank=True)
    
   
    #user= models.ForeignKey(user)
    
    # transformer_test_cert=models.FileField(null=True,blank=True)
   
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

    # HSE


    hse_is_connection_approved = models.BooleanField(default=False)
    hse_is_contractor_approved_date = models.DateField(null = True, blank=True)
    hse_approved_by=models.CharField(max_length=200,null=True,blank=True)
    hse_memo=models.FileField(null=True,blank=True)
    # BHM
    bhm_is_connection_approved = models.BooleanField(default=False)
    bhm_is_contractor_approved_date = models.DateField(null = True, blank=True)
    bhm_approved_by=models.CharField(max_length=200,null=True,blank=True)
    bhm_memo=models.FileField(null=True,blank=True)
    # HBO
    hbo_is_connection_approved = models.BooleanField(default=False)
    hbo_is_contractor_approved_date = models.DateField(null = True, blank=True)
    hbo_approved_by=models.CharField(max_length=200,null=True,blank=True)
    hbo_memo=models.FileField(null=True,blank=True)

    # HM
    hm_is_connection_approved = models.BooleanField(default=False)
    hm_is_contractor_approved_date = models.DateField(null = True, blank=True)
    hm_approved_by=models.CharField(max_length=200,null=True,blank=True)
    hm_memo=models.FileField(null=True,blank=True)

    declined = models.BooleanField(default=False)
    declined_comment = models.TextField(null=True,blank=True)
    connection_approved = models.BooleanField(default=False)



     # Commissioning form for contractor
    projsignedoff=models.BooleanField(default=False)
    inspbynemsa=models.BooleanField(default=False)
    compdate=models.DateField(auto_now_add=True, null = True, blank=True)
    comprojcert=models.FileField(null=True,blank=True)
    nemsatestcert=models.FileField(null=True,blank=True)
    letterofdonation=models.FileField(null=True,blank=True)
    ct_is_done=models.BooleanField(default=False)
    ct_is_completed=models.FileField(null=True,blank=True)
    ct_is_completed_date = models.DateField(null = True, blank=True)

    # Evaluation Form Data

    # Summary report for relief dss
    #    Project details
    eval_titlepro=models.CharField(max_length=200,null=True,blank=True)
    eval_usercom=models.CharField(max_length=200,null=True,blank=True)
    eval_projmaincat=models.CharField(max_length=200,null=True,blank=True)
    eval_dtrating=models.CharField(max_length=200,null=True,blank=True)
    eval_voltlevel=models.CharField(max_length=200,null=True,blank=True)
    eval_subhead=models.CharField(max_length=200,null=True,blank=True)
    eval_title=models.CharField(max_length=200,null=True,blank=True)
    # Finding from site visit
    eval_datevisit=models.CharField(max_length=200,null=True,blank=True)
    eval_extload=models.CharField(max_length=200,null=True,blank=True)
    eval_majchaexidss=models.CharField(max_length=200,null=True,blank=True)
   
   
    # RELIEF SUBSTATION ANALYSIS
    nameofsubstation = (
            ('existing substation bf relief', 'existing substation bf relief'),
            
            ('existing substation after relieve', 'existing substation after relieve'),
        
        )
    eval_nameofsub = models.CharField(max_length=100, choices=nameofsubstation, default='existing substation bf relief')
    # eval_region=models.CharField(max_length=200,null=True,blank=True) 
    # eval_bhub=models.CharField(max_length=200,null=True,blank=True)
    eval_rating=models.CharField(max_length=200,null=True,blank=True)
    eval_loading=models.CharField(max_length=200,null=True,blank=True)
    eval_loadpercent=models.CharField(max_length=200,null=True,blank=True)
    eval_1yrloadpercentload=models.CharField(max_length=200,null=True,blank=True)
    eval_quarterlyload=models.CharField(max_length=200,null=True,blank=True)
    eval_amtbillkwh=models.CharField(max_length=200,null=True,blank=True)
    eval_amtbillnaira=models.CharField(max_length=200,null=True,blank=True)
    eval_collection=models.CharField(max_length=200,null=True,blank=True)
    eval_collectioneff=models.CharField(max_length=200,null=True,blank=True)
    eval_custpop=models.CharField(max_length=200,null=True,blank=True)


    # NEW EXTENSION S/S ANALYSIS
    # nameofnewss = (
    #         ('name of ss', 'name of ss'),
            
    #         ('proposed ss', 'proposed ss'),
        
    #     )
    eval_nameofextss = models.CharField(max_length=200,null=True,blank=True)
    eval_extrating=models.CharField(max_length=200,null=True,blank=True)
    eval_proposedloading=models.CharField(max_length=200,null=True,blank=True)
    eval_extloadpercent=models.CharField(max_length=200,null=True,blank=True)
    eval_3monthloadproj=models.CharField(max_length=200,null=True,blank=True)
    eval_extprojbilling=models.CharField(max_length=200,null=True,blank=True)
    eval_projbillingkwh=models.CharField(max_length=200,null=True,blank=True)
    eval_projcollection=models.CharField(max_length=200,null=True,blank=True)
    eval_projcollectioneff=models.CharField(max_length=200,null=True,blank=True)
    eval_extcustpop=models.CharField(max_length=200,null=True,blank=True)




    #     # RECOMMENDED FEEDER/ASSETS FOR CONNECTION
    eval_fdrname=models.CharField(max_length=200,null=True,blank=True)  
    eval_fdrcapacity=models.CharField(max_length=200,null=True,blank=True)
    eval_fdrtrendpeak=models.CharField(max_length=200,null=True,blank=True)
    eval_fdrsupload=models.CharField(max_length=200,null=True,blank=True)
    eval_cumload=models.CharField(max_length=200,null=True,blank=True)
    eval_srcfeeder=models.CharField(max_length=200,null=True,blank=True)

    #     # PROJECT COST ANALYSIS
    eval_projcost=models.CharField(max_length=200,null=True,blank=True)
    eval_donor=models.CharField(max_length=200,null=True,blank=True)
    eval_ibedc=models.CharField(max_length=200,null=True,blank=True)

    # PROJECT COMMERCIAL ANALYSIS
    nocustomers=models.CharField(max_length=200,null=True,blank=True)
    expected_billcom=models.CharField(max_length=200,null=True,blank=True)
    expected_gaincom=models.CharField(max_length=200,null=True,blank=True)

    #     # APPROVAL
    eval_aprovmbgrant=models.CharField(max_length=200,null=True,blank=True)
    eval_recmetertyp=models.CharField(max_length=200,null=True,blank=True)
    eval_statmeter=models.CharField(max_length=200,null=True,blank=True)
    
    #     # ATTACHMENT BY TE
    eval_custreq=models.FileField(null=True,blank=True)
    eval_blockdiag=models.FileField(null=True,blank=True)
    eval_schdiag=models.FileField(null=True,blank=True)
    eval_sitevform=models.FileField(null=True,blank=True)
    eval_projplanby=models.CharField(max_length=200,null=True,blank=True)

    # DETAILED PROJECT INSPECTION REPORT
    title=models.CharField(max_length=200,null=True,blank=True)
    preamble=models.CharField(max_length=200,null=True,blank=True)
    findings=models.CharField(max_length=200,null=True,blank=True)
    scopeofwork=models.CharField(max_length=200,null=True,blank=True)
    recommendation=models.CharField(max_length=200,null=True,blank=True)


    # Precomissioning Form
    precom_project_title=models.CharField(max_length=250, null=True, blank=True)
    precom_last_inspection_date=models.CharField(max_length=250, null=True, blank=True)
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
    precom_cabletype=models.CharField(max_length=200,null=True,blank=True)
    precom_fdrpillarcurr=models.CharField(max_length=200,null=True,blank=True)
    precom_icomcablesiz=models.CharField(max_length=200,null=True,blank=True)
    precom_uprizercable=models.CharField(max_length=200,null=True,blank=True)
    precom_nouprizercable=models.CharField(max_length=200,null=True,blank=True)
    precom_earthresv=models.CharField(max_length=200,null=True,blank=True)
    precom_pcm=models.FileField(null=True,blank=True)
    precom_others=models.FileField(null=True,blank=True)
    action=models.CharField(max_length=200,null=True,blank=True)
    approval_role=models.CharField(max_length=200,null=True,blank=True)
    public_connection=models.BooleanField(default=False)


    def __str__(self):
        return self.company_name
