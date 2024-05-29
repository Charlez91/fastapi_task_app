from contextlib import asynccontextmanager

from fastapi import FastAPI

from utils.init_db import create_tables
from router.urls import router
#handlle routes

#adding lifespan event for performing task on app startup
@asynccontextmanager
async def lifespan(app:FastAPI):
    """
    Initializes the database tables when the application starts up.
    """
    #creates db tables on app startup
    create_tables()
    yield

app = FastAPI(
    debug=True, title="Task Management App", 
    description="""A Task Managment app built using FastAPI 
            and exposing CRUD RestAPI endpoints and a websocket for events""",
    lifespan= lifespan,
    version='1.0.0')


"""
@app.on_event("startup")#deprecated will use lifespan instead
def on_startup():
    '''
    Initializes the database tables when the application starts up.
    '''
    create_tables()
"""


app.include_router(router)