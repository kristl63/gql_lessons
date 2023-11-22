import strawberry
import datetime
from typing import List, Optional, Annotated
from .BaseGQLModel import BaseGQLModel
import uuid
def getLoaders(info):
    return info.context['all']

from ._GraphResolvers import (
    resolve_id,
    resolve_name,
    resolve_name_en,
    resolve_changedby,
    resolve_created,
    resolve_lastchange,
    resolve_createdby,

    createRootResolver_by_id,
    createRootResolver_by_page,
    createAttributeScalarResolver,
    createAttributeVectorResolver
)

UserGQLModel = Annotated["UserGQLModel", strawberry.lazy(".UserGQLModel")]
GroupGQLModel = Annotated["GroupGQLModel", strawberry.lazy(".GroupGQLModel")]
FacilityGQLModel = Annotated["FacilityGQLModel", strawberry.lazy(".FacilityGQLModel")]
EventGQLModel = Annotated["EventGQLModel", strawberry.lazy(".EventGQLModel")]
AcLessonTypeGQLModel = Annotated["AcLessonTypeGQLModel", strawberry.lazy(".AcLessonTypeGQLModel")]
AcTopicGQLModel = Annotated["AcTopicGQLModel", strawberry.lazy(".AcTopicGQLModel")]
AcSemesterGQLModel = Annotated["AcSemesterGQLModel", strawberry.lazy(".AcSemesterGQLModel")]
PlannedLessonGQLModel = Annotated["PlannedLessonGQLModel", strawberry.lazy(".PlannedLessonGQLModel")]

@strawberry.federation.type(
    keys=["id"],
    description="""Entity representing a study plan for timetable creation""",
)
class PlanGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoaders(info).psps

    id = resolve_id
    name = resolve_name
    changedby = resolve_changedby
    lastchange = resolve_lastchange
    created = resolve_created
    createdby = resolve_createdby

    
    @strawberry.field(description="""planned lessons""")
    async def lessons(self, info: strawberry.types.Info) -> List["PlannedLessonGQLModel"]:
        loader = getLoaders(info).plans
        result = await loader.filter_by(plan_id=self.id)
        return result
    
    @strawberry.field(description="""acredited semester""")
    async def semester(self, info: strawberry.types.Info) -> Optional["AcSemesterGQLModel"]:
        from .AcSemesterGQLModel import AcSemesterGQLModel
        result = await AcSemesterGQLModel.resolve_reference(id=self.semester_id)
        return result