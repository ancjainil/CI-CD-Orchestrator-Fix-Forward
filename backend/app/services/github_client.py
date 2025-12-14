import base64
import hashlib
import hmac
import json
from typing import Any, Dict, Optional

import httpx

from ..config import get_settings


class GithubClient:
    def __init__(self, token: Optional[str] = None):
        self.settings = get_settings()
        self.token = token
        self._client = httpx.AsyncClient(base_url="https://api.github.com")

    async def close(self):
        await self._client.aclose()

    async def get_pr(self, repo_full_name: str, pr_number: int) -> Dict[str, Any]:
        return {
            "number": pr_number,
            "head": {"sha": "headsha", "ref": "feature"},
            "base": {"sha": "basesha", "ref": "main"},
            "title": "Demo PR",
            "user": {"login": "octocat"},
        }

    async def get_files(self, repo_full_name: str, pr_number: int) -> list[str]:
        return ["service/handler.py", "rollout.yaml"]

    async def post_comment(self, repo_full_name: str, pr_number: int, body: str) -> None:
        # Stubbed comment call
        return None

    async def open_fix_forward_pr(self, repo_full_name: str, base: str, head: str, title: str, body: str) -> str:
        # Return fake URL
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
