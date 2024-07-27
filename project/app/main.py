from fastapi import FastAPI
from .database import init_db
from .routers import user_router , category_router

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await init_db()


app.include_router(user_router.router, prefix="/users", tags=["user"])
app.include_router(category_router.router, prefix="/categories", tags=["category"])