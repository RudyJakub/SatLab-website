from pydantic import BaseModel
from typing import Optional

class Article(BaseModel):
    title: str
    content: str
    hidden: Optional[bool] = True
    image: Optional[str] = ""

class LoginCredentials(BaseModel):
    password: str
