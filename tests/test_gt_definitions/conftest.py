import time
import logging
import datetime
import pytest_asyncio
import uuid

queries = {
    "plans": {
        "read": """query($id: UUID!){ result: planById(id: $id) { id } }""",
        "readext": """query($id: UUID!){ 
          result: planById(id: $id) {
                id name
                lessons { id } semester { id }
            } }""",
        "readp": """query($skip: Int, $limit: Int){ result: planPage(skip: $skip, limit: $limit) { id } }""",
        "create": """mutation createPlan($semester_id: UUID!, $masterevent_id: UUID!) {
            result: planInsert(plan: {semesterId: $semester_id, mastereventId: $masterevent_id}) {
                id
                msg
                plan {
                    id
                    lastchange
                }
            }
            }"""
    }, 
    "plan_lessons": {
        "read": """query($id: UUID!){ result: plannedLessonById(id: $id) { id } }""",
        "readext": """query($id: UUID!){ 
          result: plannedLessonById(id: $id) {
            id order name length
            type { id } users { id } facilities { id }
            groups { id } linkedTo { id } linkedWith { id }
        }}""",
        "readp": """query($skip: Int, $limit: Int){ result: plannedLessonPage(skip: $skip, limit: $limit) { id } }""",
        "create": """mutation createPlanItem($plan_id: UUID!, $name: String!) {
            result: plannedLessonInsert(lesson: {planId: $plan_id, name: $name}) {
                id
                msg
                lesson {
                id
                lastchange
                }
            }
            }"""        
    },
    "plan_lessons_users": {
        "read": "query($id: UUID!){ result: plannedLessonById(id: $id) { id } }",
        "readext": "query($id: UUID!){ result: plannedLessonById(id: $id) { id } }",
        "create": """mutation insertUser($id: UUID, $user_id: UUID!, $planlesson_id: UUID!) {
            result: plannedLessonUserInsert(userlesson: {id: $id, userId: $user_id, planlessonId: $planlesson_id}) {
                id
                msg
                lesson {
                    id
                }
            }
            }"""
    },
    "plan_lessons_groups": {
        "read": "query($id: UUID!){ result: plannedLessonById(id: $id) { id } }",
        "readext": "query($id: UUID!){ result: plannedLessonById(id: $id) { id } }",
        "create": """mutation insertGroup($id: UUID, $group_id: UUID!, $planlesson_id: UUID!) {
            result: plannedLessonGroupInsert(grouplesson: {id: $id, groupId: $group_id, planlessonId: $planlesson_id}) {
                id
                msg
                lesson {
                    id
                }
            }
            }"""
    },
    "plan_lessons_facilities": {
        "read": "query($id: UUID!){ result: plannedLessonById(id: $id) { id } }",
        "readext": "query($id: UUID!){ result: plannedLessonById(id: $id) { id } }",
        "create": """mutation insertFacility($id: UUID, $facility_id: UUID!, $planlesson_id: UUID!) {
            result: plannedLessonFacilityInsert(facilitylesson: {id: $id, facilityId: $facility_id, planlessonId: $planlesson_id}) {
                id
                msg
                lesson {
                    id
                }
            }
            }"""
    }

}
    


@pytest_asyncio.fixture
async def GQLInsertQueries():  
    return queries


@pytest_asyncio.fixture
async def FillDataViaGQL(DBModels, DemoData, GQLInsertQueries, ClientExecutorAdmin):

    start_time = time.time()
    queriesR = 0
    queriesW = 0
    

    types = [type(""), type(datetime.datetime.now()), type(uuid.uuid1())]
    for DBModel in DBModels:
        tablename = DBModel.__tablename__
        queryset = GQLInsertQueries.get(tablename, None)
        assert queryset is not None, f"missing queries for table {tablename}"
        table = DemoData.get(tablename, None)
        assert table is not None, f"{tablename} is missing in DemoData"

        readQuery = queryset.get("read", None)
        assert readQuery is not None, f"missing read op on table {tablename}"
        createQuery = queryset.get("create", None)
        assert createQuery is not None, f"missing create op on table {tablename}"

        for row in table:
            variable_values = {}
            for key, value in row.items():
                variable_values[key] = value
                if isinstance(value, datetime.datetime):
                    variable_values[key] = value.isoformat()
                elif type(value) in types:
                    variable_values[key] = f"{value}"

            # readResponse = await ClientExecutorAdmin(query=queryset["read"], variable_values=variable_values)
            readResponse = await ClientExecutorAdmin(query=queryset["readext"], variable_values=variable_values)
            queriesR = queriesR + 1
            if readResponse["data"]["result"] is not None:
                logging.info(f"row with id `{variable_values['id']}` already exists in `{tablename}`")
                continue
            insertResponse = await ClientExecutorAdmin(query=queryset["create"], variable_values=variable_values)
            assert insertResponse.get("errors", None) is None, insertResponse
            queriesW = queriesW + 1

        logging.info(f"{tablename} initialized via gql query")
    duration = time.time() - start_time
    logging.info(f"All WANTED tables are initialized in {duration}, total read queries {queriesR} and write queries {queriesW}")