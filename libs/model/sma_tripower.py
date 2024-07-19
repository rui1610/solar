import dataclasses
from libs.constants.sma_inverter import CHANNELS_TO_USE


@dataclasses.dataclass
class SmaChannelToUse:
    channel: int
    device: str
    name: str
    unit: str


@dataclasses.dataclass
class InverterMetadata:
    label: str
    channel: int
    valueType: str
    length: int
    objectType: str
    device: str
    name: str
    unit: str
    valueFactor: float = 1

    def __str__(self):
        return f"{self.label} ({self.channel})"

    def __repr__(self):
        return f"{self.label} ({self.channel})"

    def __hash__(self):
        return hash(str(self))

    def __init__(self, raw_data):
        channelID = int(raw_data["SMA Modbus Registeradresse"])

        this_item, self.label = getItemAndLabelName(channelID)
        self.channel = this_item.channel
        self.device = this_item.device
        self.name = this_item.name
        self.unit = this_item.unit
        self.length, self.valueType = getValueType(raw_data["SMA Modbus Datentyp"])
        self.objectType = raw_data["Objekttyp"]
        self.valueFactor = getFactor(raw_data["Schrittweite"])


def getItemAndLabelName(channelId: str):
    for item in CHANNELS_TO_USE:
        # Map the item to the dataclass
        thisItem = SmaChannelToUse(**item)
        if thisItem.channel == channelId:
            label = f"{thisItem.device} - {thisItem.name} ({channelId})"
            return thisItem, label

    return None, None


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

    # replace all , with a .
    result = result.replace(",", ".")
    result = float(result)

    return result
