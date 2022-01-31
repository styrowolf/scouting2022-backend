from fastapi import HTTPException, status

from app.models.models import TeamMatchStats, Match
from app.providers.dataprovider import DataProvider

async def team_match_stats_addition_endpoint(data_provider: DataProvider, team: int, tournament_id: str, match_id: str, tms: TeamMatchStats):
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
    
    match = tournament.get_match_by_id(match_id)

    if match is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"no such match has been found",
        )
    
    match.put_stats(tms)
    tournament.put_match(match)
    data.put_tournament(tournament)
    data_provider.put_team_data(data)
    return {"detail": f"stats added successfully"}