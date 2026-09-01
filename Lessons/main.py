from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel 
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1,}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

@app.get("/")
def root():
    return {"message" : "Hello World"}

@app.get("/post")
def get_posts():
    return {"data": "This is your post"}

@app.post("/posts")
def create_posts(post: Post):
    post_dict = post
    post_dict['id'] = randrange(0, 193012931203410947104912471289471984721941)
    my_posts.append(post)
    return {"data": "new_post"}


@app.get("/posts/{id}")
def get_post(id):
    print(id)
    return {"post_detail", f"This is your post {id}"}