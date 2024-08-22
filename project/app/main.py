# import os

# from fastapi import FastAPI, Depends
# from tortoise.contrib.fastapi import register_tortoise # type: ignore

# from app.config import get_settings, Settings

# app = FastAPI()
# # print("DATABASE_URL:", os.environ.get("DATABASE_URL"))

# register_tortoise(
#     app,
#     db_url=os.environ.get("DATABASE_URL"),
#     modules={"models": ["app.models.tortoise"]},
#     generate_schemas=False,
#     add_exception_handlers=True,
# )

# @app.get("/ping")
# async def pong(settings: Settings = Depends(get_settings)):
#     return {
#             "ping": "pong!",
#             "environment": settings.environment,
#             "testing": settings.testing
#         }
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from tortoise import Tortoise

from app.api import ping, summaries


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await Tortoise.init(
        db_url=os.environ.get("DATABASE_URL"),
        modules={"models": ["app.models.tortoise"]},
    )
    # We're not generating schemas here as your original code had generate_schemas=False
    # If you need to generate schemas, uncomment the following line:
    # await Tortoise.generate_schemas()

    yield

    # Shutdown
    await Tortoise.close_connections()


def create_application() -> FastAPI:
    application = FastAPI(lifespan=lifespan)
    # application = FastAPI()

    application.include_router(ping.router)
    application.include_router(
        summaries.router, prefix="/summaries", tags=["summaries"]
    )  # new

    return application


app = create_application()

# The exception handlers will be added automatically by FastAPI
# If you need custom exception handling, you can add it here
