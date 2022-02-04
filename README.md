# FastApi Auth
This POC is an example of authentication apis to any project. This POC includes the following:
  1) user registration
  2) user login
  3) user update
  4) user profile

This POC uses jwt tokens for the authentications (https://jwt.io/). <br>
User must login before using profile .
  
# Prerequisites
You will need the following programmes properly installed on your computer.<br>
Python 3.7+

# Installation and Running

clone the repository
```
git clone https://github.com/ongraphpythondev/FastApi_Auth.git
cd FastApi_Auth
```
create a vertual environment
```
python3 -m venv .venv
.venv/bin/activate.bat
```
install required packages
```
pip install -r requirements.txt
```
running
```
uvicorn main:app --reload
```
# Functionalities Included:
   1) User Registration
   2) User Login
   3) User Update
   4) User Profile
   5) post create
   6) post update
   7) post delete
   8) post show

# Testing:
registration/authentication : http://localhost:8000/user/signup <br>
login/authentication : http://localhost:8000/user/login  <br>
update/functionalities : http://localhost:8000/user/update  <br>
profile/functionalities : http://localhost:8000/user/profile  <br>
post/create : http://localhost:8000/post/insert <br>
posts/allposts : http://localhost:8000/posts  <br>
post/show post : http://localhost:8000/post/{id} <br>
post/delete : http://localhost:8000/post/{id} <br>
post/update : http://localhost:8000//post/update/{id} <br>

# Format 
* Registration : {<br>
                    "name": "string",<br>
                    "email": "user@example.com",<br>
                    "password": "string",<br>
                    "age": 0<br>
                }<br>

* Login : {<br>
            "email": "user@example.com",<br>
            "password": "string"<br>
        }<br>
* Profile and Update : user must send token in the header .
        