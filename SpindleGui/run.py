from spindleGui import gui
from spindleGui.gui import app
import requests
import time
import math

def insertData(temp):
    dat = {
        "name": "DieSpindel01",
        "ID": 3746707,
        "token": "A1E-IZtoP8oAhbKV0SUKTCw4IjOcyfel9s",
        "angle": 46.95489,
        "temperature": temp,
        "temp_units": "C",
        "battery": 3.799102,
        "gravity": 11.4164,
        "interval": 1,
        "RSSI": -54
    }
    resp = requests.post('http://spindle-api/spindle/Doerte',
                     json=dat
                     )
    print(f'posted temp: {temp} - response{str(resp)}')

def simulateData():
    for x in range(10):
        val =float(10+ 3*(math.sin(x/0.1)))
        print(f'try to insert {val}')
        insertData(val)
        time.sleep(1)


#simulateData()
app.run_server(debug=True, host='0.0.0.0', port=80)



