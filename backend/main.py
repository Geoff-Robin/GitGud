from contextlib import asynccontextmanager
from fastapi import FastAPI
from dotenv import load_dotenv
import os
from motor.motor_asyncio import AsyncIOMotorClient
app = FastAPI()

@asynccontextmanager
async def db_lifespan(app: FastAPI):
    load_dotenv()
    MONGO_DB_USERNAME = os.getenv("MONGO_DB_USERNAME")
    MONGO_DB_PASSWORD = os.getenv("MONGO_DB_PASSWORD")
    uri = f"mongodb+srv://{MONGO_DB_USERNAME}:{MONGO_DB_PASSWORD}@cluster0.and0a.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    app.mongodb_client = AsyncIOMotorClient(uri)
    app.database = app.mongodb_client.get_default_database()
    ping_response = await app.database.command("ping")
    if int(ping_response["ok"]) != 1:
        raise Exception("Problem connecting to database cluster.")
    else:
        print("Connected to database cluster.")
    
    yield

    app.mongodb_client.close()


app: FastAPI = FastAPI(lifespan=db_lifespan)