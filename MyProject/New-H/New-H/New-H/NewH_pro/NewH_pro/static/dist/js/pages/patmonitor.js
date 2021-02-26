function pad(num) {return ("0" + num).slice(-2);}
function time1() {
  var today = new Date(),
    h = today.getHours(),
    m = today.getMinutes(),
    s = today.getSeconds();
    
  h = h % 12;
  h = h ? h : 12; // the hour '0' should be '12'
  clk.innerHTML = h + ':' + 
    pad(m) + ':' + 
    pad(s) + ' ' + 
    (h >= 12 ? 'PM' : 'AM');
}
window.onload = function() {
 
  var clk = document.getElementById('clk');
  t = setInterval(time1, 500);
}


$( document ).ready(function() {  
    var today = new Date();
    var date = today.getDate()+'/'+(today.getMonth()+1)+'/'+today.getFullYear();// console.log(date)
    $('#tdaydate').text(date)    
    var drname = $('input[name="docname"]').val()// console.log(drname)  
    drname = JSON.parse(drname)  
    listdao(drname);
});

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

async function listdao(drname){ //  console.log("hi") 
    for (var i = 0; i <drname.length; i++) {    
    var text = drname[i];// console.log(drname[i]) 
    patientsearch(text);
    await sleep(10000); }
    setTimeout(function(){  
        listdao(drname);
    },10000);
}

function patientsearch(text){
    var docname = text; // console.log(docname)     
    for (var key in docname){
       var spltdrname=docname[key];// console.log(spltdrname)
    }   
    $.ajax({
        url: '/patientsearch',
        type: 'GET',
        data: {
            'spltdrname': spltdrname,
        },
        dataType: 'json',
        success: function(data)  {   
       if(data.shtlit){//  console.log(data.shtlit)
        var shtlit1 =  data.shtlit;//  console.log(shtlit1);   
          var tokenno= shtlit1.tokenno;//   console.log(tokenno)
          var consult= shtlit1.consult;//   console.log(consult)
          var name = shtlit1.name;//    console.log(name)  
      $('#docname').text(consult)
      $('#tokno').text(tokenno)
      $('#pname').text(name) 
       }
       if(data.tokcount){
        var tokcount=data.tokcount;
        $('#tokcut').text(tokcount)
       }
       if(data.waitcount){
        var waitcount=data.waitcount;
        $('#waitcount').text(waitcount)
       }
        }
    });
  }

