from pydantic import BaseModel


class Translation(BaseModel):
    translation: str
    language_name: str
    language_code: str
