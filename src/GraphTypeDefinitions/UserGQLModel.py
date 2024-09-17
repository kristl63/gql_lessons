import strawberry
import typing
import asyncio
import uuid
from typing import Annotated, List

from src.Dataloaders import getLoadersFromInfo
PlannedLessonGQLModel = Annotated["PlannedLessonGQLModel", strawberry.lazy(".PlannedLessonGQLModel")]

@strawberry.federation.type(extend=True, keys=["id"])
class UserGQLModel:

    id: uuid.UUID = strawberry.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: uuid.UUID):
        return cls(id=id)  # jestlize rozsirujete, musi byt tento vyraz


#     zde je rozsireni o dalsi resolvery
#     @strawberry.field(description="""Inner id""")
#     async def external_ids(self, info: strawberry.types.Info) -> List['ExternalIdGQLModel']:
#         result = await resolveExternalIds(session,  self.id)
#         return result

    @strawberry.field(description="""planned items""")
    async def planned_lessons(self, info: strawberry.types.Info) -> typing.List['PlannedLessonGQLModel']:
        from .PlannedLessonGQLModel import PlannedLessonGQLModel
        # loader = PlannedLessonGQLModel.getLoader(info)
        loader = getLoadersFromInfo(info).plan_lessons_users
        rows = await loader.filter_by(user_id=self.id)
        rowids = (row.planlesson_id for row in rows)
        # rowids = list(rowids)
        # print(rowids)
        awaitables = (PlannedLessonGQLModel.resolve_reference(info, id) for id in rowids)
        results = await asyncio.gather(*awaitables)
        return filter(lambda item: item is not None, results)