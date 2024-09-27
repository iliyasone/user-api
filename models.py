from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String, index=True)
    content = Column(Text, nullable=False)
    hide_rating = Column(Boolean, default=False)

class Vote(Base):
    __tablename__ = "votes"

    post_id = Column(Integer, ForeignKey("posts.id"), primary_key=True)
    ip = Column(String, nullable=False, primary_key=True)
    vote = Column(Integer)  # 1 or -1
