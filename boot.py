from tb_client import TBClient
from service import Config, WIFIConnector
from machine import Pin, unique_id, deepsleep, reset

led = Pin(4, Pin.OUT)

client = None
main_configurator = Config("config.json")
camera_flashlight = False

wifi_connection = WIFIConnector(main_configurator.wifi_config)

print(main_configurator.wifi_config)
print(main_configurator.thingsboard_config)
print(main_configurator.connectors_config)


def main():
    try:
        global client
        client = TBClient(main_configurator.thingsboard_config)
        client.connect()
    except Exception as e:
        print(e)

wifi_connection.connect()
main()