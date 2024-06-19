from datetime import datetime, timezone
from typing import Optional
from fastapi import Request
from pydantic import BaseModel
from beanie import Document, Indexed

class Events(Document):
    title:Indexed(str,unique=True)
    description:str
    body: str
    author: str
    month:str
    day:str
    created_on: datetime = datetime.now(tz=timezone.utc)

    class Settings:
        name = "event"
class EventForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.form_data = {}

    async def create_form_data(self):
        form = await self.request.form()
        for key, value in form.items():
            self.form_data[key] = value