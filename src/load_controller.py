import pybk8500
import serial
import time

# Per the pybk8500 documentation, there is no high-level BK8500 class.
# Interaction is done by sending command objects over a serial port.

# --- Connection Settings ---
SERIAL_PORT = 'COM9'
BAUD_RATE = 9600 # Trying a common default baud rate
TIMEOUT = 1 # seconds

ser = None
try:
    # --- Setup Connection ---
    # Per the manual, DTR and RTS must be enabled.
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT)
    ser.rts = True
    ser.dtr = True
    print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud.")
    time.sleep(0.1) # Short delay for device to initialize

    parser = pybk8500.Parser()

    def send_and_parse(command):
        """Sends a command and waits for and parses the 26-byte response."""
        ser.write(bytes(command))
        time.sleep(0.2) # Add delay to allow device to process
        response_bytes = ser.read(26)
        if len(response_bytes) < 26:
            print(f"Warning: Received incomplete response ({len(response_bytes)} bytes).")
            return None, None
        msg, error, _ = parser.parse_msg(response_bytes)
        return msg, error

    # --- Configure the Load ---

    # Put device in remote mode
    print("Setting remote control ON...")
    send_and_parse(pybk8500.RemoteOn())

    # Set remote sense
    # Note: The original code had `load.remote_sense = True`.
    # The command is SetRemoteSensingState, value=1 for ON.
    print("Setting remote sense ON...")
    send_and_parse(pybk8500.SetRemoteSensingState(value=1))

    # Set function to Constant Current (CC)
    print("Setting mode to CC...")
    send_and_parse(pybk8500.SetMode(value='CC'))

    # Set current to 10 Amps
    current_to_set = 10.0
    print(f"Setting CC current to {current_to_set} A...")
    send_and_parse(pybk8500.SetCCModeCurrent(value=current_to_set))

    # --- Run the Load ---

    # Turn the load on
    print("Turning load ON...")
    send_and_parse(pybk8500.LoadOn())

    # Let it run for a moment
    time.sleep(2)

    # --- Read Measurements ---
    print("Reading input voltage and current...")
    msg, error = send_and_parse(pybk8500.ReadInputVoltageCurrentPowerState())

    if error:
        print(f"Error parsing response: {error}")
    elif msg:
        # The field names 'voltage' and 'current' are educated guesses based on the
        # library's structure. If this doesn't work, the fields of the
        # message object should be inspected (e.g., print(msg.fields())).
        voltage = msg.fields().get('voltage', 'N/A')
        current = msg.fields().get('current', 'N/A')
        print(f"  Voltage: {voltage} V")
        print(f"  Current: {current} A")
    else:
        print("  No message received from device.")


except serial.SerialException as e:
    print(f"Error opening or using serial port {SERIAL_PORT}: {e}")

finally:
    # --- Shutdown ---
    if ser and ser.is_open:
        print("Turning load OFF...")
        send_and_parse(pybk8500.LoadOff())

        print("Setting remote control OFF...")
        send_and_parse(pybk8500.RemoteOff())

        ser.close()
        print("Serial port closed.")
