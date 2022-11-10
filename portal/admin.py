from django.contrib import admin

# Register your models here.
from .models import ContractorUser,contract_application, technicalEvaluation


# Register your models here.
# admin.site.register(contractor_registration)
# admin.site.register(contract_application)
admin.site.register(technicalEvaluation)



@admin.register(ContractorUser)
class ContractorUserAdmin(admin.ModelAdmin):
    list_display=('contractor_name','licensed_no', 'tel_no','email','reg_date',)
    ordering=('reg_date',)
    search_fields=('contractor_name','licensed_no', 'tel_no','email','reg_date',)
    list_filter=('contractor_name','tel_no','email','reg_date')
@admin.register(contract_application)
class contract_applicationAdmin(admin.ModelAdmin):
    list_display = ('id','contractor', 'company_name', 'connectiontype', 'capacity', 'est_load_of_premises', 'useofpremises','date_of_application','letter_of_donation_dss')
    ordering= ('-date_of_application',)
    search_fields=('id','contractor__id', 'company_name', 'connectiontype', 'capacity', 'est_load_of_premises', 'useofpremises','date_of_application',)
    list_filter=('contractor', 'company_name','date_of_application','connectiontype',)