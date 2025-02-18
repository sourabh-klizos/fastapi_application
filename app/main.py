from fastapi import FastAPI, status, Request
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


app = FastAPI()


app.include_router(auth.auth_routes)
app.include_router(obtain_access_router.access_routes)
app.include_router(admin.admin_routes)
app.include_router(trash.trash_routes)
app.include_router(profile.profile_routes)
app.include_router(upload_profile_s3.profile_upolad_s3)


@app.get("/health", status_code=status.HTTP_200_OK)
def helth_check(request: Request) -> dict:
    return {"status": "I am healthy"}
