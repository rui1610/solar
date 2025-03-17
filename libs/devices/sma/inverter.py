from dotenv import dotenv_values
from libs.constants.files import FILE_CONFIG_SECRETS, FILE_CONFIG_SMA_METADATA
from libs.model.openhab import ThingConfig
from libs.constants.sma_inverter import CHANNELS_TO_USE
import os
import dataclasses
import json

# https://hoerli.net/openhab-sma-wechselrichter-via-modbus-anbinden/


@dataclasses.dataclass
class SmaModbusMeasurement:
    device_name: str
    address: str
    length: int
    valueType: str
    name: str
    transformation: str
    unit: str

    def __init__(self, raw_modbusData: dict, raw_config: dict, device_info: str):
        self.address = raw_config["address"]
        self.unit = raw_config["unit"]
        self.name = raw_config["name"]
        self.transformation = raw_config.get("transformation")
        self.device_name = device_info

        for thing in raw_modbusData:
            if thing["SMA Modbus Registeradresse"] == self.address:
                # if thing["SMA Modbus Registeradresse"] in str(CHANNELS_TO_USE) and thing[
                if thing["SMA Modbus Datentyp"] in [
                    "U32",
                    "S32",
                    "U64",
                    "S64",
                    "U16",
                    "S16",
                ]:
                    self.length, self.valueType = getValueType(
                        thing["SMA Modbus Datentyp"]
                    )


@dataclasses.dataclass
class SmaInverterModbusBridge(ThingConfig):
    thingTypeUid: str
    thingType: str
    id: str
    uid: str
    label: str
    label_name: str
    label_type: str
    label_item: str
    location: str
    configuration_complete: dict
    configuration_for_setup: dict
    channels: list

    def __init__(self):
        config = dotenv_values(FILE_CONFIG_SECRETS)

        ip_address = config["SMA_INVERTER_IP"]

        modbus_port = config["SMA_INVERTER_PORT"]
        name = config["SMA_INVERTER_NAME"]
        modbus_id = config["SMA_INVERTER_ID"]
        location = config["SMA_INVERTER_LOCATION"]

        myuuid = os.urandom(5).hex()
        self.uid = f"modbus:tcp:{myuuid}"
        self.id = myuuid
        self.label_item = "Modbus Bridge"
        self.label_type = "Inverter"
        self.label_name = name
        self.label = f"{self.label_name} - {self.label_type} - {self.label_item}"
        self.configuration_complete = {
            "host": ip_address,
            "id": modbus_id,
            "port": modbus_port,
            "modbus_channel_config": get_modbus_things(),
        }
        self.configuration_for_setup = {
            "host": ip_address,
            "id": modbus_id,
            "port": modbus_port,
        }

        self.channels = []
        self.thingTypeUid = "modbus:tcp"
        self.thingType = "thingTypeUID"
        self.location = location


def get_modbus_things(useAll: bool = False) -> list[SmaModbusMeasurement]:
    allModbusData = None
    with open(FILE_CONFIG_SMA_METADATA, "r") as f:
        allModbusData = json.load(f)

    modbusMeasurements = []
    for device in CHANNELS_TO_USE:
        for measurement in device["measurements"]:
            thisMeasurement = SmaModbusMeasurement(
                raw_modbusData=allModbusData,
                raw_config=measurement,
                device_info=device["deviceName"],
            )
            modbusMeasurements.append(thisMeasurement)

    return modbusMeasurements


# def getLabelName(raw_data: str):
#     channelId = int(raw_data["SMA Modbus Registeradresse"])
#     device = "SMA Device"
#     name = raw_data["Name (SMA Speedwire)"]
#     # label = f"{device} {channelId} - {name}"
#     label = f"{channelId} - {name}"
#     return label


def getValueType(rawValue: str):
    match rawValue:
        case "U64":
            return 4, "uint64"
        case "S64":
            return 4, "int64"
        case "U32":
            return 2, "uint32"
        case "S32":
            return 2, "int32"
        case "U16":
            return 1, "uint16"
        case "S16":
            return 1, "int16"
    return rawValue


