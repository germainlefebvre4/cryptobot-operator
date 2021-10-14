import kopf
import kubernetes
from kubernetes import client, config
from kubernetes.client.rest import ApiException
import json
from base64 import b64encode
import os


if not os.getenv('CRYPTOBOT_VERSION') or not os.getenv('CRYPTOBOT_VERSION').startswith('v'):
    print("CRYPTOBOT_VERSION is not set or not a valid version")
    exit(1)


if os.getenv('DOCKER_IMAGE_PULL_POLICY') in ["IfNotPresent", "Always"]:
    pass
else:
    os.environ["DOCKER_IMAGE_PULL_POLICY"] = "IfNotPresent"


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


def create_secret(
    name = None,
    namespace = None,
    data = None,
) -> None:
    api = client.CoreV1Api()
    secret = client.V1Secret(
        api_version = "v1",
        kind = "Secret",
        data = data,
        metadata = client.V1ObjectMeta(
            name = name,
            namespace = namespace,
        )
    )

    try:
        api_response = api.create_namespaced_secret(
            namespace = namespace,
            body = secret,
        )
    except ApiException as e:
        print("Exception when calling CoreV1Api->create_namespaced_secret: %s\n" % e)


def update_secret(
    name = None,
    namespace = None,
    data = None,
) -> None:
    api = client.CoreV1Api()
    secret = client.V1ConfigMap(
        api_version = "v1",
        kind = "Secret",
        data = data,
        metadata = client.V1ObjectMeta(
            name = name,
            namespace = namespace,
        )
    )

    try:
        api_response = api.patch_namespaced_secret(
            name = name,
            namespace = namespace,
            body = secret,
        )
    except ApiException as e:
        print("Exception when calling CoreV1Api->patch_namespaced_secret: %s\n" % e)


