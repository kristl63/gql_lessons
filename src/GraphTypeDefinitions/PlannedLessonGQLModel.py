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
    resolve_rbacobject,
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

# Definice anotací pro lazy načítání modelů
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
    """Model pro plánovanou lekci."""

    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        """Vrací loader pro načítání plánovaných lekcí."""
        return getLoadersFromInfo(info).plan_lessons

    id = resolve_id  # ID lekce
    name = resolve_name  # Název lekce
    changedby = resolve_changedby  # Kdo naposledy změnil
    lastchange = resolve_lastchange  # Datum poslední změny
    created = resolve_created  # Datum vytvoření
    createdby = resolve_createdby  # Kdo vytvořil

    rbac_object = resolve_rbacobject  # RBAC objekt pro oprávnění

    @strawberry.field(description="""Pořadí lekce v plánu""")
    def order(self) -> Optional[int]:
        """Vrací pořadí lekce, pokud není definováno, vrací 0."""
        return self.order if self.order else 0

    @strawberry.field(description="""Délka lekce v minutách""")
    def length(self) -> Optional[int]:
        """Vrací délku lekce, pokud není definována, vrací 0."""
        return self.length if self.length else 0

    @strawberry.field(description="""Typ lekce (např. přednáška, cvičení)""")
    async def type(self, info: strawberry.types.Info) -> Optional["AcLessonTypeGQLModel"]:
        """Vrací typ lekce na základě ID."""
        from .AcLessonTypeGQLModel import AcLessonTypeGQLModel
        result = await AcLessonTypeGQLModel.resolve_reference(id=self.lessontype_id)
        return result

    @strawberry.field(description="""Lekce, na kterou je tato lekce navázána""")
    async def linked_to(
        self, info: strawberry.types.Info
    ) -> Optional["PlannedLessonGQLModel"]:
        """Vrací lekci, na kterou je tato lekce navázána."""
        loader = PlannedLessonGQLModel.getLoader(info)
        result = None
        if self.linkedlesson_id is not None:
            result = await loader.load(self.linkedlesson_id)
        return result

    @strawberry.field(description="""Lekce navázané na tuto lekci""")
    async def linked_with(
        self, info: strawberry.types.Info, including_self: Optional[bool] = False
    ) -> List["PlannedLessonGQLModel"]:
        """Vrací seznam lekcí navázaných na tuto lekci."""
        loader = PlannedLessonGQLModel.getLoader(info)
        result1 = [self]
        if self.linkedlesson_id is not None:
            result2 = await loader.filter_by(linkedlesson_id=self.id)
            result1 = [*result1, *result2]
        return result1

    @strawberry.field(description="""Seznam učitelů přiřazených k lekci""")
    async def users(self, info: strawberry.types.Info) -> List["UserGQLModel"]:
        """Vrací seznam uživatelů (učitelů) přiřazených k lekci."""
        from .UserGQLModel import UserGQLModel
        loader = getLoadersFromInfo(info).plan_lessons_users
        result = await loader.filter_by(planlesson_id=self.id)
        return [UserGQLModel(id=item.user_id) for item in result]

    @strawberry.field(description="""Seznam studijních skupin přiřazených k lekci""")
    async def groups(self, info: strawberry.types.Info) -> List["GroupGQLModel"]:
        """Vrací seznam studijních skupin přiřazených k lekci."""
        from .GroupGQLModel import GroupGQLModel
        loader = getLoadersFromInfo(info).plan_lessons_groups
        result = await loader.filter_by(planlesson_id=self.id)
        return [GroupGQLModel(id=item.group_id) for item in result]

    @strawberry.field(description="""Seznam zařízení přiřazených k lekci""")
    async def facilities(
        self, info: strawberry.types.Info
    ) -> List["FacilityGQLModel"]:
        """Vrací seznam zařízení přiřazených k lekci."""
        from .FacilityGQLModel import FacilityGQLModel
        loader = getLoadersFromInfo(info).plan_lessons_facilities
        result = await loader.filter_by(planlesson_id=self.id)
        return [FacilityGQLModel(id=item.facility_id) for item in result]

    @strawberry.field(description="""Událost spojená s lekcí""")
    async def event(self, info: strawberry.types.Info) -> Optional["EventGQLModel"]:
        """Vrací událost spojenou s lekcí."""
        from .EventGQLModel import EventGQLModel
        if self.event_id is None:
            result = None
        else:
            result = EventGQLModel(id=self.event_id)
        return result

    @strawberry.field(description="""Téma lekce z akreditace""")
    async def topic(
        self, info: strawberry.types.Info
    ) -> Optional["AcTopicGQLModel"]:
        """Vrací téma lekce z akreditace."""
        from .AcTopicGQLModel import AcTopicGQLModel
        if self.topic_id is None:
            result = None
        else:
            result = AcTopicGQLModel(id=self.topic_id)
        return result

    @strawberry.field(description="""Semestr, ke kterému lekce patří""")
    async def semester(
        self, info: strawberry.types.Info
    ) -> Optional["AcSemesterGQLModel"]:
        """Vrací semestr, ke kterému lekce patří."""
        from .AcSemesterGQLModel import AcSemesterGQLModel
        if self.semester_id is None:
            result = None
        else:
            result = AcSemesterGQLModel(id=self.semester_id)
        return result

    @strawberry.field(description="""Plán, ke kterému lekce patří""")
    async def plan(
        self, info: strawberry.types.Info
    ) -> Optional["PlanGQLModel"]:
        """Vrací plán, ke kterému lekce patří."""
        from .PlanGQLModel import PlanGQLModel
        result = await PlanGQLModel.resolve_reference(info, self.plan_id)
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

