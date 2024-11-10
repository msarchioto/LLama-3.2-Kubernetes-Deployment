# LLama-3.2-Kubernetes-Deployment
Scalable LLama 3.2 chatbot deployment using Kubernetes

## Project Overview
This project implements a scalable chatbot using LLama 3.2 (1B parameters) with the following features:
- LangChain integration for context management and system prompts
- Containerized deployment using Docker
- Kubernetes deployment with auto-scaling capabilities
- Load balancing with sticky sessions

## Project Structure
```
project/
├── app/
│ ├── main.py
│ ├── chat_model.py
│ └── config.py
├── kubernetes/
│ ├── deployment.yaml
│ ├── service.yaml
│ └── hpa.yaml
├── Dockerfile
├── requirements.txt
└── README.md
```

## Setup Instructions

### Local Development
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app/main.py
```

### Docker Deployment
1. Build the Docker image:
```bash
docker build -t llama-chatbot:latest .
```

### Kubernetes Deployment
1. Start Minikube:
```bash
minikube start
```

2. Apply Kubernetes configurations:
```bash
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
kubectl apply -f kubernetes/hpa.yaml
```

3. Enable ingress:
```bash
minikube addons enable ingress
```

4. Get the service URL:
```bash
minikube service llama-chatbot --url
```

## Architecture
- Base Model: LLama 3.2 (1B parameters)
- Framework: LangChain for context management
- Deployment: Kubernetes with HPA (Horizontal Pod Autoscaling)
- Scaling: 3-10 replicas based on CPU utilization
- Session Affinity: Enabled for consistent user experience

## API Endpoints
- POST `/chat`: Send messages to the chatbot
- GET `/health`: Health check endpoint

## Configuration
- Default replicas: 3
- Max replicas: 10
- CPU threshold for scaling: 70%
- Memory limit: 4Gi per pod
```

## Example curl request
```bash
curl -X POST "$(minikube service llama-chatbot --url)/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "Hello, how are you?"}'
```