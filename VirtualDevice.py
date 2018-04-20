import sys, os
sys.path.append(os.getcwd())
from private import *

import random
import time
import sys
import iothub_client
from iothub_client import IoTHubClient, IoTHubClientError, IoTHubTransportProvider, IoTHubClientResult
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError, DeviceMethodReturnValue

PROTOCOL = IoTHubTransportProvider.MQTT
MESSAGE_TIMEOUT = 10000
AVG_WIND_SPEED = 10.0
SEND_CALLBACKS = 0
MSG_TXT = '{"deviceId": "VirtualDevice0001", "windSpeed": %.2f}'

def send_confirmation_callback(message, result, user_context):
    global SEND_CALLBACKS
    print("Confirmation[%d] received for message with result = %s" % (user_context, result))
    print("\tmessage_id: %s" % message.message_id)
    print("\tcorrelation_id: %s" % message.correlation_id)
    map_properties = message.properties()
    key_value_pair = map_properties.get_internals()
    print("\tProperties: %s" % key_value_pair)
    SEND_CALLBACKS += 1
    print("\tTotal calls confirmed: %d" % SEND_CALLBACKS)

def iothub_client_init():
    # prepare iothub client
    client = IoTHubClient(DEVICE_CONNECTION_STRING, PROTOCOL)
    # set the time until a message times out
    client.set_option("messageTimeout", MESSAGE_TIMEOUT)
    client.set_option("logtrace", 0)
    client.set_option("product_info", "KOREATECH_Virtual_Python")
    return client

def iothub_client_telemetry_sample_run():
    try:
        client = iothub_client_init()
        print("IoT Hub device sending periodic messages, press Ctrl-C to exit\n")
        message_counter = 0

        while True:
            msg_txt_formatted = MSG_TXT % (AVG_WIND_SPEED + (random.random() * 4 + 2))
            # messages can be encoded as string or bytearray
            if (message_counter % 2) == 1:
                message = IoTHubMessage(bytearray(msg_txt_formatted, 'utf8'))
                prop_text = "bytearray_%d" % message_counter
            else:
                message = IoTHubMessage(msg_txt_formatted)
                prop_text = "string_%d" % message_counter
            # optional: assign ids
            message.message_id = "message_%d" % message_counter
            message.correlation_id = "correlation_%d" % message_counter
            # optional: assign properties
            prop_map = message.properties()
            prop_map.add("Property", prop_text)

            client.send_event_async(message, send_confirmation_callback, message_counter)
            print("IoTHubClient.send_event_async accepted message [%d] for transmission to IoT Hub." % message_counter)
            status = client.get_send_status()
            print("Send status: %s" % status)

            time.sleep(10)

            status = client.get_send_status()
            print("Send status: %s" % status)

            message_counter += 1
            print()
    except IoTHubError as iothub_error:
        print("Unexpected error %s from IoTHub" % iothub_error)
        return
    except KeyboardInterrupt:
        print("IoTHubClient sample stopped")

if __name__ == '__main__':
    print("Simulating a device using the Azure IoT Hub Device SDK for Python")
    print("\tProtocol %s" % PROTOCOL)
    print("\tConnection string=%s" % DEVICE_CONNECTION_STRING)

    iothub_client_telemetry_sample_run()