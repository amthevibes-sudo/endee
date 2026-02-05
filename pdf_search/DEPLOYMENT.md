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

## Cloud Deployment on Render (+ Local Endee)

Since your Endee database is running locally on your Mac, Render cannot access it directly. You must use a tunneling service like **ngrok** to expose Endee securely.

### Step 1: Expose Endee on your Mac
1.  On your **Mac**, install ngrok: `brew install ngrok/ngrok/ngrok`
2.  Start a tunnel to your Endee port (locked to port 8080):
    ```bash
    ngrok http 8080
    ```
3.  Copy the forwarding URL (e.g., `https://1234-abcd.ngrok-free.app`).

### Step 2: Deploy to Render
1.  Push this code to GitHub.
2.  Create a new **Web Service** on Render.
3.  Connect your repo.
4.  **Important**: Set Environment Variables:
    - `ENDEE_HOST`: `1234-abcd.ngrok-free.app` (remove `https://` and trailing slash)
    - `ENDEE_PORT`: `80` (or `443` depending on if you use http/https)
    - `PORT`: `8000`
5.  Deploy.

> [!NOTE]
> Detailed Render setup can be automated by using the included `render.yaml` Blueprint if you connect your account in the Render dashboard.

## Troubleshooting

- **Connection Refused**: If running on Windows and connecting to Mac, ensure your Mac's Firewall allows incoming connections on port 8080. You can test this by trying to open `http://<MAC_IP>:8080/api/health` in your Windows browser.
- **Docker Not Found**: ensure Docker Desktop is installed and running.
