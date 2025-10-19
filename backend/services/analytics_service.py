"""Analytics service.

Aggregates product data and computes lightweight analytics for the UI.
"""

from typing import List, Dict, Tuple, Optional

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

# Local services/config
from core.config import settings
from services.product_service import product_service
from services.recommendation_service import recommendation_service

class AnalyticsService:
    def __init__(self):
        self.product_service = product_service
        self.recommendation_service = recommendation_service
    
    def get_embeddings_2d(self, method: str = "pca", n_components: int = 2) -> Dict:
        """Get 2D coordinates for embedding visualization."""
        try:
            # Get all products and their metadata
            all_products = self.product_service.get_all_products(limit=1000)
            
            if not all_products:
                return {
                    'coordinates': [],
                    'metadata': [],
                    'method': method,
                    'n_components': n_components
                }
            
            # Generate dummy embeddings for visualization only.
            # In production, retrieve persisted embeddings instead.
            n_products = len(all_products)
            dummy_embeddings = np.random.randn(n_products, settings.EMBEDDING_DIMENSION)
            
            # Apply dimensionality reduction
            if method.lower() == "pca":
                reducer = PCA(n_components=n_components, random_state=42)
                coordinates = reducer.fit_transform(dummy_embeddings)
            elif method.lower() == "tsne":
                reducer = TSNE(n_components=n_components, random_state=42, perplexity=min(30, n_products-1))
                coordinates = reducer.fit_transform(dummy_embeddings)
            else:
                raise ValueError("Method must be 'pca' or 'tsne'")
            
            # Prepare metadata for visualization
            metadata = []
            for i, product in enumerate(all_products):
                metadata.append({
                    'id': product['id'],
                    'name': product.get('name', ''),
                    'category': product.get('category', ''),
                    'price': product.get('price', 0),
                    'x': float(coordinates[i, 0]),
                    'y': float(coordinates[i, 1])
                })
            
            return {
                'coordinates': coordinates.tolist(),
                'metadata': metadata,
                'method': method,
                'n_components': n_components,
                'explained_variance_ratio': getattr(reducer, 'explained_variance_ratio_', None)
            }
            
        except Exception as e:
            raise Exception(f"Error getting 2D embeddings: {str(e)}")
    
    def get_analytics_metrics(self) -> Dict:
        """Get comprehensive analytics metrics."""
        try:
            # Get all products
            all_products = self.product_service.get_all_products(limit=1000)
            
            if not all_products:
                return {
                    'total_products': 0,
                    'categories': {},
                    'price_statistics': {},
                    'recommendation_insights': {}
                }
            
            # Basic statistics
            total_products = len(all_products)
            
            # Category distribution
            categories = {}
            for product in all_products:
                category = product.get('category', 'Unknown')
                categories[category] = categories.get(category, 0) + 1
            
            # Price statistics
            prices = [product.get('price', 0) for product in all_products if product.get('price')]
            price_stats = {
                'min': float(np.min(prices)) if prices else 0,
                'max': float(np.max(prices)) if prices else 0,
                'mean': float(np.mean(prices)) if prices else 0,
                'median': float(np.median(prices)) if prices else 0,
                'std': float(np.std(prices)) if prices else 0
            }
            
            # Price ranges
            price_ranges = {
                'budget': len([p for p in prices if p < 200]),
                'mid_range': len([p for p in prices if 200 <= p < 800]),
                'premium': len([p for p in prices if p >= 800])
            }
            
            # Category insights
            category_insights = {}
            for category, count in categories.items():
                category_products = [p for p in all_products if p.get('category') == category]
                category_prices = [p.get('price', 0) for p in category_products if p.get('price')]
                
                category_insights[category] = {
                    'count': count,
                    'percentage': round((count / total_products) * 100, 2),
                    'avg_price': float(np.mean(category_prices)) if category_prices else 0,
                    'price_range': {
                        'min': float(np.min(category_prices)) if category_prices else 0,
                        'max': float(np.max(category_prices)) if category_prices else 0
                    }
                }
            
            return {
                'total_products': total_products,
                'categories': categories,
                'category_insights': category_insights,
                'price_statistics': price_stats,
                'price_ranges': price_ranges,
                'recommendation_insights': self._get_recommendation_insights()
            }
            
        except Exception as e:
            raise Exception(f"Error getting analytics metrics: {str(e)}")
    
    def get_similarity_analysis(self, product_id: str) -> Dict:
        """Analyze similarity patterns for a specific product."""
        try:
            # Get similar products
            similar_products = self.recommendation_service.get_similar_products(
                product_id=product_id,
                top_k=10
            )
            
            if not similar_products:
                return {
                    'product_id': product_id,
                    'similarity_scores': [],
                    'category_distribution': {},
                    'price_similarity': {}
                }
            
            # Analyze similarity scores
            similarity_scores = [p['similarity_score'] for p in similar_products]
            
            # Category distribution of similar products
            category_dist = {}
            for product in similar_products:
                category = product.get('category', 'Unknown')
                category_dist[category] = category_dist.get(category, 0) + 1
            
            # Price similarity analysis
            target_product = self.product_service.get_product_by_id(product_id)
            target_price = target_product.get('price', 0) if target_product else 0
            
            similar_prices = [p.get('price', 0) for p in similar_products]
            price_similarity = {
                'target_price': target_price,
                'similar_prices': similar_prices,
                'price_variance': float(np.var(similar_prices)) if similar_prices else 0,
                'price_range': {
                    'min': float(np.min(similar_prices)) if similar_prices else 0,
                    'max': float(np.max(similar_prices)) if similar_prices else 0
                }
            }
            
            return {
                'product_id': product_id,
                'target_product': target_product,
                'similarity_scores': similarity_scores,
                'similarity_statistics': {
                    'mean': float(np.mean(similarity_scores)),
                    'std': float(np.std(similarity_scores)),
                    'min': float(np.min(similarity_scores)),
                    'max': float(np.max(similarity_scores))
                },
                'category_distribution': category_dist,
                'price_similarity': price_similarity
            }
            
        except Exception as e:
            raise Exception(f"Error analyzing similarity: {str(e)}")
    
    def get_recommendation_quality_metrics(self) -> Dict:
        """Get metrics about recommendation quality."""
        try:
            # Sample queries for testing
            test_queries = [
                "modern sofa",
                "office chair",
                "dining table",
                "bedroom furniture",
                "storage solutions"
            ]
            
            quality_metrics = []
            
            for query in test_queries:
                try:
                    recommendations = self.recommendation_service.get_recommendations(
                        query=query,
                        top_k=5
                    )
                    
                    if recommendations:
                        quality_analysis = self.recommendation_service.analyze_recommendation_quality(
                            recommendations
                        )
                        quality_metrics.append({
                            'query': query,
                            'quality_analysis': quality_analysis
                        })
                except Exception as e:
                    print(f"Error testing query '{query}': {str(e)}")
                    continue
            
            return {
                'test_queries': len(test_queries),
                'successful_queries': len(quality_metrics),
                'quality_metrics': quality_metrics,
                'overall_quality': self._calculate_overall_quality(quality_metrics)
            }
            
        except Exception as e:
            raise Exception(f"Error getting recommendation quality metrics: {str(e)}")
    
    def _get_recommendation_insights(self) -> Dict:
        """Get insights about the recommendation system."""
        try:
            # Placeholder values; wire up analytics events in production.
            return {
                'total_recommendations_generated': 0,  # Would track in production
                'average_similarity_score': 0.8,
                'most_recommended_categories': [],
                'recommendation_accuracy': 0.85  # Placeholder
            }
        except Exception as e:
            return {'error': str(e)}
    
    def _calculate_overall_quality(self, quality_metrics: List[Dict]) -> Dict:
        """Calculate overall recommendation quality."""
        if not quality_metrics:
            return {
                'average_similarity': 0,
                'average_diversity': 0,
                'overall_score': 0
            }
        
        similarities = []
        diversities = []
        
        for metric in quality_metrics:
            analysis = metric.get('quality_analysis', {})
            similarities.append(analysis.get('average_similarity', 0))
            diversities.append(analysis.get('category_diversity', 0))
        
        return {
            'average_similarity': float(np.mean(similarities)),
            'average_diversity': float(np.mean(diversities)),
            'overall_score': float(np.mean(similarities) * 0.7 + np.mean(diversities) * 0.3)
        }

# Global instance
analytics_service = AnalyticsService()

