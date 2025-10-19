"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Bar, BarChart, CartesianGrid, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis, Cell } from "recharts";
import { DollarSign, Package, Star, TrendingUp } from "lucide-react";
import { getAnalyticsMetrics, getCategoryAnalytics, getPriceAnalysis } from "@/lib/api";

interface AnalyticsMetrics {
  total_products: number;
  categories: Record<string, number>;
  category_insights: Record<string, any>;
  price_statistics: Record<string, number>;
  price_ranges: Record<string, number>;
  recommendation_insights: Record<string, any>;
}

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8', '#82CA9D'];

/**
 * Analytics widgets showing high-level system metrics.
 */
export default function MetricsDashboard() {
  const [metrics, setMetrics] = useState<AnalyticsMetrics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchMetrics();
  }, []);

  const fetchMetrics = async () => {
    try {
      setLoading(true);
      const data = await getAnalyticsMetrics();
      setMetrics(data);
    } catch (err) {
      setError("Failed to fetch analytics data");
      console.error("Error fetching metrics:", err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Analytics Dashboard</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-center h-64">
            <div className="animate-spin h-8 w-8 border-2 border-muted-foreground/30 border-t-muted-foreground rounded-full"></div>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (error || !metrics) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Analytics Dashboard</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center text-destructive py-8">
            <p>{error || "Failed to load analytics data"}</p>
            <Button onClick={fetchMetrics} className="mt-4" variant="ikarus">
              Retry
            </Button>
          </div>
        </CardContent>
      </Card>
    );
  }

  // Prepare data for charts
  const categoryData = Object.entries(metrics.categories).map(([name, value]) => ({
    name: name.charAt(0).toUpperCase() + name.slice(1),
    value,
  }));

  const priceRangeData = [
    { name: "Budget (<$200)", value: metrics.price_ranges.budget || 0 },
    { name: "Mid-range ($200-$800)", value: metrics.price_ranges.mid_range || 0 },
    { name: "Premium (>$800)", value: metrics.price_ranges.premium || 0 },
  ];

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrendingUp className="h-5 w-5" />
            Overview Metrics
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-primary">{metrics.total_products}</div>
              <div className="text-sm text-muted-foreground">Total Products</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-500">{Object.keys(metrics.categories).length}</div>
              <div className="text-sm text-muted-foreground">Categories</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-purple-500">
                ${Math.round(metrics.price_statistics.mean || 0)}
              </div>
              <div className="text-sm text-muted-foreground">Avg Price</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-orange-500">
                {Math.round((metrics.recommendation_insights.recommendation_accuracy || 0) * 100)}%
              </div>
              <div className="text-sm text-muted-foreground">Accuracy</div>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Package className="h-5 w-5" />
            Category Distribution
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={categoryData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {categoryData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <DollarSign className="h-5 w-5" />
            Price Range Distribution
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={priceRangeData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="value" fill="#8884d8" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Star className="h-5 w-5" />
            Price Statistics
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center">
              <div className="text-lg font-semibold text-green-500">
                ${Math.round(metrics.price_statistics.min || 0)}
              </div>
              <div className="text-sm text-muted-foreground">Min Price</div>
            </div>
            <div className="text-center">
              <div className="text-lg font-semibold text-red-500">
                ${Math.round(metrics.price_statistics.max || 0)}
              </div>
              <div className="text-sm text-muted-foreground">Max Price</div>
            </div>
            <div className="text-center">
              <div className="text-lg font-semibold text-primary">
                ${Math.round(metrics.price_statistics.mean || 0)}
              </div>
              <div className="text-sm text-muted-foreground">Average</div>
            </div>
            <div className="text-center">
              <div className="text-lg font-semibold text-purple-500">
                ${Math.round(metrics.price_statistics.median || 0)}
              </div>
              <div className="text-sm text-muted-foreground">Median</div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

