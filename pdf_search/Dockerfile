# -----------------------------
# Stage 1: Build React Frontend
# -----------------------------
FROM node:18-slim AS build-frontend

WORKDIR /app_build

# Copy only frontend source
COPY pdf_search/frontend ./frontend

WORKDIR /app_build/frontend

RUN npm ci
RUN npm run build


# -----------------------------
# Stage 2: Python Backend
# -----------------------------
FROM python:3.11-slim

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements
COPY pdf_search/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY pdf_search .

# Copy built frontend
COPY --from=build-frontend /app_build/frontend/dist ./frontend/dist

EXPOSE 8000

ENV PORT=8000
ENV ENDEE_HOST=host.docker.internal
ENV ENDEE_PORT=8080

CMD ["sh", "-c", "uvicorn api:app --host 0.0.0.0 --port ${PORT}"]
