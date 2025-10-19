from transformers import pipeline, GPT2LMHeadModel, GPT2Tokenizer
from typing import Dict, Optional
import torch
import re
from core.config import settings

class GenAIService:
    def __init__(self):
        self.model_name = settings.GENAI_MODEL
        self.generator = None
        self.tokenizer = None
        self._load_model()
    
    def _load_model(self):
        """Load the GPT-2 model and tokenizer."""
        try:
            # Load model and tokenizer
            self.tokenizer = GPT2Tokenizer.from_pretrained(self.model_name)
            self.model = GPT2LMHeadModel.from_pretrained(self.model_name)
            
            # Add padding token if it doesn't exist
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Create text generation pipeline
            self.generator = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                pad_token_id=self.tokenizer.eos_token_id,
                max_length=150,
                do_sample=True,
                temperature=0.8,
                top_p=0.9,
                repetition_penalty=1.1
            )
            
        except Exception as e:
            print(f"Warning: Could not load {self.model_name}. Using fallback generator.")
            self.generator = None
    
    def generate_creative_description(
        self, 
        product_name: str, 
        category: str, 
        original_description: str = "",
        features: Optional[Dict] = None
    ) -> str:
        """Generate a creative marketing description for a product."""
        try:
            if not self.generator:
                return self._generate_fallback_description(product_name, category, original_description)
            
            # Create a prompt for the model
            prompt = self._create_prompt(product_name, category, original_description, features)
            
            # Generate text
            result = self.generator(
                prompt,
                max_length=len(prompt.split()) + 50,  # Add 50 words to the prompt
                num_return_sequences=1,
                temperature=0.8,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
            
            # Extract and clean the generated text
            generated_text = result[0]['generated_text']
            description = self._extract_description(generated_text, prompt)
            
            return description
            
        except Exception as e:
            print(f"Error generating description: {str(e)}")
            return self._generate_fallback_description(product_name, category, original_description)
    
    def enhance_existing_description(
        self, 
        product_name: str, 
        original_description: str
    ) -> str:
        """Enhance an existing product description with creative marketing copy."""
        try:
            if not self.generator:
                return self._enhance_fallback_description(product_name, original_description)
            
            # Create enhancement prompt
            prompt = f"Enhance this product description to be more engaging and marketing-focused:\n\nProduct: {product_name}\nOriginal: {original_description}\n\nEnhanced description:"
            
            # Generate enhanced description
            result = self.generator(
                prompt,
                max_length=len(prompt.split()) + 30,
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True
            )
            
            generated_text = result[0]['generated_text']
            enhanced_description = self._extract_description(generated_text, prompt)
            
            return enhanced_description
            
        except Exception as e:
            print(f"Error enhancing description: {str(e)}")
            return self._enhance_fallback_description(product_name, original_description)
    
    def generate_category_specific_description(
        self, 
        product_name: str, 
        category: str
    ) -> str:
        """Generate a description tailored to a specific furniture category."""
        try:
            category_prompts = {
                'sofa': f"Create a compelling description for a {product_name} sofa that emphasizes comfort, style, and durability:",
                'chair': f"Write an engaging description for a {product_name} chair that highlights ergonomics and design:",
                'table': f"Describe a {product_name} table focusing on functionality, craftsmanship, and versatility:",
                'bed': f"Create a cozy description for a {product_name} bed that emphasizes comfort and quality sleep:",
                'desk': f"Write a professional description for a {product_name} desk that highlights productivity and organization:",
                'storage': f"Describe a {product_name} storage solution that emphasizes organization and space efficiency:"
            }
            
            prompt = category_prompts.get(category.lower(), f"Create a compelling description for a {product_name} {category}:")
            
            if not self.generator:
                return self._generate_fallback_description(product_name, category, "")
            
            result = self.generator(
                prompt,
                max_length=len(prompt.split()) + 40,
                num_return_sequences=1,
                temperature=0.8,
                do_sample=True
            )
            
            generated_text = result[0]['generated_text']
            description = self._extract_description(generated_text, prompt)
            
            return description
            
        except Exception as e:
            print(f"Error generating category-specific description: {str(e)}")
            return self._generate_fallback_description(product_name, category, "")
    
    def _create_prompt(
        self, 
        product_name: str, 
        category: str, 
        original_description: str, 
        features: Optional[Dict]
    ) -> str:
        """Create a prompt for the GPT-2 model."""
        prompt = f"Product: {product_name}\nCategory: {category}\n"
        
        if original_description:
            prompt += f"Original description: {original_description}\n"
        
        if features:
            feature_text = ", ".join([f"{k}: {v}" for k, v in features.items()])
            prompt += f"Features: {feature_text}\n"
        
        prompt += "Creative marketing description:"
        return prompt
    
    def _extract_description(self, generated_text: str, prompt: str) -> str:
        """Extract the description from the generated text."""
        # Remove the prompt from the generated text
        description = generated_text.replace(prompt, "").strip()
        
        # Clean up the description
        description = re.sub(r'\n+', ' ', description)  # Replace multiple newlines with space
        description = re.sub(r'\s+', ' ', description)  # Replace multiple spaces with single space
        
        # Ensure it ends with a period
        if description and not description.endswith(('.', '!', '?')):
            description += "."
        
        return description
    
    def _generate_fallback_description(
        self, 
        product_name: str, 
        category: str, 
        original_description: str
    ) -> str:
        """Generate a fallback description when the model is not available."""
        category_templates = {
            'sofa': f"The {product_name} is a beautifully crafted sofa that combines comfort and style. Perfect for your living room, it offers exceptional comfort and durability.",
            'chair': f"The {product_name} chair features ergonomic design and premium materials. Ideal for both work and relaxation.",
            'table': f"The {product_name} table is a versatile piece that combines functionality with elegant design. Perfect for dining, work, or display.",
            'bed': f"The {product_name} bed provides the perfect foundation for a good night's sleep. Crafted with quality materials and attention to detail.",
            'desk': f"The {product_name} desk offers a perfect workspace solution with its clean design and practical features.",
            'storage': f"The {product_name} storage solution helps you organize your space efficiently while maintaining a stylish appearance."
        }
        
        if category.lower() in category_templates:
            return category_templates[category.lower()]
        
        return f"The {product_name} is a high-quality {category} that combines style and functionality. Perfect for modern homes and offices."
    
    def _enhance_fallback_description(self, product_name: str, original_description: str) -> str:
        """Enhance description using fallback method."""
        if not original_description:
            return self._generate_fallback_description(product_name, "furniture", "")
        
        # Simple enhancement by adding marketing words
        enhanced = original_description
        marketing_words = ["premium", "elegant", "stunning", "exceptional", "beautiful", "sophisticated"]
        
        # Add a marketing word if not already present
        for word in marketing_words:
            if word not in enhanced.lower():
                enhanced = f"{word.capitalize()} {enhanced.lower()}"
                break
        
        return enhanced

# Global instance
genai_service = GenAIService()
