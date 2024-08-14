from typing import List

from pydantic import BaseModel


class ExceptionSchema(BaseModel):
    """Base Exception Schema."""
    detail: str


class ExceptionValidationFieldSchema(BaseModel):
    """Exception Validation Field Schema."""
    field: str = 'field name'
    message: str = 'message error'


class ExceptionValidationSchema(BaseModel):
    """Base Exception Validation Schema."""
    detail: List[ExceptionValidationFieldSchema]