@strawberry.field(description="""Plánovaná lekce podle jejího ID""")
async def planned_lesson_by_id(self, info, id: uuid.UUID) -> Optional[PlannedLessonGQLModel]:
    """Vrací plánovanou lekci podle jejího ID."""
    return await PlannedLessonGQLModel.resolve_reference(info, id)

@strawberry.field(description="""Plánované lekce stránkované""")
@asPage
async def planned_lesson_page(
    self, info: strawberry.types.Info, skip: int = 0, limit: int = 10, 
    where: Optional[PlannedLessonInputFilter] = None
) -> List[PlannedLessonGQLModel]:
    """Vrací stránkované plánované lekce."""
    return PlannedLessonGQLModel.getLoader(info)

#########################################################
#
# Mutace
#
#########################################################

@strawberry.input(description="Vstupní model pro vložení plánované lekce")
class PlannedLessonInsertGQLModel:
    name: str = strawberry.field(default=None, description="Název lekce, např. 'Úvod'")
    plan_id: uuid.UUID = strawberry.field(default=None, description="ID plánu, ke kterému lekce patří")
    length: Optional[int] = strawberry.field(default=2, description="Délka lekce v 45min intervalech")
    startproposal: Optional[datetime.datetime] = strawberry.field(default=None, description="Návrh data a času")
    order: Optional[int] = strawberry.field(default=1, description="Pořadí lekce v plánu")

    linkedlesson_id: Optional[uuid.UUID] =  strawberry.field(default=None, description="ID lekce z jiného plánu, která bude vyučována společně")
    topic_id: Optional[uuid.UUID] = None
    lessontype_id: Optional[uuid.UUID] = strawberry.field(default=uuid.UUID("e2b7cbf6-95e1-11ed-a1eb-0242ac120002"), description="Typ lekce, např. Konzultace, Laboratoř, ...")
    semester_id: Optional[uuid.UUID] = strawberry.field(default=None, description="ID semestru (předmětu) z akreditace")
    event_id: Optional[uuid.UUID] = strawberry.field(default=None, description="Událost definující, kdy bude lekce vyučována")
    id: Optional[uuid.UUID]  = strawberry.field(default=None, description="Primární klíč generovaný klientem, očekává se UUID")

    createdby: strawberry.Private[IDType] = None
    rbacobject: strawberry.Private[IDType] = None

