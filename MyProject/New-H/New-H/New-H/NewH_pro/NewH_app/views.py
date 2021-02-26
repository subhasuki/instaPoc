from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from datetime import date,datetime 
from django.http import JsonResponse
import random
from .models import Checkupinfo,opinfo,ComplaintsSetting,DiagnosisSetting,ComplaintDetails,DiagnosisDetails,Remarks,Group,SubGroupName,Test,LabRequest,LabDetails,ThermalAmount,DrugInfo,PrescriptionDetails,AppointmentSerial,Appointment,TesterInfo,TestResult,DrDetails,KUTtok,NIHtok,SAMtok,peropidtbl,TokenDiagnosis,Fee,DoctorLeaveInfo,IPSerialNo,Roomtype,IPInfo,User,role,sub_user
from django.core import serializers
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
import json 
import re
import pyodbc 
from django.db.models import Sum
import pytz
from django.db.models import DateTimeField, ExpressionWrapper, F
from django.contrib.auth import authenticate, login
from django.contrib.auth import authenticate, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from django.contrib.auth import authenticate, login as django_login
from django.contrib.auth import authenticate, login, logout



@login_required(login_url='/login/')
def index(request):   
    user=request.user # print(user)
    userid=user.id #print(userid) 
    hospital_id=user.created_by      
    if hospital_id is None:
        hospital_id=user.id#print(hospital_id)  
    hosdel = User.objects.filter(id = hospital_id) 
    return render(request,'index.html',{'hosdel':hosdel})

def makeKey():
    key=''
    while len(key)<4:
        n=random.randint(0,9)
        key+=str(n)# print(key)
    k=int(key)    # print(k)
    today = date.today()
    h = str(today.year)+ '-OP-' +str(k)  
    return h

@login_required(login_url='/login/')
def tokengen(request):      
    if request.method == 'GET':     
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id
        docname = DrDetails.objects.all() # print(docname)  
        dialist = DiagnosisSetting.objects.all()   
        token = peropidtbl.objects.last() # print(token)   
        newtoken=token.peropids # print(newtoken)        
        today = date.today()
        yr=today.year                
        newtd=int(str(yr)[-2:]) #print(newtd)
        tokno = str(newtd)+ '-OP-' +str(newtoken)     
        return render(request,'tokengen.html',{'docname':docname,'tokno':tokno,'dialist':dialist})

@login_required(login_url='/login/')
def tokengenshot(request):  
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id
        drtoken = request.GET.get('drtoken', None) # print(drtoken)
        drshrtlist = DrDetails.objects.filter(drname=drtoken).values('shortname')#print(drshrtlist)

        if drtoken == "Dr.S.A.NIHMATHULLAH":
            niktok = NIHtok.objects.all().last()   #print(niktok) 
            xx = niktok.tokno# print(xx)
            result = xx+1 # print(result)
            h =  'NIH'+ str(result)#   print(h)   
        elif drtoken == "Dr.S.M.A.KUTHOOS":
            kuttok = KUTtok.objects.all().last() 
            xx2 = kuttok.tokno# print(xx)
            result2 = xx2+1 #print(xx2)#print(kuttok)
            h = 'KUT'+ str(result2)#    print(h)
        elif drtoken == "Dr.S.SAMINA YASMIN":
            samtok = SAMtok.objects.all().last() 
            xx = samtok.tokno# print(xx)
            result = xx+1#  print(result)
            h =  'SAM'+ str(result)# print(h) 
        else:
            pass  

        data = {'h': h,  }      #print(data)    
        return JsonResponse(data) 

@login_required(login_url='/login/')
def tokengenshot1(request):  
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id
        drtoken = request.GET.get('drtoken1', None) #print(drtoken)
        drshrtlist = DrDetails.objects.filter(drname=drtoken).values('shortname')#print(drshrtlist)

        if drtoken == "Dr.S.A.NIHMATHULLAH":
            niktok = NIHtok.objects.all().last()   #print(niktok) 
            xx = niktok.tokno# print(xx)
            result = xx+1 # print(result)
            h =  'NIH'+ str(result)# print(h)   
        elif drtoken == "Dr.S.M.A.KUTHOOS":
            kuttok = KUTtok.objects.all().last() 
            xx2 = kuttok.tokno# print(xx)
            result2 = xx2+1 #print(xx2)#print(kuttok)
            h = 'KUT'+ str(result2)# print(h)
        elif drtoken == "Dr.S.SAMINA YASMIN":
            samtok = SAMtok.objects.all().last() 
            xx = samtok.tokno# print(xx)
            result = xx+1#  print(result)
            h =  'SAM'+ str(result)# print(h) 
        else:
            pass  
        data = {'h': h,}  #print(data)     
        return JsonResponse(data) 

@login_required(login_url='/login/')
def monitor(request): 
    return render(request,"monitor.html")

@login_required(login_url='/login/')
def doclist(request): 
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id
        select = request.GET.get('select', None)        
        today = date.today()        
        oplist = Checkupinfo.objects.filter(date=today,consult=select,status="Normal",cstatus = "Waiting")          
        docsearch =  serializers.serialize('json', oplist)      #print(docsearch) 
        opemlist = Checkupinfo.objects.filter(date=today,consult=select,status="Emergency",cstatus = "Waiting")              
        docsearch1 =  serializers.serialize('json', opemlist)   #print(docsearch1)  
        Finishnoprmal = Checkupinfo.objects.filter(date=today,consult=select,status="Normal",cstatus = "Finish")              
        Finishnoprmal =  serializers.serialize('json', Finishnoprmal) 
        Finishemergency = Checkupinfo.objects.filter(date=today,consult=select,status="Emergency",cstatus = "Finish")              
        Finishemergency =  serializers.serialize('json', Finishemergency) #        print(Finishnoprmal)            
        data = { 'docsearch':docsearch,
            'docsearch1':docsearch1,
            'Finishnoprmal':Finishnoprmal,
            'Finishemergency':Finishemergency,}
        return JsonResponse(data)        

@login_required(login_url='/login/')
def patientdetail(request):  
    return render(request,'patientdetails.html')

@login_required(login_url='/login/')
def patientdetails(request,pk):    # plist = Checkupinfo.objects.filter(id=pk)
    user=request.user # print(username)
    userid=user.id # print(userid) 
    hospital_id=user.created_by    
    if hospital_id is None:
        hospital_id=user.id
    plisttest = Checkupinfo.objects.get(id=pk)   # print(plist)
    galist = plisttest.peropno                   # print(galist) 
    detail = opinfo.objects.filter(peropid=galist)   
    plist = Checkupinfo.objects.filter(peropno=galist).order_by('-id')   # print(queryset)
    tokenlist =  Checkupinfo.objects.filter(peropno=galist).order_by('-id')[:1]   #print(tokenlist)
    com = ComplaintsSetting.objects.all()   # print(l)
    des = DiagnosisSetting.objects.all()    # print(l)
    lab1 = Group.objects.values('groupname')
    product = DrugInfo.objects.values('name','kindprod')
    return render(request,'patientdetails.html',{'users':plist,'galist':galist,'tokenlist':tokenlist,'detail':detail,'com':com,'des':des,'lab1':lab1,'product':product})

@login_required(login_url='/login/')
def calculateAge(request):
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id
        tndob = request.GET.get('tndob', None)   #print(tndob)
        todate = datetime.strptime(tndob,"%Y-%m-%d")
        today = date.today() 
        userage = today.year - todate.year - ((today.month, today.day) < (todate.month, todate.day))       
        data = {'user': userage}
        return JsonResponse(data)

@login_required(login_url='/login/')
def calculateAge1(request):
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id
        tndob1 = request.GET.get('tndob1', None)   #print(tndob)
        todate =datetime.strptime(tndob1,"%Y-%m-%d")
        today = date.today() 
        userage = today.year - todate.year - ((today.month, today.day) < (todate.month, todate.day))       
        data = {'user': userage}
        return JsonResponse(data)

@login_required(login_url='/login/')
def createThing(request):
    if (request.method == 'POST'):
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id
        ss = request.POST['sname']   #print(ss)
        key=makeKey()   #print(key)       

@login_required(login_url='/login/')
def KUT(request):
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id
        tnconsult = request.GET.get('tnconsult', None)   # print(tnconsult)   
        data = { 'user': userage }
        return JsonResponse(data)  

@login_required(login_url='/login/')
def jdatasave(request):
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id
        jcdata1 = request.GET.get('jcdata', None) #print(jcdata1)
        pid1 = request.GET.get('galist', None) # print(pid1)
        today = date.today()  #  print(jcdata1)
        jddata1 = request.GET.get('jddata', None) # print(jddata1) 
        jremark1 = request.GET.get('jremark', None)# print(jremark1)
        JsonDatas1 = json.loads(str(jcdata1)) #print(JsonDatas1)
        JsonDatas2 = json.loads(str(jddata1))  #print(JsonDatas2)          
        JsonDatas3 = json.loads(str(jremark1))
        for i in JsonDatas1:
            s = i   #print(s['Complaints'])
            complaint = s['Complaints']
            obj = ComplaintDetails.objects.create(complaint = complaint,dt = today,peropid = pid1)#   print(obj)           
        for j in JsonDatas2:
            ss = j  #print(ss['Diagnosis'])
            diagnosis = ss['Diagnosis']
            obj1 = DiagnosisDetails.objects.create(diagnosis = diagnosis,dt = today,peropid = pid1) # print(obj1)       
        for k in JsonDatas3:
            sss = k   #print(s['Complaints'])
            remark = sss['Remark']
            obj2 =  Remarks.objects.create(remark = remark,dt = today,perop = pid1)#    print(obj2)
        remfil = Remarks.objects.filter(dt=today,perop = pid1)  #print(comfil)
        remfil = serializers.serialize('json', remfil)#      print(remfil)
        comfil = ComplaintDetails.objects.filter(dt=today,peropid = pid1)  #print(comfil)
        comfil =  serializers.serialize('json', comfil)  
        diafil = DiagnosisDetails.objects.filter(dt=today,peropid = pid1)  #print(comfil)
        diafil =  serializers.serialize('json', diafil)
        data = {
            'comfil': comfil,   
            'diafil': diafil,
            'remfil': remfil,                 
        }   #print(data)
        return JsonResponse(data)

@login_required(login_url='/login/')
def labdatafetch(request):
    if request.method == 'GET': 
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id      
        today = date.today()              
        group = request.GET.get('group', None)  #print(group)        
        lab = SubGroupName.objects.filter(GroupName=group).values('SubGroupName') #print(lab)
        data = {'lab': list(lab)}
        return JsonResponse(data)

@login_required(login_url='/login/')
def labdatafetch1(request):
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
           hospital_id=user.id
        supgroup = request.GET.get('supgroup', None)  # print(supgroup)
        checkdt = Test.objects.filter(SubGroupName=supgroup)
        chfil =  serializers.serialize('json', checkdt)  # print(chfil)
        data = {'chfil': chfil}
        return JsonResponse(data)

@login_required(login_url='/login/')
def labdatasave(request):    
    if request.method == 'GET': 
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id
        grpdata = request.GET.get('grpdata', None)    #print(grpdata) 
        supdata = request.GET.get('supdata', None)    #print(supdata)
        pid1 = request.GET.get('galist', None)
        name1 = request.GET.get('namelist', None)
        token1 = request.GET.get('tokenlist', None)
        genter1 = request.GET.get('genterlist', None)
        age1 = request.GET.get('agelist', None)        
        today = date.today() 
        tbl1sonDatasgrp = json.loads(str(grpdata))
        tbl2sonDatassup = json.loads(str(supdata)) 
        #if grpdata is None:
        obj = LabRequest.objects.create(opno = pid1,tokno = token1, dt = today,name = name1,status = "Assign",labid = "Idnotassign") # print(obj) # print(obj) 
        k=1      
        for i in tbl1sonDatasgrp:           # print(k)
            s = i   #print(s['Complaints'])
            groupname = s['GroupName']
            subgroupname = s['SubGroupName']
            testname = s['Test']
            refrange = s['ReferRange']
            amount = s['Amount']            
            obj1 = LabDetails.objects.create(opno = pid1,tokno = token1, dt = today,sno = k, groupname = groupname, subgroupname = subgroupname, testname = testname,result = "Null", refrange = refrange, amount = amount)     #print(obj1)
            k = k+1        
        for j in tbl2sonDatassup:            
            ss = j   #print(s['Complaints'])   #print(ss)
            testname = ss['Name']
            amount = s['Amount']   #print(testname)                       
            obj2 = ThermalAmount.objects.create(opno = pid1,tokno = token1, dt = today, test = testname, amount = amount)    # print(obj2)
        #if grpdata is None:
        to_update = Checkupinfo.objects.filter(peropno = pid1).update(cstatus = "Lab")  # print(to_update)
        data = { 'comfil': 1,  } #print(data)      
        return JsonResponse(data)

@login_required(login_url='/login/')
def productsavecomplaint(request):       
    if request.method == 'GET':
        today = date.today() 
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id
        id = request.GET.get('id', None)      
        pid1 = request.GET.get('galist', None)
        oldcomplaint = request.GET.get('complaint', None)    #print(oldcomplaint) 
        ComplaintDetails.objects.filter(dt=today,peropid = pid1).filter(id=id).update(complaint = oldcomplaint) #  print(to_updatenewcomplaint)
    to_updatenewcomplaint = ComplaintDetails.objects.get(id=id)# print(to_updatenewcomplaint) 
    to_updatenewcomplaint =  serializers.serialize('json', [to_updatenewcomplaint])#print(to_updatenewcomplaint)  
    data = {'to_updatenewcomplaint': to_updatenewcomplaint,}   
    return JsonResponse(data)

@login_required(login_url='/login/')
def productsavediagnosis(request): 
    today = date.today()       
    if request.method == 'GET': 
       user=request.user # print(username)
       userid=user.id # print(userid) 
       hospital_id=user.created_by    
       if hospital_id is None:
          hospital_id=user.id 
       id = request.GET.get('ids', None)      
       pid1 = request.GET.get('galist', None)
       olddiagnosis = request.GET.get('diagnosis', None)  #       print(olddiagnosis) 
       DiagnosisDetails.objects.filter(dt=today,peropid = pid1).filter(id=id).update(diagnosis = olddiagnosis) #  print(to_updatenewdiagnosis)
    to_updatenewdiagnosis  = DiagnosisDetails .objects.get(id=id)
    to_updatenewdiagnosis  = serializers.serialize('json', [to_updatenewdiagnosis])#print(to_updatenewdiagnosis)  
    data = {'to_updatenewdiagnosis': to_updatenewdiagnosis,}   #print(data)                   
    return JsonResponse(data)   

@login_required(login_url='/login/')
def productsaveremark(request): 
    today = date.today()   
    if request.method == 'GET': 
       user=request.user # print(username)
       userid=user.id # print(userid) 
       hospital_id=user.created_by    
       if hospital_id is None:
           hospital_id=user.id
       id = request.GET.get('idr1', None)      
       pid1 = request.GET.get('galist', None)
       oldremark = request.GET.get('remark', None)  #       print(oldremark) 
    Remarks.objects.filter(dt=today,perop = pid1).filter(id=id).update(remark = oldremark) #  print(to_updatenewremark)
    to_updatenewremark = Remarks.objects.get(id=id)
    to_updatenewremark = serializers.serialize('json', [to_updatenewremark])
    data = {'to_updatenewremark': to_updatenewremark, }  #print(data)  
    return JsonResponse(data) 

