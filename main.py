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
config = SmaManagerConfig()
sma_manager = OpenhabThing(openhab=openhab, thingConfig=config)
thing = sma_manager.createThing()

# Create the SMA inverter
openhab.install_addon(ADDON_ID_MODBUS)
config = SmaInverterModbusBridge()
sma_inverter_brigde = OpenhabThing(openhab=openhab, thingConfig=config)
thing = sma_inverter_brigde.createThing()


exit()

# Create the Kostal inverter
openhab.install_addon(ADDON_ID_KOSTAL)
kostal_inverter = KostalInverter(openhab=openhab)
kostal_inverter.add_as_thing()
