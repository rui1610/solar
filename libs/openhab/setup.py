import dataclasses
from libs.openhab.generic import OpenhabClient
from libs.model.openhab import ThingConfig
from libs.openhab.addons import cleanup_string


@dataclasses.dataclass
class OpenhabThing:
    openhab: OpenhabClient
    thingConfig: ThingConfig
    thing: dict
    items: list

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
            self.thing = data_response.json()
        else:
            self.thing = checkIfExists

    def createItemsFromChannels(self, channelsToUse: list = None):
        thing = self.thing
        name = cleanup_string(f"{thing['label']}")

        all_channels = self.thing["channels"]

        if channelsToUse is not None and len(channelsToUse) > 0:
            filteredChannels = []
            for channel in all_channels:
                for channel_to_use in channelsToUse:
                    if channel["channelTypeUID"] == channel_to_use["typeUID"]:
                        channel["label"] = channel_to_use["myLabel"]
                        filteredChannels.append(channel)
            all_channels = filteredChannels

        for channel in all_channels:
            item_name = f"{thing['label']} - {channel['label']}"
            id = cleanup_string(item_name)
            data = {
                "category": "Energy",
                "groupNames": None,
                "label": item_name,
                "name": id,
                "tags": ["Point"],
                "type": channel["itemType"],
            }
            data_response = self.openhab.put(type="item", data=data, id=id)
            item = data_response.json()

            itemName = item["name"]
            channelUID = f"{channel['uid']}"
            data_link = {
                "channelUID": channelUID,
                "configuration": {},
                "itemName": itemName,
            }

            itemLink_response = self.openhab.put(
                type="link", data=data_link, id=f"{itemName}/{channelUID}"
            )
            # item_link = itemLink_response.json()
