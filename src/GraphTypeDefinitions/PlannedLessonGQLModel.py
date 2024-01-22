import strawberry
import datetime
from typing import List, Optional, Annotated
from .BaseGQLModel import BaseGQLModel
import uuid
from uoishelpers.resolvers import createInputs
from dataclasses import dataclass
from ._GraphResolvers import (
    resolve_id,
    resolve_name,
    resolve_name_en,
    resolve_changedby,
    resolve_created,
    resolve_lastchange,
    resolve_createdby,
    getLoadersFromInfo,
    asPage,
    IDType,
    encapsulateInsert,
    encapsulateUpdate,
    actinguserid
)

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
        return getLoadersFromInfo(info).plan_lessons
        
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
    async def type(self, info: strawberry.types.Info) -> Optional["AcLessonTypeGQLModel"]:
        from .AcLessonTypeGQLModel import AcLessonTypeGQLModel
        result = await AcLessonTypeGQLModel.resolve_reference(id=self.lessontype_id)
        return result

    @strawberry.field(
        description="""planned lesson linked to (aka master planned lesson)"""
    )
    async def linked_to(
        self, info: strawberry.types.Info
    ) -> Optional["PlannedLessonGQLModel"]:
        loader = PlannedLessonGQLModel.getLoader(info)
        result = None
        if self.linkedlesson_id is not None:
            result = await loader.load(self.linkedlesson_id)
        return result

    @strawberry.field(
        description="""planned lessons linked with, even trought master, excluding self"""
    )
    async def linked_with(
        self, info: strawberry.types.Info, including_self: Optional[bool] = False
    ) -> List["PlannedLessonGQLModel"]:
        loader = PlannedLessonGQLModel.getLoader(info)
        # result1 = await loader.load(self.id)
        result1 = [self]
        if self.linkedlesson_id is not None:
            result2 = await loader.filter_by(linkedlesson_id=self.id)
            result1 = [*result1, *result2]
        return result1

    @strawberry.field(description="""teachers""")
    async def users(self, info: strawberry.types.Info) -> List["UserGQLModel"]:
        from .UserGQLModel import UserGQLModel
        loader = getLoadersFromInfo(info).plan_lessons_users
        result = await loader.filter_by(planlesson_id=self.id)
        return [UserGQLModel(id=item.user_id) for item in result]

    @strawberry.field(description="""study groups""")
    async def groups(self, info: strawberry.types.Info) -> List["GroupGQLModel"]:
        from .GroupGQLModel import GroupGQLModel
        loader = getLoadersFromInfo(info).plan_lessons_groups
        result = await loader.filter_by(planlesson_id=self.id)
        return [GroupGQLModel(id=item.group_id) for item in result]

    @strawberry.field(description="""facilities""")
    async def facilities(
        self, info: strawberry.types.Info
    ) -> List["FacilityGQLModel"]:
        from .FacilityGQLModel import FacilityGQLModel
        loader = getLoadersFromInfo(info).plan_lessons_facilities
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

@createInputs
@dataclass    
class PlannedUserInputFilter:
    user_id: IDType

@createInputs
@dataclass    
class PlannedGroupInputFilter:
    group_id: IDType

@createInputs
@dataclass    
class PlannedFacilityInputFilter:
    facility_id: IDType

@createInputs
@dataclass
class PlannedLessonInputFilter:
    name: str
    plan_id: IDType
    semester_id: IDType
    topic_id: IDType
    linkedlesson_id: IDType
    # facilities: PlannedFacilityInputFilter
    # users: PlannedUserInputFilter
    # groups: PlannedGroupInputFilter

@strawberry.field(description="""Planned lesson by its id""")
async def planned_lesson_by_id(
    self, info: strawberry.types.Info, id: uuid.UUID
) -> Optional[PlannedLessonGQLModel]:
    return await PlannedLessonGQLModel.resolve_reference(info=info, id=id)

@strawberry.field(description="""Planned lesson paged""")
@asPage
async def planned_lesson_page(
    self, info: strawberry.types.Info, skip: int = 0, limit: int = 10, 
    where: Optional[PlannedLessonInputFilter] = None
) -> List[PlannedLessonGQLModel]:
    return PlannedLessonGQLModel.getLoader(info)

#########################################################
#
# Mutations
#
#########################################################

@strawberry.input
class PlannedLessonInsertGQLModel:
    name: str = strawberry.field(default=None, description="Name of lesson aka 'Introduction'")
    plan_id: uuid.UUID = strawberry.field(default=None, description="which plan contains this lesson")
    length: Optional[int] = strawberry.field(default=2, description="how many 45min intervals")
    startproposal: Optional[datetime.datetime] = strawberry.field(default=None, description="proposal of datetime")
    order: Optional[int] = strawberry.field(default=1, description="order of the item in plan")

    linkedlesson_id: Optional[uuid.UUID] =  strawberry.field(default=None, description="id of lesson from other plan which would be teached with")
    topic_id: Optional[uuid.UUID] = None
    lessontype_id: Optional[uuid.UUID] = strawberry.field(default=None, description="aka Consultation, Laboratory, ...")
    semester_id: Optional[uuid.UUID] = strawberry.field(default=None, description="link to semester (subject) from accreditation")
    event_id: Optional[uuid.UUID] = strawberry.field(default=None, description="event defining when this would be teached")
    id: Optional[uuid.UUID]  = strawberry.field(default=None, description="could be primary key generated by client, UUID is expected")

    createdby: strawberry.Private[IDType] = None
    rbacobject: strawberry.Private[IDType] = None

