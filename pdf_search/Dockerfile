# Stage 1: Build the React Frontend
FROM node:18-slim as build-frontend

WORKDIR /app_build

# Copy entire project context (relative to build root)
COPY . .

# Move to frontend directory
WORKDIR /app_build/frontend

# Install dependencies
RUN npm ci

# Build the frontend
RUN npm run build


# Stage 2: Set up the Python Backend
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code (everything in context)
COPY . .

# Copy built frontend from the previous stage
COPY --from=build-frontend /app_build/frontend/dist ./frontend/dist

EXPOSE 8000

ENV PORT=8000
# Default env vars (override these in Render)
ENV ENDEE_HOST=localhost
ENV ENDEE_PORT=8080

CMD ["sh", "-c", "uvicorn api:app --host 0.0.0.0 --port ${PORT}"]
