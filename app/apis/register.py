from fastapi import HTTPException, status
from pydantic import BaseModel, EmailStr

from app.providers.authenticationprovider import AuthenticationProvider

class RegistrationRequest(BaseModel):
    email: EmailStr
    password: str

async def registration_endpoint(auth: AuthenticationProvider, req: RegistrationRequest):
    result = auth.register_new_user(req.email, req.password)
    if result:
        return {"detail": f"user with email {req.email} has been registered"}
    raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="user already registered",
        )