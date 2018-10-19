# Smappee Energy Monitor Dashboard 

Use smappee local api data to generate amazing dashboards. This is created for a one fase plus solar connected to a Smapee Energy (not solar one)


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites
Get a Smappee
Smappee Input one: Grid
Smappee Input two: Solar Panels

Install InfluxDB
```
Easy way using docker:
root@docker:~# docker run -p 8083:8083 -p 8086:8086 --restart=always --name=influxdb -v influxdb:/var/lib/influxdb influxdb:latest
```

Create a InfluxDB database
```
root@docker:~# docker exec -ti influxdb bash
root@420bb9285990:/# influx
> create database power
```

Install the Grafana
```
Easy way using docker:
root@docker:~# docker run -d -p 3000:3000 --restart=always --name=grafana -v grafana-data:/var/lib/grafana -v grafana-log:/var/log/grafana -v grafana-etc:/etc/grafana grafana/grafana:latest
```

Install the Python 3 dependencies
```
root@docker:~# pip3 install influxdb pycurl
```

### Installing

Get from smappee and send to influxdb
```
Now that you have all the tools, get from Scripts\Smappee folder the Python file (smappeesync.py) and change the variables to meet your needs.
You can also use the forever.py to run this py forever when got errors or connection lost.
```

Get the dashboards
```
Go to folder Grafana and you will find the EnergyMonitor.json file
Now go to your grafana dashboard and import it.
Dont forget to change the dashboard variables to meet your energy costs.
```

## Dashboards Example

![Dashboard](https://preview.ibb.co/cbJmzU/dashb1.png)
![Dashboard](https://preview.ibb.co/my1TDp/dashb2.png)
![Dashboard](https://preview.ibb.co/iYPC69/dashb3.png)

## Contributing

Be free to change, contribute and submit pull requests to me.

## Authors

Based on this https://struband.net/visualisierung-fuer-smappee-und-mystrom-mit-influxdbgrafana/
Updated and dashboards redesigned by Flávio Rodrigues

## License

This project is open and free to use.

