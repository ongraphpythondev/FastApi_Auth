from fastapi import FastAPI , status , Depends
from models import Base, engine , User , Post
from schema import UserSchema , UserLoginSchema , PostSchema
from auth.jwt_handler import signJWT
from sqlalchemy.orm import Session
from fastapi import HTTPException
from auth.jwt_bearer import jwtBearer

app = FastAPI()


# Create the database
Base.metadata.create_all(engine)


@app.post("/user/signup" , status_code=status.HTTP_201_CREATED ,  tags=["users"])
def signup(user : UserSchema) -> dict:

    """
    User is created by username , email , password , age credential

    Returns:
    dict: It contain token
    
    """

    # create a new database session
    session = Session(bind=engine, expire_on_commit=False) 

    # create an instance of the user database model
    userobj = User(name = user.name , email = user.email ,password = user.password , age = user.age )

    # add it to the session and commit it
    session.add(userobj)
    session.commit()

    # close the session
    session.close() 


    return signJWT(user.email)

def check_user(userdata : UserLoginSchema) -> bool:

    """
    It checks the user exists or not
  
    Parameters:
    userdata (UserLoginSchema): It is the user data that we need to check
  
    Returns:
    bool: True is user exist False if not
  
    """

    # create a new database session
    session = Session(bind=engine, expire_on_commit=False) 

    # it check that user with this detail present or not
    userobj = session.query(User).filter(User.email==userdata.email, User.password==userdata.password)

    # close the session
    session.close() 

    if not userobj:
        return False
    else:
        return True

@app.post("/user/login" , tags=["users"])
def login(user : UserLoginSchema) -> dict:
    """
    It login the user if credential is correct 

    Returns:
    dict: It contain token
  
    """

    # we call check_user it tell user is present or not in database
    if check_user(user):
        return signJWT(user.email)
    else: 
        raise HTTPException(status_code=404, detail=f"User not found")
        
@app.put("/user/update" , tags=["users"])
def update_todo(userdata : UserSchema , Tokenpayload = Depends(jwtBearer())) -> User:
    """
    It update the user data
  
    Parameters:
    userdata (UserSchema): It is the user data that we need to update
    Tokenpayload (dict) : It is the token to authenticate user
  
    Returns:
    User: user object
  
    """

    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get the user data from token
    userobj = session.query(User).filter(User.email == Tokenpayload["userID"]).first()

    # update user data
    if userobj:
        userobj.name = userdata.name
        userobj.email = userdata.email
        userobj.password = userdata.password
        userobj.age = userdata.age
        session.commit()

    # close the session
    session.close()

    if not userobj:
        raise HTTPException(status_code=404, detail=f"User not found")

    return userobj


@app.get("/user/profile" , tags=["users"])
def profile(Tokenpayload = Depends(jwtBearer())) -> User:
    """
    It get the user credintial
  
    Parameters:
    Tokenpayload (dict) : It is the token to authenticate user
  
    Returns:
    User: user object
  
    """

    # create a new database session
    session = Session(bind=engine, expire_on_commit=False) 


    # it check that user with this detail present or not
    userobj = session.query(User).filter(User.email == Tokenpayload["userID"]).first()

    # close the session
    session.close() 
    return userobj


@app.post("/post/insert" , tags=["post"])
def post_insert(post : PostSchema , Tokenpayload = Depends(jwtBearer())) -> Post:
    """
    It is to insert post
  
    Parameters:
    post (PostSchema): It is the post data 
    Tokenpayload (dict) : It is the token to authenticate user
  
    Returns:
    Post: post object
  
    """

    # create a new database session
    session = Session(bind=engine, expire_on_commit=False) 


    # create an instance of the post database model
    postobj = Post(title = post.title , description = post.description )

    # add it to the session and commit it
    session.add(postobj)
    session.commit()

    # close the session
    session.close() 
    return postobj


@app.get("/posts" , tags=["post"])
def posts(Tokenpayload = Depends(jwtBearer())) -> list[Post]:
    """
    It shows all post
  
    Parameters:
    Tokenpayload (dict) : It is the token to authenticate user
  
    Returns:
    Post: post object
  
    """

    # create a new database session
    session = Session(bind=engine, expire_on_commit=False) 

    # create an instance of the post database model
    postobjs = session.query(Post).all()

    # close the session
    session.close() 
    return postobjs



@app.get("/post/{id}" , tags=["post"])
def post( id:int ,Tokenpayload = Depends(jwtBearer())) -> Post:
    """
    It shows one post
  
    Parameters:
    id (int) : id of the post
    Tokenpayload (dict) : It is the token to authenticate user
  
    Returns:
    Post: post object
  
    """

    # create a new database session
    session = Session(bind=engine, expire_on_commit=False) 

    # create an instance of the post database model
    postobj = session.query(Post).get(id)

    if postobj:
        session.delete(postobj)
        session.commit()
        session.close()
    else:
        raise HTTPException(status_code=404, detail=f"Post not found")

    # close the session
    session.close() 
    return postobj


@app.delete('/post/{id}'  , tags=["post"])
def post_del(id: int , Tokenpayload = Depends(jwtBearer())) -> str:
    """
    It delete post
  
    Parameters:
    id (int) : id of the post
    Tokenpayload (dict) : It is the token to authenticate user
  
    Returns:
    str: message that message is deleted
  
    """

    # create a new database session
    session = Session(bind=engine, expire_on_commit=False) 

    postobj = session.query(Post).get(id)

    # if todo item with given id exists, delete it from the database. Otherwise raise 404 error
    if postobj:
        session.delete(postobj)
        session.commit()
        session.close()
    else:
        raise HTTPException(status_code=404, detail=f"Post not found")

    # close the session
    session.close() 

    return {"message": "post delete"}
        

@app.put("/post/update/{id}" , tags=["post"])
def update_todo(id: int ,post : PostSchema ,Tokenpayload = Depends(jwtBearer())) -> Post:
    """
    It delete post
  
    Parameters:
    id (int) : id of the post
    post (PostSchema) : post data to updated
    Tokenpayload (dict) : It is the token to authenticate user
  
    Returns:
    Post: updated post object
  
    """

    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get the todo item with the given id
    postobj = session.query(Post).get(id)

    # update todo item with the given task (if an item with the given id was found)
    if postobj:
        postobj.title = post.title
        postobj.description = post.description
        session.commit()

    # close the session
    session.close()

    # check if todo item with given id exists. If not, raise exception and return 404 not found response
    if not postobj:
        raise HTTPException(status_code=404, detail=f"todo item with id {id} not found")

    return postobj


