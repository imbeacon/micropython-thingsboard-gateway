from mqtt_client import MQTTClient

RPC_RESPONSE_TOPIC = '/v1/devices/me/rpc/response/'.encode('UTF-8')
RPC_REQUEST_TOPIC = '/v1/devices/me/rpc/request/'.encode('UTF-8')
ATTRIBUTES_TOPIC = '/v1/devices/me/attributes'.encode('UTF-8')
ATTRIBUTES_TOPIC_REQUEST = '/v1/devices/me/attributes/request/'.encode('UTF-8')
ATTRIBUTES_TOPIC_RESPONSE = '/v1/devices/me/attributes/response/'.encode('UTF-8')
TELEMETRY_TOPIC = '/v1/devices/me/telemetry'.encode('UTF-8')

class TBTimeoutException(Exception):
    pass

class TBQoSException(Exception):
    pass


class TBClient(object):
    def __init__(self, config):
        client_id = 'Gateway'
        self.__host = config["host"]
        self.__port = config.get("port", 1883)
        self.__access_token = config["security"].get("accessToken")
        self.service_topics = [ATTRIBUTES_TOPIC, ATTRIBUTES_TOPIC_REQUEST, ATTRIBUTES_TOPIC_RESPONSE, TELEMETRY_TOPIC, RPC_RESPONSE_TOPIC, RPC_REQUEST_TOPIC]

        self._client = MQTTClient(client_id, self.__host, self.__port, self.__access_token, "", keepalive=60, ssl=False, ssl_params={})
        self._client.set_callback(self.__on_message)
        print(config)

    def connect(self, callback=None):
        print("Connecting to TB...")
        response = 0
        try:
            response = self._client.connect()
        except Exception as e:
            print(e)
        if response == 1:
            self.__on_connect()


    def disconnect(self, callback=None):
        print("Disconnecting...")
        self._client.disconnect()
        if callback is not None:
            callback(self, )

    def __on_connect(self):
        self.__subscribe_to_service_topics()
        print("Connected")

    def __on_message(self, topic, data):
        print("topic\t", topic)
        print("data\t", data)

    def __subscribe_to_service_topics(self):
        for service_topic in self.service_topics:
            print("subscribing to %s topic..." % service_topic)
            self._client.subscribe(service_topic, 0)
            print("Subscribed")

    def send_telemetry(self, msg, qos=1):
        self._client.publish(TELEMETRY_TOPIC, msg, qos=qos)

if __name__ == '__main__':
    try:
        from simplejson import load
        config = None
        with open("config.json", "r") as config_file:
            config = load(config_file)
        client = TBClient(config["thingsboard"])
        client.connect()
    except Exception as e:
        print(e)