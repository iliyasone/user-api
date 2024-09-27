from sqlalchemy.orm import Session
import crud, models, schemas, database

def construct_post_response(post: models.Post, db: Session, user_ip: str) -> schemas.PostResponse:
    votes = crud.get_all_votes(db, post.id)
    
    rating = sum([vote.vote for vote in votes])
    is_voted = any([vote.ip == user_ip for vote in votes])
    if post.id == 11:
        print(f'{rating=}')
        print(f'{is_voted=}')
    return schemas.PostResponse(
        id=post.id,
        label=post.label,
        content=post.content,
        hideRating=post.hide_rating,
        rating=rating,
        isVoted=is_voted,
    )
