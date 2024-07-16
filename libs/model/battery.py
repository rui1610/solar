import datetime
import dataclasses

@dataclasses.dataclass
class Battery:
    Power: float
    Energy: float
    Status: str
    Timestamp: datetime
    
