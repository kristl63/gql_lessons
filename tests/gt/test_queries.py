import pytest
import logging
import uuid
import sqlalchemy
import json
import datetime

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
test_plan_by_id = createByIdTest2(tableName="plans")
test_plan_update = createUpdateTest2(tableName="plans", variables={"name": "updated plan name"})
test_plan_create = createTest2(tableName="plans", queryName="create", variables={"name": "new plan"})
test_plan_delete = createDeleteTest2(tableName="plans", variables={"id": "18375c23-767c-4c1e-adb6-9b2beb463533", "name": "new plan"})

# Test for PlannedLessons
test_planned_lesson_by_id = createByIdTest2(tableName="plannedLessons")
test_planned_lesson_update = createUpdateTest2(tableName="plannedLessons", variables={"name": "updated lesson name"})
test_planned_lesson_create = createTest2(tableName="plannedLessons", queryName="create", variables={"name": "new lesson"})
test_planned_lesson_delete = createDeleteTest2(tableName="plannedLessons", variables={"id": "18375c23-767c-4c1e-adb6-9b2beb463533", "name": "new lesson"})