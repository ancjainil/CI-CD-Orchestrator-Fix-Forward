from typing import Dict

import httpx

from ..config import get_settings


class PrometheusClient:
    def __init__(self):
        self.settings = get_settings()
        self._client = httpx.AsyncClient(base_url=self.settings.prom_base_url)

    async def close(self):
        await self._client.aclose()

    async def query_slo(self, service: str) -> Dict:
        if self.settings.prom_mock:
            return {
                "service": service,
                "window": "30d",
                "latency_p95": 180,
                "error_rate": 0.0015,
                "burn_rate": 1.2,
                "budget_remaining": 0.73,
            }
        # Placeholder for real PromQL query
        return {
            "service": service,
            "window": "30d",
            "latency_p95": 200,
            "error_rate": 0.002,
            "burn_rate": 1.0,
            "budget_remaining": 0.7,
        }
