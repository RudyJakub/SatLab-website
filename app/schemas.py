from pydantic import BaseModel
from typing import Optional

class Article(BaseModel):
    title: str
    content: str
    hidden: Optional[bool] = True
    image: Optional[str] = ""

class User(BaseModel):
    username: str
    password: str

class LoginCredentials(BaseModel):
    password: str
