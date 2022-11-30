var mqtt = require('mqtt')

var options = {
    host: '71f8087751ae4fc6b20ce20b4820d6e9.s2.eu.hivemq.cloud',
    port: 8883,
    protocol: 'mqtts',
    username: 'swiot',
    password: 'Mysecretpassword!'
}

// initialize the MQTT client
var client = mqtt.connect(options);

// setup the callbacks
client.on('connect', function () {
    console.log('🐝 The Backend is now connected to the HiveMQ Broker!');
});

client.on('error', function (error) {
    console.log('🚨 ' + error);
});

client.on('message', function (topic, message) {
    // called each time a message is received
    console.log('📩 ' + 'Received message:', topic, message.toString());
});

// subscribe to topic 'data/*'
var temp = client.subscribe("data/temperature")
var hum = client.subscribe("data/humidity")
// console.log(temp)
// console.log(hum)
