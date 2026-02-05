# Stage 1: Build the React Frontend
FROM node:18-slim as build-frontend

WORKDIR /app/frontend

# Copy package.json and package-lock.json (if available)
COPY frontend/package*.json ./

# Install dependencies
RUN npm ci

# Copy the rest of the frontend source code
COPY frontend/ ./

# Build the frontend
RUN npm run build

# Stage 2: Set up the Python Backend
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (if any needed for pymupdf or others)
# builds-essential might be needed for some python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY . .

# Copy built frontend from the previous stage
COPY --from=build-frontend /app/frontend/dist ./frontend/dist

# Expose the API port
EXPOSE 8000

# Set environment variables (Defaults, can be overridden)
ENV PORT=8000
ENV ENDEE_HOST=host.docker.internal
ENV ENDEE_PORT=8080

# Command to run the application
CMD ["sh", "-c", "uvicorn api:app --host 0.0.0.0 --port ${PORT}"]
