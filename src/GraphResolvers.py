from ast import Call
from typing import Coroutine, Callable, Awaitable, Union, List
import uuid
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from uoishelpers.resolvers import (
    create1NGetter,
    createEntityByIdGetter,
    createEntityGetter,
    createInsertResolver,
    createUpdateResolver,
)
from uoishelpers.resolvers import putSingleEntityToDb

from src.DBDefinitions import (
    BaseModel,
    PlannedLessonModel,
    UserPlanModel,
    GroupPlanModel,
    FacilityPlanModel,
)

# from src.DBDefinitions import UnavailabilityPL, UnavailabilityUser, UnavailabilityFacility
# from src.DBDefinitions import FacilityModel

###########################################################################################################################
#
# zde si naimportujte sve SQLAlchemy modely
#
###########################################################################################################################


###########################################################################################################################
#
# zde definujte sve resolvery s pomoci funkci vyse
# tyto pouzijete v GraphTypeDefinitions
#
###########################################################################################################################

## Nasleduji funkce, ktere lze pouzit jako asynchronni resolvery

resolvePlannedLessonPage = createEntityGetter(
    PlannedLessonModel
)  # fuction. return a list
resolvePlannedLessonById = createEntityByIdGetter(PlannedLessonModel)  # single row .
resolvePlannedLessonByTopic = create1NGetter(
    PlannedLessonModel, foreignKeyName="topic_id"
)
resolvePlannedLessonBySemester = create1NGetter(
    PlannedLessonModel, foreignKeyName="semester_id"
)
resolvePlannedLessonByEvent = create1NGetter(
    PlannedLessonModel, foreignKeyName="event_id"
)
resolvePlannedLessonsByLink = create1NGetter(
    PlannedLessonModel, foreignKeyName="linkedlesson_id"
)

# intermediate data resolver
resolveUserLinksForPlannedLesson = create1NGetter(
    UserPlanModel, foreignKeyName="plannedlesson_id"
)  #
resolveGroupLinksForPlannedLesson = create1NGetter(
    GroupPlanModel, foreignKeyName="plannedlesson_id"
)
resolveFacilityLinksForPlannedLesson = create1NGetter(
    FacilityPlanModel, foreignKeyName="plannedlesson_id"
)
# resolveEventLinksForPlannedLesson = create1NGetter(Eve)

# unavailable Plan lesson resolver
# resolveUnavailabilityPLById = createEntityByIdGetter(UnavailabilityPL)
# resolveUnavailabilityPLAll = createEntityGetter(UnavailabilityPL)
# resolverUpdateUnavailabilityPL = createUpdateResolver(UnavailabilityPL)
# resolveInsertUnavailabilityPL = createInsertResolver(UnavailabilityPL)

# unavailable User resolver
# resolveUnavailabilityUserById = createEntityByIdGetter(UnavailabilityUser)
# resolveUnavailabilityUserAll = createEntityGetter(UnavailabilityUser)
# resolverUpdateUnavailabilityUser = createUpdateResolver(UnavailabilityUser)
# resolveInsertUnavailabilityUser = createInsertResolver(UnavailabilityUser)

# unavailable Facility resolver
# resolveUnavailabilityFacilityById = createEntityByIdGetter(UnavailabilityFacility)
# resolveUnavailabilityFacilityAll = createEntityGetter(UnavailabilityFacility)
# resolverUpdateUnavailabilityFacility = createUpdateResolver(UnavailabilityFacility)
# resolveInsertUnavailabilityFacility = createInsertResolver(UnavailabilityFacility)

from sqlalchemy import delete, insert
import strawberry#
from typing import Optional#

async def resolveRemoveUsersFromPlan(asyncSessionMaker, plan_id, usersids):
    # selectStmt = (select(UserPlanModel)
    #     .where(UserPlanModel.planlesson_id==plan_id)
    #     .where(UserPlanModel.user_id.in_(set(usersids))))
    
    deleteStmt = (delete(UserPlanModel)
        .where(UserPlanModel.planlesson_id==plan_id)
        .where(UserPlanModel.user_id.in_(set(usersids))))
    #print(deleteStmt)
    #print(usersids)
    async with asyncSessionMaker() as session:
        # print(selectStmt.compile(compile_kwargs={"literal_binds": True}))
        rows = await session.execute(deleteStmt)
        # items = list(rows.scalars())
        # print(items)
        # for item in items:
        #     print("item", item.id, item.user_id)
        #     session.delete(item)
        #print(rows.rowcount)
        await session.commit()
        

async def resolveAddUsersToPlan(asyncSessionMaker, plan_id, usersids):
    async with asyncSessionMaker() as session:
        await session.execute(insert(UserPlanModel), [{"planlesson_id": plan_id, "user_id": user_id} for user_id in usersids])
        await session.commit()

async def resolveRemoveGroupsFromPlan(asyncSessionMaker, plan_id, groupids):
    deleteStmt = (delete(GroupPlanModel)
        .where(GroupPlanModel.planlesson_id==plan_id)
        .where(GroupPlanModel.group_id.in_(groupids)))
    async with asyncSessionMaker() as session:
        await session.execute(deleteStmt)
        await session.commit()

async def resolveAddGroupsToPlan(asyncSessionMaker, plan_id, groupids):
    async with asyncSessionMaker() as session:
        await session.execute(insert(GroupPlanModel), [{"planlesson_id": plan_id, "group_id": group_id} for group_id in groupids])
        await session.commit()

async def resolveRemoveFacilitiesFromPlan(asyncSessionMaker, plan_id, facilityids):
    deleteStmt = (delete(FacilityPlanModel)
        .where(FacilityPlanModel.planlesson_id==plan_id)
        .where(FacilityPlanModel.facility_id.in_(facilityids)))
    async with asyncSessionMaker() as session:
        await session.execute(deleteStmt)
        await session.commit()

async def resolveAddFacilitiesToPlan(asyncSessionMaker, plan_id, facilityids):
    async with asyncSessionMaker() as session:
        await session.execute(insert(FacilityPlanModel), [{"plan_id": plan_id, "facility_id": facility_id} for facility_id in facilityids])
        await session.commit()

async def resolveRemovePlan(asyncSessionMaker, plan_id):
    deleteAStmt = delete(UserPlanModel).where(UserPlanModel.planlesson_id==plan_id)
    deleteBStmt = delete(GroupPlanModel).where(GroupPlanModel.planlesson_id==plan_id)
    deleteCStmt = delete(FacilityPlanModel).where(FacilityPlanModel.planlesson_id==plan_id)
    deleteDStmt = delete(PlannedLessonModel).where(PlannedLessonModel.id==plan_id)
    async with asyncSessionMaker() as session:
        await session.execute(deleteAStmt)
        await session.execute(deleteBStmt)
        await session.execute(deleteCStmt)
        await session.execute(deleteDStmt)
        await session.commit()


#added
@strawberry.type
class Plan:
    id: strawberry.ID
    name: str
    lastchange: str

@strawberry.type
class Query:
    @strawberry.field
    async def plan_by_id(self, info: strawberry.types.Info, id: strawberry.ID) -> Optional[Plan]:
        async with info.context["asyncSessionMaker"]() as session:
            result = await session.execute(select(PlannedLessonModel).where(PlannedLessonModel.id == id))
            plan = result.scalar_one_or_none()
            if plan:
                return Plan(id=plan.id, name=plan.name, lastchange=plan.lastchange)
            return None