import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Tuple
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec
from core.config import settings
import json
import os
from pathlib import Path

class ProductService:
    def __init__(self):
        self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        self.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)
        self.index_name = settings.PINECONE_INDEX_NAME
        self.products_data = []
        
    def get_or_create_index(self) -> str:
        """Get an existing index or create a new one if it doesn't exist."""
        index_list = self.pc.list_indexes().names()
        
        if self.index_name not in index_list:
            self.pc.create_index(
                name=self.index_name,
                dimension=settings.EMBEDDING_DIMENSION,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region=settings.PINECONE_ENVIRONMENT)
            )
        
        return self.index_name
    
    def load_dataset(self, file_path: str) -> List[Dict]:
        """Load furniture dataset from CSV or JSON file."""
        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith('.json'):
                df = pd.read_json(file_path)
            else:
                raise ValueError("Unsupported file format. Use CSV or JSON.")
            
            # Validate required columns
            required_columns = ['id', 'name', 'category', 'price', 'description']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise ValueError(f"Missing required columns: {missing_columns}")
            
            # Convert to list of dictionaries
            products = df.to_dict('records')
            self.products_data = products
            
            return products
            
        except Exception as e:
            raise Exception(f"Error loading dataset: {str(e)}")
    
    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for a list of texts."""
        return self.embedding_model.encode(texts)
    
    def store_products_in_pinecone(self, products: List[Dict]) -> bool:
        """Store product embeddings in Pinecone vector database."""
        try:
            index_name = self.get_or_create_index()
            index = self.pc.Index(index_name)
            
            # Prepare vectors for Pinecone
            vectors = []
            for i, product in enumerate(products):
                # Create text for embedding (combine name, category, description)
                text_for_embedding = f"{product['name']} {product['category']} {product.get('description', '')}"
                
                # Generate embedding
                embedding = self.embedding_model.encode([text_for_embedding])[0]
                
                # Prepare metadata
                metadata = {
                    'name': product['name'],
                    'category': product['category'],
                    'price': float(product['price']),
                    'description': product.get('description', ''),
                    'image_url': product.get('image_url', ''),
                    'product_id': str(product['id'])
                }
                
                vectors.append({
                    'id': str(product['id']),
                    'values': embedding.tolist(),
                    'metadata': metadata
                })
            
            # Upsert vectors to Pinecone
            index.upsert(vectors=vectors)
            
            return True
            
        except Exception as e:
            raise Exception(f"Error storing products in Pinecone: {str(e)}")
    
    def search_similar_products(self, query: str, top_k: int = 5, filters: Optional[Dict] = None) -> List[Dict]:
        """Search for similar products using vector similarity."""
        try:
            index_name = self.get_or_create_index()
            index = self.pc.Index(index_name)
            
            # Generate embedding for query
            query_embedding = self.embedding_model.encode([query])[0]
            
            # Search in Pinecone
            search_params = {
                'vector': query_embedding.tolist(),
                'top_k': top_k,
                'include_metadata': True
            }
            
            if filters:
                search_params['filter'] = filters
            
            results = index.query(**search_params)
            
            # Format results
            similar_products = []
            for match in results.matches:
                product = {
                    'id': match.id,
                    'similarity_score': match.score,
                    **match.metadata
                }
                similar_products.append(product)
            
            return similar_products
            
        except Exception as e:
            raise Exception(f"Error searching similar products: {str(e)}")
    
    def get_all_products(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """Get all products with pagination."""
        try:
            index_name = self.get_or_create_index()
            index = self.pc.Index(index_name)
            
            # Query all vectors
            results = index.query(
                vector=[0.0] * settings.EMBEDDING_DIMENSION,  # Dummy vector
                top_k=limit + offset,
                include_metadata=True
            )
            
            # Format and paginate results
            products = []
            for match in results.matches[offset:offset + limit]:
                product = {
                    'id': match.id,
                    **match.metadata
                }
                products.append(product)
            
            return products
            
        except Exception as e:
            raise Exception(f"Error getting all products: {str(e)}")
    
    def get_product_by_id(self, product_id: str) -> Optional[Dict]:
        """Get a specific product by ID."""
        try:
            index_name = self.get_or_create_index()
            index = self.pc.Index(index_name)
            
            # Fetch specific vector
            results = index.fetch(ids=[product_id])
            
            if product_id in results.vectors:
                vector_data = results.vectors[product_id]
                return {
                    'id': product_id,
                    **vector_data.metadata
                }
            
            return None
            
        except Exception as e:
            raise Exception(f"Error getting product by ID: {str(e)}")
    
    def get_embeddings_for_analytics(self) -> Tuple[np.ndarray, List[Dict]]:
        """Get all embeddings and metadata for analytics visualization."""
        try:
            index_name = self.get_or_create_index()
            index = self.pc.Index(index_name)
            
            # Get all vectors
            results = index.query(
                vector=[0.0] * settings.EMBEDDING_DIMENSION,
                top_k=10000,  # Large number to get all
                include_metadata=True
            )
            
            embeddings = []
            metadata = []
            
            for match in results.matches:
                # Reconstruct embedding from Pinecone (this is a simplified approach)
                # In practice, you might want to store embeddings separately for analytics
                embeddings.append([0.0] * settings.EMBEDDING_DIMENSION)  # Placeholder
                metadata.append({
                    'id': match.id,
                    'similarity_score': match.score,
                    **match.metadata
                })
            
            return np.array(embeddings), metadata
            
        except Exception as e:
            raise Exception(f"Error getting embeddings for analytics: {str(e)}")

# Global instance
product_service = ProductService()
