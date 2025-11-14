import pybk8500

# Create a new BK8500 object
load = pybk8500.BK8500('COM6')

# Put device in remote mode
load.remote_sense = True
load.remote_control = True


load.function = 'CC'
load.current = 10
load.load_on = True

print("Voltage:", load.voltage)
print("Current:", load.current)

load.load_on = False
load.remote_control = False
