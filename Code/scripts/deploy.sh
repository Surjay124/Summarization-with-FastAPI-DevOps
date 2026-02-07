#!/bin/bash

# Deployment Script (Automated & Manual)

# Variables
APP_DIR="/home/ubuntu/ai-summarizer"
REPO_URL="https://github.com/YOUR_USERNAME/YOUR_REPO.git"
BRANCH="main"

echo "Starting Deployment..."

# 1. Clone or Pull Code
if [ -d "$APP_DIR" ]; then
    echo "Directory exists. Pulling latest code..."
    cd $APP_DIR
    git pull origin $BRANCH
else
    echo "Cloning repository..."
    git clone $REPO_URL $APP_DIR
    cd $APP_DIR
fi

# 2. Check for .env file or Fetch from Secrets Manager
SECRET_NAME="prod/ai-summarizer/env"
REGION="us-east-1"

if aws secretsmanager get-secret-value --secret-id $SECRET_NAME --region $REGION &> /dev/null; then
    echo "Fetching secrets from AWS Secrets Manager..."
    # Requires 'jq' installed: sudo apt-get install jq
    aws secretsmanager get-secret-value --secret-id $SECRET_NAME --region $REGION --query SecretString --output text | jq -r 'to_entries|map("\(.key)=\(.value)")|.[]' > .env
else
    echo "Secrets Manager retrieval failed or not configured."
    if [ ! -f .env ]; then
        echo "WARNING: .env file not found! Copying .env.example..."
        cp .env.example .env
    fi
fi

# 3. Build and Run Containers
echo "Building and Deploying Containers..."

# Stop existing containers if running
docker compose -f docker-compose.prod.yml down

# Build and start
docker compose -f docker-compose.prod.yml up -d --build

echo "Deployment Complete!"
echo "Backend running on port 8000"
echo "Frontend running on port 8501"
