from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles

from deta import Deta
from jose import jwt, JWTError
from app.apis.register import RegistrationRequest, registration_endpoint
from app.apis.match_creation import MatchCreationRequest, match_creation_endpoint
from app.apis.metadata import metadata_endpoint
from app.apis.retrieve_data import retrieve_data_endpoint
from app.apis.team_match_stats_addition import team_match_stats_addition_endpoint
from app.apis.tournament_creation import TournamentCreationRequest, tournament_creation_endpoint
from app.models.models import TeamData, TeamDataMetadata, TeamMatchStats

from app.models.token import Token
from app.models.user import User
from app.providers.authenticationprovider import AuthenticationProvider
from app.providers.dataprovider import DataProvider
from app.providers.tokenprovider import TokenProvider


# deta
# project id: a0pvuks1
# project key: a0pvuks1_DqYg7DWJaY9q2xq918Dz7sSnFBn777NM
deta_project_key = "a0pvuks1_DqYg7DWJaY9q2xq918Dz7sSnFBn777NM"

deta = Deta(deta_project_key)

app = FastAPI()

auth_provider = AuthenticationProvider(deta)
token_provider = TokenProvider()
data_provider = DataProvider(deta)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/")
async def index():
    from fastapi.responses import RedirectResponse
    return RedirectResponse("/static/index.html")

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth_provider.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = token_provider.get_token(user.to_user())
    return {"access_token": access_token, "token_type": "bearer"}

async def get_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, token_provider.SECRET_KEY)
        user = User(**payload)
    except:
        raise credentials_exception
    return user

def check_team(user: User, team: int):
    if user.teams.count(team) != 1:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        raise credentials_exception
    return True


@app.post("/register")
async def register(request: RegistrationRequest):
    return await registration_endpoint(auth_provider, request)

@app.get("/metadata/{team}", response_model=TeamDataMetadata)
async def metadata(team: int, user: User = Depends(get_user)):
    if check_team(user, team):
        return await metadata_endpoint(data_provider, team)
    
@app.post("/create/{team}/tournament")
async def create_tournament(team: int, request: TournamentCreationRequest, user: User = Depends(get_user)):
    if check_team(user, team):    
        return await tournament_creation_endpoint(data_provider, team, request)

@app.post("/create/{team}/{tournament_id}/match")
async def create_match(team: int, tournament_id: str, request: MatchCreationRequest, user: User = Depends(get_user)):
    if check_team(user, team):
        return await match_creation_endpoint(data_provider, team, tournament_id, request)

@app.post("/add/{team}/{tournament_id}/{match_id}")
async def add_team_match_stats(team: int, tournament_id: str, match_id: str, tms: TeamMatchStats, user: User = Depends(get_user)):
    if check_team(user, team):
        return await team_match_stats_addition_endpoint(data_provider, team, tournament_id, match_id, tms)

@app.get("/data/{team}", response_model=TeamData)
async def get_data(team: int, user: User = Depends(get_user)):
    if check_team(user, team):
        return await retrieve_data_endpoint(data_provider, team)


app.mount("/", StaticFiles(directory="static"), name="static")