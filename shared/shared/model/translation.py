from pydantic import BaseModel


class Translation(BaseModel):
    translation: str
    language: str
