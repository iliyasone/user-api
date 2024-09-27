from typing import Literal
from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
import crud, models, schemas, database
from utils import construct_post_response

def lifespan(app: FastAPI):
    print("Starting up...")
    models.Base.metadata.create_all(bind=database.engine)    
    yield  # The app runs between yield points
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)

def get_user_ip(request: Request) -> str:
    ip = request.client.host
    return ip

@app.get("/posts", response_model=list[schemas.PostResponse])
def get_posts(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db), user_ip: str = Depends(get_user_ip)):
    posts = crud.get_posts(db, skip=skip, limit=limit)
    # print(f'{[construct_post_response(post, db, user_ip) for post in posts]=}')
    return [construct_post_response(post, db, user_ip) for post in posts]

@app.get("/posts/{post_id}", response_model=schemas.PostResponse)
def get_post(post_id: int, db: Session = Depends(database.get_db), user_ip: str = Depends(get_user_ip)):
    post = crud.get_post(db, post_id=post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return construct_post_response(post, db, user_ip)

@app.put("/posts", response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(database.get_db), user_ip: str = Depends(get_user_ip)):
    return construct_post_response(crud.create_post(db, post=post), db, user_ip)


@app.post("/posts/{post_id}/vote", response_model=schemas.PostResponse)
def vote_on_post(post_id: int, vote: schemas.VoteCreate, db: Session = Depends(database.get_db), user_ip: str = Depends(get_user_ip)):
    post = crud.get_post(db, post_id=post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if post.hide_rating:
        raise HTTPException(status_code=400, detail="Voting is disabled for this post")


    crud.vote_on_post(db, post_id=post_id, vote=vote, user_ip=user_ip)
    
    # Recalculate the rating and return the updated post
    return construct_post_response(post, db, user_ip)