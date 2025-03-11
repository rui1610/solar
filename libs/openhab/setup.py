import dataclasses
from libs.openhab.generic import OpenhabClient
from libs.model.openhab import ThingConfig


@dataclasses.dataclass
class OpenhabThing:
    openhab: OpenhabClient
    thingConfig: ThingConfig

    def __init__(self, openhab: OpenhabClient, thingConfig: ThingConfig):
        self.openhab = openhab
        self.thingConfig = thingConfig

    def exists(self):
        openhab = self.openhab
        return openhab.object_exists(
            objectType="thing", checkType=self.thingTypeUid, thingType=self.thingType
        )

    def createThing(self):
        openhab = self.openhab
        config = self.thingConfig

        checkIfExists = openhab.object_exists(
            objectType="thing",
            checkText=config.thingTypeUid,
            checkType=config.thingType,
        )

        if checkIfExists is None:
            data = {
                "UID": config.uid,
                "label": config.label,
                "configuration": config.configuration,
                "channels": config.channels,
                "thingTypeUID": config.thingTypeUid,
                "ID": config.id,
                "location": config.location,
            }
            data_response = openhab.post(type="thing", data=data)
            result = data_response.json()
        else:
            result = checkIfExists

        return result

    def getThingChannels(self, thingType: str):
        channels = []
        data_response = self.openhab.get("thing-type", thingType)
        data_response_json = data_response.json()
        channels = data_response_json["channels"]

        return channels
