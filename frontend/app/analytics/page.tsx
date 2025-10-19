import EmbeddingVisualization from "@/components/EmbeddingVisualization";
import MetricsDashboard from "@/components/MetricsDashboard";

export default function AnalyticsPage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Analytics Dashboard
        </h1>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto">
          Explore product embeddings, recommendation patterns, and system insights.
        </p>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Metrics Dashboard */}
        <div className="lg:col-span-1">
          <MetricsDashboard />
        </div>
        
        {/* Embedding Visualization */}
        <div className="lg:col-span-1">
          <EmbeddingVisualization />
        </div>
      </div>
    </div>
  );
}
