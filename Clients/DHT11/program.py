import RPi.GPIO as GPIO
import time
import DHT11
import paho.mqtt.client as paho
from paho import mqtt

DHTPin = 11     #define the pin of DHT11

# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

# with this callback you can see if your publish was successful
def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))

# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

# using MQTT version 5 here, for 3.1.1: MQTTv311, 3.1: MQTTv31
# userdata is user defined data of any type, updated by user_data_set()
# client_id is the given name of the client
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect

# enable TLS for secure connection
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# set username and password
client.username_pw_set("swiot", "Mysecretpassword!")
# connect to HiveMQ Cloud on port 8883 (default for MQTT)
client.connect("71f8087751ae4fc6b20ce20b4820d6e9.s2.eu.hivemq.cloud", 8883, keepalive=120)

# setting callbacks, use separate functions like above for better visibility
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish


def loop():
    dht = DHT11.DHT(DHTPin)   #create a DHT class object
    counts = 0 # Measurement counts
    while(True):
        counts += 1
        print("📏 Measurement #", counts)
        for i in range(0,15):            
            chk = dht.readDHT11()     #read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
            if (chk is dht.DHTLIB_OK):      #read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
                print("✅ DHT11 is OK!")
                break
            time.sleep(0.1)
        print("💧 Humidity : %.2f, \n🌡️ Temperature : %.2f \n"%(dht.humidity,dht.temperature))
        client.publish("data/temperature", payload=dht.temperature, qos=1)
        client.publish("data/humidity", payload=dht.humidity, qos=1)
        time.sleep(10)       
        
if __name__ == '__main__':
    print ('Program is starting ... ')
    try:
        loop()
    except KeyboardInterrupt:
        GPIO.cleanup()
        print('\nExiting program...')
        exit()  

