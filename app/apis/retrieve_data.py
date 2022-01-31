from app.models.models import TeamData
from app.providers.dataprovider import DataProvider

async def retrieve_data_endpoint(data_provider: DataProvider, team: int):
    data = data_provider.get_team_data(team)
    if data is None:
        data = TeamData(team=team, tournaments=[])
    return data