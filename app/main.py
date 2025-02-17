from fastapi import FastAPI, status
from app.routes import (
    auth,
    get_access_by_refresh_token as obtain_access_router,
    admin,
    trash,
    profile,
)


from dotenv import load_dotenv


app = FastAPI()
load_dotenv(".env")


app.include_router(auth.auth_routes)
app.include_router(obtain_access_router.access_routes)
app.include_router(admin.admin_routes)
app.include_router(trash.trash_routes)
app.include_router(profile.profile_routes)


@app.get("/health", status_code=status.HTTP_200_OK)
def helth_check() -> dict:
    return {"status": "I am healthy"}
