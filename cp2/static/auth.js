// get elements for authentication
const SuName = document.getElementById("txtNameSU");
const SuEmail = document.getElementById("txtEmailSU");
const SuPassword = document.getElementById("txtPasswordSU");

const SiEmail = document.getElementById("txtEmailSI");
const SiPassword = document.getElementById("txtPasswordSI");

const btnSignup = document.getElementById("btnSignup");
const btnSignin = document.getElementById("btnSignin");
const btnLogout = document.getElementById("btnLogout");

const signupForm = document.getElementById('sign-up-container');
const signinForm = document.getElementById('sign-in-container');

function closeModal(){
  modal.style.display = 'none';
}

function redirect(){
  window.location.href = "indexprofile.html";
}


function logout(){
  window.location.href = "index.html";
}
btnLogout.addEventListener('click', logout);

// Sign Up
signupForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const name = signupForm['txtNameSU'].value="";
    const email = signupForm['txtEmailSU'].value="";
    const password = signupForm['txtPasswordSU'].value="";
    console.log(name,email,password);
    // signup the user
    auth.createUserWithEmailAndPassword(email, password).then(cred => {console.log(cred)})
    alert("You are registered :)");
})
// btnSignup.addEventListener('click', closeModal);
btnSignup.addEventListener('click', redirect);

// Sign In
signinForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const email = signinForm['txtEmailSI'].value="";
    const password = signinForm['txtPasswordSI'].value="";
    console.log(email,password);
    // signup the user
    auth.signInWithEmailAndPassword(email, password).then(cred => {console.log(cred)})
    alert("Thank your logged in :)");
})
btnSignin.addEventListener('click', redirect);


// Google Auth

googleSignIn=() =>{
var provider = new firebase.auth.GoogleAuthProvider();
firebase.auth().signInWithPopup(provider).then((result) => {
    console.log(result);
    console.log("Success");
  }).catch((error) => {
    console.log(error);
    console.log("Failed");
  });
}