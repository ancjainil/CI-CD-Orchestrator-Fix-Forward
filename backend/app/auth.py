from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .config import get_settings

bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_role(
    credentials: HTTPAuthorizationCredentials | None = Security(bearer_scheme),
) -> str:
    settings = get_settings()
    if not credentials:
        return "viewer"
    token = credentials.credentials
    if token == settings.jwt_secret:
        return "admin"
    if token == f"{settings.jwt_secret}-operator":
        return "operator"
    return "viewer"


def require_operator(role: str = Depends(get_current_role)) -> str:
    if role not in {"operator", "admin"}:
        raise HTTPException(status_code=403, detail="Operator role required")
    return role
