from django.db import models
import random
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser): 
    class Meta:  
        permissions = (('can_user', 'Can link user'),
        ('can_profile', 'Can link profile'),)     
    hosname = models.CharField(max_length=200,db_column='hosname',blank=True, null=True)
    address = models.CharField(max_length=200,db_column='address',blank=True, null=True)
    pincode = models.CharField(max_length=200,db_column='pincode',blank=True, null=True)
    city = models.CharField(max_length=200,db_column='city',blank=True, null=True)
    country = models.CharField(max_length=200,db_column='country',blank=True, null=True)
    phoneno = models.CharField(max_length=200,db_column='phoneno',blank=True, null=True)
    mobileno = models.CharField(max_length=200,db_column='mobileno')   
    slogan = models.CharField(max_length=200,db_column='slogan',blank=True, null=True) 
    tandc = models.CharField(max_length=200,db_column='tandc',blank=True, null=True)     
    profile = models.ImageField(upload_to='profile/',default='hospital-logo.png')
    created_by = models. IntegerField(db_column='created_by',blank=True,null=True)    
    role = models.CharField (max_length=200,db_column='role')      
    status = models.CharField(max_length=200,db_column='status',default=False)    

class Checkupinfo(models.Model):
    class Meta:
        db_table ='Checkupinfo_tbl_IT'
        permissions = (('can_Checkupinfo', 'Can link Checkupinfo'),
        ('can_Dashboard', 'Can link Dashboard'),
        ('can_Tokengen', 'Can link Tokengen'),
        ('can_Emergencychange', 'Can link Emergencychange'),
        ('can_Updatestatus', 'Can link Updatestatus'),
        ('can_Patientvisitingstatus', 'Can link Patientvisitingstatus'),               
        ('can_Patientmonitor', 'Can link Patientmonitor'),
        ('can_Dailyreport', 'Can link Dailyreport'),
        ('can_Tokenstatusreport', 'Can link Tokenstatusreport'),)
    created_by = models. IntegerField(db_column='created_by',blank=True,null=True)  
    emp_id = models. IntegerField(db_column='emp_id',blank=True,null=True)  
    peropno = models.CharField(max_length=100,db_column='peropno')
    tokenno = models.CharField(max_length=100,db_column='tokenno')
    date = models.DateField(auto_now=True,db_column='date')
    consult = models.CharField(max_length=200,db_column='consult')
    name = models.CharField(max_length=200,db_column='name')
    amount = models.FloatField(db_column='amount')
    status = models.CharField(max_length=200,db_column='status')
    ctype = models.CharField(max_length=200,db_column='type')
    cstatus = models.CharField(max_length=200,db_column='cstatus')
    diagnosis = models.CharField(max_length=200,db_column='diagnosis')

class role(models.Model):
    class Meta:
        db_table='Role_tbl_IT'   
        permissions = (('can_role', 'Can link role'),) 
    created_by = models. IntegerField(db_column='created_by',blank=True,null=True)  
    emp_id = models. IntegerField(db_column='emp_id',blank=True,null=True)  
    role = models.CharField(max_length=100,db_column='role')  

class sub_user(models.Model):
    class Meta:
        db_table ='subuser_tbl_HA'
        permissions = (('can_sub_user', 'Can link sub_user'),
        ('can_Addemployee', 'Can link Addemployee'),) 
    created_by = models.CharField(max_length=100,db_column='created_by')
    username = models.CharField(max_length=100,db_column='username')
    email = models.CharField(max_length=100,db_column='email',blank=True, null=True)
    empcode = models.CharField(max_length=100,db_column='empcode',blank=True, null=True)
    dob = models.DateField(max_length=100,db_column='dob',blank=True, null=True)  
    age = models.CharField(max_length=200,db_column='age',blank=True, null=True) 
    bloodgroup = models.CharField(max_length=200,db_column='bloodgroup',blank=True, null=True) 
    gender = models.CharField(max_length=200,db_column='gender',blank=True, null=True)
    address = models.CharField(max_length=200,db_column='address',blank=True, null=True)
    mobileno = models.CharField(max_length=200,db_column='mobileno',blank=True, null=True)
    qualification = models.CharField(max_length=200,db_column='qualification',blank=True, null=True)  
    role = models.CharField(max_length=200,db_column='role',blank=True, null=True)  
    profile = models.ImageField(upload_to='profile/',blank=True,null=True)
    status = models.CharField (max_length=200,db_column='status',default=False)      
    date_join = models.DateField(max_length=200,db_column='date_join') 
    update_join = models.DateField(default=datetime.now,blank=True) 

