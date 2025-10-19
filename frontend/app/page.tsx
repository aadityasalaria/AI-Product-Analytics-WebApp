// Landing page showing the chat-driven recommender
import ProductRecommendationChat from "@/components/ProductRecommendationChat";

/**
 * Home page renders the recommendation chat experience.
 */
export default function Home() {
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-foreground mb-4 font-gantari">
          AI-Powered Product Recommendations
        </h1>
        <p className="text-base text-muted-foreground max-w-3xl mx-auto">
          Discover the perfect furniture for your space with our intelligent recommendation system. 
          Get personalized suggestions and creative AI-generated descriptions.
        </p>
      </div>
      
      <ProductRecommendationChat />
    </div>
  );
}

