import json
import csv
from kafka import KafkaConsumer
from jsonbender import bend, S
from influxdb import InfluxDBClient


global ifluxdbIP
global influxPort
global influxUsername
global influxPassword
global kafkaBroker
global MAPPING_KAFKA_INFLUXDB
global kafkaTopic

ifluxdbIP       = '10.58.82.245'
influxPort      = 8086
influxUsername  = 'telemetry'
influxPassword  = 'telemetry'
kafkaBroker     = ['10.58.82.201:9092']

MAPPING_KAFKA_INFLUXDB = {
    'measurement': 'twamp-asad-asad',                                                  ## measurement/table name
    'tags'  : S('data', 'ietf-restconf:notification', 'nsp-kpi:real_time_kpi-event'),
    'fields': S('data', 'ietf-restconf:notification', 'nsp-kpi:real_time_kpi-event'),
    'time'  : S('data', 'ietf-restconf:notification', 'eventTime'),
    }

kafkaTopic = "ns-eg-2580730d-afb0-4557-815a-d26041d56e24"

consumer = KafkaConsumer(kafkaTopic,
                          bootstrap_servers=kafkaBroker,
                          value_deserializer = lambda m: json.loads(m.decode('ascii')))

client = InfluxDBClient(host=ifluxdbIP, port=influxPort, username=influxUsername, password=influxPassword)
client.switch_database('pyexample')

def kafka2influxdb():
    for kafka_message in consumer:
        print('kafka_message_value: ')
        print(kafka_message.value)
        print(json.dumps(kafka_message.value, indent=5))
        influx_entry = [bend(MAPPING_KAFKA_INFLUXDB, kafka_message.value)]
        print('influx_entry: ')
        print(json.dumps(influx_entry, indent=5))
        client.write_points(influx_entry)

def kafka2Cvs(consumer, MAPPING_KAFKA_INFLUXDB):
    cvsFile = csv.writer(open("test.csv", "w", newline=''))
    # Write CSV Header, If you dont need that, remove this line
    cvsFile.writerow(["session-name", "metric-id", "direction", "close-time", "delay"])
    for kafka_message in consumer:
        #print('kafka_message_value: ')
        #print(kafka_message.value)
        #print(json.dumps(kafka_message.value, indent=5))
        json_entry = [bend(MAPPING_KAFKA_INFLUXDB, kafka_message.value)]
        print('json_entry: ')
        print(json.dumps(json_entry, indent=5))

        for json_entry in json_entry:
            cvsFile.writerow([json_entry["tags"]["session-name"],
                              json_entry["tags"]["metric-id"],
                              json_entry["tags"]["close-time"],
                              json_entry["tags"]["suspect"],
                              json_entry["tags"]["sample-count"],
                              json_entry["tags"]["delay"],
                              json_entry["tags"]["system-id"],
                              json_entry["tags"]["time-captured"],
                              json_entry["tags"]["time-captured-periodic"],
                              json_entry["tags"]["neId"],
                              json_entry["tags"]["kpiType"],
                              json_entry["tags"]["objectId"],
                              json_entry["tags"]["dataType"],
                              ])



def main():
    kafka2Cvs(consumer, MAPPING_KAFKA_INFLUXDB)

main()