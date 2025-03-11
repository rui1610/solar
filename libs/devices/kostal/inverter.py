from libs.constants.files import FILE_CONFIG_SECRETS
from dotenv import dotenv_values
import dataclasses
import os

THING_TYPE_KOSTAL = "kostalinverter:piko1020"
CHANNELS_TO_USE = [
    {
        "typeUID": "kostalinverter:device-local-grid-output-power",
        "myLabel": "Solarmodule - Aktuelle Leistung",
    },
    {
        "typeUID": "kostalinverter:statistic-yield-day-second-gen",
        "myLabel": "Solarmodule - Erzeugte Energie heute",
    },
    {
        "typeUID": "kostalinverter:statistic-yield-total-second-gen",
        "myLabel": "Solarmodule - Erzeugte Energie gesamt",
    },
]


from libs.model.openhab import ThingConfig


@dataclasses.dataclass
class KostalInverter(ThingConfig):
    thingTypeUid: str
    thingType: str
    id: str
    uid: str
    label: str
    location: str
    configuration: dict
    channels: list

    def __init__(self):
        config = dotenv_values(FILE_CONFIG_SECRETS)

        ip = config["KOSTAL_PICO_IP"]
        user = config["KOSTAL_PICO_USER"]
        password = config["KOSTAL_PICO_PASSWORD"]
        location = config["KOSTAL_PICO_LOCATION"]
        name = config["KOSTAL_PICO_NAME"]

        myuuid = os.urandom(5).hex()
        self.uid = f"kostalinverter:piko1020:{myuuid}"
        self.id = myuuid
        self.label = name
        self.configuration = {
            "url": f"http://{ip}",
            "username": user,
            "password": password,
        }
        self.channels = []
        self.thingTypeUid = "kostalinverter:piko1020"
        self.thingType = "thingTypeUID"
        self.location = location


# @dataclasses.dataclass
# class KostalInverter:
#     ip_address: str
#     password: str
#     openhab: OpenhabClient
#     user: str = "pvserver"
#     location: str = "SuedWest"
#     label: str = "KOSTAL PIKO 4.2"
#     name: str = "Solar1"
#     channels: list = dataclasses.field(default_factory=list)

#     def __init__(self, openhab: OpenhabClient):
#         config = dotenv_values(FILE_CONFIG_SECRETS)

#         ip = config["KOSTAL_PICO_IP"]
#         user = config["KOSTAL_PICO_USER"]
#         password = config["KOSTAL_PICO_PASSWORD"]
#         location = config["KOSTAL_PICO_LOCATION"]
#         name = config["KOSTAL_PICO_NAME"]

#         self.openhab = openhab

#         if name is not None:
#             self.name = name

#         if ip is not None:
#             self.ip_address = ip

#         if user is not None:
#             self.user = user

#         if password is not None:
#             self.password = password

#         if location is not None:
#             self.location = location

#     # Add the Kostal thing
#     def add_as_thing(self) -> dict:
#         name = self.name
#         myuuid = None

#         result = self.openhab.object_exists(
#             objectType="thing",
#             checkType="thingTypeUID",
#             checkText=THING_TYPE_KOSTAL,
#         )

#         if result is None:
#             # Build the data thing
#             myuuid = os.urandom(5).hex()
#             data = {
#                 "UID": f"kostalinverter:piko1020:{myuuid}",
#                 "label": name,
#                 "configuration": {
#                     "url": f"http://{self.ip_address}",
#                     "username": self.user,
#                     "password": self.password,
#                 },
#                 "channels": [],
#                 "thingTypeUID": "kostalinverter:piko1020",
#                 "ID": myuuid,
#                 "location": self.location,
#             }
#             # Create the data thing
#             data_response = self.openhab.post(type="thing", data=data)
#             result = data_response.json()
#             myuuid = result["UID"]
#         else:
#             myuuid = result["UID"]

#         # Get the channels
#         self.channels = self.get_thing_channels()

#         self.build_kostal_items_from_channels(myuuid)

#         return result

#     def get_thing_channels(self):
#         result = []
#         data_response = self.openhab.get("thing-type", THING_TYPE_KOSTAL)
#         data_response_json = data_response.json()
#         channels = data_response_json["channels"]
#         for channel in channels:
#             for channel_to_use in CHANNELS_TO_USE:
#                 if channel["typeUID"] == channel_to_use["typeUID"]:
#                     channel["label"] = channel_to_use["myLabel"]
#                     result.append(channel)
#         return result

#     # Build the poller json payload
#     def build_kostal_items_from_channels(self, myuuid: str) -> dict:
#         for channel in self.channels:
#             name = cleanup_string(f"{self.name}_{channel['label']}")
#             label = f"{self.name} - {channel['label']}"
#             data = {
#                 "name": name,
#                 "label": label,
#                 "category": channel["category"],
#                 "groupNames": [],
#                 "type": "Number:Power",
#                 "tags": channel["tags"],
#             }
#             data_response = self.openhab.put(type="item", data=data, id=name)
#             result = data_response.json()

#             item_name = result["name"]

#             add_item_link(
#                 openhab=self.openhab,
#                 dataID=myuuid,
#                 itemName=item_name,
#                 channelUID=myuuid,
#                 id=channel["id"],
#             )

#         return data


# # Add the SMA item link
# def add_item_link(
#     openhab: OpenhabClient, dataID: str, itemName: str, channelUID: str, id: str
# ) -> dict:
#     # Build the item
#     item = build_item_link(channelUID=channelUID, itemName=itemName, id=id)
#     # Create the item link
#     item_response = openhab.put(type="link", data=item, id=f"{itemName}/{dataID}:{id}")


# # Build the item json payload
# def build_item_link(channelUID: str, itemName: str, id: str) -> dict:
#     data = {
#         "channelUID": f"{channelUID}:{id}",
#         "configuration": {},
#         "itemName": itemName,
#     }
#     return data
