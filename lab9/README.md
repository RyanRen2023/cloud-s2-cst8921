Lab Activity Overview:
Step 1: Create an AKS Cluster

az group create --name aks-lab-rg --location eastus
az aks create \
  --resource-group aks-lab-rg \
  --name aks-lab-cluster \
  --node-count 2 \
  --enable-addons monitoring \
  --generate-ssh-keys

Step 2: Connect to the Cluster

az aks get-credentials --resource-group aks-lab-rg --name aks-lab-cluster
             kubectl get nodes

Step 3: Deploy a Sample App

# save as deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: webapp
spec:
  replicas: 2
  selector:
    matchLabels:
      app: webapp
  template:
    metadata:
      labels:
        app: webapp
    spec:
      containers:
      - name: webapp
        image: mcr.microsoft.com/azuredocs/aks-helloworld:v1
        ports:
        - containerPort: 80


kubectl apply -f deployment.yaml
kubectl expose deployment webapp --type=LoadBalancer --port=80
kubectl get service webapp

Step 4: Enable Horizontal Pod Autoscaler

kubectl autoscale deployment webapp --cpu-percent=50 --min=2 --max=5
kubectl get hpa

Step 5: Monitor the Cluster
Enable Container Insights via Azure Portal under the AKS cluster’s Monitoring tab.

View logs, metrics, and live traffic.



Step 6: Perform a Rolling Update
# Update the image version
kubectl set image deployment/webapp webapp=mcr.microsoft.com/azuredocs/aks-helloworld:v2
kubectl rollout status deployment/webapp


Step 7: Clean Up Resources
az group delete --name aks-lab-rg --yes --no-wait




Important Notes: 
For grading prepare a lab report with your findings and analysis and share that in an Assignments tab in Brightspace.
Lab Activity Overview:
Step 1: Create an AKS Cluster

az group create --name aks-lab-rg --location eastus
az aks create \
  --resource-group aks-lab-rg \
  --name aks-lab-cluster \
  --node-count 2 \
  --enable-addons monitoring \
  --generate-ssh-keys

Step 2: Connect to the Cluster

az aks get-credentials --resource-group aks-lab-rg --name aks-lab-cluster
             kubectl get nodes

Step 3: Deploy a Sample App

# save as deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: webapp
spec:
  replicas: 2
  selector:
    matchLabels:
      app: webapp
  template:
    metadata:
      labels:
        app: webapp
    spec:
      containers:
      - name: webapp
        image: mcr.microsoft.com/azuredocs/aks-helloworld:v1
        ports:
        - containerPort: 80


kubectl apply -f deployment.yaml
kubectl expose deployment webapp --type=LoadBalancer --port=80
kubectl get service webapp

Step 4: Enable Horizontal Pod Autoscaler

kubectl autoscale deployment webapp --cpu-percent=50 --min=2 --max=5
kubectl get hpa

Step 5: Monitor the Cluster
Enable Container Insights via Azure Portal under the AKS cluster’s Monitoring tab.

View logs, metrics, and live traffic.


Step 6: Perform a Rolling Update
# Update the image version
kubectl set image deployment/webapp webapp=mcr.microsoft.com/azuredocs/aks-helloworld:v2
kubectl rollout status deployment/webapp


Step 7: Clean Up Resources
az group delete --name aks-lab-rg --yes --no-wait




Important Notes: 
For grading prepare a lab report with your findings and analysis and share that in an Assignments tab in Brightspace.
