from pydantic import BaseModel


class ApplicationError(BaseModel):
    error_message: str
