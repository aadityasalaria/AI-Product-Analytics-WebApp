// Central API base; override via NEXT_PUBLIC_API_URL at runtime
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface RecommendationRequest {
  query: string;
  top_k?: number;
  category_filter?: string;
  price_min?: number;
  price_max?: number;
}

export interface RecommendationResponse {
  query: string;
  recommendations: Product[];
  total: number;
  filters_applied: {
    category?: string;
    price_min?: number;
    price_max?: number;
  };
}

export interface Product {
  id: string;
  name: string;
  category: string;
  price: number;
  description: string;
  image_url?: string;
  similarity_score?: number;
  recommendation_reason?: string;
}

export interface GenerateDescriptionRequest {
  product_id: string;
  enhance_existing: boolean;
}

export interface GenerateDescriptionResponse {
  product_id: string;
  original_description: string;
  generated_description: string;
  enhancement_type: string;
}

export interface TrendingResponse {
  trending_products: Product[];
  total: number;
}

export interface AnalyticsMetrics {
  total_products: number;
  categories: Record<string, number>;
  category_insights: Record<string, any>;
  price_statistics: Record<string, number>;
  price_ranges: Record<string, number>;
  recommendation_insights: Record<string, any>;
}

export interface Embedding2DResponse {
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

// API Functions
/** Fetch recommendations for a user query. */
export async function getRecommendations(request: RecommendationRequest): Promise<RecommendationResponse> {
  const response = await fetch(`${API_BASE_URL}/api/products/recommend`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response.json();
}

/** Fetch trending products (simple proxy metric). */
export async function getTrendingProducts(top_k: number = 10): Promise<TrendingResponse> {
  const response = await fetch(`${API_BASE_URL}/api/products/trending?top_k=${top_k}`);

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response.json();
}

/** Fetch products similar to a given product. */
export async function getSimilarProducts(productId: string, top_k: number = 5): Promise<{similar_products: Product[]}> {
  const response = await fetch(`${API_BASE_URL}/api/products/${productId}/similar?top_k=${top_k}`);

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response.json();
}

/** Fetch products within a category with optional price filters. */
export async function getCategoryProducts(category: string, top_k: number = 10, priceMin?: number, priceMax?: number): Promise<{products: Product[]}> {
  const params = new URLSearchParams({
    top_k: top_k.toString(),
    ...(priceMin && { price_min: priceMin.toString() }),
    ...(priceMax && { price_max: priceMax.toString() }),
  });

  const response = await fetch(`${API_BASE_URL}/api/products/category/${category}?${params}`);

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response.json();
}

/** Ask backend to generate/enhance a product description. */
export async function generateProductDescription(request: GenerateDescriptionRequest): Promise<GenerateDescriptionResponse> {
  const response = await fetch(`${API_BASE_URL}/api/products/generate-description`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response.json();
}

/** Fetch a paginated list of products. */
export async function getAllProducts(limit: number = 100, offset: number = 0): Promise<{products: Product[]}> {
  const response = await fetch(`${API_BASE_URL}/api/products/all?limit=${limit}&offset=${offset}`);

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response.json();
}

/** Fetch a single product by id. */
export async function getProduct(productId: string): Promise<Product> {
  const response = await fetch(`${API_BASE_URL}/api/products/${productId}`);

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response.json();
}

// Analytics API Functions
/** Analytics: overall metrics */
export async function getAnalyticsMetrics(): Promise<AnalyticsMetrics> {
  const response = await fetch(`${API_BASE_URL}/api/analytics/metrics`);

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response.json();
}

/** Analytics: 2D embedding coordinates for visualization */
export async function getEmbeddings2D(method: string = 'pca', nComponents: number = 2): Promise<Embedding2DResponse> {
  const response = await fetch(`${API_BASE_URL}/api/analytics/embeddings-2d?method=${method}&n_components=${nComponents}`);

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response.json();
}

/** Analytics: similarity breakdown for a product */
export async function getSimilarityAnalysis(productId: string): Promise<any> {
  const response = await fetch(`${API_BASE_URL}/api/analytics/similarity/${productId}`);

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response.json();
}

/** Analytics: aggregate recommendation quality */
export async function getRecommendationQuality(): Promise<any> {
  const response = await fetch(`${API_BASE_URL}/api/analytics/quality`);

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response.json();
}

/** Analytics: category insights */
export async function getCategoryAnalytics(): Promise<any> {
  const response = await fetch(`${API_BASE_URL}/api/analytics/categories`);

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response.json();
}

/** Analytics: price distributions */
export async function getPriceAnalysis(): Promise<any> {
  const response = await fetch(`${API_BASE_URL}/api/analytics/price-analysis`);

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response.json();
}

// Upload function for dataset
/** Upload a CSV/JSON dataset to the backend. */
export async function uploadDataset(file: File): Promise<any> {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_BASE_URL}/api/products/upload`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response.json();
}

