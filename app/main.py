from fastapi import FastAPI , status
from app.routers import auth , get_access_by_refresh_token as obtain_access_router , admin




app = FastAPI()
app.include_router(auth.auth_routes)
app.include_router(obtain_access_router.access_router)
app.include_router(admin.admin_routes)




@app.get('/health',status_code=status.HTTP_200_OK)
def helth_check() -> dict:
    return {"status" : "I am healthy"}