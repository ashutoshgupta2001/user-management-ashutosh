function searchFun(){
  let filter = document.getElementById('myInput').value.toUpperCase();
  // console.log(filter)
  let myTable = document.getElementById('myTable');
  let tr = myTable.getElementsByTagName('tr');

  for(var i=0; i<tr.length; i++){
      let td = tr[i].getElementsByTagName('td')[1];

      if(td){
          let textvalue = td.textContent || td.innerHTML;
          if(textvalue.toUpperCase().indexOf(filter) > -1){
              tr[i].style.display = "";    
          }
          else{
              tr[i].style.display = "none";
          }
      }
  }
}


var state = false;
function togglePassword()
{
    if(state){
        document.getElementById("password").setAttribute("type","password");
        document.getElementById("eye").style.color= 'grey';
        state = false;
    }
    else{
        document.getElementById("password").setAttribute("type","text");
        document.getElementById("eye").style.color= '#5887ef';
        state = true;
    }
}
function togglePassword2()
{
    if(state){
        document.getElementById("password2").setAttribute("type","password");
        document.getElementById("eye2").style.color= 'grey';
        state = false;
    }
    else{
        document.getElementById("password2").setAttribute("type","text");
        document.getElementById("eye2").style.color= '#5887ef';
        state = true;
    }
}
function togglePassword3()
{
    if(state){
        document.getElementById("password3").setAttribute("type","password");
        document.getElementById("eye3").style.color= 'grey';
        state = false;
    }
    else{
        document.getElementById("password3").setAttribute("type","text");
        document.getElementById("eye3").style.color= '#5887ef';
        state = true;
    }
}

function toggleViewProfile(){
    
    let btnviewprofile = document.getElementById('btn-viewprofile');
    let tablediv = document.getElementById('table-div');
    if(tablediv.style.display != "none"){
        tablediv.style.display= "none";
    }
    else{
        tablediv.style.display='block'
    }
}