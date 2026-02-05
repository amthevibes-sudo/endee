# Deployment Guide: Hybrid Cloud (Recommended)

This gives you the best of both worlds:
1.  **Frontend**: **Vercel** (Fast, global CDN, optimized for React).
2.  **API**: **Render** (Hosts Python Logic + Embeddings).
3.  **Database**: **Render** (Hosts Endee Vector DB).

## Architecture
```mermaid
graph TD
    User[User Browser] -->|Visit URL| Vercel[Frontend (Vercel)]
    Vercel -->|API Calls (fetch)| API[Python API (Render)]
    API -->|Vectors| DB[Endee DB (Render)]
```

---

## Part 1: Deploy Endee DB (Render)
1.  Deploy the **Root Directory** to Render as a "Web Service".
2.  **Name**: `endee-db`.
3.  **Docker**: Yes.
4.  Copy the internal address (e.g., `endee-db:8080`) or public URL if needed.

## Part 2: Deploy Python API (Render)
1.  Deploy the **`pdf_search`** directory to Render as a "Web Service".
2.  **Name**: `pdf-search-api`.
3.  **Docker**: Yes.
4.  **Env Vars**:
    - `ENDEE_HOST`: URL of Part 1 (e.g., `endee-db-xyz.onrender.com`).
    - `ENDEE_PORT`: `443` (for https) or `80`.
5.  Copy the **API URL** (e.g., `https://pdf-search-api.onrender.com`).

## Part 3: Deploy Frontend (Vercel)
1.  Import repo to Vercel.
2.  **Root Directory**: Edit to `pdf_search/frontend`.
3.  **Environment Variables**:
    - `VITE_API_URL`: Paste the **API URL** from Part 2 (e.g., `https://pdf-search-api.onrender.com`).
4.  **Deploy**.

---

## Why this is better?
- **Faster UI**: Vercel is much faster at serving static assets than Python/Uvicorn.
- **Cheaper**: You can often fit the API + DB on Render Free Tier separately (or scaling them independently).
- **Separation**: Frontend crashes don't kill the API, and vice-versa.
