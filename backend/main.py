"""FastAPI application entrypoint.

Sets up CORS, health checks, and mounts product and analytics routers.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Local routers
from routers import products, analytics

app = FastAPI(title="Product Recommendation API", version="1.0.0")

origins = [
    # Development origins; keep permissive for local iteration
    "http://localhost:3000/",
    "http://localhost:3001/",
    "*",  # TODO: tighten CORS in production
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    """Basic service descriptor for quick smoke tests."""
    return {"message": "Product Recommendation API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    """Liveness probe endpoint."""
    return {"status": "healthy"}

app.include_router(products.router, prefix="/api/products", tags=["Products"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])

