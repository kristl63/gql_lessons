import pytest
import logging
import uuid
import sqlalchemy
import json
import datetime

from unittest.mock import AsyncMock
from src.GraphTypeDefinitions.AcSemesterGQLModel import AcSemesterGQLModel
from src.GraphTypeDefinitions.AcLessonTypeGQLModel import AcLessonTypeGQLModel


myquery = """
{
  me {
    id
    fullname
    email
    roles {
      valid
      group { id name }
      roletype { id name }
    }
  }
}"""

@pytest.mark.asyncio
async def test_result_test(NoRole_UG_Server):
    # response = {}
    response = await NoRole_UG_Server(query=myquery, variables={})
    
    print("response", response, flush=True)
    logging.info(f"response {response}")
    pass

from .gt_utils import (
    getQuery,

    createByIdTest2, 
    createUpdateTest2, 
    createTest2, 
    createDeleteTest2
)

# Test for Plan
test_plan_by_id = createByIdTest2(tableName="plans", variables={"id": "f2e9996c-2cca-42d9-93ec-660baf6f95b9"})
test_plan_update = createUpdateTest2(tableName="plans", variables={"name": "updated plan name", "id": "f2e9996c-2cca-42d9-93ec-660baf6f95b9","lastchange":"2024-08-11T21:45:06.685651"})
test_plan_create = createTest2(tableName="plans", queryName="create", variables={"name": "new plan", "semesterId": "b888524e-ab80-4078-b457-841cafbfb325", "mastereventId": "3e52a301-caad-46ba-8fe6-1a7e2f370866","lastchange":"2024-08-11T21:45:06.685651"})
test_plan_delete = createDeleteTest2(tableName="plans", variables={"name": "new plan", "semesterId": "b888524e-ab80-4078-b457-841cafbfb325", "mastereventId": "3e52a301-caad-46ba-8fe6-1a7e2f370866", "lastchange":"2024-08-11T21:45:06.685651"})

# Test for PlannedLessons
test_planned_lesson_by_id = createByIdTest2(tableName="plannedLessons", variables={"id": "18375c23-767c-4c1e-adb6-9b2beb463533"})
test_planned_lesson_update = createUpdateTest2(tableName="plannedLessons", variables={"name": "Téma new", "id": "e1f3405f-9492-4030-822e-df1c720cfb9e","lastchange":"2024-08-11T21:45:06.685651"})
test_planned_lesson_create = createTest2(tableName="plannedLessons", queryName="create", variables={"name": "new lesson"})
test_planned_lesson_delete = createDeleteTest2(tableName="plannedLessons", variables={"id": "18375c23-767c-4c1e-adb6-9b2beb463533", "name": "new lesson", "lastchange":"2024-08-11T21:45:06.685651"})


text_event_resolve_reference = createTest2(
    tableName="events",
    queryName="resolve_reference",
    variables={
        "id": "a64871f8-2308-48ff-adb2-33fb0b0741f1"
    }
)

test_user_resolve_reference = createTest2(
    tableName="users",
    queryName="resolve_reference",
    variables={"id": "ccb397ad-0de7-46e7-bff0-42452f11dd5e"}
)

test_group_resolve_reference = createTest2(
    tableName="groups",
    queryName="resolve_reference",
    variables={"id": "e806e77a-8bb0-49aa-ad01-d501400353fe"}
)

test_plan_resolve_reference = createTest2(
    tableName="plans",
    queryName="resolve_reference",
    variables={"id": "f2e9996c-2cca-42d9-93ec-660baf6f95b9"}
)

test_planned_lesson_resolve_reference = createTest2(
    tableName="plannedLessons",
    queryName="resolve_reference",
    variables={"id": "18375c23-767c-4c1e-adb6-9b2beb463533"}
)

test_facility_resolve_reference = createTest2(
    tableName="facilities",
    queryName="resolve_reference",
    variables={"id": "d5f66675-11db-4c65-9f11-bfe4e3cc25e2"}
)

@pytest.mark.asyncio
async def test_user_resolve_reference_direct():
    from src.GraphTypeDefinitions.UserGQLModel import UserGQLModel
    id = uuid.UUID("ccb397ad-0de7-46e7-bff0-42452f11dd5e")  # nahraď existujícím
    result = await UserGQLModel.resolve_reference(id)
    assert result.id == id