class opinfo(models.Model): 
    class Meta:
        db_table='opinfo_tbl_IT' 
        permissions = (('can_opinfo', 'Can link opinfo'),
        ('can_Searchip', 'Can link Searchip'),
        ('can_Updateform', 'Can link Updateform'),          
        ('can_Searchopno', 'Can link Searchopno'),)
    created_by = models. IntegerField(db_column='created_by',blank=True,null=True)  
    emp_id = models. IntegerField(db_column='emp_id',blank=True,null=True)   
    peropid = models.CharField(max_length=100,db_column='peropid')
    regdr = models.DateField(auto_now=True,db_column='regdr')
    name = models.CharField(max_length=100,db_column='name')
    addrs = models.CharField(max_length=200,db_column='addrs')
    gender = models.CharField(max_length=200,db_column='gender')
    dob = models.DateField(auto_now=True,db_column='dob')
    age = models.CharField(max_length=200,db_column='age')
    mobileno = models.CharField(max_length=200,db_column='mobileno')
    diagnosis = models.CharField(max_length=200,db_column='diagnosis')  

class DoctorLeaveInfo(models.Model): 
    class Meta:
        db_table='DoctorLeaveInfo_tbl_IT'  
        permissions = (('can_DoctorLeaveInfo', 'Can link DoctorLeaveInfo'),
        ('can_Doctorleavesetting', 'Can link Doctorleavesetting'),) 
    created_by = models. IntegerField(db_column='created_by',blank=True,null=True)  
    emp_id = models. IntegerField(db_column='emp_id',blank=True,null=True)    
    doctorname = models.CharField(max_length=100,db_column='doctorname')
    leavedate = models.DateField(auto_now=True,db_column='leavedate')
    purpose = models.CharField(max_length=100,db_column='purpose')    

class peropidtbl(models.Model):
    class Meta:
        db_table='peropid_tbl_IT'   
        permissions = (('can_peropidtbl', 'Can link peropidtbl'),)          
    created_by = models. IntegerField(db_column='created_by',blank=True,null=True)  
    emp_id = models. IntegerField(db_column='emp_id',blank=True,null=True)  
    peropids = models.CharField(max_length=100,db_column='peropid', primary_key=True) 

class Fee(models.Model):
    class Meta:
        db_table='Fee_tbl_IT'    
        permissions = (('can_Fee', 'Can link Fee'),) 
    created_by = models. IntegerField(db_column='created_by',blank=True,null=True)  
    emp_id = models. IntegerField(db_column='emp_id',blank=True,null=True)   
    status = models.CharField(max_length=100,db_column='status') 
    newnormal = models.CharField(max_length=100,db_column='newnormal') 
    newemer = models.CharField(max_length=100,db_column='newemer') 
    oldnormal = models.CharField(max_length=100,db_column='oldnormal') 
    oldemer = models.CharField(max_length=100,db_column='oldemer') 
    lastupdate = models.CharField(max_length=100,db_column='lastupdate') 

class ComplaintsSetting(models.Model):
    class Meta:
        db_table='ComplaintsSetting_tbl_IT' 
        permissions = (('can_ComplaintsSetting', 'Can link ComplaintsSetting'),
        ('can_complaintform', 'Can link complaintform'),)   
    created_by = models. IntegerField(db_column='created_by',blank=True,null=True)  
    emp_id = models. IntegerField(db_column='emp_id',blank=True,null=True)  
    complaints = models.CharField(max_length=100,db_column='complaints')