def delete_secret(
    name = None,
    namespace = None,
    data = None,
) -> None:
    api = client.CoreV1Api()
    try:
        api_response = api.delete_namespaced_secret(
            name = name,
            namespace = namespace
        )
    except ApiException as e:
        print("Exception when calling CoreV1Api->remove_namespaced_secret: %s\n" % e)


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
                        "image": f"germainlefebvre4/pycryptobot:{os.getenv('CRYPTOBOT_VERSION')}",
                        "imagePullPolicy": f"{os.getenv('DOCKER_IMAGE_PULL_POLICY')}",
                        "env": [{
                            "name": "PYTHONUNBUFFERED",
                            "value": "1",
                        }],
                        "ports": [{
                            "containerPort": 80,
                        }],
                        "resources": {
                            "requests": {
                                "cpu": "10m",
                                "memory": "16Mi",
                            },
                            "limits": {
                                "cpu": "1",
                                "memory": "512Mi",
                            },
                        },
                        "volumeMounts": [
                            {
                                "name": "config",
                                "mountPath": "/app/config.json",
                                "subPath": "config.json",
                            },
                            {
                                "name": "api-keys",
                                "mountPath": "/app/keys",
                                "readOnly": True,
                            },
                        ],
                    }],
                    "volumes": [
                        {
                            "name": "config",
                            "configMap": {
                                "name": f'{name}',
                            },
                        },
                        {
                            "name": "api-keys",
                            "secret": {
                                "secretName": f'{name}',
                            },
                        }
                    ],
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
                        "image": f"germainlefebvre4/pycryptobot:{os.getenv('CRYPTOBOT_VERSION')}",
                        "imagePullPolicy": f"{os.getenv('DOCKER_IMAGE_PULL_POLICY')}",
                        "env": [{
                            "name": "PYTHONUNBUFFERED",
                            "value": "1",
                        }],
                        "ports": [{
                            "containerPort": 80,
                        }],
                        "resources": {
                            "requests": {
                                "cpu": "10m",
                                "memory": "16Mi",
                            },
                            "limits": {
                                "cpu": "1",
                                "memory": "512Mi",
                            },
                        },
                        "volumeMounts": [
                            {
                                "name": "config",
                                "mountPath": "/app/config.json",
                                "subPath": "config.json",
                            },
                            {
                                "name": "api-keys",
                                "mountPath": "/app/keys",
                                "readOnly": True,
                            },
                        ],
                    }],
                    "volumes": [
                        {
                            "name": "config",
                            "configMap": {
                                "name": f'{name}',
                            },
                        },
                        {
                            "name": "api-keys",
                            "secretName": {
                                "name": f'{name}',
                                "items": [
                                    {"key": "binance.key"},
                                ],
                            },
                        }
                    ],
                },
            },
        },
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
    binance_config_disablebullonly = False,
    binance_config_disablebuynearhigh = False,
    binance_config_disablebuymacd = False,
    binance_config_disablebuyema = False,
    binance_config_disablebuyobv = False,
    binance_config_disablebuyelderray = False,
    binance_config_disablefailsafefibonaccilow = False,
    binance_config_disablefailsafelowerpcnt = False,
    binance_config_disableprofitbankupperpcnt = False,
    binance_config_disableprofitbankfibonaccihigh = False,
    binance_config_disableprofitbankreversal = False,
    logger_consoleloglevel = "INFO",
    telegram_client_id = None,
    telegram_token = None,
):
    configmap = {
        "binance": {
            "api_url": f'{binance_api_url}',
            "api_key_file" : "/app/keys/binance.key",
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
                "disablebullonly": int(binance_config_disablebullonly),
                "disablebuynearhigh": int(binance_config_disablebuynearhigh),
                "disablebuymacd": int(binance_config_disablebuymacd),
                "disablebuyema": int(binance_config_disablebuyema),
                "disablebuyobv": int(binance_config_disablebuyobv),
                "disablebuyelderray": int(binance_config_disablebuyelderray),
                "disablefailsafefibonaccilow": int(binance_config_disablefailsafefibonaccilow),
                "disablefailsafelowerpcnt": int(binance_config_disablefailsafelowerpcnt),
                "disableprofitbankupperpcnt": int(binance_config_disableprofitbankupperpcnt),
                "disableprofitbankfibonaccihigh": int(binance_config_disableprofitbankfibonaccihigh),
                "disableprofitbankreversal": int(binance_config_disableprofitbankreversal),
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


def restart_deployment(
    name = None,
    namespace = None,
):
    api = client.AppsV1Api()
    try:
        api_response = api.patch_namespaced_deployment_scale(
            name = name,
            namespace = namespace,
            body={"spec": {"replicas": 0}}
        )
    except ApiException as e:
        print("Exception when calling AppsV1Api->patch_namespaced_deployment_scale->0: %s\n" % e)
    try:
        api_response = api.patch_namespaced_deployment_scale(
            name = name,
            namespace = namespace,
            body={"spec": {"replicas": 1}}
        )
    except ApiException as e:
        print("Exception when calling AppsV1Api->patch_namespaced_deployment_scale->1: %s\n" % e)


def create_secret_data(
    binance_api_key = None,
    binance_api_secret = None,
):
    secret = b64encode(f'{binance_api_key}\n{binance_api_secret}'.encode("ascii")).decode("ascii")

    return {"binance.key": f"{secret}"}


@kopf.on.create('bots')
def create_bot(spec, name, namespace, logger, **kwargs):
    configmap_data = create_configmap_data(**spec)
    secret_data = create_secret_data(spec.get("binance_api_key"), spec.get("binance_api_secret"))

    create_secret(name=name, namespace="cryptobot", data=secret_data)
    create_configmap(name=name, namespace="cryptobot", data=configmap_data)
    create_deployment(name=name, namespace="cryptobot")


@kopf.on.update('bots')
def update_bot(spec, name, namespace, logger, **kwargs):
    configmap_data = create_configmap_data(**spec)
    secret_data = create_secret_data(spec.get("binance_api_key"), spec.get("binance_api_secret"))

    update_secret(name=name, namespace="cryptobot", data=secret_data)
    update_configmap(name=name, namespace="cryptobot", data=configmap_data)
    update_deployment(name=name, namespace="cryptobot")
    restart_deployment(name=name, namespace="cryptobot")


@kopf.on.delete('bots')
def delete_bot(spec, name, namespace, logger, **kwargs):
    delete_secret(name=name, namespace="cryptobot")
    delete_deployment(name=name, namespace="cryptobot")
    delete_configmap(name=name, namespace="cryptobot")
