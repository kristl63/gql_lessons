from typing import List, Union, Optional, Annotated
import typing
import asyncio
from unittest import result
import strawberry
import uuid
from contextlib import asynccontextmanager
import datetime

@asynccontextmanager
async def withInfo(info):
    asyncSessionMaker = info.context["asyncSessionMaker"]
    async with asyncSessionMaker() as session:
        try:
            yield session
        finally:
            pass

def asyncSessionMakerFromInfo(info):
    asyncSessionMaker = info.context["asyncSessionMaker"]
    return asyncSessionMaker

def AsyncSessionFromInfo(info):
    print(
        "obsolete function used AsyncSessionFromInfo, use withInfo context manager instead"
    )
    return info.context["session"]

def getLoaders(info):
    return info.context['all']
###########################################################################################################################
#
# zde definujte sve GQL modely
# - nove, kde mate zodpovednost
# - rozsirene, ktere existuji nekde jinde a vy jim pridavate dalsi atributy
#
###########################################################################################################################
#
# priklad rozsireni UserGQLModel
#

from .UserGQLModel import UserGQLModel
#UserGQLModel = Annotated["UserGQLModel", strawberry.lazy(".UserGQLModel")]
from .GroupGQLModel import GroupGQLModel
from .FacilityGQLModel import FacilityGQLModel
from .EventGQLModel import EventGQLModel
from .AcTopicGQLModel import AcTopicGQLModel
from .AcSemesterGQLModel import AcSemesterGQLModel
from .AcLessonTypeGQLModel import AcLessonTypeGQLModel

from .PlanGQLModel import PlanGQLModel
from .PlannedLessonGQLModel import PlannedLessonGQLModel


from gql_lessons.GraphResolvers import (
    resolvePlannedLessonById,
    resolvePlannedLessonPage,
    resolveUserLinksForPlannedLesson,
    resolveGroupLinksForPlannedLesson,
    resolveFacilityLinksForPlannedLesson,
    # resolveEventLinksForPlannedLesson,
    resolvePlannedLessonsByLink,
)

# @strawberry.federation.type(
#     keys=["id"],
#     description="""Entity representing a study plan for timetable creation""",
# )
# class PlanGQLModel:
#     @classmethod
#     async def resolve_reference(cls, info: strawberry.types.Info, id: uuid.UUID):
#         loader = getLoaders(info).psps
#         result = await loader.load(id)
#         if result is not None:
#             result._type_definition = cls._type_definition  # little hack :)
#         return result

#     @strawberry.field(description="""primary key""")
#     def id(self) -> uuid.UUID:
#         return self.id

#     @strawberry.field(description="""Timestap""")
#     def lastchange(self) -> datetime.datetime:
#         return self.lastchange
    
#     @strawberry.field(description="""planned lessons""")
#     async def lessons(self, info: strawberry.types.Info) -> List["PlannedLessonGQLModel"]:
#         loader = getLoaders(info).plans
#         result = await loader.filter_by(plan_id=self.id)
#         return result
    
#     @strawberry.field(description="""acredited semester""")
#     async def semester(self, info: strawberry.types.Info) -> Union["AcSemesterGQLModel", None]:
#         result = await AcSemesterGQLModel.resolve_reference(id=self.semester_id)
#         return result
    
# @strawberry.federation.type(
#     keys=["id"],
#     description="""Entity representing a planned lesson for timetable creation""",
# )
# class PlannedLessonGQLModel:
#     @classmethod
#     async def resolve_reference(cls, info: strawberry.types.Info, id: uuid.UUID):
#         # print("PlannedLessonGQLModel.resolve_reference", id)
#         loader = getLoaders(info).plans
#         result = await loader.load(id)
#         if result is not None:
#             result._type_definition = cls._type_definition  # little hack :)
#         return result

#     @strawberry.field(description="""primary key""")
#     def id(self) -> uuid.UUID:
#         return self.id

#     @strawberry.field(description="""Timestap""")
#     def lastchange(self) -> datetime.datetime:
#         return self.lastchange

#     @strawberry.field(description="""primary key""")
#     def name(self) -> str:
#         return self.name

#     @strawberry.field(description="""order""")
#     def order(self) -> int:
#         return self.order

