
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
  function fetchAdminToken() {
    let url = 'http://127.0.0.1:5000/api/v2/admin/login'
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
const createMenuTable = (array) =>{
    let menu = document.getElementById("menu");
    let length = array.length
    if (length == 0){
        menu.appendChild(document.createTextNode("Sorry, there is no food available at the moment.")); 
    }
    else{ 
        const menuTable = document.createElement("p");
        menuTable.setAttribute("id", "food-menu");
        let row1 = document.createElement("tr");
        let header1= document.createElement("th"); 
        let title1 = document.createTextNode("Name"); 

        header1.appendChild(title1);
        row1.appendChild(header1);

        let header2= document.createElement("th"); 
        let title2 = document.createTextNode("Price"); 

        header2.appendChild(title2);
        row1.appendChild(header2);
        menuTable.appendChild(row1);
        menu.appendChild(menuTable);
        let menuBody= document.createElement("tbody"); 
        for (let i=0; i<length; i++){
            let row = document.createElement("tr");
            let meal_name_cell = document.createElement("td"); 
            let meal_name = document.createTextNode(array[i]["meal_name"]);
            meal_name_cell.appendChild(meal_name);
            row.appendChild(meal_name_cell);
            let meal_price_cell = document.createElement("td"); 
            let meal_price = document.createTextNode(array[i]["meal_price"]);
            meal_price_cell.appendChild(meal_price);
            row.appendChild(meal_price_cell);
            menuBody.appendChild(row);
        }
        menuTable.appendChild(menuBody);
        menu.appendChild(menuTable);
        
    }


}
const fetchMenu = () => {
    let url = 'http://127.0.0.1:5000/api/v2/menu'
    const options ={
        method: 'GET',
        headers: new Headers({
            'token': window.sessionStorage.getItem('token')
        })
    }
    return fetch(url,options)
    .then(res => res.json())
    .then( res=> {alert(res["Message"]);createMenuTable(res["menu"]);})
    .catch(error => console.error(`Error: ${error}`))
    
}
const availableFood = (select) => {
    let url = 'http://127.0.0.1:5000/api/v2/menu'
    const options ={
        method: 'GET',
        headers: new Headers({
            'token': window.sessionStorage.getItem('token')
        })
    }
    return fetch(url,options)
    .then(res => res.json())
    .then( res=> {
                    const select =  document.createElement("select");
                    const select_food = document.getElementById("available_food");
                    const form = document.getElementById('orderFood_form');
                    foods = [];
                    prices = [];
                    if (res["menu"].length == 0){   //no food in menu
                        let error_h2 = document.createElement("h2"); 
                        let error = document.createTextNode("Sorry, we do not have any food at the moment.");
                        error_h2.appendChild(error);
                        form.parentNode.appendChild(error_h2);
                        form.parentNode.removeChild(form);
                    }
                    else {
                        for (let i=0; i<res["menu"].length; i++){
                            foods.push(res["menu"][i]["meal_name"]);
                            let food_option = document.createElement("option"); 
                            food_option.text=res["menu"][i]["meal_name"];
                            food_option.value=res["menu"][i]["meal_name"];
                            select_food.appendChild(food_option);
                            prices.push(res["menu"][i]["meal_price"])}
                    }
        
                })
    .catch(error => console.error(`Error: ${error}`))
    
}
const placeOrder = () => {
    let select = document.getElementById("available_food");
    let url = 'http://127.0.0.1:5000/api/v2/users/orders';
    const order = {
        meal_name:select.options[select.selectedIndex].text,
        order_address:document.getElementById("address").value,
        order_quantity:Number(document.getElementById("quantity").value),
        order_contact:Number(document.getElementById("contact").value)
    }
    const order2 = {
        
            "meal_name":"fries",
            "order_address" : "Westlands",
            "order_quantity" : 2,
            "order_contact" : 720682290
        }
    const options ={
        method: 'GET',
        //body: JSON.stringify(order),
        //body: order2,
        headers: new Headers({
            'Content-Type': 'application/json',
            'token': window.sessionStorage.getItem('token')
        })
    }
    return fetch(url,options)
    .then(res => {console.log(order);res.json();})
    .then( res=> {console.log(order);alert(res["Message"]);})
    .catch(error => {console.error(`Error: ${error}`)})
    
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