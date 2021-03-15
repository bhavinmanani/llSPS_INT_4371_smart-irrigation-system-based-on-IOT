import time
import sys
import ibmiotf.application
import ibmiotf.device
import random
#Provide your IBM Watson Device Credentials
organization = "l0iga1"
deviceType = "rsip"
deviceId = "1001"
authMethod = "token"
authToken = "1234567890"

# Initialize GPIO

def myCommandCallback(cmd):
        print("Command received: %s" % cmd.data)
        print(type(cmd.data))
        i=cmd.data['command']
        if i=='motoron':
                print("Motor is on")
        elif i=='motoroff':
                print("Motor is off")

try:
        deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
        deviceCli = ibmiotf.device.Client(deviceOptions)#.............................................

except Exception as e:
    print("Caught exception connecting device: %s" % str(e))
    sys.exit()

# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
deviceCli.connect()

while True:
        hum=30
        #print(hum)
        temp = 50
        moi =40

        #Send Temperature & Humidity to IBM Watson
        data = {'d':{'temperature' : temp, 'humidity': hum,'soilmoisturesensor': moi}}
        #print (data)
        def myOnPublishCallback():
            print ("Published Temperature = %s C" % temp, "Humidity = %s %%" % hum, "Soil Moisture Sensor = %s Units" % moi, "to IBM Watson")
            if moi <= 5:
                print("Moisture is Low.....Motor Turned On !!!")
            if moi >=90:
                print("Moisture is High.....Motor Turned Off !!!")
        


        success = deviceCli.publishEvent("DHT11", "json", data, qos=0, on_publish=myOnPublishCallback)
        if not success:
            print("Not connected to IoTF")
        time.sleep(5)
        
        deviceCli.commandCallback = myCommandCallback

# Disconnect the device and application from the cloud
deviceCli.disconnect()