@login_required(login_url='/login/')
def perscrproduct(request): 
    user=request.user # print(username)
    userid=user.id # print(userid) 
    hospital_id=user.created_by    
    if hospital_id is None:
        hospital_id=user.id
    product = DrugInfo.objects.values('name','kindprod') # print(product)
    data = {'product': list(product),}   # print(data)               
    return JsonResponse(data) 

@login_required(login_url='/login/')
def perscrpitionsave(request):
    today = date.today()    
    if request.method == 'GET': 
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
             hospital_id=user.id
        prohidname = request.GET.get('prohidname', None)  # print(prohidname)        
        pid1 = request.GET.get('galist', None)           # print(pid1)
        name1 = request.GET.get('namelist', None)     # print(name1)
        token1 = request.GET.get('tokennolist', None)  #print(token1)
        tbl1sonDatasgrp = json.loads(str(prohidname))        
        for i in tbl1sonDatasgrp:   
            s = i  
            product = s['Product Name']   # print('product=>>>'+product)
            qty = s['Qty']          # print(product)
            morn = s['Morning']     # print(morn)
            after = s['AfterNoon']  #  print(after)
            night = s['Night']
            beforefood = s['Before Food']
            afterfood = s['After Food']
            productobj1 = PrescriptionDetails.objects.create(perid = pid1,tokenid = token1,pname = name1, dt = today,product = product, qty = qty, morn = morn,after = after, night = night, beforefood = beforefood,afterfood=afterfood)  # print(productobj1)           
        to_update = Checkupinfo.objects.filter(peropno = pid1).update(cstatus="Finish")  #print(to_update)
        data = { 'save':True, } #'productobj1': productobj1,#'to_update' : to_update,  #print(data)           
        return JsonResponse(data)

@login_required(login_url='/login/')
def appoinmentsave(request):
    today = date.today()    
    if request.method == 'GET': 
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id
        mobileno = request.GET.get('mobileno', None)#   print(mobileno)        
        consult = request.GET.get('consult', None)   #  print(consult) 
        datepicker = request.GET.get('datepicker', None) # print(datepicker)
        psession = request.GET.get('psession', None) # print(psession)
        namelist =  request.GET.get('namelist', None) 
        objectseial = AppointmentSerial.objects.last()  # print(objectseial.serialno)
        num = objectseial.serialno
        num = num + 1#   print(num)
        objectseialfinal = AppointmentSerial.objects.create(serialno=num)# print(objectseialfinal)
        snumber= 'A' + str(num)#print(snumber) 
        obj = Appointment.objects.create(serialno=snumber,patientname=namelist,doctorname=consult,dt=today,conduct=mobileno,purpose='-',status ='Booked',session= psession)#print(obj)
    data = {'save':1,}   
    return JsonResponse(data)

@login_required(login_url='/login/') 
def otherupdate(request):
    today = date.today()    
    if request.method == 'GET':    
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id            
        consult = request.GET.get('consult', None) # print(consult) 
        pid1 = request.GET.get('galist', None)      #  print(pid1)       
        token1 = request.GET.get('tokennolist', None)  # print(token1)
        othername = request.GET.get('othername', None) # print(othername)
        to_updated = Checkupinfo.objects.filter(peropno = pid1).update(cstatus=othername)  #print(to_updated)
        data = {'save': True } #print(list(labresult))
        return JsonResponse(data) 

@login_required(login_url='/login/')
def inkA4(request):  
    today = date.today()  
    if request.method == 'POST':  
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id  
        pid = request.POST.get('pidname') #print(pid)
        detail = opinfo.objects.filter(peropid=pid) #print(detail)
        tokenlist =  Checkupinfo.objects.filter(peropno=pid).order_by('-id')[:1] #print(tokenlist)
        bp = request.POST.get('bp')  #print(bp)  
        pb = request.POST.get('pb')  #print(pb)  
        spo2 = request.POST.get('spo2')  #print(spo2)  
        temp = request.POST.get('temp')  #print(temp)  
        wt = request.POST.get('wt')     #print(wt)
        productobj1 = PrescriptionDetails.objects.filter(perid = pid)  #print(productobj1)    
        Complaintlist = ComplaintDetails.objects.filter(peropid = pid)  #print(Complaintlist) 
        Diagnosislist = DiagnosisDetails.objects.filter(peropid = pid)  #print(Diagnosislist) 
        Remarkslist = Remarks.objects.filter(perop = pid)  #print(Remarkslist)         
        context={'today':today,'pid':pid,'pb':pb,'bp':bp,'spo2':spo2,
        'temp':temp,'wt':wt,'tokenlist':tokenlist,'detail':detail,
        'productobj1':productobj1,'Complaintlist':Complaintlist,
        'Diagnosislist':Diagnosislist,'Remarkslist':Remarkslist}
        return render(request,'inkA4.html',context)
    else:
        return render(request, 'inkA4.html') 

@login_required(login_url='/login/')
def todaylabupdate(request):  
    today = date.today()# print(today)
    if request.method == 'GET':
      user=request.user # print(username)
      userid=user.id # print(userid) 
      hospital_id=user.created_by    
      if hospital_id is None:
        hospital_id=user.id           
      pid1 = request.GET.get('peropno', None) # print(pid1)
      opid = request.GET.get('opid', None) #  print(opid)
      labid1 = TesterInfo.objects.filter(date=today).filter(opipid=pid1).values('labid','status')#print(labid1) 
      for i in labid1:  
        j =  i['labid'] #  print(j)
      if j != '':  
        labresult = TestResult.objects.filter(labid=j).values('groupname','subgroupname','testname','result','refrange')# print(labresult)         
        data = {'labresult': list(labresult)} #print(list(labresult))
        return JsonResponse(data) 
      else:
        data = {'save': True} #print(list(labresult))
        return JsonResponse(data)

@login_required(login_url='/login/')
def feesave(request):
    today = date.today() 
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id  
        feestatus = request.GET.get('feestatus') # print(feestatus) 
        if feestatus == "Normal":           
            connection = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-EB1CMRU;'
                      'Database=DynamicHospital;'
                      'Trusted_Connection=yes;')
            # cursor = conn.cursor()
            cursor= connection.cursor()        
            cursor.execute("select newnormal from Fee_tbl")            
            row = cursor.fetchall()  #  print(row)            
            for fest in row:
                if fest:# print(fest)
                    for fest1 in fest:
                        if fest1: 
                            print(fest1)
            connection.commit() 
            connection.close() 
        elif feestatus == "Emergency":           
            connection = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-EB1CMRU;'
                      'Database=DynamicHospital;'
                      'Trusted_Connection=yes;')
            # cursor = conn.cursor()
            cursor= connection.cursor()        
            cursor.execute("select newemer from Fee_tbl")            
            row = cursor.fetchall()  #  print(row)            
            for fest in row:
                if fest:# print(fest)
                    for fest1 in fest:
                        if fest1:
                            print(fest1)
            connection.commit() 
            connection.close()                   
        data = {'fest1': fest1} 
        print(fest1)
        return JsonResponse(data)

@login_required(login_url='/login/')
def feesave1(request):
    today = date.today() 
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id  
        feestatus1 = request.GET.get('feestatus1')#print(feestatus1) 
        if feestatus1 == "Normal":           
            connection = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-EB1CMRU;'
                      'Database=DynamicHospital;'
                      'Trusted_Connection=yes;')
            # cursor = conn.cursor()
            cursor= connection.cursor()        
            cursor.execute("select oldnormal from Fee_tbl")            
            row = cursor.fetchall()  #  print(row)            
            for fest in row:
                if fest:# print(fest)
                    for fest1 in fest:
                        if fest1:
                            print(fest1)
            connection.commit() 
            connection.close() 
        elif feestatus1 == "Emergency":           
            connection = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-EB1CMRU;'
                      'Database=DynamicHospital;'
                      'Trusted_Connection=yes;')
            # cursor = conn.cursor()
            cursor= connection.cursor()        
            cursor.execute("select oldemer from Fee_tbl")            
            row = cursor.fetchall()  #  print(row)            
            for fest in row:
                if fest:# print(fest)
                    for fest1 in fest:
                        if fest1:
                            print(fest1)
            connection.commit() 
            connection.close()                   
        data = {'fest1': fest1} # print(fest1)
        return JsonResponse(data)

@login_required(login_url='/login/')
def pdetailssave(request):
    today = date.today()    
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id  
        tnid = request.GET.get('tnid', None) #  print(tnid)   
        temp1 = re.findall(r'\d+', tnid) # through regular expression
        res2 = list(map(int, temp1)) # print(res2)       
        gg = list(res2[:2]) # print(gg)
        restok1 = gg[1] # print(restok1)
        drtoken = request.GET.get('drtoken', None) # print(drtoken) 
        tokenid = request.GET.get('tokenid', None) #  print(tokenid) 
        tnname = request.GET.get('tnname', None)  # print(tnname)       
        tgenter = request.GET.get('tgenter', None) # print(tgenter) 
        tnage = request.GET.get('tnage', None) # print(tnage)
        feestatus = request.GET.get('feestatus', None) # print(feestatus)
        amount = request.GET.get('amount', None) #  print(amount) 
        tnplace = request.GET.get('tnplace', None) # print(tnplace)
        tndob = request.GET.get('tndob', None) # print(tndob)
        tnmobile = request.GET.get('tnmobile', None) # print(tnmobile)
        pdisease = request.GET.get('pdisease', None) # print(pdisease)              
        pdltsave = opinfo.objects.create(peropid = tnid,regdr = today,
                name = tnname,addrs=tnplace,gender=tgenter,dob=tndob,age=tnage,
                mobileno=tnmobile,diagnosis=pdisease) #  print(pdltsave)            
        pchecksave = Checkupinfo.objects.create(peropno=tnid,tokenno=tokenid, 
            date=today,consult=drtoken,name=tnname,amount=amount,status= feestatus,
            diagnosis=pdisease,ctype="New",cstatus = "Waiting") #  print(pchecksave) 
        # pchecksavefetch =  serializers.serialize('json', pchecksave)    
        perposave = peropidtbl.objects.create(peropids=restok1) #    print(perposave)
        spshtdoc =  Checkupinfo.objects.last() #  print(spshtdoc)       
        docnum = spshtdoc.tokenno # print(docnum)        
        m = re.match(r"([a-zA-Z]+)([0-9]+)",docnum)         
        m1 = m.group(1)
        ms = str(m1) # print (ms)         
        if ms == "NIH":            
            m2 = m.group(2) # print (m2) # z = int(m2)  
            # shtresult = z+1  # print(shtresult)  
            niktok = NIHtok.objects.create(tokno=m2) # print(niktok) 
        elif ms == "SAM":            
            m2 = m.group(2) #  print (m2) # z = int(m2)  
            # shtresult = z+1   # print(shtresult)  
            niktok = SAMtok.objects.create(tokno=m2) #print(samtok)
        elif ms == "KUT":
            m2 = m.group(2) # print (m2) # z = int(m2)  
            # shtresult = z+1  # print(shtresult)  
            niktok = KUTtok.objects.create(tokno=m2) # print(samtok)
        else:
            pass #  print(m2)
        user = {'id':pdltsave.id,'peropid':pdltsave.peropid,
        'addrs':pdltsave.addrs,'gender':pdltsave.gender,'name':pdltsave.name,
        'age':pdltsave.age,'diagnosis':pdltsave.diagnosis
        } #  print(user)
        token = peropidtbl.objects.last() # print(token)   
        newtoken=token.peropids # print(newtoken)
        addtok = int(newtoken)+1 # print(addtok)
        today = date.today()
        yr=today.year                
        newtd=int(str(yr)[-2:]) #print(newtd)
        tokno = str(newtd)+ '-OP-' +str(addtok)  
        user1 = {'status':pchecksave.status,'id':pchecksave.id}
        data = {'user': user,'user1':user1,'tokno':tokno} 
        return JsonResponse(data) 
        
@login_required(login_url='/login/')
def pdetailssave1(request):
    today = date.today()    
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id  
        tnid1 = request.GET.get('oldidsearchnm', None)# print(tnid)        
        temp1 = re.findall(r'\d+', tnid1) # through regular expression
        res2 = list(map(int, temp1)) # print(res2)       
        gg = list(res2[:2]) # print(gg) 
        restok1 = gg[1] # print(restok1)          
        drtoken1 = request.GET.get('drtoken1', None) # print(drtoken) 
        tokenid1 = request.GET.get('tokenid1', None) # print(tokenid) 
        tnname1 = request.GET.get('tnname1', None)  # print(tnname)       
        tgenter1 = request.GET.get('tgenter1', None) # print(tgenter) 
        tnage1 = request.GET.get('tnage1', None) # print(tnage)
        amount1 = request.GET.get('amount1', None) #  print(amount) 
        feestatus1 = request.GET.get('feestatus1', None) # print(feestatus)        
        tnplace1 = request.GET.get('tnplace1', None) # print(tnplace)
        tndob1 = request.GET.get('tndob1', None) # print(tndob)
        tnmobile1 = request.GET.get('tnmobile1', None) # print(tnmobile)
        pdisease1 = request.GET.get('pdisease1', None) # print(pdisease)
        pdltsave = opinfo.objects.create(peropid = tnid1,regdr = today,
                name = tnname1,addrs=tnplace1,gender=tgenter1,dob=tndob1,age=tnage1,
                mobileno=tnmobile1,diagnosis=pdisease1) # print(pdltsave)            
        pchecksave = Checkupinfo.objects.create(peropno=tnid1,tokenno=tokenid1, 
            date=today,consult=drtoken1,name=tnname1,amount=amount1,status= feestatus1,
            diagnosis=pdisease1,ctype="Old",cstatus = "Waiting")  #  print(pchecksave) 
        perposave = peropidtbl.objects.create(peropids=restok1) # print(perposave)
        spshtdoc =  Checkupinfo.objects.last()        
        docnum = spshtdoc.tokenno # print(docnum)        
        m = re.match(r"([a-zA-Z]+)([0-9]+)",docnum)         
        m1 = m.group(1)
        ms = str(m1) # print (ms) 
        
        if ms == "NIH":            
            m2 = m.group(2) # print (m2)
            # z = int(m2)  
            # shtresult = z+1  
            # print(shtresult)  
            niktok = NIHtok.objects.create(tokno=m2) # print(niktok) 
        elif ms == "KUT":            
            m2 = m.group(2) # print (m2)
            # z = int(m2)  
            # shtresult = z+1 
            # print(shtresult)  
            niktok = SAMtok.objects.create(tokno=m2) # print(niktok)
        elif ms == "SAM":
            m2 = m.group(2) # print (m2)
            # z = int(m2)  
            # shtresult = z+1 
            # print(shtresult)  
            niktok = KUTtok.objects.create(tokno=m2) # print(niktok)
        else:
            pass 
        user = {'id':pdltsave.id,'peropid':pdltsave.peropid,
        'addrs':pdltsave.addrs,'gender':pdltsave.gender,'name':pdltsave.name,
        'age':pdltsave.age,'diagnosis':pdltsave.diagnosis} #  print(user)
        user1 = {'status':pchecksave.status,'id':pchecksave.id}
        data = {'user': user,'user1':user1} 
        return JsonResponse(data)

