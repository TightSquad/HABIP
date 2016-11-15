import daqcs_pi_pb2 as daqcs_pi

device = daqcs_pi.Data(id=0)
device.id = 0

# Initialize the temperature sensors
tempSensor1 = device.tempSensors.add(id=0)
tempSensor2 = device.tempSensors.add(id=1)

# Add in the temperature values
tempSensor1.value = 1.125;
tempSensor2.value = -2.25;

# Initialize the pressure sensor
pressureSensor = device.pressureSensors.add(id=0)

# Add the pressure value
pressureSensor.value = 0.1875

# Serialize the data
serialized = device.SerializeToString()


# Read in serialized data
newDevice = daqcs_pi.Data()
newDevice.ParseFromString(serialized)

# ========== Unit Testing! ==========

assert device.id == newDevice.id
assert len(device.tempSensors) == len(newDevice.tempSensors)
for i in range(0,len(newDevice.tempSensors)):
	assert device.tempSensors[i].id == newDevice.tempSensors[i].id
	assert device.tempSensors[i].value == newDevice.tempSensors[i].value

assert len(device.pressureSensors) == len(newDevice.pressureSensors)
for i in range(0,len(newDevice.pressureSensors)):
	assert device.pressureSensors[i].id == newDevice.pressureSensors[i].id
	assert device.pressureSensors[i].value == newDevice.pressureSensors[i].value
