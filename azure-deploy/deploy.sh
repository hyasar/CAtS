#!/bin/sh

echo "<---------------Variables--------------->"
# Change the names here
ACR="zyhacr"
RESOURCEGROUP="MyResourceGroup"
AKSNAME="MyAKS"

echo "<---------------Create AKS--------------->"
az group create --name $RESOURCEGROUP --location eastus
az acr create --resource-group $RESOURCEGROUP --name $ACR --sku Basic
sudo az acr login --name $ACR
sudo apt-get install pass gnupg2
az aks create -g $RESOURCEGROUP -n $AKSNAME --location eastus  --attach-acr $ACR --generate-ssh-keys
sudo az aks install-cli
sudo az aks get-credentials --resource-group $RESOURCEGROUP --name $AKSNAME

echo "<---------------Build and Upload Image--------------->"
ACRSERVER=$(az acr show -n $ACR --resource-group MyResourceGroup --query loginServer | tr -d '"')

# You may want to change the name and tag of the image here
cd ~/CAtS/CAS_WEB
sudo docker build -f Dockerfile -t caswebservice:new .
cd ../azure-deploy
sudo docker tag caswebservice:new $ACRSERVER/caswebservice:v1
sudo docker push $ACRSERVER/caswebservice:v1

echo "<---------------Create Helm chart and config--------------->"
helm create caswebservice
cp CASWEB/values.yaml caswebservice/
cp CASWEB/Chart.yaml caswebservice/
cp CASWEB/deployment.yaml caswebservice/templates/
cp CASWEB/service.yaml caswebservice/templates/

echo "<---------------Deploy with Helm--------------->"
sudo helm install caswebservice caswebservice/
sleep 60
sudo kubectl get pods
sudo kubectl get svc
export SERVICE_IP=$(sudo kubectl get svc --namespace default caswebservice --template "{{ range (index .status.loadBalancer.ingress 0) }}{{.}}{{ end }}")
echo "now visit http://$SERVICE_IP:8000 to access our service"
