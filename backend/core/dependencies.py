from fastapi import Depends, HTTPException, status
from typing import Optional
import os

def get_upload_directory() -> str:
    """Get the upload directory path"""
    upload_dir = os.getenv("UPLOAD_DIRECTORY", "uploads/")
    os.makedirs(upload_dir, exist_ok=True)
    return upload_dir

def get_dataset_directory() -> str:
    """Get the dataset directory path"""
    dataset_dir = os.getenv("DATASET_DIRECTORY", "datasets/")
    os.makedirs(dataset_dir, exist_ok=True)
    return dataset_dir

def validate_api_keys():
    """Validate that required API keys are present"""
    from core.config import settings
    
    if not settings.PINECONE_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="PINECONE_API_KEY not configured"
        )
    
    return True