class TokenDiagnosis(models.Model):
    class Meta:
        db_table='TokenDiagnosis_tbl_IT'    
        permissions = (('can_TokenDiagnosis', 'Can link TokenDiagnosis'),
        ('can_tokendiagonsisform', 'Can link tokendiagonsisform'),)  
    created_by = models. IntegerField(db_column='created_by',blank=True,null=True)  
    emp_id = models. IntegerField(db_column='emp_id',blank=True,null=True)   
    diagnosis = models.CharField(max_length=100,db_column='diagnosis')

class ComplaintDetails(models.Model):
    class Meta:
        db_table='ComplaintDetails_tbl_IT'
        permissions = (('can_ComplaintDetails', 'Can link ComplaintDetails'),)
    peropid = models.CharField(max_length=100,db_column='peropid')
    dt = models.DateField(auto_now=True,db_column='dt')
    complaint = models.CharField(max_length=100,db_column='complaint')

class DiagnosisSetting(models.Model):
    class Meta:
        db_table='DiagnosisSetting_tbl_IT'    
        permissions = (('can_DiagnosisSetting', 'Can link DiagnosisSetting'),
        ('can_Diagnosisform', 'Can link Diagnosisform'),)
    created_by = models. IntegerField(db_column='created_by',blank=True,null=True)  
    emp_id = models. IntegerField(db_column='emp_id',blank=True,null=True)  
    diagnosis = models.CharField(max_length=100,db_column='diagnosis')

class DiagnosisDetails(models.Model):
    class Meta:
        db_table='DiagnosisDetails_tbl_IT'
        permissions = (('can_DiagnosisDetails', 'Can link DiagnosisDetails'),)
    created_by = models. IntegerField(db_column='created_by',blank=True,null=True)  
    emp_id = models. IntegerField(db_column='emp_id',blank=True,null=True)  
    peropid = models.CharField(max_length=100,db_column='peropid')
    dt = models.DateField(auto_now=True,db_column='dt')
    diagnosis = models.CharField(max_length=100,db_column='diagnosis')

class DrDetails(models.Model):
    class Meta:
        db_table='DrDetails_tbl_IT'
        permissions = (('can_DrDetails', 'Can link DrDetails'),
        ('can_tokenset', 'Can link tokenset'),)
    created_by = models. IntegerField(db_column='created_by',blank=True,null=True)  
    emp_id = models. IntegerField(db_column='emp_id',blank=True,null=True)  
    drname = models.CharField(max_length=100,db_column='drname')
    shortname = models.CharField(max_length=100,db_column='shortname')
    visitingtime = models.CharField(max_length=100,db_column='visitingtime')
    
class KUTtok(models.Model):
    class Meta:
        db_table='KUTtok_tbl_IT'    
        permissions = (('can_KUTtok', 'Can link KUTtok'),)
    created_by = models. IntegerField(db_column='created_by',blank=True,null=True)  
    emp_id = models. IntegerField(db_column='emp_id',blank=True,null=True)  
    tokno = models.CharField(max_length=100,db_column='tokno') 

class NIHtok(models.Model):
    class Meta:
        db_table='NIHtok_tbl_IT'
        permissions = (('can_NIHtok', 'Can link NIHtok'),)
    created_by = models. IntegerField(db_column='created_by',blank=True,null=True)  
    emp_id = models. IntegerField(db_column='emp_id',blank=True,null=True)  
    tokno = models.CharField(max_length=100,db_column='tokno')

class SAMtok(models.Model):
    class Meta:
        db_table='SAMtok_tbl_IT'   
        permissions = (('can_SAMtok', 'Can link SAMtok'),)
    created_by = models. IntegerField(db_column='created_by',blank=True,null=True)  
    emp_id = models. IntegerField(db_column='emp_id',blank=True,null=True)  
    tokno = models.CharField(max_length=100,db_column='tokno')

