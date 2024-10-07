from api.model.base import Base


class Tag(Base):
    name: str


class TagSchema(Tag):
    id: int
