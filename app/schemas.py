from pydantic import BaseModel
from typing import Union, Optional

class Article(BaseModel):
    title: str
    content: str
    hidden: Optional[bool] = True
    image: Optional[str] = ""
