import requests
from dotenv import dotenv_values
from libs.constants.files import FILE_CONFIG_SECRETS
import json
import time
import urllib.parse
import sys

SLEEP_TIME_SECONDS_WRITE = 2
SLEEP_TIME_SECONDS_READ = 0
SLEEP_TIME_SECONDS_DELETE = 2

config = dotenv_values(FILE_CONFIG_SECRETS)
ip = config["OPENHAB_IP"]
user = config["OPENHAB_USER"]
password = config["OPENHAB_PASSWORD"]
token = config["OPENHAB_TOKEN"]


def openhab_post(type: str, data):
    # Add a delay for not getting into any throteling issues
    time.sleep(SLEEP_TIME_SECONDS_WRITE)

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
    # Add a delay for not getting into any throteling issues
    time.sleep(SLEEP_TIME_SECONDS_WRITE)

    base_url = f"http://{ip}:8080/rest"
    headers = {
        "Content-type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer %s" % token,
    }
    url = None
    if id is not None:
        id = urllib.parse.quote(id)
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
    # Add a delay for not getting into any throteling issues
    time.sleep(SLEEP_TIME_SECONDS_DELETE)

    base_url = f"http://{ip}:8080/rest"
    headers = {
        "Content-type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer %s" % token,
    }

    url = f"{base_url}/{type}s/{uid}"

    try:
        response = requests.delete(url, headers=headers, timeout=8)
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as errh:
        print(errh)
        # sys.exit(1)
    except requests.exceptions.ConnectionError as errc:
        print(errc)
        # sys.exit(1)
    except requests.exceptions.Timeout as errt:
        print(errt)
        # sys.exit(1)
    except requests.exceptions.RequestException as err:
        print(err)
        # sys.exit(1)


def openhab_get(type: str):
    # Add a delay for not getting into any throteling issues
    time.sleep(SLEEP_TIME_SECONDS_READ)

    base_url = f"http://{ip}:8080/rest"
    # auth = HTTPBasicAuth(username=user, password=password)
    headers = {
        "Content-type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer %s" % token,
    }
    url = f"{base_url}/{type}s"

    try:
        response = requests.get(url, headers=headers, timeout=8)
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as errh:
        print(errh)
        # sys.exit(1)
    except requests.exceptions.ConnectionError as errc:
        print(errc)
        # sys.exit(1)
    except requests.exceptions.Timeout as errt:
        print(errt)
        # sys.exit(1)
    except requests.exceptions.RequestException as err:
        print(err)
        # sys.exit(1)


def delete_all_objects():
    # Don't change the sequence of the objectTypes!
    objectTypes = ["item", "link", "thing"]

    for objectType in objectTypes:
        response = openhab_get(objectType)
        if response is not None:
            myObjects = response.json()

            for myObject in myObjects:
                try:
                    match objectType:
                        case "thing":
                            openhab_delete(uid=myObject["UID"], type=objectType)
                        case "link":
                            openhab_delete(uid=myObject["itemName"], type=objectType)
                        case "item":
                            openhab_delete(uid=myObject["name"], type=objectType)
                except Exception as e:
                    print(e)