@login_required(login_url='/login/')
def appoinmentcal(request):
    if request.method == 'GET':    
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id    
        aptid = request.GET.get('aptid', None) # print(aptid)   
        aplist = Appointment.objects.filter(serialno=aptid).values('patientname','session')# print(aplist) 
        data = {'aplist': list(aplist)} # print(aplist)
        return JsonResponse(data)

@login_required(login_url='/login/')
def appoinmentcal1(request):
    if request.method == 'GET': 
      user=request.user # print(username)
      userid=user.id # print(userid) 
      hospital_id=user.created_by    
      if hospital_id is None:
        hospital_id=user.id         
      aptid1 = request.GET.get('aptid1', None) # print(aptid)   
      aplist1 = Appointment.objects.filter(serialno=aptid1).values('patientname','session')#print(aplist1) 
      data = {'aplist1': list(aplist1)} #print(aplist1)
      return JsonResponse(data)            

@login_required(login_url='/login/')
def oldidsearch(request):
    if request.method == 'GET':
      user=request.user # print(username)
      userid=user.id # print(userid) 
      hospital_id=user.created_by    
      if hospital_id is None:
        hospital_id=user.id    
      oldidsearchnm = request.GET.get('oldidsearchnm', None) #print(oldidsearchnm) 
      oldlist = opinfo.objects.filter(peropid=oldidsearchnm).values('name','addrs','gender','dob','age','mobileno') # print(oldlist) 
      data = {'oldlist': list(oldlist)}#print(oldlist)
      return JsonResponse(data)

@login_required(login_url='/login/')
def complaints(request): 
    if request.method == 'GET':  
       user=request.user # print(username)
       userid=user.id # print(userid) 
       hospital_id=user.created_by    
       if hospital_id is None:
         hospital_id=user.id       
       pdltfetch = ComplaintsSetting.objects.all() # print(pdltfetch)
       return render(request,'complaints.html',{'pdltfetch':pdltfetch})

@login_required(login_url='/login/')
def saveco(request): 
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id             
        complaint = request.GET.get('complaint', None) # print(complaint)
        if ComplaintsSetting.objects.filter(complaints=complaint).exists():        
            data = {'exist': True}  
            return JsonResponse(data)
        else:     
            pupsave = ComplaintsSetting.objects.create(complaints = complaint)#print(pupsave)   
            user = {'id':pupsave.id,'complaints':pupsave.complaints}     
            data = {'user': user} #   print(data)
            return JsonResponse(data)

@login_required(login_url='/login/')
def updatecomplaint(request): 
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id        
        oldcomplaint = request.GET.get('complaintupdate', None)  # print(oldcomplaint)
        sno = request.GET.get('snoupt', None) # print(sno)      
        upcom = ComplaintsSetting.objects.get(id=sno)  
        upcom.complaints = oldcomplaint
        upcom.save()
        user = {'id':upcom.id,'complaints':upcom.complaints}
        data = {'to_updatenewcomplaint': user, }   
        return JsonResponse(data)

@login_required(login_url='/login/')
def deletecom(request): 
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id        
        comid = request.GET.get('id', None)
        comdlt = ComplaintsSetting.objects.get(id=comid) #  print(comdlt)
        comdlt.delete() # print(comdlt)
        data = {'success': True} # print(data)
        return JsonResponse(data)

@login_required(login_url='/login/')
def diagnosisset(request): 
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id         
        pdltfetch = DiagnosisSetting.objects.all() # print(pdltfetch) 
        return render(request,'diagnosisset.html',{'pdltfetch':pdltfetch})

@login_required(login_url='/login/')
def savecodia(request): 
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id             
        Diagnosis = request.GET.get('Diagnosis', None) # print(complaint)
        if DiagnosisSetting.objects.filter(diagnosis=Diagnosis).exists():        
            data = {'exist': True}  
            return JsonResponse(data)
        else:     
            pupsave = DiagnosisSetting.objects.create(diagnosis = Diagnosis)# print(pupsave)   
            user = {'id':pupsave.id,'diagnosis':pupsave.diagnosis}     
            data = {'user': user}# print(data)
            return JsonResponse(data)

@login_required(login_url='/login/')
def updateDiagnosis(request): 
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id        
        olddiagnosis = request.GET.get('Diagnosisupdate', None)  # print(oldcomplaint)
        sno = request.GET.get('snoupt', None) # print(sno)    
        updia = DiagnosisSetting.objects.get(id=sno)        
        updia.diagnosis = olddiagnosis  # print(olddiagnosis)
        updia.save()
        user = {'id':updia.id,'diagnosis':updia.diagnosis}
        data = {'to_updatenewdiagnosis': user,}   
        return JsonResponse(data)

@login_required(login_url='/login/')
def deletedia(request): 
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id        
        diaid = request.GET.get('id', None)
        diadlt = DiagnosisSetting.objects.get(id=diaid)  # print(diadlt)
        diadlt.delete() # print(diadlt)
        data = {'success': True} # print(data)
        return JsonResponse(data)

@login_required(login_url='/login/')
def tokendisease(request): 
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id         
        pdltfetch = TokenDiagnosis.objects.all() # print(pdltfetch) 
        return render(request,'tokendisease.html',{'pdltfetch':pdltfetch})

@login_required(login_url='/login/')
def savetokdis(request): 
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id             
        Diagnosis = request.GET.get('Diagnosis', None) # print(complaint)
        if TokenDiagnosis.objects.filter(diagnosis=Diagnosis).exists():        
            data = {'exist': True}  
            return JsonResponse(data)
        else:     
            pupsave = TokenDiagnosis.objects.create(diagnosis = Diagnosis) # print(pupsave)   
            user = {'id':pupsave.id,'diagnosis':pupsave.diagnosis}     
            data = {'user': user}# print(data)
            return JsonResponse(data)

@login_required(login_url='/login/')
def updateDisease(request): 
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id        
        olddiagnosis = request.GET.get('Diagnosisupdate', None)  # print(oldcomplaint)
        sno = request.GET.get('snoupt', None) # print(sno)    
        updia = TokenDiagnosis.objects.get(id=sno)        
        updia.diagnosis = olddiagnosis  # print(olddiagnosis)
        updia.save()
        user = {'id':updia.id,'diagnosis':updia.diagnosis}
        data = {'to_updatenewdiagnosis': user, }   
        return JsonResponse(data)

@login_required(login_url='/login/')
def deleteDisease(request): 
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id        
        diaid = request.GET.get('id', None)
        diadlt = TokenDiagnosis.objects.get(id=diaid)  # print(diadlt)
        diadlt.delete() # print(diadlt)
        data = {'success': True} # print(data)
        return JsonResponse(data)

@login_required(login_url='/login/')
def loginset(request): 
    user=request.user # print(username)
    userid=user.id # print(userid) 
    hospital_id=user.created_by    
    if hospital_id is None:
        hospital_id=user.id   
    return render(request,'loginset.html')

@login_required(login_url='/login/')
def loguser(request): 
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id             
        username = request.GET.get('username', None) # print(username)
        userpwd = request.GET.get('userpwd', None)# print(userpwd)
        if username=="RECPASS" and  userpwd=="1REC2PASS3":
           return render(request,'tokesetting.html')      
        else:
           return render(request,'loginset.html')

@login_required(login_url='/login/')       
def tokesetting(request):
    user=request.user # print(username)
    userid=user.id # print(userid) 
    hospital_id=user.created_by    
    if hospital_id is None:
        hospital_id=user.id   
    docname = DrDetails.objects.all()  # print(docname) 
    feedlt = Fee.objects.all() # print(feedlt)
    return render(request,'tokesetting.html',{'docname':docname,'feedlt':feedlt})

@login_required(login_url='/login/')
def doctokengenshot(request):  
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id  
        drtoken = request.GET.get('drtoken', None) #print(drtoken)
        drshrtlist = DrDetails.objects.filter(drname=drtoken).values('shortname')#print(drshrtlist)

        if drtoken == "Dr.S.A.NIHMATHULLAH":
            tok = NIHtok.objects.all() #  print(tok) 
              
        elif drtoken == "Dr.S.M.A.KUTHOOS":
            tok = KUTtok.objects.all() #   print(tok)  
           
        elif drtoken == "Dr.S.SAMINA YASMIN":
            tok = SAMtok.objects.all()  #   print(tok) 
           
        else:
            pass              
        data = {'success': True,}  #print(data)                          
        return JsonResponse(data) 

@login_required(login_url='/login/')
def tokdlt(request):  
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id  
        drtoken = request.GET.get('drtoken', None) #print(drtoken)
        drshrtlist = DrDetails.objects.filter(drname=drtoken).values('shortname')#print(drshrtlist)

        if drtoken == "Dr.S.A.NIHMATHULLAH":
            tok = NIHtok.objects.all().delete()
            tok1 = NIHtok.objects.create(tokno="0") #print(tok1) 
              
        elif drtoken == "Dr.S.M.A.KUTHOOS":
            tok = KUTtok.objects.all().delete()
            tok1 = KUTtok.objects.create(tokno="0") # print(tok1)  
           
        elif drtoken == "Dr.S.SAMINA YASMIN":
            tok = SAMtok.objects.all().delete()
            tok1 = SAMtok.objects.create(tokno="0") # print(tok1) 
           
        else:
            pass              
        data = {'success': True, } #print(data)                         
        return JsonResponse(data) 

@login_required(login_url='/login/')
def checkavail(request): 
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id  
        docname = request.GET.get('docname', None) # print(docname)
        visittime = request.GET.get('visittime', None) # print(visittime)
        shrtname = request.GET.get('shrtname', None)  # print(shrtname)        
        if DrDetails.objects.filter(shortname=shrtname).filter(shortname=shrtname).exists():                   
            data = {'exist': True}  #  print(data)       
        else:
            data = {'exist': False} # print(data)
    return JsonResponse(data)

@login_required(login_url='/login/')       
def savedrname(request): 
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id  
        docname = request.GET.get('docname', None) # print(docname)
        visittime = request.GET.get('visittime', None) # print(visittime)
        shrtname = request.GET.get('shrtname', None)        
        newsrtnm = str(shrtname)+'tok_tbl' #  print(newsrtnm)
        grdlts = DrDetails.objects.create(drname=docname,shortname=shrtname,visitingtime=visittime)
        user = {'id':grdlts.id,'drname':grdlts.drname,'shortname':grdlts.shortname,'visitingtime':grdlts.visitingtime}                    
        connection = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-EB1CMRU;'
                      'Database=DynamicHospital;'
                      'Trusted_Connection=yes;')
        # cursor = conn.cursor()
        cursor= connection.cursor()
        cursor.execute('''CREATE TABLE ''' + newsrtnm + ''' (id bigint, tokno varchar(255));''')       
        connection.commit() #print("Data Successfully Inserted")   
        connection.close()
        data = {'user': user,
        'newsrtnm' : newsrtnm} # print(data)
        return JsonResponse(data) 

@login_required(login_url='/login/')
def updatedrdetails(request): 
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id            
        sno = request.GET.get('snoupt', None) # print(sno)   
        drname = request.GET.get('drname', None)  # print(drname) 
        visitingtime = request.GET.get('visitingtime', None)  # print(visitingtime)   
        updrdtl = DrDetails.objects.get(id=sno)  
        updrdtl.drname = drname
        updrdtl.visitingtime = visitingtime
        updrdtl.save()
        user = {'id':updrdtl.id,'drname':updrdtl.drname,'visitingtime':updrdtl.visitingtime}
        data = {'to_updatenewdrdtl': user}    
        return JsonResponse(data)

@login_required(login_url='/login/')
def deletedrdtl(request): 
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id       
        drdltid = request.GET.get('id', None) 
        shortname = request.GET.get('shortname', None)# print(shrtdrdtl)
        newsrtnm = str(shortname)+'tok_tbl' 
        connection = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-EB1CMRU;'
                      'Database=DynamicHospital;'
                      'Trusted_Connection=yes;')
        # cursor = conn.cursor()
        cursor= connection.cursor()
        cursor.execute('''DROP TABLE ''' + newsrtnm + ''';''')       
        connection.commit() #print("Data Successfully Inserted")   
        connection.close() 
        drdlt = DrDetails.objects.get(id=drdltid)  # print(diadlt)
        drdlt.delete()       
        data = {'success': True} # print(data)
        return JsonResponse(data)    

@login_required(login_url='/login/')        
def updatefee(request): 
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id     
        feeid =  request.GET.get('feeid', None)  
        newnormal = request.GET.get('newnormal', None)# print(shrtdrdtl)
        newemer = request.GET.get('newemer', None) 
        oldnormal = request.GET.get('oldnormal', None)
        oldemer = request.GET.get('oldemer', None)
        lastupdate = request.GET.get('lastupdate', None)
        updateprof = Fee.objects.get(id=feeid) 
        updateprof.newnormal = newnormal
        updateprof.newemer = newemer
        updateprof.oldnormal = oldnormal
        updateprof.oldemer = oldemer
        #updateprof.lastupdate = lastupdate ,'lastupdate':updateprof.lastupdate
        updateprof.save()
        user = {'id':updateprof.id,'newnormal':updateprof.newnormal,'newemer':updateprof.newemer,'oldnormal':updateprof.oldnormal,'oldemer':updateprof.oldemer} 
        data = {'to_updatefee': user }    
        return JsonResponse(data)

@login_required(login_url='/login/')
def dailyreport(request):
    user=request.user # print(username)
    userid=user.id # print(userid) 
    hospital_id=user.created_by    
    if hospital_id is None:
        hospital_id=user.id   
    docname = DrDetails.objects.all()  # print(docname)    
    return render(request,'dailyreport.html',{'docname':docname} )

