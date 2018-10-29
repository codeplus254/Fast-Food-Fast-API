
function signUpFunction(){
    document.getElementById("signUpBtn").className = "active";
    document.getElementById("signInBtn").className = "";
    
} 

const fetchToken = (user_details,url) => {
    let options ={
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
    let user_details = {
        email:document.getElementsByName("email")[0].value,
        username:document.getElementsByName("username")[0].value,
        password:document.getElementsByName("password")[0].value
    }
    fetchToken(user_details,url)
    let token = window.sessionStorage.getItem('token')
  }
  function fetchLoginToken() {
    let url = 'http://127.0.0.1:5000/api/v2/auth/login'
    let user_details = {
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
    let user_details = {
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
    let options ={
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
    let options ={
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
                    console.log(res["menu"])
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
    let url = 'http://127.0.0.1:5000/api/v2/users/orders'
    let order = {
        meal_name:select.options[select.selectedIndex].text,
        order_address:document.getElementById("address").value,
        order_quantity:Number(document.getElementById("quantity").value),
        order_contact:Number(document.getElementById("contact").value)
        //"order_contact":720682290
    }
    let order2 ={
        "meal_name":"pizza",
        "order_address":"Westlands",
        "order_quantity":7,
        "order_contact":720682290
    }
    let options ={
        method: 'POST',
        body: JSON.stringify(order),
        headers: new Headers({
            'token': window.sessionStorage.getItem('token'),
            'Content-Type': 'application/json'
        })
    }
    return fetch(url,options)
    .then(res => res.json())
    .then( res=> {console.log(res);alert(res["Message"]);})
    .catch(error => console.error(`Error: ${error}`))
    
}
const createOrderHistoryTable = (array) =>{
    let user_history = document.getElementById("user_history");
    let length = array.length
    if (length == 0){
        user_history.appendChild(document.createTextNode("You have never ordered for food.")); 
    }
    else{ 
        const orderHistoryTable = document.createElement("div");
        orderHistoryTable.setAttribute("id", "order-history");
        let row1 = document.createElement("tr");
        let header1= document.createElement("th"); 
        let title1 = document.createTextNode("Name"); 
        header1.appendChild(title1);
        row1.appendChild(header1);

        let header2= document.createElement("th"); 
        let title2 = document.createTextNode("Contact"); 
        header2.appendChild(title2);
        row1.appendChild(header2);

        let header3= document.createElement("th"); 
        let title3 = document.createTextNode("Delivery Address"); 
        header3.appendChild(title3);
        row1.appendChild(header3);

        let header4= document.createElement("th"); 
        let title4 = document.createTextNode("Status"); 
        header4.appendChild(title4);
        row1.appendChild(header4);

        let header5= document.createElement("th"); 
        let title5 = document.createTextNode("Unit(s)"); 
        header5.appendChild(title5);
        row1.appendChild(header5);

        let header6= document.createElement("th"); 
        let title6 = document.createTextNode("Total Price"); 
        header6.appendChild(title6);
        row1.appendChild(header6);

        orderHistoryTable.appendChild(row1);
        user_history.appendChild(orderHistoryTable);
        let orderHistoryBody= document.createElement("tbody"); 
        for (let i=0; i<length; i++){
            let row = document.createElement("tr");
            let meal_name_cell = document.createElement("td"); 
            let meal_name = document.createTextNode(array[i]["meal_name"]);
            meal_name_cell.appendChild(meal_name);
            row.appendChild(meal_name_cell);

            let order_contact_cell = document.createElement("td"); 
            let order_contact = document.createTextNode(array[i]["order_contact"]);
            order_contact_cell.appendChild(order_contact);
            row.appendChild(order_contact_cell);

            let order_address_cell = document.createElement("td"); 
            let order_address = document.createTextNode(array[i]["order_delivery_address"]);
            order_address_cell.appendChild(order_address);
            row.appendChild(order_address_cell);

            let order_status_cell = document.createElement("td"); 
            let order_status = document.createTextNode(array[i]["order_status"]);
            order_status_cell.appendChild(order_status);
            row.appendChild(order_status_cell);

            let order_quantity_cell = document.createElement("td"); 
            let order_quantity = document.createTextNode(array[i]["order_quantity"]);
            order_quantity_cell.appendChild(order_quantity);
            row.appendChild(order_quantity_cell);

            let order_price_cell = document.createElement("td"); 
            let order_price = document.createTextNode(array[i]["order_price"]);
            order_price_cell.appendChild(order_price);
            row.appendChild(order_price_cell);

            orderHistoryBody.appendChild(row);
        }
        orderHistoryTable.appendChild(orderHistoryBody);
        user_history.appendChild(orderHistoryTable);
        
    }


}
const orderHistory = () => {
    let url = 'http://127.0.0.1:5000/api/v2/users/orders'
    
    let options ={
        method: 'GET',
        headers: new Headers({
            'token': window.sessionStorage.getItem('token')
        })
    }
    return fetch(url,options)
    .then(res => res.json())
    .then( res=> {alert(res["Message"]);createOrderHistoryTable(res["Orders"]);})
    .catch(error => console.error(`Error: ${error}`))
    
}
const logout = () =>{
    
    let url = 'http://127.0.0.1:5000/api/v2/logout'
    const options ={
        method: 'GET',
        headers: new Headers({
            'token': window.sessionStorage.getItem('token')
        })
    }
    return fetch(url,options)
    .then(res => res.json())
    .then( res=> {alert(res["Message"]);sessionStorage.clear();})
    .catch(error => console.error(`Error: ${error}`))
}