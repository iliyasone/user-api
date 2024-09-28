from pydantic import BaseModel
from typing import Literal

class VoteCreate(BaseModel):
    vote: Literal[-1, 1]

class PostCreate(BaseModel):
    label: str
    content: str
    hideRating: bool

class PostResponse(BaseModel):
    id: int
    label: str
    content: str
    hideRating: bool
    rating: int
    published_time: int
    vote: Literal[-1, 0, 1]
