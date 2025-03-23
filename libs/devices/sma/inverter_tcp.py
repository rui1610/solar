import dataclasses
from dotenv import dotenv_values
from libs.constants.files import FILE_CONFIG_SECRETS
from libs.constants.sma_inverter import RAW_KEYS, RAW_KEYS_MAPPING
import requests
import json


CONFIG = dotenv_values(FILE_CONFIG_SECRETS)
BASE_URL = f"https://{CONFIG['SMA_INVERTER_IP']}"


@dataclasses.dataclass
class SMAInverterValue:
    key: str
    name: str
    value: str


@dataclasses.dataclass
class SMAInverterClient:
    ip_address: str
    token: str

    def __init__(self):
        self.ip_address = CONFIG["SMA_INVERTER_IP"]
        self.token = getToken()

    def getValues(self):
        url = f"{BASE_URL}/dyn/getValues.json?sid={self.token}"
        headers = {"Content-type": "application/json"}

        data = {"destDev": [], "keys": RAW_KEYS}

        try:
            response = requests.post(
                url=url, headers=headers, verify=False, data=json.dumps(data)
            )
            response_code = response.status_code
            if response_code != 200:
                print(f"Error getting values: {response_code}")
                self.logout()
                return None
            response_result = response.json()

            result = extract_all_vals(response_result)

            return result
        except requests.exceptions.RequestException as e:
            print(f"Error getting values: {e}")
            self.logout()
            return None

    def logout(self):
        url = f"{BASE_URL}/dyn/logout.json?sid={self.token}"
        headers = {"Content-type": "application/json"}

        try:
            response = requests.post(url=url, headers=headers, verify=False)
            print("logout", response.json())
            return None
        except requests.exceptions.RequestException as e:
            print(e)
            return None


def getToken():
    user = CONFIG["SMA_INVERTER_USER"]
    password = CONFIG["SMA_INVERTER_PASSWORD"]

    url = f"{BASE_URL}/dyn/login.json"
    headers = {
        "Content-type": "application/json;charset=UTF-8",
        "Accept": "application/json, text/plain, */*",
        # "Connection": "keep-alive",
    }
    data = {
        "right": user,
        "pass": password,
    }
    try:
        response = requests.post(
            url=url,
            headers=headers,
            data=json.dumps(data),
            verify=False,
        )
    except requests.exceptions.RequestException as e:
        print(e)
        return None
    response_code = response.status_code
    if response_code != 200:
        print(f"Error getting token: {response_code}")
        return None
    # get the response code

    return response.json()["result"]["sid"]


def extract_all_vals(data):
    """
    Extracts all 'val' values for all keys from the JSON structure.

    Args:
        data (dict): The JSON data.

    Returns:
        A dictionary where keys are the keys from the JSON and values are the extracted 'val'.
    """
    extracted_vals = {}
    try:
        # Navigate to the "result" section
        result = data.get("result", {})
        for device_id, device_data in result.items():
            for key, value_data in device_data.items():
                val_data = value_data.get("9", [{}])[0]
                extracted_vals[key] = val_data.get("val")
    except (KeyError, IndexError, TypeError):
        pass

    result = []
    # iterate over the keys and map it  to RAW_KEYS_MAPPING
    for key, value in extracted_vals.items():
        for mapping in RAW_KEYS_MAPPING:
            # if the key is in the RAW_KEYS_MAPPING
            if key == mapping["key"]:
                # get the name of the key
                name = mapping["name"]
                # create a new object with the key, name and value
                item = SMAInverterValue(key=key, name=name, value=value)

                # if the item is not in the result list, add it
                if item not in result:
                    result.append(item)

    return result
