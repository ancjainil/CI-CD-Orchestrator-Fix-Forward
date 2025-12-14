import os
from typing import Optional

import httpx
import jwt
from fastapi import APIRouter, HTTPException, Query

from ..config import get_settings

router = APIRouter()


@router.get("/oauth/callback")
async def oauth_callback(code: str = Query(...), state: Optional[str] = None):
    """
    Exchanges GitHub OAuth code for an access token and returns a signed session token.
    """
    settings = get_settings()
    client_id = settings.github_oauth_client_id
    client_secret = settings.github_oauth_client_secret
    if not client_id or not client_secret:
        raise HTTPException(status_code=500, detail="OAuth client is not configured")

    token_url = "https://github.com/login/oauth/access_token"
    async with httpx.AsyncClient() as client:
        res = await client.post(
            token_url,
            headers={"Accept": "application/json"},
            data={"client_id": client_id, "client_secret": client_secret, "code": code},
        )
        if res.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to exchange code")
        token_payload = res.json()
        access_token = token_payload.get("access_token")
        if not access_token:
            raise HTTPException(status_code=400, detail="No access token returned")

        user_res = await client.get(
            "https://api.github.com/user",
            headers={"Authorization": f"Bearer {access_token}", "Accept": "application/vnd.github+json"},
        )
        if user_res.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to fetch user")
        user = user_res.json()

    session_token = jwt.encode(
        {"login": user.get("login"), "id": user.get("id"), "token": access_token},
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )
    return {
        "login": user.get("login"),
        "name": user.get("name"),
        "avatar_url": user.get("avatar_url"),
        "session_token": session_token,
        "state": state,
    }
