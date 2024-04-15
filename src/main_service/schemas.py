from pydantic import BaseModel


class SubjectSchema(BaseModel):
    name: str

class ServiceSchema(BaseModel):
    name: str

class StatusSchema(BaseModel):
    name: str

class OrderSchema(BaseModel):
    name: str