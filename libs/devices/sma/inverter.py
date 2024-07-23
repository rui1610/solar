from libs.openhab.generic import openhab_post, openhab_delete, openhab_put, openhab_get
from libs.constants.files import FILE_CONFIG_SMA_METADATA, FILE_CONFIG_SECRETS
import json
import os
import logging as log

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

    # sort the result by the ["SMA Modbus Datentyp"]
    result.sort(key=lambda x: x["SMA Modbus Datentyp"])

    return result


# Build the poller json payload
def build_modbus_poller(bridgeUID: str, inverter: InverterMetadata) -> dict:
    data = {
        "label": f"Modbus {inverter.label} - poller",
        "bridgeUID": bridgeUID,
        "configuration": {
            "start": inverter.channel,
            "length": inverter.length,
            "refresh": 5000,
            "maxTries": 3,
            "cacheMillis": 50,
            "type": "input",
        },
        "properties": {},
        "thingTypeUID": "modbus:poller",
        "location": config["SMA_INVERTER_LOCATION"],
        "channels": [],
        "statusInfo": {},
        "firmwareStatus": {},
    }

    return data


# Build the data json payload
def build_modbus_data(bridgeUID: str, inverter: InverterMetadata) -> dict:
    labelData = f"Modbus {inverter.label} - data"
    data = {
        "label": labelData,
        "bridgeUID": bridgeUID,
        "configuration": {
            "readValueType": inverter.valueType,
            "readTransform": "default",
            "writeTransform": "default",
            "readStart": str(inverter.channel),
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
def build_modbus_item(inverter: InverterMetadata) -> dict:
    item_name = (
        f"Item SMA {inverter.label} ".replace(" ", "_")
        .replace("-", "_")
        .replace("(", "")
        .replace(")", "")
        .replace("ä", "ae")
        .replace("ö", "oe")
        .replace("ü", "ue")
    )
    item_label = f"SMA {inverter.label}"

    data = {
        "category": "Energy",
        "groupNames": [],
        "label": item_label,
        "name": item_name,
        "tags": ["Point"],
        "type": "Number",
        "location": config["SMA_INVERTER_LOCATION"],
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
def add_sma_poller(inverter: InverterMetadata, bridgeUID: str) -> dict:
    # set the default length

    # Build the poller thing
    poller = build_modbus_poller(bridgeUID=bridgeUID, inverter=inverter)
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
def add_sma_item(inverter: InverterMetadata) -> dict:
    # Build the item
    item = build_modbus_item(inverter)
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
def add_sma_data(inverter: InverterMetadata, poller_bridgeUID: str) -> dict:
    # Create the data thing
    # Build the data thing
    data = build_modbus_data(
        bridgeUID=poller_bridgeUID,
        inverter=inverter,
    )
    # Create the data thing
    data_response = openhab_post(type="thing", data=data)
    response_data = data_response.json()

    return response_data


def modbus_data_exists(inverter: InverterMetadata):
    response = openhab_get("thing")
    response_json = response.json()
    for thing in response_json:
        if thing["label"] == f"Modbus {inverter.label} - data":
            return True

    return False


def modbus_poller_exists(inverter: InverterMetadata):
    response = openhab_get("thing")
    response_json = response.json()
    for thing in response_json:
        if thing["label"] == f"Modbus {inverter.label} - poller":
            return True

    return False


def modbus_item_exists(inverter: InverterMetadata):
    response = openhab_get("item")
    response_json = response.json()
    for item in response_json:
        if item["label"] == f"SMA {inverter.label}":
            return True

    return False


# Add the SMA channel
def add_sma_channel(uids: list, inverter: InverterMetadata, bridgeUID: str) -> dict:
    # Create the poller thing if not exists
    if modbus_poller_exists(inverter=inverter) is False:
        response_poller = add_sma_poller(inverter=inverter, bridgeUID=bridgeUID)
        poller_bridgeUID = response_poller["UID"]
        uids.append(poller_bridgeUID)

    # Create the data thing if not exists
    if modbus_data_exists(inverter=inverter) is False:
        response_data = add_sma_data(
            inverter=inverter,
            poller_bridgeUID=poller_bridgeUID,
        )

        data_uid = response_data["UID"]
        uids.append(data_uid)

    # Create the item if not exists
    if modbus_item_exists(inverter=inverter) is False:
        response_item = add_sma_item(inverter=inverter)
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

    data = {
        "UID": f"modbus:modbus:{myuuid}",
        "label": name,
        "configuration": {"host": ip, "id": id, "port": port},
        "channels": [],
        "thingTypeUID": "modbus:tcp",
        "ID": myuuid,
        "location": "",
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
def add_sma_inverter_thing(
    name: str = "SMA Modbus Bridge", useAll: bool = False
) -> dict:
    sma_modbus_bridge = None
    exists = exists_sma_inverter()
    uids = []

    if exists is False:
        # Create the SMA Modbus Bridge thing
        sma_modbus_bridge = add_sma_modbus_bridge()
        log.info(f"Added SMA Modbus Bridge: {sma_modbus_bridge}")
    else:
        sma_modbus_bridge = exists
        log.info(f"SMA Modbus Bridge already exists: {sma_modbus_bridge}")

    if sma_modbus_bridge is not None:
        for thing in get_sma_things():
            # convert the thing to a SMA Tripower metadata object
            this = InverterMetadata(thing, useAll=useAll)
            if this.channel is not None:
                # Add the SMA channel
                uids = add_sma_channel(
                    uids=uids, inverter=this, bridgeUID=sma_modbus_bridge["UID"]
                )
                log.info(f"Added SMA items for channel: {this.label}")

    return uids


def pollerAlreadyExists(inverterMetadata: InverterMetadata):
    # check if the poller already exists
    response_poller = openhab_get("thing")
    response_poller_json = response_poller.json()
    for poller in response_poller_json:
        if (
            poller["label"]
            == f"Poller SMA {inverterMetadata.label} ({inverterMetadata.channel})"
        ):
            # poller already exists
            return True
    return False
