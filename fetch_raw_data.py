from libs.devices.sma.inverter_modbus import SmaModbus

myInverter = SmaModbus()
myInverter.connect()
myInverter.getValues()
myInverter.close()
for measurement in myInverter.values:
    print(
        f"{measurement.channel} - {measurement.name} = {measurement.value} {measurement.unit}"
    )
