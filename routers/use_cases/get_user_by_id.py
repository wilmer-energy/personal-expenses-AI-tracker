from fastapi import HTTPException
from sqlalchemy.orm import Session

from routers.repositories.user import UserRepository


def execute(id: int, db: Session):
    repository = UserRepository(db)
    user = repository.get_by_id(id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
