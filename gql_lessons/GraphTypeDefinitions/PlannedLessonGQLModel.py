import strawberry
import datetime
from typing import List, Optional, Annotated
from .BaseGQLModel import BaseGQLModel
import uuid
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

def getLoaders(info):
    return info.context['all']

UserGQLModel = Annotated["UserGQLModel", strawberry.lazy(".UserGQLModel")]
GroupGQLModel = Annotated["GroupGQLModel", strawberry.lazy(".GroupGQLModel")]
FacilityGQLModel = Annotated["FacilityGQLModel", strawberry.lazy(".FacilityGQLModel")]
EventGQLModel = Annotated["EventGQLModel", strawberry.lazy(".EventGQLModel")]
AcLessonTypeGQLModel = Annotated["AcLessonTypeGQLModel", strawberry.lazy(".AcLessonTypeGQLModel")]
AcTopicGQLModel = Annotated["AcTopicGQLModel", strawberry.lazy(".AcTopicGQLModel")]
AcSemesterGQLModel = Annotated["AcSemesterGQLModel", strawberry.lazy(".AcSemesterGQLModel")]
PlanGQLModel = Annotated["PlanGQLModel", strawberry.lazy(".PlanGQLModel")]


@strawberry.federation.type(
    keys=["id"],
    description="""Entity representing a planned lesson for timetable creation""",
)
class PlannedLessonGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoaders(info).plans
        
    id = resolve_id
    name = resolve_name
    changedby = resolve_changedby
    lastchange = resolve_lastchange
    created = resolve_created
    createdby = resolve_createdby

    @strawberry.field(description="""order""")
    def order(self) -> int:
        return self.order

    @strawberry.field(description="""primary key""")
    def length(self) -> Optional[int]:
        return self.length

    @strawberry.field(description="""type of lesson (lecture, ...)""")
    async def type(self, info) -> Optional["AcLessonTypeGQLModel"]:
        from .AcLessonTypeGQLModel import AcLessonTypeGQLModel
        result = await AcLessonTypeGQLModel.resolve_reference(id=self.lessontype_id)
        return result

    @strawberry.field(
        description="""planned lesson linked to (aka master planned lesson)"""
    )
    async def linked_to(
        self, info: strawberry.types.Info
    ) -> Optional["PlannedLessonGQLModel"]:
        loader = getLoaders(info).plans
        result = None
        if self.linkedlesson_id is not None:
            result = await loader.load(self.linkedlesson_id)
        return result

    @strawberry.field(
        description="""planned lessons linked with, even trought master, excluding self"""
    )
    async def linked_with(
        self, info: strawberry.types.Info
    ) -> List["PlannedLessonGQLModel"]:
        loader = getLoaders(info).plans
        result1 = await loader.load(self.id)
        if self.linkedlesson_id is not None:
            result2 = await loader.filter_by(linkedlesson_id=self.id)
            result1 = [result1, *result2]
        return result1

    @strawberry.field(description="""teachers""")
    async def users(self, info: strawberry.types.Info) -> List["UserGQLModel"]:
        from .UserGQLModel import UserGQLModel
        loader = getLoaders(info).userplans
        result = await loader.filter_by(planlesson_id=self.id)
        return [UserGQLModel(id=item.user_id) for item in result]

    @strawberry.field(description="""study groups""")
    async def groups(self, info: strawberry.types.Info) -> List["GroupGQLModel"]:
        from .GroupGQLModel import GroupGQLModel
        loader = getLoaders(info).groupplans
        result = await loader.filter_by(planlesson_id=self.id)
        return [GroupGQLModel(id=item.group_id) for item in result]

    @strawberry.field(description="""facilities""")
    async def facilities(
        self, info: strawberry.types.Info
    ) -> List["FacilityGQLModel"]:
        from .FacilityGQLModel import FacilityGQLModel
        loader = getLoaders(info).facilityplans
        result = await loader.filter_by(planlesson_id=self.id)
        return [FacilityGQLModel(id=item.facility_id) for item in result]

    @strawberry.field(description="""linked event""")
    async def event(self, info: strawberry.types.Info) -> Optional["EventGQLModel"]:
        from .EventGQLModel import EventGQLModel
        if self.event_id is None:
            result = None
        else:
            result = EventGQLModel(id=self.event_id)
        return result

    @strawberry.field(description="""linked topic from accreditation""")
    async def topic(
        self, info: strawberry.types.Info
    ) -> Optional["AcTopicGQLModel"]:
        from .AcTopicGQLModel import AcTopicGQLModel
        if self.topic_id is None:
            result = None
        else:
            result = AcTopicGQLModel(id=self.topic_id)
        return result

    @strawberry.field(
        description="""linked subject semester from program (accreditation)"""
    )
    async def semester(
        self, info: strawberry.types.Info
    ) -> Optional["AcSemesterGQLModel"]:
        from .AcSemesterGQLModel import AcSemesterGQLModel
        if self.semester_id is None:
            result = None
        else:
            result = AcSemesterGQLModel(id=self.semester_id)
        return result

    @strawberry.field(
        description="""linked subject semester from program (accreditation)"""
    )
    async def plan(
        self, info: strawberry.types.Info
    ) -> Optional["PlanGQLModel"]:
        from .PlanGQLModel import PlanGQLModel
        print("PlannedLessonGQLModel.plan", self.plan_id)
        result = await PlanGQLModel.resolve_reference(info, self.plan_id)
        print("PlannedLessonGQLModel.plan", result)
        return result