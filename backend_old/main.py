from fastapi import FastAPI, HTTPException, Path
from sqlalchemy import create_engine, text
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from hashlib import sha256
from typing import List
from backend_old.schemas import (
    Info, Integrity
)
from backend_old.models import (
    info,Base, integrity
) 

app = FastAPI()

db_user = "monitoring_user"
db_pass = "isis2405"
db_host = "10.128.0.2"
db_port = "5432"
db_name = "monitoring_db"


 
engine = create_engine(
    f"postgresql+psycopg://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}", echo=True
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# GET 
@app.get("/health")
def healthCheck():
    return [] 


# GET ALL
@app.get("/info", response_model=List[Info])
def getInfos():
    with engine.connect() as c:
        result = c.execute(text("SELECT * FROM INFOs"))
        return result.all()

@app.get("/integrity", response_model=List[Integrity])
def getInts():
    with engine.connect() as c:
        result = c.execute(text("SELECT * FROM INTEGRITY"))
        return result.all()

# GET ONE
@app.get("/integrity/{id}", response_model=Integrity)
def getInt(id: int):
    with engine.connect() as c:
        stmt = integrity.select().where(integrity.c.id == id)
        result = c.execute(stmt).fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="Client not found")
        
        return result
@app.get("/info/{id}", response_model=Info)
def getInfo(id: int):
    with engine.connect() as c:
        stmt = info.select().where(info.c.id == id)
        result = c.execute(stmt).fetchone()
        
        if result is None:
            raise HTTPException(status_code=404, detail="Client not found")
       
        sha256((result[1]+str(result[2])+str(result[3])+str(result[4])).encode('utf-8')).hexdigest()
        return result
    
@app.get("/compare/{id}")
def compare(id: int):
    with engine.connect() as c:
        stmt = integrity.select().where(integrity.c.id == id)
        result2 = c.execute(stmt).fetchone()
        
        stmt = info.select().where(info.c.id == id)
        result = c.execute(stmt).fetchone()
        if result is None or result2 is None:
            raise HTTPException(status_code=404, detail="Client not found")
        
        if (result2[1] == sha256((result[1]+str(result[2])+str(result[3])+str(result[4])).encode('utf-8')).hexdigest()):
            return {"message": "No se ha derectado ningun cambio reciente"}
        else:
            return {"message": "Se ha derectado ningun cambio reciente"}

# POS
@app.post("/info")
def addClient(client: Info):
    clientD = {
        "id": client.id,
        "trabajo": client.trabajo,
        "ingresos": client.ingresos,
        "deudas": client.deudas,
        "credito": client.credito
    }
    with engine.connect() as c:
        try:
            getInfo(client.id)
            return "Cannot create client info, already exists"
        except HTTPException as e:
            c.execute(info.insert().values(clientD))
            addInt(client)
            c.commit()
            return clientD


def addInt(client: Info):
    clientD = {
        "id": client.id,
        "hash": sha256((client.trabajo + str(client.ingresos) + str(client.deudas)+ str(client.credito)).encode('utf-8')).hexdigest()
    }
    with engine.connect() as c:
        try:
            getInt(client.id)
            return "Cannot create client info, already exists"
        except HTTPException as e:
            c.execute(integrity.insert().values(clientD))
            c.commit()
            return clientD


# UPDATE
@app.put("/info/{id}")
def updateInfo(id: int, client: Info):
    clientD = {
        "trabajo": client.trabajo,
        "ingresos": client.ingresos,
        "deudas": client.deudas,
        "credito": client.credito
    }
    with engine.connect() as c:
        try:
            getInfo(id)
            updateHash(id,clientD)
            c.execute(info.update().where(info.c.id == id).values(**clientD))
            c.commit()
            return clientD
        except HTTPException as e:
            return "Client does not exist"

@app.put("/attack/{id}")
def updateAttack(id: int, client: Info):
    clientD = {
        "trabajo": client.trabajo,
        "ingresos": client.ingresos,
        "deudas": client.deudas,
        "credito": client.credito
    }
    with engine.connect() as c:
        try:
            getInfo(id)
            c.execute(info.update().where(info.c.id == id).values(**clientD))
            c.commit()
            return clientD
        except HTTPException as e:
            return "Client does not exist"

def updateHash(id,client: Info):
    clientD = {
        "id": id,
        "hash": sha256((client['trabajo'] + str(client['ingresos']) + str(client['deudas'])+ str(client['credito'])).encode('utf-8')).hexdigest()
    }
    with engine.connect() as c:
        try:
            c.execute(integrity.update().where(info.c.id==id).values(**clientD))
            c.commit()
            return clientD
            
        except HTTPException as e:
            
            return "Cannot create client info, already exists"

# DELETE


@app.delete("/info/{id}")
def deteleInfo(id: int):
    with engine.connect() as c:
        stmt = info.delete().where(info.c.id == id)
        result = c.execute(stmt)
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Client not found")
        c.commit()
        return {"message": "Client deleted successfully"}


@app.get("/")
def root():
    with engine.connect() as c:
        postgresql_version = c.execute(text("SELECT version()")).fetchone()[0]
        return ["Hello world", {"postgres_version": postgresql_version}]
