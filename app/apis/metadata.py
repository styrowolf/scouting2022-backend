from app.models.models import TeamDataMetadata, TournamentMetadata
from app.providers.dataprovider import DataProvider

async def metadata_endpoint(data_provider: DataProvider, team: int):
    data = data_provider.get_team_data(team)
    if data is None:
        return TeamDataMetadata(team=team, tournaments=[])
    return data.to_metadata()