@login_required(login_url='/login/')
def searchop(request): 
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id     
        docname =  request.GET.get('docname', None)  #   print(docname)
        fromdt = request.GET.get('fromdt', None) #  print(fromdt)
        todt = request.GET.get('todt', None) #   print(todt)  
        connection = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-EB1CMRU;'
                      'Database=DynamicHospital;'
                      'Trusted_Connection=yes;')
        cursor= connection.cursor()
        query='''select Checkupinfo_tbl.id,Checkupinfo_tbl.peropno,Checkupinfo_tbl.tokenno,Checkupinfo_tbl.date,Checkupinfo_tbl.consult,Checkupinfo_tbl.name,Checkupinfo_tbl.amount,Checkupinfo_tbl.status,Checkupinfo_tbl.type,Checkupinfo_tbl.cstatus,Checkupinfo_tbl.diagnosis,opinfo_tbl.mobileno from Checkupinfo_tbl inner join  opinfo_tbl on Checkupinfo_tbl.peropno=opinfo_tbl.peropid where Checkupinfo_tbl.consult=? and Checkupinfo_tbl.date between ? and ?''';      
        cursor.execute(query,(docname,fromdt,todt))
        listtest=cursor.fetchall() #  print(listtest)
        fields = ['pk', 'peropno', 'tokenno', 'date', 'consult',
        'name', 'amount', 'status', 'ctype','cstatus', 'diagnosis','mobileno']
        user = [dict(zip(fields, d)) for d in listtest]  # print(user)       
        connection.commit()
        connection.close()             
        drshrtlist1 = Checkupinfo.objects.filter(consult=docname,date__range=[fromdt, todt]).filter(cstatus="Cancel").count()  #print(drshrtlist1)     
        drshrtlist2 = Checkupinfo.objects.filter(consult=docname,date__range=[fromdt, todt]).filter(cstatus="Cancel").aggregate(sum=Sum('amount'))['sum']#print(drshrtlist2)               
        drshrtlist5 = Checkupinfo.objects.filter(consult=docname,date__range=[fromdt, todt]).filter(cstatus="Finish").count()#print(drshrtlist5)
        drshrtlist6 = Checkupinfo.objects.filter(date__range=[fromdt, todt]).filter(consult=docname).count()#print(drshrtlist6)
        totalop = drshrtlist5 + drshrtlist6 # print(totalop)
        drshrtlist3 = Checkupinfo.objects.filter(consult=docname,date__range=[fromdt, todt]).filter(cstatus="Finished").aggregate(sum=Sum('amount'))['sum']#print(drshrtlist3)        
        drshrtlist4 = Checkupinfo.objects.filter(consult=docname).filter(date__range=[fromdt, todt]).aggregate(tot=Sum('amount'))['tot'] # print(drshrtlist4)
        # if drshrtlist3 is None : 
        #     drshrtlist3 = 0 
        # if drshrtlist4 is None : 
        #    drshrtlist4 = 0 
        # totalopamt = float(drshrtlist3) + float(drshrtlist4) #  print(totalopamt)        
        data = {'user': user,'drshrtlist2':drshrtlist2,
        'drshrtlist1':drshrtlist1,'drshrtlist6':drshrtlist6,
        'drshrtlist4':drshrtlist4,'docname':docname}    
        return JsonResponse(data)     

@login_required(login_url='/login/')
def appoinmentreport(request):
    user=request.user # print(username)
    userid=user.id # print(userid) 
    hospital_id=user.created_by    
    if hospital_id is None:
        hospital_id=user.id   
    docname = DrDetails.objects.all() 
    return render(request,'appoinmentreport.html',{'docname':docname})

@login_required(login_url='/login/')
def searchapponiment(request):
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id     
        docname =  request.GET.get('docname', None)  # print(docname)
        dateapp =  request.GET.get('dateapp', None)  #  print(dateapp)
        session =  request.GET.get('session', None)  #   print(session)
        deapplist = Appointment.objects.filter(doctorname=docname,dt=dateapp,session=session) # print(deapplist)
        user =  serializers.serialize('json', deapplist)# print(user)
        data = {'user': user }    
        return JsonResponse(data)

@login_required(login_url='/login/')
def searchid(request):
    user=request.user # print(username)
    userid=user.id # print(userid) 
    hospital_id=user.created_by    
    if hospital_id is None:
        hospital_id=user.id       
    return render(request,'searchid.html')

@login_required(login_url='/login/')
def searchopno(request):
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id     
        serchdtl =  request.GET.get('serchdtl', None)  #  print(serchdtl)
        enval =  request.GET.get('enval', None)  # print(enval)

        if serchdtl == "Name": #  print("resname")
            deapplist = opinfo.objects.filter(name=enval).values('id','name','addrs','gender','dob','age','mobileno','regdr','peropid') # print(deapplist)
              
        elif serchdtl == "Address": #   print("resaddress")
            deapplist = opinfo.objects.filter(addrs=enval).values('id','name','addrs','gender','dob','age','mobileno','regdr','peropid') # print(deapplist)  
           
        elif serchdtl == "Mobile": # print("resmobile")
            deapplist = opinfo.objects.filter(mobileno=enval).values('id','name','addrs','gender','dob','age','mobileno','regdr','peropid') # print(deapplist)
           
        else:
            pass         
        data = {'user': list(deapplist)}   # print(data)  
        return JsonResponse(data)                  

@login_required(login_url='/login/')
def updateform(request):
    user=request.user # print(username)
    userid=user.id # print(userid) 
    hospital_id=user.created_by    
    if hospital_id is None:
        hospital_id=user.id       
    return render(request,'updateform.html')

@login_required(login_url='/login/')
def peropid(request):   
     if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id      
        peropid =  request.GET.get('peropid', None)  # print(peropid)
        oldlist = opinfo.objects.filter(peropid=peropid).values('id','name','addrs','gender','dob','age','mobileno')#print(oldlist) 
        data = {'oldlist': list(oldlist)}#print(oldlist)
        return JsonResponse(data)

@login_required(login_url='/login/')
def newupdateform(request): 
    today = date.today()    
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id  
        tnid1 = request.GET.get('tnid1', None) # print(feestatus)
        peropid = request.GET.get('peropid', None)# print(tnid) 
        tnname1 = request.GET.get('tnname1', None)  # print(tnname)       
        tgenter1 = request.GET.get('tgenter1', None) # print(tgenter) 
        tnage1 = request.GET.get('tnage1', None) # print(tnage)            
        tnplace1 = request.GET.get('tnplace1', None) # print(drtoken) 
        tndob1 = request.GET.get('tndob1', None) # print(tokenid) 
        tnmobile1 = request.GET.get('tnmobile1', None) # print(tokenid) 
        updrdtl = opinfo.objects.get(id=tnid1)  
        updrdtl.peropid = peropid
        updrdtl.name = tnname1
        updrdtl.addrs = tnplace1
        updrdtl.gender = tgenter1
        updrdtl.dob = tndob1
        updrdtl.age = tnage1
        updrdtl.mobileno = tnmobile1
        newup=updrdtl.save()# print(newup)
        user = {'id':updrdtl.id,'peropid':updrdtl.peropid,'name':updrdtl.name,
        'addrs':updrdtl.addrs,'gender':updrdtl.gender,'dob':updrdtl.dob,
        'age':updrdtl.age,'mobileno':updrdtl.mobileno}
        data = {'save': True}    
        return JsonResponse(data)

@login_required(login_url='/login/')
def newtherprt(request,tokid): 
    newtoid = tokid # print(newtoid)
    today = date.today()
    now = datetime.now()
    d1 = now.strftime("%d/%m/%Y %H:%M:%S")
    user=request.user # print(username)
    userid=user.id # print(userid) 
    hospital_id=user.created_by    
    if hospital_id is None:
        hospital_id=user.id  
    plisttest = opinfo.objects.get(id=newtoid)  
    plisttest1 = Checkupinfo.objects.get(id=newtoid)#  print(plisttest)  
    user={'id':plisttest.id,'peropid':plisttest.peropid,
        'addrs':plisttest.addrs,'gender':plisttest.gender,'name':plisttest.name,
        'age':plisttest.age,'diagnosis':plisttest.diagnosis,
        'status':plisttest1.status,'tokenno':plisttest1.tokenno,'id':plisttest1.id} #  print(user)
    context = {'d1':d1,'user':user}# print(context)
    return render(request,'newtherprt.html',context)
   
@login_required(login_url='/login/')
def oldtherprt(request,tokid): 
    newtoid = tokid #  print(newtoid)
    today = date.today()
    now = datetime.now()
    d1 = now.strftime("%d/%m/%Y %H:%M:%S")
    user=request.user # print(username)
    userid=user.id # print(userid) 
    hospital_id=user.created_by    
    if hospital_id is None:
        hospital_id=user.id  
    plisttest = opinfo.objects.get(id=newtoid)#  print(plisttest) 
    plisttest1 = Checkupinfo.objects.get(id=newtoid)  # print(plisttest1)     
    user={'id':plisttest.id,'peropid':plisttest.peropid,
        'addrs':plisttest.addrs,'gender':plisttest.gender,
        'name':plisttest.name,'age':plisttest.age,
        'diagnosis':plisttest.diagnosis,'tokenno':plisttest1.tokenno,'status':plisttest1.status,
        'id':plisttest1.id} #  print(user)
    context = {'d1':d1,'user':user} # print(context)
    return render(request,'oldtherprt.html',context)

@login_required(login_url='/login/')        
def emerchange(request): 
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id     
        key=makeKey()
        docname = DrDetails.objects.all()  #print(docname)
        return render(request,'emerchange.html',{'docname':docname})       

@login_required(login_url='/login/')
def emgidsearch(request):
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id  
        oldidsearchnm = request.GET.get('oldidsearchnm', None) #print(oldidsearchnm) 
        oldlistck = Checkupinfo.objects.filter(peropno=oldidsearchnm).values('id','tokenno','amount')#print(oldlistck)
        oldlist = opinfo.objects.filter(peropid=oldidsearchnm).values('id','name','addrs','gender','dob','age','mobileno') # print(oldlist) 
        data = {'oldlist': list(oldlist),
        'oldlistck':list(oldlistck)}#print(oldlist)
        return JsonResponse(data)

@login_required(login_url='/login/')
def emgtokengenshot1(request):  
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id  
        drtoken = request.GET.get('drtoken1', None) #print(drtoken)
        drshrtlist = DrDetails.objects.filter(drname=drtoken).values('shortname')#print(drshrtlist)
        if drtoken == "Dr.S.A.NIHMATHULLAH":
            niktok = NIHtok.objects.all().last()   #print(niktok) 
            xx = niktok.tokno# print(xx)
            result = xx+1 # print(result)
            h =  'NIH'+ str(result)# print(h)   
        elif drtoken == "Dr.S.M.A.KUTHOOS":
            kuttok = KUTtok.objects.all().last() 
            xx2 = kuttok.tokno# print(xx)
            result2 = xx2+1 #print(xx2)#print(kuttok)
            h = 'KUT'+ str(result2)#  print(h)
        elif drtoken == "Dr.S.SAMINA YASMIN":
            samtok = SAMtok.objects.all().last() 
            xx = samtok.tokno# print(xx)
            result = xx+1#  print(result)
            h =  'SAM'+ str(result)# print(h) 
        else:
            pass  
        data = {'h': h, } #print(data)   
        return JsonResponse(data) 

@login_required(login_url='/login/')
def emgfeesave1(request):
    today = date.today() 
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id  
        feestatus1 = request.GET.get('feestatus1')#print(feestatus1) 
        if feestatus1 == "Normal":           
            connection = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-EB1CMRU;'
                      'Database=DynamicHospital;'
                      'Trusted_Connection=yes;')
            # cursor = conn.cursor()
            cursor= connection.cursor()        
            cursor.execute("select oldnormal from Fee_tbl")            
            row = cursor.fetchall()  #  print(row)            
            for fest in row:
                if fest:# print(fest)
                    for fest1 in fest:
                        if fest1:
                            print(fest1)
            connection.commit() 
            connection.close() 
        elif feestatus1 == "Emergency":           
            connection = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-EB1CMRU;'
                      'Database=DynamicHospital;'
                      'Trusted_Connection=yes;')
            # cursor = conn.cursor()
            cursor= connection.cursor()        
            cursor.execute("select oldemer from Fee_tbl")            
            row = cursor.fetchall()  #  print(row)            
            for fest in row:
                if fest:# print(fest)
                    for fest1 in fest:
                        if fest1:
                            print(fest1)
            connection.commit() 
            connection.close()                   
        data = {'fest1': fest1}#print(fest1)
        return JsonResponse(data)

@login_required(login_url='/login/')
def emgpdetailssave(request):
    today = date.today()    
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id  
        pid = request.GET.get('pid', None)
        ppid = request.GET.get('ppid', None)
        crntdt = request.GET.get('crntdt', None)
        tnid1 = request.GET.get('oldidsearchnm', None)# print(tnid)        
        temp1 = re.findall(r'\d+', tnid1) # through regular expression
        res2 = list(map(int, temp1)) # print(res2)       
        gg = list(res2[:2]) # print(gg) 
        restok1 = gg[1] # print(restok1)          
        drtoken1 = request.GET.get('drtoken1', None) # print(drtoken) 
        tokenid1 = request.GET.get('tokenid1', None) # print(tokenid) 
        tnname1 = request.GET.get('tnname1', None)  # print(tnname)       
        tgenter1 = request.GET.get('tgenter1', None) # print(tgenter1) 
        tnage1 = request.GET.get('tnage1', None) # print(tnage)
        amount1 = request.GET.get('amount1', None) #  print(amount) 
        feestatus1 = request.GET.get('feestatus1', None) # print(feestatus)        
        tnplace1 = request.GET.get('tnplace1', None) # print(tnplace)
        tndob1 = request.GET.get('tndob1', None) # print(tndob)
        tnmobile1 = request.GET.get('tnmobile1', None) # print(tnmobile)
        pdisease1 = request.GET.get('pdisease1', None) # print(pdisease)
        updrdtl = opinfo.objects.get(id=pid)  
        updrdtl.regdr = crntdt
        updrdtl.name = tnname1
        updrdtl.addrs = tnplace1
        updrdtl.gender = tgenter1
        updrdtl.dob = tndob1
        updrdtl.age = tnage1
        updrdtl.mobileno = tnmobile1
        newup=updrdtl.save() #   print(newup)
        updrdtlck = Checkupinfo.objects.get(id=ppid)  
        updrdtlck.tokenno = tokenid1
        updrdtlck.date = crntdt
        updrdtlck.consult = drtoken1
        updrdtlck.name = tnname1
        updrdtlck.amount = amount1
        updrdtlck.status = feestatus1        
        newupck=updrdtlck.save() #  print(newupck)
        perposave = peropidtbl.objects.create(peropids=restok1) # print(perposave)
        spshtdoc =  Checkupinfo.objects.last()        
        docnum = spshtdoc.tokenno # print(docnum)        
        m = re.match(r"([a-zA-Z]+)([0-9]+)",docnum)         
        m1 = m.group(1)
        ms = str(m1) # print (ms)         
        if ms == "NIH":            
            m2 = m.group(2) # print (m2)
            # z = int(m2)  
            # shtresult = z+1  
            # print(shtresult)  
            niktok = NIHtok.objects.create(tokno=m2) # print(niktok) 
        elif ms == "KUT":            
            m2 = m.group(2) # print (m2)
            # z = int(m2)  
            # shtresult = z+1 
            # print(shtresult)  
            niktok = SAMtok.objects.create(tokno=m2) # print(niktok)
        elif ms == "SAM":
            m2 = m.group(2) # print (m2)
            # z = int(m2)  
            # shtresult = z+1 
            # print(shtresult)  
            niktok = KUTtok.objects.create(tokno=m2) # print(niktok)
        else:
            pass         
        data = {'save': True} 
        return JsonResponse(data)

@login_required(login_url='/login/')
def confirmbtn(request): 
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id  
        pid = request.GET.get('pid', None) #print(pid)
        ppid = request.GET.get('ppid', None)# print(ppid)
        pswck = request.GET.get('pswck', None)# print(pswck)
        emgopdlt = opinfo.objects.get(id=pid) # print(emgopdlt)
        emgopdlt.delete()
        emgckdlt = Checkupinfo.objects.get(id=ppid)#print(emgckdlt)
        emgckdlt.delete()
        data = {'save': True} 
        return JsonResponse(data) 

