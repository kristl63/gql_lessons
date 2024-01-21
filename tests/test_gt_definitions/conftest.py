import time
import logging
import datetime
import pytest_asyncio
import uuid

queries = {
    "acprograms": {
        "read": """query($id: UUID!){ result: planById(id: $id) { id } }""",
        "readext": """query($id: UUID!){ 
          result: acProgramById(id: $id) { 
            id type { id } subjects {id } students { id } grantsGroup { id } licencedGroup { id }
          } }""",
        "readp": """query($skip: Int, $limit: Int){ result: Page(skip: $skip, limit: $limit) { id } }""",
        "create": """mutation ($id: UUID!, $name: String!, $type_id: UUID!, $group_id: UUID!, $licenced_group_id: UUID!) {
        result: programInsert(program: {id: $id, name: $name, typeId: $type_id, groupId: $group_id, licencedGroupId: $licenced_group_id}) {
            id
            msg
            result: program {
                id
                name
                nameEn
                type { id }
                subjects { id }
                students { id }
                grantsGroup { id }
                licencedGroup { id }
                createdby { id }
                changedby { id }
                rbacobject { id }
            }
        }
    }"""
    }, 
    "acclassifications": {
        "read": """query($id: UUID!){ result: acClassificationById(id: $id) { id } }""",
        "readext": """query($id: UUID!){ 
          result: acClassificationById(id: $id) { 
            id date order student { id } semester { id } level { id }
          }}""",
        "readp": """query($skip: Int, $limit: Int){ result: acClassificationPage(skip: $skip, limit: $limit) { id } }""",
        "create": """mutation ($id: UUID!, $date: DateTime!, $order: Int!
            $student_id: UUID!, $semester_id: UUID! 
            $classificationlevel_id: UUID!
        ) {
        result: programClassificationInsert(classification: {
                id: $id, date: $date, order: $order
                studentId: $student_id, semesterId: $semester_id,
                classificationlevelId: $classificationlevel_id
            }) {
            id
            msg
            result: classification {
                id
                lastchange
                date
                order
                student { id }
                semester { id }
                level { id }
            }
        }
    }"""        
    },

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