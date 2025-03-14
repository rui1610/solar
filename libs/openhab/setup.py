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
    modbus_poller: list
    modbus_data: list

    def __init__(self, openhab: OpenhabClient, thingConfig: ThingConfig):
        self.openhab = openhab
        self.thingConfig = thingConfig
        self.items = []

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
            self.items.append(item)

            itemName = item["name"]
            channelUID = f"{channel['uid']}"
            data_link = {
                "channelUID": channelUID,
                "configuration": {},
                "itemName": itemName,
            }

            self.openhab.put(type="link", data=data_link, id=f"{itemName}/{channelUID}")

    def createModbusItems(self, channelsToUse: list = None):
        thing = self.thing
        openhab = self.openhab

        start = thing["configuration"]["port"]
        length = thing["configuration"]["id"]
        maxTries = thing["configuration"]["connectMaxTries"]
        location = thing["location"]
        bridgeUID = thing["thingTypeUID"]

        channelsToCreate = thing["configuration"]["modbus_channel_config"]

        for channel in channelsToCreate:

            valueType = channel[]

            pollerLabel = f"{thing.label} - Poller"
            dataLabel = f"{thing.label} - Data"

            config_poller = {
                "label": pollerLabel,
                "bridgeUID": bridgeUID,
                "configuration": {
                    "start": start,
                    "length": length,
                    "refresh": 5000,
                    "maxTries": 3,
                    "cacheMillis": 50,
                    "type": "input",
                },
                "properties": {},
                "thingTypeUID": "modbus:poller",
                "location": location,
                "channels": [],
                "statusInfo": {},
                "firmwareStatus": {},
            }

            poller_response = openhab.post(type="thing", data=config_poller)
            poller = poller_response.json()

            pollerUID = poller["UID"]

            config_data = {
                "label": dataLabel,
                "bridgeUID": bridgeUID,
                "configuration": {
                    "readValueType": inverter.valueType,
                    "readTransform": "default",
                    "writeTransform": "default",
                    "readStart": str(start),
                    "updateUnchangedValuesEveryMillis": 5000,
                    "writeMaxTries": 3,
                },
                "properties": {},
                "thingTypeUID": "modbus:data",
                "location": "",
                "statusInfo": {},
                "firmwareStatus": {},
            }