@strawberry.input(description="Vstupní model pro aktualizaci plánované lekce")
class PlannedLessonUpdateGQLModel:
    lastchange: datetime.datetime = strawberry.field(default=None, description="Časová značka poslední změny")
    id: uuid.UUID = strawberry.field(default=None, description="Primární klíč lekce")
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

@strawberry.input(description="Vstupní model pro odstranění plánované lekce")
class PlannedLessonDeleteGQLModel:
    lastchange: datetime.datetime
    id: uuid.UUID
    plan_id: Optional[uuid.UUID] = None

@strawberry.type(description="Výsledek operace s plánovanou lekcí")
class PlannedLessonResultGQLModel:
    id: uuid.UUID = None
    msg: str = None

    @strawberry.field(description="""Výsledek operace s lekcí""")
    async def lesson(self, info: strawberry.types.Info) -> Optional[PlannedLessonGQLModel]:
        """Vrací lekci na základě ID."""
        result = await PlannedLessonGQLModel.resolve_reference(info, self.id)
        return result
    
    @strawberry.field(description="""Plán, ke kterému lekce patří""")
    async def plan(self, info: strawberry.types.Info) -> Optional[PlanGQLModel]:
        """Vrací plán, ke kterému lekce patří."""
        from .PlanGQLModel import PlanGQLModel
        result = await PlannedLessonGQLModel.resolve_reference(info, self.id)
        if result.plan_id:
            return await PlanGQLModel.resolve_reference(info, id=result.plan_id)
        return None
        
@strawberry.input(description="Vstupní model pro přiřazení učitele k lekci")
class PlannedLessonUserInsertGQLModel:
    user_id: uuid.UUID
    planlesson_id: uuid.UUID
    id: Optional[IDType] = None
    createdby: strawberry.Private[IDType] = None
    rbacobject: strawberry.Private[IDType] = None
    
@strawberry.input(description="Vstupní model pro odstranění učitele z lekce")
class PlannedLessonUserDeleteGQLModel:
    user_id: uuid.UUID
    planlesson_id: uuid.UUID

@strawberry.input(description="Vstupní model pro přiřazení skupiny k lekci")
class PlannedLessonGroupInsertGQLModel:
    group_id: uuid.UUID
    planlesson_id: uuid.UUID
    id: Optional[IDType] = None
    createdby: strawberry.Private[IDType] = None
    rbacobject: strawberry.Private[IDType] = None
    
@strawberry.input(description="Vstupní model pro odstranění skupiny z lekce")
class PlannedLessonGroupDeleteGQLModel:
    group_id: uuid.UUID
    planlesson_id: uuid.UUID

@strawberry.input(description="Vstupní model pro přiřazení zařízení k lekci")
class PlannedLessonFacilityInsertGQLModel:
    facility_id: uuid.UUID
    planlesson_id: uuid.UUID
    id: Optional[IDType] = None
    createdby: strawberry.Private[IDType] = None
    rbacobject: strawberry.Private[IDType] = None
    
@strawberry.input(description="Vstupní model pro odstranění zařízení z lekce")
class PlannedLessonFacilityDeleteGQLModel:
    facility_id: uuid.UUID
    planlesson_id: uuid.UUID

@strawberry.input(description="Vstupní model pro přiřazení uživatelů, zařízení a skupin k lekci")
class PlannedLessonAssignmentGQLModel:
    lastchange: datetime.datetime
    id: uuid.UUID
    users: Optional[List[uuid.UUID]] = None
    facilities: Optional[List[uuid.UUID]] = None
    groups: Optional[List[uuid.UUID]] = None

@strawberry.mutation(description="Přiřazuje učitele k plánované lekci")
async def planned_lesson_user_insert(self, info: strawberry.types.Info, userlesson: PlannedLessonUserInsertGQLModel) -> PlannedLessonResultGQLModel:
    """Přiřazuje učitele k plánované lekci."""
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

