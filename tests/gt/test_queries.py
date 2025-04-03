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

@pytest.mark.asyncio
async def test_linked_to_fetches_data():
    from src.GraphTypeDefinitions.PlannedLessonGQLModel import PlannedLessonGQLModel
    import uuid

    linked_id = uuid.uuid4()
    instance_id = uuid.uuid4()

    # Create instance "bez" initu
    instance = object.__new__(PlannedLessonGQLModel)
    instance.__dict__["id"] = instance_id
    instance.__dict__["linkedlesson_id"] = linked_id

    # Mock loader
    class MockLoader:
        async def load(self, _id):
            assert _id == linked_id
            return {"id": _id}

    class Info:
        context = {
            "loaders": type("Loaders", (), {"plan_lessons": MockLoader()})()
        }

    result = await instance.linked_to(Info())
    assert result["id"] == linked_id

import uuid
import pytest
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_linked_with_fetches_linked_lessons():
    from src.GraphTypeDefinitions.PlannedLessonGQLModel import PlannedLessonGQLModel

    lesson_id = uuid.uuid4()
    linked_id = uuid.uuid4()

    # Vytvoření instance bez __init__
    instance = object.__new__(PlannedLessonGQLModel)
    instance.__dict__["id"] = lesson_id
    instance.__dict__["linkedlesson_id"] = linked_id

    # Mock loader
    class MockLoader:
        async def filter_by(self, **kwargs):
            assert kwargs == {"linkedlesson_id": lesson_id}
            return [{"id": "mock-lesson-1"}, {"id": "mock-lesson-2"}]

    class Info:
        context = {
            "loaders": type("Loaders", (), {
                "plan_lessons": MockLoader()
            })()
        }

    result = await instance.linked_with(Info())

    # Assertion: první položka je "self", další jsou z filter_by
    assert isinstance(result, list)
    assert result[0] == instance
    assert len(result) == 3  # 1 self + 2 mock results

import pytest
from src.GraphTypeDefinitions.PlannedLessonGQLModel import PlannedLessonGQLModel

@pytest.mark.asyncio
async def test_event_returns_none_when_event_id_is_none():
    # Vytvoř instanci bez __init__
    instance = object.__new__(PlannedLessonGQLModel)
    instance.__dict__["event_id"] = None

    class Info:
        context = {}  # není potřeba loader

    result = await instance.event(Info())

    assert result is None

import pytest
from src.GraphTypeDefinitions.PlannedLessonGQLModel import PlannedLessonGQLModel

@pytest.mark.asyncio
async def test_topic_returns_none_when_topic_id_is_none():
    instance = object.__new__(PlannedLessonGQLModel)
    instance.__dict__["topic_id"] = None

    class Info:
        context = {}

    result = await instance.topic(Info())

    assert result is None

import pytest
import uuid
from src.GraphTypeDefinitions.PlannedLessonGQLModel import PlannedLessonGQLModel

@pytest.mark.asyncio
async def test_semester_returns_model_when_id_present():
    semester_uuid = uuid.uuid4()

    instance = object.__new__(PlannedLessonGQLModel)
    instance.__dict__["semester_id"] = semester_uuid

    class Info:
        context = {}

    result = await instance.semester(Info())

    assert result is not None
    assert result.id == semester_uuid

import pytest
from unittest.mock import AsyncMock
from src.GraphTypeDefinitions.PlannedLessonGQLModel import planned_lesson_page

@pytest.mark.asyncio
async def test_planned_lesson_page_returns_loader():
    # Připrav mock loader s .page metodou
    mock_loader = AsyncMock()
    mock_loader.page = AsyncMock(return_value="paged-result")

    class MockAll:
        plan_lessons = mock_loader

    class Info:
        context = {"loaders": MockAll()}

    # Zavolání resolveru přes base_resolver
    result = await planned_lesson_page.base_resolver(None, Info(), skip=0, limit=10, where=None)

    # Ověř výsledek
    assert result == "paged-result"

    # Ověř že .page bylo zavoláno (minimálně)
    mock_loader.page.assert_awaited_once()

    # A volitelně zkontroluj klíčové argumenty
    called_args = mock_loader.page.await_args.kwargs
    assert called_args["skip"] == 0
    assert called_args["limit"] == 10
    assert called_args["where"] is None


