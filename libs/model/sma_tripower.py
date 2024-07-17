import dataclasses


@dataclasses.dataclass
class InverterMetadata:
    label: str
    channelID: int
    valueType: str
    objectType: str

    def __str__(self):
        return f"{self.label} ({self.channelID})"

    def __repr__(self):
        return f"{self.label} ({self.channelID})"

    def __hash__(self):
        return hash(str(self))

    def __init__(self, raw_data):
        self.label = raw_data["Name (SMA Speedwire)"]
        if self.label == "-":
            self.label = raw_data["Kanal"]
        self.channelID = int(raw_data["SMA Modbus Registeradresse"])
        valueType = raw_data["SMA Modbus Datentyp"]

        self.valueType = valueType

        match valueType:
            case "U64":
                self.valueType = "uint64"
            case "S64":
                self.valueType = "int64"
            case "U32":
                self.valueType = "uint32"
            case "S32":
                self.valueType = "int32"
            case "U16":
                self.valueType = "uint16"
            case "S16":
                self.valueType = "int16"

        self.objectType = raw_data["Objekttyp"]
