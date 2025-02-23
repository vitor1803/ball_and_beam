import serial
import threading
import time

class SerialApp:
    def __init__(self, port, baudrate):
        self.serial_port = serial.Serial(port, baudrate, timeout=1)
        self.running = True

    def read_from_serial(self):
        while self.running:
            if self.serial_port.in_waiting > 0:
                data = int.from_bytes(self.serial_port.read(), byteorder='big')
                print(f"Received: {data}")
            time.sleep(0.1)

    def send_to_serial(self, value):
        if self.serial_port.is_open:
            self.serial_port.write(f"{value}\n".encode('utf-8'))
            print(f"Sent: {value}")
        else:
            print("Serial port is not open")

    def start(self):
        read_thread = threading.Thread(target=self.read_from_serial)
        read_thread.start()

        while True:
            user_input = input("Enter a number to send (or 'exit' to quit): ")
            if user_input.lower() == 'exit':
                self.running = False
                self.serial_port.close()
                break
            elif user_input.isdigit():
                self.send_to_serial(user_input)
            else:
                print("Please enter a valid number")

if __name__ == "__main__":
    port = "/dev/ttyACM0"  # Substitua pelo nome correto da porta serial
    baudrate = 9600  # Taxa de baud configurada no Arduino
    app = SerialApp(port, baudrate)
    app.start()
