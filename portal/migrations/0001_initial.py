# Generated by Django 4.1.6 on 2023-12-13 15:43

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContractorUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('contractor_name', models.CharField(blank=True, max_length=250)),
                ('con_address', models.CharField(blank=True, max_length=250)),
                ('licensed_no', models.IntegerField(blank=True, null=True)),
                ('tel_no', models.CharField(blank=True, max_length=100, null=True)),
                ('role', models.CharField(blank=True, max_length=100, null=True)),
                ('job_title', models.CharField(blank=True, max_length=100, null=True)),
                ('staff_type', models.CharField(choices=[('hqstaff', 'hqstaff'), ('regionstaff', 'regionstaff'), ('businesshubstaff', 'businesshubstaff'), ('servicecentrestaff', 'servicecentrestaff')], default='hqstaff', max_length=100)),
                ('region', models.CharField(blank=True, max_length=100, null=True)),
                ('businesshub', models.CharField(blank=True, max_length=100, null=True)),
                ('coren_or_nemsa_competency', models.FileField(blank=True, null=True, upload_to='')),
                ('coren', models.FileField(blank=True, null=True, upload_to='')),
                ('reg_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('is_contractor', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_tm', models.BooleanField(default=False)),
                ('is_te', models.BooleanField(default=False)),
                ('is_npd', models.BooleanField(default=False)),
                ('is_cto', models.BooleanField(default=False)),
                ('is_md', models.BooleanField(default=False)),
                ('is_hsch', models.BooleanField(default=False)),
                ('is_hse', models.BooleanField(default=False)),
                ('is_bhm', models.BooleanField(default=False)),
                ('is_hbo', models.BooleanField(default=False)),
                ('is_hm', models.BooleanField(default=False)),
                ('in_approval_workflow', models.BooleanField(default=False)),
                ('registration_status', models.CharField(blank=True, max_length=200, null=True)),
                ('cto_is_contractor_approved', models.BooleanField(default=False)),
                ('cto_is_contractor_approved_date', models.DateField(blank=True, null=True)),
                ('cto_approved_by', models.CharField(blank=True, max_length=200, null=True)),
                ('cto_memo', models.FileField(blank=True, null=True, upload_to='')),
                ('md_is_contractor_approved', models.BooleanField(default=False)),
                ('md_is_contractor_approved_date', models.DateField(blank=True, null=True)),
                ('md_approved_by', models.CharField(blank=True, max_length=200, null=True)),
                ('md_memo', models.FileField(blank=True, null=True, upload_to='')),
                ('declined', models.BooleanField(default=False)),
                ('declined_comment', models.TextField(blank=True, null=True)),
                ('registration_approved', models.BooleanField(default=False)),
                ('action', models.CharField(blank=True, max_length=200, null=True)),
                ('approval_role', models.CharField(blank=True, max_length=200, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='BusinessHub',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('businesshub', models.CharField(blank=True, max_length=200, null=True)),
                ('location', models.CharField(blank=True, max_length=200, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phoneNumber', models.CharField(blank=True, max_length=200, null=True)),
                ('hubManager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='hub_manager', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(blank=True, max_length=200, null=True)),
                ('location', models.CharField(blank=True, max_length=200, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phoneNumber', models.CharField(blank=True, max_length=200, null=True)),
                ('regionManager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='region_manager', to=settings.AUTH_USER_MODEL)),
                ('technicalManager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='region_t_manager', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='contract_application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(blank=True, max_length=100, null=True)),
                ('connectiontype', models.CharField(choices=[('transformer installation', 'transformer installation'), ('transformer uprating', 'transformer uprating'), ('relocation', 'relocation'), ('change of transformer source', 'change of transformer source'), ('others', 'others')], default='transformer installation', max_length=100)),
                ('other_connection', models.CharField(blank=True, max_length=150)),
                ('capacity', models.CharField(choices=[('catd_50kva', 'catd_50kva'), ('catc_100kva', 'catc_100kva'), ('catb_1000kva', 'catb_1000kva'), ('cata_all', 'cata_all')], default='catd_50kva', max_length=100)),
                ('voltage_ratio', models.CharField(choices=[('elevenby400', 'elevenby400'), ('thirtythreeby400', 'thirtythreeby400'), ('thirtythreebyeleven', 'thirtythreebyeleven')], default='elevenby400', max_length=100)),
                ('route_length_km', models.CharField(choices=[('1-10', '1-10'), ('10-20', '10-20'), ('over_20', 'over_20')], default='1-10', max_length=250)),
                ('add_house_no', models.CharField(blank=True, max_length=250)),
                ('add_street', models.CharField(blank=True, max_length=250)),
                ('add_town_or_city', models.CharField(blank=True, max_length=250)),
                ('add_lga', models.CharField(blank=True, max_length=250)),
                ('add_state', models.CharField(blank=True, max_length=250)),
                ('est_load_of_premises', models.CharField(blank=True, max_length=250)),
                ('useofpremises', models.CharField(choices=[('residential', 'residential'), ('commercial', 'commercial'), ('industrial', 'industrial')], default='residential', max_length=100)),
                ('security_receipt', models.FileField(blank=True, null=True, upload_to='')),
                ('letter_of_donation_dss', models.FileField(blank=True, null=True, upload_to='')),
                ('nemsa_test_cert', models.FileField(blank=True, null=True, upload_to='')),
                ('transformer_waranty', models.FileField(blank=True, null=True, upload_to='')),
                ('date_of_application', models.DateTimeField(auto_now_add=True, null=True)),
                ('in_approval_workflow', models.BooleanField(default=False)),
                ('connection_status', models.CharField(blank=True, max_length=200, null=True)),
                ('tm_is_connection_approved', models.BooleanField(default=False)),
                ('tm_is_connection_approved_date', models.DateField(blank=True, null=True)),
                ('tm_is_connection_approved_by', models.CharField(blank=True, max_length=200, null=True)),
                ('tm_memo', models.FileField(blank=True, null=True, upload_to='')),
                ('te_is_connection_approved', models.BooleanField(default=False)),
                ('te_is_connection_approved_date', models.DateField(blank=True, null=True)),
                ('te_is_connection_approved_by', models.CharField(blank=True, max_length=200, null=True)),
                ('te_memo', models.FileField(blank=True, null=True, upload_to='')),
                ('npd_is_connection_approved', models.BooleanField(default=False)),
                ('npd_is_connection_approved_date', models.DateField(blank=True, null=True)),
                ('npd_is_connection_approved_by', models.CharField(blank=True, max_length=200, null=True)),
                ('npd_memo', models.FileField(blank=True, null=True, upload_to='')),
                ('cto_is_connection_approved', models.BooleanField(default=False)),
                ('cto_is_connection_approved_date', models.DateField(blank=True, null=True)),
                ('cto_approved_by', models.CharField(blank=True, max_length=200, null=True)),
                ('cto_memo', models.FileField(blank=True, null=True, upload_to='')),
                ('ct_is_pre_requested', models.BooleanField(default=False)),
                ('ct_is_pre_requested_date', models.DateField(blank=True, null=True)),
                ('tept_is_connection_approved', models.BooleanField(default=False)),
                ('tept_is_connection_approved_date', models.DateField(blank=True, null=True)),
                ('tept_is_connection_approved_by', models.CharField(blank=True, max_length=200, null=True)),
                ('hse_is_connection_approved', models.BooleanField(default=False)),
                ('hse_is_contractor_approved_date', models.DateField(blank=True, null=True)),
                ('hse_approved_by', models.CharField(blank=True, max_length=200, null=True)),
                ('hse_memo', models.FileField(blank=True, null=True, upload_to='')),
                ('bhm_is_connection_approved', models.BooleanField(default=False)),
                ('bhm_is_contractor_approved_date', models.DateField(blank=True, null=True)),
                ('bhm_approved_by', models.CharField(blank=True, max_length=200, null=True)),
                ('bhm_memo', models.FileField(blank=True, null=True, upload_to='')),
                ('hbo_is_connection_approved', models.BooleanField(default=False)),
                ('hbo_is_contractor_approved_date', models.DateField(blank=True, null=True)),
                ('hbo_approved_by', models.CharField(blank=True, max_length=200, null=True)),
                ('hbo_memo', models.FileField(blank=True, null=True, upload_to='')),
                ('hm_is_connection_approved', models.BooleanField(default=False)),
                ('hm_is_contractor_approved_date', models.DateField(blank=True, null=True)),
                ('hm_approved_by', models.CharField(blank=True, max_length=200, null=True)),
                ('hm_memo', models.FileField(blank=True, null=True, upload_to='')),
                ('declined', models.BooleanField(default=False)),
                ('declined_comment', models.TextField(blank=True, null=True)),
                ('connection_approved', models.BooleanField(default=False)),
                ('eval_applicant', models.CharField(blank=True, max_length=250, null=True)),
                ('eval_voltage_level', models.CharField(choices=[('elevenkv', 'elevenkv'), ('thirtythreekv', 'thirtythreekv'), ('fourhundred', 'fourhundred')], default='elevenkv', max_length=100)),
                ('eval_dt', models.CharField(blank=True, max_length=250, null=True)),
                ('eval_estimated_load', models.CharField(blank=True, max_length=250, null=True)),
                ('eval_site_visit_date', models.CharField(blank=True, max_length=250, null=True)),
                ('eval_new4upgrade', models.CharField(blank=True, max_length=50, null=True)),
                ('eval_conworkdone', models.CharField(blank=True, max_length=50, null=True)),
                ('eval_dtsubname', models.CharField(blank=True, max_length=200, null=True)),
                ('eval_region', models.CharField(blank=True, max_length=200, null=True)),
                ('eval_bhub', models.CharField(blank=True, max_length=200, null=True)),
                ('eval_comentoncon', models.TextField(blank=True, null=True)),
                ('eval_fdrname', models.CharField(blank=True, max_length=200, null=True)),
                ('eval_fdrcapacity', models.CharField(blank=True, max_length=200, null=True)),
                ('eval_fdrpload', models.CharField(blank=True, max_length=200, null=True)),
                ('eval_tilldate', models.CharField(blank=True, max_length=250, null=True)),
                ('eval_cumloada', models.CharField(blank=True, max_length=200, null=True)),
                ('eval_srcfeeder', models.CharField(blank=True, max_length=200, null=True)),
                ('eval_ptrsf', models.CharField(blank=True, max_length=200, null=True)),
                ('eval_trsfrating', models.CharField(blank=True, max_length=200, null=True)),
                ('eval_trendpeak', models.CharField(blank=True, max_length=200, null=True)),
                ('eval_cumtilldate', models.CharField(blank=True, max_length=250, null=True)),
                ('eval_cummwithload', models.CharField(blank=True, max_length=200, null=True)),
                ('eval_permload', models.CharField(blank=True, max_length=200, null=True)),
                ('eval_maravail', models.CharField(blank=True, max_length=200, null=True)),
                ('eval_fulspons', models.CharField(blank=True, max_length=200, null=True)),
                ('eval_estpcost', models.CharField(blank=True, max_length=200, null=True)),
                ('eval_specoment', models.TextField(blank=True, null=True)),
                ('eval_title2', models.CharField(blank=True, max_length=200, null=True)),
                ('eval_preamble', models.TextField(blank=True, null=True)),
                ('eval_findings', models.TextField(blank=True, null=True)),
                ('eval_scopework', models.TextField(blank=True, null=True)),
                ('eval_recom', models.TextField(blank=True, null=True)),
                ('eval_pcm', models.FileField(blank=True, null=True, upload_to='')),
                ('eval_otherdoc', models.FileField(blank=True, null=True, upload_to='')),
                ('eval_titlepro', models.CharField(blank=True, max_length=200, null=True)),
                ('eval_usercom', models.CharField(blank=True, max_length=200, null=True)),
                ('eval_projmaincat', models.CharField(blank=True, max_length=200, null=True)),
                ('eval_dtrating', models.CharField(blank=True, max_length=200, null=True)),
                ('eval_voltlevel', models.CharField(blank=True, max_length=200, null=True)),
                ('eval_subhead', models.CharField(blank=True, max_length=200, null=True)),
                ('eval_title', models.CharField(blank=True, max_length=200, null=True)),
                ('eval_datevisit', models.CharField(blank=True, max_length=250, null=True)),
                ('eval_specloc', models.CharField(blank=True, max_length=200, null=True)),
                ('eval_majchaexidss', models.CharField(blank=True, max_length=200, null=True)),
                ('eval_nameofsub', models.CharField(choices=[('existing substation', 'existing substation'), ('proposed substation', 'proposed substation'), ('existing substation after relieve', 'existing substation after relieve')], default='existing substation', max_length=100)),
                ('eval_rating', models.CharField(blank=True, max_length=200, null=True)),
                ('eval_loading', models.CharField(blank=True, max_length=200, null=True)),
                ('eval_loadpercent', models.CharField(blank=True, max_length=200, null=True)),
                ('eval_2yrsloadproj', models.CharField(blank=True, max_length=200, null=True)),
                ('eval_2yrsloadprojpercent', models.CharField(blank=True, max_length=200, null=True)),
                ('eval_amtbillkwh', models.CharField(blank=True, max_length=200, null=True)),
                ('eval_amtbillnaira', models.CharField(blank=True, max_length=200, null=True)),
                ('eval_collection', models.CharField(blank=True, max_length=200, null=True)),
                ('eval_collectioneff', models.CharField(blank=True, max_length=200, null=True)),
                ('eval_fdrname2', models.CharField(blank=True, max_length=200, null=True)),
                ('eval_fdravail', models.CharField(blank=True, max_length=200, null=True)),
                ('eval_fdrcapacity2', models.CharField(blank=True, max_length=200, null=True)),
                ('eval_fdrtrendpeak', models.CharField(blank=True, max_length=200, null=True)),
                ('eval_fdrdate', models.CharField(blank=True, max_length=250, null=True)),
                ('eval_cumload2', models.CharField(blank=True, max_length=200, null=True)),
                ('eval_srcfeeder2', models.CharField(blank=True, max_length=200, null=True)),
                ('eval_projcost', models.CharField(blank=True, max_length=200, null=True)),
                ('eval_sanctioncost', models.CharField(blank=True, max_length=200, null=True)),
                ('eval_capcontribproj', models.CharField(blank=True, max_length=200, null=True)),
                ('eval_donor', models.CharField(blank=True, max_length=200, null=True)),
                ('eval_ibedc', models.CharField(blank=True, max_length=200, null=True)),
                ('eval_aprovmbgrant', models.CharField(blank=True, max_length=200, null=True)),
                ('eval_recmetertyp', models.CharField(blank=True, max_length=200, null=True)),
                ('eval_statmeter', models.CharField(blank=True, max_length=200, null=True)),
                ('eval_specoment2', models.TextField(blank=True, null=True)),
                ('eval_custreq', models.CharField(blank=True, max_length=200, null=True)),
                ('eval_condiag', models.FileField(blank=True, null=True, upload_to='')),
                ('eval_schdiag', models.FileField(blank=True, null=True, upload_to='')),
                ('eval_sitevform', models.FileField(blank=True, null=True, upload_to='')),
                ('eval_projplanby', models.CharField(blank=True, max_length=200, null=True)),
                ('precom_project_title', models.CharField(blank=True, max_length=250, null=True)),
                ('precom_last_inspection_date', models.CharField(blank=True, max_length=250, null=True)),
                ('precom_project_objectives', models.TextField(blank=True, null=True)),
                ('precom_supplysrc', models.CharField(blank=True, max_length=200, null=True)),
                ('precom_fdrname3', models.CharField(blank=True, max_length=200, null=True)),
                ('precom_peakload', models.CharField(blank=True, max_length=200, null=True)),
                ('precom_dwndrpcon', models.BooleanField(default=False)),
                ('precom_distofnss', models.CharField(blank=True, max_length=200, null=True)),
                ('precom_nopoleht', models.CharField(blank=True, max_length=200, null=True)),
                ('precom_nopolelt', models.CharField(blank=True, max_length=200, null=True)),
                ('precom_podeptht', models.CharField(blank=True, max_length=200, null=True)),
                ('precom_podepthlh', models.CharField(blank=True, max_length=200, null=True)),
                ('precom_sizeconduct', models.CharField(blank=True, max_length=200, null=True)),
                ('precom_qtyused', models.CharField(blank=True, max_length=200, null=True)),
                ('precom_wellallmetalprt', models.BooleanField(default=False)),
                ('precom_ssfencedibedc', models.BooleanField(default=False)),
                ('precom_wellgraveled', models.BooleanField(default=False)),
                ('precom_typfence', models.CharField(blank=True, max_length=200, null=True)),
                ('precom_nemsavail', models.BooleanField(default=False)),
                ('precom_trsfcap', models.CharField(blank=True, max_length=200, null=True)),
                ('precom_voltratio', models.CharField(blank=True, max_length=200, null=True)),
                ('precom_make', models.CharField(blank=True, max_length=200, null=True)),
                ('precom_sn', models.CharField(blank=True, max_length=200, null=True)),
                ('precom_current', models.CharField(blank=True, max_length=200, null=True)),
                ('precom_vectorgrp', models.CharField(blank=True, max_length=200, null=True)),
                ('precom_impedance', models.CharField(blank=True, max_length=200, null=True)),
                ('precom_yrsofman', models.CharField(blank=True, max_length=200, null=True)),
                ('precom_cooling', models.CharField(blank=True, max_length=200, null=True)),
                ('precom_cabletypsiz', models.CharField(blank=True, max_length=200, null=True)),
                ('precom_fdrpillarcurr', models.CharField(blank=True, max_length=200, null=True)),
                ('precom_icomcablesiz', models.CharField(blank=True, max_length=200, null=True)),
                ('precom_uprizercable', models.CharField(blank=True, max_length=200, null=True)),
                ('precom_nouprizercable', models.CharField(blank=True, max_length=200, null=True)),
                ('precom_earthresv', models.CharField(blank=True, max_length=200, null=True)),
                ('precom_pcm', models.FileField(blank=True, null=True, upload_to='')),
                ('precom_others', models.FileField(blank=True, null=True, upload_to='')),
                ('action', models.CharField(blank=True, max_length=200, null=True)),
                ('approval_role', models.CharField(blank=True, max_length=200, null=True)),
                ('public_connection', models.BooleanField(default=False)),
                ('bh', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='portal.businesshub')),
                ('contractor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='usercontractor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='businesshub',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='portal.region'),
        ),
        migrations.AddField(
            model_name='businesshub',
            name='technicalManager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='hub_t_manager', to=settings.AUTH_USER_MODEL),
        ),
    ]
