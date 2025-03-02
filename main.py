from libs.devices.kostal.inverter import KostalInverter
from libs.devices.sma.inverter import SmaInverter
from libs.openhab.generic import OpenhabClient
from libs.constants.openhab import ADDON_ID_KOSTAL, ADDON_ID_MODBUS

# Create the Openhab client
openhab = OpenhabClient()

# Install all necessary addons
openhab.install_addon(ADDON_ID_KOSTAL)
openhab.install_addon(ADDON_ID_MODBUS)

# Create the Kostal inverter
kostal_inverter = KostalInverter(openhab=openhab)
# kostal_inverter.add_as_thing()

# Create the SMA inverter
sma_inverter = SmaInverter(openhab=openhab)
# sma_inverter.add_as_thing()

openhab.delete_all_objects()