@login_required(login_url='/login/')    
def updatestatus(request): 
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id         
        docname = DrDetails.objects.all()  #print(docname)
        return render(request,'updatestatus.html',{'docname':docname}) 

@login_required(login_url='/login/')
def updatedoclist(request): 
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id  
        select = request.GET.get('select', None)        
        today = date.today()        
        oplist = Checkupinfo.objects.filter(date=today,consult=select,status="Normal",cstatus = "Waiting")          
        docsearch =  serializers.serialize('json', oplist)      #print(docsearch) 
        opemlist = Checkupinfo.objects.filter(date=today,consult=select,status="Emergency",cstatus = "Waiting")              
        docsearch1 =  serializers.serialize('json', opemlist)
        opemlist2 = Checkupinfo.objects.filter(date=today,consult=select,status="Free",cstatus = "Waiting")    # print(opemlist2)
        docsearch2 =  serializers.serialize('json', opemlist2)  #print(docsearch2)  
        Finishnoprmal = Checkupinfo.objects.filter(date=today,consult=select,status="Normal",cstatus = "Finish")              
        Finishnoprmal =  serializers.serialize('json', Finishnoprmal) 
        Finishemergency = Checkupinfo.objects.filter(date=today,consult=select,status="Emergency",cstatus = "Finish")              
        Finishemergency =  serializers.serialize('json', Finishemergency) # 
        Finishemergency2 = Checkupinfo.objects.filter(date=today,consult=select,status="Free",cstatus = "Finish")# print(Finishemergency2)
        Finishemergency2 =  serializers.serialize('json', Finishemergency2) #  print(Finishemergency2)            
        data = { 'docsearch':docsearch,
            'docsearch1':docsearch1,
            'docsearch2':docsearch2,
            'Finishnoprmal':Finishnoprmal,
            'Finishemergency':Finishemergency,
            'Finishemergency2':Finishemergency2 }
        return JsonResponse(data)    

@login_required(login_url='/login/')
def editwaitnrml(request): 
    today = date.today()   
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id   
        idInput = request.GET.get('idInput', None) 
        pid = request.GET.get('pid', None) 
        token = request.GET.get('token', None)    #print(oldcomplaint) 
        name = request.GET.get('name', None)
        Status = request.GET.get('Status', None)
        updtwnrml = Checkupinfo.objects.get(id=pid)  
        updtwnrml.tokenno = token
        updtwnrml.name = name
        updtwnrml.cstatus = Status       
        newup=updtwnrml.save()#   print(newup)
    data = { 'save': True,}   
    return JsonResponse(data)

@login_required(login_url='/login/')
def editfinnrml(request): 
    today = date.today()   
    if request.method == 'GET':
       user=request.user # print(username)
       userid=user.id # print(userid) 
       hospital_id=user.created_by    
       if hospital_id is None:
           hospital_id=user.id   
       idInput = request.GET.get('idInput', None) 
       pid = request.GET.get('pid', None) 
       token = request.GET.get('token', None)    #print(oldcomplaint) 
       name = request.GET.get('name', None)
       Status = request.GET.get('status', None)
       updtwnrml = Checkupinfo.objects.get(id=pid)  
       updtwnrml.tokenno = token
       updtwnrml.name = name
       updtwnrml.cstatus = Status       
       newup=updtwnrml.save()# print(newup)
    data = {'save': True,}   
    return JsonResponse(data)

@login_required(login_url='/login/')
def editwaitemg(request): 
    today = date.today()   
    if request.method == 'GET':
       user=request.user # print(username)
       userid=user.id # print(userid) 
       hospital_id=user.created_by    
       if hospital_id is None:
           hospital_id=user.id   
       idInput = request.GET.get('idInput', None) 
       pid = request.GET.get('pid', None) 
       token = request.GET.get('token', None)    #print(oldcomplaint) 
       name = request.GET.get('name', None)
       Status = request.GET.get('status', None)
       updtwnrml = Checkupinfo.objects.get(id=pid)  
       updtwnrml.tokenno = token
       updtwnrml.name = name
       updtwnrml.cstatus = Status       
       newup=updtwnrml.save()#  print(newup)
    data = {'save': True,}   
    return JsonResponse(data)

@login_required(login_url='/login/')
def editfinemg(request): 
    today = date.today()   
    if request.method == 'GET':
       user=request.user # print(username)
       userid=user.id # print(userid) 
       hospital_id=user.created_by    
       if hospital_id is None:
           hospital_id=user.id   
       idInput = request.GET.get('idInput', None) 
       pid = request.GET.get('pid', None) 
       token = request.GET.get('token', None)    #print(oldcomplaint) 
       name = request.GET.get('name', None)
       Status = request.GET.get('status', None)
       updtwnrml = Checkupinfo.objects.get(id=pid)  
       updtwnrml.tokenno = token
       updtwnrml.name = name
       updtwnrml.cstatus = Status       
       newup=updtwnrml.save()# print(newup)
    data = { 'save': True, }   
    return JsonResponse(data)

@login_required(login_url='/login/')
def editwfree(request): 
    today = date.today()   
    if request.method == 'GET':
       user=request.user # print(username)
       userid=user.id # print(userid) 
       hospital_id=user.created_by    
       if hospital_id is None:
           hospital_id=user.id   
       idInput = request.GET.get('idInput', None) 
       pid = request.GET.get('pid', None) 
       token = request.GET.get('token', None)    #print(oldcomplaint) 
       name = request.GET.get('name', None)
       Status = request.GET.get('status', None)
       updtwnrml = Checkupinfo.objects.get(id=pid)  
       updtwnrml.tokenno = token
       updtwnrml.name = name
       updtwnrml.cstatus = Status       
       newup=updtwnrml.save()# print(newup)
    data = {'save': True,}   
    return JsonResponse(data)

@login_required(login_url='/login/')
def editfinfre(request): 
    today = date.today()   
    if request.method == 'GET':
       user=request.user # print(username)
       userid=user.id # print(userid) 
       hospital_id=user.created_by    
       if hospital_id is None:
          hospital_id=user.id   
       idInput = request.GET.get('idInput', None) 
       pid = request.GET.get('pid', None) 
       token = request.GET.get('token', None)    #print(oldcomplaint) 
       name = request.GET.get('name', None)
       Status = request.GET.get('status', None)
       updtwnrml = Checkupinfo.objects.get(id=pid)  
       updtwnrml.tokenno = token
       updtwnrml.name = name
       updtwnrml.cstatus = Status       
       newup=updtwnrml.save()#  print(newup)
    data = {'save': True,}   
    return JsonResponse(data)

@login_required(login_url='/login/')
def ip(request):
    if request.method == 'GET':
      user=request.user # print(username)
      userid=user.id # print(userid) 
      hospital_id=user.created_by    
      if hospital_id is None:
        hospital_id=user.id           
      docname = DrDetails.objects.all()  #print(docname)
      return render(request,'ip.html',{'docname':docname})     

@login_required(login_url='/login/')
def doctor(request):
    user=request.user # print(username)
    userid=user.id # print(userid) 
    hospital_id=user.created_by    
    if hospital_id is None:
        hospital_id=user.id      
    return render(request,'doctor.html')

@login_required(login_url='/login/')
def searchidprint(request,id):
    user=request.user # print(username)
    userid=user.id # print(userid) 
    hospital_id=user.created_by    
    if hospital_id is None:
        hospital_id=user.id  
    ptokid = id
    plisttest = opinfo.objects.get(id=ptokid) #  print(plisttest)        
    users={'peropid':plisttest.peropid,'name':plisttest.name}   # print(users) 
    context = {'users':users}
    return render(request,'searchidprint.html',context)

@login_required(login_url='/login/')   
def updateformprint(request,topid):   
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id     
        tnid1 = request.GET.get('tnid1', None)   # print(tnid1)
        plisttest = opinfo.objects.get(id=topid) #  print(plisttest)        
        users={'peropid':plisttest.peropid,'name':plisttest.name}   # print(users) 
        context = {'users':users}
        return render(request,'updateformprint.html',context)

@login_required(login_url='/login/')
def updateformprints(request):
    user=request.user # print(username)
    userid=user.id # print(userid) 
    hospital_id=user.created_by    
    if hospital_id is None:
        hospital_id=user.id      
    return render(request,'updateformprint.html')

@login_required(login_url='/login/')
def levset(request):   
   if request.method == 'GET':
      user=request.user # print(username)
      userid=user.id # print(userid) 
      hospital_id=user.created_by    
      if hospital_id is None:
        hospital_id=user.id          
      docname = DrDetails.objects.all()  #print(docname)
      return render(request,'levsetting.html',{'docname':docname}) 

@login_required(login_url='/login/')   
def savelev(request):   
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id     
        drselect5 = request.GET.get('drselect5', None)   # print(tnid1)    
        levdtsv = request.GET.get('levdtsv', None)
        purposesv = request.GET.get('purposesv', None)
        doclev = DoctorLeaveInfo.objects.create(doctorname = drselect5,leavedate = levdtsv,purpose = purposesv)#print(doclev) 
        data = {'save': True}   
        return JsonResponse(data)

@login_required(login_url='/login/')
def viewleave(request):   
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id     
        drselect6 = request.GET.get('drselect6', None)   # print(tnid1)   
        user = DoctorLeaveInfo.objects.filter(doctorname=drselect6).values('id','doctorname','leavedate','purpose')#print(user)        
        data = {'user': list(user)}   
        return JsonResponse(data)

@login_required(login_url='/login/')        
def updateleave(request):   
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id     
        drselect7 = request.GET.get('drselect7', None)   # print(tnid1)   
        user = DoctorLeaveInfo.objects.filter(doctorname=drselect7).values('id','doctorname','leavedate','purpose')#print(user)        
        data = {'user': list(user)}   
        return JsonResponse(data)

@login_required(login_url='/login/')
def editdoclev(request):   
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id     
        docid3 = request.GET.get('docid3', None)   # print(tnid1) 
        doctorname2 = request.GET.get('doctorname2', None)  
        leavedate2 = request.GET.get('leavedate12', None)  
        purpose2 = request.GET.get('purpose2', None)  
        docupdate = DoctorLeaveInfo.objects.get(id=docid3) #  print(plisttest)        
        docupdate.doctorname = doctorname2
        docupdate.leavedate = leavedate2
        docupdate.purpose = purpose2       
        docupdate.save()#  print(user)    
        user={'id':docupdate.id,'doctorname':docupdate.doctorname,'leavedate':docupdate.leavedate,'purpose':docupdate.purpose}# print(user)
        data = {'user': user} #  print(data)  
        return JsonResponse(data)

@login_required(login_url='/login/')
def deletedoclev(request): 
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id        
        comid = request.GET.get('id', None)
        comdlt = DoctorLeaveInfo.objects.get(id=comid) #  print(comdlt)
        comdlt.delete() # print(comdlt)
        data = {'success': True} # print(data)
        return JsonResponse(data)

@login_required(login_url='/login/')
def ip(request):
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id         
        docname = DrDetails.objects.all()  #print(docname)      
        return render(request,'ip.html',{'docname':docname}) 

@login_required(login_url='/login/')
def ipenterform(request):        
    today = date.today() 
    if request.method == 'GET':
      user=request.user # print(username)
      userid=user.id # print(userid) 
      hospital_id=user.created_by    
      if hospital_id is None:
            hospital_id=user.id         
      docname = DrDetails.objects.all()  #print(docname)
      roomtype = Roomtype.objects.all()#  print(roomtype)
      return render(request,'ipenterform.html',{'docname':docname,'roomtype':roomtype}) 

@login_required(login_url='/login/')
def ipoldidsearch(request):
    today = date.today() 
    if request.method == 'GET':
      user=request.user # print(username)
      userid=user.id # print(userid) 
      hospital_id=user.created_by    
      if hospital_id is None:
        hospital_id=user.id    
      oldidsearchnm = request.GET.get('oldidsearchnm', None) #print(oldidsearchnm) 
      oldlist = opinfo.objects.filter(peropid=oldidsearchnm).values('name','addrs','gender','age','mobileno') #print(oldlist) 
      ipserno = IPSerialNo.objects.last()# print(ipserno) 
      ipnoget = ipserno.ipno # print(ipnoget)  
      nip=int(ipnoget)+1 #    print(nip)
      yr=today.year        
      newtd=int(str(yr)[-2:]) #print(newtd)
      user1=  str(newtd)+'-IP-'+str(nip)# print(newip)
      data = {'oldlist': list(oldlist),'user1':user1}#print(oldlist)
      return JsonResponse(data)

@login_required(login_url='/login/')
def roomvalidate(request):
    if request.method == 'GET':
      user=request.user # print(username)
      userid=user.id # print(userid) 
      hospital_id=user.created_by    
      if hospital_id is None:
        hospital_id=user.id    
      roomno = request.GET.get('roomno', None) #print(oldidsearchnm) 
      if IPInfo.objects.filter(roomno=roomno).exists():
        data = {'exist': True} 
      else:
        data = {'exist': False} 
    return JsonResponse(data)

@login_required(login_url='/login/')
def saveip(request): # myDate = datetime.now() # formatedDate = myDate.strftime("%Y-%m-%d %H:%M:%S")
    today = date.today() 
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id  
        oldidsearchnm = request.GET.get('oldidsearchnm', None)# print(tnid) 
        drtoken1 = request.GET.get('drtoken1', None) # print(drtoken) 
        tokenid1 = request.GET.get('tokenid1', None) # print(tokenid)
        temp1 = re.findall(r'\d+', tokenid1) # through regular expression
        res2 = list(map(int, temp1)) # print(res2)       
        gg = list(res2[:2]) # print(gg)
        restok1 = gg[1] # print(restok1) 
        tnname1 = request.GET.get('tnname1', None)  # print(tnname) 
        dttime = request.GET.get('dttime', None)  # print(tnname)       
        tgenter1 = request.GET.get('tgenter1', None) # print(tgenter) 
        tnage1 = request.GET.get('tnage1', None) # print(tnage)
        adavnce = request.GET.get('adavnce', None) # print(tnage)
        roomtype = request.GET.get('roomtype', None) #  print(amount) 
        roomno = request.GET.get('roomno', None) # print(feestatus)        
        tnplace1 = request.GET.get('tnplace1', None) # print(tnplace)        
        tnmobile1 = request.GET.get('tnmobile1', None) # print(tnmobile)
        ipsave = IPInfo.objects.create(ipno=tokenid1,perid=oldidsearchnm,
        doctorname=drtoken1,name=tnname1,age=tnage1,gender=tgenter1,adres=tnplace1,
        mobile=tnmobile1,advance=adavnce,roomtype=roomtype,roomno=roomno,
        status="Admitted") # print(ipsave)
        ipserno = IPSerialNo.objects.create(ipno=int(restok1)) #print(ipserno)
        oldlist = Checkupinfo.objects.filter(peropno=oldidsearchnm).filter(date=today).update(cstatus = "Admitted")#print(oldlist)             
        user = {'id':ipsave.id,'ipno':ipsave.ipno,'name':ipsave.name}
        data = {'user':user}   
        return JsonResponse(data)

