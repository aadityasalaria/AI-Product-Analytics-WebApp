# Product Recommendation Web App

An AI/ML-driven furniture product recommendation system with creative GenAI descriptions, built with FastAPI, Next.js, and Pinecone vector database.

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Vector DB     │
│   (Next.js)     │◄──►│   (FastAPI)     │◄──►│   (Pinecone)    │
│                 │    │                 │    │                 │
│ • Chat UI       │    │ • Product API   │    │ • Embeddings    │
│ • Analytics     │    │ • GenAI Service │    │ • Similarity    │
│ • Visualizations│    │ • ML Services   │    │ • Search        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Features

- **Smart Recommendations**: Metadata + embedding-based product suggestions
- **GenAI Descriptions**: Creative product descriptions using GPT-2
- **Interactive Chat**: Natural language product queries
- **Analytics Dashboard**: Embedding visualizations and insights
- **Vector Search**: Pinecone-powered similarity search
- **Real-time API**: FastAPI backend with comprehensive endpoints

## 📋 Prerequisites

- Python 3.9+
- Node.js 18+
- Pinecone account (free tier available)
- Git

## 🛠️ Setup Instructions

### 1. Clone and Setup

```bash
git clone <your-repo-url>
cd Product-Recommendation-WebApp
```

### 2. Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env
```

### 3. Environment Configuration

Create `backend/.env` with your API keys:

```env
# Pinecone Configuration
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=us-east-1
PINECONE_INDEX_NAME=furniture-products

# Optional: OpenAI for enhanced features
OPENAI_API_KEY=your_openai_api_key

# Model Configuration
EMBEDDING_MODEL=all-MiniLM-L6-v2
GENAI_MODEL=gpt2
EMBEDDING_DIMENSION=384
DEFAULT_TOP_K=5
SIMILARITY_THRESHOLD=0.7

# Directories
UPLOAD_DIRECTORY=uploads/
DATASET_DIRECTORY=datasets/
```

### 4. Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env.local
```

Create `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 5. Run the Application

**Terminal 1 - Backend:**
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Visit: http://localhost:3000

## 📊 Dataset Format

Your furniture dataset should be a CSV or JSON file with these columns:

```csv
id,name,category,price,description,image_url
1,Modern Sofa,sofa,899.99,Comfortable modern sofa for living room,https://example.com/sofa.jpg
2,Office Chair,chair,299.99,Ergonomic office chair with lumbar support,https://example.com/chair.jpg
```

**Required fields:**
- `id`: Unique product identifier
- `name`: Product name
- `category`: Product category (sofa, chair, table, bed, desk, storage)
- `price`: Product price (numeric)
- `description`: Product description

**Optional fields:**
- `image_url`: Product image URL

## 🔧 API Endpoints

### Products
- `POST /api/products/upload` - Upload dataset
- `GET /api/products/all` - List all products
- `GET /api/products/{id}` - Get specific product
- `POST /api/products/recommend` - Get recommendations
- `GET /api/products/{id}/similar` - Get similar products
- `GET /api/products/category/{category}` - Get products by category
- `GET /api/products/trending` - Get trending products
- `POST /api/products/generate-description` - Generate AI description

### Analytics
- `GET /api/analytics/metrics` - Get analytics metrics
- `GET /api/analytics/embeddings-2d` - Get 2D embeddings for visualization
- `GET /api/analytics/similarity/{id}` - Analyze product similarity
- `GET /api/analytics/quality` - Get recommendation quality metrics

## 🧪 Testing the System

### 1. Upload Dataset
```bash
curl -X POST "http://localhost:8000/api/products/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_dataset.csv"
```

### 2. Get Recommendations
```bash
curl -X POST "http://localhost:8000/api/products/recommend" \
  -H "Content-Type: application/json" \
  -d '{"query": "modern sofa under 1000", "top_k": 5}'
```

### 3. Generate AI Description
```bash
curl -X POST "http://localhost:8000/api/products/generate-description" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "1", "enhance_existing": false}'
```

## 📈 Analytics & ML Notebooks

Explore the Jupyter notebooks in `models/notebooks/`:

1. **01_data_exploration.ipynb** - Dataset analysis and insights
2. **02_embedding_generation.ipynb** - Embedding creation and visualization
3. **03_recommendation_testing.ipynb** - Recommendation algorithm testing

Run notebooks:
```bash
cd models/notebooks
jupyter notebook
```

## 🎨 Frontend Features

### Recommendation Page
- Interactive chat interface
- Real-time product recommendations
- AI-generated descriptions
- Filter by category and price
- Trending products

### Analytics Page
- Embedding visualization (PCA/t-SNE)
- Category distribution charts
- Price analysis
- Recommendation quality metrics

## 🚀 Deployment

### Backend (Railway/Render)
1. Connect your GitHub repository
2. Set environment variables
3. Deploy automatically

### Frontend (Vercel)
1. Connect repository to Vercel
2. Set `NEXT_PUBLIC_API_URL` to your backend URL
3. Deploy

### Environment Variables for Production
```env
# Backend
PINECONE_API_KEY=your_production_key
PINECONE_ENVIRONMENT=us-east-1

# Frontend
NEXT_PUBLIC_API_URL=https://your-backend-url.com
```

## 🔍 Troubleshooting

### Common Issues

1. **Pinecone Connection Error**
   - Verify API key and environment
   - Check index name matches configuration

2. **Model Loading Issues**
   - Ensure sufficient disk space for model downloads
   - Check internet connection for first-time model loading

3. **CORS Errors**
   - Verify frontend URL in backend CORS settings
   - Check API URL configuration

4. **Embedding Generation Slow**
   - First-time model loading takes time
   - Consider using GPU for faster processing

### Performance Tips

- Use smaller embedding models for faster processing
- Implement caching for frequently accessed products
- Consider batch processing for large datasets
- Use connection pooling for database operations

## 📚 Technology Stack

**Backend:**
- FastAPI - Web framework
- Sentence-Transformers - Embeddings
- Hugging Face Transformers - GenAI
- Pinecone - Vector database
- Scikit-learn - ML utilities

**Frontend:**
- Next.js 14 - React framework
- TypeScript - Type safety
- Tailwind CSS - Styling
- Recharts - Data visualization
- Radix UI - Component library

**ML/Data:**
- Pandas - Data manipulation
- NumPy - Numerical computing
- Matplotlib/Seaborn - Visualization
- Jupyter - Interactive notebooks

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the API documentation
3. Open an issue on GitHub
4. Check the Jupyter notebooks for examples

## 🔮 Future Enhancements

- [ ] Image-based recommendations using CLIP
- [ ] User preference learning
- [ ] A/B testing framework
- [ ] Real-time recommendation updates
- [ ] Multi-language support
- [ ] Advanced filtering options
- [ ] Recommendation explanation system
- [ ] Performance monitoring dashboard
