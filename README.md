# Gov_Support_RAG_Chatbot
This project can be used to easily know the government schemes and polices

AI-Powered Chatbot for MSME ONE Portal
Future Vision: Every entrepreneur in Andhra Pradesh—whether a first-time entrepreneur in a rural cluster or a seasoned manufacturer in an industrial park—should be able to access accurate, real-time information about government schemes, registrations, subsidies, and compliance through a multilingual AI assistant available 24/7.
Driving the State: This will ensure last-mile inclusion, reduce dependence on physical helpdesks, and create a culture of self-service, where entrepreneurs make informed decisions faster and with confidence.

## Existing Scenario
- MSME entrepreneurs often face delays and difficulties in accessing scheme information, application guidance, and regulatory resources.
- The AP MSME ONE Portal provides a centralized platform for schemes, policies, and resources, but users often struggle to navigate it, leading to low engagement and missed opportunities.
- Current support mechanisms rely on emails, helplines, or manual guidance, resulting in long response times and limited personalization.
- Entrepreneurs lack real-time, personalized assistance, which is critical for first-time founders and small businesses unfamiliar with government processes.

## Expected Solution
Seeking a multi-channel AI-powered chatbot solution that:
- User-friendly multilingual (Telugu and English) chatbot with Voice To Text feature that significantly enhances the overall user experience on the AP MSME ONE portal.
- Uses AI/ML to analyze queries and provide personalized recommendations based on user profiles and business needs.
- Allows users to track application statuses and receive timely updates on funding opportunities.
- Integrates analytics dashboards to track interactions, query trends, common concerns, and user satisfaction metrics.
- Must be cloud-based, mobile-friendly, and accessible across devices, ensuring entrepreneurs from urban and rural areas can use it.
- Include features for iterative improvement based on feedback and usage analytics.
- Must adhere to data privacy and security regulations, ensuring sensitive user information is protected.

## Outcomes
- Improved access to information and resources for MSMEs, leading to higher engagement with government programs.
- Faster, more efficient responses to user queries, freeing human resources for complex tasks.
- Increased trust and transparency in government services through timely updates and responsive support.
- Data-driven insights to continuously refine services, aligning offerings with user needs.

