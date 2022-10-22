# Orchastretation With K8s
This directory presents the yaml files for deploying course attendance application along with MySQL database.

- **mysql-secrets-template** --> Secrets that contains the password for MySQL database.
- **mysql-env.yaml** --> ConfigMap that contains MySQL environment variables.
- **host-pv.yaml && host-pvc.yaml** --> Persistent volume and persistent volume claim.
- **mysql-deployment.yaml && mysql-svc.yaml"** --> MySQL database deployment and service.
- **flask-deployment.yaml && flask-svc.yaml** --> Course attendance application deployment and service.

## Installation

- This project runs on a single node K8s cluster, minikube.
- To install minikube along with kubectl on Ubuntu 22.04 OS, follow the instructions provided [here](https://www.linuxtechi.com/how-to-install-minikube-on-ubuntu/).
- Before you run the application, please fill up **mysql-secrets-template.yaml** as described in the file.
## Run The Application

- **Apply configurations:**
```sh
# config environment variables and secrets
kubectl apply -f=mysql-secrets.yaml,mysql-env.yaml
# config pv and pvc
kubectl apply -f=host-pv.yaml, host-pvc.yaml
# config mysql deployment and service
kubectl apply -f=mysql-deployment.yaml,mysql-svc.yaml
# config flask app deployment and service
kubectl apply -f=flask-deployment.yaml,flask-svc.yaml
```
- **Run the application:**
```sh
minikube service flask
```
- **Stop the application:**
```sh
kubectl delete -f=mysql-secrets.yaml,mysql-evn.yaml,host-pv.yaml,host-pvc.yaml,mysql-deployment.yaml,mysql-svc.yaml,flask-deployment.yaml,flask-svc.yaml
```
