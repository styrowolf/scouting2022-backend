import imp
from typing import Optional
from pydantic import BaseModel
from app.models.models import TeamData
from deta import _Base, Deta
from app.constants import PREFIX

class DataProvider():
    db: _Base

    def __init__(self, deta: Deta):
        self.db = deta.Base(PREFIX + "data")
    
    def get_team_data(self, team: int) -> Optional[TeamData]:
        team_data = self.db.get(str(team))
        if team_data is None:
            return None
        return TeamData.parse_obj(team_data)
    
    def put_team_data(self, team_data: TeamData):
        self.db.put(team_data.dict(), str(team_data.team))