from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    date_joined = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))    

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    date_posted = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    content = Column(Text, nullable=False)