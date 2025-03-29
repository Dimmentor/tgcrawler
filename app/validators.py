from typing import Any
from pydantic import BaseModel, HttpUrl, ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import Source


class SourceCheck(BaseModel):
    title: str
    url: HttpUrl
    xpath: str


async def validate_source_data(title: str, url: str, xpath: str) -> Any:
    try:
        SourceCheck(title=title, url=url, xpath=xpath)
        return None
    except ValidationError as e:
        return str(e)


async def check_entry(session: AsyncSession, title: str, url: str, xpath: str) -> bool:
    query = select(Source).where(
        (Source.title == title) |
        (Source.url == url) |
        (Source.xpath == xpath)
    )
    result = await session.execute(query)
    existing_sources = result.scalars().all()
    return len(existing_sources) > 0
