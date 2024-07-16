from libs.openhab.generic import openhab_get

import json

# from libs.openhab.things import add_sma_channel, delete_sma_channel
# from libs.openhab.generic import get_sma_things

# from libs.openhab.things import build_modbus_data, openhab_post

response = openhab_get(type="item")

result = response.text

# remove all items not containing "SMA" as a label
result = json.loads(result)
result = [x for x in result if "SMA" in x["label"]]
result = json.dumps(result, indent=4)

print(result)

# smaThings = get_sma_things()
# uids = []
# for thing in smaThings:
#     label = thing["label"]
#     id = thing["channelID"]
#     type = thing["valueType"]

#     uids = add_sma_channel(uids=uids, label=label, channelID=id, valueType=type)
#     delete_sma_channel(uids=uids)


# data = build_modbus_data("modbus:poller:fd8a48df440c", "TEMP", "30775", "int32")
# data_response = openhab_post(type="thing", data=data)
