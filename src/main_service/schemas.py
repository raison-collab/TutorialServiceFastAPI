from pydantic import BaseModel


class SubjectSchema(BaseModel):
    name: str


class SubjectResponseSchema(BaseModel):
    id: int
    name: str


class ServiceSchema(BaseModel):
    subject_id: int
    user_id: int
    amount: float
    info: str


class ServiceResponseSchema(ServiceSchema):
    id: int


class StatusSchema(BaseModel):
    name: str


class StatusResponseSchema(StatusSchema):
    id: int


class OrderSchema(BaseModel):
    service_id: int
    user_id: int
    status_id: int


class OrderResponseSchema(OrderSchema):
    id: int


class DeleteResponseSchema(BaseModel):
    id: int
