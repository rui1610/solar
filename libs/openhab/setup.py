import dataclasses
from libs.openhab.generic import OpenhabClient, 

@dataclasses.dataclass
class OpenhabThing:
    openhab: OpenhabClient
    thingType: str
    thingTypeUid: str

    def __init__(self, openhab: OpenhabClient, thingTypeUid: str):
        self.openhab = openhab
        self.thingType = thingTypeUid
        self.thingTypeUid = thingTypeUid
    
    def exists(self):
        openhab = self.openhab
        return = openhab.object_exists(objectType="thing", checkType=self.thingTypeUid, thingType=self.thingType)
        
