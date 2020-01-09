
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import onionGpio
import time
import sys          
import time
import datetime
import json
import SDL_Pi_HDC1000

hdc1000 = SDL_Pi_HDC1000.SDL_Pi_HDC1000()
gpio0 = onionGpio.OnionGpio(2)
gpio0.setOutputDirection(0)
led_value=0
gpio0.setValue(led_value)

# A random programmatic shadow client ID.
SHADOW_CLIENT = "myShadowClient"

# The unique hostname that AWS IoT generated for 
# this device.
HOST_NAME = "aj9bkl2jv8zj-ats.iot.us-west-2.amazonaws.com"

# The relative path to the correct root CA file for AWS IoT, 
# that you have already saved onto this device.
ROOT_CA = "/root/cert/AmazonRootCA1.pem"

# The relative path to your private key file that 
# AWS IoT generated for this device, that you 
# have already saved onto this device.
PRIVATE_KEY = "/root/cert/private-key.pem.key"

# The relative path to your certificate file that 
# AWS IoT generated for this device, that you 
# have already saved onto this device.
CERT_FILE = "/root/cert/iot-cert.pem.crt"

# A programmatic shadow handler name prefix.
SHADOW_HANDLER = "test_esp32"

# Automatically called whenever the shadow is updated.
def myShadowUpdateCallback(payload, responseStatus, token):
  print()
  print('UPDATE: $aws/things/' + SHADOW_HANDLER +
    '/shadow/update/#')
  print("payload = " + payload)
  print("responseStatus = " + responseStatus)
  print("token = " + token)

# Create, configure, and connect a shadow client.
myShadowClient = AWSIoTMQTTShadowClient(SHADOW_CLIENT)
myShadowClient.configureEndpoint(HOST_NAME, 8883)
myShadowClient.configureCredentials(ROOT_CA, PRIVATE_KEY,
  CERT_FILE)
myShadowClient.configureConnectDisconnectTimeout(10)
myShadowClient.configureMQTTOperationTimeout(5)
myShadowClient.connect()

# Create a programmatic representation of the shadow.
myDeviceShadow = myShadowClient.createShadowHandlerWithName(
  SHADOW_HANDLER, True)

while True:
     led_value=1
     gpio0.setValue(led_value)
     tempp = hdc1000.readTemperature()
     humidd = hdc1000.readHumidity()
     myjson = {}
     myjson["state"] = {}
     myjson["state"]["reported"] = {}
     myjson["state"]["reported"]["temperature"]=tempp
     myjson["state"]["reported"]["humidity"]= humidd
     print(myjson)
     payloadjson=json.dumps(myjson)
     myDeviceShadow.shadowUpdate(payloadjson,myShadowUpdateCallback, 5)
     led_value=0
     gpio0.setValue(led_value)
     time.sleep(60)

