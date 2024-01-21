import strawberry
import uuid

@classmethod
async def resolve_reference(cls, info: strawberry.types.Info, id: uuid.UUID):
    return cls(id=id)

class BaseEternal:
    id: uuid.UUID = strawberry.federation.field(external=True)
    


