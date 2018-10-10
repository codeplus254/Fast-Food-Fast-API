# Fast-Food-Fast-API
Fast-Food-Fast is a food delivery service app for a restaurant.

## API endpoints
This API has nine end-points

| Endpoint | Functionality |Note|
|----------|---------------|----|
|POST api/v2/auth/signup|Register a user| |
|POST api/v2/admin|REgister an admin|Only an admin can access this page|
|POST api/v2/auth/login|Login a user| |
|POST api/v2/users/orders|Place an order for food.| |
|GET api/v2/users/orders|Get the order history for a logged in user.| |
|GET api/v2/orders|Get all orders|Only Admin (caterer) should have access to this route| |
|GET api/v2/orders/orderId|Fetch a specific order|orderId is an integer. Only Admin (caterer) should have access to this route|
|PUT api/v2/orders/orderId| Only Admin (caterer) should have access to this route.The status of an order could either be New, Processing, Cancelled or Complete.| orderid is an integer|                         |
|GET /menu|Get available menu| |
|POST /menu|Add a meal option to the menu.| Only Admin (caterer) should have access to this route|

## API Documentation
Here is a link to my postman API documentation.
[API DOCUMENTATION](https://documenter.getpostman.com/view/5303268/RWgm41ZX)

## DEPLOYMENT
A live version of this API has been hosted on Heroku
[SEE LIVE VERSION](fast-food-fast-api-v1.herokuapp.com)

## Continuous Integration
[![Build Status](https://travis-ci.org/codeplus254/Fast-Food-Fast-API.svg?branch=master)](https://travis-ci.org/codeplus254/Fast-Food-Fast-API) 

[![Coverage Status](https://coveralls.io/repos/github/codeplus254/Fast-Food-Fast-API/badge.svg?branch=master)](https://coveralls.io/github/codeplus254/Fast-Food-Fast-API?branch=master)

[![Maintainability](https://api.codeclimate.com/v1/badges/608657040a150d9fe104/maintainability)](https://codeclimate.com/github/codeplus254/Fast-Food-Fast-API/maintainability)

## Authors

* **Ronny Mageh** - *Initial work*

## Acknowledgments

* Hat tip to #team-titans and #team-thanos  
* Thank you Paul Rimiru (Week 1 Learning Facilitator Assistant at Andela) and Michael Mutoro (Week 2 Learning Facilitator Assistant at Andela) for the continued feedback