@login_required(login_url='/login/')        
def ipthermal (request,ipid): 
    newipid = ipid # print(newipid)
    today = date.today()
    now = datetime.now()
    d1 = now.strftime("%d-%m-%Y %H:%M:%S")
    user=request.user # print(username)
    userid=user.id # print(userid) 
    hospital_id=user.created_by    
    if hospital_id is None:
        hospital_id=user.id  
    iplisttest = IPInfo.objects.get(id=newipid) # print(iplisttest)  
    user={'id':iplisttest.id,'ipno':iplisttest.ipno,'name':iplisttest.name} #  print(user)
    context = {'user':user} # print(context)
    return render(request,'ipthermal.html',context)

@login_required(login_url='/login/')       
def ipdoclist(request): 
    today = date.today() #print(today)    
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id  
        select1 = request.GET.get('select', None)
        d = datetime.now()  # or whatever you want        
        datetime_filter = datetime(2020, 10, 17)         
        tdyiplist = IPInfo.objects.filter(admitdate__year=today.year, admitdate__month=int(today.month), admitdate__day=today.day).filter(doctorname=select1)#print(tdyiplist)       
        docipsearch =  serializers.serialize('json', tdyiplist)
        preiplist = IPInfo.objects.filter(doctorname=select1).all()  #print(preiplist)        
        docipsearch1 =  serializers.serialize('json', preiplist)
        data = {'docipsearch':docipsearch,
            'docipsearch1':docipsearch1,}
        return JsonResponse(data) 

@login_required(login_url='/login/')
def ippatientdetail(request):  
    return render(request,'ippatientdetails.html')
    
@login_required(login_url='/login/')
def ippatientdetails(request,pk): 
    today = date.today() # print(today) 
    pkid=pk # print(pkid)
    user=request.user # print(username)
    userid=user.id # print(userid) 
    hospital_id=user.created_by    
    if hospital_id is None:
        hospital_id=user.id  
    preiplist = IPInfo.objects.get(id=pkid) #print(preiplist)
    galist = preiplist.perid # print(galist)  
    galist1 = preiplist.ipno #  print(galist1)   
    adate = preiplist.admitdate  # print(adate)    
    plisttest = Checkupinfo.objects.filter(peropno=galist).filter(cstatus="Admit") # print(plisttest)
    detail = opinfo.objects.filter(peropid=galist) # print(detail)  
    plist = Checkupinfo.objects.filter(peropno=galist).order_by('-id') #print(plist)
    tokenlist =  Checkupinfo.objects.filter(peropno=galist).order_by('-id')[:1] # print(tokenlist)
    tokenlist1 =  Checkupinfo.objects.filter(peropno=galist)# print(tokenlist1)
    com = ComplaintsSetting.objects.all()  # print(com)
    des = DiagnosisSetting.objects.all()  #print(des)
    lab1 = Group.objects.values('groupname')#print(lab1)
    product = DrugInfo.objects.values('name','kindprod')#print(product)
    productobj1 = PrescriptionDetails.objects.filter(perid=galist).values('id','dt','perid','tokenid')#print(productobj1)#
    context={'plist':plist,'galist':galist,
    'galist1':galist1,'tokenlist':tokenlist,'detail':detail,'com':com,'adate':adate,
    'today':today,'des':des,'lab1':lab1,'product':product,'productobj1':productobj1,'tokenlist1':tokenlist1}
    return render(request,'ippatientdetails.html',context)

@login_required(login_url='/login/')   
def jdatasaveip(request):
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id  
        jcdata1 = request.GET.get('jcdata', None) #print(jcdata1)
        pid1 = request.GET.get('galist', None) # print(pid1)
        pid2 = request.GET.get('galist1', None) # print(pid1)
        today = date.today()  #  print(jcdata1)
        jddata1 = request.GET.get('jddata', None) # print(jddata1) 
        jremark1 = request.GET.get('jremark', None)# print(jremark1)
        JsonDatas1 = json.loads(str(jcdata1)) #print(JsonDatas1)
        JsonDatas2 = json.loads(str(jddata1))  #print(JsonDatas2)          
        JsonDatas3 = json.loads(str(jremark1))
        for i in JsonDatas1:
            s = i   #print(s['Complaints'])
            complaint = s['Complaints']
            obj = ComplaintDetails.objects.create(complaint = complaint,dt = today,peropid = pid2)#print(obj)           
        for j in JsonDatas2:
            ss = j  #print(ss['Diagnosis'])
            diagnosis = ss['Diagnosis']
            obj1 = DiagnosisDetails.objects.create(diagnosis = diagnosis,dt = today,peropid = pid2)#print(obj1)       
        for k in JsonDatas3:
            sss = k   #print(s['Complaints'])
            remark = sss['Remark']
            obj2 =  Remarks.objects.create(remark = remark,dt = today,perop = pid2) # print(obj2)
        remfil = Remarks.objects.filter(dt=today,perop = pid2) # print(remfil)
        remfil = serializers.serialize('json', remfil)# print(remfil)
        comfil = ComplaintDetails.objects.filter(dt=today,peropid = pid2)  # print(comfil)
        comfil =  serializers.serialize('json', comfil)  
        diafil = DiagnosisDetails.objects.filter(dt=today,peropid = pid2) # print(diafil)
        diafil =  serializers.serialize('json', diafil)
        data = {'comfil': comfil,   
            'diafil': diafil,
            'remfil': remfil, }  # print(data)
        return JsonResponse(data)

@login_required(login_url='/login/')
def iplabdatasave(request):    
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id   
        grpdata = request.GET.get('grpdata', None)    #print(grpdata) 
        supdata = request.GET.get('supdata', None)    #print(supdata)
        pid1 = request.GET.get('galist', None)
        pid2 = request.GET.get('galist1', None)
        name1 = request.GET.get('namelist', None)
        token1 = request.GET.get('tokenlist', None)
        genter1 = request.GET.get('genterlist', None)
        age1 = request.GET.get('agelist', None)        
        today = date.today() 
        tbl1sonDatasgrp = json.loads(str(grpdata))
        tbl2sonDatassup = json.loads(str(supdata)) 
        #if grpdata is None:
        obj = LabRequest.objects.create(opno = pid2,tokno = token1, dt = today,name = name1,status = "Assign",labid = "Idnotassign") #print(obj) # print(obj) 
        k=1      
        for i in tbl1sonDatasgrp:           # print(k)
            s = i   #print(s['Complaints'])
            groupname = s['GroupName']
            subgroupname = s['SubGroupName']
            testname = s['Test']
            refrange = s['ReferRange']
            amount = s['Amount']            
            obj1 = LabDetails.objects.create(opno = pid2,tokno = token1, dt = today,sno = k, groupname = groupname, subgroupname = subgroupname, testname = testname,result = "Null", refrange = refrange, amount = amount)  #print(obj1)
            k = k+1        
        for j in tbl2sonDatassup:            
            ss = j   #print(s['Complaints'])   #print(ss)
            testname = ss['Name']
            amount = s['Amount']   #print(testname)                       
            obj2 = ThermalAmount.objects.create(opno = pid2,tokno = token1, dt = today, test = testname, amount = amount)# print(obj2)        
        data = {'comfil': 1,}   #print(data)       
        return JsonResponse(data)

@login_required(login_url='/login/')
def ipperscrpitionsave(request):
    today = date.today()    
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id   
        prohidname = request.GET.get('prohidname', None)  # print(prohidname)        
        pid1 = request.GET.get('galist', None)           # print(pid1)
        pid2 = request.GET.get('pid2', None)   
        name1 = request.GET.get('namelist', None)     # print(name1)
        token1 = request.GET.get('tokennolist', None)  #print(token1)
        tbl1sonDatasgrp = json.loads(str(prohidname))        
        for i in tbl1sonDatasgrp:   
            s = i  
            product = s['Product Name']   # print('product=>>>'+product)
            qty = s['Qty']          # print(product)
            morn = s['Morning']     # print(morn)
            after = s['AfterNoon']  #  print(after)
            night = s['Night']
            beforefood = s['Before Food']
            afterfood = s['After Food']
            productobj1 = PrescriptionDetails.objects.create(perid = pid2,
            tokenid = token1,pname = name1, dt = today,product = product,
            qty = qty, morn = morn,after = after, night = night,
            beforefood = beforefood,afterfood=afterfood)  # print(productobj1)  
        data = { 'save':True, } #'productobj1': productobj1,#'to_update' : to_update,  #print(data)  
        return JsonResponse(data)

@login_required(login_url='/login/')
def ipotherupdate(request):
    today = date.today()    
    if request.method == 'GET':                
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id  
        consult = request.GET.get('consult', None) # print(consult) 
        pid1 = request.GET.get('galist', None)      #  print(pid1)       
        pid2 = request.GET.get('pid2', None)  #  print(pid2)      
        token1 = request.GET.get('tokennolist', None)  # print(token1)
        othername = request.GET.get('othername', None) # print(othername)
        to_updated = IPInfo.objects.filter(perid = pid1).filter(ipno = pid2).update(status=othername)  # print(to_updated)
        data = { 'save':True,  }  
        return JsonResponse(data)

@login_required(login_url='/login/')
def nxtpreget(request):
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id                  
        ipid = request.GET.get('ipid', None) # print(ipid) 
        product = PrescriptionDetails.objects.filter(id=ipid).all()# print(user)
        productitem  =  serializers.serialize('json', product) #print(productitem)
        data = { 'productitem':productitem,}  
        return JsonResponse(data)

@login_required(login_url='/login/')
def pushprescr(request):
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id                  
        ipid = request.GET.get('ipid', None) # print(ipid) 
        product = PrescriptionDetails.objects.filter(id=ipid).all()# print(user)
        productitem  =  serializers.serialize('json', product) #print(productitem)
        data = { 'productitem':productitem,}  
        return JsonResponse(data)

@login_required(login_url='/login/')
def ipproductsavecomplaint(request): 
    today = date.today()   
    if request.method == 'GET':
       user=request.user # print(username)
       userid=user.id # print(userid) 
       hospital_id=user.created_by    
       if hospital_id is None:
            hospital_id=user.id   
       id = request.GET.get('id', None)      
       pid1 = request.GET.get('galist', None)
       pid2 = request.GET.get('pid2', None)
       oldcomplaint = request.GET.get('complaint', None)    #print(oldcomplaint) 
       ComplaintDetails .objects.filter(dt=today,peropid = pid2).filter(id=id).update(complaint = oldcomplaint) #  print(to_updatenewcomplaint)
    to_updatenewcomplaint = ComplaintDetails .objects.get(id=id)# print(to_updatenewcomplaint) 
    to_updatenewcomplaint =  serializers.serialize('json', [to_updatenewcomplaint])# print(to_updatenewcomplaint)  
    data = {'to_updatenewcomplaint': to_updatenewcomplaint,}   
    return JsonResponse(data)

@login_required(login_url='/login/')
def ipproductsavediagnosis(request): 
    today = date.today()   
    if request.method == 'GET':
       user=request.user # print(username)
       userid=user.id # print(userid) 
       hospital_id=user.created_by    
       if hospital_id is None:
            hospital_id=user.id   
       id = request.GET.get('ids', None)      
       pid1 = request.GET.get('galist', None)
       pid2 = request.GET.get('pid2', None)
       olddiagnosis = request.GET.get('diagnosis', None)  #       print(olddiagnosis) 
       DiagnosisDetails.objects.filter(dt=today,peropid = pid2).filter(id=id).update(diagnosis = olddiagnosis) #  print(to_updatenewdiagnosis)
    to_updatenewdiagnosis  = DiagnosisDetails.objects.get(id=id)
    to_updatenewdiagnosis  = serializers.serialize('json', [to_updatenewdiagnosis])# print(to_updatenewdiagnosis)  
    data = { 'to_updatenewdiagnosis': to_updatenewdiagnosis,}   
    return JsonResponse(data)

@login_required(login_url='/login/')
def ipproductsaveremark(request): 
    today = date.today()   
    if request.method == 'GET':
       user=request.user # print(username)
       userid=user.id # print(userid) 
       hospital_id=user.created_by    
       if hospital_id is None:
           hospital_id=user.id    
       id = request.GET.get('idr1', None)      
       pid1 = request.GET.get('galist', None)
       pid2 = request.GET.get('pid2', None)
       oldremark = request.GET.get('remark', None)  #       print(oldremark) 
       Remarks.objects.filter(dt=today,perop = pid2).filter(id=id).update(remark = oldremark) #  print(to_updatenewremark)
       to_updatenewremark = Remarks.objects.get(id=id)
       to_updatenewremark = serializers.serialize('json', [to_updatenewremark])
       data = { 'to_updatenewremark': to_updatenewremark}   
       return JsonResponse(data) 

@login_required(login_url='/login/')
def dailyreportprint(request,docname,fromdt,todt):
    user=request.user # print(username)
    userid=user.id # print(userid) 
    hospital_id=user.created_by    
    if hospital_id is None:
        hospital_id=user.id   
    docname=docname # print(docname)
    fromdt=fromdt # print(fromdt)
    todt=todt #   print(todt)
    drshrtlist5 = Checkupinfo.objects.filter(consult=docname,date__range=[fromdt, todt]).filter(cstatus="Finished").count()# print(drshrtlist1)print(drshrtlist5)
    drshrtlist6 = Checkupinfo.objects.filter(consult=docname,date__range=[fromdt, todt]).filter(cstatus="Waiting").count()#print(drshrtlist6)
    oplist = drshrtlist5 + drshrtlist6 
    tnewop = Checkupinfo.objects.filter(consult=docname,date__range=[fromdt, todt]).filter(ctype="New").count()# print(drshrtnewop)
    toldop = Checkupinfo.objects.filter(consult=docname,date__range=[fromdt, todt]).filter(ctype="Old").count()# print(drshrtoldop)
    tappoi = Checkupinfo.objects.filter(consult=docname,date__range=[fromdt, todt]).filter(cstatus="Appointment").count()#print(drshrtappop)
    cancelold = Checkupinfo.objects.filter(consult=docname,date__range=[fromdt, todt]).filter(cstatus="Cancel").filter(ctype="Old").count()#print(cancelold)
    cancelnew = Checkupinfo.objects.filter(consult=docname,date__range=[fromdt, todt]).filter(cstatus="Cancel").filter(ctype="New").count()#print(cancelold)
    newnormal = Checkupinfo.objects.filter(consult=docname,date__range=[fromdt, todt]).filter(status="Normal").filter(ctype="New").count()#print(newnormal)
    mulnewnormal = newnormal * 120# print(mulnewnormal)
    oldnormal = Checkupinfo.objects.filter(consult=docname,date__range=[fromdt, todt]).filter(status="Normal").filter(ctype="Old").count()#print(oldnormal)
    muloldnormal= oldnormal * 100 # print(muloldnormal)
    newemgy = Checkupinfo.objects.filter(consult=docname,date__range=[fromdt, todt]).filter(status="Emergency").filter(ctype="New").count()# print(newemgy)
    mulnewemgy=newemgy*150 # print(mulnewemgy)
    oldemgy = Checkupinfo.objects.filter(consult=docname,date__range=[fromdt, todt]).filter(status="Emergency").filter(ctype="Old").count()# print(oldemgy)
    muloldemgy=oldemgy*150 # print(muloldemgy)
    oldcancelnormal = Checkupinfo.objects.filter(consult=docname,date__range=[fromdt, todt]).filter(status="Normal").filter(ctype="Old").filter(cstatus="Cancel").count()#print(oldcancelnormal)
    muloldcancelnormal=oldcancelnormal*100 #  print(muloldcancelnormal)
    newcancelnormal = Checkupinfo.objects.filter(consult=docname,date__range=[fromdt, todt]).filter(status="Normal").filter(ctype="New").filter(cstatus="Cancel").count()#print(newcancelnormal)
    mulnewcancelnormal=newcancelnormal*120 # print(mulnewcancelnormal)
    oldcancelemgy = Checkupinfo.objects.filter(consult=docname,date__range=[fromdt, todt]).filter(status="Normal").filter(ctype="Old").filter(cstatus="Cancel").count()#print(oldcancelemgy)
    muloldcancelemgy=oldcancelemgy*150 # print(muloldcancelemgy)
    newcancelemgy= Checkupinfo.objects.filter(consult=docname,date__range=[fromdt, todt]).filter(status="Emergency").filter(ctype="New").filter(cstatus="Cancel").count()#print(newcancelemgy)
    mulnewcancelemgy= newcancelemgy*150 # print(mulnewcancelemgy)
    total=mulnewnormal+muloldnormal+mulnewemgy+muloldemgy-muloldcancelnormal-mulnewcancelnormal-muloldcancelemgy-mulnewcancelemgy# print(total)
    context={'tnewop':tnewop,'toldop':toldop,
       'tappoi':tappoi,'cancelold':cancelold,
       'cancelnew':cancelnew,'newnormal':newnormal,
       'oldnormal':oldnormal,'newemgy':newemgy,
       'oldemgy':oldemgy,'oldcancelnormal':oldcancelnormal,
       'newcancelnormal':newcancelnormal,'oldcancelemgy':oldcancelemgy,
       'newcancelemgy':newcancelemgy,'docname':docname,
       'fromdt':fromdt,'todt':todt,'oplist':oplist,
       'mulnewnormal':mulnewnormal,'muloldnormal':muloldnormal,
       'mulnewemgy':mulnewemgy,'muloldemgy':muloldemgy,
       'muloldcancelnormal':muloldcancelnormal,'mulnewcancelnormal':mulnewcancelnormal,
       'muloldcancelemgy':muloldcancelemgy,'mulnewcancelemgy':mulnewcancelemgy,'total':total}
    return render(request,"dailyreportprint.html",context)

