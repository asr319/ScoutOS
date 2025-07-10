from fastapi import Security, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from jose import JWTError, jwt
import os

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=os.getenv("OAUTH_AUTHORIZE_URL", ""),
    tokenUrl=os.getenv("OAUTH_TOKEN_URL", ""),
)

# Default key is for testing only. Set SECRET_KEY in the environment for production.
SECRET_KEY = os.getenv("SECRET_KEY", "CHANGE_ME")
ALGORITHM = "HS256"


async def get_current_user(token: str = Security(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
        return user_id
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
