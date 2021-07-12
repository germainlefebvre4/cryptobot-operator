import kopf
import kubernetes
from kubernetes import client, config
from kubernetes.client.rest import ApiException
import json

def create_configmap(
    name = None,
    namespace = None,
    data = None,
) -> None:
    api = client.CoreV1Api()
    configmap = client.V1ConfigMap(
        api_version = "v1",
        kind = "ConfigMap",
        data = data,
        metadata = client.V1ObjectMeta(
            name = name,
            namespace = namespace,
        )
    )

    try:
        api_response = api.create_namespaced_config_map(
            namespace = namespace,
            body = configmap,
        )
    except ApiException as e:
        print("Exception when calling CoreV1Api->create_namespaced_config_map: %s\n" % e)


def update_configmap(
    name = None,
    namespace = None,
    data = None,
) -> None:
    api = client.CoreV1Api()
    configmap = client.V1ConfigMap(
        api_version = "v1",
        kind = "ConfigMap",
        data = data,
        metadata = client.V1ObjectMeta(
            name = name,
            namespace = namespace,
        )
    )

    try:
        api_response = api.patch_namespaced_config_map(
            name = name,
            namespace = namespace,
            body = configmap,
        )
    except ApiException as e:
        print("Exception when calling CoreV1Api->patch_namespaced_config_map: %s\n" % e)


def delete_configmap(
    name = None,
    namespace = None,
    data = None,
) -> None:
    api = client.CoreV1Api()
    try:
        api_response = api.delete_namespaced_config_map(
            name = name,
            namespace = namespace
        )
    except ApiException as e:
        print("Exception when calling CoreV1Api->remove_namespaced_config_map: %s\n" % e)


def create_deployment(
    name = None,
    namespace = None,
) -> None:
    api = client.AppsV1Api()
    deployment = client.V1Deployment(
        api_version = "apps/v1",
        kind = "Deployment",
        metadata = client.V1ObjectMeta(
            name = name,
            namespace = namespace,
        ),
        spec = {
            "selector": {
                "matchLabels": {
                    "app": f'{name}'
                },
            },
            "replicas": 1,
            "template": {
                "metadata": {
                    "labels": {
                        "app": f'{name}'
                    },
                },
                "spec": {
                    "containers": [{
                        "name": 'cryptobot',
                        "image": "germainlefebvre4/pycryptobot:latest",
                        "env": [{
                            "name": "PYTHONUNBUFFERED",
                            "value": "1",
                        }],
                        "ports": [{
                            "containerPort": 80,
                        }],
                        "volumeMounts": [{
                            "name": "config-volume",
                            "mountPath": "/app/config.json",
                            "subPath": "config.json",
                        }],
                    }],
                    "volumes": [{
                        "name": "config-volume",
                        "configMap": {
                            "name": f'{name}',
                        },
                    }],
                },
            },
        }
    )

    try:
        api_response = api.create_namespaced_deployment(
            namespace = namespace,
            body = deployment,
        )
    except ApiException as e:
        print("Exception when calling AppsV1Api->create_namespaced_deployment: %s\n" % e)


def update_deployment(
    name = None,
    namespace = None,
) -> None:
    api = client.AppsV1Api()
    deployment = client.V1Deployment(
        api_version = "apps/v1",
        kind = "Deployment",
        metadata = client.V1ObjectMeta(
            name = name,
            namespace = namespace,
        ),
        spec = {
            "selector": {
                "matchLabels": {
                    "app": f'{name}'
                },
            },
            "replicas": 1,
            "template": {
                "metadata": {
                    "labels": {
                        "app": f'{name}'
                    },
                },
                "spec": {
                    "containers": [{
                        "name": 'cryptobot',
                        "image": "germainlefebvre4/pycryptobot:latest",
                        "env": [{
                            "name": "PYTHONUNBUFFERED",
                            "value": "1",
                        }],
                        "ports": [{
                            "containerPort": 80,
                        }],
                        "volumeMounts": [{
                            "name": "config-volume",
                            "mountPath": "/app/config.json",
                            "subPath": "config.json",
                        }],
                    }],
                    "volumes": [{
                        "name": "config-volume",
                        "configMap": {
                            "name": f'{name}',
                        },
                    }],
                },
            },
        }
    )

    try:
        api_response = api.patch_namespaced_deployment(
            name = name,
            namespace = namespace,
            body = deployment,
        )
    except ApiException as e:
        print("Exception when calling AppsV1Api->patch_namespaced_deployment: %s\n" % e)


def delete_deployment(
    name = None,
    namespace = None,
    app = None,
) -> None:
    api = client.AppsV1Api()
    # name = f'{customer}-{currency}'
    try:
        api_response = api.delete_namespaced_deployment(
            name = name,
            namespace = namespace
        )
    except ApiException as e:
        print("Exception when calling AppsV1Api->delete_namespaced_deployment: %s\n" % e)

def create_configmap_data(
    exchange = "binance",
    binance_api_url = "https://api.binance.com",
    binance_api_key = None,
    binance_api_secret = None,
    binance_config_base_currency = "BTC",
    binance_config_quote_currency = "EUR",
    binance_config_granularity = "15m",
    binance_config_live = 0,
    binance_config_verbose = 1,
    binance_config_graphs = 0,
    binance_config_buymaxsize = None,
    binance_config_sellupperpcnt = 10,
    binance_config_selllowerpcnt = -2,
    logger_consoleloglevel = "INFO",
    telegram_client_id = None,
    telegram_token = None,
):
    configmap = {
        "binance": {
            "api_url": f'{binance_api_url}',
            "api_key": f'{binance_api_key}',
            "api_secret": f'{binance_api_secret}',
            "config": {
                "base_currency": f'{binance_config_base_currency}',
                "quote_currency": f'{binance_config_quote_currency}',
                "granularity": f'{binance_config_granularity}',
                "live": int(binance_config_live),
                "verbose": int(binance_config_verbose),
                "graphs": int(binance_config_graphs),
                "buymaxsize": float(binance_config_buymaxsize),
                "sellupperpcnt": int(binance_config_sellupperpcnt),
                "selllowerpcnt": int(binance_config_selllowerpcnt),
            },
        },
        "logger": {
            "filelog": 0,
            "logfile": "pycryptobot.log",
            "fileloglevel": "DEBUG",
            "consolelog": 1,
            "consoleloglevel": f'{logger_consoleloglevel}',
        },
        "telegram": {
            "client_id": f'{telegram_client_id}',
            "token": f'{telegram_token}',
        },
    }

    return {"config.json": json.dumps(configmap, indent=4)}


@kopf.on.create('bots')
def create_bot(spec, name, namespace, logger, **kwargs):
    configmap_data = create_configmap_data(**spec)

    create_configmap(name=name, namespace="cryptobot", data=configmap_data)
    create_deployment(name=name, namespace="cryptobot")


@kopf.on.update('bots')
def update_bot(spec, name, namespace, logger, **kwargs):
    configmap_data = create_configmap_data(**spec)
    update_configmap(name=name, namespace="cryptobot", data=configmap_data)
    update_deployment(name=name, namespace="cryptobot")


@kopf.on.delete('bots')
def delete_bot(spec, name, namespace, logger, **kwargs):
    delete_deployment(name=name, namespace="cryptobot")
    delete_configmap(name=name, namespace="cryptobot")