class PrescriptionDetails(models.Model):
    class Meta:
        db_table='PrescriptionDetails_tbl_IT'
        permissions = (('can_PrescriptionDetails', 'Can link PrescriptionDetails'),)
    created_by = models. IntegerField(db_column='created_by',blank=True,null=True)  
    emp_id = models. IntegerField(db_column='emp_id',blank=True,null=True)  
    perid = models.CharField(max_length=100,db_column='perid')
    tokenid = models.CharField(max_length=100,db_column='tokenid')
    pname = models.CharField(max_length=100,db_column='pname')
    dt = models.DateField(auto_now=True,db_column='dt')
    product = models.CharField(max_length=100,db_column='product')
    qty = models.CharField(max_length=200,db_column='qty')
    morn = models.CharField(max_length=200,db_column='morn')
    after = models.CharField(max_length=200,db_column='after')   
    night = models.CharField(max_length=200,db_column='night')   
    beforefood = models.CharField(max_length=200,db_column='beforefood')   
    afterfood = models.CharField(max_length=200,db_column='afterfood') 

class AppointmentSerial(models.Model):
    class Meta:
        db_table='AppointmentSerial_IT' 
        permissions = (('can_AppointmentSerial', 'Can link AppointmentSerial'),)   
    created_by = models. IntegerField(db_column='created_by',blank=True,null=True)  
    emp_id = models. IntegerField(db_column='emp_id',blank=True,null=True)  
    serialno = models.CharField(max_length=100,db_column='serialno')  

class Appointment(models.Model):
    class Meta:
        db_table='Appointment_tbl_IT'
        permissions = (('can_Appointment', 'Can link Appointment'),
        ('can_Appointmententry', 'Can link Appointmententry'),
        ('can_Appointmentreport', 'Can link Appointmentreport'),)   
    created_by = models. IntegerField(db_column='created_by',blank=True,null=True)  
    emp_id = models. IntegerField(db_column='emp_id',blank=True,null=True)  
    serialno = models.CharField(max_length=100,db_column='serialno')
    patientname = models.CharField(max_length=200,db_column='patientname')
    doctorname = models.CharField(max_length=100,db_column='doctorname')
    dt = models.DateField(db_column='dt')   
    conduct = models.CharField(max_length=200,db_column='conduct')    
    purpose = models.CharField(max_length=200,db_column='purpose')
    status = models.CharField(max_length=200,db_column='status')
    session = models.CharField(max_length=200,db_column='session')          

class LabRequest(models.Model):
    class Meta:
        db_table='LabRequest_tbl_IT'
        permissions = (('can_LabRequest', 'Can link LabRequest'),
        ('can_patinetdetails', 'Can link patinetdetails'),)
    created_by = models. IntegerField(db_column='created_by',blank=True,null=True)  
    emp_id = models. IntegerField(db_column='emp_id',blank=True,null=True)  
    opno = models.CharField(max_length=100,db_column='opno')
    tokno = models.CharField(max_length=100,db_column='tokno')
    dt = models.DateField(auto_now=True,db_column='dt')
    name = models.CharField(max_length=100,db_column='name')
    status = models.CharField(max_length=100,db_column='status')
    labid = models.CharField(max_length=100,db_column='labid')

class LabDetails(models.Model):
    class Meta:    
        db_table='LabDetails_tbl_IT'
        permissions = (('can_LabDetails', 'Can link LabDetails'),)
    created_by = models. IntegerField(db_column='created_by',blank=True,null=True)  
    emp_id = models. IntegerField(db_column='emp_id',blank=True,null=True)  
    opno = models.CharField(max_length=100,db_column='opno')
    tokno = models.CharField(max_length=100,db_column='tokno')
    dt = models.DateField(auto_now=True,db_column='dt')
    sno = models.CharField(max_length=100,db_column='sno')
    groupname = models.CharField(max_length=100,db_column='groupname')
    subgroupname = models.CharField(max_length=100,db_column='subgroupname')
    testname = models.CharField(max_length=100,db_column='testname')
    result = models.CharField(max_length=100,db_column='result')
    refrange = models.CharField(max_length=100,db_column='refrange')
    amount = models.FloatField(db_column='amount')

