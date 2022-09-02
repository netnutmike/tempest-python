import socket
import json

class tempest:

    def __init__(self, port = 50222):
        #create default values
        self.timestamp = " "
        self.windLull = " "
        self.windAvg = " "
        self.windGust = " "
        self.windDirection = " "
        self.windSpeed = " "
        self.pressure = " "
        self.temperature = " "
        self.humidity = " "
        self.UV = " "
        self.solarRadiation = " "
        self.rainMinute = " "
        self.precipType = " "
        self.lightningAvgDistance = " "
        self.lightningCount = " "
        self.battery = " "
        self.reportInterval = " "
        self.hubSerial = " "
        self.deviceUptime = " "
        self.voltage = " "
        self.firmwareVersion = " "
        self.rssi = " "
        self.hubrssi = " "
        self.sensorStatus = " "
        self.firmwareVersion  = " "
        self.uptime  = " "
        self.radioStatVersion  = " "
        self.radioStatRebootCnt  = " "
        self.radioStati2cErrors = " "
        self.radioStatus = " "
        self.radioStatNetworkID = " "

        #setup UDP listening port
        self.UDPPort = port

        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP

        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

        # Enable broadcasting mode
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        #self.client.setblocking(0)

        self.client.bind(("", 50222))

    def newRapidWind(self, messageDict):
        self.windDirection = messageDict['ob'][2]
        self.windSpeed = messageDict['ob'][1]

    def newHubStatus(self, messageDict):
        self.firmwareVersion = messageDict['firmware_revision']
        self.uptime = messageDict['uptime']
        self.rssi = messageDict['rssi']
        self.timestamp = messageDict['timestamp']
        self.radioStatVersion = messageDict['radio_stats'][0]
        self.radioStatRebootCnt = messageDict['radio_stats'][1]
        self.radioStati2cErrors = messageDict['radio_stats'][2]
        self.radioStatus = messageDict['radio_stats'][3]
        self.radioStatNetworkID = messageDict['radio_stats'][4]

    def newDeviceStatus(self, messageDict):
        #print("In newHubStatus")
        #print(messageDict)
        #ob = messageDict['ob']
        #print(messageDict['ob'][1])
        #print(messageDict['ob'][2])
        self.hubSerial = messageDict['hub_sn']
        self.deviceUptime = messageDict['uptime']
        self.voltage = messageDict['voltage']
        self.deviceFirmwareVersion = messageDict['firmware_revision']
        self.rssi = messageDict['rssi']
        self.hubrssi = messageDict['hub_rssi']
        self.sensorStatus = messageDict['sensor_status']


    def newObsSt(self, messageDict):
        #print("In newHubStatus")
        #print(messageDict)
        #ob = messageDict['ob']
        #print(messageDict['obs'][0])
        #print(messageDict['ob'][2])
        self.timestamp = messageDict['obs'][0][0]
        self.windLull = messageDict['obs'][0][1]
        self.windAvg = messageDict['obs'][0][2]
        self.windGust = messageDict['obs'][0][3]
        self.windDirection = messageDict['obs'][0][4]
        self.pressure = messageDict['obs'][0][5]
        self.temperature = messageDict['obs'][0][6]
        self.humidity = messageDict['obs'][0][7]
        self.UV = messageDict['obs'][0][8]
        self.solarRadiation = messageDict['obs'][0][9]
        self.rainMinute = messageDict['obs'][0][10]
        self.precipType = messageDict['obs'][0][11]
        self.lightningAvgDistance = messageDict['obs'][0][12]
        self.lightningCount = messageDict['obs'][0][13]
        self.battery = messageDict['obs'][0][14]
        self.reportInterval = messageDict['obs'][0][15]
        
    def getCurrentJSON(self, indentLevel = 0):
        response = {}

        response["timestamp"] = self.timestamp
        response["windLull"] = self.windLull
        response["windAvg"] = self.windAvg
        response["windGust"] = self.windGust
        response["windDirection"] = self.windDirection
        response["windSpeed"] = self.windSpeed
        response["pressure"] = self.pressure
        response["temperature"] = self.temperature
        response["humidity"] = self.humidity
        response["UV"] = self.UV
        response["solarRadiation"] = self.solarRadiation
        response["rainMinute"] = self.rainMinute
        response["precipType"] = self.precipType
        response["lightningAvgDistance"] = self.lightningAvgDistance
        response["lightningCount"] = self.lightningCount
        response["battery"] = self.battery
        response["reportingInterval"] = self.reportInterval
        response["hubSerial"] = self.hubSerial
        response["deviceUptime"] = self.deviceUptime
        response["voltage"] = self.voltage
        response["deviceFirmwareVersion"] = self.firmwareVersion
        response["rssi"] = self.rssi
        response['hubrssi'] = self.hubrssi
        response["sensorStatus"] = self.sensorStatus
        response["firmwareVersion"] = self.firmwareVersion
        response["uptime"] = self.uptime
        response["radioStatVersion"] = self.radioStatVersion
        response["radioStatRebootCnt"] = self.radioStatRebootCnt
        response["radioStati2cErrors"] = self.radioStati2cErrors
        response["radioStatus"] = self.radioStatus
        response["radioStatNetworkID"] = self.radioStatNetworkID

        if (indentLevel == 0):
            response_json = json.dumps(response)
        else:
            response_json = json.dumps(response, indent=indentLevel)

        return response_json


    def newMessage(self, messageText, addr):
        #print("received message: %s" % messageText)
        messageDict = json.loads(messageText)

        if (messageDict["type"] == 'rapid_wind'):
            self.newRapidWind(messageDict)
            return

        if (messageDict["type"] == 'hub_status'):
            self.newHubStatus(messageDict)
            return

        if (messageDict["type"] == 'device_status'):
            self.newDeviceStatus(messageDict)
            return

        if (messageDict["type"] == 'obs_st'):
            self.newObsSt(messageDict)
            return

        print(messageDict)
        print(messageDict["type"])
        print("")

    def readNextMessage(self):
        data, addr = self.client.recvfrom(1024)
        self.newMessage(data, addr)
        
    