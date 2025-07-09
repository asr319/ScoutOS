from fastapi import FastAPI
from .endpoints import router as api_router
from .background_tasks import start_background_tasks

app = FastAPI()

app.include_router(api_router)


@app.on_event("startup")
async def startup_event():
    await start_background_tasks()


@app.get("/health")
async def health_check():
    return {"status": "ok"}
