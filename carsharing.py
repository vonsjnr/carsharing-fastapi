import uvicorn
from fastapi import FastAPI, Request
from sqlmodel import SQLModel

from db import engine
from schemas import load_db
from routers import cars as crs
from routers import web, auth

app = FastAPI(title="Car Sharing")
app.include_router(crs.router)
app.include_router(web.router)
app.include_router(auth.router)


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

'''
@app.middleware("http")
async def add_cars_cookie(request: Request, call_next):
    response = await call_next(request)
    response.set_cookie(key="cars_cookie", value="you_visited_the_carsharing_app")
    return response'''

if __name__ == "__main__":
    uvicorn.run("carsharing:app", reload=True)