@login_required(login_url='/login/')
def ipdailyreport(request):
    user=request.user # print(username)
    userid=user.id # print(userid) 
    hospital_id=user.created_by    
    if hospital_id is None:
        hospital_id=user.id      
    docname = DrDetails.objects.all() 
    return render(request,'ipdailyreport.html',{'docname':docname})

@login_required(login_url='/login/')
def ipsearchop(request):   
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id     
        docname =  request.GET.get('docname', None)  #print(docname)
        todt = request.GET.get('todt', None) #  print(todt) 
        fromdt = request.GET.get('fromdt', None) #  print(fromdt)  
        user1 = IPInfo.objects.filter(doctorname=docname,admitdate__range=[fromdt, todt]).only('id','admitdate', 'doctorname', 'ipno',  'name', 'perid', 'roomno', 'status') # print(user)
        user =  serializers.serialize('json', user1) # print(user)
        data = {'user':user,'docname':docname}    
        return JsonResponse(data) 

@login_required(login_url='/login/')
def appoinmententry(request):
    user=request.user # print(username)
    userid=user.id # print(userid) 
    hospital_id=user.created_by    
    if hospital_id is None:
        hospital_id=user.id   
    docname = DrDetails.objects.all()  
    serialno1 = AppointmentSerial.objects.last() # print(serialno1)
    sno=serialno1.serialno # print(sno)
    sid=int(sno)+1
    serialnos='A'+ str(sid)# print(serialnos)
    return render(request,'appoinmententry.html',{'docname':docname,'serialnos':serialnos})        

@login_required(login_url='/login/')
def appientrysave(request): 
    today = date.today()   
    if request.method == 'GET':
       user=request.user # print(username)
       userid=user.id # print(userid) 
       hospital_id=user.created_by    
       if hospital_id is None:
           hospital_id=user.id    
       apid = request.GET.get('apid', None) #print(apid)          
       temp1 = re.findall(r'\d+', apid) # through regular expression
       res2 = list(map(int, temp1)) # print(res2)        
       restok1 = res2[-1] # print(restok1)   
       pname = request.GET.get('pname', None)
       docname = request.GET.get('docname', None)
       mblno = request.GET.get('mblno', None)      
       session = request.GET.get('session', None)
       purpose = request.GET.get('purpose', None)
       apdate = request.GET.get('apdate', None)
       appisave = Appointment.objects.create(serialno = apid,patientname = pname,doctorname = docname,
            dt=apdate,conduct=mblno,purpose=purpose,status="Booked",session=session)#   print(serialno1) 
       serialnosave = AppointmentSerial.objects.create(serialno = restok1) # print(serialnosave)
       appiget= Appointment.objects.last()
       getid=appiget.id #print(getid)
       serialno1 = AppointmentSerial.objects.last() # print(serialno1)
       sno=serialno1.serialno # print(sno)
       sid=int(sno)+1  # print(sid)
       getid1='A'+ str(sid)# print(serialnos)
       data = {'getid':getid,'getid1':getid1}    
       return JsonResponse(data) 

@login_required(login_url='/login/')
def appoinmentprint(request,gid):
    user=request.user # print(username)
    userid=user.id # print(userid) 
    hospital_id=user.created_by    
    if hospital_id is None:
        hospital_id=user.id   
    newid = gid # print(newid)
    appisave = Appointment.objects.get(id=newid)
    user={'id':appisave.id,'serialno':appisave.serialno,'doctorname':appisave.doctorname,
    'dt':appisave.dt,'session':appisave.session} #  print(user)
    context = {'user':user} #  print(context)
    return render(request,'appoinmentprint.html',context)

@login_required(login_url='/login/')
def appisearch(request):
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id   
        apid1 = request.GET.get('apid1', None) #  print(apid1)    
        appisave = Appointment.objects.filter(serialno=apid1).values('id','serialno', 
        'patientname','doctorname','dt','conduct','purpose','session')# print(appisave)      
        data = {'appisave':list(appisave)}    
        return JsonResponse(data) 

@login_required(login_url='/login/')
def appientryupdate(request):   
    if request.method == 'GET':
       user=request.user # print(username)
       userid=user.id # print(userid) 
       hospital_id=user.created_by    
       if hospital_id is None:
           hospital_id=user.id   
       pid1 = request.GET.get('pid1', None) #print(apid)          
       pname1 = request.GET.get('pname1', None)
       docname1 = request.GET.get('docname1', None)
       mblno1 = request.GET.get('mblno1', None)      
       session1 = request.GET.get('session1', None)
       purpose1 = request.GET.get('purpose1', None)
       apdate1 = request.GET.get('apdate1', None)          
       appiupdate = Appointment.objects.get(id=pid1)  
       appiupdate.patientname = pname1
       appiupdate.doctorname = docname1
       appiupdate.conduct = mblno1
       appiupdate.session = session1
       appiupdate.purpose = purpose1
       appiupdate.dt = apdate1       
       newupdate=appiupdate.save() #
       data = {'save':True}    
       return JsonResponse(data)

@login_required(login_url='/login/')
def appientrydelete(request):   
    if request.method == 'GET':
       user=request.user # print(username)
       userid=user.id # print(userid) 
       hospital_id=user.created_by    
       if hospital_id is None:
           hospital_id=user.id   
       pid1 = request.GET.get('pid1', None) #print(apid)  
       appidelete = Appointment.objects.get(id=pid1)  
       appidelete.status = "Deleted"             
       newdelete=appidelete.save() #appientrydelete
       data = {'save':True}    
       return JsonResponse(data)

@login_required(login_url='/login/')
def tokstatusreport(request):
    user=request.user # print(username)
    userid=user.id # print(userid) 
    hospital_id=user.created_by    
    if hospital_id is None:
        hospital_id=user.id     
    docname = DrDetails.objects.all() 
    return render(request,'tokstatusreport.html',{'docname':docname})

@login_required(login_url='/login/')
def normalcheck(request):
    today = date.today()
    if request.method == 'GET':
       user=request.user # print(username)
       userid=user.id # print(userid) 
       hospital_id=user.created_by    
       if hospital_id is None:
            hospital_id=user.id    
       docname = request.GET.get('docname', None) # print(docname)          
       customRadio1 = request.GET.get('customRadio1', None) #  print(customRadio1)
       user = Checkupinfo.objects.filter(date=today).filter(consult=docname).filter(status=customRadio1).values('peropno',
       'tokenno','date','consult','name','amount','status','diagnosis','ctype','cstatus')#print(user)
       #user =  serializers.serialize('json', drshrtlist)# print(user)
       data = {'user':list(user)}    
       return JsonResponse(data)

@login_required(login_url='/login/')
def emergencycheck(request):
    today = date.today()
    if request.method == 'GET':
       user=request.user # print(username)
       userid=user.id # print(userid) 
       hospital_id=user.created_by    
       if hospital_id is None:
            hospital_id=user.id   
       docname = request.GET.get('docname', None) # print(docname)          
       customRadio2 = request.GET.get('customRadio2', None) # print(customRadio2)
       user = Checkupinfo.objects.filter(date=today).filter(consult=docname).filter(status=customRadio2).values('peropno',
       'tokenno','date','consult','name','amount','status','diagnosis','ctype','cstatus')#print(user)       
       data = {'user':list(user)}     
       return JsonResponse(data)

@login_required(login_url='/login/')
def pvisitingstatus(request):
    user=request.user # print(username)
    userid=user.id # print(userid) 
    hospital_id=user.created_by    
    if hospital_id is None:
        hospital_id=user.id  
    return render(request,'pvisitingstatus.html')

@login_required(login_url='/login/')
def visitsearch(request):
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id   
        peropid = request.GET.get('peropid', None) # print(peropid)        
        drshrtlist = Checkupinfo.objects.filter(peropno=peropid).all() 
        user =  serializers.serialize('json', drshrtlist) #print(user)    
        pdltsave = opinfo.objects.filter(peropid = peropid).values('peropid','name', 'gender','age')# print(pdltsave)
        data = {'user':user,'pdltsave':list(pdltsave)}     
        return JsonResponse(data)

@login_required(login_url='/login/')
def prescriptionsearch(request):
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id   
        pperopid = request.GET.get('pperopid', None) #  print(pperopid)     
        pdate = request.GET.get('pdate', None) # print(peropid)        
        prescrlist = PrescriptionDetails.objects.filter(perid=pperopid).filter(dt=pdate).all() 
        perscrlist =  serializers.serialize('json', prescrlist) # print(perscrlist)    
        pdltsave = opinfo.objects.filter(peropid = pperopid).values('peropid','name', 'gender','age') #print(pdltsave)
        data = {'perscrlist':perscrlist,'pdltsave':list(pdltsave)}     
        return JsonResponse(data)

@login_required(login_url='/login/')
def dashboard(request):
    today = date.today()
    user=request.user # print(username)
    userid=user.id # print(userid) 
    hospital_id=user.created_by    
    if hospital_id is None:
        hospital_id=user.id     
    totplist = Checkupinfo.objects.filter(date=today).count()
    totaplist = Appointment.objects.filter(dt=today).count()
    nrmllist = Checkupinfo.objects.filter(date=today).filter(status="Normal").count() #print(nrmllist)
    emeglist = Checkupinfo.objects.filter(date=today).filter(status="Emergency").count()#print(emeglist)
    appoinlist = Appointment.objects.filter(dt=today).filter(status="Booked").count()#print(appoinlist)
    docount = DrDetails.objects.all().count()
    doclist = DrDetails.objects.all()
    results = []
    appresult = []
    for producer in doclist:
        i=producer.drname # print(i)
        data1 = Checkupinfo.objects.filter(date=today).filter(consult=i).count() #print(data1)
        tdyappoinlist = Appointment.objects.filter(dt=today).filter(doctorname=i).count()#print(appoinlist)
        dict1 = {'Doctor': i,'Count': data1}# print(dict1) 
        dict2 = {'Doctor':i,'Count':tdyappoinlist}
        results.append(dict1)#  print(results)
        appresult.append(dict2)
    context={'totplist':totplist,'nrmllist':nrmllist,'emeglist':emeglist,
    'appoinlist':appoinlist,'docount':docount,'results':results,'appresult':appresult}
    return render(request,'dashboard.html',context)

@login_required(login_url='/login/')
def chatdata(request):    
    today=date.today()
    user=request.user # print(username)
    userid=user.id # print(userid) 
    hospital_id=user.created_by    
    if hospital_id is None:
        hospital_id=user.id   
    doclist = DrDetails.objects.all() # print(doclist)profile
    results = [] #print(results)
    for producer in doclist:
        datas=[producer.shortname]# print(datas)
        results.append(datas[0])  # print(results)   
    default=[] # print(default)
    data1 = Checkupinfo.objects.filter(date=today).filter(consult="Dr.S.A.NIHMATHULLAH").count() 
    default.append(data1)#  print(default)
    data2 = Checkupinfo.objects.filter(date=today).filter(consult="Dr.S.SAMINA YASMIN").count() 
    default.append(data2) # print(default)
    data3 = Checkupinfo.objects.filter(date=today).filter(consult="Dr.S.M.A.KUTHOOS").count() 
    default.append(data3) # print(default)
    data = {'results':results,'default1':default}     
    return JsonResponse(data)

@login_required(login_url='/login/')
def Profile(request):
    user=request.user # print(username)
    userid=user.id # print(userid) 
    hospital_id=user.created_by    
    if hospital_id is None:
        hospital_id=user.id     
    hosdel = User.objects.filter(id = hospital_id) 
    print(hosdel)      
    # for producer in hosdel:
    #     flogo=producer.profile 
    return render(request,'Profile.html',{'hosdel':hosdel})#

@login_required(login_url='/login/')
def profupdate(request):       
    if request.method == 'POST' or request.FILES.get("newlogo",False):#  print("Hlo image")
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by  
        oldlogo=user.profile  
        if hospital_id is None:
            hospital_id=user.id  
        proid = request.POST.get('proid') # print(proid) 
        hosname = request.POST.get('hosname') # print(hosname)     
        email = request.POST.get('email') # print(email)   
        mblno = request.POST.get('mblno') # print(mblno)   
        address = request.POST.get('address') # print(address)   
        city = request.POST.get('city') # print(city)   
        pincode = request.POST.get('pincode')
        country = request.POST.get('country') # print(country)   
        slogan = request.POST.get('slogan') 
        print(slogan)    
        # oldlogo = request.POST.get('logo')  #b = logo.encode() print(oldlogo)  
        upload_file = request.FILES.get('newlogo') 
        print(upload_file) 
        if upload_file is None:
            upload_file=oldlogo
        logopics=FileSystemStorage()
        logopics.save(upload_file.name, upload_file, max_length=None)
        to_updated = User.objects.filter(id = hospital_id).update(hosname = hosname,
        email = email,mobileno = mblno,address = address,city = city,pincode=pincode,country = country,
        slogan = slogan,profile=upload_file)
        print(to_updated)  
        data = {'save': True }    
        return JsonResponse(data)

