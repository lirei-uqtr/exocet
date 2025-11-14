import serial
import time
import threading
from queue import Queue

class FuelCellController:
    def __init__(self, port, baudrate=57600):
        self.port = port
        self.baudrate = baudrate
        self.serial = None
        self.is_reading = False
        self.read_thread = None
        self.buffer = ''
        self.data_queue = Queue()

    def connect(self):
        try:
            self.serial = serial.Serial(self.port, self.baudrate, timeout=1)
            print(f"Connected to {self.port} at {self.baudrate} baud.")
            self.start_reading()
        except serial.SerialException as e:
            print(f"Error connecting to {self.port}: {e}")
            exit()

    def disconnect(self):
        self.stop_reading()
        if self.serial and self.serial.is_open:
            self.serial.close()
            print("Disconnected from serial port.")

    def send_command(self, command):
        if self.serial and self.serial.is_open:
            self.serial.write(command.encode('ascii'))
        else:
            print("Serial port not connected.")

    def start_fuel_cell(self):
        self.send_command('start\r')

    def end_fuel_cell(self):
        self.send_command('end\r')

    def set_fans_auto(self):
        self.send_command('f\r')

    def set_blowers_auto(self):
        self.send_command('b\r')

    def manual_purge(self):
        self.send_command('p\r')

    def get_version(self):
        self.send_command('ver\r')

    def decrease_fan_speed_1(self):
        self.send_command('9\r')

    def increase_fan_speed_1(self):
        self.send_command('0\r')

    def decrease_fan_speed_5(self):
        self.send_command('-\r')

    def increase_fan_speed_5(self):
        self.send_command('=\r')

    def decrease_blower_intensity_3(self):
        self.send_command('[\r')

    def increase_blower_intensity_3(self):
        self.send_command(']\r')

    def _read_loop(self):
        while self.is_reading:
            try:
                if self.serial and self.serial.is_open and self.serial.in_waiting > 0:
                    raw_data = self.serial.read(self.serial.in_waiting).decode('ascii')
                    self.buffer += raw_data
                    
                    # Process complete messages from the buffer
                    while '!' in self.buffer:
                        message, self.buffer = self.buffer.split('!', 1)
                        message += '!'
                        parsed_data = self.parse_data(message)
                        if parsed_data:
                            self.data_queue.put(parsed_data)
                    
                    # Also put raw, unparsed data on the queue
                    if self.buffer.strip():
                        self.data_queue.put({"raw": self.buffer.strip()})
                        self.buffer = ''

            except Exception as e:
                print(f"Error in read loop: {e}")
            time.sleep(0.1)

    def start_reading(self):
        if not self.is_reading:
            self.is_reading = True
            self.read_thread = threading.Thread(target=self._read_loop)
            self.read_thread.daemon = True
            self.read_thread.start()

    def stop_reading(self):
        if self.is_reading:
            self.is_reading = False
            if self.read_thread:
                self.read_thread.join()

    def parse_data(self, data):
        if not data.strip():
            return None
        
        if "Command not found" in data:
            return {"error": "Command not found"}

        if "FC_V" in data:
            parsed_data = {}
            messages = data.strip().split('!')
            for message in messages:
                if not message.strip() or '|' not in message:
                    continue
                
                if message.startswith('|'):
                    message = message[1:]

                parts = message.strip().split('|')
                for part in parts:
                    part = part.strip()
                    if ':' in part:
                        key_value = part.split(':', 1)
                        if len(key_value) == 2:
                            key = key_value.strip()
                            value_str = key_value.strip()
                            
                            try:
                                value_parts = value_str.split()
                                if value_parts:
                                    # Find the first part that can be a float
                                    for i, v_part in enumerate(value_parts):
                                        try:
                                            value = float(v_part)
                                            unit = value_parts[i+1] if len(value_parts) > i+1 else ''
                                            parsed_data[key] = {"value": value, "unit": unit}
                                            break
                                        except ValueError:
                                            continue
                            except (ValueError, IndexError):
                                continue
            return parsed_data if parsed_data else None
        
        if data.strip():
             return {"raw": data.strip()}
        
        return None

def main():
    # Replace 'COMx' with your actual serial port
    # On Linux it might be '/dev/ttyUSB0' or '/dev/ttyACM0'
    # On macOS it might be '/dev/cu.usbmodemXXXX'
    port = 'COM7'
    controller = FuelCellController(port)
    controller.connect()

    while True:
        print("\n--- Fuel Cell Controller ---")
        print("1. Start Fuel Cell")
        print("2. End Fuel Cell")
        print("3. Set Fans to Auto")
        print("4. Set Blowers to Auto")
        print("5. Manual Purge")
        print("6. Get Firmware Version")
        print("7. Decrease Fan Speed by 1%")
        print("8. Increase Fan Speed by 1%")
        print("9. Decrease Fan Speed by 5%")
        print("10. Increase Fan Speed by 5%")
        print("11. Decrease Blower Intensity by 3%")
        print("12. Increase Blower Intensity by 3%")
        print("0. Exit")

        choice = input("> ")

        if choice == '1':
            controller.start_fuel_cell()
        elif choice == '2':
            controller.end_fuel_cell()
        elif choice == '3':
            controller.set_fans_auto()
        elif choice == '4':
            controller.set_blowers_auto()
        elif choice == '5':
            controller.manual_purge()
        elif choice == '6':
            controller.get_version()
        elif choice == '7':
            controller.decrease_fan_speed_1()
        elif choice == '8':
            controller.increase_fan_speed_1()
        elif choice == '9':
            controller.decrease_fan_speed_5()
        elif choice == '10':
            controller.increase_fan_speed_5()
        elif choice == '11':
            controller.decrease_blower_intensity_3()
        elif choice == '12':
            controller.increase_blower_intensity_3()
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")

    controller.disconnect()

if __name__ == "__main__":
    main()