class ThermalAmount(models.Model):
    class Meta:
        db_table='ThermalAmount_tbl_IT'    
        permissions = (('can_ThermalAmount', 'Can link ThermalAmount'),)   
    created_by = models. IntegerField(db_column='created_by',blank=True,null=True)  
    emp_id = models. IntegerField(db_column='emp_id',blank=True,null=True)  
    opno = models.CharField(max_length=100,db_column='opno')
    tokno = models.CharField(max_length=100,db_column='tokno')
    dt = models.DateField(auto_now=True,db_column='dt')
    test = models.CharField(max_length=100,db_column='test')
    amount = models.FloatField(db_column='amount')    

class Remarks(models.Model):
    class Meta:
        db_table='Remarks_tbl_IT'
        permissions = (('can_Remarks', 'Can link Remarks'),)  
    created_by = models. IntegerField(db_column='created_by',blank=True,null=True)  
    emp_id = models. IntegerField(db_column='emp_id',blank=True,null=True)  
    perop = models.CharField(max_length=100,db_column='perop')
    dt = models.DateField(auto_now=True,db_column='dt')
    remark = models.CharField(max_length=100,db_column='remark')

class Group(models.Model):
    class Meta:
        db_table ='Group_tbl_LS'
        app_label = 'NewH_app'   
        permissions = (('can_Group', 'Can link Group'),) 
    created_by = models. IntegerField(db_column='created_by',blank=True,null=True)  
    emp_id = models. IntegerField(db_column='emp_id',blank=True,null=True)  
    groupname = models.CharField(max_length=100,db_column='groupname')

class TesterInfo(models.Model):
    class Meta:  
        db_table ='TesterInfo_tbl_LS'
        app_label = 'NewH_app'
        permissions = (('can_TesterInfo', 'Can link TesterInfo'),)
    created_by = models. IntegerField(db_column='created_by',blank=True,null=True)  
    emp_id = models. IntegerField(db_column='emp_id',blank=True,null=True)  
    labid = models.CharField(max_length=100,db_column='labid',blank=True, primary_key=True)
    optype = models.CharField(max_length=100,db_column='optype')
    opipid = models.CharField(max_length=100,db_column='opipid')
    date = models.DateField(auto_now=True,db_column='date')    
    patiendname = models.CharField(max_length=100,db_column='patiendname')
    Agesex = models.CharField(max_length=100,db_column='Agesex')
    Drname = models.CharField(max_length=100,db_column='Drname')
    collecttime = models.CharField(max_length=100,db_column='collecttime')
    reporttime = models.CharField(max_length=100,db_column='reporttime')    
    status = models.CharField(max_length=100,db_column='status')
    totalamount = models.CharField(max_length=100,db_column='totalamount')
    paidamoun = models.CharField(max_length=100,db_column='paidamoun')
    balance = models.CharField(max_length=100,db_column='balance')
 
class TestResult(models.Model):
    class Meta:
        db_table ='TestResult_tbl_LS'
        app_label = 'NewH_app'  
        permissions = (('can_TestResult', 'Can link TestResult'),)
    created_by = models. IntegerField(db_column='created_by',blank=True,null=True)  
    emp_id = models. IntegerField(db_column='emp_id',blank=True,null=True)  
    labid = models.CharField(max_length=100,db_column='labid',null=True)         
    groupname = models.CharField(max_length=100,db_column='groupname')
    date = models.DateField(auto_now=True,db_column='dt')
    subgroupname = models.CharField(max_length=100,db_column='subgroupname')
    testname = models.CharField(max_length=100,db_column='testname')
    result = models.CharField(max_length=100,db_column='result')
    refrange = models.CharField(max_length=100,db_column='refrange')
    amount = models.CharField(max_length=100,db_column='amount')  

class SubGroupName(models.Model):
    class Meta:
        db_table ='SubGroupName_tbl_LS'
        app_label = 'NewH_app'   
        permissions = (('can_SubGroupName', 'Can link SubGroupName'),) 
    created_by = models. IntegerField(db_column='created_by',blank=True,null=True)  
    emp_id = models. IntegerField(db_column='emp_id',blank=True,null=True)  
    GroupName = models.CharField(max_length=100,db_column='GroupName')
    SubGroupName = models.CharField(max_length=100,db_column='SubGroupName')

