# Orchastretation With K8s
This directory presents the yaml files for deploying course attendance application along with MySQL database.

- **mysql-secrets-template.yml** --> Secrets that contains the password for MySQL database.
- **mysql-env.yml** --> ConfigMap that contains MySQL environment variables.
- **host-pv.yml & host-pvc.yml** --> Persistent volume and persistent volume claim.
- **mysql-deployment.yml & mysql-svc.yml"** --> MySQL database deployment and service.
- **flask-deployment.yml & flask-svc.yml** --> Course attendance application deployment and service.

## Installation

- This project runs on a single node K8s cluster, minikube.
- To install minikube along with kubectl on Ubuntu 22.04 OS, follow the instructions provided [here](https://www.linuxtechi.com/how-to-install-minikube-on-ubuntu/).
- Before you run the application, please fill up **mysql-secrets-template.yaml** with encoded password for the mysql root account.
  To encode password use this cmd:
  ```sh
  echo -n 'password' | base64
  ```

## Run The Application
- **Create minikube cluster:**
```sh
minikube start
```
- **Apply configurations:**
```sh
# config environment variables and secrets
kubectl apply -f=mysql-secrets-template.yml,mysql-env.yml
# config pv and pvc
kubectl apply -f=host-pv.yml, host-pvc.yml
# config mysql deployment and service
kubectl apply -f=mysql-deployment.yml,mysql-svc.yml
# config flask app deployment and service
kubectl apply -f=flask-deployment.yml,flask-svc.yml
```
- **Run the application:**
```sh
minikube service flask
```
- **Stop the application:**
```sh
kubectl delete -f=mysql-secrets.yml,mysql-evn.yml,host-pv.yml,host-pvc.yml,mysql-deployment.yml,mysql-svc.yml,flask-deployment.yml,flask-svc.yml
```
- **Delete minikube cluster:**
```sh
minikube delete
```
