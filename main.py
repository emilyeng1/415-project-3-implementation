from fastapi import FastAPI, Query, WebSocket, HTTPException
from sqlalchemy import create_engine, text
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

DATABASE1_URL = "postgresql://postgres:testpassword@localhost:5432/reddit_crawler"
DATABASE2_URL = "postgresql://postgres:testpassword@localhost:5432/chan_crawler"
engine = create_engine(DATABASE1_URL)
engine2 = create_engine(DATABASE2_URL)

class Post(BaseModel):
    subreddit: str
    post_title: str
    toxicity_score: str
    data: str

class Comment(BaseModel):
    comment_body: str
    toxicity_score: str

class Thread(BaseModel):
    board: str
    thread_number: int
    post_number: int
    toxicity_score: str
    data: str

class QueryRequest(BaseModel):
    query: str

@app.get("/")
def root():
    return {"message": "Welcome to the Toxicity Dashboard API. Use /interactive-query to submit a query."}

@app.post("/interactive-query")
def interactive_query(request: QueryRequest):
    try:
        with engine.connect() as conn:
            result = conn.execute(text(request.query))
            if hasattr(result, "mappings"):
                out = [dict(row) for row in result.mappings()]
            else:
                out = [dict(zip(result.keys(), row)) for row in result.fetchall()]
        return {"rows": out}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Query failed: {str(e)}")

@app.get("/posts", response_model=List[Post])
def get_posts():
    query = text("SELECT subreddit, post_title, toxicity_score, data FROM posts LIMIT 10")
    with engine.connect() as conn:
        result = conn.execute(query).fetchall()
        posts = [
            {
                "subreddit": row[0], 
                "post_title": row[1], 
                "toxicity_score": row[2] if row[2] is not None else "N/A", 
                "data": row[3].get("selftext", "N/A") if isinstance(row[3], dict) else "N/A"
            }
            for row in result
        ]
    return posts

@app.get("/comments", response_model=List[Comment])
def get_comments():
    query = text("SELECT comment_body, toxicity_score FROM comments LIMIT 10")
    with engine.connect() as conn:
        result = conn.execute(query).fetchall()
        comments = [
            {
                "comment_body": row[0],
                "toxicity_score": row[1] if row[1] is not None else "N/A"
            }
            for row in result
        ]
    return comments

@app.post("/4chan-interactive-query")
def fourchan_interactive_query(request: QueryRequest):
    try:
        with engine2.connect() as conn:
            result = conn.execute(text(request.query))
            if hasattr(result, "mappings"):
                out = [dict(row) for row in result.mappings()]
            else:
                out = [dict(zip(result.keys(), row)) for row in result.fetchall()]
        return {"rows": out}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Query failed: {str(e)}")

@app.get("/threads", response_model=List[Thread])
def get_threads():
    query = text("SELECT board, thread_number, post_number, toxicity_score, data FROM posts LIMIT 10")
    with engine2.connect() as conn:
        result = conn.execute(query).fetchall()
        threads = [
            {
                "board": row[0],
                "thread_number": row[1],
                "post_number": row[2],
                "toxicity_score": row[3] if row[3] is not None else "N/A",
                "data": row[4] if isinstance(row[4], dict) else json.loads(row[4])
            }
            for row in result
        ]
    return threads
