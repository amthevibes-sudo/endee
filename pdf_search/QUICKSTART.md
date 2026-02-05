# Quick Start Guide - PDF Semantic Search

## 🚀 Getting Started in 3 Steps

### Step 1: Setup Environment

**Command Prompt:**
```batch
setup.bat
```

**PowerShell:**
```powershell
.\setup.bat
# If you get a script execution error, run:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

### Step 2: Start Endee Server

Make sure Endee is running on `localhost:50051` (default).

**Using Docker:**
```bash
cd ..  # Go to Endee root directory
docker-compose up
```

**Or update `.env` if Endee is running elsewhere:**
```env
ENDEE_HOST=your-endee-host
ENDEE_PORT=50051
```

### Step 3: Add PDFs and Search!

**Activate virtual environment:**
- Command Prompt: `activate.bat`
- PowerShell: `.\activate.ps1`

**Then run commands:**
```powershell
# Ingest your PDFs
python cli.py ingest

# Search!
python cli.py search "your query here"
```

---

## 📖 Detailed Usage

### CLI Commands

#### 1. Ingest PDFs
```bash
# Ingest all PDFs from pdfs/ directory
python cli.py ingest

# Ingest from custom directory
python cli.py ingest --pdf-dir C:\path\to\pdfs
```

#### 2. Search
```bash
# Basic search (returns top 5 results)
python cli.py search "machine learning algorithms"

# Get more results
python cli.py search "neural networks" --top-k 10

# Filter by specific file
python cli.py search "data preprocessing" --file "research_paper.pdf"
```

#### 3. Interactive Mode
```bash
python cli.py interactive
```
Type queries and get instant results. Type `quit` to exit.

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

---

## 🐍 Python API Usage

```python
from search_engine import SemanticSearchEngine
from pathlib import Path

# Initialize
engine = SemanticSearchEngine()
engine.initialize()

# Ingest PDFs
engine.ingest_pdfs(Path("./pdfs"))

# Search
results = engine.search("machine learning", top_k=5)

# Process results
for result in results:
    metadata = result['metadata']
    print(f"File: {metadata['file_name']}")
    print(f"Page: {metadata['page']}")
    print(f"Score: {result['score']:.4f}")
    print(f"Text: {metadata['text'][:200]}...")
    print("-" * 80)
```

---

## ⚙️ Configuration

Edit `.env` file:

```env
# Endee connection
ENDEE_HOST=localhost
ENDEE_PORT=50051

# Embedding model (options below)
EMBEDDING_MODEL=all-MiniLM-L6-v2
EMBEDDING_DIM=384

# Text chunking
CHUNK_SIZE=500
CHUNK_OVERLAP=50
```

### Available Embedding Models

| Model | Dimension | Speed | Quality |
|-------|-----------|-------|---------|
| `all-MiniLM-L6-v2` | 384 | ⚡⚡⚡ Fast | ⭐⭐ Good |
| `all-mpnet-base-v2` | 768 | ⚡⚡ Medium | ⭐⭐⭐ Best |
| `multi-qa-mpnet-base-dot-v1` | 768 | ⚡⚡ Medium | ⭐⭐⭐ Best for Q&A |

---

## 🎯 Example Workflow

```bash
# 1. Activate environment
activate.bat

# 2. Add PDFs to pdfs/ folder
# (Copy your PDF files here)

# 3. Ingest
python cli.py ingest

# Output:
# ============================================================
# PDF INGESTION PIPELINE
# ============================================================
# 
# Step 1: Extracting text from PDFs...
# Processing: research_paper.pdf
#   → Extracted 45 chunks
# Processing: tutorial.pdf
#   → Extracted 32 chunks
# 
# ✓ Extracted 77 total chunks from PDFs
# ...

# 4. Search
python cli.py search "deep learning optimization"

# 5. Interactive mode for multiple queries
python cli.py interactive
```

---

## 🔧 Troubleshooting

### "Failed to initialize Endee collection"
- Check if Endee server is running: `curl http://localhost:50051/health`
- Verify `ENDEE_HOST` and `ENDEE_PORT` in `.env`

### "No PDF files found"
- Make sure PDFs are in the `pdfs/` directory
- Or specify custom directory: `python cli.py ingest --pdf-dir C:\path\to\pdfs`

### Out of Memory
- Use smaller model: `EMBEDDING_MODEL=all-MiniLM-L6-v2`
- Reduce chunk size: `CHUNK_SIZE=300`

### Slow Performance
- Use GPU if available (sentence-transformers auto-detects)
- Reduce batch size in `embedder.py`

---

## 📁 Project Structure

```
pdf_search/
├── cli.py              # Command-line interface
├── config.py           # Configuration
├── embedder.py         # Embedding generation
├── endee_client.py     # Endee database client
├── pdf_processor.py    # PDF processing
├── search_engine.py    # Main search engine
├── quickstart.py       # Demo script
├── requirements.txt    # Dependencies
├── setup.bat           # Setup script
├── activate.bat        # Activation script
├── .env                # Configuration (create from .env.example)
├── pdfs/               # Place PDF files here
└── index/              # Index metadata (auto-created)
```

---

## 🎓 How It Works

1. **PDF Processing**: Extract text from PDFs using PyMuPDF
2. **Chunking**: Split text into overlapping chunks (preserves context)
3. **Embedding**: Convert chunks to vectors using sentence-transformers
4. **Storage**: Store vectors in Endee with metadata
5. **Search**: Convert query to vector, find similar vectors in Endee
6. **Results**: Return ranked results with original text and metadata

---

## 💡 Tips

- **Chunk Size**: Larger chunks (800-1000) for broad context, smaller (300-500) for precise matching
- **Overlap**: 10-20% overlap helps maintain context across chunks
- **Model Selection**: Start with `all-MiniLM-L6-v2`, upgrade to `all-mpnet-base-v2` for better quality
- **Batch Processing**: Process multiple PDFs at once for efficiency

---

## 🆘 Need Help?

1. Check the [README.md](README.md) for detailed documentation
2. Run `python cli.py --help` for command help
3. Use `python quickstart.py` for a demo

---

**Happy Searching! 🔍**
