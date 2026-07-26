from sqlalchemy.orm import Session

from routers.repositories.user import UserRepository


def execute(db: Session):
    repository = UserRepository(db)
    return repository.get_all()
