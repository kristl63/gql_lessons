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
test_plan_by_id = createByIdTest2(tableName="plans", variables={"id": "f2e9996c-2cca-42d9-93ec-660baf6f95b9"})
test_plan_update = createUpdateTest2(tableName="plans", variables={"name": "updated plan name", "id": "f2e9996c-2cca-42d9-93ec-660baf6f95b9","lastchange":"2024-08-11T21:45:06.685651"})
test_plan_create = createTest2(tableName="plans", queryName="create", variables={"name": "new plan", "semesterId": "b888524e-ab80-4078-b457-841cafbfb325", "mastereventId": "3e52a301-caad-46ba-8fe6-1a7e2f370866","lastchange":"2024-08-11T21:45:06.685651"})
test_plan_delete = createDeleteTest2(tableName="plans", variables={"name": "new plan", "semesterId": "b888524e-ab80-4078-b457-841cafbfb325", "mastereventId": "3e52a301-caad-46ba-8fe6-1a7e2f370866", "lastchange":"2024-08-11T21:45:06.685651"})

# Test for PlannedLessons
test_planned_lesson_by_id = createByIdTest2(tableName="plannedLessons", variables={"id": "18375c23-767c-4c1e-adb6-9b2beb463533"})
test_planned_lesson_update = createUpdateTest2(tableName="plannedLessons", variables={"name": "updated lesson name", "id": "18375c23-767c-4c1e-adb6-9b2beb463533"})
test_planned_lesson_create = createTest2(tableName="plannedLessons", queryName="create", variables={"name": "new lesson", "semesterId": "b888524e-ab80-4078-b457-841cafbfb325", "mastereventId": "3e52a301-caad-46ba-8fe6-1a7e2f370866"})
test_planned_lesson_delete = createDeleteTest2(tableName="plannedLessons", variables={"id": "18375c23-767c-4c1e-adb6-9b2beb463533", "name": "new lesson"})