[dataset](https://drive.google.com/drive/folders/1edexdjnka99Fa56Y-1y2fanbtiBKlLxq?usp=drive_link)


# Gov Support RAG Chatbot

An AI-powered chatbot for the AP MSME ONE Portal that helps entrepreneurs access government schemes, policies, and subsidies through natural language queries.

---

## Project Flow

```
                        ┌─────────────────────────────────────────────────────┐
                        │                   DATA INGESTION                     │
                        │                                                       │
                        │  PDF Files                                            │
                        │  (Guidelines / Policies / RAMP)                      │
                        │       │                                               │
                        │       ▼                                               │
                        │  ┌─────────────┐    ┌──────────────┐                │
                        │  │   Docling    │───▶│  Metadata    │                │
                        │  │   Parser     │    │  Extractor   │                │
                        │  └─────────────┘    └──────┬───────┘                │
                        │       │                     │                        │
                        │       ▼                     ▼                        │
                        │  ┌─────────┐  ┌──────────────────┐                  │
                        │  │  Text   │  │  PostgreSQL       │                  │
                        │  │ Chunks  │─▶│  documents table  │                  │
                        │  └────┬────┘  │  chunks table     │                  │
                        │       │       └──────────────────┘                   │
                        │  ┌────┴────┐                                         │
                        │  │ Tables  │─▶ MongoDB (tables collection)           │
                        │  └─────────┘                                         │
                        │  ┌─────────┐                                         │
                        │  │ Images  │─▶ MongoDB (images collection)           │
                        │  └─────────┘                                         │
                        └─────────────────────────────────────────────────────┘
                                              │
                                              ▼
                        ┌─────────────────────────────────────────────────────┐
                        │                  EMBEDDING PIPELINE                  │
                        │                                                       │
                        │  PostgreSQL chunks (is_embedded = FALSE)             │
                        │       │                                               │
                        │       ▼                                               │
                        │  BGE-small-en-v1.5 (sentence-transformers)           │
                        │       │                                               │
                        │       ▼                                               │
                        │  Pinecone Vector Index                               │
                        │  (chunk_text, doc_id, category,                      │
                        │   document_title, page_number)                       │
                        │       │                                               │
                        │  PostgreSQL chunks (is_embedded = TRUE)              │
                        └─────────────────────────────────────────────────────┘
                                              │
                                              ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              RETRIEVAL PIPELINE                                  │
│                                                                                  │
│   User Question                                                                  │
│        │                                                                         │
│        ├──────────────────────────┬──────────────────────────┐                  │
│        │                          │                          │                   │
│        ▼                          ▼                          ▼                   │
│   BGE Embedding            BM25 Index                  Guardrails               │
│   (Dense Search)          (Sparse Search)           (Input Validation)          │
│        │                          │                                              │
│        ▼                          ▼                                              │
│   Pinecone Query          Keyword Matches                                        │
│   (Top K results)         (Top K results)                                        │
│        │                          │                                              │
│        └──────────────┬───────────┘                                             │
│                        │                                                         │
│                        ▼                                                         │
│              Reciprocal Rank Fusion                                              │
│              (RRF — combines both)                                               │
│                        │                                                         │
│                        ▼                                                         │
│              CrossEncoder Reranker                                               │
│         (ms-marco-MiniLM-L-6-v2)                                                │
│                        │                                                         │
│                        ▼                                                         │
│              Top K Final Chunks                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
                                              │
                                              ▼
                        ┌─────────────────────────────────────────────────────┐
                        │                  GENERATION PIPELINE                 │
                        │                                                       │
                        │  Conversation History (PostgreSQL)                   │
                        │       │                                               │
                        │       ▼                                               │
                        │  Prompt Template                                      │
                        │  ┌─────────────────────────────────┐                 │
                        │  │ System: AP MSME assistant        │                 │
                        │  │ Context: {retrieved chunks}      │                 │
                        │  │ History: {last 10 messages}      │                 │
                        │  │ Question: {user question}        │                 │
                        │  └─────────────────────────────────┘                 │
                        │       │                                               │
                        │       ▼                                               │
                        │  Groq API (Llama 3.1)                                │
                        │       │                                               │
                        │       ▼                                               │
                        │  Answer + Citations                                   │
                        │  (document_title, page_number, category)             │
                        └─────────────────────────────────────────────────────┘
                                              │
                                              ▼
                        ┌─────────────────────────────────────────────────────┐
                        │                    API LAYER                          │
                        │                                                       │
                        │  FastAPI                                              │
                        │  ├── POST /chat      → RAG chat endpoint             │
                        │  ├── POST /ingest    → trigger ingestion             │
                        │  ├── POST /embed     → trigger embedding             │
                        │  ├── GET  /ingest/status → ingestion logs            │
                        │  └── GET  /health    → health check                  │
                        │                                                       │
                        │  Middleware Stack                                     │
                        │  ├── CORS                                            │
                        │  ├── Rate Limiting (SlowAPI)                         │
                        │  ├── Request Logging (Loguru)                        │
                        │  └── Global Exception Handler                        │
                        └─────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| API Framework | FastAPI |
| PDF Parsing | Docling |
| Embeddings | BGE-small-en-v1.5 (sentence-transformers) |
| Vector Store | Pinecone |
| Keyword Search | BM25 (rank-bm25) |
| Reranker | CrossEncoder ms-marco-MiniLM-L-6-v2 |
| LLM | Groq (Llama 3.1) |
| Relational DB | PostgreSQL (asyncpg) |
| Document Store | MongoDB (PyMongo async) |
| Logging | Loguru |
| Rate Limiting | SlowAPI |
| Containerisation | Docker + Docker Compose |

---

## Project Structure

```
Gov_Support_RAG_Chatbot/
├── app/
│   ├── api/
│   │   └── routes.py           # API endpoints
│   ├── core/
│   │   ├── config.py           # Pydantic settings
│   │   └── logger.py           # Loguru setup
│   ├── db/
│   │   ├── postgres.py         # asyncpg connection pool
│   │   └── mongo.py            # MongoDB async client
│   ├── middleware/
│   │   ├── cors.py
│   │   ├── logging_middleware.py
│   │   ├── rate_limiter.py
│   │   └── exception_handler.py
│   ├── rag/
│   │   ├── ingest.py           # Docling parsing pipeline
│   │   ├── embeddings.py       # BGE embeddings + Pinecone upsert
│   │   ├── hybrid_search.py    # BM25 index + search
│   │   ├── retrieval.py        # Vector + BM25 + RRF + reranker
│   │   ├── reranker.py         # CrossEncoder reranking
│   │   ├── generation.py       # Groq LLM call
│   │   ├── guardrails.py       # Input validation + relevance check
│   │   ├── memory.py           # Conversation history (PostgreSQL)
│   │   ├── pipeline.py         # RAG orchestrator
│   │   └── prompt_templates.py # Prompt builder with history
│   ├── utils/
│   │   └── helper.py           # Shared utilities
│   └── schemas.py
│       
├── tests/
├── notebooks/
├── infra/
├── main.py                     # FastAPI app entry point
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## Setup

### Prerequisites
- Python 3.11
- Docker Desktop
- PostgreSQL (via Docker or local)
- MongoDB Atlas account
- Pinecone account
- Groq API key

### Local Development

```bash
# Clone the repository
git clone https://github.com/Root-Minus-One/Gov_Support_RAG_Chatbot.git
cd Gov_Support_RAG_Chatbot

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env
# Fill in your actual values in .env

# Run the app
uvicorn main:app --reload
```

### Docker

```bash
# Build and run all services
docker-compose up --build

# Stop all services
docker-compose down
```
---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/ingest` | Ingest PDFs from folder |
| GET | `/ingest/status` | Ingestion log |
| POST | `/embed` | Run embedding pipeline |
| POST | `/chat` | RAG chat endpoint |

### Chat Request

```json
{
  "question": "What are the eligibility criteria for MSME registration?",
  "category": "Guidelines",
  "session_id": "optional-uuid-for-memory"
}
```

### Chat Response

```json
{
  "session_id": "uuid",
  "question": "What are the eligibility criteria?",
  "answer": "According to the guidelines...",
  "citations": [
    {
      "document_title": "MSME Registration Guidelines",
      "category": "Guidelines",
      "page_number": 3,
      "relevance_score": 0.923
    }
  ]
}
```

---

## RAG Pipeline

```
Query → Input Guardrails → Hybrid Retrieval → Reranking → Generation → Response
              │                   │                │             │
         Validate input     BM25 + Vector      CrossEncoder   Groq LLM
         Injection check    RRF Fusion         Reranker       + History
```

---

## Future Improvements

- [ ] Tool calling for live scheme updates
- [ ] Telugu language support
- [ ] Conversation summarization for long sessions