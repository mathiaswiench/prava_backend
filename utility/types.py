from pydantic import BaseModel


class ActivityRequest(BaseModel):
    file: str
