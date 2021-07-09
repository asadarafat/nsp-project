
import influxdb_client

global ifluxdbIP
global influxPort
global influxUsername
global influxPassword


ifluxdbIP       = '10.58.23.111'
influxPort      = 8086
influxUsername  = 'telemetry'
influxPassword  = 'telemetry'


client = InfluxDBClient(host=ifluxdbIP, port=influxPort, username=influxUsername, password=influxPassword)
print (client)




