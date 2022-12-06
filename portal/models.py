from django.db import models

from django.contrib.auth.models import AbstractUser

class Region(models.Model):
    region=models.CharField(max_length=200, null=True, blank=True)
    location=models.CharField(max_length=200,null=True, blank=True)
    regionManager=models.CharField(max_length=200,null=True, blank=True)
    email=models.EmailField(null=True, blank=True)
    phoneNumber=models.CharField(max_length=200,null=True, blank=True)

class BusinessHub(models.Model):
    region=models.ForeignKey(Region,on_delete=models.CASCADE, null=True,blank=True)
    businesshub=models.CharField(max_length=200, null=True, blank=True)
    location=models.CharField(max_length=200,null=True, blank=True)
    hubManager=models.CharField(max_length=200,null=True, blank=True)
    email=models.EmailField(null=True, blank=True)
    phoneNumber=models.CharField(max_length=200,null=True, blank=True)



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

    # @property
    # def group(self):
    #     groups = self.groups.all()
    #     return groups[0].name if groups else None

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

    capacity=  models.CharField(max_length=250,blank=True)
    voltage_ratio=models.CharField(max_length=250,blank=True)
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
    
    

    #user= models.ForeignKey(user)
    letter_of_donation_dss=models.FileField(null=True,blank=True)
    nemsa_test_cert=models.FileField(null=True,blank=True)
    transformer_waranty=models.FileField(null=True,blank=True)
    transformer_test_cert=models.FileField(null=True,blank=True)
   
    date_of_application=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    #md approval
    # isMd=models.BooleanField(default=False)
    # Mdcomment=models.TextField(null=True,blank=True)
    # Md_date=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    # Md_approve=models.BooleanField(default=False)
    # Md_dissaprove=models.BooleanField(default=False)
    #  #tm approval
    # isTm=models.BooleanField(default=False)
    # Tmcomment=models.TextField(null=True,blank=True)
    # Tm_date=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    # Tm_approve=models.BooleanField(default=False)
    # Tm_dissaprove=models.BooleanField(default=False)
    #  #te approval
    # isTe=models.BooleanField(default=False)
    # Tecomment=models.TextField(null=True,blank=True)
    # Tedate=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    # Te_approve=models.BooleanField(default=False)
    # Te_dissaprove=models.BooleanField(default=False)
    # Project details
    Te_Title=models.CharField(max_length=100 ,null=True,blank=True)
    Te_applicant=models.CharField(max_length=100 ,null=True,blank=True)
    Te_dt=models.CharField(max_length=100 ,null=True,blank=True)
    Te_voltagelev=models.CharField(max_length=100 ,null=True,blank=True)
    # finding From the site visits
    Te_vdate=models.DateField(auto_now_add=False,null=True,blank=True)
    Te_estload=models.CharField(max_length=50,null=True,blank=True)
    Te_new4upgrade=models.CharField(max_length=50,null=True,blank=True)
    Te_conworkdone=models.CharField(max_length=50,null=True,blank=True)
    Te_dtsubname=models.CharField(max_length=200,null=True,blank=True)
    # though already a te must belong to rh &bh
    Te_region=models.CharField(max_length=200,null=True,blank=True) 
    Te_bhub=models.CharField(max_length=200,null=True,blank=True)
    Te_comentoncon=models.TextField(null=True,blank=True)
    # Recommended feeder/assets for connection
    Te_fdrname=models.CharField(max_length=200,null=True,blank=True)
    Te_fdrcapacity=models.CharField(max_length=200,null=True,blank=True)
    Te_fdrpload=models.CharField(max_length=200,null=True,blank=True)
    Te_tilldate=models.DateField(auto_now_add=False,null=True,blank=True)
    Te_cumloada=models.CharField(max_length=200,null=True,blank=True)
    # Details of source substation
    Te_srcfeeder=models.CharField(max_length=200,null=True,blank=True)
    Te_ptrsf=models.CharField(max_length=200,null=True,blank=True)
    Te_trsfrating=models.CharField(max_length=200,null=True,blank=True)
    Te_trendpeak=models.CharField(max_length=200,null=True,blank=True)
    Te_cumtilldate=models.DateField(auto_now_add=False,null=True,blank=True)
    Te_permload=models.CharField(max_length=200,null=True,blank=True)
    Te_maravail=models.CharField(max_length=200,null=True,blank=True)
    # Approval
    Te_fulspons=models.CharField(max_length=200,null=True,blank=True)
    Te_estpcost=models.CharField(max_length=200,null=True,blank=True)
    # Detailed project report
    # Te_title=models.CharField(max_length=200,null=True,blank=True)
    Te_specoment=models.TextField(null=True, blank=True)
    Te_preamble=models.TextField(null=True, blank=True)
    Te_findings=models.TextField(null=True, blank=True)
    Te_scopework=models.TextField(null=True, blank=True)
    Te_recom=models.TextField(null=True,blank=True)
    # Summary report for relief dss
    #    Project details
    Te_titlepro=models.CharField(max_length=200,null=True,blank=True)
    Te_usercom=models.CharField(max_length=200,null=True,blank=True)
    Te_projmaincat=models.CharField(max_length=200,null=True,blank=True)
    Te_dtrating=models.CharField(max_length=200,null=True,blank=True)
    Te_voltlevel=models.CharField(max_length=200,null=True,blank=True)
    Te_subhead=models.CharField(max_length=200,null=True,blank=True)
    # Te_title=models.CharField(max_length=200,null=True,blank=True)
    # Finding from site visit
    Te_datevisit=models.DateField(auto_now_add=False,null=True,blank=True)
    Te_specloc=models.CharField(max_length=200,null=True,blank=True)
    Te_majchaexidss=models.CharField(max_length=200,null=True,blank=True)
    
    # SUBSTATION ANALYSIS
    nameofsubstation = (
        ('existing substation', 'existing substation'),
        ('proposed substation', 'proposed substation'),
        ('existing substation after relieve', 'existing substation after relieve'),
       
    )
    te_nameofsub = models.CharField(max_length=100, choices=nameofsubstation, default='existing substation')
    Te_rating=models.CharField(max_length=200,null=True,blank=True)
    Te_loading=models.CharField(max_length=200,null=True,blank=True)
    Te_loadpercent=models.CharField(max_length=200,null=True,blank=True)
    Te_2yrsloadproj=models.CharField(max_length=200,null=True,blank=True)
    Te_2yrsloadprojpercent=models.CharField(max_length=200,null=True,blank=True)
    Te_amtbillkwh=models.CharField(max_length=200,null=True,blank=True)
    Te_amtbillnaira=models.CharField(max_length=200,null=True,blank=True)
    Te_collection=models.CharField(max_length=200,null=True,blank=True)
    Te_collectioneff=models.CharField(max_length=200,null=True,blank=True)
    # RECOMMENDED FEEDER/ASSETS FOR CONNECTION
    Te_fdrname2=models.CharField(max_length=200,null=True,blank=True)
    Te_fdravail=models.CharField(max_length=200,null=True,blank=True)
    Te_fdrcapacity2=models.CharField(max_length=200,null=True,blank=True)
    Te_fdrtrendpeak=models.CharField(max_length=200,null=True,blank=True)
    Te_fdrdate=models.DateField(auto_now_add=False,null=True,blank=True)
    Te_cumload2=models.CharField(max_length=200,null=True,blank=True)
    Te_srcfeeder2=models.CharField(max_length=200,null=True,blank=True)

    # PROJECT COST ANALYSIS
    Te_projcost=models.CharField(max_length=200,null=True,blank=True)
    Te_sanctioncost=models.CharField(max_length=200,null=True,blank=True)
    Te_capcontribproj=models.CharField(max_length=200,null=True,blank=True)
    Te_donor=models.CharField(max_length=200,null=True,blank=True)
    Te_ibedc=models.CharField(max_length=200,null=True,blank=True)
    # APPROVAL
    Te_aprovmbgrant=models.CharField(max_length=200,null=True,blank=True)
    Te_recmetertyp=models.CharField(max_length=200,null=True,blank=True)
    Te_statmeter=models.CharField(max_length=200,null=True,blank=True)
    Te_specoment2=models.TextField(null=True,blank=True)
    # ATTACHMENT BY TE
    Te_custreq=models.CharField(max_length=200,null=True,blank=True)
    Te_condiag=models.FileField(null=True,blank=True)
    Te_schdiag=models.FileField(null=True,blank=True)
    Te_sitevform=models.FileField(null=True,blank=True)
    Te_projplanby=models.CharField(max_length=200,null=True,blank=True)


    #  #Hnp_D approval
    # isHnp_D=models.BooleanField(default=False)
    # Hnp_D_comment=models.TextField(null=True,blank=True)
    # Hnp_D_date=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    # Hnp_D_approve=models.BooleanField(default=False)
    # Hnp_D_dissaprove=models.BooleanField(default=False)
    #  #CTO approval
    # isCto=models.BooleanField(default=False)
    # Ctocomment=models.TextField(null=True,blank=True)
    # Ctodate=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    # Ctoapprove=models.BooleanField(default=False)
    # Ctodissaprove=models.BooleanField(default=False)

   # CONTRACTOR NOW REQUEST FOR COMMISSIONING
