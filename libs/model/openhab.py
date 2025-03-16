import dataclasses


@dataclasses.dataclass
class ThingConfig:
    thingTypeUid: str
    thingType: str
    id: str
    uid: str
    label: str
    label_type: str
    location: str
    configuration_complete: dict
    configuration_for_setup: dict

    channels: list


class ItemConfig:
    name: str
    label: str
    category: str
    groupNames: list
    type: str
    tags: list
