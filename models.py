# models.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Blog(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    title: str = Field(..., min_length=5, max_length=100)
    content: str = Field(..., min_length=10)
    author: str = Field(..., min_length=3, max_length=50)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class BlogCreate(BaseModel):
    title: str = Field(..., min_length=5, max_length=100)
    content: str = Field(..., min_length=10)
    author: str = Field(..., min_length=3, max_length=50)
