import requests
import random
import json
import time

url = 'http://127.0.0.1:8085/api/temp'
mac = '__CORYTEST_5'
headers = {'Content-Type': 'application/json'}

temp_1 = 300
temp_2 = 330
rt = 0

for x in range(0,120):
    if x < 26:
        temp_1 += 1
        temp_2 += 2
    elif x < 51:
        temp_1 -= 1
        temp_2 -= 2
    elif x < 76:
        temp_1 += 3
        temp_2 += 5
    else:
        temp_1 -= 2
        temp_2 -= 3
    data = {'MAC': mac, 'Temp1': temp_1, 'Temp2': temp_2,
            'Volts': 5.5, 'Mode': 'Away', 'Runtime(ms)': rt}

    r = requests.post(url, data=json.dumps(data), headers=headers)
    print(r.json())
    time.sleep(5)
    rt += 30