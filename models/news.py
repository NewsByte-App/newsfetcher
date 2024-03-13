from pydantic import BaseModel
from datetime import datetime


class News(BaseModel):
    title: str
    content: str
    description: str
    summary: str
    url: str
    category: str
    author: str
    image_url: str
    published_date: datetime = datetime.now()
    created_at: datetime = datetime.now()
    summarized: bool = False
