from pydantic import BaseModel
from typing import Union

class Article(BaseModel):
    title: str
    content: str
    hidden: bool
