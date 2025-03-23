from libs.openhab.generic import OpenhabClient
from libs.devices.sma.inverter_tcp import SMAInverterClient
import urllib3

# Suppress only the single warning from urllib3.
urllib3.disable_warnings(category=urllib3.exceptions.InsecureRequestWarning)

# Create the Openhab client
openhab = OpenhabClient()

smaInverter = SMAInverterClient()

values = smaInverter.getValues()

smaInverter.logout()

print(values)
