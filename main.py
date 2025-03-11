from libs.openhab.generic import OpenhabClient
from libs.constants.openhab import (
    ADDON_ID_KOSTAL,
    ADDON_ID_MODBUS,
    ADDON_SMA_ENERGY_METER,
)
from libs.devices.kostal.inverter import KostalInverter
from libs.devices.sma.inverter import SmaInverterModbusBridge
from libs.devices.sma.manager import SmaManagerConfig
from libs.openhab.setup import OpenhabThing

# Create the Openhab client
openhab = OpenhabClient()

# Create the SMA Manager
openhab.install_addon(ADDON_SMA_ENERGY_METER)
thing = OpenhabThing(openhab=openhab, thingConfig=SmaManagerConfig())
sma_manager = thing.createThing()

# Create the Kostal inverter
openhab.install_addon(ADDON_ID_KOSTAL)
thing = OpenhabThing(openhab=openhab, thingConfig=KostalInverter())
kostal_inverter = thing.createThing()

# Create the SMA inverter
openhab.install_addon(ADDON_ID_MODBUS)
thing = OpenhabThing(openhab=openhab, thingConfig=SmaInverterModbusBridge())
sma_inverter_brigde = thing.createThing()
