from contextlib import asynccontextmanager
import sys
import os
import time
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from starlette.status import *
import uvicorn
from Database.database import db, create_database, engine
from Router import item, login, price
from dotenv import load_dotenv
create_database()

load_dotenv(".env")

# 스웨거 예시 표시
SWAGGER_HEADERS = {
    "title": "SWAGGER API REFERENCE",
    "version": "1.0.0",
    "description": "",}

# app = FastAPI()


# 스웨거 예시 표시
app = FastAPI(
    swagger_ui_parameters={
        "deepLinking": True,
        "displayRequestDuration": True,
        "docExpansion": "none",
        "operationsSorter": "method",
        "filter": True,
        "tagsSorter": "alpha",
        "syntaxHighlight.theme": "tomorrow-night",
    },
    **SWAGGER_HEADERS
)

app.include_router(item.router)
app.include_router(login.router)
app.include_router(price.router)

# CORS
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)