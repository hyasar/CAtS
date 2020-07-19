#!/bin/sh

echo "<--------------Create Helm chart and config--------------->"
helm create caswebservice
cp CASWEB/values.yaml caswebservice/
cp CASWEB/Chart.yaml caswebservice/
cp CASWEB/deployment.yaml caswebservice/templates/
cp CASWEB/service.yaml caswebservice/templates/

echo "<--------------Deploy with Helm--------------->"
sudo helm install caswebservice caswebservice/
sleep 60
sudo kubectl get pods
sudo kubectl get svc
export SERVICE_IP=$(sudo kubectl get svc --namespace default caswebservice --template "{{ range (index .status.loadBalancer.ingress 0) }}{{.}}{{ end }}")
echo "now visit http://$SERVICE_IP:8000 to access our service"
