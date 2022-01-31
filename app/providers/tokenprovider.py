from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from app.models.user import User

class TokenProvider:
    SECRET_KEY = "8e136c7a2db2c8fd0371c3a2ff1bda6ef52dc0244ee3b2dfd2269ee44de7fa7e"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY)
        return encoded_jwt

    def get_token(self, user: User):
        return self.create_access_token(
            user.dict(),
            expires_delta=timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        )