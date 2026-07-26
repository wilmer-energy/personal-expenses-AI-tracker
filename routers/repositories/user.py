from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from entities.user import User as UserModel  # Importamos el modelo de la BD7
from routers.dtos.user_by_id import UserResponse


class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, user_data: dict[str, Any]) -> UserModel:
        db_user = UserModel(**user_data)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_by_id(self, id: int) -> UserResponse | None:
        query = select(
            UserModel.id,
            UserModel.name,
            UserModel.email
        ).where(UserModel.id == id)
        row = self.db.execute(query).first()

        if row:
            return UserResponse.model_validate(row)
        return None
    
    def get_all(self) -> list[UserResponse]:
        query = select(
            UserModel.id,
            UserModel.name,
            UserModel.email
        ).where(UserModel.deleted_at.is_(None))
        
        results = self.db.execute(query).mappings().all()

        return [UserResponse.model_validate(row) for row in results]
