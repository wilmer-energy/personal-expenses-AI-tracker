from sqlalchemy.orm import Session

from core.security import hash_password
from routers.dtos.create_user import CreateUser
from routers.repositories.user import UserRepository


def execute(dto: CreateUser, db: Session):
    repository = UserRepository(db)
    hashed_pwd = hash_password(dto.password)
    user_data = dto.model_dump()
    user_data["password"] = hashed_pwd
    new_user = repository.create(user_data)

    return new_user
