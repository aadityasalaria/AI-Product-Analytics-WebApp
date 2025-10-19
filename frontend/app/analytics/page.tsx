// Analytics dashboard page: charts and embeddings view
import EmbeddingVisualization from "@/components/EmbeddingVisualization";
import MetricsDashboard from "@/components/MetricsDashboard";

/**
 * AnalyticsPage aggregates metrics and embedding visualization.
 */
export default function AnalyticsPage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-foreground mb-4 font-gantari">
          Analytics Dashboard
        </h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
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

