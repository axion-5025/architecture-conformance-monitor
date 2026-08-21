from typing import Final

from fastapi import FastAPI
from pydantic import BaseModel

SERVICE_NAME: Final[str] = "inventory-service"
SERVICE_VERSION: Final[str] = "0.1.0"


class HealthResponse(BaseModel):
    service: str
    version: str
    status: str


app = FastAPI(
    title="Inventory Service",
    description="Manages product inventory in the sample microservice system.",
    version=SERVICE_VERSION,
)


@app.get("/", tags=["General"])
async def root() -> dict[str, str]:
    return {
        "message": "Inventory Service is running",
        "documentation": "/docs",
    }


@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["Health"],
)
async def health_check() -> HealthResponse:
    return HealthResponse(
        service=SERVICE_NAME,
        version=SERVICE_VERSION,
        status="healthy",
    )
