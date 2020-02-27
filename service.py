#      Copyright 2020. ThingsBoard
#  #
#      Licensed under the Apache License, Version 2.0 (the "License");
#      you may not use this file except in compliance with the License.
#      You may obtain a copy of the License at
#  #
#          http://www.apache.org/licenses/LICENSE-2.0
#  #
#      Unless required by applicable law or agreed to in writing, software
#      distributed under the License is distributed on an "AS IS" BASIS,
#      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#      See the License for the specific language governing permissions and
#      limitations under the License.

from ujson import load, loads
from network import WLAN, STA_IF
from utime import time, sleep
import uasyncio


class Config(object):
    def __init__(self, json_config):
        if json_config is not None:
            try:
                self.__json_config = loads(json_config)
            except Exception as e:
                print(e)
                with open(json_config, "r") as config_file:
                    self.__json_config = load(config_file)
        print(self.__json_config)
        self.wifi_config = None
        self.thingsboard_config = None
        self.connectors_config = None
        self.__parse_wifi_config()
        self.__parse_thingsboard_config()
        self.__parse_connectors_config()

    def __parse_wifi_config(self):
        if self.__json_config.get("wifi") is not None:
            self.wifi_config = self.__json_config.get("wifi")

    def __parse_thingsboard_config(self):
        self.thingsboard_config = self.__json_config.get("thingsboard")

    def __parse_connectors_config(self):
        pass

class WIFIConnector(object):
    def __init__(self, wifi_settings):
        self.connection = WLAN(STA_IF)
        self.connection.active(True)
        self._networks = wifi_settings

    def connect(self):
        self.connection_thread = _thread.start_new_thread(self.__connect)

    def __connect(self):
        while True:
            try:
                if not self.connection.isconnected():
                    start_connection_time = time()
                    for network in self._networks:
                        while time() - start_connection_time < network.get("timeout", 60):
                            self.connection.connect(ssid=network["ssid"], password=network["password"])
                            if self.connection.isconnected():
                                break
                else:
                    sleep(1)
            except Exception as e:
                print(e)
