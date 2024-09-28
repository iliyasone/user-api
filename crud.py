from sqlalchemy.orm import Session
import models, schemas
from time import time

def create_post(db: Session, post: schemas.PostCreate):
    db_post = models.Post(
        label=post.label, 
        content=post.content, 
        hide_rating=post.hideRating,
        published_time=int(time()))
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_post(db: Session, post_id: int):
    return db.query(models.Post).filter(models.Post.id == post_id).first()

def get_posts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Post).order_by(models.Post.id.desc()).offset(skip).limit(limit).all()

def get_all_votes(db: Session, post_id: int) -> list[models.Vote]:
    return db.query(models.Vote).filter(models.Vote.post_id == post_id).all()

def get_vote_by_ip(db: Session, post_id: int, ip: str):
    return db.query(models.Vote).filter(models.Vote.post_id == post_id, models.Vote.ip == ip).first()

def vote_on_post(db: Session, post_id: int, vote: schemas.VoteCreate, user_ip: str):
    existing_vote = get_vote_by_ip(db, post_id=post_id, ip=user_ip)
    if existing_vote:
        existing_vote.vote = vote.vote
    else:
        new_vote = models.Vote(post_id=post_id, ip=user_ip, vote=vote.vote)
        db.add(new_vote)
    db.commit()
    return vote

def delete_vote_by_ip(db: Session, post_id: int, user_ip: str):
    vote = get_vote_by_ip(db, post_id=post_id, ip=user_ip)
    if vote:
        db.delete(vote)
        db.commit()
        return True
    return False