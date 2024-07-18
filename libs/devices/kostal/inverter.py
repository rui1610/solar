import os
from libs.constants.files import FILE_CONFIG_SECRETS
from libs.openhab.generic import openhab_post, openhab_get
from dotenv import dotenv_values

config = dotenv_values(FILE_CONFIG_SECRETS)


# Build the poller json payload
def build_kostal_thing(name: str) -> dict:
    myuuid = os.urandom(5).hex()

    ip = config["KOSTAL_PICO_IP"]
    user = config["KOSTAL_PICO_USER"]
    password = config["KOSTAL_PICO_PASSWORD"]

    data = {
        "UID": f"kostalinverter:piko1020:{myuuid}",
        "label": name,
        "configuration": {
            "url": f"http://{ip}",
            "username": user,
            "password": password,
        },
        "channels": [],
        "thingTypeUID": "kostalinverter:piko1020",
        "ID": myuuid,
    }

    return data


# Add the SMA thing
def add_kostal_inverter_thing(name: str = "KOSTAL PIKO 4.2") -> dict:
    result = exists_kostal_thing()

    if result is False:
        # Build the data thing
        data = build_kostal_thing(name)
        # Create the data thing
        data_response = openhab_post(type="thing", data=data)
        result = data_response.json()

    return result


# Returns False if not exists or the thing object if exists
def exists_kostal_thing():
    result = False
    response = openhab_get("thing")
    if response is not None:
        response_json = response.json()

        for thing in response_json:
            if thing["thingTypeUID"] == "kostalinverter:piko1020":
                return thing

    return result
