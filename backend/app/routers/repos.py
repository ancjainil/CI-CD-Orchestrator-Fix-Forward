from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import get_session
from ..models import Repo
from ..schemas import RepoOut

router = APIRouter(prefix="/repos", tags=["repos"])


@router.get("/", response_model=list[RepoOut])
async def list_repos(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Repo))
    return result.scalars().all()