@login_required(login_url='/login/')
def patmonitor(request):
    user=request.user # print(username)
    userid=user.id # print(userid) 
    hospital_id=user.created_by    
    if hospital_id is None:
        hospital_id=user.id  
    docname = DrDetails.objects.all().values('drname') # print(docname)
    return render(request,'patmonitor.html',{'docname':json.dumps(list(docname))})

@login_required(login_url='/login/')
def patientsearch(request):
    today=date.today() 
    if request.method == 'GET':
       user=request.user # print(username)
       userid=user.id # print(userid) 
       hospital_id=user.created_by    
       if hospital_id is None:
            hospital_id=user.id   
       spltdrname = request.GET.get('spltdrname', None) # print(spltdrname) 
       tokcount = Checkupinfo.objects.filter(date=today,consult=spltdrname).count()#print(tokcount)
       waitcount = Checkupinfo.objects.filter(date=today,consult=spltdrname,cstatus="Waiting").count()#print(waitcount)
       shtlit = Checkupinfo.objects.filter(date=today,consult=spltdrname).values('tokenno','consult','name','cstatus').last()#print(shtlit)  
       data = {'shtlit':shtlit,'tokcount':tokcount,'waitcount':waitcount}    
       return JsonResponse(data)

@login_required(login_url='/login/')
def newemp(request):
    today=date.today()
    yr=today.year 
    mtn=today.month               
    newtd=int(str(yr)[-2:]) # print(newtd)
    empcd = sub_user.objects.last()   #print(empcd)   
    # docnum = empcd.empcode# print(docnum)
    # temp1 = re.findall(r'\d+', docnum) # through regular expression print(temp1)
    # res2 = list(map(int, temp1))# print(res2)       
    # gg = list(res2[:2])#print(gg)
    # restok1 = gg[1]# print(restok1)
    # docno=len(docnum)# print(docno)
    # for i in range(6,docno):# print(i)
    #     docnum = empcd.empcode[i] # print(docnum)      
    #     newempno=int(docnum)+1   # print(newempno)
    # newempcd = str(newtd)+ '-'+str(mtn)+'-'+ str(newempno)# print(newempcd)
    user=request.user # print(username)+str(newtoken) 
    userid=user.id # print(userid) 
    hospital_id=user.created_by    
    if hospital_id is None:
        hospital_id=user.id  
    rolelist=role.objects.all()#print(rolelist)
    prfpic = sub_user.objects.filter(created_by=hospital_id)#for producer in prfpic:,'profpics':profpicsprint(prfpic)print(prfpic)   
    return render(request,'newemp.html',{'rolelist':rolelist,'prfpic':prfpic}) #'newempcd':newempcd,'active':active,'inactive':inactive

@login_required(login_url='/login/')
def saveuserlogin(request):#print("saveuser")
    today = date.today()     
    if request.method == 'POST' or request.FILES.get("images",False): 
        user=request.user # print(username)
        userid=user.id # print(userid) 
        useremail=user.email
        userhosname=user.hosname
        useraddress=user.address# print(useraddress)
        userpincode=user.pincode
        usercity=user.city
        usercountry=user.country
        userphoneno=user.phoneno
        usermobileno=user.mobileno
        userslogan=user.slogan
        usertandc=user.tandc
        userprofile=user.profile
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id  
        name = request.POST.get('name', None) #print(apid) 
        email = request.POST.get('email', None)        
        dob = request.POST.get('dob', None)
        age = request.POST.get('age', None)
        empcode = request.POST.get('empcode', None)
        bldgrp = request.POST.get('bldgrp', None)
        mblno = request.POST.get('mblno', None)      
        gender = request.POST.get('gender', None)
        address = request.POST.get('address', None)
        qulifi = request.POST.get('qulifi', None)# print(qulifi)
        role = request.POST.get('role', None)#print(role)
        pwd = request.POST.get('pwd', None)#print(role)
        prfpic = request.FILES.get('images', None)# print(prfpic)   
        fs1=FileSystemStorage()
        fs1.save(prfpic.name, prfpic, max_length=None)
        joindate = request.POST.get('date1', None)# print(prfpic)        
        active = request.POST.get('active', None)# print(active)
        if active == "True":
            status = True
        else:
            status = False            
        usersave = User.objects.create_user(created_by=userid,username = name,password=pwd,
            email=email,hosname=userhosname,address=useraddress,pincode=userpincode,
            city=usercity,country=usercountry,phoneno=userphoneno,mobileno=usermobileno,
            slogan=userslogan,tandc=usertandc,role=role,status=status,profile=prfpic)       
        
        subusersave = sub_user.objects.create(id=usersave.id,created_by=userid,username = name,
            empcode=empcode,bloodgroup=bldgrp,dob = dob,age = age,mobileno=mblno,
            gender=gender,address=address,qualification=qulifi,role=role,email=email,
            status=status,profile=prfpic,date_join=joindate)#print(userlogsave)       
        data = {'save':True} 
        return JsonResponse(data) 

@login_required(login_url='/login/')
def updateuserlogin(request):
    today = date.today()   
    if request.method == 'POST' or request.FILES.get("prfpic1",False):        
       user=request.user # print(username)
       userid=user.id # print(userid) 
       hospital_id=user.created_by    
       if hospital_id is None:
            hospital_id=user.id  
       id1 = request.POST.get('id1', None) # print(id1) 
       usergetdata = sub_user.objects.get(id=id1)# print(usergetdata)
       olddob=usergetdata.dob #print(olddob)
       oldpic=usergetdata.profile# print(oldpic)
       name1 = request.POST.get('name1', None) #print(apid) 
       empcode1 = request.POST.get('empcode1', None) #print(apid) 
       dob1 = request.POST.get('dob1', None)# print(dob1)     
       if dob1 is None:
           dob1=olddob#  print(dob1)
       age1 = request.POST.get('age1', None)
       mblno1 = request.POST.get('mblno1', None)      
       gender1 = request.POST.get('gender1', None)# print(gender1)
       address1 = request.POST.get('address1', None)
       qulifi1 = request.POST.get('qulifi1', None)#print(qulifi)
       role1 = request.POST.get('role1', None)# print(role)
       bloodgroup1 = request.POST.get('bloodgroup1', None)# print(bloodgroup1)
       prfpic = request.FILES.get('prfpic1', None)# print(prfpic)
       if prfpic is None:
           prfpic=oldpic
       fs1=FileSystemStorage()
       fs1.save(prfpic.name, prfpic, max_length=None)       
       active1 = request.POST.get('active1', None)# print(active)  
       userupdate = sub_user.objects.get(id=id1) # print(userupdate)             
       userupdate.name= name1
       userupdate.empcode= empcode1
       userupdate.dob = dob1
       userupdate.age = age1   
       userupdate.mobileno = mblno1   
       userupdate.gender = gender1   
       userupdate.address = address1   
       userupdate.qualification = qulifi1   
       userupdate.role = role1   
       userupdate.bloodgroup = bloodgroup1   
       userupdate.status = active1   
       userupdate.profile = prfpic  
       users=userupdate.save()
       print(users)    
       user={'id':userupdate.id,'name':userupdate.name,'empcode':userupdate.empcode,'age':userupdate.age,
       'mobileno':userupdate.mobileno,'gender':userupdate.gender,'address':userupdate.address,'bloodgroup':userupdate.bloodgroup,
       'qualification':userupdate.qualification,'dob':userupdate.dob,'role':userupdate.role,'status':userupdate.status
       ,'profile':userupdate.profile}              #   print(user) 
       data = {'user': list(user)} #   print(data)  
       return JsonResponse(data)

@login_required(login_url='/login/')
def deleteuser(request): 
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id        
        userid = request.GET.get('id', None)
        userdlt = sub_user.objects.get(id=userid) #  print(userid)
        userdlt.delete() # print(userid)
        data = {'success': True} # print(data)
        return JsonResponse(data)

def registerform(request):
    return render(request,'registerform.html')

def login(request):
    rolelist=role.objects.all()#print(rolelist)
    return render(request,'login.html',{'rolelist':rolelist})


def forgotpassword(request):
    return render(request,'forgotpassword.html')

def regform(request):
    if request.method == 'POST':       
        username = request.POST.get('username') # print(hosname) 
        hosname = request.POST.get('hosname') # print(hosname)     
        email = request.POST.get('email') # print(email)   
        phono = request.POST.get('phono') # print(phono)  
        mblno = request.POST.get('mblno') # print(mblno)   
        password = request.POST.get('password') # print(password)   
        address = request.POST.get('address') # print(address)  
        pincode = request.POST.get('pincode') # print(pincode)   
        city = request.POST.get('city') # print(city)   
        country = request.POST.get('country') # print(country)   
        content = request.POST.get('content') # print(content1)  
        chkbx = request.POST.get('chkbx') # print(content1) 
        if User.objects.filter(username=username).exists(): 
            data = {'username': True} # print(data)
            return JsonResponse(data) 
        elif User.objects.filter(email=email).exists(): 
            data = {'email': True} # print(data)
            return JsonResponse(data)
        elif User.objects.filter(phoneno = phono).exists(): 
            data = {'phnno': True} # print(data)
            return JsonResponse(data)
        elif User.objects.filter(mobileno = mblno).exists(): 
            data = {'mblno': True} # print(data)
            return JsonResponse(data)
        else:  
            to_updated = User.objects.create_user(username=username,hosname = hosname,password=password,
            email = email,phoneno = phono,mobileno = mblno,address = address,pincode=pincode,city = city,country = country,
            slogan = content,tandc = chkbx,role="Admin",status='True')
            #user.user_permissions.add('Can link Checkupinfo')
            Permission_lists=['can_Appointment','can_Checkupinfo','can_AppointmentSerial',
            'can_ComplaintDetails','can_ComplaintsSetting','can_DiagnosisDetails',
            'can_DiagnosisSetting','can_DoctorLeaveInfo','can_DrDetails','can_DrugInfo',
            'can_Fee','can_Group','can_IPInfo','can_IPSerialNo','can_KUTtok',
            'can_LabDetails','can_LabRequest','can_NIHtok','can_opinfo','can_peropidtbl',
            'can_PrescriptionDetails','can_Remarks','can_role','can_Roomtype','can_SAMtok',
            'can_sub_user','can_SubGroupName','can_Test','can_TesterInfo','can_TestResult',
            'can_ThermalAmount','can_TokenDiagnosis','can_profile','can_Dashboard',
            'can_Tokengen','can_Emergencychange','can_Updatestatus','can_Patientvisitingstatus',
            'can_Patientmonitor','can_Dailyreport','can_Tokenstatusreport','can_Addemployee',
            'can_Searchip','can_Updateform','can_Newadmission','can_Searchopno','can_Doctorleavesetting',
            'can_complaintform','can_tokendiagonsisform','can_Diagnosisform','can_tokenset',
            'can_Appointmententry','can_Appointmentreport','can_patinetdetails','can_Ipdailyreport',
            'can_Ipmonitor']          
            for p in Permission_lists:
                permissions = Permission.objects.get(codename=p) # print(permissions)
                to_updated.user_permissions.add(permissions)#print(ss)
            data = {'save': True }    
            return JsonResponse(data) 

def mailcal(request):
    if request.method == 'GET':
        mailid= request.GET.get('mailid', None) #print(drtoken)
        if User.objects.filter(email=mailid).exists():            
            maillist = User.objects.filter(email=mailid).values('hosname','role') #  print(maillist)               
            data = {'maillist': list(maillist)} # print(data)
            return JsonResponse(data)           
        else:
            data = {'ermail': True} # print(data)
            return JsonResponse(data)

def usernamecal(request):
    if request.method == 'GET':    
        mailid= request.GET.get('mailid', None)
        username= request.GET.get('username', None) #print(drtoken)
        if User.objects.filter(username=username).exists():            
            userlist = User.objects.filter(email=mailid,username=username).values('hosname','role') #  print(maillist)               
            data = {'userlist': list(userlist)} # print(data)
            return JsonResponse(data)           
        else:
            data = {'username': True} # print(data)
            return JsonResponse(data)


def my_login(request):
    if request.method == 'POST':   
        mailid = request.POST.get('mailid')#print(mailid)
        role = request.POST.get('role')# print(role)
        hosname = request.POST.get('hosname')# print(hosname)   
        username = request.POST.get('username')#print(username)
        password = request.POST.get('password')# print(password)#   
        user = authenticate(request,email=mailid,hosname=hosname, 
        username=username, password=password,role=role)#print("Login Sucess")        
        if user is not None:
            django_login(request, user)
            data = {'index': True} # print(data)
            return JsonResponse(data) 
        else:
            data = {'login': True} # print(data)
            return JsonResponse(data) 

@login_required(login_url='/login/')
def logout(request):#print('logged out')    
    django_logout(request)          
    return redirect('registerform')

@login_required(login_url='/login/')
def empcalculateAge(request):
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id  
        dob = request.GET.get('dob', None)   #print(dob)
        todate = datetime.strptime(dob,"%Y-%m-%d")
        today = date.today() 
        userage = today.year - todate.year - ((today.month, today.day) < (todate.month, todate.day))       
        data = {'user': userage}
        return JsonResponse(data)

@login_required(login_url='/login/')
def empcalculateAge1(request):
    if request.method == 'GET':
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id  
        date2 = request.GET.get('date2', None)  # print(date2)
        todate = datetime.strptime(date2,"%Y-%m-%d")
        today = date.today() 
        userage = today.year - todate.year - ((today.month, today.day) < (todate.month, todate.day))       
        data = {'user': userage}
        return JsonResponse(data)

@login_required(login_url='/login/')
def empsavepermission(request):
    if request.method == 'POST':  
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id             
        id1 = request.POST.get('id1') #   print(id1)    
        userdetails=User.objects.get(id=id1)
        print(userdetails)         
        userdetails.user_permissions.clear() 
        checkbox_value = json.loads(request.POST.get('jsonText'))
        # checkbox_value =request.POST.getlist('jsonText')  print(checkbox_value)         
        for p in checkbox_value:
            permissions = Permission.objects.get(name=p) # print(permissions)
            userdetails.user_permissions.add(permissions) #  print(ss)          
        data = {'save': True}
        return JsonResponse(data)
  

def employeepermission(request):
    if request.method == 'POST':  
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id             
        id = request.POST.get('id')#print(id)    
        userdetails=User.objects.get(id=id)# print(userdetails)  
        per_get=userdetails.user_permissions.all().values('name')#print(ss)
        data = {'per_get': list(per_get)}
        return JsonResponse(data)

def forgatpwd(request):
    print("forgetpassword")
    if request.method == 'POST':  
        user=request.user # print(username)
        userid=user.id # print(userid) 
        hospital_id=user.created_by    
        if hospital_id is None:
            hospital_id=user.id             
        email = request.POST.get('email')#print(email)
        username = request.POST.get('username')#print(username)
        if sub_user.objects.filter(email=email,username=username).exists():            
            sub_userlist = sub_user.objects.filter(email=mailid,username=username).values('hosname','role') #  print(maillist)               
            data = {'save': True} # print(data)
            return JsonResponse(data)           
        else:
            data = {'username': True} # print(data)
            return JsonResponse(data)
