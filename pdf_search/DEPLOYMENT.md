# Deployment Guide for PDF Search App

This application is containerized using Docker, which makes it easy to deploy to various platforms.

## Prerequisites

- **Endee Server**: This application acts as a client to an Endee Vector Database. You must have an Endee server running and accessible.
- **Docker**: If you want to build/run locally.

## Environment Variables

You need to provide the following environment variables to the container:

- `ENDEE_HOST`: Hostname of the Endee Endee server (default: `host.docker.internal` for local dev)
- `ENDEE_PORT`: Port of the Endee server (default: `8080`)
- `PORT`: Port to serve the app on (default: `8000`)

## Local Deployment (with Docker)

### Scenario A: Running everything on the same machine
If you run this app on the SAME machine where Endee is running (e.g., both on your Mac):
```bash
docker run -p 8000:8000 \
  -e ENDEE_HOST=host.docker.internal \
  -e ENDEE_PORT=8080 \
  pdf-search-app
```

### Scenario B: Running on Windows, connecting to Mac (LAN)
If you run this app on Windows, but Endee is on your Mac:
1.  Find your Mac's LAN IP address (e.g., `192.168.1.50`).
2.  Run the container:
```bash
docker run -p 8000:8000 \
  -e ENDEE_HOST=192.168.1.50 \
  -e ENDEE_PORT=8080 \
  pdf-search-app
```

### Step 1: Expose Endee on your Mac
1.  On your **Mac**, install localtunnel (requires Node.js):
    ```bash
    npx localtunnel --port 8080
    ```
2.  Copy the URL it gives you (e.g., `https://calm-zebra-45.loca.lt`).

### Step 2: Deploy to Render
1.  Push this code to GitHub.
2.  Create a new **Web Service** on Render.
3.  Connect your repo.
4.  **Important**: Set Environment Variables:
    - `ENDEE_HOST`: `calm-zebra-45.loca.lt` (remove `https://` and trailing slash).
    - `ENDEE_PORT`: `80` (or `443` - localtunnel usually runs on 443 HTTPS).
    - `PORT`: `8000`
5.  Deploy.

> [!TIP]
> Localtunnel URLs often change when you restart the command. If you restart `lt`, update the `ENDEE_HOST` variable in Render.

> [!NOTE]
> Detailed Render setup can be automated by using the included `render.yaml` Blueprint if you connect your account in the Render dashboard.

### Troubleshooting

- **Dockerfile Not Found**: If Render says `failed to read dockerfile`, check your **Root Directory** setting in Render. Since this app is in a subfolder, set **Root Directory** to `pdf_search` (or wherever the `Dockerfile` is located).
- **Connection Refused**: If running on Windows and connecting to Mac, ensure your Mac's Firewall allows incoming connections on port 8080. You can test this by trying to open `http://<MAC_IP>:8080/api/health` in your Windows browser.
- **Docker Not Found**: ensure Docker Desktop is installed and running.
