from pydantic import BaseModel


class Page(BaseModel):
    skip: int = 0
    limit: int = 10
