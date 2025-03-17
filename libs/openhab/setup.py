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
                "configuration": config.configuration_for_setup,
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

        # start = thing["configuration"]["port"]
        # length = thing["configuration"]["id"]
        maxTries = thing["configuration"]["connectMaxTries"]
        location = thing["location"]
        bridgeUID = thing["UID"]

        channelsToCreate = thingConfig.configuration_complete["modbus_channel_config"]

        for channel in channelsToCreate:
            valueType = channel.valueType

            pollerLabel = f"{thingConfig.label} - Poller - {channel.name}"
            dataLabel = f"{thingConfig.label} - Data - {channel.name}"
            itemLabel = f"{thingConfig.label} - {channel.name}"

            start = channel.address
            length = channel.length

            modbus_poller = create_modbus_poller(
                openhab=openhab,
                label=pollerLabel,
                uid=bridgeUID,
                start=start,
                length=length,
                maxTries=maxTries,
                location=location,
            )

            modbus_data = create_modbus_data(
                openhab=openhab,
                label=dataLabel,
                uid=modbus_poller["UID"],
                valueType=valueType,
                start=start,
                maxTries=maxTries,
                transformation=channel.transformation,
            )

            item = create_modbus_item(
                openhab=openhab,
                thingConfig=self.thingConfig,
                channel=channel,
                uidModbusData=modbus_data["UID"],
            )
            self.items.append(item)


def create_modbus_poller(
    openhab: OpenhabClient,
    label: str,
    uid: str,
    start: str,
    length: str,
    maxTries: str,
    location: str,
):
    config_poller = {
        "label": label,
        "bridgeUID": uid,
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

    modbus_poller = openhab.object_exists(
        objectType="thing",
        checkType="label",
        checkText=label,
    )

    if modbus_poller is None:
        modbus_poller_response = openhab.post(type="thing", data=config_poller)
        modbus_poller = modbus_poller_response.json()

    return modbus_poller


def create_modbus_data(
    openhab: OpenhabClient,
    label: str,
    uid: str,
    valueType: str,
    start: str,
    maxTries: str,
    transformation: str,
):
    if transformation is None:
        transformation = "default"

    modbus_config_data = {
        "label": label,
        "bridgeUID": uid,
        "configuration": {
            "readValueType": valueType,
            "readTransform": transformation,
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

    modbus_data = openhab.object_exists(
        objectType="thing",
        checkType="label",
        checkText=label,
    )

    if modbus_data is None:
        modbus_data_response = openhab.post(type="thing", data=modbus_config_data)
        modbus_data = modbus_data_response.json()

    return modbus_data


def create_modbus_item(
    openhab: OpenhabClient, thingConfig: ThingConfig, channel: dict, uidModbusData: str
):
    channel_address = channel.address

    label = f"{thingConfig.label_name} - {channel.name} ({channel_address})"
    id = cleanup_string(label)

    item_data = {
        "category": "energy",
        "groupNames": [],
        "label": label,
        "name": id,
        "tags": ["Point"],
        "type": "Number",
    }

    modbus_item = openhab.object_exists(
        objectType="thing",
        checkType="label",
        checkText=label,
    )

    if modbus_item is None:
        data_response = openhab.put(type="item", data=item_data, id=id)
        modbus_item = data_response.json()

        itemName = modbus_item["name"]
        modbus_data_UID = uidModbusData
        data_link = {
            "channelUID": f"{modbus_data_UID}:number",
            "configuration": {},
            "itemName": itemName,
        }

        openhab.put(
            type="link", data=data_link, id=f"{itemName}/{modbus_data_UID}:number"
        )
        item_data = item_data

    return modbus_item
