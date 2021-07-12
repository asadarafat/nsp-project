import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

from jsonbender import bend, S


import socket
import time
import json


host = socket.gethostname() 
print(host)

bucket = "nsp-bucket"
org="nsp-org"
token="Rt_B7M0P40LXvqs1OgrAeng5yxWUXvI2m9q3FhobdzEwi6W0Vf9VaK2MLON9l5RsrqfKPQHDQ6xBfPozy1TW_Q=="

client = influxdb_client.InfluxDBClient(url="http://10.58.23.122:8086", token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

p = influxdb_client.Point("my_measurement").tag("location", "Prague").field("temperature", 2.0)
write_api.write(bucket=bucket, org=org, record=p)
time.sleep(1.0)

p = influxdb_client.Point("my_measurement").tag("location", "Prague").field("temperature", 24.0)
write_api.write(bucket=bucket, org=org, record=p)


with open("ipLinks.json", "r") as read_file:
    data = json.load(read_file)

