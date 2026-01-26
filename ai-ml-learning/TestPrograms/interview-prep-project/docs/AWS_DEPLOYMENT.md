# AWS Deployment Guide

This guide explains how to deploy the interview prep project to AWS using EKS (Elastic Kubernetes Service).

## Architecture on AWS

```
Internet
  ↓
Route 53 (DNS: api.example.com)
  ↓
AWS WAF (Web Application Firewall)
  ↓
ALB (Application Load Balancer)
  ↓
EKS Cluster (Kubernetes)
  ├── API Pods (2-10 replicas, auto-scaling)
  ├── Monitoring (CloudWatch Container Insights)
  └── Logging (CloudWatch Logs)
  ↓
ElastiCache for Redis
  ↓
(Optional) RDS for Database
```

## Prerequisites

1. AWS Account
2. AWS CLI installed and configured
3. kubectl installed
4. eksctl installed
5. Docker installed
6. Helm installed (for AWS Load Balancer Controller)

```bash
# Install eksctl (macOS)
brew tap weaveworks/tap
brew install weaveworks/tap/eksctl

# Install kubectl
brew install kubectl

# Install Helm
brew install helm

# Configure AWS CLI
aws configure
```

## Step-by-Step Deployment

### 1. Create EKS Cluster

```bash
# Create cluster with eksctl (easiest method)
eksctl create cluster \
  --name interview-prep \
  --region us-east-1 \
  --nodegroup-name standard-workers \
  --node-type t3.medium \
  --nodes 3 \
  --nodes-min 2 \
  --nodes-max 5 \
  --managed

# This takes ~15 minutes
# Creates: VPC, subnets, security groups, EKS cluster, node group
```

**What this creates:**
- EKS cluster (managed Kubernetes control plane)
- 3 EC2 t3.medium instances (worker nodes)
- VPC with public and private subnets
- Security groups
- IAM roles

**Cost estimate:** ~$0.10/hour for EKS + ~$0.12/hour for 3 t3.medium instances

### 2. Create ECR Repository

```bash
# Create repository for Docker images
aws ecr create-repository \
  --repository-name interview-prep-api \
  --region us-east-1

# Get repository URI (save this)
aws ecr describe-repositories \
  --repository-names interview-prep-api \
  --region us-east-1 \
  --query 'repositories[0].repositoryUri' \
  --output text
```

### 3. Build and Push Docker Image

```bash
# Authenticate Docker to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Build image
docker build -t interview-prep-api:latest .

# Tag image for ECR
docker tag interview-prep-api:latest \
  <account-id>.dkr.ecr.us-east-1.amazonaws.com/interview-prep-api:latest

# Push to ECR
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/interview-prep-api:latest
```

### 4. Create ElastiCache for Redis

```bash
# Create subnet group
aws elasticache create-cache-subnet-group \
  --cache-subnet-group-name interview-prep-redis \
  --cache-subnet-group-description "Redis for interview prep" \
  --subnet-ids <subnet-id-1> <subnet-id-2>

# Create Redis cluster
aws elasticache create-cache-cluster \
  --cache-cluster-id interview-prep-redis \
  --cache-node-type cache.t3.micro \
  --engine redis \
  --num-cache-nodes 1 \
  --cache-subnet-group-name interview-prep-redis

# Get Redis endpoint (save this)
aws elasticache describe-cache-clusters \
  --cache-cluster-id interview-prep-redis \
  --show-cache-node-info \
  --query 'CacheClusters[0].CacheNodes[0].Endpoint.Address' \
  --output text
```

**Alternative: Use Redis in Kubernetes** (simpler for demo)
- Just deploy Redis using k8s/redis-deployment.yaml
- Not recommended for production (use ElastiCache)

### 5. Update Kubernetes Manifests

Update `k8s/api-deployment.yaml`:

```yaml
# Change image to ECR image
image: <account-id>.dkr.ecr.us-east-1.amazonaws.com/interview-prep-api:latest
imagePullPolicy: Always
```

Update `k8s/configmap.yaml`:

```yaml
# If using ElastiCache, update Redis host
REDIS_HOST: "<redis-endpoint-from-elasticache>"
```

### 6. Install AWS Load Balancer Controller

