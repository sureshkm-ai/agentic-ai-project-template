# Deployment Guide

## Prerequisites

- Cloud platform account (GCP/AWS/Azure)
- Docker installed locally
- Cloud CLI configured
- GitHub account (for CI/CD)

## Local Deployment

### Using Docker
```bash
# Build image
docker build -t agentic-ai-app:local .

# Run container
docker run -p 8080:8080 \
  -e OPENAI_API_KEY=your-key \
  -e ANTHROPIC_API_KEY=your-key \
  agentic-ai-app:local
```

### Using Docker Compose
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f app

# Stop services
docker-compose down
```

## Cloud Deployment

### Google Cloud Platform (GCP)

#### Prerequisites
```bash
# Install gcloud CLI
# https://cloud.google.com/sdk/docs/install

# Authenticate
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable \
  run.googleapis.com \
  aiplatform.googleapis.com \
  firestore.googleapis.com \
  storage.googleapis.com \
  cloudbuild.googleapis.com
```

#### Manual Deployment
```bash
# Deploy to Cloud Run
gcloud run deploy agentic-ai-app \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY=your-key \
  --set-env-vars ANTHROPIC_API_KEY=your-key \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300 \
  --max-instances 10 \
  --min-instances 0

# Get service URL
gcloud run services describe agentic-ai-app \
  --region us-central1 \
  --format 'value(status.url)'
```

#### CI/CD Deployment

1. **Set GitHub Secrets:**
   - `GCP_PROJECT_ID`
   - `GCP_SA_KEY` (service account JSON key)
   - `OPENAI_API_KEY`
   - `ANTHROPIC_API_KEY`

2. **Push to main branch:**
```bash
   git push origin main
```

3. **GitHub Actions will automatically:**
   - Run tests
   - Build Docker image
   - Deploy to Cloud Run

---

### Amazon Web Services (AWS)

#### Prerequisites
```bash
# Install AWS CLI
# https://aws.amazon.com/cli/

# Configure
aws configure
```

#### Deploy to Lambda
```bash
# Package application
zip -r function.zip src/ requirements.txt

# Create Lambda function
aws lambda create-function \
  --function-name agentic-ai-function \
  --runtime python3.11 \
  --handler src.lambda_handler.handler \
  --zip-file fileb://function.zip \
  --role arn:aws:iam::ACCOUNT_ID:role/lambda-role \
  --timeout 300 \
  --memory-size 2048 \
  --environment Variables="{OPENAI_API_KEY=your-key}"

# Update function code
aws lambda update-function-code \
  --function-name agentic-ai-function \
  --zip-file fileb://function.zip
```

#### Deploy to ECS
```bash
# Build and push to ECR
aws ecr create-repository --repository-name agentic-ai-app

docker build -t agentic-ai-app .
docker tag agentic-ai-app:latest \
  ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/agentic-ai-app:latest

aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

docker push ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/agentic-ai-app:latest

# Deploy to ECS (using existing cluster/service)
aws ecs update-service \
  --cluster agentic-ai-cluster \
  --service agentic-ai-service \
  --force-new-deployment
```

---

### Microsoft Azure

#### Prerequisites
```bash
# Install Azure CLI
# https://docs.microsoft.com/en-us/cli/azure/install-azure-cli

# Login
az login
```

#### Deploy to Azure Web Apps
```bash
# Create resource group
az group create \
  --name agentic-ai-rg \
  --location eastus

# Create container registry
az acr create \
  --resource-group agentic-ai-rg \
  --name agenticairegistry \
  --sku Basic

# Build and push image
az acr build \
  --registry agenticairegistry \
  --image agentic-ai-app:latest .

# Create web app
az webapp create \
  --resource-group agentic-ai-rg \
  --plan agentic-ai-plan \
  --name agentic-ai-app \
  --deployment-container-image-name \
    agenticairegistry.azurecr.io/agentic-ai-app:latest

# Configure environment variables
az webapp config appsettings set \
  --resource-group agentic-ai-rg \
  --name agentic-ai-app \
  --settings OPENAI_API_KEY=your-key
```

## Environment Variables

### Required
```bash
OPENAI_API_KEY=your-key
ANTHROPIC_API_KEY=your-key
LANGCHAIN_API_KEY=your-key
```

### Cloud-Specific

**GCP:**
```bash
GCP_PROJECT_ID=your-project
GCP_REGION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json
```

**AWS:**
```bash
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
```

**Azure:**
```bash
AZURE_SUBSCRIPTION_ID=your-sub-id
AZURE_RESOURCE_GROUP=your-rg
```

## Monitoring

### Health Checks
```bash
# Check service health
curl https://your-app.run.app/health

# Expected response
{
  "status": "healthy",
  "version": "1.0.0"
}
```

### Logs

**GCP:**
```bash
gcloud run logs tail agentic-ai-app --region us-central1
```

**AWS:**
```bash
aws logs tail /aws/lambda/agentic-ai-function --follow
```

**Azure:**
```bash
az webapp log tail --resource-group agentic-ai-rg --name agentic-ai-app
```

## Rollback

**GCP:**
```bash
# List revisions
gcloud run revisions list --service agentic-ai-app

# Rollback to previous
gcloud run services update-traffic agentic-ai-app \
  --to-revisions REVISION_NAME=100
```

**AWS:**
```bash
# Deploy previous version
aws lambda update-function-code \
  --function-name agentic-ai-function \
  --image-uri PREVIOUS_IMAGE_URI
```

## Scaling

**GCP Cloud Run:**
- Auto-scales based on requests
- Configure: `--min-instances` and `--max-instances`

**AWS Lambda:**
- Auto-scales automatically
- Configure: Reserved concurrency

**Azure Web Apps:**
- Manual or auto-scale rules
- Configure in Azure Portal

## Cost Optimization

1. **Use minimum instances: 0** (scale to zero when idle)
2. **Set appropriate timeout** (avoid long-running idle instances)
3. **Implement caching** (reduce LLM API calls)
4. **Use cheaper LLM models** for simple queries
5. **Monitor and set budget alerts**

---

Last Updated: December 2025
