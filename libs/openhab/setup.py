import dataclasses
from libs.openhab.generic import OpenhabClient


@dataclasses.dataclass
class OpenhabThing:
    openhab: OpenhabClient
    thingType: str
    thingTypeUid: str
    id: str
    uid: str
    label: str
    location: str
    configuration: dict
    channels: list

    def __init__(self, openhab: OpenhabClient, thingTypeUid: str):
        self.openhab = openhab
        self.thingType = thingTypeUid
        self.thingTypeUid = thingTypeUid

    def exists(self):
        openhab = self.openhab
        return openhab.object_exists(
            objectType="thing", checkType=self.thingTypeUid, thingType=self.thingType
        )

    def createThing(self):
        openhab = self.openhab
        data = {
            "UID": self.uid,
            "label": self.label,
            "configuration": self.configuration,
            "channels": self.channels,
            "thingTypeUID": self.thingTypeUid,
            "ID": self.id,
            "location": self.location,
        }
        data_response = self.openhab.post(type="thing", data=data)
        result = data_response.json()

        return result

    def getThingChannels(self, thingType: str):
        channels = []
        data_response = self.openhab.get("thing-type", thingType)
        data_response_json = data_response.json()
        channels = data_response_json["channels"]

        return channels
