from random import randrange
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

# schema for our post
class Post(BaseModel):
    title: str
    content: str

# DATABASE CONNECTION    
while True:
    try:
        connection = psycopg2.connect(host='localhost', database='blogmon-api', user='postgres', password='ayushbaisla', cursor_factory=RealDictCursor)
        cursor = connection.cursor()
        print("Database Connection was successful!")
        break
    except Exception as error:
        print("Failed to connect to the database!")
        print("Error : ", error)
        time.sleep(2)

@app.get("/")
def root():
    return {"data" : "Hello World"}

@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"data" : posts}

@app.post("/posts/new", status_code=status.HTTP_201_CREATED)
def posts(post: Post):
    cursor.execute(""" INSERT INTO posts (title, content) VALUES (%s,%s) RETURNING * """, (post.title, post.content))
    new_post = cursor.fetchone()
    connection.commit()
    return {"data" : new_post}

@app.get("/posts/{id}")
def get_post(id: int):  # internal interger validation
    cursor.execute(""" SELECT * FROM posts WHERE id = %s""", (str(id),))
    extracted_post = cursor.fetchone()
    if not extracted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return {"post_detail" : extracted_post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    deleted_post = cursor.fetchone()
    connection.commit()
    if deleted_post == None: 
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"post with id: {id} does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(""" UPDATE posts SET title = %s, content = %s WHERE id = %s RETURNING *""", (post.title, post.content, str(id)))
    updated_post = cursor.fetchone()
    connection.commit()
    if updated_post == None: 
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"post with id: {id} does not exist")
    return {"data" : updated_post}