class Test(models.Model):
    class Meta:
        db_table ='Test_tbl_LS'
        app_label = 'NewH_app'   
        permissions = (('can_Test', 'Can link Test'),) 
    created_by = models. IntegerField(db_column='created_by',blank=True,null=True)  
    emp_id = models. IntegerField(db_column='emp_id',blank=True,null=True)  
    GroupName = models.CharField(max_length=100,db_column='GroupName')
    SubGroupName = models.CharField(max_length=100,db_column='SubGroupName')
    TestName = models.CharField(max_length=100,db_column='TestName')
    Unit = models.CharField(max_length=100,db_column='Unit')
    RefRange = models.CharField(max_length=100,db_column='RefRange')
    high = models.FloatField(max_length=100,db_column='high')
    low = models.FloatField(max_length=100,db_column='low')
    Amount = models.FloatField(max_length=100,db_column='Amount')

class DrugInfo(models.Model):
    class Meta:
        db_table ='DrugInfo_tbl_RM'
        app_label = 'NewH_app'        
        permissions = (('can_DrugInfo', 'Can link DrugInfo'),) 
    created_by = models. IntegerField(db_column='created_by',blank=True,null=True)  
    emp_id = models. IntegerField(db_column='emp_id',blank=True,null=True)  
    dt = models.DateField(auto_now=True,db_column='dt')    
    name = models.CharField(max_length=100,db_column='name')
    mfr = models.CharField(max_length=100,db_column='mfr')
    iu = models.CharField(max_length=100,db_column='iu')
    kindprod = models.CharField(max_length=100,db_column='kindprod')
    storeplace = models.CharField(max_length=100,db_column='storeplace')
    stockremaining =models.CharField(max_length=100,db_column='stockremaining')
    stockvalue =models.CharField(max_length=100,db_column='stockvalue')

class IPSerialNo(models.Model):
    class Meta:
        db_table ='IPSerialNo_tbl_IP'
        app_label = 'NewH_app'
        permissions = (('can_IPSerialNo', 'Can link IPSerialNo'),)
    created_by = models. IntegerField(db_column='created_by',blank=True,null=True)  
    emp_id = models. IntegerField(db_column='emp_id',blank=True,null=True)  
    ipno = models.CharField(max_length=100,db_column='ipno') 

class IPInfo(models.Model):
    class Meta:
        db_table ='IPInfo_tbl_IP'
        app_label = 'NewH_app'
        permissions = (('can_IPInfo', 'Can link IPInfo'),
        ('can_Newadmission', 'Can link Newadmission'),
        ('can_Ipdailyreport', 'Can link Ipdailyreport'),
        ('can_Ipmonitor', 'Can link Ipmonitor'),)
    created_by = models. IntegerField(db_column='created_by',blank=True,null=True)  
    emp_id = models. IntegerField(db_column='emp_id',blank=True,null=True)  
    ipno = models.CharField(max_length=100,db_column='ipno') 
    perid = models.CharField(max_length=100,db_column='perid')    
    admitdate = models.DateTimeField(default=datetime.now,blank=True)
    dischargedate = models.DateField(blank=True)
    doctorname = models.CharField(max_length=100,db_column='doctorname')
    name = models.CharField(max_length=100,db_column='name')
    age = models.CharField(max_length=100,db_column='age')
    gender =models.CharField(max_length=100,db_column='gender')
    adres = models.CharField(max_length=100,db_column='adres')
    mobile = models.CharField(max_length=100,db_column='mobile')
    advance = models.CharField(max_length=100,db_column='advance')
    roomtype =models.CharField(max_length=100,db_column='roomtype')
    roomno =models.CharField(max_length=100,db_column='roomno')
    status =models.CharField(max_length=100,db_column='status')

class Roomtype(models.Model):
    class Meta:
        db_table ='Roomtype_tbl_IP'
        app_label = 'NewH_app'
        permissions = (('can_Roomtype', 'Can link Roomtype'),)
    created_by = models. IntegerField(db_column='created_by',blank=True,null=True)  
    emp_id = models. IntegerField(db_column='emp_id',blank=True,null=True)  
    roomtype = models.CharField(max_length=100,db_column='roomtype') 



