$("form#regform").submit(function(event){
	event.preventDefault();
	alert("hiiiii")
      var username = $('input[name="username"]').val()	  
	  var hosname = $('input[name="hosname"]').val()//console.log(hosname)
	  var email = $('input[name="email"]').val() //console.log(email)
	  var mblno = $('input[name="mblno"]').val() //  console.log(mblno)
	  var address = $('textarea[name="address"]').val() // console.log(address)  
	  var pwd = $('textarea[name="pwd"]').val() // console.log(address)  
	  var pincode = $('textarea[name="pincode"]').val() // console.log(address)  
	  var city = $('input[name="city"]').val() //  console.log(city)
	  var country = $('input[name="country"]').val() // console.log(country)
	  var content1 = $('input[name="content"]').val() // console.log(content1)	  
	  var formData = new FormData();
	  formData.append('csrfmiddlewaretoken', $('input[name=csrfmiddlewaretoken]').val());
	  formData.append('username',username);
	  formData.append('hosname',hosname);
	  formData.append('email',email);
	  formData.append('mblno',mblno); 
	  formData.append('pwd',pwd); 
	  formData.append('address',address); 
	  formData.append('pincode',pincode); 
	  formData.append('city',city); 
	  formData.append('country',country); 
	  formData.append('content',content1); 	 
	  $.ajax({
		  url: '/regform',        
		  type: 'POST', 
		  data: formData,
		  processData: false,
		  contentType: false,            
		  dataType: 'json',
		  success: function(data)  { 
			if (data.save) {  
			  swal("Good job!", "Save Successfully", "success")
			}           
	  }
	  });         
	});
  