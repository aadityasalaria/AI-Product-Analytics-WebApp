import ProductRecommendationChat from "@/components/ProductRecommendationChat";

export default function Home() {
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          AI-Powered Product Recommendations
        </h1>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto">
          Discover the perfect furniture for your space with our intelligent recommendation system. 
          Get personalized suggestions and creative AI-generated descriptions.
        </p>
      </div>
      
      <ProductRecommendationChat />
    </div>
  );
}
