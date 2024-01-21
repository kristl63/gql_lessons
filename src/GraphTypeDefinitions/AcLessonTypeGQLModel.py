import strawberry
import typing
import asyncio
import uuid
from typing import Annotated, List

def getLoadersFromInfo(info):
    return info.context['all']

PlannedLessonGQLModel = Annotated["PlannedLessonGQLModel", strawberry.lazy(".PlannedLessonGQLModel")]
PlanGQLModel = Annotated["PlanGQLModel", strawberry.lazy(".PlanGQLModel")]

@strawberry.federation.type(extend=True, keys=["id"])
class AcLessonTypeGQLModel:

    id: uuid.UUID = strawberry.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: uuid.UUID):
        return AcLessonTypeGQLModel(id=id)