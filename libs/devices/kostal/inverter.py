import os
from libs.constants.files import FILE_CONFIG_SECRETS
from libs.openhab.generic import OpenhabClient
from dotenv import dotenv_values
import dataclasses


@dataclasses.dataclass
class KostalInverter:
    ip_address: str
    password: str
    openhab: OpenhabClient
    user: str = "pvserver"
    location: str = "SuedWest"
    label: str = "KOSTAL PIKO 4.2"

    def __init__(self, openhab: OpenhabClient):
        config = dotenv_values(FILE_CONFIG_SECRETS)

        ip = config["KOSTAL_PICO_IP"]
        user = config["KOSTAL_PICO_USER"]
        password = config["KOSTAL_PICO_PASSWORD"]
        location = config["KOSTAL_PICO_LOCATION"]

        self.openhab = openhab

        if ip is not None:
            self.ip_address = ip

        if user is not None:
            self.user = user

        if password is not None:
            self.password = password

        if location is not None:
            self.location = location

    # Add the Kostal thing
    def add_as_thing(self) -> dict:
        name = self.label
        result = self.exists_kostal_thing()

        if result is False:
            # Build the data thing
            data = self.build_kostal_thing(name)
            # Create the data thing
            data_response = self.openhab.post(type="thing", data=data)
            result = data_response.json()

        return result

    # Build the poller json payload
    def build_kostal_thing(self, name: str) -> dict:
        myuuid = os.urandom(5).hex()

        data = {
            "UID": f"kostalinverter:piko1020:{myuuid}",
            "label": name,
            "configuration": {
                "url": f"http://{self.ip_address}",
                "username": self.user,
                "password": self.password,
            },
            "channels": [],
            "thingTypeUID": "kostalinverter:piko1020",
            "ID": myuuid,
            "location": self.location,
        }

        return data

    # Returns False if not exists or the thing object if exists
    def exists_kostal_thing(self):
        result = False
        response = self.openhab.get("thing")
        if response is not None:
            response_json = response.json()

            for thing in response_json:
                if thing["thingTypeUID"] == "kostalinverter:piko1020":
                    return thing

        return result
