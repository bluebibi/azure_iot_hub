import sys, os
sys.path.append(os.getcwd())
from private import *
import iothub_service_client
from iothub_service_client import IoTHubRegistryManager, IoTHubRegistryManagerAuthMethod
from iothub_service_client import IoTHubDeviceStatus, IoTHubError, IoTHubRegistryManagerResult

iothub_registry_manager = IoTHubRegistryManager(CONNECTION_STRING)
auth_method = IoTHubRegistryManagerAuthMethod.SHARED_PRIVATE_KEY

def print_device_info(iothub_device):
    print("iothubDevice.deviceId                    = {0}".format(iothub_device.deviceId))
    print("iothubDevice.primaryKey                  = {0}".format(iothub_device.primaryKey))
    print("iothubDevice.secondaryKey                = {0}".format(iothub_device.secondaryKey))
    print("iothubDevice.connectionState             = {0}".format(iothub_device.connectionState))
    print("iothubDevice.status                      = {0}".format(iothub_device.status))
    print("iothubDevice.lastActivityTime            = {0}".format(iothub_device.lastActivityTime))
    print("iothubDevice.cloudToDeviceMessageCount   = {0}".format(iothub_device.cloudToDeviceMessageCount))
    print("iothubDevice.isManaged                   = {0}".format(iothub_device.isManaged))
    print("iothubDevice.authMethod                  = {0}".format(iothub_device.authMethod))

def iothub_create_or_get_device(DEVICE_ID):
    try:
        existed_device = iothub_registry_manager.get_device(DEVICE_ID)
        if existed_device is not None:
            return existed_device
        new_device = iothub_registry_manager.create_device(DEVICE_ID, "", "", auth_method)
        return new_device
    except IoTHubError:
        new_device = iothub_registry_manager.create_device(DEVICE_ID, "", "", auth_method)
        return new_device

if __name__ == '__main__':
    DEVICE_ID = "VirtualDevice0001"

    print("Python {0}".format(sys.version) )
    print()
    print("Creating device using the Azure IoT Hub Service SDK for Python" )
    print()
    print("Connection string = {0}".format(CONNECTION_STRING) )
    print("Device ID         = {0}".format(DEVICE_ID) )
    print()

    device = iothub_create_or_get_device(DEVICE_ID)
    print_device_info(device)