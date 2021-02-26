

function  empdobcal(){     
  console.log("age cal")
  var dob = $('input[name="dob"]').val()        
  $.ajax({
      url: '/empcalculateAge',
      type: 'get',
      data: {
          'dob': dob,
      },
      dataType: 'json',
      success: function (data) {
          if (data.user) {                
            document.getElementById("age").value=data.user;                
          }
      }
  });
}

function  empdobcal1(){     
  var date2 = $('input[name="date2"]').val()        
  $.ajax({
      url: '/empcalculateAge1',
      type: 'get',
      data: {
          'date2': date2,
      },
      dataType: 'json',
      success: function (data) {
          if (data.user) {                
            document.getElementById("form-age1").value=data.user;                
          }
      }
  });
}

$( "input" ).on( "click", function() {
  $( "#log" ).html( $( "input:checked" ).val() + " " );
});

$(document).ready(function(){
  $("#myInput").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#viewtbl tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });
});

$(document).ready(function(){  
  $("#myInput1").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#activetbl tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });
});

$(document).ready(function(){  
  $("#myInput").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#inactivetbl tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });
});

function getDate(){
var today = new Date();
document.getElementById("date").value = today.getFullYear() + '-' + ('0' + (today.getMonth() + 1)).slice(-2) + '-' + ('0' + today.getDate()).slice(-2);
}

$("form#saveuserlogin").submit(function(event) {  
  event.preventDefault();
    var name = $('input[name="name"]').val() //console.log(name)
    var dob = $('input[name="dob"]').val() // console.log(dob) 
    var age = $('input[name="age"]').val()// console.log(age)
    var empcode = $('input[name="empcode"]').val()//  console.log(empcode)
    var bldgrp = $('select[name="bldgrp"]').val()//  console.log(bldgrp)
    var mblno = $('input[name="mblno"]').val()//   console.log(mblno)
    var gender = $('select[name="gender"]').val() //   console.log(gender)
    var address = $('textarea[name="address"]').val()// console.log(address)
    var qulifi = $('input[name="qulifi"]').val() // console.log(qulifi)
    var role = $('input[name="role"]').val() // console.log(role)
    var email = $('input[name="email"]').val()  // console.log(prfpic)
    var actives = $('input[name="active"]').val() //console.log(active)
    var date1 = $('input[name="date1"]').val() // console.log(date1)
    var pwd = $('input[name="pwd"]').val() // console.log(date1)
    var images = $('#prfpic').get(0).files[0];// console.log(images)
    var formData = new FormData();
    formData.append('csrfmiddlewaretoken', $('input[name=csrfmiddlewaretoken]').val());   
    formData.append('name',name);
    formData.append('dob',dob);
    formData.append('email',email);
    formData.append('age',age); 
    formData.append('empcode',empcode); 
    formData.append('bldgrp',bldgrp); 
    formData.append('mblno',mblno); 
    formData.append('gender',gender); 
    formData.append('address',address); 
    formData.append('qulifi',qulifi); 
    formData.append('role',role);	
    formData.append('active',actives);    
    formData.append('images',images);       
    formData.append('pwd',pwd);	 
    formData.append('date1',date1);		  
			jQuery.ajax({
				url: '/saveuserlogin',
				type: "POST",
				data: formData,
				processData: false,
				contentType: false,
				success:function(data){
          if(data.save){  // console.log(data.user);
            swal("Good job!", "Save Successfully!", "success");  
            } 
            window.location.reload();
        }        
			});
    // }	
    // else{
    //   swal("error!", "404 not found!", "error"); 
    // }					
	// });	
});

