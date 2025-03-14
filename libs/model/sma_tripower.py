# import dataclasses
# from libs.constants.sma_inverter import CHANNELS_TO_USE


# @dataclasses.dataclass
# class SmaChannelToUse:
#     channel: int
#     device: str
#     name: str
#     unit: str


# @dataclasses.dataclass
# class InverterMetadata:
#     label: str
#     channel: int
#     valueType: str
#     length: int
#     objectType: str
#     device: str
#     name: str
#     unit: str
#     valueFactor: float
#     location: str

#     def __str__(self):
#         return f"{self.label} ({self.channel})"

#     def __repr__(self):
#         return f"{self.label} ({self.channel})"

#     def __hash__(self):
#         return hash(str(self))

#     def __init__(self, raw_data, useAll: bool = False):
#         this_item, label = getItemAndLabelName(raw_data=raw_data, useAll=useAll)
#         if this_item is not None:
#             self.label = label
#             self.channel = this_item.channel
#             self.device = this_item.device
#             self.name = this_item.name
#             self.unit = this_item.unit
#             self.length, self.valueType = getValueType(raw_data["SMA Modbus Datentyp"])
#             self.objectType = raw_data["Objekttyp"]
#             self.valueFactor = getFactor(raw_data["Schrittweite"])
#         else:
#             self.channel = None


# def getItemAndLabelName(raw_data: str, useAll: bool = False):
#     channelId = int(raw_data["SMA Modbus Registeradresse"])
#     if useAll is False:
#         for item in CHANNELS_TO_USE:
#             # Map the item to the dataclass
#             thisItem = SmaChannelToUse(**item)

#             if int(thisItem.channel) == channelId:
#                 label = f"{thisItem.device} - {thisItem.name} ({channelId})"
#                 return thisItem, label
#     else:
#         channel = channelId
#         device = "SMA Device"
#         name = raw_data["Name (SMA Speedwire)"]
#         unit = "unkknown"
#         thisItem = SmaChannelToUse(channel=channel, device=device, name=name, unit=unit)
#         label = f"{thisItem.device} {channelId} - {thisItem.name}"
#         return thisItem, label

#     return None, None


# def getValueType(rawValue: str):
#     match rawValue:
#         case "U64":
#             return 4, "uint64"
#         case "S64":
#             return 4, "int64"
#         case "U32":
#             return 2, "uint32"
#         case "S32":
#             return 2, "int32"
#         case "U16":
#             return 1, "uint16"
#         case "S16":
#             return 1, "int16"
#     return rawValue


# def getFactor(raw_data: str):
#     result = raw_data

#     try:
#         # replace all , with a .
#         result = result.replace(",", ".")
#         result = result.replace("-", "")
#         result = float(result)
#     except Exception:
#         result = 1

#     return result
