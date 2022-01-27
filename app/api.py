from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from deta import Deta
from jose import jwt, JWTError

from app.models import Token, User
from app.authenticationprovider import AuthenticationProvider
from app.tokenprovider import TokenProvider

# deta
# project id: a0pvuks1
# project key: a0pvuks1_DqYg7DWJaY9q2xq918Dz7sSnFBn777NM
deta_project_key = "a0pvuks1_DqYg7DWJaY9q2xq918Dz7sSnFBn777NM"

deta = Deta(deta_project_key)

app = FastAPI()

auth = AuthenticationProvider(deta)
token_provider = TokenProvider()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/")
async def index():
    return {"message": "fu"}

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth.authenticate_user(form_data.username, form_data.password)
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
        payload = jwt.decode(token, token_provider.SECRET_KEY, algorithms=[token_provider.ALGORITHM])
        user = User(**payload)
    except:
        raise credentials_exception
    return user
