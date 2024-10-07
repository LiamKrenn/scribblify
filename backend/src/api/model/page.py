from api.model.base import Base
from pydantic import BaseModel


class Page(Base):
    skip: int = 0
    limit: int = 10