#     @strawberry.field(description="""primary key""")
#     def length(self) -> Union[int, None]:
#         return self.length

#     @strawberry.field(description="""type of lesson (lecture, ...)""")
#     async def type(self, info) -> Optional["AcLessonTypeGQLModel"]:
#         result = await AcLessonTypeGQLModel.resolve_reference(id=self.lessontype_id)
#         return result

#     @strawberry.field(
#         description="""planned lesson linked to (aka master planned lesson)"""
#     )
#     async def linked_to(
#         self, info: strawberry.types.Info
#     ) -> Union["PlannedLessonGQLModel", None]:
#         loader = getLoaders(info).plans
#         result = None
#         if self.linkedlesson_id is not None:
#             result = await loader.load(self.linkedlesson_id)
#         return result

#     @strawberry.field(
#         description="""planned lessons linked with, even trought master, excluding self"""
#     )
#     async def linked_with(
#         self, info: strawberry.types.Info
#     ) -> List["PlannedLessonGQLModel"]:
#         loader = getLoaders(info).plans
#         result1 = await loader.load(self.id)
#         if self.linkedlesson_id is not None:
#             result2 = await loader.filter_by(linkedlesson_id=self.id)
#             result1 = [result1, *result2]
#         return result1

#     @strawberry.field(description="""teachers""")
#     async def users(self, info: strawberry.types.Info) -> List["UserGQLModel"]:
#         loader = getLoaders(info).userplans
#         result = await loader.filter_by(planlesson_id=self.id)
#         return [UserGQLModel(id=item.user_id) for item in result]

#     @strawberry.field(description="""study groups""")
#     async def groups(self, info: strawberry.types.Info) -> List["GroupGQLModel"]:
#         loader = getLoaders(info).groupplans
#         result = await loader.filter_by(planlesson_id=self.id)
#         return [GroupGQLModel(id=item.group_id) for item in result]

#     @strawberry.field(description="""facilities""")
#     async def facilities(
#         self, info: strawberry.types.Info
#     ) -> List["FacilityGQLModel"]:
#         loader = getLoaders(info).facilityplans
#         result = await loader.filter_by(planlesson_id=self.id)
#         return [FacilityGQLModel(id=item.facility_id) for item in result]

#     @strawberry.field(description="""linked event""")
#     async def event(self, info: strawberry.types.Info) -> Union["EventGQLModel", None]:
#         if self.event_id is None:
#             result = None
#         else:
#             result = EventGQLModel(id=self.event_id)
#         return result

#     @strawberry.field(description="""linked topic from accreditation""")
#     async def topic(
#         self, info: strawberry.types.Info
#     ) -> Union["AcTopicGQLModel", None]:
#         if self.topic_id is None:
#             result = None
#         else:
#             result = AcTopicGQLModel(id=self.topic_id)
#         return result

#     @strawberry.field(
#         description="""linked subject semester from program (accreditation)"""
#     )
#     async def semester(
#         self, info: strawberry.types.Info
#     ) -> Union["AcSemesterGQLModel", None]:
#         if self.semester_id is None:
#             result = None
#         else:
#             result = AcSemesterGQLModel(id=self.semester_id)
#         return result

#     @strawberry.field(
#         description="""linked subject semester from program (accreditation)"""
#     )
#     async def plan(
#         self, info: strawberry.types.Info
#     ) -> Union["PlanGQLModel", None]:
#         print("PlannedLessonGQLModel.plan", self.plan_id)
#         result = await PlanGQLModel.resolve_reference(info, self.plan_id)
#         print("PlannedLessonGQLModel.plan", result)
#         return result

###########################################################################################################################
#
# zde definujte svuj Query model
#
###########################################################################################################################
from gql_lessons.GraphResolvers import (
    resolvePlannedLessonBySemester,
    resolvePlannedLessonByTopic,
    resolvePlannedLessonByEvent,
)


