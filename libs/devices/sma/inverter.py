from libs.openhab.generic import openhab_post, openhab_delete, openhab_put, openhab_get
from libs.constants.files import FILE_CONFIG_SMA_METADATA, FILE_CONFIG_SECRETS
import json
import os

from libs.model.sma_tripower import InverterMetadata
from dotenv import dotenv_values

config = dotenv_values(FILE_CONFIG_SECRETS)


def get_sma_things():
    result = []
    data = None
    with open(FILE_CONFIG_SMA_METADATA, "r") as f:
        data = json.load(f)

    for thing in data:
        # if thing["SMA Modbus Registeradresse"] in str(CHANNELS_TO_USE) and thing[
        if thing["SMA Modbus Datentyp"] in ["U32", "S32", "U64", "S64", "U16", "S16"]:
            result.append(thing)

    return result


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

    return data


# Build the item json payload
def build_modbus_item(label: str, channelID: str) -> dict:
    item_name = f"Item SMA {label} {channelID}_Value_as_Number".replace(
        " ", "_"
    ).replace("-", "_")
    item_label = f"Item SMA {label} ({channelID})"

    data = {
        "category": "Energy",
        "groupNames": [],
        "label": item_label,
        "name": item_name,
        "tags": ["Point"],
        "type": "Number",
    }

    return data


# Build the item json payload
def build_modbus_item_link(channelUID: str, itemName: str) -> dict:
    data = {
        "channelUID": f"{channelUID}:number",
        "configuration": {},
        "itemName": itemName,
    }
    return data


# Add the SMA poller
def add_sma_poller(label: str, channelID: str, length: int, bridgeUID: str) -> dict:
    # set the default length

    # Build the poller thing
    poller = build_modbus_poller(
        bridgeUID=bridgeUID, label=label, start=channelID, length=length
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
    item_response = openhab_put(type="item", data=item, id=item["name"])
    response_data = item_response.json()

    return response_data


# Add the SMA item link
def add_sma_item_link(dataID: str, itemName: str, channelUID: str) -> dict:
    # Build the item
    item = build_modbus_item_link(channelUID=channelUID, itemName=itemName)
    # Create the item link
    item_response = openhab_put(
        type="link", data=item, id=f"{itemName}/{dataID}:number"
    )


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
def add_sma_channel(
    uids: list, inverterMetadata: InverterMetadata, bridgeUID: str
) -> dict:
    # Create the poller thing
    response_poller = add_sma_poller(
        label=inverterMetadata.label,
        channelID=inverterMetadata.channel,
        length=inverterMetadata.length,
        bridgeUID=bridgeUID,
    )
    poller_bridgeUID = response_poller["UID"]
    uids.append(poller_bridgeUID)

    # Create the data thing
    response_data = add_sma_data(
        label=inverterMetadata.label,
        channelID=inverterMetadata.channel,
        valueType=inverterMetadata.valueType,
        poller_bridgeUID=poller_bridgeUID,
    )

    data_uid = response_data["UID"]
    uids.append(data_uid)

    # Create the item
    # label_item = f"{label}_Value_as_Number"
    response_item = add_sma_item(label=label, channelID=channelID)
    item_name = response_item["name"]

    add_sma_item_link(dataID=data_uid, itemName=item_name, channelUID=data_uid)

    # reverse the list of UIDs
    uids.reverse()

    return uids


# Delete the SMA channels
def delete_sma_channel(uids: str):
    # iterate over the UID and delete the things
    for uid in uids:
        response = openhab_delete(type="thing", uid=uid)


# Returns False if not exists or the thing object if exists
def exists_sma_inverter():
    result = False
    response = openhab_get("thing")
    response_json = response.json()

    for thing in response_json:
        if thing["thingTypeUID"] == "modbus:tcp":
            return thing

    return result


def build_sma_modbus_bridge(name: str = "SMA Modbus bridge"):
    myuuid = os.urandom(5).hex()

    ip = config["SMA_INVERTER_IP"]
    port = config["SMA_INVERTER_PORT"]
    id = config["SMA_INVERTER_ID"]
    location = config["SMA_INVERTER_LOCATION"]

    data = {
        "UID": f"modbus:modbus:{myuuid}",
        "label": name,
        "configuration": {"host": ip, "id": id, "port": port},
        "channels": [],
        "thingTypeUID": "modbus:tcp",
        "ID": myuuid,
        "location": location,
    }

    return data


def add_sma_modbus_bridge():
    # Build the SMA Modbus Bridge thing
    data = build_sma_modbus_bridge()
    # Create the SMA Modbus Bridge thing
    data_response = openhab_post(type="thing", data=data)
    result = data_response.json()

    return result


# Add the SMA thing
def add_sma_inverter_thing(name: str = "SMA Modbus Bridge") -> dict:
    sma_modbus_bridge = None
    exists = exists_sma_inverter()
    uids = []

    if exists is False:
        # Create the SMA Modbus Bridge thing
        sma_modbus_bridge = add_sma_modbus_bridge()
    else:
        sma_modbus_bridge = exists

    if sma_modbus_bridge is not None:
        for thing in get_sma_things():
            # convert the thing to a SMA Tripower metadata object
            this = InverterMetadata(thing)
            # Add the SMA channel
            uids = add_sma_channel(
                uids=uids, inverterMetadata=this, bridgeUID=sma_modbus_bridge["UID"]
            )

    return uids
