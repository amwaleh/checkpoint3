
# checkpoint3
[![Coverage Status](https://coveralls.io/repos/andela-amwaleh/checkpoint3/badge.svg?branch=feature%2Ftest&service=github)](https://coveralls.io/github/andela-amwaleh/checkpoint3?branch=feature%2Ftest)
[![Build Status](https://travis-ci.org/andela-amwaleh/checkpoint3.svg?branch=feature%2Ftest)](https://travis-ci.org/andela-amwaleh/checkpoint3)
[![Code Issues](https://www.quantifiedcode.com/api/v1/project/36021450ea624bebb9a47d637b01ed9c/badge.svg)](https://www.quantifiedcode.com/app/project/36021450ea624bebb9a47d637b01ed9c)

# Introduction
Bucketlist is an API created using Flask Framework 
### Requirements
- Postgres
- Django
- Django restFramework


### Installation
####Setup Postgress
- Download the repo
- Download and install [postgres](http://www.postgresql.org/)
- Create a databases in Postgres called 'bucketlist'
  - In the Psql Terminal run :
    - `CREATE DATABASE bucketlist`
- At the Terminal cd into the project folder and run the following commands 
 * `pip install -r requirements.txt` to install all dependencies
 * `Python manage.py makemigrations`
 * `python manage.py  migrate`
 * `python manage.py runserver` to start the server
 * In your browser navigate to `http://localhost:8000/web/`
  - this will lead to the web page 
 * You can also navigate to `http://localhost:8000/api/`
  - to access the API view 
 

### API Endpoints

| End Point                                | Functionality                     |
|------------------------------------------|-----------------------------------|
| POST /auth/login                         | Logs a user in                    |
| POST /api/users                          | Create a user                   |
| ![secure](https://cdn0.iconfinder.com/data/icons/social-messaging-ui-color-shapes/128/lock-circle-green-16.png 'logo') GET /auth/logout                         | Logs a user out                   |
| ![secure](https://cdn0.iconfinder.com/data/icons/social-messaging-ui-color-shapes/128/lock-circle-green-16.png 'logo') POST /api/bucketlists/                       | Create a new bucket list          |
| ![secure](https://cdn0.iconfinder.com/data/icons/social-messaging-ui-color-shapes/128/lock-circle-green-16.png 'logo') GET /api/bucketlists/                        | List all the created bucket lists |
| ![secure](https://cdn0.iconfinder.com/data/icons/social-messaging-ui-color-shapes/128/lock-circle-green-16.png 'logo') GET /api/bucketlists/<id>                    | Get single bucket list            |
|![secure](https://cdn0.iconfinder.com/data/icons/social-messaging-ui-color-shapes/128/lock-circle-green-16.png 'logo') PUT /api/bucketlists/<id>                    | Update this bucket list           |
| ![secure](https://cdn0.iconfinder.com/data/icons/social-messaging-ui-color-shapes/128/lock-circle-green-16.png 'logo') DELETE /api/bucketlists/<id>                 | Delete this single bucket list    |
| ![secure](https://cdn0.iconfinder.com/data/icons/social-messaging-ui-color-shapes/128/lock-circle-green-16.png 'logo') POST /api/bucketlists/<id>/items/            | Create a new item in bucket list  |
| ![secure](https://cdn0.iconfinder.com/data/icons/social-messaging-ui-color-shapes/128/lock-circle-green-16.png 'logo') PUT /api/bucketlists/<id>/items/<item_id>    | Update a bucket list item         |
| ![secure](https://cdn0.iconfinder.com/data/icons/social-messaging-ui-color-shapes/128/lock-circle-green-16.png 'logo') DELETE /api/bucketlists/<id>/items/<item_id> | Delete an item in a bucket list   |
- NB. ![secure](https://cdn0.iconfinder.com/data/icons/social-messaging-ui-color-shapes/128/lock-circle-green-16.png 'logo') Need login or Authorization Token 

### Accessing API
- Once the server is runnng, navigate to `http://localhost:8000/api/users` using Postman 
- Click the header tab and set the Header to `content_type: application/json`
- Click the body tab and select on the `raw` option 
- We shall be using this section for most of our requests
- Json format will be used in sending and recieving request

### Creating Users

- Using the `POST` Method on Postman 
- Navigate to `http://localhost:8000/api/users/`.
- Enter username and password in json format in the textarea :
      - request :  `{ "username":"admin", "password":"12345"}`

      - response :
      ```python
                    {
                     "username": "admin"
                    }
      ```


### Login
- Using `POST` method on the Postman
- Navigate to `http://localhost:8000/auth/login/`.
- Enter username and password 
  -   request : `{
                   "username":"admdin",
                    "password":"12345"
                }`
  - response  : 
  ```python
        {
              "token": "eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ1MDcyNzAxNywiaWF0IjoxNDUwNzI2NDE3fQ......."
               }
  ```
- A token will be returned.
- Copy the value of the token
- click on the header and add a key called `Authorization` and paste the copied token in to the value field
  - `JWT <TOKEN_VALUE>` e.g `Authorization : JWT eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ1MDcyNzAxNywiaWF0........`
  - *** the API uses JWT Token for authorization ***
- This token will be used to access all the necesary endpoints till it expires
- Note: Authentication relies on the token all other pages can only be accessed once a valid token is presented


### Adding Bucketlist
- Navigate to `http://localhost:8000/api/bucketlists/`.
- Set request method to `POST`
- make sure the token is set in the Header and you have logged in 
- Enter name of the bucketlist in the textarea and click send
    - request : ``` { "name": "Bucketlist1" }```
    - response :
    ```
                    {
                      "name": "digger",
                      "created_by": 2,
                      "created_on": "Mon, 21 Dec 2015 22:51:26 GMT",
                      "modified_on": "Mon, 21 Dec 2015 23:04:14 GMT",
                      "id": 2
                    }
    ```

### Editing Bucketlist
- Navigate to `http://localhost:8000/api/bucketlists/<id>/,`.
- Set request method to `PUT`
- make sure the token is set in the Header if you have logged in
- You can update the `name`  field which the id provided belongs 
    - request : `{"name":"digger"}`
    - response : `{ "Bucketlist": [ [ "digger" ] ] }`

### Deleting Bucketlist
- Navigate to `http://localhost:8000/api/bucketlists/<id>/,`.
- Set request method to `DELETE`
- replace `<id>` with id you want to delete
- click send

### Adding Item
-  Navigate to `http://localhost:8000/api/bucketlists/<id>/items/`.
-  Replace `<id>` with id of bucketlist you want to add item to 
- Set request method to `POST`
  - request : `{"name":"buy equipment"}`
  - response :
  ```python
    
    
      {
        "name": "digger",
        "items": [
          {
            "date_created": "Mon, 21 Dec 2015 23:15:09 GMT",
            "date_modified": "Mon, 21 Dec 2015 23:15:09 GMT",
            "done": false,
            "id": 3,
            "name": "buy equipment"
          }
        ],
        "created_by": 2,
        "created_on": "Mon, 21 Dec 2015 22:51:26 GMT",
        "modified_on": "Mon, 21 Dec 2015 23:04:14 GMT",
        "id": 2
      }
    
 
  ```
- To view all  items in a bucketlist set method to `GET`
- navigate to `http://localhost:8000/api/bucketlists/<id>/items/`.

### Editing or Deleteing an Item 

- To Edit :
    - Navigate to `http://localhost:8000/api/bucketlists/<id>/item/<item_id>/`.
    - Set request method to `put `
    - replace `<id>` with id of bucketlist and `<item_id>` with the id of item you want to edit
      *   send a request containing either `name` or `done` fields
      *   request : `{"done":"True"}`
      *   response :
      ```python 
          
                {
                  "done": true,
                  "name": "buy equipment"
                }
            
      ```
- To Delete Item
    - Navigate to `http://localhost:8000/api/bucketlists/<id>/item/<item_id>/`.
    - Set request method to `DELETE `
    - replace `<id>` with id of bucketlist and `<item_id>` with the id of item you want to edit
    - Send request
    
### Tests
- To run test use any of the following commands
    * `coverage run --omit="*env*","migrations*","web*","static","templates","test*" -m manage.py tests`
    * `python manage.py tests`
   
