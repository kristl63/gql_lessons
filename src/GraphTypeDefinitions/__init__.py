from typing import List, Union, Optional, Annotated
import strawberry
import uuid


###########################################################################################################################
#
# zde definujte svuj Query model
#
###########################################################################################################################

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

@strawberry.federation.type(extend=True)
class Mutation:
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

    from .PlannedLessonGQLModel import (
        planned_lesson_insert,
        planned_lesson_update,
        planned_lesson_remove
    )
    planned_lesson_insert = planned_lesson_insert
    planned_lesson_update = planned_lesson_update
    planned_lesson_remove = planned_lesson_remove
    
###########################################################################################################################
#
# Schema je pouzito v main.py, vsimnete si parametru types, obsahuje vyjmenovane modely. Bez explicitniho vyjmenovani
# se ve schema objevi jen ty struktury, ktere si strawberry dokaze odvodit z Query. Protoze v teto konkretni implementaci
# nektere modely nejsou s Query propojene je potreba je explicitne vyjmenovat. Jinak ve federativnim schematu nebude
# dostupne rozsireni, ktere tento prvek federace implementuje.
#
###########################################################################################################################

from .UserGQLModel import UserGQLModel
from .EventGQLModel import EventGQLModel
from .FacilityGQLModel import FacilityGQLModel

schema = strawberry.federation.Schema(query=Query, mutation=Mutation, types=(UserGQLModel, EventGQLModel, FacilityGQLModel))
