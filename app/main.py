import os
from time import time

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.core.deps import create_all_tables
from app.models.models import Base
from app.routes.book_operations import router as book_router
from app.routes.recommendations import router as reco_router
from app.routes.review_operations import router as review_router
from app.routes.summary import router as summary_router
from app.routes.user import router as user_router

APP_TITLE = "Intelligent Book Management System"
DEBUG = os.environ.get("DEBUG", True)
CORS_MIDDLEWARE_KWARGS = {
    "allow_origins": ["*"],
    "allow_credentials": True,
    "allow_methods": ["*"],
    "allow_headers": ["*"],
}


app = FastAPI(title=APP_TITLE, debug=DEBUG)
app.add_middleware(CORSMiddleware, **CORS_MIDDLEWARE_KWARGS)


@app.on_event("startup")
def print_logs():
    print("Book-ms app starting up.")


@app.on_event("startup")
async def start_up():
    await create_all_tables()


@app.middleware("http")
async def add_process_header_time(request: Request, call_next):
    start = time()
    response = await call_next(request)
    process_time = time() - start
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get("/health")
async def health():
    return {"message": "App Up & Running."}


for route in (user_router, book_router, review_router, summary_router, reco_router):
    app.include_router(route)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, workers=3)
