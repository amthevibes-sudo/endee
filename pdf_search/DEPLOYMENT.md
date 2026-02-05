# Deployment Guide: Split Hosting (Recommended)

This guide splits the application into two parts for easier deployment:
1.  **Frontend (React)**: Hosted on **Vercel**.
2.  **Backend (Python API)**: Hosted on **Railway** (or PythonAnywhere).

## Prerequisites
- **Endee Server**: Running on your Mac.
- **Localtunnel**: Running on your Mac to expose Endee (`npx localtunnel --port 8080`).
- **GitHub**: You must have this code pushed to GitHub.

---

## Part 1: Deploy Backend (Railway)

1.  **Sign up/Login** to [Railway.app](https://railway.app/).
2.  **New Project** > **Deploy from GitHub repo**.
3.  Select this repository.
4.  Railway will auto-detect the `requirements.txt` and `Procfile`.
5.  **Variables**: Go to the **Settings/Variables** tab for the new service and add:
    - `ENDEE_HOST`: `<your-localtunnel-url>` (e.g., `calm-zebra-45.loca.lt`) - *Remove https://*
    - `ENDEE_PORT`: `80` (or `443` if usage HTTPS)
    - `PORT`: `8000` (Railway provides this automatically usually, but good to be safe)
6.  **Public Networking**: Go to **Settings** > **Networking** and Generate a Domain.
    - Copy this URL (e.g., `web-production-1234.up.railway.app`). **This is your BACKEND_URL.**

---

## Part 2: Deploy Frontend (Vercel)

1.  **Sign up/Login** to [Vercel.com](https://vercel.com/).
2.  **Add New Framework Project**.
3.  Import from **GitHub**.
4.  **ROOT DIRECTORY**:
    - **CRITICAL**: Click "Edit" next to Root Directory and select `pdf_search/frontend`.
5.  **Environment Variables**:
    - Add `VITE_API_URL`: Paste your **BACKEND_URL** (e.g., `https://web-production-1234.up.railway.app`).
6.  **Deploy**.

---

## Part 3: Verify

1.  Open your Vercel App URL.
2.  It should load the UI.
3.  The UI will try to talk to `VITE_API_URL` (Railway).
4.  Railway will talk to `ENDEE_HOST` (Your Mac via Localtunnel).

---

## Local Development (Optional)

To run locally with this new setup:
1.  **Backend**: `uvicorn api:app --reload`
2.  **Frontend**:
    - Create a `.env` file in `frontend/`.
    - Add `VITE_API_URL=http://localhost:8000`
    - Run `npm run dev`.
