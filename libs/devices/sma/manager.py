import os
from libs.openhab.generic import OpenhabClient
import dataclasses
from libs.constants.files import FILE_CONFIG_SECRETS
from dotenv import dotenv_values


@dataclasses.dataclass
class SmaManager:
    openhab: OpenhabClient
    serial_number: str
    location: str = "Schaltschrank"
    label: str = "SMA Manager"

    def __init__(self, openhab: OpenhabClient):
        self.openhab = openhab

        config = dotenv_values(FILE_CONFIG_SECRETS)

        self.serial_number = config["SMA_MANAGER_SERIAL_NUMBER"]

    # Add the SMA Manager thing
    def add_as_thing(self) -> dict:
        name = self.label
        result = self.exists_sma_manager_thing()

        if result is False:
            # Build the data thing
            data = self.build_sma_manager_thing(name)
            # Create the data thing
            data_response = self.openhab.post(type="thing", data=data)
            result = data_response.json()

        return result

    # Build the poller json payload
    def build_sma_manager_thing(self, name: str) -> dict:
        myuuid = os.urandom(5).hex()

        data = {
            "UID": f"smaenergymeter:energymeter:{myuuid}",
            "label": name,
            "configuration": {
                "serialNumber": f"{self.serial_number}",
            },
            "thingTypeUID": "smaenergymeter:energymeter",
            "ID": myuuid,
            "location": self.location,
        }

        return data

    # Returns False if not exists or the thing object if exists
    def exists_sma_manager_thing(self):
        result = False
        response = self.openhab.get("thing")
        if response is not None:
            response_json = response.json()

            for thing in response_json:
                if thing["thingTypeUID"] == "smaenergymeter:energymeter":
                    return thing

        return result
