"""Analytics API routes.

Provides endpoints for embeddings visualization and system analytics.
"""

from typing import Dict, List, Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

# Local services
from services.analytics_service import analytics_service

router = APIRouter()

# Pydantic models for response
class Embedding2DResponse(BaseModel):
    coordinates: List[List[float]]
    metadata: List[Dict]
    method: str
    n_components: int
    explained_variance_ratio: Optional[List[float]] = None

class AnalyticsMetricsResponse(BaseModel):
    total_products: int
    categories: Dict[str, int]
    category_insights: Dict[str, Dict]
    price_statistics: Dict[str, float]
    price_ranges: Dict[str, int]
    recommendation_insights: Dict

class SimilarityAnalysisResponse(BaseModel):
    product_id: str
    target_product: Optional[Dict]
    similarity_scores: List[float]
    similarity_statistics: Dict[str, float]
    category_distribution: Dict[str, int]
    price_similarity: Dict

@router.get("/embeddings-2d")
async def get_embeddings_2d(
    method: str = Query("pca", regex="^(pca|tsne)$"),
    n_components: int = Query(2, ge=2, le=3)
):
    """Get 2D coordinates for embedding visualization."""
    try:
        result = analytics_service.get_embeddings_2d(
            method=method,
            n_components=n_components
        )
        return Embedding2DResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/metrics")
async def get_analytics_metrics():
    """Get comprehensive analytics metrics."""
    try:
        metrics = analytics_service.get_analytics_metrics()
        return AnalyticsMetricsResponse(**metrics)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/similarity/{product_id}")
async def get_similarity_analysis(product_id: str):
    """Analyze similarity patterns for a specific product."""
    try:
        analysis = analytics_service.get_similarity_analysis(product_id)
        return SimilarityAnalysisResponse(**analysis)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/quality")
async def get_recommendation_quality():
    """Get recommendation quality metrics."""
    try:
        quality_metrics = analytics_service.get_recommendation_quality_metrics()
        return quality_metrics
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/categories")
async def get_category_analytics():
    """Get detailed analytics for each category."""
    try:
        metrics = analytics_service.get_analytics_metrics()
        return {
            "category_insights": metrics.get("category_insights", {}),
            "category_distribution": metrics.get("categories", {}),
            "total_categories": len(metrics.get("categories", {}))
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/price-analysis")
async def get_price_analysis():
    """Get detailed price analysis."""
    try:
        metrics = analytics_service.get_analytics_metrics()
        return {
            "price_statistics": metrics.get("price_statistics", {}),
            "price_ranges": metrics.get("price_ranges", {}),
            "price_insights": {
                "budget_products": metrics.get("price_ranges", {}).get("budget", 0),
                "mid_range_products": metrics.get("price_ranges", {}).get("mid_range", 0),
                "premium_products": metrics.get("price_ranges", {}).get("premium", 0)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recommendation-insights")
async def get_recommendation_insights():
    """Get insights about the recommendation system performance."""
    try:
        metrics = analytics_service.get_analytics_metrics()
        return {
            "recommendation_insights": metrics.get("recommendation_insights", {}),
            "quality_metrics": analytics_service.get_recommendation_quality_metrics()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

