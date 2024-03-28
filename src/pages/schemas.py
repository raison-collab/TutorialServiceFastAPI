from typing import Annotated

from fastapi import Form
from pydantic import BaseModel, EmailStr, Field


class UserRegistrationSchema(BaseModel):
    email: str
    password: str
    repeat_password: str
    first_name: str
    second_name: str
    last_name: str
    card_number: str
    role: bool = False