import pytest
import uuid
from unittest.mock import AsyncMock
from src.GraphTypeDefinitions.PlannedLessonGQLModel import PlannedLessonResultGQLModel
from src.GraphTypeDefinitions.PlannedLessonGQLModel import PlannedLessonGQLModel
from src.GraphTypeDefinitions.PlanGQLModel import PlanGQLModel

@pytest.mark.asyncio
async def test_plan_field_returns_plan_when_plan_id_exists():
    lesson_id = uuid.uuid4()
    plan_id = uuid.uuid4()

    instance = object.__new__(PlannedLessonResultGQLModel)
    instance.__dict__["id"] = lesson_id

    # mock plannedLesson -> plan_id
    PlannedLessonGQLModel.resolve_reference = AsyncMock(return_value=type("MockLesson", (), {"plan_id": plan_id})())
    # mock Plan resolve_reference
    PlanGQLModel.resolve_reference = AsyncMock(return_value=type("MockPlan", (), {"id": plan_id})())

    class Info:
        context = {}

    result = await instance.plan(Info())
    assert result.id == plan_id


@pytest.mark.asyncio
async def test_plan_field_returns_none_when_no_plan_id():
    instance = object.__new__(PlannedLessonResultGQLModel)
    instance.__dict__["id"] = uuid.uuid4()

    PlannedLessonGQLModel.resolve_reference = AsyncMock(return_value=type("MockLesson", (), {"plan_id": None})())

    class Info:
        context = {}

    result = await instance.plan(Info())
    assert result is None

import pytest
from unittest.mock import AsyncMock
from src.GraphTypeDefinitions.PlannedLessonGQLModel import planned_lesson_user_insert
from src.GraphTypeDefinitions.PlannedLessonGQLModel import PlannedLessonUserInsertGQLModel
@pytest.mark.asyncio
async def test_planned_lesson_user_insert_new():
    userlesson = PlannedLessonUserInsertGQLModel(
        user_id="f340002d-c904-41e7-9e5d-8c8274bdf60d",
        planlesson_id="e1f3405f-9492-4030-822e-df1c720cfb9e"
    )

    class Loader:
        async def filter_by(self, **kwargs):
            return []

        async def insert(self, x):
            return {"id": "inserted"}

    class Info:
        context = {
            "loaders": type("All", (), {"plan_lessons_users": Loader()})(),
            "user": {"id": "16cc5c71-5a69-4637-91c5-6ae7cff40633"}  # ✅ mocknutý uživatel
        }

    result = await planned_lesson_user_insert.base_resolver(None, Info(), userlesson)

    assert result.msg == "ok"
    assert result.id == userlesson.planlesson_id

import pytest
from uuid import UUID
from src.GraphTypeDefinitions.PlannedLessonGQLModel import (
    planned_lesson_user_delete,
    PlannedLessonUserDeleteGQLModel,
)

@pytest.mark.asyncio
async def test_planned_lesson_user_delete_row_none():
    userlesson = PlannedLessonUserDeleteGQLModel(
        user_id=UUID("f340002d-c904-41e7-9e5d-8c8274bdf60d"),
        planlesson_id=UUID("e1f3405f-9492-4030-822e-df1c720cfb9e")
    )

    class Loader:
        async def filter_by(self, **kwargs):
            return iter([])  # ✅ iterátor místo listu

    class Info:
        context = {
            "loaders": type("All", (), {"plan_lessons_users": Loader()})(),
            "user": {"id": "16cc5c71-5a69-4637-91c5-6ae7cff40633"}
        }

    result = await planned_lesson_user_delete.base_resolver(None, Info(), userlesson)

    assert result.msg == "fail"
    assert result.id == userlesson.planlesson_id

@pytest.mark.asyncio
async def test_planned_lesson_group_insert_inserts_if_not_exists():
    from src.GraphTypeDefinitions.PlannedLessonGQLModel import (
        planned_lesson_group_insert,
        PlannedLessonGroupInsertGQLModel,
    )

    grouplesson = PlannedLessonGroupInsertGQLModel(
        planlesson_id=UUID("e1f3405f-9492-4030-822e-df1c720cfb9e"),
        group_id=UUID("f340002d-c904-41e7-9e5d-8c8274bdf60d"),
    )

    class Loader:
        async def filter_by(self, **kwargs):
            return []  # žádné existující propojení, triggerne insert

        async def insert(self, value):
            assert value == grouplesson
            return {"id": "0cb1a2ed-c205-4295-965d-b4513666de21"}

    class Info:
        context = {
            "loaders": type("All", (), {"plan_lessons_groups": Loader()})(),
            "user": {"id": "16cc5c71-5a69-4637-91c5-6ae7cff40633"}
        }

    result = await planned_lesson_group_insert.base_resolver(None, Info(), grouplesson)

    assert result.id == grouplesson.planlesson_id
    assert result.msg == "ok"

