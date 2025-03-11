import dataclasses
from libs.openhab.generic import OpenhabClient
from libs.model.openhab import ThingConfig, ItemConfig
from libs.openhab.addons import cleanup_string


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

    def getThingChannels(self):
        channels = []
        thingTypeUid = self.thingConfig.thingTypeUid
        data_response = self.openhab.get("thing-type", thingTypeUid)
        data_response_json = data_response.json()
        channels = data_response_json["channels"]

        return channels


@dataclasses.dataclass
class OpenhabItem:
    openhab: OpenhabClient
    thingConfig: ThingConfig
    itemConfig: ItemConfig

    def __init__(self, openhab: OpenhabClient, thingConfig: ThingConfig):
        self.openhab = openhab
        self.thingConfig = thingConfig
        self.itemConfig = ItemConfig

    def createItemFromChannel(self, channel: dict):
        openhab = self.openhab
        thingConfig = self.thingConfig
        itemConfig = self.itemConfig

        name = cleanup_string(f"{thingConfig.label} - {itemConfig.label}")

        data = {
            "name": name,
            "label": {itemConfig.label},
            "category": itemConfig.category,
            "groupNames": itemConfig.groupNames,
            "type": itemConfig.type,
            "tags": itemConfig.tags,
        }
        data_response = self.openhab.put(type="item", data=data, id=name)
        item = data_response.json()

        itemName = item["name"]

        data_link = {
            "channelUID": f"{item['UID']}:{id}",
            "configuration": {},
            "itemName": itemName,
        }

        itemLink_response = openhab.put(
            type="link", data=data_link, id=f"{itemName}/{item['UID']}:{id}"
        )