def getFactor(raw_data: str):
    result = raw_data

    try:
        # replace all , with a .
        result = result.replace(",", ".")
        result = result.replace("-", "")
        result = float(result)
    except Exception:
        result = 1

    return result


# @dataclasses.dataclass
# class SmaInverter:
#     ip_address: str
#     password: str
#     openhab: OpenhabClient
#     name: str = "Solar2"
#     port: int = 502
#     id: int = 3
#     location: str = "VorderesDach"

#     def __init__(self, openhab: OpenhabClient):
#         config = dotenv_values(FILE_CONFIG_SECRETS)

#         self.ip_address = config["SMA_INVERTER_IP"]
#         self.password = config["SMA_INVERTER_PASSWORD"]
#         self.openhab = openhab

#         port = config["SMA_INVERTER_PORT"]
#         name = config["SMA_INVERTER_NAME"]
#         id = config["SMA_INVERTER_ID"]
#         location = config["SMA_INVERTER_LOCATION"]

#         if port is not None:
#             self.port = port
#         if id is not None:
#             self.id = id
#         if name is not None:
#             self.name = name
#         if location is not None:
#             self.location = location

#     # Add the SMA thing
#     def add_as_thing(self, useAll: bool = True) -> dict:
#         openhab = self.openhab

#         sma_modbus_bridge = None
#         exists = openhab.object_exists(
#             objectType="thing",
#             checkType="thingTypeUID",
#             checkText="modbus:tcp",
#         )
#         uids = []

#         if exists is None:
#             # Create the SMA Modbus Bridge thing
#             sma_modbus_bridge = add_sma_modbus_bridge(
#                 openhab=self.openhab, sma_inverter=self
#             )
#             log.info(f"Added SMA Modbus Bridge: {sma_modbus_bridge}")
#         else:
#             sma_modbus_bridge = exists
#             log.info(f"SMA Modbus Bridge already exists: {sma_modbus_bridge}")

#         if sma_modbus_bridge is not None:
#             for thing in get_sma_things():
#                 # convert the thing to a SMA Tripower metadata object
#                 this = InverterMetadata(thing, useAll=useAll)
#                 if this.channel is not None:
#                     # Add the SMA channel
#                     uids = add_sma_channel(
#                         openhab=self.openhab,
#                         sma_inverter=self,
#                         uids=uids,
#                         inverter=this,
#                         bridgeUID=sma_modbus_bridge["UID"],
#                     )
#                     log.info(f"Added SMA items for channel: {this.label}")

#         return uids


# def get_sma_things():
#     result = []
#     data = None
#     with open(FILE_CONFIG_SMA_METADATA, "r") as f:
#         data = json.load(f)

#     for thing in data:
#         # if thing["SMA Modbus Registeradresse"] in str(CHANNELS_TO_USE) and thing[
#         if thing["SMA Modbus Datentyp"] in ["U32", "S32", "U64", "S64", "U16", "S16"]:
#             result.append(thing)

#     # sort the result by the ["SMA Modbus Datentyp"]
#     result.sort(key=lambda x: x["SMA Modbus Datentyp"])

#     return result


# # Build the poller json payload
# def build_modbus_poller(
#     bridgeUID: str,
#     inverter: InverterMetadata,
#     sma_inverter: SmaInverter,
#     pollerName: str,
# ) -> dict:
#     data = {
#         "label": pollerName,
#         "bridgeUID": bridgeUID,
#         "configuration": {
#             "start": inverter.channel,
#             "length": inverter.length,
#             "refresh": 5000,
#             "maxTries": 3,
#             "cacheMillis": 50,
#             "type": "input",
#         },
#         "properties": {},
#         "thingTypeUID": "modbus:poller",
#         "location": sma_inverter.location,
#         "channels": [],
#         "statusInfo": {},
#         "firmwareStatus": {},
#     }