function edituserlog(id) {//console(id)
    if (id) {  // alert(id);
      tr_id = "#user-" + id;//  console.log(tr_id)
      name1 = $(tr_id).find(".name1").text();//console.log(name1)
      empcode1 = $(tr_id).find(".empcode1").text();//  console.log(empcode1)
      id1 = $(tr_id).find(".id1").text();// console.log(name1)
      dob1 = $(tr_id).find(".dob1").text();
      email1 = $(tr_id).find(".email1").text();
      age1 = $(tr_id).find(".age1").text();
      mblno1 = $(tr_id).find(".mblno1").text();//  console.log(mblno1)
      gender1 = $(tr_id).find(".gender1").text();
      address1 = $(tr_id).find(".address1").text();
      qulifi1 = $(tr_id).find(".qulifi1").text();
      role1 = $(tr_id).find(".role1").text();
      bloodgroup1 = $(tr_id).find(".bloodgroup1").text();//  console.log(bloodgroup1)
      oldprfpic1 = $(tr_id).find(".oldprfpic1").text();//console.log(oldprfpic1)
      prfpic1 = $(tr_id).find(".prfpic1").text();
      active1 = $(tr_id).find(".active1").text();// console.log(active1)pwd
      if(active1 == "True"){
        document.getElementById("form-active1").checked = true;
      }         
      $('#form-id1').val(id1);
      $('#form-name1').val(name1);
      $('#form-email1').val(email1);
      $('#form-empcode1').val(empcode1);
      $('#form-dob1').val(dob1);
      $('#form-age1').val(age1);
      $('#form-mblno1').val(mblno1);
      $('#form-gender1').val(gender1);
      $('#form-address1').val(address1);
      $('#form-qulifi1').val(qulifi1);
      $('#form-role1').val(role1);
      $('#form-bloodgroup1').val(bloodgroup1);
      $('#form-oldprfpic1').val(oldprfpic1);
      $('#form-prfpic1').val(prfpic1);
      $('#form-active1').val(active1);
    }
}

$("form#updateuserlogin").submit(function(event) {  
    event.preventDefault();
    var id1 = $('input[name="id1"]').val() //console.log(name)
    var name1 = $('input[name="name1"]').val() //console.log(name)
    var email1 = $('input[name="email1"]').val() //console.log(name)
    var empcode1 = $('input[name="empcode1"]').val() //console.log(name)        
    var dob1 = $('input[name="date2"]').val() //console.log(dob1)    
    var age1 = $('input[name="age1"]').val()//  console.log(age)
    var mblno1 = $('input[name="mblno1"]').val()
    var gender1 = $('input[name="gender1"]').val() //console.log(gender1)
    var address1 = $('input[name="address1"]').val() // console.log(tnplace)
    var qulifi1 = $('input[name="qulifi1"]').val() // console.log(tndob)
    var role1 = $('input[name="role1"]').val()  //console.log(tnmobile)
    var bloodgroup1 = $('select[name="bloodgroup1"]').val()
    var prfpic1 = $('#form-prfpic1').get(0).files[0]; //  console.log(prfpic1)  
    var active1 = $('input[name="active1"]').val() // console.log(active)    
    var formData = new FormData();
    formData.append('csrfmiddlewaretoken', $('input[name=csrfmiddlewaretoken]').val());   
    formData.append('id1',id1);
    formData.append('name1',name1);
    formData.append('email1',email1);
    formData.append('dob1',dob1);
    formData.append('age1',age1); 
    formData.append('empcode1',empcode1); 
    formData.append('bloodgroup1',bloodgroup1); 
    formData.append('mblno1',mblno1); 
    formData.append('gender1',gender1); 
    formData.append('address1',address1); 
    formData.append('qulifi1',qulifi1); 
    formData.append('role1',role1);	
    formData.append('active1',active1);   
    formData.append('prfpic1',prfpic1);   
      $.ajax({
        type: 'POST',
        url: '/updateuserlogin',        
        data: formData,        
        processData: false,
				contentType: false,
        success: function (data) {
          if (data.user) { //  console.log(data.user)   
            swal("Good job!", "Update Successfully!", "success");            
          }     
          updateToUserTabel(data.user) 
        }
      });  
});

