import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

from jsonbender import bend, S

from progressbar import ProgressBar

from datetime import datetime
import socket
import time
import json



#host = socket.gethostname() 
#print(host)

############# influxDB connection primitive
#############

bucket = "nsp-bucket"
org="nsp-org"
token="Rt_B7M0P40LXvqs1OgrAeng5yxWUXvI2m9q3FhobdzEwi6W0Vf9VaK2MLON9l5RsrqfKPQHDQ6xBfPozy1TW_Q=="

client = influxdb_client.InfluxDBClient(url="http://10.58.23.122:8086", token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

# p = influxdb_client.Point("my_measurement").tag("location", "Prague").field("temperature", 2.0)
# write_api.write(bucket=bucket, org=org, record=p)
# time.sleep(1.0)

# p = influxdb_client.Point("my_measurement").tag("location", "Prague").field("temperature", 24.0)
# write_api.write(bucket=bucket, org=org, record=p)



############# normalize data for influxDB entry
#############
json_body = [
        {
            "measurement": "cpu_load_short_1",
            "tags": {
                "host": "server01",
                "region": "us-west"
            },
            #"time": "2021-07-10T22:00:00Z",
            #"time":  "2021-07-11T08:05:30Z",
            "time": datetime.now().astimezone().replace(microsecond=0).isoformat(),
            "fields": {
                "value": 10000000.00
            }
        }
    ]
# p = influxdb_client.Point(json_body)
write_api.write(bucket=bucket, org=org, record=json_body)

# mapping_IpOptim_InfluxDB = {
#     'measurement': 'twamp-asad-asad',                                                  ## measurement/table name
#     'tags'  : S('response', 'data'),
#     'fields': S('response', 'data'),
#     }

with open("ipLinks.json", "r") as read_file:
    ipLinksData = json.load(read_file)

## initiate 
pbar = ProgressBar()
influxEntryDict = {
            "measurement": "ipLinks",
            "tags": {},
            "fields": {},
            "time": str(datetime.now().astimezone().replace(microsecond=0).isoformat())
        }
print ("Sending data to InfluxDB")
for i in pbar(ipLinksData['response']['data']):
    ## delete nested list and dict
    i['segmentsIds'] = ''
    i['bgpPeer'] = ''
    ## to debug i
    # print (json.dumps(i, indent=5))
    influxEntryDict['tags'] = i
    influxEntryDict['fields'] = i
    write_api.write(bucket=bucket, org=org, record=influxEntryDict)



# mapping_IpOptim_InfluxDB = {
#     'measurement': 'twamp-asad-asad',                                                  ## measurement/table name
#     'tags'  : influx_entry,
#     'fields': influx_entry,
#     }

#influx_entry2 = [bend(mapping_IpOptim_InfluxDB, influx_entry)]

#print (json.dumps(influx_entry2, indent=5))


# influx_entry = ipLinksData['response']['data'][0]
# del influx_entry['segmentsIds']
# print (type(influx_entry))
# print (json.dumps(influx_entry, indent=5))




#influx_entry = [bend(mapping_IpOptim_InfluxDB, ipLinksData)]

# del influx_entry[0]['tags'][0]['segmentsIds']
# print(json.dumps(influx_entry[0]['tags'][0], indent=5))

# print (type (influx_entry[0]['tags'][0]))
# for key, value in influx_entry[0]['tags'][0].items():
#     print(key, value)

#     p = influxdb_client.Point("my_measurement").tag("location", "Prague").field("temperature", 2.0)
#     write_api.write(bucket=bucket, org=org, record=p)




