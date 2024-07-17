import requests
import sys
from requests.auth import HTTPBasicAuth
from dotenv import dotenv_values
from libs.constants.files import FILE_CONFIG_OPENHAB
import json


config = dotenv_values(FILE_CONFIG_OPENHAB)
ip = config["OPENHAB_IP"]
user = config["OPENHAB_USER"]
password = config["OPENHAB_PASSWORD"]
token = config["OPENHAB_TOKEN"]


def openhab_post(type: str, data):
    base_url = f"http://{ip}:8080/rest"
    headers = {
        "Content-type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer %s" % token,
    }
    url = f"{base_url}/{type}s"

    # convert data to a string
    data = json.dumps(data)

    try:
        response = requests.post(url=url, data=data, headers=headers)
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as errh:
        print(errh)
        sys.exit(1)
    except requests.exceptions.ConnectionError as errc:
        print(errc)
        sys.exit(1)
    except requests.exceptions.Timeout as errt:
        print(errt)
        sys.exit(1)
    except requests.exceptions.RequestException as err:
        print(err)
        sys.exit(1)


def openhab_put(type: str, id: str, data: dict):
    base_url = f"http://{ip}:8080/rest"
    headers = {
        "Content-type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer %s" % token,
    }
    url = None
    if id is not None:
        url = f"{base_url}/{type}s/{id}"
    else:
        url = f"{base_url}/{type}s"

    # convert data to a string
    data = json.dumps(data)

    try:
        response = requests.put(url=url, data=data, headers=headers)
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as errh:
        print(errh)
        sys.exit(1)
    except requests.exceptions.ConnectionError as errc:
        print(errc)
        sys.exit(1)
    except requests.exceptions.Timeout as errt:
        print(errt)
        sys.exit(1)
    except requests.exceptions.RequestException as err:
        print(err)
        sys.exit(1)


def openhab_delete(type: str, uid: str):
    base_url = f"http://{ip}:8080/rest"
    auth = HTTPBasicAuth(username=user, password=password)
    headers = {
        "Content-type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer %s" % token,
    }

    url = f"{base_url}/{type}s/{uid}"

    try:
        response = requests.delete(url, auth=auth, headers=headers, timeout=8)
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as errh:
        print(errh)
        sys.exit(1)
    except requests.exceptions.ConnectionError as errc:
        print(errc)
        sys.exit(1)
    except requests.exceptions.Timeout as errt:
        print(errt)
        sys.exit(1)
    except requests.exceptions.RequestException as err:
        print(err)
        sys.exit(1)


def openhab_get(type: str):
    base_url = f"http://{ip}:8080/rest"
    auth = HTTPBasicAuth(username=user, password=password)
    headers = {"Content-type": "application/json", "Accept": "application/json"}

    url = f"{base_url}/{type}s"

    try:
        response = requests.get(url, auth=auth, headers=headers, timeout=8)
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as errh:
        print(errh)
        sys.exit(1)
    except requests.exceptions.ConnectionError as errc:
        print(errc)
        sys.exit(1)
    except requests.exceptions.Timeout as errt:
        print(errt)
        sys.exit(1)
    except requests.exceptions.RequestException as err:
        print(err)
        sys.exit(1)
