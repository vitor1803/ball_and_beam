import serial
import serial.tools.list_ports

class SerialCommunication:
    def __init__(self, port, baud_rate=9600):
        self.serial_conn = serial.Serial(port, baud_rate, timeout=1)
        self.serial_conn.read_all()

    def send(self, data):
        """Envia dados pela serial."""
        self.serial_conn.write(bytes([data]))

    def read(self, num_of_bits=6):
        """Lê dados da serial."""
        try:
            response = self.serial_conn.read(num_of_bits)
            d = int.from_bytes(response[0:2], byteorder='little', signed=True)
            r = int.from_bytes(response[2:4], byteorder='little', signed=True)
            s = int.from_bytes(response[4:6], byteorder='little', signed=True)
            return d, r, s
        except Exception as e:
            print("  =======  FALHA  =======  ")
            print(e)

    def close(self):
        """Fecha a conexão serial."""
        if self.serial_conn.is_open:
            self.serial_conn.close()

    def waiting(self):
        """Test """
        return self.serial_conn.in_waiting

    @staticmethod
    def list_ports():
        """Retorna as portas seriais disponíveis."""
        return [port.device for port in serial.tools.list_ports.comports()]
