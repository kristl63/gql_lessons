import strawberry
import typing
import asyncio
import uuid
from typing import Annotated, List

from src.Dataloaders import getLoadersFromInfo

PlannedLessonGQLModel = Annotated["PlannedLessonGQLModel", strawberry.lazy(".PlannedLessonGQLModel")]

@strawberry.federation.type(extend=True, keys=["id"])
class EventGQLModel:

    id: uuid.UUID = strawberry.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: uuid.UUID):
        return cls(id=id)