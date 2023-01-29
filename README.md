# TODO Restapi Backend

Create your own todo app with this backend 

## Normal run


```bash
#Setup environment
pip install -r requirements
#run app
python app.py
```

Application needs PostgreSQL as Database, please setup it before hand and config auth info in routes/__init.py file.

## Deploy in docker
Want to deploy in docker? I got you.

```bash
docker-compose up --build
```
Once build successful, exit with ctrl+c. wait to exit with ease.

Run image in detached mode.

```bash
docker-compose up -d
```
Remember application is exposed at port 5001 from docker.

## Normal run

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
