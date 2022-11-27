import bcrypt


def get_hashed_password(plain_text_password: str) -> str:
    """Hash a password for the first time"""
    pwd = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    return pwd


def check_password(plain_text_password: str, hashed_password: str) -> bool:
    """Check hashed password. The salt is saved into the hash itself"""
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password.encode('utf-8'))
