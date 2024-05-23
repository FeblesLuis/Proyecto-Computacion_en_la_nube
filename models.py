from pydantic import BaseModel
from typing import List

class User(BaseModel):
    id: int
    path: str
    name: str
    emails: List[str]