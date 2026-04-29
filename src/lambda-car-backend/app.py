from fastapi import FastAPI

from settings import load_settings

from routers.auth.auth_router import router as auth_router
from routers.auth.admin_auth_router import router as admin_auth_router

from routers.user.admin_user_router import router as admin_user_router
from routers.car.admin_car_router import router as admin_car_router
from routers.commit.admin_commit_router import router as admin_commit_router

from routers.trip.trip_router import router as trip_router
from routers.refueling.refueling_router import router as refueling_router


settings = load_settings()

app = FastAPI(
    title="LambdaCar Backend",
    version="1.0.0",
)

app.include_router(auth_router, prefix=settings.api_prefix)
app.include_router(admin_auth_router, prefix=settings.api_prefix)

app.include_router(admin_user_router, prefix=settings.api_prefix)
app.include_router(admin_car_router, prefix=settings.api_prefix)
app.include_router(admin_commit_router, prefix=settings.api_prefix)

app.include_router(trip_router, prefix=settings.api_prefix)
app.include_router(refueling_router, prefix=settings.api_prefix)


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}