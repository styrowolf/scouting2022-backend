from pydantic import BaseModel
from fastapi import HTTPException, status
from app.models.models import TeamData, Tournament, TournamentMetadata

from app.providers.dataprovider import DataProvider

class TournamentCreationRequest(BaseModel):
    name: str

async def tournament_creation_endpoint(data_provider: DataProvider, team: int, req: TournamentCreationRequest):
    data = data_provider.get_team_data(team)
    
    if data is None:
        data = TeamData(team, [])

    tournament = data.get_tournament_by_id(Tournament.generate_id(req.name))

    if tournament is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"a tournament with name {req.name} already exists",
        )
    
    data.put_tournament(Tournament.from_name(req.name))
    data_provider.put_team_data(data)
    return {"detail": f"tournament with name {req.name} created"}