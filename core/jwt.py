import os
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

JWT_SECRET: str = os.environ["JWT_SECRET"]
JWT_ALGORITHM: str = os.environ.get("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_MINUTES: int = int(
    os.environ.get("JWT_EXPIRE_MINUTES", "60")
)

security = HTTPBearer()

class CurrentUser(BaseModel):
    id: int
    name: str
    email: str


def create_access_token(
    *,
    id: int,
    name: str,
    email: str,
) -> str:

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=JWT_EXPIRE_MINUTES
    )

    return jwt.encode(  # pyright: ignore[reportUnknownMemberType]
        {
            "id": id,
            "name": name,
            "email": email,
            "exp": int(expire.timestamp()),
        },
        JWT_SECRET,
        algorithm=JWT_ALGORITHM,
    )


def verify_token(token: str) -> CurrentUser:

    try:
        payload = jwt.decode(  # pyright: ignore[reportUnknownMemberType]
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM],
        )

        return CurrentUser.model_validate(payload)

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token expired",
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )
        


def get_current_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials,
        Depends(security),
    ],
) -> CurrentUser:

    token = credentials.credentials

    return verify_token(token)