@pytest.mark.asyncio
async def test_group_resolve_reference_direct():
    from src.GraphTypeDefinitions.GroupGQLModel import GroupGQLModel
    id = uuid.UUID("e806e77a-8bb0-49aa-ad01-d501400353fe")
    result = await GroupGQLModel.resolve_reference(id)
    assert result.id == id

test_planned_lesson_full = createTest2(
    tableName="plannedLessons",
    queryName="full",
    variables={
        "id": "e1f3405f-9492-4030-822e-df1c720cfb9e"
    }
)

test_planned_lesson_user_insert = createTest2(
    tableName="plannedLessons",
    queryName="user_insert",
    variables={
        "userlesson": {
            "userId": "f340002d-c904-41e7-9e5d-8c8274bdf60d",
            "planlessonId": "e1f3405f-9492-4030-822e-df1c720cfb9e"
        }
    }
)

test_planned_lesson_group_insert = createTest2(
    tableName="plannedLessons",
    queryName="group_insert",
    variables={
        "grouplesson": {
            "groupId": "31a05917-8930-4778-a127-5c760637f92b",
            "planlessonId": "e1f3405f-9492-4030-822e-df1c720cfb9e"
        }
    }
)

test_planned_lesson_facility_insert = createTest2(
    tableName="plannedLessons",
    queryName="facility_insert",
    variables={
        "facilitylesson": {
            "facilityId": "f60b6df7-0a31-420e-b21c-cbac14fbc5e8",
            "planlessonId": "e1f3405f-9492-4030-822e-df1c720cfb9e"
        }
    }
)

test_planned_lesson_user_delete = createTest2(
    tableName="plannedLessons",
    queryName="user_delete",
    variables={
        "userlesson": {
            "userId": "f340002d-c904-41e7-9e5d-8c8274bdf60d",
            "planlessonId": "e1f3405f-9492-4030-822e-df1c720cfb9e"
        }
    }
)

test_planned_lesson_group_delete = createTest2(
    tableName="plannedLessons",
    queryName="group_delete",
    variables={
        "grouplesson": {
            "groupId": "31a05917-8930-4778-a127-5c760637f92b",
            "planlessonId": "e1f3405f-9492-4030-822e-df1c720cfb9e"
        }
    }
)

test_planned_lesson_facility_delete = createTest2(
    tableName="plannedLessons",
    queryName="facility_delete",
    variables={
        "facilitylesson": {
            "facilityId": "f60b6df7-0a31-420e-b21c-cbac14fbc5e8",
            "planlessonId": "e1f3405f-9492-4030-822e-df1c720cfb9e"
        }
    }
)

test_planned_lesson_resolvers = createTest2(
    tableName="plannedLessons",
    queryName="resolvers_test",
    variables={"id": "e1f3405f-9492-4030-822e-df1c720cfb9e"}
)

test_planned_lesson_nulls = createTest2(
    tableName="plannedLessons",
    queryName="null_fields",  # create gql
    variables={"id": "e1f3405f-9492-4030-822e-df1c720cfb9e"}
)

@pytest.mark.asyncio
async def test_facility_resolve_reference_direct():
    from src.GraphTypeDefinitions.FacilityGQLModel import FacilityGQLModel
    id = uuid.UUID("d5f66675-11db-4c65-9f11-bfe4e3cc25e2")
    result = await FacilityGQLModel.resolve_reference(id)
    assert result.id == id



    test_planned_lesson_resolver_fields = createTest2(
    tableName="plannedLessons",
    queryName="resolver_fields",
    variables={"id": "e1f3405f-9492-4030-822e-df1c720cfb9e"}
)

@pytest.mark.asyncio
async def test_planned_lesson_reference_not_found():
    from src.GraphTypeDefinitions.PlannedLessonGQLModel import PlannedLessonGQLModel

    class MockLoader:
        async def load(self, _id):
            return None

    class Info:
        context = {
            "loaders": type("Loaders", (), {"plan_lessons": MockLoader()})()
        }

    result = await PlannedLessonGQLModel.resolve_reference(info=Info(), id=uuid.uuid4())
    assert result is None