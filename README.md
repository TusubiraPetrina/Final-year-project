# Routes #

#The site has been deployed https://fin-yer.herokuapp.com/

## api/register/ 
this is where a user particularly a farmer signs up onto the platform. It only accepts the POST request method. It takes input in JSON form :

    {
        "username":"johndoe",
        "first_name":"John",
        "last_name":"Doe",
        "email":"johndoe@example.com",
        "password":"************",
        "telephone":1234567890,
        "region":"central" 
    }
It returns a response also in JSON form:

    {
        "message":"Farmer Created Successfully","farmerID":"ID: ID000"
    }   

## api/login/ 
this is where a user particularly a farmer logs into their account the platform.It accepts only the POST method as request. It takes input in JSON form :

    {
        "username":"johndoe",
        "password":"************"
    }
It returns a response also in JSON form:

    {
        "Success": "Login successfully",
        "data":{
            "access":"************************",
            "refresh":"***********************"
        }
    }   

## api/logout/ 
this is where a user particularly a farmer logs out of their account on the platform. It only accepts POST as the request method. It takes input in JSON form :

    {
        "csrftoken":"*******************"
    }
It returns a response also in JSON form:

    {
        "Success": "Successfully Logged Out",
        "data":{
            "access":"************************",
            "refresh":"***********************"
        }
    }   

## api/farmers/

Allowed request methods: GET ,~~POST~~

It does not take in any input. It returns all users in the system who are farmers. It returns pagination if the number of results exceeds one page and links to the pages containing the excess results.

## api/farmers/id/

Allowed methods: GET, PUT, DELETE

for GET: it does not take in any input and returns details about the user whose id has been given as part of theh url.

for PUT: it takes input of JSON format and can be used to update a farmer's details i.e. first
name, last name, phone number etc.
it returns a response showing a success message for updating data of the user.

for DELETE: it does not take in any input and returns a message showing succesful deletion of user whose id was given as part of the url.

## api/precipitation/

Allowed methods: GET, POST


## api/precipitation/id/

Allowed methods: GET, PUT, DELETE

## api/crop/

Allowed methods: GET, POST



## api/crop/id/

Allowed methods: GET, PUT, DELETE


