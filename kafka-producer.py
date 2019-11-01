from kafka import KafkaProducer
import json
from time import sleep
from datetime import datetime
import lorem
import time
from Fila import FilaDePrioridade as fila
from event_generator import genPriority

prioritys = genPriority()
# Create an instance of the Kafka producer
producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: str(v).encode('utf-8'))

# Call the producer.send method with a producer-record
for priority in prioritys.getFila():
    valores = ( "{\"ts\": %s, \"umidade_maxima\": %s, \"temperatura_maxima\": %s, \"temperatura_minima\": %s, \"umidade_minima\": %s }" %(priority[0], priority[1][0], priority[1][2], priority[1][3] ,priority[1][1]) )
    print(valores)
    producer.send('fila', valores)
    time.sleep(10)