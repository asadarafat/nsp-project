import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

import socket
import time


host = socket.gethostname() 
print(host)

bucket = "nsp-bucket"
org="nsp-org"
token="Rt_B7M0P40LXvqs1OgrAeng5yxWUXvI2m9q3FhobdzEwi6W0Vf9VaK2MLON9l5RsrqfKPQHDQ6xBfPozy1TW_Q=="

client = influxdb_client.InfluxDBClient(url="http://10.58.23.122:8086", token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

p = influxdb_client.Point("my_measurement").tag("location", "Prague").field("temperature", 2.0)
write_api.write(bucket=bucket, org=org, record=p)
time.sleep(2.4)

p = influxdb_client.Point("my_measurement").tag("location", "Prague").field("temperature", 24.0)
write_api.write(bucket=bucket, org=org, record=p)
time.sleep(3.4)

p = influxdb_client.Point("my_measurement").tag("location", "Prague").field("temperature", 5.0)
write_api.write(bucket=bucket, org=org, record=p)
time.sleep(5.4)

p = influxdb_client.Point("my_measurement").tag("location", "Prague").field("temperature", 2.0)
write_api.write(bucket=bucket, org=org, record=p)
time.sleep(6.4)

p = influxdb_client.Point("my_measurement").tag("location", "Prague").field("temperature", 3.0)
write_api.write(bucket=bucket, org=org, record=p)