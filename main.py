# main.py
from fastapi import FastAPI, HTTPException
from models import Blog, BlogCreate
from database import blog_collection
from bson import ObjectId
from typing import List
import datetime

app = FastAPI()

# Utility to convert MongoDB document to Pydantic model
def blog_serializer(blog) -> Blog:
    blog["_id"] = str(blog["_id"])
    return Blog(**blog)

@app.post("/blogs/", response_model=Blog)
async def create_blog(blog: BlogCreate):
    blog_data = blog.dict()
    blog_data["created_at"] = datetime.utcnow()
    result = await blog_collection.insert_one(blog_data)
    new_blog = await blog_collection.find_one({"_id": result.inserted_id})
    return blog_serializer(new_blog)

@app.get("/blogs/", response_model=List[Blog])
async def get_blogs():
    blogs = []
    async for blog in blog_collection.find():
        blogs.append(blog_serializer(blog))
    return blogs

@app.get("/blogs/{blog_id}", response_model=Blog)
async def get_blog(blog_id: str):
    blog = await blog_collection.find_one({"_id": ObjectId(blog_id)})
    if blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog_serializer(blog)

@app.put("/blogs/{blog_id}", response_model=Blog)
async def update_blog(blog_id: str, updated_blog: BlogCreate):
    result = await blog_collection.update_one(
        {"_id": ObjectId(blog_id)}, {"$set": updated_blog.dict()}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Blog not found")
    blog = await blog_collection.find_one({"_id": ObjectId(blog_id)})
    return blog_serializer(blog)

@app.delete("/blogs/{blog_id}")
async def delete_blog(blog_id: str):
    result = await blog_collection.delete_one({"_id": ObjectId(blog_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Blog not found")
    return {"message": "Blog deleted successfully"}
