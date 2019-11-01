from kafka import KafkaConsumer
from json import loads
from paho.mqtt import client

from paho.mqtt import publish as pub

consumer = KafkaConsumer(
    'fila',
     bootstrap_servers=['localhost:9092'],
     auto_offset_reset='latest',
     enable_auto_commit=True,
     group_id='my-group',
     value_deserializer=lambda v: v.decode('utf-8')
            .replace("(", "")
            .replace(")", "")
            .replace("[", "")
            .replace("]", "")
            .replace(" ", "")
     ) 

client1= client.Client("control1")                    #create client object
client1.username_pw_set("MTygNSy6zeuUTBiECYw4")               #access token from thingsboard device
client1.connect("localhost",1883,keepalive=600)

for message in consumer:
    message = message.value
    y = loads(message)
    print(y["values"])
    """  message = message.split(",")
    d = {}
    values = ( "{\"ts\": %s, \"values\":{ \"umidade maxima\": %s, \"temperatura maxima\": %s, \"temperatura minima\": %s, \"umidade minima\": %s }}" %(message[0], message[1], message[3], message[4] ,message[2]) )
    print(message)
    ret = client1.publish("v1/devices/me/telemetry", values) #topic-v1/devices/me/telemetry """