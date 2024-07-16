import dataclasses


@dataclasses.dataclass
class InverterMetadata:
    label: str
    channelID: int
    valueType: str

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
        self.valueType = raw_data["SMA Modbus Datentyp"]
