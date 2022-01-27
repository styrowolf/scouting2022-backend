from pydantic import EmailStr
from app.constants import PREFIX
from deta import Deta, _Base
from passlib.context import CryptContext

from app.models import UserInDB
from typing import Optional

class AuthenticationProvider:
    pwd_context: CryptContext = CryptContext(schemes=["argon2"], deprecated="auto")
    db: _Base
    def __init__(self, deta: Deta):
        self.db = deta.Base(PREFIX + "auth")

    def get_user(self, email: EmailStr) -> Optional[UserInDB]:
        user = self.db.get(str(email))
        if user is None:
            return None
        return UserInDB.parse_obj(user)

    def get_hashed_password(self, password: str):
        return self.pwd_context.hash(password)
    
    def verify_password(self, password: str, hashed_password: str):
        return self.pwd_context.verify(password, hashed_password)

    def authenticate_user(self, email: EmailStr, password: str):
        user = self.get_user(email)
        if user is None:
            return False
        if not self.verify_password(password, user.hashed_password):
            return False
        return user

    def register_new_user(self, user: UserInDB):
        try:
            self.db.insert(user.dict(), user.email)
            return True
        except:
            return False
    
    def change_password(self, email: EmailStr, old_password: str, new_password: str):
        user = self.authenticate_user(email, old_password)
        if user:
            user.hashed_password = self.get_hashed_password(new_password)
            self.db.put(user.dict(), str(user.email))
            return True
        return False