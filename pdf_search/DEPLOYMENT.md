# Deployment Guide: Full Cloud (Endee + App)

This guide helps you deploy **both** the Endee Database and the PDF Search App to the cloud (Render), removing the need for local tunnels.

## Architecture
You will create **two separate services** on Render:
1.  **Endee Database**: A "Web Service" deployed from the root of your repo.
2.  **Search App**: A "Web Service" deployed from the `pdf_search` folder.

---

## Part 1: Deploy Endee Database Service

1.  **Push** your code to GitHub.
2.  Create a **New Web Service** on Render.
3.  **Connect** your repository.
4.  **Settings**:
    - **Name**: `endee-db` (or similar)
    - **Runtime**: `Docker`
    - **Root Directory**: `.` (leave empty)
    - **Plan**: Standard or Free (Note: C++ compilation might take time on Free tier).
5.  **Deploy**.
6.  Once deployed, copy the **Service URL** (e.g., `https://endee-db-xyz.onrender.com`).
    - *Note:* Render exposes port 80/443 externally. Your internal app will connect via this URL.

---

## Part 2: Deploy Search App Service

1.  Create **Another New Web Service** on Render.
2.  **Connect** the SAME repository.
3.  **Settings**:
    - **Name**: `pdf-search-app`
    - **Runtime**: `Docker`
    - **Root Directory**: `pdf_search` (Important!)
4.  **Environment Variables**:
    - `ENDEE_HOST`: Paste the URL from Part 1 (e.g., `endee-db-xyz.onrender.com`). **Remove `https://`**.
    - `ENDEE_PORT`: `443` (Render handles SSL by default).
    - `PORT`: `8000`
5.  **Deploy**.

---

## Verification

1.  Open the URL of your **Search App**.
2.  Try uploading a PDF.
3.  The App (Cloud) will talk to Endee (Cloud). No local computer required!