function updateToUserTabel(user){ // console.log(user); 
      for (i=0; i<user.length; i++) {
      var uid = user[i]; // console.log(uid)
    $("#viewbdy #user-" + uid).children(".userData").each(function() {
          var attr = $(this).attr("name");
          if (attr == "name1") {
            $(this).text( user.name1);      
          } 
          if (attr == "empcode1") {
            $(this).text( user.empcode1);      
          } 
          if (attr == "email1") {
            $(this).text( user.email1);      
          } 
          if (attr == "dob1") {
            $(this).text( user.dob1);      
          } 
          if (attr == "age1") {
            $(this).text( user.age1);      
          } 
          if (attr == "gender1") {
            $(this).text( user.gender1);      
          } 
          if (attr == "mblno1") {
            $(this).text( user.mblno1);      
          } 
          if (attr == "address1") {
            $(this).text( user.address1);      
          } 
          if (attr == "qulifi1") {
            $(this).text( user.qulifi1);      
          } 
          if (attr == "bloodgroup1") {
            $(this).text( user.bloodgroup1);      
          } 
          if (attr == "role1") {
            $(this).text( user.role1);      
          } 
          if (attr == "profile1") {
            $(this).text( user.profile1);      
          } 
          if (attr == "status1") {
            $(this).text( user.status1);      
          } 
        });
      }
}
    
function deleteuser(id) {  //alert(id)
        $.ajax({
            url: '/deleteuser',
            data: {'id'  :id},  
            dataType: 'json',
            success: function (data) {
              if (data.success) { 
                $("#viewtbl #user-" + id).remove();
                swal("Good job!", "Delete Successfully", "success")   
              } 
            }
        });
}
       
function employeepermission(id) {// console.log(id)    
  var id = id    //  console.log(id)
  document.getElementById("id1").value=id;  
  var formData = new FormData();
  formData.append('csrfmiddlewaretoken', $('input[name=csrfmiddlewaretoken]').val());   
  formData.append('id',id); 
  $.ajax({
    type: 'POST',
    url: '/employeepermission',        
    data: formData,        
    processData: false,
    contentType: false,
    success: function (data) {
      if (data.per_get) {
      var get_checkvalue=data.per_get; // console.log(get_checkvalue)         
      $(":checkbox.cutomck").each(function () {             
        var newck=($(this).val());    //  console.log(newck) 
        var ss=!get_checkvalue[newck]  
        console.log(ss)
        // testArray = newck in get_checkvalue;
        // console.log(testArray)
        // var ss=($(this).checked(true));
        // console.log(ss)
    });
    }    
    }    
  });
}

$("#empsavepermission").on('click', function(){
var id1 = $('#id1').val() //console.log(id1) 
var checkbox_value = []//console.log(checkbox_value)
    $(":checkbox.cutomck").each(function () {
        var ischecked = $(this).is(":checked");
        if (ischecked) {
            checkbox_value.push($(this).val()) ;            
        }
    });// alert(checkbox_value);
    var jsonText = JSON.stringify(checkbox_value);//console.log(jsonText)
var formData = new FormData();
formData.append('csrfmiddlewaretoken', $('input[name=csrfmiddlewaretoken]').val());   
formData.append('id1',id1);
formData.append('jsonText',jsonText)
$.ajax({
  type: 'POST',
  url: '/empsavepermission',        
  data: formData,        
  processData: false,
  contentType: false,
  success: function (data) {
    if (data.save) { //  console.log(data.user)   
     swal("Good job!", "Permission set Successfully!", "success");     
     $('input:checkbox').removeAttr('checked'); 
    }    
    window.location.reload();         
  }    
});
});

// for (var car of Object.values(get_checkvalue)) {
//       var sample = car.name ; //console.log(sample)
//       }      
//       var checkbox_value = []//console.log(checkbox_value)
//         var ischecked = $(this).is(".cutomck :not(:checked)");
// if(sample == newck){
//           console.log(sample==newck)
//           // document.getElementById("appoinentry").checked = true;
//           // document.getElementById("appoinreport").checked = true;  
//         }  