@strawberry.mutation(description="Odstraňuje učitele z plánované lekce")
async def planned_lesson_user_delete(self, info: strawberry.types.Info, userlesson: PlannedLessonUserDeleteGQLModel) -> PlannedLessonResultGQLModel:
    """Odstraňuje učitele z plánované lekce."""
    loader = getLoadersFromInfo(info).plan_lessons_users
    rows = await loader.filter_by(planlesson_id=userlesson.planlesson_id, user_id=userlesson.user_id)
    row = next(rows, None)
    result = PlannedLessonResultGQLModel()
    if row is None:
        result.msg = "fail"
    else:
        await loader.delete(row.id)
        result.msg = "ok"
    result.id = userlesson.planlesson_id
    return result

@strawberry.mutation(description="Přiřazuje skupinu k plánované lekci")
async def planned_lesson_group_insert(self, info: strawberry.types.Info, grouplesson: PlannedLessonGroupInsertGQLModel) -> PlannedLessonResultGQLModel:
    """Přiřazuje skupinu k plánované lekci."""
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

@strawberry.mutation(description="Odstraňuje skupinu z plánované lekce")
async def planned_lesson_group_delete(self, info: strawberry.types.Info, grouplesson: PlannedLessonGroupDeleteGQLModel) -> PlannedLessonResultGQLModel:
    """Odstraňuje skupinu z plánované lekce."""
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

@strawberry.mutation(description="Přiřazuje zařízení k plánované lekci")
async def planned_lesson_facility_insert(self, info: strawberry.types.Info, facilitylesson: PlannedLessonFacilityInsertGQLModel) -> PlannedLessonResultGQLModel:
    """Přiřazuje zařízení k plánované lekci."""
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

@strawberry.mutation(description="Odstraňuje zařízení z plánované lekce")
async def planned_lesson_facility_delete(self, info: strawberry.types.Info, facilitylesson: PlannedLessonFacilityDeleteGQLModel) -> PlannedLessonResultGQLModel:
    """Odstraňuje zařízení z plánované lekce."""
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

@strawberry.mutation(description="Vkládá novou plánovanou lekci")
async def planned_lesson_insert(self, info: strawberry.types.Info, lesson: PlannedLessonInsertGQLModel) -> PlannedLessonResultGQLModel:
    """Vkládá novou plánovanou lekci."""
    return await encapsulateInsert(info, PlannedLessonGQLModel.getLoader(info), lesson, PlannedLessonResultGQLModel(msg="ok", id=None))

@strawberry.mutation(description="Aktualizuje plánovanou lekci")
async def planned_lesson_update(self, info: strawberry.types.Info, lesson: PlannedLessonUpdateGQLModel) -> PlannedLessonResultGQLModel:
    """Aktualizuje plánovanou lekci."""
    return await encapsulateUpdate(info, PlannedLessonGQLModel.getLoader(info), lesson, PlannedLessonResultGQLModel(msg="ok", id=None))

PlanResultGQLModel = Annotated["PlanResultGQLModel", strawberry.lazy(".PlanGQLModel")]
@strawberry.mutation(description="Odstraňuje plánovanou lekci")
async def planned_lesson_remove(self, info: strawberry.types.Info, lesson: PlannedLessonDeleteGQLModel) -> Optional["PlanResultGQLModel"]:
    """Odstraňuje plánovanou lekci."""
    from .PlanGQLModel import PlanResultGQLModel
    loader = PlannedLessonGQLModel.getLoader(info)
    row = await loader.load(lesson.id)
    result = PlanResultGQLModel()
    if row:
        await loader.delete(lesson.id)
        result.msg = "ok"
        result.id = row.plan_id or uuid.UUID(int=0)
    else:
        result.msg = "fail"
        result.id = uuid.UUID(int=0)
    return result


