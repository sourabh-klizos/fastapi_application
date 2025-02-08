from fastapi import FastAPI 


app = FastAPI()



@app.get('/helth')
def helth_check() -> dict:
    return {"status" : "I am healthy"}