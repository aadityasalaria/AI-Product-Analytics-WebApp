from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import products, analytics

app = FastAPI(title="Product Recommendation API", version="1.0.0")

origins = [
    "http://localhost:3000/",  # Next.js frontend
    "http://localhost:3001/",  # Alternative frontend port
    "*",  # Allow all origins for development
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define a root endpoint
@app.get("/")
async def read_root():
    return {"message": "Product Recommendation API", "version": "1.0.0"}

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Include routers
app.include_router(products.router, prefix="/api/products", tags=["Products"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