```bash
# Create IAM policy for ALB controller
curl -o iam-policy.json https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.6.1/docs/install/iam_policy.json

aws iam create-policy \
  --policy-name AWSLoadBalancerControllerIAMPolicy \
  --policy-document file://iam-policy.json

# Create service account
eksctl create iamserviceaccount \
  --cluster=interview-prep \
  --namespace=kube-system \
  --name=aws-load-balancer-controller \
  --attach-policy-arn=arn:aws:iam::<account-id>:policy/AWSLoadBalancerControllerIAMPolicy \
  --approve \
  --region=us-east-1

# Install controller using Helm
helm repo add eks https://aws.github.io/eks-charts
helm repo update

helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
  -n kube-system \
  --set clusterName=interview-prep \
  --set serviceAccount.create=false \
  --set serviceAccount.name=aws-load-balancer-controller
```

### 7. Update Ingress for AWS ALB

Update `k8s/ingress.yaml`:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: interview-prep-ingress
  namespace: interview-prep
  annotations:
    # AWS ALB annotations
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/target-type: ip
    alb.ingress.kubernetes.io/healthcheck-path: /health
    alb.ingress.kubernetes.io/listen-ports: '[{"HTTP": 80}, {"HTTPS": 443}]'
    # SSL certificate ARN (create in ACM first)
    # alb.ingress.kubernetes.io/certificate-arn: arn:aws:acm:...
spec:
  ingressClassName: alb
  # ... rest of ingress spec
```

### 8. Deploy Application

```bash
# Apply all Kubernetes manifests
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/redis-deployment.yaml  # Or skip if using ElastiCache
kubectl apply -f k8s/api-deployment.yaml
kubectl apply -f k8s/hpa.yaml
kubectl apply -f k8s/ingress.yaml

# Watch deployment
kubectl get pods -n interview-prep --watch

# Check ingress (ALB creation takes ~3 minutes)
kubectl get ingress -n interview-prep

# Get ALB DNS name
kubectl get ingress interview-prep-ingress -n interview-prep \
  -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'
```

### 9. Configure DNS (Route 53)

```bash
# Get ALB DNS name from previous step
ALB_DNS="<alb-dns-name>"

# Create Route 53 record
aws route53 change-resource-record-sets \
  --hosted-zone-id <zone-id> \
  --change-batch '{
    "Changes": [{
      "Action": "CREATE",
      "ResourceRecordSet": {
        "Name": "api.example.com",
        "Type": "CNAME",
        "TTL": 300,
        "ResourceRecords": [{"Value": "'$ALB_DNS'"}]
      }
    }]
  }'
```

### 10. Enable SSL with ACM

```bash
# Request certificate in AWS Certificate Manager
aws acm request-certificate \
  --domain-name api.example.com \
  --validation-method DNS \
  --region us-east-1

# Follow validation steps in ACM console
# Add certificate ARN to ingress annotations (step 7)
```

### 11. Set Up Monitoring

```bash
# Enable CloudWatch Container Insights
aws eks update-cluster-config \
  --name interview-prep \
  --logging '{"clusterLogging":[{"types":["api","audit","authenticator","controllerManager","scheduler"],"enabled":true}]}'

