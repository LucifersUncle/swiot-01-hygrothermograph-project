import RPi.GPIO as GPIO
import time
import swiot_DHT as DHT
import mqtt_client

DHTPin = 11     #define the pin of DHT11

client = mqtt_client.paho.Client(client_id="", userdata=None, protocol=mqtt_client.paho.MQTTv5)
client.on_connect = mqtt_client.on_connect

# enable TLS for secure connection
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# set username and password
client.username_pw_set("swiot", "Mysecretpassword!")
# connect to HiveMQ Cloud on port 8883 (default for MQTT)
client.connect("71f8087751ae4fc6b20ce20b4820d6e9.s2.eu.hivemq.cloud", 8883)

# setting callbacks, use separate functions like above for better visibility
client.on_subscribe = mqtt_client.on_subscribe
client.on_message = mqtt_client.on_message
client.on_publish = mqtt_client.on_publish


def loop():
    dht = DHT.DHT(DHTPin)   #create a DHT class object
    counts = 0 # Measurement counts
    while(True):
        counts += 1
        print("Measurement counts: ", counts)
        for i in range(0,15):            
            chk = dht.readDHT11()     #read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
            if (chk is dht.DHTLIB_OK):      #read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
                print("DHT11, OK!")
                break
            time.sleep(0.1)
        print("Humidity : %.2f, \t Temperature : %.2f \n"%(dht.humidity,dht.temperature))
        client.publish("data/temperature", payload=dht.temperature, qos=1)
        client.publish("data/humidity", payload=dht.humidity, qos=1)
        time.sleep(5)       
        
if __name__ == '__main__':
    print ('Program is starting ... ')
    try:
        loop()
    except KeyboardInterrupt:
        GPIO.cleanup()
        exit()  

