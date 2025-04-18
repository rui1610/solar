from libs.devices.sma.inverter_modbus import SmaModbus

myInverter = SmaModbus()
myInverter.connect()
# myInverter.getValues()
myInverter.getAllValues()
myInverter.close()
myInverter.storeValuesInFiles()
myInverter.storeValuesInOneFile()
# for measurement in myInverter.values:
#     print(
#         f"{measurement.address} - {measurement.channel} {measurement.value} {measurement.unit}"
#     )
