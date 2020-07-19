# Deploy to Azure Kubernetes Service

<a href="https://helm.sh/">Helm</a> is an open-source packaging tool that helps you install and manage the lifecycle of Kubernetes applications.

We will use Helm on **Ubuntu** to package and run an application on AKS (Azure Kubernetes Service)

## Prerequisites

-   An Azure **Pay-as-you-go** subscription. If you don't have an Azure subscription, you can create <a href="https://azure.microsoft.com/en-us/free/">a free account</a>.
-   <a href="https://docs.microsoft.com/en-us/cli/azure/install-azure-cli-apt?view=azure-cli-latest">Azure CLI installed</a>.
-   Docker installed and configured on <a href="https://docs.docker.com/engine/install/ubuntu/">Linux Ubuntu</a> system.
-   <a href="https://helm.sh/docs/intro/install/">Helm v3 installed</a>.

## Sign in Azure CLI

Execute:

```
az login
```

If the CLI can open your default browser, it will do so and load an Azure sign-in page.

Otherwise, open a browser page at <a>https://aka.ms/devicelogin</a> and enter the authorization code displayed in your terminal.

Sign in with your account credentials in the browser.

## Deploy

Change the variables (resource group name, acr name, aks name and tags) in `deploy.sh`

Change the `image.repository` with correct acr repo name in `CASWEB/values.yaml`

Change the `appVersion` to correct tag in `CASWEB/Chart.yaml`

Make sure the database IP address in `../CAS_WEB/webapps/settings.py` is configured.

Execute:

```
./deploy.sh
```

Wait until commands finish.

## Uninstall Helm Resource

 ```
 sudo helm uninstall $RELEASE_NAME
 ```
 
## Remove the Cluster

When the cluster is no longer needed, use the az group delete command to remove the resource group, the AKS cluster, the container registry, the container images stored there, and all related resources.

```
az group delete --name $RESOURCE_GROUP_NAME --yes --no-wait
```

## Reference

<a>https://docs.microsoft.com/en-us/azure/aks/quickstart-helm</a>