import datetime
import dataclasses

@dataclasses.dataclass
class InverterMeasurements:
    Power: float
    Status: str
    Timestamp: datetime
    EnergyActual: float
    EnergyDay: float
    
    def __init__(self, raw_data):
        self._raw_data = raw_data

        return
