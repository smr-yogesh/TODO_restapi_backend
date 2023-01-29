# TODO Restapi Backend

Foobar is a Python library for dealing with word pluralization.

## Required package Installation 


```bash
pip install -r requirements
```

## Usage

The application takes data in JSON format.

General keywords : 

user: email, passwword

todo : name, description,status

A token is required to perform any todo tasks. Get token form login.

use token as header under key "x-access-token"

links to different functions:

#Signup: /api/v1/signup 

#Signin: /api/v1/signin

#change password: /api/v1/changePassword

#get all todos with status filter /api/v1/todos?status=[status]

#New todo  /api/v1/todos

#Update and Delete /api/v1/todos/:id 
