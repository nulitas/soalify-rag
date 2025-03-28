import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from var import URL_PATH
import models
import routers

from database import engine
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)