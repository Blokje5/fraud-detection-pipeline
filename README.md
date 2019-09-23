# Fraud Detection Pipeline

This project contains the code for the final project of the Udacity Data Engineering Nano Degree.

## Setting up the project

The project runs on a Kubernetes cluster. A Makefile is available to simplify the process.

Requirements:
- Docker
- Kubectl
- Make

Setup of the cluster:

```bash
make create
export KUBECONFIG=$(make env)  
``` 