@strawberry.input
class PlannedLessonUpdateGQLModel:
    lastchange: datetime.datetime = strawberry.field(default=None, description="time stamp")
    id: uuid.UUID = strawberry.field(default=None, description="primary key value")
    order: Optional[int] = None
    name: Optional[str] = None
    length: Optional[int] = None
    startproposal: Optional[datetime.datetime] = None

    linkedlesson_id: Optional[uuid.UUID] = None
    topic_id: Optional[uuid.UUID] = None
    lessontype_id: Optional[uuid.UUID] = None
    semester_id: Optional[uuid.UUID] = None
    event_id: Optional[uuid.UUID] = None

    changedby: strawberry.Private[IDType] = None
    rbacobject: strawberry.Private[IDType] = None

@strawberry.input
class PlannedLessonDeleteGQLModel:
    lastchange: datetime.datetime
    id: uuid.UUID
    plan_id: Optional[uuid.UUID] = None

@strawberry.type
class PlannedLessonResultGQLModel:
    id: uuid.UUID = None
    msg: str = None

    @strawberry.field(description="""Result of lesson operation""")
    async def lesson(self, info: strawberry.types.Info) -> Optional[PlannedLessonGQLModel]:
        print("PlannedLessonResultGQLModel.lesson.id", self.id)
        result = await PlannedLessonGQLModel.resolve_reference(info, self.id)
        return result
    
@strawberry.input
class PlannedLessonUserInsertGQLModel:
    user_id: uuid.UUID
    planlesson_id: uuid.UUID
    id: Optional[IDType] = None
    createdby: strawberry.Private[IDType] = None
    rbacobject: strawberry.Private[IDType] = None
    
@strawberry.input
class PlannedLessonUserDeleteGQLModel:
    user_id: uuid.UUID
    planlesson_id: uuid.UUID

@strawberry.input
class PlannedLessonGroupInsertGQLModel:
    group_id: uuid.UUID
    planlesson_id: uuid.UUID
    id: Optional[IDType] = None
    createdby: strawberry.Private[IDType] = None
    rbacobject: strawberry.Private[IDType] = None
    
@strawberry.input
class PlannedLessonGroupDeleteGQLModel:
    group_id: uuid.UUID
    planlesson_id: uuid.UUID

@strawberry.input
class PlannedLessonFacilityInsertGQLModel:
    facility_id: uuid.UUID
    planlesson_id: uuid.UUID
    id: Optional[IDType] = None
    createdby: strawberry.Private[IDType] = None
    rbacobject: strawberry.Private[IDType] = None
    
@strawberry.input
class PlannedLessonFacilityDeleteGQLModel:
    facility_id: uuid.UUID
    planlesson_id: uuid.UUID

@strawberry.input
class PlannedLessonAssignmentGQLModel:
    lastchange: datetime.datetime
    id: uuid.UUID
    users: Optional[List[uuid.UUID]] = None
    facilities: Optional[List[uuid.UUID]] = None
    groups: Optional[List[uuid.UUID]] = None
    
@strawberry.type
class PlannedLessonAssignmentResultGQLModel:
    id: uuid.UUID = None
    msg: str = None

    @strawberry.field(description="""Result of user operation""")
    async def lesson(self, info: strawberry.types.Info) -> Optional[PlannedLessonGQLModel]:
        result = await PlannedLessonGQLModel.resolve_reference(info, self.id)
        return result
    

@strawberry.mutation(description="Assings a teacher to the planned lesson")
async def planned_lesson_user_insert(self, info: strawberry.types.Info, userlesson: PlannedLessonUserInsertGQLModel) -> PlannedLessonResultGQLModel:
    userlesson.createdby = actinguserid(info)
    loader = getLoadersFromInfo(info).plan_lessons_users
    rows = await loader.filter_by(planlesson_id=userlesson.planlesson_id, user_id=userlesson.user_id)
    exists = False
    rows = list(rows)
    exists = len(rows) > 0
    if not exists:
        row = await loader.insert(userlesson)
    result = PlannedLessonResultGQLModel()
    result.msg = "fail" if exists else "ok"
    result.id = userlesson.planlesson_id
    return result

