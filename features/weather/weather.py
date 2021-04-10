import forecast as wf
import json

result = wf.forecast(place = "Santa Fe, Provincia de Santa Fe" , time="13:03:00" , date="2021-02-23" , forecast="daily")
day = result['day']
night = result['night']

result = json.dumps(test1) 
