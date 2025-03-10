import os
from libs.openhab.generic import OpenhabClient
import dataclasses
from libs.constants.files import FILE_CONFIG_SECRETS
from dotenv import dotenv_values


@dataclasses.dataclass
class SmaManager:
    openhab: OpenhabClient
    serial_number: str
    name: str = "Solar2 - SMA Manager"
    location: str = "Schaltschrank"
    label: str = "SMA Manager"

    def __init__(self, openhab: OpenhabClient):
        self.openhab = openhab

        config = dotenv_values(FILE_CONFIG_SECRETS)

        self.serial_number = config["SMA_MANAGER_SERIAL_NUMBER"]

    # Add the SMA Manager thing
    def add_as_thing(self) -> dict:
        name = self.name
        openhab = self.openhab
        result = None

        exists = openhab.object_exists(
            objectType="thing",
            checkType="thingTypeUID",
            checkText="smaenergymeter:energymeter",
        )
        # result = self.exists_sma_manager_thing(self.openhab)

        if exists is False:
            # Build the data thing
            data = build_sma_manager_thing(self, name)
            # Create the data thing
            data_response = self.openhab.post(type="thing", data=data)
            result = data_response.json()

        sma_manager_item_exists = openhab.object_exists(
            objectType="thing",
            checkType="thingTypeUID",
            checkText="smaenergymeter:energymeter",
        )

        return result


# Build the poller json payload
def build_sma_manager_thing(smaManager: SmaManager, name: str) -> dict:
    myuuid = os.urandom(5).hex()

    data = {
        "UID": f"smaenergymeter:energymeter:{myuuid}",
        "label": name,
        "configuration": {
            "serialNumber": f"{smaManager.serial_number}",
        },
        "thingTypeUID": "smaenergymeter:energymeter",
        "ID": myuuid,
        "location": smaManager.location,
    }

    return data
