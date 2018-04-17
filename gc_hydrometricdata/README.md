GC_HydrometricData
==================
This project intend to provide an interface that can be used to extract the
data from the web site [https://eau.ec.gc.ca/](https://eau.ec.gc.ca/).
 
 Run with
 --------
 * python 2.7
 * python 3.4
 * python 3.6
 
 Dependency
 ----------
* [requests](https://pypi.python.org/pypi/requests)
* [Beautiful Soup](https://pypi.python.org/pypi/beautifulsoup4)

Usage
-----
The main interface is `HydrometricDataInterface` located in `HydrometricData.py`

```Python
from HydrometricData import HydrometricDataInterface
webStation = HydrometricDataInterface()

# getting station for the Quebec Province
webStation.getStationsForProvince('Quebec')

stationName = "01BF004"

# getting station info
print(webStation.getStationInfo(stationName))

# getting station coordinates 
print(webStation.getStationCoordinates(stationName))

# getting station data

webStation.getHistoricalStation(stationName).getData()
print(webStation.getHistoricalStation(stationName).data)
```
 

