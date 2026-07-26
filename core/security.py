from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher

# Inicializamos el hasher con Argon2 (o BcryptHasher si prefieres)
password_hash = PasswordHash((Argon2Hasher(),))


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)
