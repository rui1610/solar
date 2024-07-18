from libs.devices.kostal.inverter import add_kostal_inverter_thing
from libs.devices.sma.inverter import add_sma_inverter_thing
from libs.openhab.generic import delete_all_objects

delete_all_objects()

add_kostal_inverter_thing()
add_sma_inverter_thing()
