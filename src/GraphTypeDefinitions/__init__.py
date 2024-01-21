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

def getLoadersFromInfo(info):
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


from src.GraphResolvers import (
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
#         loader = getLoadersFromInfo(info).psps
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
#         loader = getLoadersFromInfo(info).plans
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
#         loader = getLoadersFromInfo(info).plans
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
#         loader = getLoadersFromInfo(info).plans
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
#         loader = getLoadersFromInfo(info).plans
#         result1 = await loader.load(self.id)
#         if self.linkedlesson_id is not None:
#             result2 = await loader.filter_by(linkedlesson_id=self.id)
#             result1 = [result1, *result2]
#         return result1

#     @strawberry.field(description="""teachers""")
#     async def users(self, info: strawberry.types.Info) -> List["UserGQLModel"]:
#         loader = getLoadersFromInfo(info).userplans
#         result = await loader.filter_by(planlesson_id=self.id)
#         return [UserGQLModel(id=item.user_id) for item in result]

#     @strawberry.field(description="""study groups""")
#     async def groups(self, info: strawberry.types.Info) -> List["GroupGQLModel"]:
#         loader = getLoadersFromInfo(info).groupplans
#         result = await loader.filter_by(planlesson_id=self.id)
#         return [GroupGQLModel(id=item.group_id) for item in result]

#     @strawberry.field(description="""facilities""")
#     async def facilities(
#         self, info: strawberry.types.Info
#     ) -> List["FacilityGQLModel"]:
#         loader = getLoadersFromInfo(info).facilityplans
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
from src.GraphResolvers import (
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

    from .PlanGQLModel import (
        plan_by_id,
        plan_page
    )
    plan_by_id = plan_by_id
    plan_page = plan_page

    from .PlannedLessonGQLModel import (
        planned_lesson_by_id,
        planned_lesson_page
    )
    planned_lesson_by_id = planned_lesson_by_id
    planned_lesson_page = planned_lesson_page


###########################################################################################################################
#
#
# Mutations
#
#
###########################################################################################################################

from typing import Optional



from src.GraphResolvers import resolveRemovePlan
@strawberry.federation.type(extend=True)
class Mutation:
    # @strawberry.mutation
    # async def planned_lesson_change_assignment(self, info: strawberry.types.Info, assignment: PlannedLessonAssignmentGQLModel) -> PlannedLessonAssignmentResultGQLModel:
    #     # loader = getLoadersFromInfo(info).plans
    #     # row = await loader.insert(lesson)
    #     if assignment.users is not None:
    #         loader = getLoadersFromInfo(info).userplans
    #         rows = await loader.filter_by(planlesson_id=assignment.id)
    #         rowids = set(list(map(lambda item: item.id, rows)))
    #         inputids = set(assignment.users)
    #         toAdd = inputids - rowids
    #         toRemove = rowids - inputids


    #     result = PlannedLessonResultGQLModel()
    #     result.msg = "not implemented"
    #     result.id = None
    #     return result

    from .PlanGQLModel import (
        plan_insert, plan_update
    )
    plan_insert = plan_insert
    plan_update = plan_update

    from .PlannedLessonGQLModel import (
        planned_lesson_facility_delete,
        planned_lesson_facility_insert,
        planned_lesson_group_delete,
        planned_lesson_group_insert,
        planned_lesson_user_delete,
        planned_lesson_user_insert
    )
    planned_lesson_facility_delete = planned_lesson_facility_delete
    planned_lesson_facility_insert = planned_lesson_facility_insert
    planned_lesson_group_delete = planned_lesson_group_delete
    planned_lesson_group_insert = planned_lesson_group_insert
    planned_lesson_user_delete = planned_lesson_user_delete
    planned_lesson_user_insert = planned_lesson_user_insert
    
###########################################################################################################################
#
# Schema je pouzito v main.py, vsimnete si parametru types, obsahuje vyjmenovane modely. Bez explicitniho vyjmenovani
# se ve schema objevi jen ty struktury, ktere si strawberry dokaze odvodit z Query. Protoze v teto konkretni implementaci
# nektere modely nejsou s Query propojene je potreba je explicitne vyjmenovat. Jinak ve federativnim schematu nebude
# dostupne rozsireni, ktere tento prvek federace implementuje.
#
###########################################################################################################################

schema = strawberry.federation.Schema(Query, mutation=Mutation)
