from libs.devices.sma.things import get_sma_things
from libs.model.sma_tripower import InverterMetadata
from libs.devices.sma import add_sma_channel, delete_sma_channel

uids = []
# Read-in the SMA metadata
for thing in get_sma_things():
    # convert the thing to a SMA Tripower metadata object
    this = InverterMetadata(thing)
    # Add the SMA channel
    uids = add_sma_channel(
        uids=uids, label=this.label, channelID=this.channelID, valueType=this.valueType
    )

delete_sma_channel(uids=uids)

# data = build_modbus_data("modbus:poller:fd8a48df440c", "TEMP", "30775", "int32")
# data_response = openhab_post(type="thing", data=data)
