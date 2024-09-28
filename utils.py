from sqlalchemy.orm import Session
import crud, models, schemas, database

def construct_post_response(post: models.Post, db: Session, user_ip: str) -> schemas.PostResponse:
    votes = crud.get_all_votes(db, post.id)
    
    rating = sum([vote.vote for vote in votes])
    
    user_vote = 0
    for vote in votes:
        if vote.ip == user_ip:
            user_vote = vote.vote
            break

    return schemas.PostResponse(
        id=post.id,
        label=post.label,
        content=post.content,
        hideRating=post.hide_rating,
        rating=rating,
        published_time=post.published_time,
        vote=user_vote,
    )
