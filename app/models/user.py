from pydantic import BaseModel, EmailStr

class User(BaseModel):
    email: EmailStr
    teams: list[int]

class UserInDB(User):
    hashed_password: str

    def to_user(self):
        return User(email=self.email, teams=self.teams)
