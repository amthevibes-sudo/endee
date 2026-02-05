# PDF Semantic Search Engine

A production-ready semantic search engine for PDF documents powered by **Endee Vector Database** and **Sentence Transformers**.

## Features

✨ **Semantic Search** - Find relevant content based on meaning, not just keywords  
📄 **PDF Processing** - Automatic text extraction and intelligent chunking  
🚀 **Fast & Scalable** - Powered by Endee vector database  
🎯 **High Accuracy** - Uses state-of-the-art sentence-transformers embeddings  
💻 **Rich CLI** - Beautiful command-line interface with interactive mode  
🔍 **Metadata Filtering** - Filter results by file, page, or custom metadata  

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   PDF Files │────▶│ PDF Processor│────▶│   Chunks    │
└─────────────┘     └──────────────┘     └─────────────┘
                                                │
                                                ▼
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Search    │◀────│    Endee     │◀────│  Embedder   │
│   Results   │     │   Database   │     │ (SentTrans) │
└─────────────┘     └──────────────┘     └─────────────┘
```

## Prerequisites

1. **Endee Server** running (default: `localhost:50051`)
2. **Python 3.8+**

## Installation

### 1. Install Dependencies

```bash
cd pdf_search
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Edit `.env`:
```env
ENDEE_HOST=localhost
ENDEE_PORT=50051
EMBEDDING_MODEL=all-MiniLM-L6-v2
EMBEDDING_DIM=384
CHUNK_SIZE=500
CHUNK_OVERLAP=50
```

### 3. Add PDF Files

Place your PDF files in the `pdfs/` directory (created automatically).

## Usage

### Command-Line Interface

#### 1. Ingest PDFs

```bash
python cli.py ingest
```

Or specify a custom directory:
```bash
python cli.py ingest --pdf-dir /path/to/pdfs
```

#### 2. Search

```bash
python cli.py search "your search query"
```

Options:
```bash
# Get top 10 results
python cli.py search "machine learning" --top-k 10

# Filter by specific file
python cli.py search "neural networks" --file "research_paper.pdf"
```

#### 3. Interactive Mode

```bash
python cli.py interactive
```

Start an interactive search session where you can run multiple queries.

#### 4. View Index Info

```bash
python cli.py info
```

Shows statistics about indexed documents.

#### 5. Reset Index

```bash
python cli.py reset
```

Deletes all indexed data (requires confirmation).

### Python API

```python
from search_engine import SemanticSearchEngine
from pathlib import Path

# Initialize
engine = SemanticSearchEngine()
engine.initialize()

# Ingest PDFs
engine.ingest_pdfs(Path("./pdfs"))

# Search
results = engine.search("machine learning algorithms", top_k=5)

for result in results:
    print(f"Score: {result['score']:.4f}")
    print(f"File: {result['metadata']['file_name']}")
    print(f"Page: {result['metadata']['page']}")
    print(f"Text: {result['metadata']['text'][:200]}...")
    print("-" * 80)
```

## Configuration

### Embedding Models

You can use different sentence-transformer models:

- `all-MiniLM-L6-v2` (default) - Fast, 384 dimensions
- `all-mpnet-base-v2` - Higher quality, 768 dimensions
- `multi-qa-mpnet-base-dot-v1` - Optimized for Q&A

Update `EMBEDDING_MODEL` in `.env` to change models.

### Chunking Strategy

Adjust chunking parameters in `.env`:

- `CHUNK_SIZE` - Characters per chunk (default: 500)
- `CHUNK_OVERLAP` - Overlapping characters (default: 50)

Larger chunks preserve more context but may reduce precision.

## Project Structure

```
pdf_search/
├── cli.py                  # Command-line interface
├── config.py              # Configuration management
├── embedder.py            # Embedding generation
├── endee_client.py        # Endee database client
├── pdf_processor.py       # PDF text extraction
├── search_engine.py       # Main search engine
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
├── README.md             # This file
├── pdfs/                 # PDF files (auto-created)
└── index/                # Index metadata (auto-created)
```

## How It Works

### 1. PDF Ingestion Pipeline

1. **Extract Text** - PyMuPDF extracts text from each PDF page
2. **Chunk Text** - Text is split into overlapping chunks (preserves context)
3. **Generate Embeddings** - Sentence-transformers creates vector embeddings
4. **Store in Endee** - Vectors and metadata stored in Endee database

### 2. Search Process

1. **Query Embedding** - User query converted to vector
2. **Vector Search** - Endee finds most similar vectors (cosine similarity)
3. **Rank Results** - Results ranked by similarity score
4. **Return Metadata** - Original text and metadata returned

## Performance Tips

1. **Batch Processing** - Embeddings generated in batches for efficiency
2. **GPU Acceleration** - Sentence-transformers uses GPU if available
3. **Chunking** - Optimal chunk size balances context vs. precision
4. **Model Selection** - Smaller models are faster, larger models more accurate

## Troubleshooting

### Endee Connection Failed

```bash
# Check if Endee is running
curl http://localhost:50051/health

# Update ENDEE_HOST and ENDEE_PORT in .env
```

### Out of Memory

```bash
# Use smaller embedding model
EMBEDDING_MODEL=all-MiniLM-L6-v2

# Reduce batch size in embedder.py
```

### No Results Found

```bash
# Check if PDFs were ingested
python cli.py info

# Re-ingest if needed
python cli.py reset
python cli.py ingest
```

## Advanced Usage

### Custom Metadata Filters

```python
# Search only in specific file
results = engine.search(
    "query",
    filter_by_file="document.pdf"
)
```

### Programmatic Access

```python
from endee_client import EndeeClient
from embedder import Embedder

# Direct Endee access
client = EndeeClient()
embedder = Embedder()

# Custom search
query_vec = embedder.embed_text("custom query")
results = client.search(query_vec, top_k=10)
```

## License

MIT License - See LICENSE file for details

## Contributing

Contributions welcome! Please open an issue or PR.

## Support

For issues or questions:
- Check existing issues
- Review Endee documentation
- Open a new issue with details

---

**Built with ❤️ using Endee Vector Database**
