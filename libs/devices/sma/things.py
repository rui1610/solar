from libs.openhab.generic import openhab_post, openhab_delete, openhab_put
from libs.constants.sma import SMA_MODBUS_BRIDGE_UID
from libs.constants.files import FILE_CONFIG_SMA_METADATA
import json


def get_sma_things():
    # read file with SMA things
    # with open(FILE_CONFIG_OPENHAB_SMA_THINGS, "r") as f:
    #     data = json.load(f)
    #     return data
    with open(FILE_CONFIG_SMA_METADATA, "r") as f:
        data = json.load(f)
        return data


# Build the poller json payload
def build_modbus_poller(bridgeUID: str, label: str, start: int, length: int) -> dict:
    display_name = f"Poller SMA {label} ({start})"

    data = {
        "label": display_name,
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
        "location": "",
        "channels": [],
        "statusInfo": {},
        "firmwareStatus": {},
    }

    return data


# Build the data json payload
def build_modbus_data(bridgeUID: str, label: str, start: int, valueType: str) -> dict:
    labelData = f"Data SMA {label} ({start})"
    data = {
        "label": labelData,
        "bridgeUID": bridgeUID,
        "configuration": {
            "readValueType": valueType,
            "readTransform": "default",
            "writeTransform": "default",
            "readStart": start,
            "updateUnchangedValuesEveryMillis": 5000,
            "writeMaxTries": 3,
        },
        "properties": {},
        "thingTypeUID": "modbus:data",
        "location": "",
        "statusInfo": {},
        "firmwareStatus": {},
    }

    return data


# Build the item json payload
def build_modbus_item(label: str, channelID: str) -> dict:
    item_name = f"SMA {label} {channelID}_Value_as_Number".replace(" ", "_")
    item_label = f"SMA {label} ({channelID})"

    data = [
        {
            "link": f"http://192.168.178.78:8080/rest/items/{item_name}",
            "state": "3900 W",
            "unitSymbol": "W",
            "metadata": {"semantics": {"value": "Point"}},
            "editable": True,
            "type": "Number:Power",
            "name": item_name,
            "label": item_label,
            "category": "",
            "tags": ["Point"],
            "groupNames": [],
        }
    ]
    return data


# Add the item as linkedItem to the data thing
def add_item_to_data(item: dict, item_name: str) -> dict:
    # detect the right channel for the item with channelTypeUID = "modbus:number-type"
    for value in item["channels"]:
        if value["channelTypeUID"] == "modbus:number-type":
            # ... and add the item to the linkedItems
            value["linkedItems"] = [item_name]

    data_response = openhab_put(type="thing", data=item, id=item["UID"])

    return data_response


# Add the SMA poller
def add_sma_poller(label: str, channelID: str, valueType: str) -> dict:
    # set the default length
    length = 2

    # set the length based on the valueType
    match valueType:
        case "int32":
            length = 2
        case "int64":
            length = 4
        case "STR32":
            length = 32
        case "U32":
            length = 2
        case "U64":
            length = 4
        case "S32":
            length = 2
        case "U16":
            length = 1
        case "S16":
            length = 1

    # Build the poller thing
    poller = build_modbus_poller(
        bridgeUID=SMA_MODBUS_BRIDGE_UID, label=label, start=channelID, length=length
    )
    # Create the poller thing
    poller_response = openhab_post(type="thing", data=poller)
    response_poller = poller_response.json()

    return response_poller


# Add the SMA thing
def add_sma_thing(
    label: str, channelID: str, valueType: str, poller_bridgeUID: str
) -> dict:
    # Build the data thing
    data = build_modbus_data(
        bridgeUID=poller_bridgeUID,
        label=label,
        start=channelID,
        valueType=valueType,
    )
    # Create the data thing
    data_response = openhab_post(type="thing", data=data)
    response_data = data_response.json()

    return response_data


# Add the SMA item
def add_sma_item(label: str, channelID: str) -> dict:
    # Build the item
    item = build_modbus_item(label=label, channelID=channelID)
    # Create the item
    item_response = openhab_put(type="item", data=item, id=None)
    response_data = item_response.json()

    return response_data


# Add the SMA data thing
def add_sma_data(
    label: str, channelID: str, valueType: str, poller_bridgeUID: str
) -> dict:
    # Create the data thing
    # Build the data thing
    data = build_modbus_data(
        bridgeUID=poller_bridgeUID,
        label=label,
        start=channelID,
        valueType=valueType,
    )
    # Create the data thing
    data_response = openhab_post(type="thing", data=data)
    response_data = data_response.json()

    return response_data


# Add the SMA channel
def add_sma_channel(uids: list, label: str, channelID: str, valueType: str) -> dict:
    # Create the poller thing
    response_poller = add_sma_poller(
        label=label, channelID=channelID, valueType=valueType
    )
    poller_bridgeUID = response_poller["UID"]
    uids.append(poller_bridgeUID)

    # Create the item
    response_item = add_sma_item(label=label, channelID=channelID)
    item_name = response_item[0]["name"]

    # Create the data thing
    response_data = add_sma_data(
        label=label,
        channelID=channelID,
        valueType=valueType,
        poller_bridgeUID=poller_bridgeUID,
    )

    # append the item name to the data thing as a linked item
    response_data = add_item_to_data(item=response_data, item_name=item_name)
    data_uid = response_data["UID"]
    uids.append(data_uid)

    # reverse the list of UIDs
    uids.reverse()

    return uids


# Delete the SMA channels
def delete_sma_channel(uids: str):
    # iterate over the UID and delete the things
    for uid in uids:
        response = openhab_delete(type="thing", uid=uid)
