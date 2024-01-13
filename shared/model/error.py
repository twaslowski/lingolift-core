from pydantic import BaseModel


class LingoliftError(BaseModel):
    error_message: str
