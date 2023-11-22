import strawberry
from typing import List, Optional, Annotated
import asyncio
import uuid

def getLoaders(info):
    return info.context['all']

PlannedLessonGQLModel = Annotated["PlannedLessonGQLModel", strawberry.lazy(".PlannedLessonGQLModel")]

@strawberry.federation.type(extend=True, keys=["id"])
class GroupGQLModel:

    id: uuid.UUID = strawberry.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: uuid.UUID):
        return cls(id=id)

    @strawberry.field(description="""planned items""")
    async def planned_lessons(self, info: strawberry.types.Info) -> List['PlannedLessonGQLModel']:
        from .PlannedLessonGQLModel import PlannedLessonGQLModel
        loader = getLoaders(info).groupplans
        rows = await loader.filter_by(group_id=self.id)
        rowids = (row.planlesson_id for row in rows)
        # rowids = list(rowids)
        # print(rowids)
        awaitables = (PlannedLessonGQLModel.resolve_reference(info, id) for id in rowids)
        results = await asyncio.gather(*awaitables)
        return results
