from fastapi import FastAPI 
from app.routers.auth_router import auth_routes


app = FastAPI()
app.include_router(auth_routes)




@app.get('/health')
def helth_check() -> dict:
    return {"status" : "I am healthy"}