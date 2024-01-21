import pytest


@pytest.mark.asyncio
async def test_FillDataViaGQL(DemoFalse, FillDataViaGQL, ClientExecutorAdmin, DemoData):
    return
    # for tableName, ops in queries.items():
    #     table = DemoData.get(tableName, None)
    #     assert table is not None, f"Missing {tableName} in DemoData source"
    #     readQuery = ops.get("read", None)
    #     assert readQuery is not None, f"missing read op on table {tableName}"
    #     createQuery = ops.get("create", None)
    #     assert createQuery is not None, f"missing create op on table {tableName}"

    #     for row in table:
    #         rowid = row.get("id", None)
    #         assert rowid is not None, f"missing id key somewhere in table {tableName}"

    #         variables = {**rowid}
    #         resp = await ClientExecutorAdmin(query=readQuery, variable_values=variables)
    #         result = resp["data"]["result"]
    #         if result:
    #             continue

    #         # row does not exists
    #         variables = {**rowid}
    #         resp = await ClientExecutorAdmin(query=createQuery, variable_values=variables)


