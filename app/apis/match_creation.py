from pydantic import BaseModel
from fastapi import HTTPException, status
from app.models.models import TeamData, Tournament, Match

from app.providers.dataprovider import DataProvider

class MatchCreationRequest(BaseModel):
    name: str

async def match_creation_endpoint(data_provider: DataProvider, team: int, tournament_id: str, req: MatchCreationRequest):
    data = data_provider.get_team_data(team)
    
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"team has no tournaments",
        )

    tournament = data.get_tournament_by_id(tournament_id)

    if tournament is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"no such tournament has been found",
        )
    
    tournament.put_match(Match.from_name(req.name))
    data.put_tournament(tournament)
    data_provider.put_team_data(data)
    return {"detail": f"match with name {req.name} created in tournament {tournament.name}"}