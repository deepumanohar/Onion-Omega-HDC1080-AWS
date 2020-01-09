from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import onionGpio
import time
import sys          
import time
import datetime
import json
import logging
import SDL_Pi_HDC1000   
import random

hdc1000 = SDL_Pi_HDC1000.SDL_Pi_HDC1000()  # HDC1080 temperature humidity sensor library
gpio0 = onionGpio.OnionGpio(2) # activity indication using led
gpio0.setOutputDirection(0)
led_value=0
gpio0.setValue(led_value)

logging.basicConfig(filename="/root/aws_log.log",format='%(asctime)s %(message)s', filemode='w')
logger=logging.getLogger()
logger.setLevel(logging.DEBUG)

host = "aj9bkl2jv8zj-ats.iot.us-west-2.amazonaws.com"
ROOT_CA = "/root/cert/AmazonRootCA1.pem"

# The relative path to your private key file that 
# AWS IoT generated for this device, that you 
# have already saved onto this device.
PRIVATE_KEY = "/root/cert/private-key.pem.key"

# The relative path to your certificate file that 
# AWS IoT generated for this device, that you 
# have already saved onto this device.
CERT_FILE = "/root/cert/iot-cert.pem.crt"

port = 8883
clientId = "test_esp32"
topic = "topic_1"
#def customCallback(client, userdata, message):
    #print("Received a new message: ")
    #print(message.payload)
    #print("from topic: ")
    #print(message.topic)
    #print("--------------\n\n")


myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
myAWSIoTMQTTClient.configureEndpoint(host, port)
myAWSIoTMQTTClient.configureCredentials(ROOT_CA,PRIVATE_KEY,CERT_FILE)
# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
#myAWSIoTMQTTClient.subscribe("topic_1", 1, customCallback)


while True:
    led_value=1
    gpio0.setValue(led_value)
    tempp = hdc1000.readTemperature()
    humidd = hdc1000.readHumidity()
    vibe = random.randint(0,5)

    message = {}
    message['thing_name'] = clientId
    message['temperature'] = tempp
    message['humidity'] = humidd
    message['vibration'] = vibe
    messageJson = json.dumps(message)
    myAWSIoTMQTTClient.publish(topic, messageJson, 1)
    #logger.debug('failed to publish')
    led_value=0
    gpio0.setValue(led_value)
    time.sleep(60)


