#!/usr/bin/env python3

import tempest

sensor = tempest.tempest()

while True:
    
    sensor.readNextMessage()
    print(sensor.getCurrentJSON(3))