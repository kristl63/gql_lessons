import strawberry
import typing
import asyncio
import uuid
from typing import Annotated, List

@strawberry.federation.type(extend=True, keys=["id"])
class AcTopicGQLModel:

    id: uuid.UUID = strawberry.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: uuid.UUID):
        return AcTopicGQLModel(id=id)