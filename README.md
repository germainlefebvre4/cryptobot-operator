# Cryptobot Operator

## Getting started
### Prepare
```bash
kubectl create namespace cryptobot-operator
kubectl config set-context --current --namespace=cryptobot-operator
```

### Install
```bash
kubectl apply -f kubernetes/crd.yaml
```

### Deploy
```bash
cd chart/
helm upgrade --install cryptobot-operator -n cryptobot-operator -f values.yaml .
helm uninstall cryptobot-operator
```

### Examples
```bash
kubectl apply -f examples/simple-bot/bot.yaml
```


## Contribute
```bash
kubectl create namespace cryptobot-operator
kubectl config set-context --current --namespace=cryptobot-operator
kubectl apply -f kubernetes/crd.yaml

pipenv update --dev
pipenv run kopf run main.py
```