@strawberry.mutation(description="Removes the teacher to the planned lesson")
async def planned_lesson_user_delete(self, info: strawberry.types.Info, userlesson: PlannedLessonUserDeleteGQLModel) -> PlannedLessonResultGQLModel:
    loader = getLoadersFromInfo(info).plan_lessons_users
    rows = await loader.filter_by(planlesson_id=userlesson.planlesson_id, user_id=userlesson.user_id)
    row = next(rows, None)
    result = PlannedLessonResultGQLModel()
    if row is None:
        result.msg = "fail"
    else:
        print(row)
        print(row.id)
        rr = await loader.delete(row.id)
        # for r in rr.all():
        #     print(r)
        result.msg = "ok"
    result.id = userlesson.planlesson_id
    print("planned_lesson_user_delete", userlesson.planlesson_id)
    return result

@strawberry.mutation(description="Assings a group to the planned lesson")
async def planned_lesson_group_insert(self, info: strawberry.types.Info, grouplesson: PlannedLessonGroupInsertGQLModel) -> PlannedLessonResultGQLModel:
    grouplesson.createdby = actinguserid(info)
    loader = getLoadersFromInfo(info).plan_lessons_groups
    rows = await loader.filter_by(planlesson_id=grouplesson.planlesson_id, group_id=grouplesson.group_id)
    rows = list(rows)
    exists = len(rows) > 0
    if not exists:
        row = await loader.insert(grouplesson)

    result = PlannedLessonResultGQLModel()
    result.msg = "fail" if exists else "ok"
    result.id = grouplesson.planlesson_id
    return result

@strawberry.mutation(description="Removes the group to the planned lesson")
async def planned_lesson_group_delete(self, info: strawberry.types.Info, grouplesson: PlannedLessonGroupDeleteGQLModel) -> PlannedLessonResultGQLModel:
    loader = getLoadersFromInfo(info).plan_lessons_groups
    rows = await loader.filter_by(planlesson_id=grouplesson.planlesson_id, group_id=grouplesson.group_id)
    row = next(rows, None)
    result = PlannedLessonResultGQLModel()
    if row is None:
        result.msg = "fail"
    else:
        await loader.delete(row.id)
        result.msg = "ok"
    result.id = grouplesson.planlesson_id
        
    return result

@strawberry.mutation(description="Assigns a facility to the planned lesson")
async def planned_lesson_facility_insert(self, info: strawberry.types.Info, facilitylesson: PlannedLessonFacilityInsertGQLModel) -> PlannedLessonResultGQLModel:
    facilitylesson.createdby = actinguserid(info)
    loader = getLoadersFromInfo(info).plan_lessons_facilities
    rows = await loader.filter_by(planlesson_id=facilitylesson.planlesson_id, facility_id=facilitylesson.facility_id)
    rows = list(rows)
    exists = len(rows) > 0
    if not exists:
        row = await loader.insert(facilitylesson)
    result = PlannedLessonResultGQLModel()
    result.msg = "fail" if exists else "ok"
    result.id = facilitylesson.planlesson_id
    return result

@strawberry.mutation(description="Removes the facility to the planned lesson")
async def planned_lesson_facility_delete(self, info: strawberry.types.Info, facilitylesson: PlannedLessonFacilityDeleteGQLModel) -> PlannedLessonResultGQLModel:
    loader = getLoadersFromInfo(info).plan_lessons_facilities
    rows = await loader.filter_by(planlesson_id=facilitylesson.planlesson_id, facility_id=facilitylesson.facility_id)
    row = next(rows, None)
    result = PlannedLessonResultGQLModel()
    if row is None:
        result.msg = "fail"
    else:
        await loader.delete(row.id)
        result.msg = "ok"
    result.id = facilitylesson.planlesson_id
    return result

@strawberry.mutation
async def planned_lesson_insert(self, info: strawberry.types.Info, lesson: PlannedLessonInsertGQLModel) -> PlannedLessonResultGQLModel:
    return await encapsulateInsert(info, PlannedLessonGQLModel.getLoader(info), lesson, PlannedLessonResultGQLModel(msg="ok", id=None))

@strawberry.mutation
async def planned_lesson_update(self, info: strawberry.types.Info, lesson: PlannedLessonUpdateGQLModel) -> PlannedLessonResultGQLModel:
    return await encapsulateUpdate(info, PlannedLessonGQLModel.getLoader(info), lesson, PlannedLessonResultGQLModel(msg="ok", id=None))

PlanResultGQLModel = Annotated["PlanResultGQLModel", ".PlanGQLModel"]
@strawberry.mutation
async def planned_lesson_remove(self, info: strawberry.types.Info, lesson: PlannedLessonDeleteGQLModel) -> Optional[PlanResultGQLModel]:
    loader = PlannedLessonGQLModel.getLoader(info)
    row = await loader.load(lesson.id)
    result = PlanResultGQLModel()
    if row:
        await loader.delete(lesson)
        result.msg = "ok"
        result.id = row.plan_id
    else:
        result.msg = "fail"
        result.id = row.plan_id
    return result