#     return data


# # Build the data json payload
# def build_modbus_data(
#     bridgeUID: str, inverter: InverterMetadata, dataName: str
# ) -> dict:
#     data = {
#         "label": dataName,
#         "bridgeUID": bridgeUID,
#         "configuration": {
#             "readValueType": inverter.valueType,
#             "readTransform": "default",
#             "writeTransform": "default",
#             "readStart": str(inverter.channel),
#             "updateUnchangedValuesEveryMillis": 5000,
#             "writeMaxTries": 3,
#         },
#         "properties": {},
#         "thingTypeUID": "modbus:data",
#         "location": "",
#         "statusInfo": {},
#         "firmwareStatus": {},
#     }

#     return data


# # Build the item json payload
# def build_modbus_item(sma_inverter: SmaInverter, inverter: InverterMetadata) -> dict:
#     item_name = (
#         f"{sma_inverter.name} - {inverter.label} ".replace(" ", "_")
#         .replace("-", "_")
#         .replace("(", "")
#         .replace(")", "")
#         .replace("ä", "ae")
#         .replace("ö", "oe")
#         .replace("ü", "ue")
#     )
#     item_label = f"{sma_inverter.name} - {inverter.label}"

#     data = {
#         "category": "Energy",
#         "groupNames": [],
#         "label": item_label,
#         "name": item_name,
#         "tags": ["Point"],
#         "type": "Number",
#         "location": sma_inverter.location,
#     }

#     return data


# # Build the item json payload
# def build_modbus_item_link(channelUID: str, itemName: str) -> dict:
#     data = {
#         "channelUID": f"{channelUID}:number",
#         "configuration": {},
#         "itemName": itemName,
#     }
#     return data


# # Add the SMA poller
# def add_sma_poller(
#     openhab: OpenhabClient,
#     inverter: InverterMetadata,
#     sma_inverter: SmaInverter,
#     bridgeUID: str,
#     pollerName: str,
# ) -> dict:
#     # set the default length

#     # Build the poller thing
#     poller = build_modbus_poller(
#         bridgeUID=bridgeUID,
#         inverter=inverter,
#         sma_inverter=sma_inverter,
#         pollerName=pollerName,
#     )
#     # Create the poller thing
#     poller_response = openhab.post(type="thing", data=poller)
#     response_poller = poller_response.json()

#     return response_poller


# # Add the SMA thing
# def add_sma_thing(
#     openhab: OpenhabClient,
#     label: str,
#     channelID: str,
#     valueType: str,
#     poller_bridgeUID: str,
# ) -> dict:
#     # Build the data thing
#     data = build_modbus_data(
#         bridgeUID=poller_bridgeUID,
#         label=label,
#         start=channelID,
#         valueType=valueType,
#     )
#     # Create the data thing
#     data_response = openhab.post(type="thing", data=data)
#     response_data = data_response.json()

#     return response_data


# # Add the SMA item
# def add_sma_item(
#     openhab: OpenhabClient, inverter: InverterMetadata, sma_inverter: SmaInverter
# ) -> dict:
#     # Build the item
#     item = build_modbus_item(sma_inverter=sma_inverter, inverter=inverter)
#     # Create the item
#     item_response = openhab.put(type="item", data=item, id=item["name"])
#     response_data = item_response.json()

#     return response_data


# # Add the SMA item link
# def add_sma_item_link(
#     openhab: OpenhabClient, dataID: str, itemName: str, channelUID: str
# ) -> dict:
#     # Build the item
#     item = build_modbus_item_link(channelUID=channelUID, itemName=itemName)
#     # Create the item link
#     item_response = openhab.put(
#         type="link", data=item, id=f"{itemName}/{dataID}:number"
#     )