#    TE FOR PRECOMMISSIONING TEST
    Te2_projtitle=models.CharField(max_length=200,null=True,blank=True)
    Te2_datelstinsp=models.DateTimeField(auto_now_add=False,null=True,blank=True)
    Te2_projobj=models.TextField(null=True,blank=True)
    Te2_supplysrc=models.CharField(max_length=200,null=True,blank=True)
    Te2_fdrname3=models.CharField(max_length=200,null=True,blank=True)
    Te2_peakload=models.CharField(max_length=200,null=True,blank=True)
    Te2_dwndrpcon=models.BooleanField(default=False)
    Te2_distofnss=models.CharField(max_length=200,null=True,blank=True)
    Te2_nopoleht=models.CharField(max_length=200,null=True,blank=True)
    Te2_nopolelt=models.CharField(max_length=200,null=True,blank=True)
    Te2_podeptht=models.CharField(max_length=200,null=True,blank=True)
    Te2_podepthlh=models.CharField(max_length=200,null=True,blank=True)
    Te2_sizeconduct=models.CharField(max_length=200,null=True,blank=True)
    Te2_qtyused=models.CharField(max_length=200,null=True,blank=True)
    Te2_wellallmetalprt=models.BooleanField(default=False)
    Te2_ssfencedibedc=models.BooleanField(default=False)
    Te2_wellgraveled=models.BooleanField(default=False)
    Te2_typfence=models.CharField(max_length=200,null=True,blank=True)
    Te2_nemsavail=models.BooleanField(default=False)
    # Substation Details
    Te2_trsfcap=models.CharField(max_length=200,null=True,blank=True)
    Te2_voltratio=models.CharField(max_length=200,null=True,blank=True)
    Te2_make=models.CharField(max_length=200,null=True,blank=True)
    Te2_sn=models.CharField(max_length=200,null=True,blank=True)
    Te2_current=models.CharField(max_length=200,null=True,blank=True)
    Te2_vectorgrp=models.CharField(max_length=200,null=True,blank=True)
    Te2_impedance=models.CharField(max_length=200,null=True,blank=True)
    Te2_yrsofman=models.CharField(max_length=200,null=True,blank=True)
    Te2_cooling=models.CharField(max_length=200,null=True,blank=True)
    Te2_cabletypsiz=models.CharField(max_length=200,null=True,blank=True)
    Te2_fdrpillarcurr=models.CharField(max_length=200,null=True,blank=True)
    Te2_icomcablesiz=models.CharField(max_length=200,null=True,blank=True)
    Te2_uprizercable=models.CharField(max_length=200,null=True,blank=True)
    Te2_nouprizercable=models.CharField(max_length=200,null=True,blank=True)
    Te2_earthresv=models.CharField(max_length=200,null=True,blank=True)
    Te2_pcm=models.FileField(null=True,blank=True)
    Te2_others=models.FileField(null=True,blank=True)
    
    # head metering approval
    # isHeadmetmodels.BooleanField(default=False)
    # Headmet_comment=models.TextField(null=True,blank=True)
    # Headmet_date=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    # Headmet_approve=models.BooleanField(default=False)
    # Headmet_dissaprove=models.BooleanField(default=False)
    def __str__(self):
        return self.company_name



class technicalEvaluation(models.Model):
    route_survey_mapping=models.CharField(max_length=100,null=True,blank=True)
    load_demand=models.CharField(max_length=100,null=True,blank=True)
    equipment_sizing=models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return self.load_demand