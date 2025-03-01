from libs.devices.kostal.inverter import add_kostal_inverter_thing
from libs.devices.sma.inverter import add_sma_inverter_thing


# install_addon(ADDON_ID_MODBUS)
# install_addon(ADDON_ID_KOSTAL)

add_kostal_inverter_thing()
add_sma_inverter_thing(useAll=False)
