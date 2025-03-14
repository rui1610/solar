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
            thisConfiguration = {
                "host": config.configuration["host"],
                "id": config.configuration["id"],
                "port": config.configuration["port"],
            }
            data = {
                "UID": config.uid,
                "label": config.label,
                "configuration": thisConfiguration,
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
                "category": "energy",
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
        thingConfig = self.thingConfig

        start = thing["configuration"]["port"]
        length = thing["configuration"]["id"]
        maxTries = thing["configuration"]["connectMaxTries"]
        location = thing["location"]
        bridgeUID = thing["UID"]

        channelsToCreate = thingConfig.configuration["modbus_channel_config"]

        for channel in channelsToCreate:
            valueType = channel["valueType"]

            pollerLabel = f"{thingConfig.label} - Poller"
            dataLabel = f"{thingConfig.label} - Data"
            itemLabel = f"{channel['label']}"

            config_poller = {
                "label": pollerLabel,
                "bridgeUID": bridgeUID,
                "configuration": {
                    "start": start,
                    "length": length,
                    "refresh": 5000,
                    "maxTries": maxTries,
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

            modbus_poller_response = openhab.post(type="thing", data=config_poller)
            modbus_poller = modbus_poller_response.json()

            pollerUID = modbus_poller["UID"]

            modbus_config_data = {
                "label": dataLabel,
                "bridgeUID": pollerUID,
                "configuration": {
                    "readValueType": valueType,
                    "readTransform": "default",
                    "writeTransform": "default",
                    "readStart": str(start),
                    "updateUnchangedValuesEveryMillis": 5000,
                    "writeMaxTries": maxTries,
                },
                "properties": {},
                "thingTypeUID": "modbus:data",
                "location": "",
                "statusInfo": {},
                "firmwareStatus": {},
            }
            modbus_data_response = openhab.post(type="thing", data=modbus_config_data)
            modbus_data = modbus_data_response.json()

            id = cleanup_string(itemLabel)
            item_data = {
                "category": "energy",
                "groupNames": [],
                "label": itemLabel,
                "name": id,
                "tags": ["Point"],
                "type": "Number",
            }
            data_response = self.openhab.put(type="item", data=item_data, id=id)
            item = data_response.json()
            self.items.append(item)

            itemName = item["name"]
            modbus_data_UID = f"{modbus_data['UID']}"
            data_link = {
                "channelUID": f"{modbus_data_UID}:number",
                "configuration": {},
                "itemName": itemName,
            }

            self.openhab.put(
                type="link", data=data_link, id=f"{itemName}/{modbus_data_UID}:number"
            )
            item_data = item_data