# Deploy CloudWatch agent (optional, for detailed metrics)
kubectl apply -f https://raw.githubusercontent.com/aws-samples/amazon-cloudwatch-container-insights/latest/k8s-deployment-manifest-templates/deployment-mode/daemonset/container-insights-monitoring/quickstart/cwagent-fluentd-quickstart.yaml
```

## Testing the Deployment

```bash
# Get ALB endpoint
ALB_DNS=$(kubectl get ingress interview-prep-ingress -n interview-prep \
  -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')

# Test health check
curl http://$ALB_DNS/health

# Test agent
curl -X POST http://$ALB_DNS/agent/task \
  -H "Content-Type: application/json" \
  -d '{"task": "Calculate 10 + 5"}'

# Test with domain (after DNS propagates)
curl https://api.example.com/health
```

## Monitoring and Logging

### CloudWatch Logs

```bash
# View logs in CloudWatch
aws logs tail /aws/eks/interview-prep/cluster --follow

# Or use kubectl
kubectl logs -f deployment/interview-prep-api -n interview-prep
```

### CloudWatch Metrics

Navigate to CloudWatch Console:
- Container Insights → EKS Clusters → interview-prep
- View: CPU, Memory, Network, Pod count

### Set Up Alarms

```bash
# Example: Alert if pod count drops below 2
aws cloudwatch put-metric-alarm \
  --alarm-name interview-prep-low-pod-count \
  --alarm-description "Alert if fewer than 2 pods running" \
  --metric-name pod_number_of_running_pods \
  --namespace ContainerInsights \
  --statistic Average \
  --period 300 \
  --threshold 2 \
  --comparison-operator LessThanThreshold \
  --evaluation-periods 1
```

## Cost Optimization

### Reduce Costs

1. **Use Spot Instances** (up to 90% savings)
   ```bash
   eksctl create nodegroup \
     --cluster=interview-prep \
     --name=spot-workers \
     --node-type=t3.medium \
     --nodes=3 \
     --spot
   ```

2. **Right-size instances**
   - Monitor actual usage
   - Start with t3.small, scale up if needed

3. **Auto-scaling**
   - HPA scales pods based on load
   - Cluster Autoscaler scales nodes

4. **Use Fargate** (serverless)
   - No node management
   - Pay only for pod resources
   - Good for variable workloads

### Cost Monitoring

```bash
# Enable Cost Explorer
# View costs by service, tags, etc.

# Tag resources for cost tracking
kubectl label namespace interview-prep cost-center=learning
```

## Cleanup

**IMPORTANT: Prevents unexpected charges!**

```bash
# Delete Kubernetes resources
kubectl delete namespace interview-prep

# Delete Ingress (deletes ALB)
kubectl delete ingress interview-prep-ingress -n interview-prep

# Delete EKS cluster
eksctl delete cluster --name interview-prep --region us-east-1

# Delete ElastiCache
aws elasticache delete-cache-cluster \
  --cache-cluster-id interview-prep-redis

# Delete ECR repository
aws ecr delete-repository \
  --repository-name interview-prep-api \
  --force \
  --region us-east-1

# Delete CloudWatch log groups
aws logs delete-log-group --log-group-name /aws/eks/interview-prep/cluster
```

## Troubleshooting

### Pods Not Starting

```bash
# Check pod status
kubectl describe pod <pod-name> -n interview-prep

# Common issues:
# 1. ImagePullBackOff: ECR auth issue
#    - Check ECR repository exists
#    - Check IAM permissions for nodes

# 2. CrashLoopBackOff: App error
#    - Check logs: kubectl logs <pod-name> -n interview-prep
```

### Ingress Not Creating ALB

```bash
# Check ingress controller logs
kubectl logs -n kube-system deployment/aws-load-balancer-controller

# Common issues:
# 1. IAM permissions: Check service account has correct policy
# 2. Subnet tags: Subnets need specific tags for ALB
```

### Can't Connect to Redis (ElastiCache)

```bash
# Check security groups
# ElastiCache security group must allow traffic from EKS nodes

# Get node security group
aws eks describe-cluster \
  --name interview-prep \
  --query 'cluster.resourcesVpcConfig.clusterSecurityGroupId'

# Update ElastiCache security group to allow port 6379 from node SG
```

## Interview Talking Points

### EKS vs Self-Managed Kubernetes

**EKS (Managed):**
- AWS manages control plane
- Automatic upgrades
- HA control plane (multi-AZ)
- Integrated with AWS (IAM, VPC, CloudWatch)
- Higher cost (~$72/month for control plane)

**Self-Managed:**
- You manage everything
- More control, more work
- Lower cost (just EC2)
- Requires expertise

### When to Use EKS

- Production workloads
- Need AWS integration
- Want managed control plane
- Team knows Kubernetes but not deep operations

### Alternatives

- **ECS (Elastic Container Service)**: Simpler, AWS-specific
- **Fargate**: Serverless containers
- **App Runner**: Simplest, for basic apps
- **EC2 with Docker**: Most control, most work

## Additional Resources

- [AWS EKS Documentation](https://docs.aws.amazon.com/eks/)
- [eksctl Documentation](https://eksctl.io/)
- [AWS Load Balancer Controller](https://kubernetes-sigs.github.io/aws-load-balancer-controller/)
- [EKS Best Practices](https://aws.github.io/aws-eks-best-practices/)

---

**This deployment guide demonstrates production AWS patterns you can discuss in interviews!**
