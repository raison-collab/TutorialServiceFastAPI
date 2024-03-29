import sqladmin

from src.auth.database import Role, User
from src.main_service.models import SubjectModel, ServiceModel, OrderModel, StatusModel


class RoleAdmin(sqladmin.ModelView, model=Role):
    column_list = [Role.id, Role.name]


class UserAdmin(sqladmin.ModelView, model=User):
    column_list = [User.id, User.email, User.role_id, User.first_name, User.last_name]


class SubjectAdmin(sqladmin.ModelView, model=SubjectModel):
    column_list = [SubjectModel.id, SubjectModel.name]


class ServiceAdmin(sqladmin.ModelView, model=ServiceModel):
    column_list = [ServiceModel.id, ServiceModel.user_id, ServiceModel.subject_id, ServiceModel.amount]


class OrderAdmin(sqladmin.ModelView, model=OrderModel):
    column_list = [OrderModel.id, OrderModel.service_id, OrderModel.user_id, OrderModel.status_id]


class StatusAdmin(sqladmin.ModelView, model=StatusModel):
    column_list = [StatusModel.id, StatusModel.name]
