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
# helm repo add stable https://kubernetes-charts.storage.googleapis.com/
helm repo add codecentric https://codecentric.github.io/helm-charts

# if this is unable to use with swamp, try to see if helm can install the old version
# sudo helm install jenkins stable/jenkins
sudo helm install --set image.tag=2.222.4 jenkins codecentric/jenkins

export POD_NAME=$(sudo kubectl get pods --namespace default -l "app.kubernetes.io/name=jenkins,app.kubernetes.io/instance=jenkins" -o jsonpath="{.items[0].metadata.name}")

# echo "ATTENTION: your login username is: admin"
# echo "ATTENTION: your login password is:"

sleep 300
echo "ATTENTION: your initial secret is:"
# printf $(sudo kubectl get secret --namespace default jenkins -o jsonpath="{.data.jenkins-admin-password}" | base64 --decode);echo
sudo kubectl exec --namespace default "$POD_NAME" cat /var/jenkins_home/secrets/initialAdminPassword

export MYIP=$(curl ifconfig.co)
# export PN=$(sudo kubectl get pods | grep "jenkins" | awk '{print $1}')

sleep 300

# sudo kubectl port-forward --address 0.0.0.0 pod/$PN 8080:$MYIP:8080
sudo kubectl port-forward --address 0.0.0.0 pod/$POD_NAME 8080:$MYIP:8080
