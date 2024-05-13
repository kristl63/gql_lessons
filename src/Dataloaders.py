import datetime
import aiohttp
import asyncio
import os
import uuid
from functools import cache
from aiodataloader import DataLoader
import logging
from uoishelpers.dataloaders import createIdLoader

from src.DBDefinitions import (
    BaseModel,
    PlanModel,
    PlannedLessonModel,
    UserPlanModel,
    GroupPlanModel,
    FacilityPlanModel
)

# dbmodels = {
#     "psps": PlanModel,
#     "plans": PlannedLessonModel,
#     "userplans": UserPlanModel,
#     "groupplans": GroupPlanModel,
#     "facilityplans": FacilityPlanModel
# }

# def createLoaders(asyncSessionMaker, models=dbmodels):
#     def createLambda(loaderName, DBModel):
#         return lambda self: createIdLoader(asyncSessionMaker, DBModel)
    
#     attrs = {}
#     for key, DBModel in models.items():
#         attrs[key] = property(cache(createLambda(key, DBModel)))
    
#     Loaders = type('Loaders', (), attrs)   
#     return Loaders()

# from functools import cache

# def createLoadersContext(asyncSessionMaker):
#     return {
#         "loaders": createLoaders(asyncSessionMaker)
#     }

def createLoaders(asyncSessionMaker):
    @cache
    def createModelDict():
        result = {}
        for DBModel in BaseModel.registry.mappers:
            table = DBModel.class_
            result[table.__tablename__] = table
            result[table.__name__] = table
        return result

    def createLambda(loaderName, DBModel):
        return lambda self: createIdLoader(asyncSessionMaker, DBModel)

    modelDict = createModelDict()    
    attrs = {}

    for tableName, DBModel in modelDict.items():
        attrs[tableName] = property(cache(createLambda(asyncSessionMaker, DBModel)))
        # print(tableName, DBModel)

    
    # attrs["authorizations"] = property(cache(lambda self: AuthorizationLoader()))
    Loaders = type('Loaders', (), attrs)   
    return Loaders()


def getUserFromInfo(info):
    context = info.context
    #print(list(context.keys()))
    result = context.get("user", None)
    if result is None:
        request = context.get("request", None)
        assert request is not None, context
        result = request.scope["user"]

    if result is None:
        result = {"id": None}
    else:
        result = {**result, "id": uuid.UUID(result["id"])}
    # logging.debug("getUserFromInfo", result)
    return result

def getLoadersFromInfo(info):
    # print("info", info)
    context = info.context
    # print("context", context)
    loaders = context.get("loaders", None)
    assert loaders is not None, f"'loaders' key missing in context"
    return loaders



def createLoadersContext(asyncSessionMaker):
    return {
        "loaders": createLoaders(asyncSessionMaker)
    }


print(createLoaders(None))