from fastapi import FastAPI, status, Request, Depends
from contextlib import asynccontextmanager
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
import redis.asyncio as redis
import os

from app.routes import (
    auth,
    get_access_by_refresh_token as obtain_access_router,
    admin,
    trash,
    profile,
    upload_profile_s3,
)


from dotenv import load_dotenv

load_dotenv(".env")

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_connection = redis.from_url(
        f"redis://{REDIS_HOST}:{REDIS_PORT}", encoding="utf-8", decode_responses=True
    )
    await FastAPILimiter.init(redis_connection)

    yield


app = FastAPI(lifespan=lifespan)


app.include_router(auth.auth_routes)
app.include_router(obtain_access_router.access_routes)
app.include_router(admin.admin_routes)
app.include_router(trash.trash_routes)
app.include_router(profile.profile_routes)
app.include_router(upload_profile_s3.profile_upolad_s3)


@app.get(
    "/health",
    dependencies=[Depends(RateLimiter(times=10, seconds=10))],
    status_code=status.HTTP_200_OK,
)
def helth_check(request: Request) -> dict:
    return {"status": "I am healthy"}
