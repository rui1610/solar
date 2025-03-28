from libs.openhab.generic import OpenhabClient
from libs.constants.openhab import (
    ADDON_ID_KOSTAL,
    ADDON_ID_MODBUS,
    ADDON_SMA_ENERGY_METER,
    ADDON_JAVASCRIPTING,
    ADDON_JAVASCRIPTING_NASHORN,
)
from libs.devices.kostal.inverter import KostalInverter
from libs.devices.sma.inverter import SmaInverterModbusBridge
from libs.devices.sma.manager import SmaManagerConfig
from libs.openhab.setup import OpenhabThing
from libs.constants.kostal_inverter import CHANNELS_TO_USE as CHANNELS_KOSTAL
from libs.constants.sma_manager import CHANNELS_TO_USE as CHANNELS_SMA_MANAGER

# Create the Openhab client
openhab = OpenhabClient()

openhab.install_addon(ADDON_JAVASCRIPTING)
openhab.install_addon(ADDON_JAVASCRIPTING_NASHORN)


# Create the SMA inverter
openhab.install_addon(ADDON_ID_MODBUS)
thing = OpenhabThing(openhab=openhab, thingConfig=SmaInverterModbusBridge())
sma_inverter_brigde = thing.createThing()
thing.createModbusItems()

# Create the Kostal inverter
openhab.install_addon(ADDON_ID_KOSTAL)
thing = OpenhabThing(openhab=openhab, thingConfig=KostalInverter())
thing.createThing()
thing.createItemsFromChannels(channelsToUse=CHANNELS_KOSTAL)


# Create the SMA Manager
openhab.install_addon(ADDON_SMA_ENERGY_METER)
thing = OpenhabThing(openhab=openhab, thingConfig=SmaManagerConfig())
sma_manager = thing.createThing()
thing.createItemsFromChannels(channelsToUse=CHANNELS_SMA_MANAGER)
# thing.createItemsFromChannels()
