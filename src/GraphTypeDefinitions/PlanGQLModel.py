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
    description="""Entita reprezentující studijní plán pro tvorbu rozvrhu""",
)
class PlanGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).plans

    id = resolve_id #id
    name = resolve_name # název plánu
    changedby = resolve_changedby #kdo posledná měnil
    lastchange = resolve_lastchange #datum poslední změny
    created = resolve_created #datum vytvoření
    createdby = resolve_createdby #kdo vytvořil

    event_id: Optional[uuid.UUID] # Odkaz na hlavní událost
    
    rbac_object = resolve_rbacobject
    
    @strawberry.field(description="""Seznam plánovaných lekcí v rámci tohoto plánu""")
    async def lessons(self, info: strawberry.types.Info) -> List["PlannedLessonGQLModel"]:
        from .PlannedLessonGQLModel import PlannedLessonGQLModel
        # loader = getLoadersFromInfo(info).plans
        loader = PlannedLessonGQLModel.getLoader(info)
        result = await loader.filter_by(plan_id=self.id)
        return result
    
    @strawberry.field(description="""Acreditovaný semestr, ke kterému plán patří""")
    async def semester(self, info: strawberry.types.Info) -> Optional["AcSemesterGQLModel"]:
        from .AcSemesterGQLModel import AcSemesterGQLModel
        result = await AcSemesterGQLModel.resolve_reference(id=self.semester_id)
        return result
    
    @strawberry.field(description="""Hlavní událost, na které je plán založen""")
    async def event(self, info: strawberry.types.Info) -> Optional[EventGQLModel]:
        if self.event_id is None:
            return None
        return await EventGQLModel.resolve_reference(self.event_id)

@createInputs
@dataclass
class PlanInputFilter:
    name: str # filtr dle názvu
    masterevent_id: IDType #filtrování dle ID hlavní události

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

@strawberry.input(description="""Vstupní model pro vytvoření nového plánu""")
class PlanInsertGQLModel:
    semester_id: IDType = strawberry.field(description="ID semestru")
    masterevent_id: IDType = strawberry.field(description="ID hlavní události")
    id: Optional[IDType] = strawberry.field(description="Volitelné ID (UUID) plánu", default=None)
    name: Optional[str] = strawberry.field(description="Název plánu", default="Nový plán")
    pass

@strawberry.input(description="""Vstupní model pro aktualizaci existujícího plánu""")
class PlanUpdateGQLModel:
    id: IDType = strawberry.field(description="ID plánu")
    lastchange: datetime.datetime = strawberry.field(description="Časová značka poslední změny")
    name: Optional[str] = strawberry.field(description="Nový název plánu", default=None)
    pass

@strawberry.input(description="""Vstupní model pro smazání plánu""")
class PlanDeleteGQLModel:
    id: IDType = strawberry.field(description="ID plánu ke smazání")
    lastchange: datetime.datetime = strawberry.field(description="Časová značka pro kontrolu změn")
    pass

@strawberry.type(description="""Výsledek operace s plánem""")
class PlanResultGQLModel:
    id: uuid.UUID = strawberry.field(description="ID plánu", default=None)
    msg: str = strawberry.field(description="Zpráva o výsledku operace", default=None)

    @strawberry.field(description="""Result of lesson operation""")
    async def plan(self, info: strawberry.types.Info) -> Optional[PlanGQLModel]:
        result = await PlanGQLModel.resolve_reference(info, self.id)
        return result

from uoishelpers.resolvers import Insert, InsertError
@strawberry.mutation(description="""Plan insert""")
async def plan_insert(self, info: strawberry.types.Info, plan: PlanInsertGQLModel) -> Union[PlanGQLModel, InsertError[PlanGQLModel]]:
    result = await Insert[PlanGQLModel].DoItSafeWay(info=info, entity=plan)
    return result

from uoishelpers.resolvers import Update, UpdateError
@strawberry.mutation(description="""Plan update""")
async def plan_update(self, info: strawberry.types.Info, plan: PlanUpdateGQLModel) -> Union[PlanGQLModel, UpdateError[PlanGQLModel]]:
    result = await Update[PlanGQLModel].DoItSafeWay(info=info, entity=plan)
    return result
#generated
from uoishelpers.resolvers import Delete, DeleteError
@strawberry.mutation(description="""Plan delete""")
async def plan_delete(self, info: strawberry.types.Info, plan: PlanDeleteGQLModel) -> typing.Optional[DeleteError[PlanGQLModel]]:
    result = await Delete[PlanGQLModel].DoItSafeWay(info=info, entity=plan)
    return result
