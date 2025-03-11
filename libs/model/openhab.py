import dataclasses


@dataclasses.dataclass
class ThingConfig:
    thingTypeUid: str
    thingType: str
    id: str
    uid: str
    label: str
    location: str
    configuration: dict
    channels: list
