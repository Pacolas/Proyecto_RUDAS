from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Time,
    Table,
    Date,
    ForeignKey,
    Integer,
    Float,
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()



info = Table(
    "infos",
    Base.metadata,
    Column("id", BigInteger(), primary_key=True, index=True),
    Column("trabajo", String(), index=True),
    Column("ingresos", Float()),
    Column("deudas", Float()),
    Column("credito", Float()),
)

integrity  = Table(
    "integrity",
    Base.metadata,
    Column("id", BigInteger(), primary_key=True, index=True),
    Column("hash", String(), index=True),)
