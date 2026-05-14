from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.lifespan import lifespan
from app.routers.vehicle_raw import router as vehicle_raw_router
from app.routers.vehicles import router as vehicles_router
from app.routers.recommender import router as recommender_router
from app.routers.axes_ratings import router as axes_ratings_router
from app.routers.auth import router as auth_router

app = FastAPI(debug=True, lifespan=lifespan)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(axes_ratings_router)
app.include_router(recommender_router)
app.include_router(vehicles_router)
app.include_router(vehicle_raw_router)

@app.get("/ping")
def ping():
    return {"status": "ok"}