# # Add the SMA data thing
# def add_sma_data(
#     openhab: OpenhabClient,
#     inverter: InverterMetadata,
#     poller_bridgeUID: str,
#     dataName: str,
# ) -> dict:
#     # Create the data thing
#     # Build the data thing
#     data = build_modbus_data(
#         bridgeUID=poller_bridgeUID,
#         inverter=inverter,
#         dataName=dataName,
#     )
#     # Create the data thing
#     data_response = openhab.post(type="thing", data=data)
#     response_data = data_response.json()

#     return response_data


# # Add the SMA channel
# def add_sma_channel(
#     openhab: OpenhabClient,
#     uids: list,
#     sma_inverter: SmaInverter,
#     inverter: InverterMetadata,
#     bridgeUID: str,
# ) -> dict:
#     # Create the poller thing if not exists

#     checkTextPoller = f"{sma_inverter.name} - {inverter.label} - Modbus poller"
#     modbus_poller_exists = openhab.object_exists(
#         objectType="thing",
#         checkType="label",
#         checkText=checkTextPoller,
#     )
#     poller_bridgeUID = None

#     if modbus_poller_exists is None:
#         response_poller = add_sma_poller(
#             openhab=openhab,
#             inverter=inverter,
#             sma_inverter=sma_inverter,
#             bridgeUID=bridgeUID,
#             pollerName=checkTextPoller,
#         )
#         poller_bridgeUID = response_poller["UID"]
#         uids.append(poller_bridgeUID)
#     else:
#         poller_bridgeUID = modbus_poller_exists["UID"]

#     # Create the data thing if not exists
#     checkTextData = f"{sma_inverter.name} - {inverter.label} - Modbus data"
#     modbus_data_exists = openhab.object_exists(
#         objectType="thing",
#         checkType="label",
#         checkText=checkTextData,
#     )
#     if modbus_data_exists is None:
#         response_data = add_sma_data(
#             openhab=openhab,
#             inverter=inverter,
#             poller_bridgeUID=poller_bridgeUID,
#             dataName=checkTextData,
#         )

#         data_uid = response_data["UID"]
#         uids.append(data_uid)
#     else:
#         data_uid = modbus_data_exists["UID"]

#     # Create the item if not exists
#     modbus_item_exists = openhab.object_exists(
#         objectType="item",
#         checkType="label",
#         checkText=f"SMA {inverter.label}",
#     )
#     if modbus_item_exists is None:
#         response_item = add_sma_item(
#             openhab=openhab, inverter=inverter, sma_inverter=sma_inverter
#         )
#         item_name = response_item["name"]

#         add_sma_item_link(
#             openhab=openhab, dataID=data_uid, itemName=item_name, channelUID=data_uid
#         )

#     # reverse the list of UIDs
#     uids.reverse()

#     return uids


# # Delete the SMA channels
# def delete_sma_channel(openhab: OpenhabClient, uids: str):
#     # iterate over the UID and delete the things
#     for uid in uids:
#         response = openhab.delete(type="thing", uid=uid)


# def build_sma_modbus_bridge(sma_inverter: SmaInverter):
#     myuuid = os.urandom(5).hex()

#     ip = sma_inverter.ip_address
#     port = sma_inverter.port
#     id = sma_inverter.id
#     name = None
#     name_default = "Modbus bridge"

#     if sma_inverter.name is None:
#         name = "Modbus bridge"
#     else:
#         name = f"{sma_inverter.name} - {name_default}"

#     data = {
#         "UID": f"modbus:modbus:{myuuid}",
#         "label": name,
#         "configuration": {"host": ip, "id": id, "port": port},
#         "channels": [],
#         "thingTypeUID": "modbus:tcp",
#         "ID": myuuid,
#         "location": "",
#     }

#     return data


# def add_sma_modbus_bridge(openhab: OpenhabClient, sma_inverter: SmaInverter):
#     # Build the SMA Modbus Bridge thing
#     data = build_sma_modbus_bridge(sma_inverter)
#     # Create the SMA Modbus Bridge thing
#     data_response = openhab.post(type="thing", data=data)
#     result = data_response.json()

#     return result
