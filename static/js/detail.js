var getElementById = function(id, context) {
  var element,
  id = id.replace('#', '');

  if ('jQuery' in this && context) {
    element = $("#" + id, context)[0];
  } else {
    element = document.getElementById(id);
  };

  return element;
};

function showBid()
{
    //document.getElementById("review").style.display="block";
    $('#review').css('display','block');
    $('#bid').css('display','none');
    //document.getElementById("bid").style.display="block";
    //document.getElementById("bid").style.display="none";
}

function showStudent()
{
    getElementById("studentForm").style.display="block";
    document.getElementById("recruiterForm").style.display="none";
}

/* FORM VALIDATIONS */
function signupValidations()
{
    var userType, status=true;
    if(document.getElementById("r1").checked)
        userType = document.getElementById("r1").value;
    else
        userType = document.getElementById("r2").value;

    if(userType === 'student')
    {
        alert("student");
       var fName = document.getElementById('id_firstName').value;
       var lName = document.getElementById('id_lastName').value;
       var email = document.getElementById('id_email').value;
       var pass = document.getElementById('id_password').value;
       if(fName === "" || lName === "" ||email === "" ||pass === "" )
       {
           status = false;
       }
    }
    else
    {
        var cName = document.getElementById('id_companyName').value;
       var rName = document.getElementById('id_recruiterName').value;
       var email = document.getElementById('id_email').value;
       var pass = document.getElementById('id_password').value;
       if(cName === "" || rName === "" ||email === "" ||pass === "" )
       {
           status = false;
       }
    }

    if(!status)
        alert("please fill all the fields");
    return status;
}

function loginValidate()
{
    alert("please fill all the fields");
     var email = document.getElementById('id_email').value;
     var pass = document.getElementById('id_password').value;
     if (email ==="" || pass==="")
     {
         alert("please fill all the fields");
         return false;
     }
     return true;
}