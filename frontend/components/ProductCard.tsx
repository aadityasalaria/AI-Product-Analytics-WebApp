"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Sparkles, Star, DollarSign } from "lucide-react";
import { generateProductDescription } from "@/lib/api";

interface Product {
  id: string;
  name: string;
  category: string;
  price: number;
  description: string;
  image_url?: string;
  similarity_score?: number;
  recommendation_reason?: string;
}

interface ProductCardProps {
  product: Product;
}

export default function ProductCard({ product }: ProductCardProps) {
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedDescription, setGeneratedDescription] = useState<string | null>(null);
  const [showGenerated, setShowGenerated] = useState(false);

  const handleGenerateDescription = async () => {
    setIsGenerating(true);
    try {
      const response = await generateProductDescription({
        product_id: product.id,
        enhance_existing: false,
      });
      setGeneratedDescription(response.generated_description);
      setShowGenerated(true);
    } catch (error) {
      console.error("Error generating description:", error);
    } finally {
      setIsGenerating(false);
    }
  };

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(price);
  };

  const getSimilarityColor = (score?: number) => {
    if (!score) return "text-gray-500";
    if (score >= 0.9) return "text-green-600";
    if (score >= 0.8) return "text-blue-600";
    if (score >= 0.7) return "text-yellow-600";
    return "text-gray-500";
  };

  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardHeader className="pb-3">
        <div className="flex justify-between items-start">
          <CardTitle className="text-lg line-clamp-2">{product.name}</CardTitle>
          {product.similarity_score && (
            <div className={`text-sm font-medium ${getSimilarityColor(product.similarity_score)}`}>
              {Math.round(product.similarity_score * 100)}% match
            </div>
          )}
        </div>
        <div className="flex items-center gap-2 text-sm text-gray-600">
          <span className="capitalize">{product.category}</span>
          <span>•</span>
          <div className="flex items-center gap-1">
            <DollarSign className="h-3 w-3" />
            <span className="font-medium">{formatPrice(product.price)}</span>
          </div>
        </div>
      </CardHeader>
      
      <CardContent className="pt-0">
        {/* Product Image */}
        <div className="mb-3">
          {product.image_url ? (
            <img
              src={product.image_url}
              alt={product.name}
              className="w-full h-32 object-cover rounded-md"
              onError={(e) => {
                e.currentTarget.src = `https://via.placeholder.com/300x200?text=${encodeURIComponent(product.name)}`;
              }}
            />
          ) : (
            <div className="w-full h-32 bg-gray-100 rounded-md flex items-center justify-center">
              <span className="text-gray-400 text-sm">No image available</span>
            </div>
          )}
        </div>

        {/* Description */}
        <div className="mb-3">
          <p className="text-sm text-gray-700 line-clamp-3">
            {showGenerated && generatedDescription 
              ? generatedDescription 
              : product.description
            }
          </p>
        </div>

        {/* Recommendation Reason */}
        {product.recommendation_reason && (
          <div className="mb-3 p-2 bg-blue-50 rounded-md">
            <p className="text-xs text-blue-700">
              <Star className="h-3 w-3 inline mr-1" />
              {product.recommendation_reason}
            </p>
          </div>
        )}

        {/* Generate AI Description Button */}
        <Button
          onClick={handleGenerateDescription}
          disabled={isGenerating}
          variant="outline"
          size="sm"
          className="w-full"
        >
          {isGenerating ? (
            <div className="flex items-center gap-2">
              <div className="animate-spin h-3 w-3 border-2 border-gray-300 border-t-gray-600 rounded-full"></div>
              <span>Generating...</span>
            </div>
          ) : (
            <div className="flex items-center gap-2">
              <Sparkles className="h-3 w-3" />
              <span>Generate AI Description</span>
            </div>
          )}
        </Button>

        {/* Toggle between original and generated description */}
        {generatedDescription && (
          <Button
            onClick={() => setShowGenerated(!showGenerated)}
            variant="ghost"
            size="sm"
            className="w-full mt-2 text-xs"
          >
            {showGenerated ? "Show Original" : "Show AI Generated"}
          </Button>
        )}
      </CardContent>
    </Card>
  );
}
