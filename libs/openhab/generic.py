import requests
from dotenv import dotenv_values
from libs.constants.files import FILE_CONFIG_SECRETS
import json
import time
import urllib.parse
import sys
import dataclasses

SLEEP_TIME_SECONDS_WRITE = 0
SLEEP_TIME_SECONDS_READ = 0
SLEEP_TIME_SECONDS_DELETE = 0


@dataclasses.dataclass
class OpenhabClient:
    ip_address: str
    user: str
    password: str
    token: str

    def __init__(self):
        config = dotenv_values(FILE_CONFIG_SECRETS)

        ip = config["OPENHAB_IP"]
        user = config["OPENHAB_USER"]
        password = config["OPENHAB_PASSWORD"]
        token = config["OPENHAB_TOKEN"]

        if ip is not None:
            self.ip_address = ip
        if user is not None:
            self.user = user
        if password is not None:
            self.password = password
        if token is not None:
            self.token = token

    def post(self, type: str, data, command=None, id=None):
        # Add a delay for not getting into any throteling issues
        time.sleep(SLEEP_TIME_SECONDS_WRITE)

        base_url = f"http://{self.ip_address}:8080/rest"
        headers = {
            "Content-type": "application/json",
            "Accept": "application/json",
            "Authorization": "Bearer %s" % self.token,
        }
        url = f"{base_url}/{type}s"
        if id is not None and command is not None:
            url = f"{url}/{id}/{command}"

        # convert data to a string
        if data is not None:
            data = json.dumps(data)

        try:
            if data is None:
                response = requests.post(url=url, headers=headers)
            else:
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

    def put(self, type: str, id: str, data: dict, additions: str = None):
        # Add a delay for not getting into any throteling issues
        time.sleep(SLEEP_TIME_SECONDS_WRITE)

        base_url = f"http://{self.ip_address}:8080/rest"
        headers = {
            "Content-type": "application/json",
            "Accept": "application/json",
            "Authorization": "Bearer %s" % self.token,
        }
        url = None
        if id is not None:
            id = urllib.parse.quote(id)
            url = f"{base_url}/{type}s/{id}"
        else:
            url = f"{base_url}/{type}s"

        if additions is not None:
            url = f"{url}/{additions}"

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

    def delete(self, type: str, uid: str):
        # Add a delay for not getting into any throteling issues
        time.sleep(SLEEP_TIME_SECONDS_DELETE)

        base_url = f"http://{self.ip_address}:8080/rest"
        headers = {
            "Content-type": "application/json",
            "Accept": "application/json",
            "Authorization": "Bearer %s" % self.token,
        }

        url = f"{base_url}/{type}s/{uid}?force=true"

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

        while response.status_code != 200:
            response = requests.delete(url, headers=headers, timeout=8)
            response.raise_for_status()

    def get(self, type: str, thing_id: str = None):
        # Add a delay for not getting into any throteling issues
        time.sleep(SLEEP_TIME_SECONDS_READ)

        base_url = f"http://{self.ip_address}:8080/rest"
        # auth = HTTPBasicAuth(username=user, password=password)
        headers = {
            "Content-type": "application/json",
            "Accept": "application/json",
            "Authorization": "Bearer %s" % self.token,
        }
        url = f"{base_url}/{type}s"
        if thing_id is not None:
            url = f"{url}/{thing_id}"

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

    def delete_all_objects(self):
        # Don't change the sequence of the objectTypes!
        # objectTypes = ["link", "item", "thing"]
        objectTypes = ["link", "item", "thing"]

        for objectType in objectTypes:
            response = self.get(objectType)
            if response is not None:
                myObjects = response.json()

                for myObject in myObjects:
                    try:
                        match objectType:
                            case "thing":
                                self.delete(uid=myObject["UID"], type=objectType)
                            case "link":
                                self.delete(uid=myObject["itemName"], type=objectType)
                            case "item":
                                self.delete(uid=myObject["name"], type=objectType)
                    except Exception as e:
                        print(e)

    def install_addon(self, id: str):
        response = self.post(type="addon", data=None, command="install", id=id)
        response.raise_for_status()

    def object_exists(
        self,
        objectType: str,
        checkType: str,
        checkText: str,
    ) -> bool:
        response = self.get(objectType)
        response_json = response.json()
        for item in response_json:
            if item[checkType] == checkText:
                return item

        return None