@pytest.mark.asyncio
async def test_planned_lesson_group_delete_row_none():
    from src.GraphTypeDefinitions.PlannedLessonGQLModel import (
        planned_lesson_group_delete,
        PlannedLessonGroupDeleteGQLModel,
    )

    grouplesson = PlannedLessonGroupDeleteGQLModel(
        planlesson_id=UUID("e1f3405f-9492-4030-822e-df1c720cfb9e"),
        group_id=UUID("f340002d-c904-41e7-9e5d-8c8274bdf60d"),
    )

    class Loader:
        async def filter_by(self, **kwargs):
            return iter([])  # ⬅ přidáno iter() – řeší problém


        async def delete(self, id):
            pass  # nebude voláno

    class Info:
        context = {
            "loaders": type("All", (), {"plan_lessons_groups": Loader()})(),
            "user": {"id": "16cc5c71-5a69-4637-91c5-6ae7cff40633"}
        }

    result = await planned_lesson_group_delete.base_resolver(None, Info(), grouplesson)

    assert result.msg == "fail"
    assert result.id == grouplesson.planlesson_id

import pytest
from uuid import UUID
from src.GraphTypeDefinitions.PlannedLessonGQLModel import planned_lesson_facility_insert
from src.GraphTypeDefinitions.PlannedLessonGQLModel import PlannedLessonFacilityInsertGQLModel

@pytest.mark.asyncio
async def test_planned_lesson_facility_insert_calls_insert():
    facilitylesson = PlannedLessonFacilityInsertGQLModel(
        planlesson_id=UUID("e1f3405f-9492-4030-822e-df1c720cfb9e"),
        facility_id=UUID("a2d7ef58-b2e5-4f7f-9b0a-e518d1b25af8")
    )

    class Loader:
        async def filter_by(self, **kwargs):
            return []  # ⬅️ způsobí vstup do bloku `if not exists`

        async def insert(self, data):
            return {"id": "inserted-facility"}

    class Info:
        context = {
            "loaders": type("All", (), {"plan_lessons_facilities": Loader()})(),
            "user": {"id": "16cc5c71-5a69-4637-91c5-6ae7cff40633"}
        }

    result = await planned_lesson_facility_insert.base_resolver(None, Info(), facilitylesson)

    assert result.id == facilitylesson.planlesson_id
    assert result.msg == "ok"

@pytest.mark.asyncio
async def test_planned_lesson_facility_delete_row_none():
    from src.GraphTypeDefinitions.PlannedLessonGQLModel import planned_lesson_facility_delete
    from src.GraphTypeDefinitions.PlannedLessonGQLModel import PlannedLessonFacilityDeleteGQLModel
    from uuid import UUID

    facilitylesson = PlannedLessonFacilityDeleteGQLModel(
        facility_id=UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),
        planlesson_id=UUID("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb")
    )

    class Loader:
        async def filter_by(self, **kwargs):
            return iter([])  # ✅ vrací iterator, ne list

        async def delete(self, id):
            pass


    class Info:
        context = {
            "loaders": type("All", (), {"plan_lessons_facilities": Loader()})()
        }

    result = await planned_lesson_facility_delete.base_resolver(None, Info(), facilitylesson)

    assert result.msg == "fail"                       # ⬅ this hits line 415
    assert result.id == facilitylesson.planlesson_id

import pytest
from uuid import UUID
from datetime import datetime
from src.GraphTypeDefinitions.PlannedLessonGQLModel import planned_lesson_remove, PlannedLessonDeleteGQLModel

@pytest.mark.asyncio
async def test_planned_lesson_remove_row_none():
    # Arrange
    lesson = PlannedLessonDeleteGQLModel(
        id=UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),
        lastchange=datetime.utcnow()  # nebo nějaký pevný čas, pokud chceš deterministický test
    )

    class Loader:
        async def load(self, _id):
            return None  # ⬅ triggne else větev → pokryje řádky 445–446

        async def delete(self, _id):  # není voláno v tomto scénáři
            pass

    class Info:
        context = {"loaders": type("All", (), {"plan_lessons": Loader()})()}

    # Act
    result = await planned_lesson_remove.base_resolver(None, Info(), lesson)

    # Assert
    assert result.msg == "fail"
    assert result.id == UUID(int=0)