@strawberry.type(description="""Type for query root""")
class Query:
    @strawberry.field(description="""just a check""")
    async def say_hello(
        self, info: strawberry.types.Info, id: uuid.UUID
    ) -> Union[str, None]:
        result = f"Hello {id}"
        return result

    @strawberry.field(description="""Planned lesson by its id""")
    async def plan_by_id(
        self, info: strawberry.types.Info, id: uuid.UUID
    ) -> Union[PlanGQLModel, None]:
        result = await PlanGQLModel.resolve_reference(info, id)
        return result

    @strawberry.field(description="""Planned lesson paged""")
    async def plan_page(
        self, info: strawberry.types.Info, skip: int = 0, limit: int = 10
    ) -> List[PlanGQLModel]:
        loader = getLoaders(info).psps
        result = await loader.page(skip, limit)
        return result

    @strawberry.field(description="""Planned lesson by its id""")
    async def planned_lesson_by_id(
        self, info: strawberry.types.Info, id: uuid.UUID
    ) -> Union[PlannedLessonGQLModel, None]:
        async with withInfo(info) as session:
            result = await resolvePlannedLessonById(session, id)
            return result

    @strawberry.field(description="""Planned lesson paged""")
    async def planned_lesson_page(
        self, info: strawberry.types.Info, skip: int = 0, limit: int = 10
    ) -> List[PlannedLessonGQLModel]:
        async with withInfo(info) as session:
            result = await resolvePlannedLessonPage(session, skip, limit)
            return result

    @strawberry.field(description="""Planned lesson by its semester (subject)""")
    async def planned_lessons_by_semester(
        self, info: strawberry.types.Info, id: uuid.UUID
    ) -> List[PlannedLessonGQLModel]:
        async with withInfo(info) as session:
            result = await resolvePlannedLessonBySemester(session, id)
            return result

    @strawberry.field(description="""Planned lesson by its topic""")
    async def planned_lessons_by_topic(
        self, info: strawberry.types.Info, id: uuid.UUID
    ) -> List[PlannedLessonGQLModel]:
        async with withInfo(info) as session:
            result = await resolvePlannedLessonByTopic(session, id)
            return result

    @strawberry.field(description="""Planned lesson """)
    async def planned_lessons_by_event(
        self, info: strawberry.types.Info, id: uuid.UUID
    ) -> List[PlannedLessonGQLModel]:
        async with withInfo(info) as session:
            result = await resolvePlannedLessonByEvent(session, id)
            return result


###########################################################################################################################
#
#
# Mutations
#
#
###########################################################################################################################

from typing import Optional

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

@strawberry.input
class PlannedLessonDeleteGQLModel:
    lastchange: datetime.datetime
    id: uuid.UUID
    plan_id: Optional[uuid.UUID] = None

@strawberry.type
class PlannedLessonResultGQLModel:
    id: Union[uuid.UUID, None] = None
    msg: str = None

    @strawberry.field(description="""Result of lesson operation""")
    async def lesson(self, info: strawberry.types.Info) -> Union[PlannedLessonGQLModel, None]:
        print("lesson", self.id)
        result = await PlannedLessonGQLModel.resolve_reference(info, self.id)
        return result
    
@strawberry.type
class PlanResultGQLModel:
    id: Union[uuid.UUID, None] = None
    msg: str = None

    @strawberry.field(description="""Result of lesson operation""")
    async def plan(self, info: strawberry.types.Info) -> Union[PlanGQLModel, None]:
        result = await PlanGQLModel.resolve_reference(info, self.id)
        return result
    
@strawberry.input
class PlannedLessonUserInsertGQLModel:
    user_id: uuid.UUID
    planlesson_id: uuid.UUID
    
@strawberry.input
class PlannedLessonUserDeleteGQLModel:
    user_id: uuid.UUID
    planlesson_id: uuid.UUID

@strawberry.input
class PlannedLessonGroupInsertGQLModel:
    group_id: uuid.UUID
    planlesson_id: uuid.UUID
    
@strawberry.input
class PlannedLessonGroupDeleteGQLModel:
    group_id: uuid.UUID
    planlesson_id: uuid.UUID

@strawberry.input
class PlannedLessonFacilityInsertGQLModel:
    facility_id: uuid.UUID
    planlesson_id: uuid.UUID
    
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
    async def lesson(self, info: strawberry.types.Info) -> Union[PlannedLessonGQLModel, None]:
        result = await PlannedLessonGQLModel.resolve_reference(info, self.id)
        return result

