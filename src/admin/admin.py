import sqladmin

from src.auth.database import Role, User


class RoleAdmin(sqladmin.ModelView, model=Role):
    column_list = [Role.id, Role.name]


class UserAdmin(sqladmin.ModelView, model=User):
    column_list = [User.id, User.email, User.role_id, User.first_name, User.last_name]
