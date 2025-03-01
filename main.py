# from libs.devices.kostal.inverter import add_kostal_inverter_thing
from libs.devices.kostal.inverter import KostalInverter
from libs.openhab.generic import OpenhabClient
from libs.constants.openhab import ADDON_ID_KOSTAL, ADDON_ID_MODBUS

# install_addon(ADDON_ID_MODBUS)
# install_addon(ADDON_ID_KOSTAL)

openhab = OpenhabClient()
openhab.install_addon(ADDON_ID_KOSTAL)
openhab.install_addon(ADDON_ID_MODBUS)

exit()

kostal_inverter = KostalInverter()
kostal_inverter.add_as_thing()


add_kostal_inverter_thing()
add_sma_inverter_thing(useAll=False)
