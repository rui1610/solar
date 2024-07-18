from libs.devices.sma.things import get_sma_things
from libs.model.sma_tripower import InverterMetadata
from libs.devices.sma.things import add_sma_channel

# Read-in the SMA metadata
uids = []
for thing in get_sma_things():
    # convert the thing to a SMA Tripower metadata object
    this = InverterMetadata(thing)
    if (
        this.valueType in ["int16", "int32", "int64", "uint16", "uint32", "uint64"]
        and this.objectType == "Messwert"
    ):
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
