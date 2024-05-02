from pydantic import BaseModel


class SubjectSchema(BaseModel):
    name: str


class ServiceSchema(BaseModel):
    name: str
    subject_id: int
    user_id: int
    amount: float
    info: str


class StatusSchema(BaseModel):
    name: str


class OrderSchema(BaseModel):
    name: str
    service_id: int
    user_id: int
    status_id: int


class UserServiceData(BaseModel):
    user_id: int
    role_id: int
    f_name: str
    s_name: str
    l_name: str
