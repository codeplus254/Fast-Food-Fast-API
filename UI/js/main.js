
function signUpFunction(){
    document.getElementById("signUpBtn").className = "active";
    document.getElementById("signInBtn").className = "";
    
} 

const fetchToken = (user_details,url) => {
    const options ={
        method: 'POST',
        body: JSON.stringify(user_details),
        headers: new Headers({
            'Content-Type': 'application/json'
        })
    }
    return fetch(url,options)
    .then(res => res.json())
    .then( res=> {token = res["token"];window.sessionStorage.setItem('token', token);alert(res["Message"]);})
    .catch(error => console.error(`Error: $(error)`))
    
}
function fetchSignUpToken() {
    let url = 'http://127.0.0.1:5000/api/v2/auth/signup'
    const user_details = {
        email:document.getElementsByName("email")[0].value,
        username:document.getElementsByName("username")[0].value,
        password:document.getElementsByName("password")[0].value
    }
    fetchToken(user_details,url)
    let token = window.sessionStorage.getItem('token')
  }
  function fetchLoginToken() {
    let url = 'http://127.0.0.1:5000/api/v2/auth/login'
    const user_details = {
        email:document.getElementsByName("email")[0].value,
        username:document.getElementsByName("username")[0].value,
        password:document.getElementsByName("password")[0].value
    }
    fetchToken(user_details,url)
    let token = window.sessionStorage.getItem('token')
    console.log(token)
  }  

function signInFunction() {
    document.getElementById("signUpBtn").className = "";
    document.getElementById("signInBtn").className = "active";
}
const fetchMenu = (token,url) => {
    const options ={
        method: 'GET',
        headers: new Headers({
            'Content-Type': 'application/json'
        })
    }
    return fetch(url,options)
    .then(res => res.json())
    .then( res=> {token = res["token"];window.sessionStorage.setItem('token', token);alert(res["Message"]);})
    .catch(error => console.error(`Error: $(error)`))
    
}
/*
function signUpUser() {
    
    let x = document.getElementById("signUp_form");
    //the user email given in form
    name= document.getElementsByName("email").value;
    document.getElementById("sign_up").style.display= "none";
    document.getElementById("sign_in").style.display= "none";
    document.getElementById("admin").style.display= "none";
    document.getElementById("order_food").style.display= "block";
    document.getElementById("orderFoodBtn").className = "active";
    document.getElementById("signUpBtn").className = "";
    document.getElementById("signInBtn").className = "";
    console.log(name);
    
}
function signInUser() {
    
    let x = document.getElementById("signIn_form");
      //the user email given in form
    name= document.getElementsByName("email").value;
    document.getElementById("sign_up").style.display= "none";
    document.getElementById("sign_in").style.display= "none";
    document.getElementById("admin").style.display= "none";
    document.getElementById("order_food").style.display= "block";
    document.getElementById("orderFoodBtn").className = "active";
    document.getElementById("signUpBtn").className = "";
    document.getElementById("signInBtn").className = "";
    console.log(name);
    
}
function orderFood() {
    console.log(name);
    document.getElementById("sign_up").style.display= "none";
    document.getElementById("sign_in").style.display= "none";
    document.getElementById("order_food").style.display= "none";
    document.getElementById("admin").style.display= "block";


    let data = document.getElementById("orderFood_form");
    document.getElementById("Items").innerHTML=data.elements;

}*/