"use client";

import { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Send, Sparkles, TrendingUp, Filter } from "lucide-react";
import ProductCard from "./ProductCard";
import { getRecommendations, getTrendingProducts } from "@/lib/api";

interface Message {
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

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

export default function ProductRecommendationChat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [recommendations, setRecommendations] = useState<Product[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [showFilters, setShowFilters] = useState(false);
  const [filters, setFilters] = useState({
    category: "",
    priceMin: "",
    priceMax: "",
  });
  const scrollAreaRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollAreaRef.current) {
      scrollAreaRef.current.scrollTop = scrollAreaRef.current.scrollHeight;
    }
  }, [messages, recommendations]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage: Message = {
      role: "user",
      content: input,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const response = await getRecommendations({
        query: input,
        top_k: 5,
        category_filter: filters.category || undefined,
        price_min: filters.priceMin ? parseFloat(filters.priceMin) : undefined,
        price_max: filters.priceMax ? parseFloat(filters.priceMax) : undefined,
      });

      const assistantMessage: Message = {
        role: "assistant",
        content: `Found ${response.recommendations.length} recommendations for "${input}"`,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
      setRecommendations(response.recommendations);
    } catch (error) {
      const errorMessage: Message = {
        role: "assistant",
        content: "Sorry, I couldn't find recommendations. Please try again.",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleTrending = async () => {
    setIsLoading(true);
    try {
      const response = await getTrendingProducts(5);
      setRecommendations(response.trending_products);
      
      const message: Message = {
        role: "assistant",
        content: "Here are the trending products right now:",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, message]);
    } catch (error) {
      console.error("Error fetching trending products:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="max-w-6xl mx-auto">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Chat Interface */}
        <div className="lg:col-span-2">
          <Card className="h-[600px] flex flex-col">
            <CardHeader className="bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-t-lg">
              <CardTitle className="flex items-center gap-2">
                <Sparkles className="h-5 w-5" />
                Product Recommendation Chat
              </CardTitle>
            </CardHeader>
            <CardContent className="flex-1 flex flex-col p-0">
              {/* Messages */}
              <div 
                ref={scrollAreaRef}
                className="flex-1 p-4 overflow-y-auto space-y-4"
              >
                {messages.length === 0 && (
                  <div className="text-center text-gray-500 py-8">
                    <p className="text-lg mb-2">Welcome to ProductRec!</p>
                    <p>Ask me to find furniture like "modern sofas under $1000" or "minimalist desks"</p>
                  </div>
                )}
                
                {messages.map((message, index) => (
                  <div
                    key={index}
                    className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}
                  >
                    <div
                      className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                        message.role === "user"
                          ? "bg-blue-500 text-white"
                          : "bg-gray-100 text-gray-800"
                      }`}
                    >
                      <p className="text-sm">{message.content}</p>
                      <p className="text-xs opacity-70 mt-1">
                        {message.timestamp.toLocaleTimeString()}
                      </p>
                    </div>
                  </div>
                ))}
                
                {isLoading && (
                  <div className="flex justify-start">
                    <div className="bg-gray-100 text-gray-800 px-4 py-2 rounded-lg">
                      <div className="flex items-center gap-2">
                        <div className="animate-spin h-4 w-4 border-2 border-gray-300 border-t-gray-600 rounded-full"></div>
                        <span>Finding recommendations...</span>
                      </div>
                    </div>
                  </div>
                )}
              </div>

              {/* Input Area */}
              <div className="p-4 border-t bg-gray-50">
                <div className="flex gap-2">
                  <Input
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Ask for furniture recommendations..."
                    className="flex-1"
                    disabled={isLoading}
                  />
                  <Button
                    onClick={handleSend}
                    disabled={isLoading || !input.trim()}
                    className="bg-blue-500 hover:bg-blue-600"
                  >
                    <Send className="h-4 w-4" />
                  </Button>
                </div>
                
                {/* Quick Actions */}
                <div className="flex gap-2 mt-3">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={handleTrending}
                    disabled={isLoading}
                    className="flex items-center gap-1"
                  >
                    <TrendingUp className="h-4 w-4" />
                    Trending
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setShowFilters(!showFilters)}
                    className="flex items-center gap-1"
                  >
                    <Filter className="h-4 w-4" />
                    Filters
                  </Button>
                </div>

                {/* Filters */}
                {showFilters && (
                  <div className="mt-3 p-3 bg-white rounded-lg border">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                      <div>
                        <label className="text-sm font-medium">Category</label>
                        <select
                          value={filters.category}
                          onChange={(e) => setFilters({...filters, category: e.target.value})}
                          className="w-full mt-1 p-2 border rounded-md"
                        >
                          <option value="">All Categories</option>
                          <option value="sofa">Sofa</option>
                          <option value="chair">Chair</option>
                          <option value="table">Table</option>
                          <option value="bed">Bed</option>
                          <option value="desk">Desk</option>
                          <option value="storage">Storage</option>
                        </select>
                      </div>
                      <div>
                        <label className="text-sm font-medium">Min Price</label>
                        <Input
                          type="number"
                          placeholder="0"
                          value={filters.priceMin}
                          onChange={(e) => setFilters({...filters, priceMin: e.target.value})}
                          className="mt-1"
                        />
                      </div>
                      <div>
                        <label className="text-sm font-medium">Max Price</label>
                        <Input
                          type="number"
                          placeholder="1000"
                          value={filters.priceMax}
                          onChange={(e) => setFilters({...filters, priceMax: e.target.value})}
                          className="mt-1"
                        />
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Recommendations */}
        <div className="lg:col-span-1">
          <Card className="h-[600px]">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Sparkles className="h-5 w-5" />
                Recommendations
              </CardTitle>
            </CardHeader>
            <CardContent className="overflow-y-auto">
              {recommendations.length === 0 ? (
                <div className="text-center text-gray-500 py-8">
                  <p>No recommendations yet.</p>
                  <p className="text-sm">Try asking for furniture recommendations!</p>
                </div>
              ) : (
                <div className="space-y-4">
                  {recommendations.map((product) => (
                    <ProductCard key={product.id} product={product} />
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
