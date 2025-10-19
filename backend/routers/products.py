"""Product API routes.

Handles dataset uploads, product retrieval, recommendations, and GenAI endpoints.
"""

import os
import json
from typing import List, Dict, Optional

from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Query, Depends
from pydantic import BaseModel

# Local services and dependencies
from core.dependencies import get_dataset_directory
from services.genai_service import genai_service
from services.product_service import product_service
from services.recommendation_service import recommendation_service

router = APIRouter()

# Pydantic models for request/response
class RecommendationRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5
    category_filter: Optional[str] = None
    price_min: Optional[float] = None
    price_max: Optional[float] = None

class ProductResponse(BaseModel):
    id: str
    name: str
    category: str
    price: float
    description: str
    image_url: Optional[str] = None
    similarity_score: Optional[float] = None
    recommendation_reason: Optional[str] = None

class GenerateDescriptionRequest(BaseModel):
    product_id: str
    enhance_existing: bool = False

class GenerateDescriptionResponse(BaseModel):
    product_id: str
    original_description: str
    generated_description: str
    enhancement_type: str

@router.post("/upload")
async def upload_dataset(
    file: UploadFile = File(...),
    dataset_dir: str = Depends(get_dataset_directory)
):
    """Upload and process a furniture dataset."""
    try:
        # Basic file type check; parse later according to extension
        if not file.filename.endswith(('.csv', '.json')):
            raise HTTPException(
                status_code=400,
                detail="Only CSV and JSON files are supported"
            )
        
        # Persist upload for downstream processing
        file_path = os.path.join(dataset_dir, file.filename)
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Load and process dataset
        products = product_service.load_dataset(file_path)
        
        # Store in Pinecone
        success = product_service.store_products_in_pinecone(products)
        
        if not success:
            raise HTTPException(
                status_code=500,
                detail="Failed to store products in vector database"
            )
        
        return {
            "message": "Dataset uploaded and processed successfully",
            "filename": file.filename,
            "products_processed": len(products),
            "file_path": file_path
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/all")
async def get_all_products(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    """Get all products with pagination."""
    try:
        products = product_service.get_all_products(limit=limit, offset=offset)
        return {
            "products": products,
            "total": len(products),
            "limit": limit,
            "offset": offset
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{product_id}")
async def get_product(product_id: str):
    """Get a specific product by ID."""
    try:
        product = product_service.get_product_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/recommend")
async def get_recommendations(request: RecommendationRequest):
    """Get product recommendations based on query and filters."""
    try:
        recommendations = recommendation_service.get_recommendations(
            query=request.query,
            top_k=request.top_k,
            category_filter=request.category_filter,
            price_min=request.price_min,
            price_max=request.price_max
        )
        
        return {
            "query": request.query,
            "recommendations": recommendations,
            "total": len(recommendations),
            "filters_applied": {
                "category": request.category_filter,
                "price_min": request.price_min,
                "price_max": request.price_max
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{product_id}/similar")
async def get_similar_products(
    product_id: str,
    top_k: int = Query(5, ge=1, le=20)
):
    """Get products similar to a specific product."""
    try:
        similar_products = recommendation_service.get_similar_products(
            product_id=product_id,
            top_k=top_k
        )
        
        return {
            "product_id": product_id,
            "similar_products": similar_products,
            "total": len(similar_products)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/category/{category}")
async def get_category_products(
    category: str,
    top_k: int = Query(10, ge=1, le=50),
    price_min: Optional[float] = Query(None),
    price_max: Optional[float] = Query(None)
):
    """Get products in a specific category."""
    try:
        products = recommendation_service.get_category_recommendations(
            category=category,
            top_k=top_k,
            price_min=price_min,
            price_max=price_max
        )
        
        return {
            "category": category,
            "products": products,
            "total": len(products),
            "filters": {
                "price_min": price_min,
                "price_max": price_max
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/trending")
async def get_trending_products(top_k: int = Query(10, ge=1, le=20)):
    """Get trending/popular products."""
    try:
        trending = recommendation_service.get_trending_products(top_k=top_k)
        return {
            "trending_products": trending,
            "total": len(trending)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-description")
async def generate_product_description(request: GenerateDescriptionRequest):
    """Generate a creative description for a product."""
    try:
        # Get the product
        product = product_service.get_product_by_id(request.product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Generate description
        if request.enhance_existing and product.get('description'):
            generated_description = genai_service.enhance_existing_description(
                product_name=product['name'],
                original_description=product['description']
            )
            enhancement_type = "enhanced"
        else:
            generated_description = genai_service.generate_creative_description(
                product_name=product['name'],
                category=product.get('category', ''),
                original_description=product.get('description', ''),
                features={'price': product.get('price', 0)}
            )
            enhancement_type = "generated"
        
        return GenerateDescriptionResponse(
            product_id=request.product_id,
            original_description=product.get('description', ''),
            generated_description=generated_description,
            enhancement_type=enhancement_type
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/embeddings")
async def get_embeddings_for_analytics():
    """Get embeddings for analytics visualization."""
    try:
        embeddings, metadata = product_service.get_embeddings_for_analytics()
        return {
            "embeddings": embeddings.tolist(),
            "metadata": metadata,
            "dimension": len(embeddings[0]) if len(embeddings) > 0 else 0,
            "total_products": len(embeddings)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

