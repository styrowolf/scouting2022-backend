from pydantic import BaseModel, EmailStr
from enum import Enum, auto

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    email: EmailStr
    teams: list[int]

class UserInDB(User):
    hashed_password: str

    def to_user(self):
        return User(self.email, self.teams)

class AllianceColor(Enum):
    BLUE = auto()
    RED = auto()

class TeamMatchStats(BaseModel):
    match_name: str
    alliance_color: AllianceColor
    team: int

class Tournament(BaseModel):
    name: str
    matches: list[TeamMatchStats]
