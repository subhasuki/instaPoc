$("form#profilesub").submit(function(event){
  event.preventDefault();//alert("hiiiii")
    var proid = $('input[name="proid"]').val()
    var hosname = $('input[name="hosname"]').val()//console.log(hosname)
    var email = $('input[name="email"]').val() //console.log(email)
    var mblno = $('input[name="mblno"]').val() //  console.log(mblno)
    var address = $('textarea[name="address"]').val() // console.log(address)  
    var city = $('input[name="city"]').val() //  console.log(city)
    var pincode = $('input[name="pincode"]').val() //  console.log(pincode)
    var country = $('input[name="country"]').val() // console.log(country)
    var slogan = $('input[name="slogan"]').val() // console.log(slogan)    
    var newlogo = $('#newlogo').get(0).files[0]; //console.log(newlogo) 
    var formData = new FormData();
    formData.append('csrfmiddlewaretoken', $('input[name=csrfmiddlewaretoken]').val());
    formData.append('proid',proid);
    formData.append('hosname',hosname);
    formData.append('email',email);
    formData.append('mblno',mblno); 
    formData.append('address',address); 
    formData.append('city',city); 
    formData.append('pincode',pincode); 
    formData.append('country',country); 
    formData.append('slogan',slogan);     
    formData.append('newlogo',newlogo); 
    $.ajax({
        url: '/profupdate',        
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


  
  // function logoimg() {//alert("HUUUUUUU")
  // var hlogo = $('input[name="hlogo"]').val()//console.log(hlogo)
  // //var myImg = hlogo;//console.log(myImg)
  // var image = document.createElement('img');
  // console.log(image)
  // image.src = hlogo;
  // document.body.appendChild(image);
  // }

  