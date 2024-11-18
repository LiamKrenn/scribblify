from typing import Annotated, Optional, Self, Union
from api.model.base import BaseModel

from pydantic.functional_validators import WrapValidator
from pydantic import model_validator


WRITE = 1
DELETE = 2


class NoteCommand(BaseModel):
    command: int
    cursor: int
    char: Optional[Union[str, None]] = None

    @model_validator(mode="after")
    def validate_command(self) -> Self:
        if self.command not in [WRITE, DELETE]:
            raise ValueError(f"Invalid command. Must be in [{WRITE}, {DELETE}]")

        if self.command != DELETE and self.char == None:
            raise ValueError("Char must be provided for unless for DELETE command")

        return self
