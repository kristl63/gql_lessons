import strawberry
import datetime
from typing import List, Optional, Annotated, Union
from .BaseGQLModel import BaseGQLModel
import uuid
from dataclasses import dataclass
from uoishelpers.resolvers import createInputs
import typing

from ._GraphResolvers import (
    resolve_id,
    resolve_name,
    resolve_name_en,
    resolve_changedby,
    resolve_created,
    resolve_lastchange,
    resolve_createdby,
)

from ._GraphPermissions import (
    OnlyForAuthentized
)
from ._GraphResolvers import (
    IDType,
    getLoadersFromInfo,
    resolve_reference,
    resolve_id,
    resolve_name,
    resolve_name_en,
    resolve_lastchange,
    resolve_created,
    resolve_createdby,
    resolve_changedby,
    resolve_rbacobject,

    encapsulateInsert,
    encapsulateUpdate,

    asPage
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
        return getLoadersFromInfo(info).plans

    id = resolve_id
    name = resolve_name
    changedby = resolve_changedby
    lastchange = resolve_lastchange
    created = resolve_created
    createdby = resolve_createdby
    
    rbac_object = resolve_rbacobject
    
    @strawberry.field(description="""planned lessons""")
    async def lessons(self, info: strawberry.types.Info) -> List["PlannedLessonGQLModel"]:
        from .PlannedLessonGQLModel import PlannedLessonGQLModel
        loader = PlannedLessonGQLModel.getLoader(info)
        result = await loader.filter_by(plan_id=self.id)
        return result
    
    @strawberry.field(description="""acredited semester""")
    async def semester(self, info: strawberry.types.Info) -> Optional["AcSemesterGQLModel"]:
        from .AcSemesterGQLModel import AcSemesterGQLModel
        result = await AcSemesterGQLModel.resolve_reference(id=self.semester_id)
        return result

@createInputs
@dataclass
class PlanInputFilter:
    name: str
    masterevent_id: IDType

@strawberry.field(description="""Planned lesson by its id""")
async def plan_by_id(
    self, info: strawberry.types.Info, id: uuid.UUID
) -> Optional[PlanGQLModel]:
    result = await PlanGQLModel.resolve_reference(info, id)
    return result

@strawberry.field(description="""Planned lesson paged""")
@asPage
async def plan_page(
    self, info: strawberry.types.Info, skip: int = 0, limit: int = 10, 
    where: Optional[PlanInputFilter] = None
) -> List[PlanGQLModel]:
    return PlanGQLModel.getLoader(info)

@strawberry.input(description="")
class PlanInsertGQLModel:
    semester_id: IDType
    masterevent_id: IDType
    id: Optional[IDType] = None
    name: Optional[str] = "Nový plán"
    pass

@strawberry.input(description="")
class PlanUpdateGQLModel:
    id: IDType
    lastchange: datetime.datetime
    name: Optional[str]
    pass

@strawberry.input(description="")
class PlanDeleteGQLModel:
    id: IDType
    lastchange: datetime.datetime
    pass

@strawberry.type(description="")
class PlanResultGQLModel:
    id: uuid.UUID = None
    msg: str = None

    @strawberry.field(description="""Result of lesson operation""")
    async def plan(self, info: strawberry.types.Info) -> Optional[PlanGQLModel]:
        result = await PlanGQLModel.resolve_reference(info, self.id)
        return result
    
@strawberry.mutation(description="""Plan insert""")
async def plan_insert(self, info: strawberry.types.Info, plan: PlanInsertGQLModel) -> PlanResultGQLModel:
    return await encapsulateInsert(info, PlanGQLModel.getLoader(info), plan, PlanResultGQLModel(msg="ok", id=None))

@strawberry.mutation(description="""Plan update""")
async def plan_update(self, info: strawberry.types.Info, plan: PlanUpdateGQLModel) -> PlanResultGQLModel:
    return await encapsulateUpdate(info, PlanGQLModel.getLoader(info), plan, PlanResultGQLModel(msg="ok", id=plan.id))

# @strawberry.mutation(description="""Plan delete""")
# async def plan_delete(self, info: strawberry.types.Info, plan: PlanDeleteGQLModel) -> PlanResultGQLModel:
#     loader = PlanGQLModel.getLoader(info)
#     result = await loader.delete(plan.id)
#     return PlanResultGQLModel(id=plan.id, msg="ok")

from uoishelpers.resolvers import Insert, InsertError, Update, UpdateError
@strawberry.mutation(description="""Plan insert""")
async def plan_insert(self, info: strawberry.types.Info, plan: PlanInsertGQLModel) -> Union[PlanGQLModel, InsertError[PlanGQLModel]]:
    result = await Insert[PlanGQLModel].DoItSafeWay(info=info, entity=plan)
    return result

@strawberry.mutation(description="""Plan update""")
async def plan_update(self, info: strawberry.types.Info, plan: PlanUpdateGQLModel) -> Union[PlanGQLModel, UpdateError[PlanGQLModel]]:
    result = await Update[PlanGQLModel].DoItSafeWay(info=info, entity=plan)
    return result

from uoishelpers.resolvers import Delete, DeleteError
@strawberry.mutation(description="""Plan delete""")
async def plan_delete(self, info: strawberry.types.Info, id: PlanDeleteGQLModel) -> typing.Optional[DeleteError[PlanGQLModel]]:
    result = await Delete[PlanGQLModel].DoItSafeWay(info=info, id=id)
    return result
