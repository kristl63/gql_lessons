import strawberry
import dataclasses
import datetime

from typing import List, Optional
from ._GraphResolvers import IDType
from uoishelpers.resolvers import createInputs

@classmethod
async def resolve_reference(cls, info: strawberry.types.Info, id: IDType):
    return cls(id=id)

from ._GraphResolvers import (
    getLoadersFromInfo, 
    )
@strawberry.federation.type(extend=True, keys=["id"])
class RBACObjectGQLModel:
    id: IDType = strawberry.federation.field(external=True)
    resolve_reference = resolve_reference

    @classmethod
    async def resolve_roles(cls, info: strawberry.types.Info, id: IDType):
        loader = getLoadersFromInfo(info).authorizations
        authorizedroles = await loader.load(id)
        return authorizedroles

    # @classmethod
    # async def resolve_all_roles(cls, info: strawberry.types.Info):
    #     return []
    

    
# @strawberry.federation.type(extend=True, keys=["id"])
# class GroupGQLModel:
#     id: IDType = strawberry.federation.field(external=True)

#     @classmethod
#     async def resolve_reference(cls, id: IDType):
#         return GroupGQLModel(id=id)  # jestlize rozsirujete, musi byt tento vyraz

#     async def program(
#         self, info: strawberry.types.Info
#     ) -> Union["AcProgramGQLModel", None]:
#         async with withInfo(info) as session:
#             result = await resolveProgramForGroup(session, id)
#             return result


# @strawberry.federation.type(extend=True, keys=["id"])
# class UserGQLModel:
#     id: IDType = strawberry.federation.field(external=True)

#     @classmethod
#     async def resolve_reference(cls, id: IDType):
#         return UserGQLModel(id=id)  # jestlize rozsirujete, musi byt tento vyraz

# #     zde je rozsireni o dalsi resolvery
# #     @strawberry.field(description="""Inner id""")
# #     async def external_ids(self, info: strawberry.types.Info) -> List['ExternalIdGQLModel']:
# #         result = await resolveExternalIds(session,self.id)
# #         return result

    
#     @strawberry.field(description="""List of programs which the user is studying""")
#     async def study_programs(self, info: strawberry.types.Info) -> List['AcProgramGQLModel']:
#         loader = getLoadersFromInfo(info).programstudents
#         result = await loader.filter_by(student_id=self.id)       
#         return result
    
#     @strawberry.field(description="""List of programs which the user is studying""")
#     async def classifications(self, info: strawberry.types.Info) -> List['AcClassificationGQLModel']:
#         loader = getLoadersFromInfo(info).classifications
#         result = await loader.filter_by(user_id=self.id)       
#         return result
    
