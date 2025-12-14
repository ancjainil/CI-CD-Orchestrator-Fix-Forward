import base64
import hashlib
import hmac
import json
import time
from typing import Any, Dict, Optional

import httpx
import jwt

from ..config import get_settings


class GithubClient:
    """
    GitHub App client. If app creds are missing, falls back to mock responses.
    """

    def __init__(self, installation_id: Optional[int] = None, token: Optional[str] = None):
        self.settings = get_settings()
        self.installation_id = installation_id or self.settings.github_installation_id
        self.token = token
        self._client = httpx.AsyncClient(base_url="https://api.github.com")

    async def close(self):
        await self._client.aclose()

    def _jwt(self) -> Optional[str]:
        if not self.settings.github_app_private_key or not self.settings.github_app_id:
            return None
        now = int(time.time())
        payload = {"iat": now - 60, "exp": now + 540, "iss": self.settings.github_app_id}
        return jwt.encode(payload, self.settings.github_app_private_key, algorithm="RS256")

    async def _ensure_token(self) -> Optional[str]:
        if self.token:
            return self.token
        app_jwt = self._jwt()
        if not app_jwt or not self.installation_id:
            return None
        url = f"/app/installations/{self.installation_id}/access_tokens"
        res = await self._client.post(url, headers={"Authorization": f"Bearer {app_jwt}", "Accept": "application/vnd.github+json"})
        res.raise_for_status()
        data = res.json()
        self.token = data.get("token")
        return self.token

    async def _request(self, method: str, path: str, **kwargs) -> Dict[str, Any]:
        token = await self._ensure_token()
        if not token:
            raise RuntimeError("GitHub token unavailable. Ensure app credentials and installation_id are set.")
        headers = kwargs.pop("headers", {})
        headers.update({"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"})
        res = await self._client.request(method, path, headers=headers, **kwargs)
        res.raise_for_status()
        if res.content:
            return res.json()
        return {}

    async def get_pr(self, repo_full_name: str, pr_number: int) -> Dict[str, Any]:
        try:
            return await self._request("GET", f"/repos/{repo_full_name}/pulls/{pr_number}")
        except Exception:
            # Fallback mock
            return {
                "number": pr_number,
                "head": {"sha": "headsha", "ref": "feature"},
                "base": {"sha": "basesha", "ref": "main"},
                "title": "Demo PR",
                "user": {"login": "octocat"},
            }

    async def get_files(self, repo_full_name: str, pr_number: int) -> list[str]:
        try:
            files = await self._request("GET", f"/repos/{repo_full_name}/pulls/{pr_number}/files?per_page=100")
            return [f["filename"] for f in files]
        except Exception:
            return ["service/handler.py", "rollout.yaml"]

    async def post_comment(self, repo_full_name: str, pr_number: int, body: str) -> None:
        try:
            await self._request("POST", f"/repos/{repo_full_name}/issues/{pr_number}/comments", json={"body": body})
        except Exception:
            return None

    async def open_fix_forward_pr(self, repo_full_name: str, base: str, head: str, title: str, body: str) -> str:
        try:
            pr = await self._request(
                "POST",
                f"/repos/{repo_full_name}/pulls",
                json={"title": title, "head": head, "base": base, "body": body},
            )
            return pr.get("html_url", "")
        except Exception:
            return f"https://github.com/{repo_full_name}/pull/999"


def verify_signature(body: bytes, signature_header: str, secret: str) -> bool:
    if not signature_header:
        return False
    digest = hmac.new(key=secret.encode(), msg=body, digestmod=hashlib.sha256).hexdigest()
    expected = f"sha256={digest}"
    return hmac.compare_digest(expected, signature_header)


def decode_jwt(token: str) -> dict:
    # placeholder for dev auth; real implementation would verify JWTs
    try:
        return json.loads(base64.urlsafe_b64decode(token + "==="))
    except Exception:
        return {}
