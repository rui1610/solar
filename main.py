from libs.openhab.generic import OpenhabClient
from libs.constants.openhab import (
    ADDON_ID_KOSTAL,
    ADDON_ID_MODBUS,
    ADDON_SMA_ENERGY_METER,
)
from libs.devices.kostal.inverter import KostalInverter
from libs.devices.sma.inverter import SmaInverter
from libs.devices.sma.manager import SmaManager

# Create the Openhab client
openhab = OpenhabClient()


# Create the Kostal inverter
openhab.install_addon(ADDON_ID_KOSTAL)
kostal_inverter = KostalInverter(openhab=openhab)
kostal_inverter.add_as_thing()

# Create the SMA Manager
openhab.install_addon(ADDON_SMA_ENERGY_METER)
sma_manager = SmaManager(openhab=openhab)
sma_manager.add_as_thing()

# Create the SMA inverter
openhab.install_addon(ADDON_ID_MODBUS)
sma_inverter = SmaInverter(openhab=openhab)
sma_inverter.add_as_thing(useAll=False)
