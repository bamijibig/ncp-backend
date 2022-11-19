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
    businesshub=models.ForeignKey(BusinessHub,on_delete=models.CASCADE, null=True,blank=True)
    contractor_name=models.CharField(max_length=250,blank=True)
    con_address=models.CharField(max_length=250,blank=True)
    licensed_no=models.IntegerField(null=True,blank=True)
    tel_no=models.CharField(max_length=100,null=True,blank=True)
    role=models.CharField(max_length=100,null=True,blank=True)
    
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
    #  #Hse_pc_np_d approval
    # isHse_pc_np_d=models.BooleanField(default=False)
    # Hse_pc_np_d_comment=models.TextField(null=True,blank=True)
    # Hse_pc_np_d_date=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    # Hse_pc_np_d_approve=models.BooleanField(default=False)
    # Hse_pc_np_ddissaprove=models.BooleanField(default=False)
    def __str__(self):
        return self.company_name



class technicalEvaluation(models.Model):
    route_survey_mapping=models.CharField(max_length=100,null=True,blank=True)
    load_demand=models.CharField(max_length=100,null=True,blank=True)
    equipment_sizing=models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return self.load_demand