from libs.constants.files import FILE_CONFIG_SECRETS
from libs.openhab.generic import OpenhabClient
from dotenv import dotenv_values
import dataclasses


THING_TYPE_KOSTAL = "kostalinverter:piko1020"
CHANNELS_TO_USE = [
    {
        "typeUID": "kostalinverter:device-local-grid-output-power",
        "myLabel": "Grid Output Power",
    },
    {
        "typeUID": "kostalinverter:statistic-yield-day-second-gen",
        "myLabel": "Statistic Yield Day Second Gen",
    },
    {
        "typeUID": "kostalinverter:statistic-yield-total-second-gen",
        "myLabel": "Statistic Yield Total Second Gen",
    },
    {
        "typeUID": "kostalinverter:device-local-operating-status",
        "myLabel": "Device Local Operating Status",
    },
]


@dataclasses.dataclass
class KostalInverter:
    ip_address: str
    password: str
    openhab: OpenhabClient
    user: str = "pvserver"
    location: str = "SuedWest"
    label: str = "KOSTAL PIKO 4.2"
    name: str = "Solar1"
    channels: list = dataclasses.field(default_factory=list)

    def __init__(self, openhab: OpenhabClient):
        config = dotenv_values(FILE_CONFIG_SECRETS)

        ip = config["KOSTAL_PICO_IP"]
        user = config["KOSTAL_PICO_USER"]
        password = config["KOSTAL_PICO_PASSWORD"]
        location = config["KOSTAL_PICO_LOCATION"]
        name = config["KOSTAL_PICO_NAME"]

        self.openhab = openhab

        if name is not None:
            self.name = name

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
        name = self.name

        result = self.openhab.object_exists(
            objectType="thing",
            checkType="thingTypeUID",
            checkText=THING_TYPE_KOSTAL,
        )

        if result is None:
            # Build the data thing
            data = self.build_kostal_thing(name)
            # Create the data thing
            data_response = self.openhab.post(type="thing", data=data)
            result = data_response.json()

        # Get the channels
        self.channels = self.get_thing_channels()

        return result

    def get_thing_channels(self):
        result = []
        data_response = self.openhab.get("thing-type", THING_TYPE_KOSTAL)
        data_response_json = data_response.json()
        channels = data_response_json["channels"]
        for channel in channels:
            for channel_to_use in CHANNELS_TO_USE:
                if channel["typeUID"] == channel_to_use["typeUID"]:
                    result.append(channel)
        return result

    # Build the poller json payload
    def build_kostal_things(self) -> dict:
        for channel in self.channels:
            print(channel)
            data = {
                "name": f"{self.name}_Grid_Output_Power",
                "label": "Grid Output Power",
                "category": "Energy",
                "groupNames": [],
                "type": "Number:Power",
                "tags": ["Point"],
            }

        return data