import pytest
from uuid import UUID
from unittest.mock import AsyncMock
@pytest.mark.asyncio
async def test_lessons_returns_filtered_plans():
    from src.GraphTypeDefinitions.PlanGQLModel import PlanGQLModel
    from src.GraphTypeDefinitions.PlannedLessonGQLModel import PlannedLessonGQLModel
    from uuid import UUID
    from unittest.mock import AsyncMock

    class Info:
        context = {}

    mock_loader = AsyncMock()
    mock_loader.filter_by.return_value = ["lesson1", "lesson2"]

    PlannedLessonGQLModel.getLoader = lambda info: mock_loader

    # 👉 použij originální třídu, ne mock
    instance = object.__new__(PlanGQLModel)
    instance.id = UUID("f2e9996c-2cca-42d9-93ec-660baf6f95b9")

    result = await instance.lessons(Info())

    mock_loader.filter_by.assert_awaited_once_with(plan_id=instance.id)
    assert result == ["lesson1", "lesson2"]

@pytest.mark.asyncio
async def test_plan_semester_returns_resolved_object():
    from src.GraphTypeDefinitions.PlanGQLModel import PlanGQLModel
    from src.GraphTypeDefinitions.AcSemesterGQLModel import AcSemesterGQLModel
    from uuid import UUID
    from unittest.mock import AsyncMock

    # ⚙️ Mock resolve_reference
    AcSemesterGQLModel.resolve_reference = AsyncMock(return_value="mock-semester")

    # ⚙️ Vytvoř PlanGQLModel instanci
    instance = object.__new__(PlanGQLModel)
    instance.semester_id = UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")

    class Info: pass
    result = await instance.semester(Info())

    AcSemesterGQLModel.resolve_reference.assert_awaited_once_with(id=instance.semester_id)
    assert result == "mock-semester"

from unittest.mock import AsyncMock, patch
from uuid import UUID
import pytest

@pytest.mark.asyncio
async def test_plan_event_returns_resolved_object_or_none():
    from src.GraphTypeDefinitions.PlanGQLModel import PlanGQLModel

    class Info: pass

    # ➤ Test 1: event_id is None
    instance_none = object.__new__(PlanGQLModel)
    instance_none.event_id = None
    assert await instance_none.event(Info()) is None

    # ➤ Test 2: event_id exists
    instance = object.__new__(PlanGQLModel)
    instance.event_id = UUID("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb")

    # ➤ Patch uvnitř resolveru
    with patch("src.GraphTypeDefinitions.PlanGQLModel.EventGQLModel") as MockEvent:
        MockEvent.resolve_reference = AsyncMock(return_value="mock-event")
        result = await instance.event(Info())

    assert result == "mock-event"
    MockEvent.resolve_reference.assert_awaited_once_with(instance.event_id)

from unittest.mock import AsyncMock, ANY

@pytest.mark.asyncio
async def test_plan_page_executes_loader_page():
    from src.GraphTypeDefinitions.PlanGQLModel import plan_page

    mock_loader = AsyncMock()
    mock_loader.page = AsyncMock(return_value="mocked-result")

    class MockAll:
        plans = mock_loader

    class Info:
        context = {"loaders": MockAll()}

    result = await plan_page.base_resolver(None, Info(), skip=0, limit=10, where=None)

    assert result == "mocked-result"
    mock_loader.page.assert_awaited_once_with(
        skip=0,
        limit=10,
        where=None,
        orderby=ANY,
        desc=ANY,
        extendedfilter=ANY
    )

@pytest.mark.asyncio
async def test_plan_result_gqlmodel_plan():
    from src.GraphTypeDefinitions.PlanGQLModel import PlanGQLModel, PlanResultGQLModel as ConcreteClass
    from uuid import UUID
    from unittest.mock import AsyncMock

    # Mock metoda resolve_reference
    PlanGQLModel.resolve_reference = AsyncMock(return_value="mocked-plan")

    # ⬅ Stejná instance info
    info = type("Info", (), {})()

    instance = ConcreteClass()
    instance.id = UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")

    result = await instance.plan(info)

    assert result == "mocked-plan"
    PlanGQLModel.resolve_reference.assert_awaited_once_with(info, instance.id)