from gql_lessons.GraphResolvers import resolveRemovePlan
@strawberry.federation.type(extend=True)
class Mutation:
    # @strawberry.mutation
    # async def planned_lesson_change_assignment(self, info: strawberry.types.Info, assignment: PlannedLessonAssignmentGQLModel) -> PlannedLessonAssignmentResultGQLModel:
    #     # loader = getLoaders(info).plans
    #     # row = await loader.insert(lesson)
    #     if assignment.users is not None:
    #         loader = getLoaders(info).userplans
    #         rows = await loader.filter_by(planlesson_id=assignment.id)
    #         rowids = set(list(map(lambda item: item.id, rows)))
    #         inputids = set(assignment.users)
    #         toAdd = inputids - rowids
    #         toRemove = rowids - inputids


    #     result = PlannedLessonResultGQLModel()
    #     result.msg = "not implemented"
    #     result.id = None
    #     return result

    @strawberry.mutation(description="Assings a teacher to the planned lesson")
    async def planned_lesson_user_insert(self, info: strawberry.types.Info, userlesson: PlannedLessonUserInsertGQLModel) -> PlannedLessonResultGQLModel:
        loader = getLoaders(info).userplans
        row = await loader.insert(userlesson)
        result = PlannedLessonResultGQLModel()
        result.msg = "ok"
        result.id = userlesson.planlesson_id
        return result

    @strawberry.mutation(description="Removes the teacher to the planned lesson")
    async def planned_lesson_user_delete(self, info: strawberry.types.Info, userlesson: PlannedLessonUserDeleteGQLModel) -> PlannedLessonResultGQLModel:
        loader = getLoaders(info).userplans
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
        loader = getLoaders(info).groupplans
        row = await loader.insert(grouplesson)
        result = PlannedLessonResultGQLModel()
        result.msg = "ok"
        result.id = row.planlesson_id
        return result

    @strawberry.mutation(description="Removes the group to the planned lesson")
    async def planned_lesson_group_delete(self, info: strawberry.types.Info, grouplesson: PlannedLessonGroupDeleteGQLModel) -> PlannedLessonResultGQLModel:
        loader = getLoaders(info).groupplans
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
        loader = getLoaders(info).facilityplans
        row = await loader.insert(facilitylesson)
        result = PlannedLessonResultGQLModel()
        result.msg = "ok"
        result.id = row.planlesson_id
        return result

    @strawberry.mutation(description="Removes the facility to the planned lesson")
    async def planned_lesson_facility_delete(self, info: strawberry.types.Info, facilitylesson: PlannedLessonFacilityDeleteGQLModel) -> PlannedLessonResultGQLModel:
        resolveRemovePlan
        loader = getLoaders(info).facilityplans
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
        loader = getLoaders(info).plans
        row = await loader.insert(lesson)
        result = PlannedLessonResultGQLModel()
        result.msg = "ok"
        result.id = row.id
        return result

    @strawberry.mutation
    async def planned_lesson_update(self, info: strawberry.types.Info, lesson: PlannedLessonUpdateGQLModel) -> PlannedLessonResultGQLModel:
        resolveRemovePlan
        loader = getLoaders(info).plans
        row = await loader.update(lesson)
        result = PlannedLessonResultGQLModel()
        result.msg = "ok"
        result.id = lesson.id
        if row is None:
            result.msg = "fail"
            
        return result
    
    @strawberry.mutation
    async def planned_lesson_remove(self, info: strawberry.types.Info, lesson: PlannedLessonDeleteGQLModel) -> PlanResultGQLModel:
        asyncSessionMaker = asyncSessionMakerFromInfo(info)
        await resolveRemovePlan(asyncSessionMaker, lesson.id)
        result = PlanResultGQLModel()
        result.msg = "ok"
        result.id = lesson.plan_id
            
        return result
    
###########################################################################################################################
#
# Schema je pouzito v main.py, vsimnete si parametru types, obsahuje vyjmenovane modely. Bez explicitniho vyjmenovani
# se ve schema objevi jen ty struktury, ktere si strawberry dokaze odvodit z Query. Protoze v teto konkretni implementaci
# nektere modely nejsou s Query propojene je potreba je explicitne vyjmenovat. Jinak ve federativnim schematu nebude
# dostupne rozsireni, ktere tento prvek federace implementuje.
#
###########################################################################################################################

schema = strawberry.federation.Schema(Query, mutation=Mutation)
