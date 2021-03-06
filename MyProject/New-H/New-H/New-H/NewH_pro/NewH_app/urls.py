from django.urls import path
from .import views
from django.conf import settings


urlpatterns=[
    path('',views.registerform,name="registerform"),
    path('my_login',views.my_login,name="my_login"),  
    path('index',views.index,name="index"),  
    path('tokengen/',views.tokengen,name="tokengen"), 
    path('complaints',views.complaints,name="complaints"), 
    path('monitor',views.monitor,name="monitor"),  
    path('patientdetails',views.patientdetails,name="patientdetails"),
    path('patientdetails/<int:pk>/',views.patientdetails,name="patientdetails"),     
    path('calculateAge',views.calculateAge,name='calculateAge'),
    path('calculateAge1',views.calculateAge1,name='calculateAge1'),
    path('createThing',views.createThing,name="createThing"),
    path('doclist',views.doclist,name="doclist"),
    path('jdatasave',views.jdatasave,name='jdatasave'),
    path('labdatafetch',views.labdatafetch,name='labdatafetch'),
    path('labdatafetch1',views.labdatafetch1,name='labdatafetch1'),  
    path('labdatasave',views.labdatasave,name='labdatasave'),
    path('productsavecomplaint',views.productsavecomplaint,name='productsavecomplaint'),
    path('productsavediagnosis',views.productsavediagnosis,name='productsavediagnosis'),
    path('productsaveremark',views.productsaveremark,name='productsaveremark'),
    path('perscrproduct',views.perscrproduct,name='perscrproduct'),
    path('perscrpitionsave',views.perscrpitionsave,name='perscrpitionsave'),
    path('appoinmentsave',views.appoinmentsave,name='appoinmentsave'),
    path('otherupdate',views.otherupdate,name='otherupdate'),   
    path('inkA4',views.inkA4,name='inkA4'),    
    path('todaylabupdate',views.todaylabupdate,name='todaylabupdate'),    
    path('feesave',views.feesave,name='feesave'), 
    path('feesave1',views.feesave1,name='feesave1'),
    path('pdetailssave',views.pdetailssave,name='pdetailssave'),   
    path('pdetailssave1',views.pdetailssave1,name='pdetailssave1'),   
    path('appoinmentcal',views.appoinmentcal,name='appoinmentcal'), 
    path('appoinmentcal1',views.appoinmentcal1,name='appoinmentcal1'),    
    path('oldidsearch',views.oldidsearch,name='oldidsearch'),
    path('tokengenshot',views.tokengenshot,name='tokengenshot'),
    path('tokengenshot1',views.tokengenshot1,name='tokengenshot1'),
    path('saveco',views.saveco,name='saveco'),
    path('updatecomplaint',views.updatecomplaint,name='updatecomplaint'),
    path('deletecom',views.deletecom,name='deletecom'), 
    path('diagnosisset',views.diagnosisset,name='diagnosisset'),
    path('savecodia',views.savecodia,name='savecodia'),
    path('updateDiagnosis',views.updateDiagnosis,name='updateDiagnosis'),
    path('deletedia',views.deletedia,name='deletedia'),
    path('tokendisease',views.tokendisease,name='tokendisease'),
    path('savetokdis',views.savetokdis,name='savetokdis'),
    path('updateDisease',views.updateDisease,name='updateDisease'),
    path('deleteDisease',views.deleteDisease,name='deleteDisease'),
    path('tokesetting',views.tokesetting,name='tokesetting'),
    path('loguser',views.loguser,name='loguser'),
    path('loginset',views.loginset,name='loginset'),
    path('doctokengenshot',views.doctokengenshot,name='doctokengenshot'),
    path('tokdlt',views.tokdlt,name='tokdlt'),
    path('checkavail',views.checkavail,name='checkavail'),
    path('savedrname',views.savedrname,name='savedrname'),
    path('updatedrdetails',views.updatedrdetails,name='updatedrdetails'),
    path('deletedrdtl',views.deletedrdtl,name='deletedrdtl'),
    path('updatefee',views.updatefee,name='updatefee'),
    path('dailyreport',views.dailyreport,name='dailyreport'),    
    path('searchop',views.searchop,name='searchop'),
    path('appoinmentreport',views.appoinmentreport,name='appoinmentreport'),
    path('searchapponiment',views.searchapponiment,name='searchapponiment'),
    path('searchid',views.searchid,name='searchid'),
    path('searchopno',views.searchopno,name='searchopno'),
    path('updateform',views.updateform,name='updateform'),
    path('peropid',views.peropid,name='peropid'), 
    path('newupdateform',views.newupdateform,name='newupdateform'),
    path('newtherprt/<int:tokid>/',views.newtherprt,name='newtherprt'),
    path('oldtherprt/<int:tokid>/',views.oldtherprt,name='oldtherprt'),
    path('emerchange',views.emerchange,name='emerchange'), 
    path('emgidsearch',views.emgidsearch,name='emgidsearch'),
    path('emgtokengenshot1',views.emgtokengenshot1,name='emgtokengenshot1'),     
    path('emgfeesave1',views.emgfeesave1,name='emgfeesave1'),
    path('emgpdetailssave',views.emgpdetailssave,name='emgpdetailssave'),
    path('confirmbtn',views.confirmbtn,name='confirmbtn'),
    path('updatestatus/',views.updatestatus,name='updatestatus'),
    path('updatedoclist',views.updatedoclist,name='updatedoclist'),
    path('editwaitnrml',views.editwaitnrml,name='editwaitnrml'),
    path('editfinnrml',views.editfinnrml,name='editfinnrml'),
    path('editwaitemg',views.editwaitemg,name='editwaitemg'),
    path('editfinemg',views.editfinemg,name='editfinemg'),
    path('editwfree',views.editwfree,name='editwfree'),
    path('editfinfre',views.editfinfre,name='editfinfre'),
    path('ip',views.ip,name='ip'),
    path('doctor',views.doctor,name='doctor'),
    path('searchidprint/<int:id>/',views.searchidprint,name='searchidprint'),
    path('updateformprints',views.updateformprints,name='updateformprints'),
    path('updateformprint/<int:topid>/',views.updateformprint,name='updateformprint'),
    path('levset',views.levset,name='levset'),
    path('savelev',views.savelev,name='savelev'),
    path('viewleave',views.viewleave,name='viewleave'),
    path('updateleave',views.updateleave,name='updateleave'),
    path('editdoclev',views.editdoclev,name='editdoclev'),
    path('ipenterform/',views.ipenterform,name='ipenterform'),
    path('ipoldidsearch',views.ipoldidsearch,name='ipoldidsearch'),
    path('deletedoclev',views.deletedoclev,name='deletedoclev'),
    path('saveip',views.saveip,name='saveip'),
    path('roomvalidate',views.roomvalidate,name='roomvalidate'),
    path('ipthermal/<int:ipid>/',views.ipthermal,name='ipthermal'),
    path('ipdoclist',views.ipdoclist,name='ipdoclist'),
    path('ippatientdetail',views.ippatientdetail,name='ippatientdetails'),
    path('ippatientdetails/<int:pk>/',views.ippatientdetails,name='ippatientdetails'),
    path('jdatasaveip',views.jdatasaveip,name='jdatasaveip'),
    path('iplabdatasave',views.iplabdatasave,name='iplabdatasave'),
    path('ipperscrpitionsave',views.ipperscrpitionsave,name='ipperscrpitionsave'),
    path('ipotherupdate',views.ipotherupdate,name='ipotherupdate'),
    path('nxtpreget',views.nxtpreget,name='nxtpreget'),
    path('pushprescr',views.pushprescr,name='pushprescr'),
    path('ipproductsavecomplaint',views.ipproductsavecomplaint,name='ipproductsavecomplaint'),
    path('ipproductsavediagnosis',views.ipproductsavediagnosis,name='ipproductsavediagnosis'),
    path('ipproductsaveremark',views.ipproductsaveremark,name='ipproductsaveremark'),       
    path('dailyreportprint/<str:docname>/<str:fromdt>/<str:todt>/',views.dailyreportprint,name='dailyreportprint'),#
    path('ipdailyreport',views.ipdailyreport,name='ipdailyreport'),
    path('ipsearchop',views.ipsearchop,name='ipsearchop'),
    path('appoinmententry',views.appoinmententry,name='appoinmententry'),
    path('appientrysave',views.appientrysave,name='appientrysave'),
    path('appoinmentprint/<int:gid>/',views.appoinmentprint,name='appoinmentprint'),
    path('appisearch',views.appisearch,name='appisearch'),
    path('appientryupdate',views.appientryupdate,name='appientryupdate'),
    path('tokstatusreport',views.tokstatusreport,name='tokstatusreport'),
    path('normalcheck',views.normalcheck,name='normalcheck'),
    path('emergencycheck',views.emergencycheck,name='emergencycheck'),
    path('pvisitingstatus',views.pvisitingstatus,name='pvisitingstatus'),
    path('visitsearch',views.visitsearch,name='visitsearch'),
    path('prescriptionsearch',views.prescriptionsearch,name='prescriptionsearch'),
    path('appientrydelete',views.appientrydelete,name='appientrydelete'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('chatdata',views.chatdata,name='chatdata'),
    path('Profile',views.Profile,name='Profile'),
    path('profupdate',views.profupdate,name='profupdate'),
    path('patmonitor',views.patmonitor,name='patmonitor'),
    path('patientsearch',views.patientsearch,name='patientsearch'),
    path('newemp',views.newemp,name='newemp'),
    path('saveuserlogin',views.saveuserlogin,name='saveuserlogin'),
    path('updateuserlogin',views.updateuserlogin,name='updateuserlogin'),
    path('deleteuser',views.deleteuser,name='deleteuser'),    
    path('login',views.login,name='login'),
    path('forgotpassword',views.forgotpassword,name='forgotpassword'),
    path('regform',views.regform,name='regform'),
    path('mailcal',views.mailcal,name='mailcal'),
    path('empcalculateAge',views.empcalculateAge,name='empcalculateAge'),
    path('logout',views.logout,name='logout'),
    path('empcalculateAge1',views.empcalculateAge1,name='empcalculateAge1'),
    path('empsavepermission',views.empsavepermission,name='empsavepermission'),
    path('usernamecal',views.usernamecal,name='usernamecal'),
    path('employeepermission',views.employeepermission,name='employeepermission'),
    path('forgatpwd',views.forgatpwd,name='forgatpwd'),
]

