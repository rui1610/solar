from libs.devices.sma.inverter import get_sma_things
from libs.model.sma_tripower import InverterMetadata
from libs.devices.sma.inverter import add_sma_channel
from libs.devices.kostal.inverter import add_kostal_inverter_thing


add_kostal_inverter_thing()
exit()


# Read-in the SMA metadata
uids = []
for thing in get_sma_things():
    # convert the thing to a SMA Tripower metadata object
    this = InverterMetadata(thing)
    # Add the SMA channel
    uids = add_sma_channel(
        uids=uids,
        label=this.label,
        channelID=this.channelID,
        valueType=this.valueType,
    )

# delete_sma_channel(uids=uids)

# data = build_modbus_data("modbus:poller:fd8a48df440c", "TEMP", "30775", "int32")
# data_response = openhab_post(type="thing", data=data)
