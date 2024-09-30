from sqlalchemy.orm import Query
from api.model.page import Page


def pageinate(cursor: Query, page: Page):
    if page.limit < 0:
        raise ValueError("Limit value cannot be negative")
    if page.skip < 0:
        raise ValueError("Skip value cannot be negative")

    return cursor.limit(page.limit).offset(page.skip)
