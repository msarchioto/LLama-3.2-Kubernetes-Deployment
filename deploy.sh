#!/bin/bash

# Start minikube if not running
minikube status || minikube start

# Enable ingress addon
minikube addons enable ingress

# Build the Docker image
eval $(minikube docker-env)
docker build -t llama-chatbot:latest .

# Apply Kubernetes configurations
kubectl apply -f kubernetes/pvc.yaml
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
kubectl apply -f kubernetes/hpa.yaml

# Wait for deployment
kubectl rollout status deployment/llama-chatbot

# Get the service URL
echo "Service URL:"
minikube service llama-chatbot --url 