from network import WLAN, STA_IF
from tb_device import TBClient
from service import Config, WIFIConnector
from utime import sleep


client = None
main_configurator = Config("config.json")

wifi_connection = WIFIConnector(main_configurator.wifi_config)

print(main_configurator.wifi_config)
print(main_configurator.thingsboard_config)
print(main_configurator.connectors_config)

def main():
    try:
        global client
        client = TBClient(main_configurator.thingsboard_config["thingsboard"])
        client.connect()
    except Exception as e:
        print(e)
