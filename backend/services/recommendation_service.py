from typing import List, Dict, Optional, Tuple
from services.product_service import product_service
from core.config import settings
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class RecommendationService:
    def __init__(self):
        self.product_service = product_service
    
    def get_recommendations(
        self, 
        query: str, 
        top_k: int = None, 
        category_filter: Optional[str] = None,
        price_min: Optional[float] = None,
        price_max: Optional[float] = None
    ) -> List[Dict]:
        """Get product recommendations based on query and filters."""
        try:
            top_k = top_k or settings.DEFAULT_TOP_K
            
            # Build filters for Pinecone
            filters = {}
            if category_filter:
                filters['category'] = {"$eq": category_filter}
            if price_min is not None or price_max is not None:
                price_filter = {}
                if price_min is not None:
                    price_filter['$gte'] = price_min
                if price_max is not None:
                    price_filter['$lte'] = price_max
                filters['price'] = price_filter
            
            # Search for similar products
            similar_products = self.product_service.search_similar_products(
                query=query,
                top_k=top_k * 2,  # Get more to filter later
                filters=filters if filters else None
            )
            
            # Apply additional filtering and scoring
            filtered_products = []
            for product in similar_products:
                # Apply similarity threshold
                if product['similarity_score'] >= settings.SIMILARITY_THRESHOLD:
                    # Add recommendation metadata
                    product['recommendation_reason'] = self._get_recommendation_reason(
                        query, product, product['similarity_score']
                    )
                    filtered_products.append(product)
            
            # Sort by similarity score and return top_k
            filtered_products.sort(key=lambda x: x['similarity_score'], reverse=True)
            return filtered_products[:top_k]
            
        except Exception as e:
            raise Exception(f"Error getting recommendations: {str(e)}")
    
    def get_similar_products(
        self, 
        product_id: str, 
        top_k: int = None,
        exclude_self: bool = True
    ) -> List[Dict]:
        """Get products similar to a specific product."""
        try:
            top_k = top_k or settings.DEFAULT_TOP_K
            
            # Get the target product
            target_product = self.product_service.get_product_by_id(product_id)
            if not target_product:
                raise ValueError(f"Product with ID {product_id} not found")
            
            # Create query from product attributes
            query = f"{target_product['name']} {target_product['category']} {target_product.get('description', '')}"
            
            # Get similar products
            similar_products = self.product_service.search_similar_products(
                query=query,
                top_k=top_k + 1 if exclude_self else top_k  # +1 to account for self
            )
            
            # Filter out the original product if requested
            if exclude_self:
                similar_products = [p for p in similar_products if p['id'] != product_id]
            
            # Add recommendation metadata
            for product in similar_products:
                product['recommendation_reason'] = f"Similar to {target_product['name']}"
            
            return similar_products[:top_k]
            
        except Exception as e:
            raise Exception(f"Error getting similar products: {str(e)}")
    
    def get_category_recommendations(
        self, 
        category: str, 
        top_k: int = None,
        price_min: Optional[float] = None,
        price_max: Optional[float] = None
    ) -> List[Dict]:
        """Get recommendations within a specific category."""
        try:
            top_k = top_k or settings.DEFAULT_TOP_K
            
            # Build filters
            filters = {'category': {"$eq": category}}
            if price_min is not None or price_max is not None:
                price_filter = {}
                if price_min is not None:
                    price_filter['$gte'] = price_min
                if price_max is not None:
                    price_filter['$lte'] = price_max
                filters['price'] = price_filter
            
            # Search with category filter
            similar_products = self.product_service.search_similar_products(
                query=category,  # Use category as query
                top_k=top_k,
                filters=filters
            )
            
            # Add recommendation metadata
            for product in similar_products:
                product['recommendation_reason'] = f"Popular in {category} category"
            
            return similar_products
            
        except Exception as e:
            raise Exception(f"Error getting category recommendations: {str(e)}")
    
    def get_trending_products(self, top_k: int = None) -> List[Dict]:
        """Get trending/popular products (simplified implementation)."""
        try:
            top_k = top_k or settings.DEFAULT_TOP_K
            
            # Get all products and sort by price (as a proxy for popularity)
            # In a real implementation, you'd use actual popularity metrics
            all_products = self.product_service.get_all_products(limit=100)
            
            # Sort by price (higher price = more premium = trending)
            trending_products = sorted(
                all_products, 
                key=lambda x: x.get('price', 0), 
                reverse=True
            )
            
            # Add recommendation metadata
            for product in trending_products[:top_k]:
                product['recommendation_reason'] = "Trending product"
                product['similarity_score'] = 0.9  # High score for trending
            
            return trending_products[:top_k]
            
        except Exception as e:
            raise Exception(f"Error getting trending products: {str(e)}")
    
    def _get_recommendation_reason(self, query: str, product: Dict, similarity_score: float) -> str:
        """Generate a human-readable reason for the recommendation."""
        reasons = []
        
        # Similarity-based reason
        if similarity_score > 0.9:
            reasons.append("Highly similar to your search")
        elif similarity_score > 0.8:
            reasons.append("Very similar to your search")
        elif similarity_score > 0.7:
            reasons.append("Similar to your search")
        
        # Category-based reason
        if product.get('category'):
            reasons.append(f"Popular in {product['category']} category")
        
        # Price-based reason
        price = product.get('price', 0)
        if price > 1000:
            reasons.append("Premium quality")
        elif price < 200:
            reasons.append("Great value")
        
        return "; ".join(reasons) if reasons else "Recommended for you"
    
    def analyze_recommendation_quality(self, recommendations: List[Dict]) -> Dict:
        """Analyze the quality of recommendations."""
        if not recommendations:
            return {
                'total_recommendations': 0,
                'average_similarity': 0,
                'category_diversity': 0,
                'price_range': {'min': 0, 'max': 0}
            }
        
        similarities = [r['similarity_score'] for r in recommendations]
        categories = [r.get('category', '') for r in recommendations]
        prices = [r.get('price', 0) for r in recommendations]
        
        return {
            'total_recommendations': len(recommendations),
            'average_similarity': np.mean(similarities),
            'max_similarity': np.max(similarities),
            'min_similarity': np.min(similarities),
            'category_diversity': len(set(categories)),
            'price_range': {
                'min': np.min(prices),
                'max': np.max(prices),
                'mean': np.mean(prices)
            }
        }

# Global instance
recommendation_service = RecommendationService()
