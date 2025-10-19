"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from "recharts";
import { Eye, RefreshCw, Settings } from "lucide-react";
import { getEmbeddings2D } from "@/lib/api";

interface EmbeddingPoint {
  x: number;
  y: number;
  id: string;
  name: string;
  category: string;
  price: number;
}

interface Embedding2DResponse {
  coordinates: number[][];
  metadata: Array<{
    id: string;
    name: string;
    category: string;
    price: number;
    x: number;
    y: number;
  }>;
  method: string;
  n_components: number;
  explained_variance_ratio?: number[];
}

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8', '#82CA9D'];

export default function EmbeddingVisualization() {
  const [data, setData] = useState<EmbeddingPoint[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [method, setMethod] = useState<'pca' | 'tsne'>('pca');
  const [selectedPoint, setSelectedPoint] = useState<EmbeddingPoint | null>(null);
  const [showSettings, setShowSettings] = useState(false);

  useEffect(() => {
    fetchEmbeddings();
  }, [method]);

  const fetchEmbeddings = async () => {
    try {
      setLoading(true);
      const response = await getEmbeddings2D(method, 2);
      
      // Transform data for visualization
      const points: EmbeddingPoint[] = response.metadata.map((item) => ({
        x: item.x,
        y: item.y,
        id: item.id,
        name: item.name,
        category: item.category,
        price: item.price,
      }));
      
      setData(points);
    } catch (err) {
      setError("Failed to fetch embedding data");
      console.error("Error fetching embeddings:", err);
    } finally {
      setLoading(false);
    }
  };

  const getCategoryColor = (category: string) => {
    const categories = [...new Set(data.map(d => d.category))];
    const index = categories.indexOf(category);
    return COLORS[index % COLORS.length];
  };

  const handlePointClick = (point: any) => {
    if (point && point.payload) {
      setSelectedPoint(point.payload);
    }
  };

  if (loading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Eye className="h-5 w-5" />
            Product Embeddings Visualization
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-center h-64">
            <div className="animate-spin h-8 w-8 border-2 border-gray-300 border-t-gray-600 rounded-full"></div>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (error || data.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Eye className="h-5 w-5" />
            Product Embeddings Visualization
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center text-red-500 py-8">
            <p>{error || "No embedding data available"}</p>
            <Button onClick={fetchEmbeddings} className="mt-4">
              Retry
            </Button>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-4">
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="flex items-center gap-2">
              <Eye className="h-5 w-5" />
              Product Embeddings Visualization
            </CardTitle>
            <div className="flex gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setShowSettings(!showSettings)}
              >
                <Settings className="h-4 w-4 mr-1" />
                Settings
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={fetchEmbeddings}
              >
                <RefreshCw className="h-4 w-4 mr-1" />
                Refresh
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          {showSettings && (
            <div className="mb-4 p-4 bg-gray-50 rounded-lg">
              <div className="flex items-center gap-4">
                <div>
                  <label className="text-sm font-medium">Method</label>
                  <select
                    value={method}
                    onChange={(e) => setMethod(e.target.value as 'pca' | 'tsne')}
                    className="ml-2 p-1 border rounded"
                  >
                    <option value="pca">PCA</option>
                    <option value="tsne">t-SNE</option>
                  </select>
                </div>
              </div>
            </div>
          )}

          <div className="h-96">
            <ResponsiveContainer width="100%" height="100%">
              <ScatterChart
                data={data}
                margin={{ top: 20, right: 20, bottom: 20, left: 20 }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  type="number" 
                  dataKey="x" 
                  name="x"
                  label={{ value: 'X', position: 'insideBottom', offset: -5 }}
                />
                <YAxis 
                  type="number" 
                  dataKey="y" 
                  name="y"
                  label={{ value: 'Y', angle: -90, position: 'insideLeft' }}
                />
                <Tooltip 
                  cursor={{ strokeDasharray: '3 3' }}
                  content={({ active, payload }) => {
                    if (active && payload && payload.length) {
                      const point = payload[0].payload;
                      return (
                        <div className="bg-white p-3 border rounded shadow-lg">
                          <p className="font-semibold">{point.name}</p>
                          <p className="text-sm text-gray-600">Category: {point.category}</p>
                          <p className="text-sm text-gray-600">Price: ${point.price}</p>
                        </div>
                      );
                    }
                    return null;
                  }}
                />
                <Scatter 
                  dataKey="y" 
                  fill="#8884d8"
                  onClick={handlePointClick}
                >
                  {data.map((entry, index) => (
                    <Cell 
                      key={`cell-${index}`} 
                      fill={getCategoryColor(entry.category)}
                    />
                  ))}
                </Scatter>
              </ScatterChart>
            </ResponsiveContainer>
          </div>

          {/* Legend */}
          <div className="mt-4">
            <h4 className="text-sm font-medium mb-2">Categories</h4>
            <div className="flex flex-wrap gap-2">
              {[...new Set(data.map(d => d.category))].map((category, index) => (
                <div key={category} className="flex items-center gap-1">
                  <div 
                    className="w-3 h-3 rounded-full"
                    style={{ backgroundColor: getCategoryColor(category) }}
                  />
                  <span className="text-xs capitalize">{category}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Selected Point Details */}
          {selectedPoint && (
            <div className="mt-4 p-4 bg-blue-50 rounded-lg">
              <h4 className="font-semibold text-blue-900">Selected Product</h4>
              <p className="text-sm text-blue-700">Name: {selectedPoint.name}</p>
              <p className="text-sm text-blue-700">Category: {selectedPoint.category}</p>
              <p className="text-sm text-blue-700">Price: ${selectedPoint.price}</p>
              <p className="text-sm text-blue-700">Coordinates: ({selectedPoint.x.toFixed(2)}, {selectedPoint.y.toFixed(2)})</p>
            </div>
          )}

          {/* Summary Stats */}
          <div className="mt-4 grid grid-cols-2 gap-4 text-sm">
            <div>
              <span className="font-medium">Total Points:</span> {data.length}
            </div>
            <div>
              <span className="font-medium">Method:</span> {method.toUpperCase()}
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
