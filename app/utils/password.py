from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password_hash(password: str, hash_str: str) -> bool:
    return pwd_context.verify(password, hash_str)
