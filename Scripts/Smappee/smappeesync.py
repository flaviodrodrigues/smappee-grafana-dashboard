#!/usr/bin/python3
# Python Modules
# Source: https://struband.net/visualisierung-fuer-smappee-und-mystrom-mit-influxdbgrafana/
# Updated by Flávio Rodrigues
import re, time, urllib.request, pycurl
import datetime
import time
from influxdb import InfluxDBClient
# Configuration Smappee
ip_smappee = 'smappeeip:port80default'
pollcycle = 5 # Seconds to get from smappee and publish to influxdb
c = pycurl.Curl()
c.setopt(c.URL, 'http://'+ip_smappee+'/gateway/apipublic/logon')
c.setopt(c.HTTPHEADER, ['Content-Type: application/json'])
c.setopt(c.POSTFIELDS, 'yoursmappelocalpassword') # by default is admin
c.setopt(c.VERBOSE, False)
# Configuration Influx_DB
db = InfluxDBClient(host='127.0.0.1', port=8086, database='power')
measurement = 'Messungen'
# Log in to Smappee
c.perform()
# Main Loop
while True:
    try:
        poll = urllib.request.urlopen('http://'+ip_smappee+'/gateway/apipublic/reportInstantaneousValues')
        data = poll.read().decode('utf-8').replace('<BR>','\n').replace('\\t','')
        rd = {}
        for match in re.findall("([^=,\r\n]+)=([^' ',\r\n]+)",data):
            if match[0].strip() in rd:
                if match[0].strip()+'2' in rd:
                    rd[str(match[0].strip()+'3')] = float(match[1].strip())
                else:
                    rd[str(match[0].strip()+'2')] = float(match[1].strip())
            else:
                rd[str(match[0].strip())] = float(match[1].strip())
            try:
                rd['activeGridImportCostDia'] = 0.0
                rd['activeGridImportCostNoite'] = 0.0
                rd['activeGridImport'] = 0.0
                rd['activeGridExport'] = 0.0
				# If getting energy from grid
                if rd.get('activePower') > 0:
                    rd['activeGridImport'] = rd.get('activePower')
                    timestamp = datetime.datetime.now().time() # Throw away the date information
                    start = datetime.time(8)
                    end = datetime.time(22)
                    if (start <= timestamp <= end):
                        rd['activeGridImportCostDia'] = rd.get('activePower')
                    else:
                        rd['activeGridImportCostNoite'] = rd.get('activePower')
                else:
                    rd['activeGridExport'] = rd.get('activePower')
                if rd['activePower2'] < 0:
                    rd['activePower3'] = rd['activePower']
            except:
                pass

        # Write Dictionary to InfluxDB
        json_body = [
            {
            'measurement': measurement,
            'fields': rd
            }
        ]
        db.write_points(json_body)
    except:
        c.perform()
        continue
    time.sleep(pollcycle)
