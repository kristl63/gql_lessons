import datetime
import aiohttp
import asyncio
import os
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

def createLoadersContext(asyncSessionMaker):
    return {
        "loaders": createLoaders(asyncSessionMaker)
    }

print(createLoaders(None))