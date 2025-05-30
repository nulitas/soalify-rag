import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import run_in_threadpool
 
from var import URL_PATH
import models
import routers
from database_seeder import seed_database
from database import engine, get_db
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[URL_PATH],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("data", exist_ok=True)

app.include_router(routers.users_router)
app.include_router(routers.tags_router)
app.include_router(routers.packages_router)
app.include_router(routers.rag_router)
app.include_router(routers.questions_router)


@app.on_event("startup")
async def startup_event():
    db = next(get_db())
    try:
        await run_in_threadpool(seed_database, db)
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)