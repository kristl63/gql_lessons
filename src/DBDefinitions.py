import sqlalchemy
import datetime

from sqlalchemy import (
    Column,
    String,
    BigInteger,
    Integer,
    DateTime,
    ForeignKey,
    Sequence,
    Table,
    Boolean,
)
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
import uuid

BaseModel = declarative_base()

from uuid import uuid4, UUID
from sqlalchemy import Column, Uuid
uuid = uuid4

def UUIDFKey(comment=None, nullable=True, **kwargs):
    return Column(Uuid, index=True, comment=comment, nullable=nullable, **kwargs)

def UUIDColumn():
    return Column(Uuid, primary_key=True, comment="primary key", default=uuid)

# id = Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"),)

###########################################################################################################################
#
# zde definujte sve SQLAlchemy modely
# je-li treba, muzete definovat modely obsahujici jen id polozku, na ktere se budete odkazovat
#
###########################################################################################################################

class PlanModel(BaseModel):
    """Defines a lesson which is going to be planned in timetable"""

    __tablename__ = "plans"

    id = UUIDColumn()
    name = Column(String, comment="Name of the plan")#<-- toto!
    # neni nadbytecne, topic_id muze byt null, pak je nutne mit semester_id, jedna-li se o akreditovanou vyuku
    semester_id = UUIDFKey(nullable=True)#Column(ForeignKey("acsemesters.id"), index=True, nullable=True)
    masterevent_id = UUIDFKey(nullable=True)#Column(ForeignKey("acsemesters.id"), index=True, nullable=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    rbacobject = UUIDFKey(nullable=True, comment="id rbacobject")#Column(ForeignKey("users.id"), index=True, nullable=True)

class PlannedLessonModel(BaseModel):
    """Defines a lesson which is going to be planned in timetable"""

    __tablename__ = "plan_lessons"

    id = UUIDColumn()
    name = Column(String)
    order = Column(Integer, default=lambda:1)
    length = Column(Integer)
    startproposal = Column(DateTime)
    plan_id = Column(ForeignKey("plans.id"), index=True, nullable=True)

    linkedlesson_id = Column(ForeignKey("plan_lessons.id"), index=True, nullable=True)
    topic_id = UUIDFKey(nullable=True)#Column(ForeignKey("actopics.id"), index=True, nullable=True)
    lessontype_id = UUIDFKey(nullable=True)#Column(ForeignKey("aclessontypes.id"), index=True)

    # neni nadbytecne, topic_id muze byt null, pak je nutne mit semester_id, jedna-li se o akreditovanou vyuku
    semester_id = UUIDFKey(nullable=True)#Column(ForeignKey("acsemesters.id"), index=True, nullable=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    rbacobject = UUIDFKey(nullable=True, comment="id rbacobject")#Column(ForeignKey("users.id"), index=True, nullable=True)

    event_id = UUIDFKey(nullable=True)#Column(ForeignKey("events.id"), index=True, nullable=True)
    users = relationship("UserPlanModel", back_populates="plan", uselist=True)
    facilities = relationship("FacilityPlanModel", back_populates="plan", uselist=True)
    groups = relationship("GroupPlanModel", back_populates="plan", uselist=True)

class UserPlanModel(BaseModel):
    __tablename__ = "plan_lessons_users"

    id = UUIDColumn()
    user_id = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True)
    planlesson_id = Column(ForeignKey("plan_lessons.id"), index=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    rbacobject = UUIDFKey(nullable=True, comment="id rbacobject")#Column(ForeignKey("users.id"), index=True, nullable=True)

    plan = relationship("PlannedLessonModel", back_populates="users", uselist=False)

class GroupPlanModel(BaseModel):
    __tablename__ = "plan_lessons_groups"

    id = UUIDColumn()
    group_id = UUIDFKey(nullable=True)#Column(ForeignKey("groups.id"), index=True)
    planlesson_id = Column(ForeignKey("plan_lessons.id"), index=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    rbacobject = UUIDFKey(nullable=True, comment="id rbacobject")#Column(ForeignKey("users.id"), index=True, nullable=True)

    plan = relationship("PlannedLessonModel", back_populates="groups", uselist=False)

class FacilityPlanModel(BaseModel):
    __tablename__ = "plan_lessons_facilities"

    id = UUIDColumn()
    facility_id = UUIDFKey(nullable=True)#Column(ForeignKey("facilities.id"), index=True)
    planlesson_id = Column(ForeignKey("plan_lessons.id"), index=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    rbacobject = UUIDFKey(nullable=True, comment="id rbacobject")#Column(ForeignKey("users.id"), index=True, nullable=True)

    plan = relationship("PlannedLessonModel", back_populates="facilities", uselist=False)

###########################################################

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine


async def startEngine(connectionstring, makeDrop=False, makeUp=True):
    """Provede nezbytne ukony a vrati asynchronni SessionMaker"""
    asyncEngine = create_async_engine(connectionstring)

    async with asyncEngine.begin() as conn:
        if makeDrop:
            await conn.run_sync(BaseModel.metadata.drop_all)
            print("BaseModel.metadata.drop_all finished")
        if makeUp:
            await conn.run_sync(BaseModel.metadata.create_all)
            print("BaseModel.metadata.create_all finished")

    async_sessionMaker = sessionmaker(
        asyncEngine, expire_on_commit=False, class_=AsyncSession
    )
    return async_sessionMaker


import os


def ComposeConnectionString():
    """Odvozuje connectionString z promennych prostredi (nebo z Docker Envs, coz je fakticky totez).
    Lze predelat na napr. konfiguracni file.
    """
    user = os.environ.get("POSTGRES_USER", "postgres")
    password = os.environ.get("POSTGRES_PASSWORD", "example")
    database = os.environ.get("POSTGRES_DB", "data")
    hostWithPort = os.environ.get("POSTGRES_HOST", "localhost:5432")
    #hostWithPort = os.environ.get("POSTGRES_HOST", "host.docker.internal:5432")

    driver = "postgresql+asyncpg"  # "postgresql+psycopg2"
    connectionstring = f"{driver}://{user}:{password}@{hostWithPort}/{database}"
    connectionstring = os.environ.get("CONNECTION_STRING", connectionstring)

    return connectionstring
