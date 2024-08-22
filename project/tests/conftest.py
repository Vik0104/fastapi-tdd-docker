import asyncio
import os
from contextlib import asynccontextmanager

import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient
from tortoise import Tortoise

from app.config import Settings, get_settings
from app.main import create_application  # updated


def get_settings_override():
    return Settings(testing=1, database_url=os.environ.get("DATABASE_TEST_URL"))


@pytest.fixture(scope="module")
def test_app():
    # set up
    app = create_application()  # new
    app.dependency_overrides[get_settings] = get_settings_override
    with TestClient(app) as test_client:  # updated
        # testing
        yield test_client

    # tear down


@asynccontextmanager
async def override_lifespan(app: FastAPI):
    await Tortoise.init(
        db_url=os.environ.get("DATABASE_TEST_URL"),
        modules={"models": ["app.models.tortoise"]},
    )
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()


@pytest.fixture(scope="module")
def test_app_with_db():
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override

    # Override the lifespan
    app.router.lifespan_context = override_lifespan

    # Create a test client
    with TestClient(app) as test_client:
        # Run the lifespan events
        asyncio.run(app.router.startup())

        yield test_client

        # Run the shutdown events
        asyncio.run(app.router.shutdown())
