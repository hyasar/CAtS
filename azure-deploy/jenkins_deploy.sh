#!/bin/sh

echo "<---------------Variables--------------->"
# Change the names here
ACR="zyhacr"
RESOURCEGROUP="MyResourceGroup"
AKSNAME="MyAKS"

echo "<---------------Link your AKS--------------->"
sudo az acr login --name $ACR
sudo az aks get-credentials --resource-group $RESOURCEGROUP --name $AKSNAME

echo "<---------------Deploy Jenkins to AKS--------------->"
helm repo add codecentric https://codecentric.github.io/helm-charts
sudo helm install --set image.tag=2.222.4 jenkins codecentric/jenkins

export POD_NAME=$(sudo kubectl get pods --namespace default -l "app.kubernetes.io/name=jenkins,app.kubernetes.io/instance=jenkins" -o jsonpath="{.items[0].metadata.name}")

sleep 300
echo "ATTENTION: your initial secret is:"
sudo kubectl exec --namespace default "$POD_NAME" cat /var/jenkins_home/secrets/initialAdminPassword

# Change this if you want to use some private ip
export MYIP=$(curl ifconfig.co)

sudo kubectl port-forward --address 0.0.0.0 pod/$POD_NAME 8080:$MYIP:8080
