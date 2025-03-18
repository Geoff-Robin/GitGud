from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from dotenv import load_dotenv
import os
from motor.motor_asyncio import AsyncIOMotorClient
from routes.routes import router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import traceback

@asynccontextmanager
async def db_lifespan(app: FastAPI):
    load_dotenv()
    try:
        MONGO_DB_USERNAME = os.getenv("MONGO_DB_USERNAME")
        MONGO_DB_PASSWORD = os.getenv("MONGO_DB_PASSWORD")
        uri = f"mongodb+srv://{MONGO_DB_USERNAME}:{MONGO_DB_PASSWORD}@cluster0.and0a.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        app.mongodb_client = AsyncIOMotorClient(uri)
        app.database = app.mongodb_client["GitGud"]
        ping_response = await app.database.command("ping")
        if int(ping_response["ok"]) != 1:
            raise Exception("Problem connecting to database cluster.")
        else:
            print("✅ Connected to the database cluster.")
    except Exception as e:
        print(e)

    yield

    app.mongodb_client.close()


app: FastAPI = FastAPI(lifespan=db_lifespan,debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router=router)

if __name__ == "__main__" :
    import uvicorn
    uvicorn.run(app,port = 4000)