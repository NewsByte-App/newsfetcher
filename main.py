from routes.route import router
from fastapi import FastAPI

app = FastAPI()


app.include_router(router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
