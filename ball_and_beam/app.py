import tkinter as tk
import threading
from .interface import SerialInterface
from .saving import saving_csv
from .serial_com import SerialCommunication


class SerialApp:
    def __init__(self):
        self.serial_comm = None
        self.print_ctrl = False
        self.running = True
        self.read_thread = threading.Thread(target=self.read_from_serial)
        self.saving = saving_csv()

    def start(self):
        """Inicia a aplicação."""
        root = tk.Tk()
        self.interface = SerialInterface(root, self.connect_serial, self.send_command, self.reset_serial)
        self.refresh_ports()
        root.mainloop()

    def refresh_ports(self):
        """Atualiza a lista de portas disponíveis."""
        ports = SerialCommunication.list_ports()[::-1]
        self.interface.update_ports(ports)

    def connect_serial(self, port):
        """Conecta à porta serial."""
        try:
            self.serial_comm = SerialCommunication(port)
            self.interface.show_message("Conectado", f"Conectado à porta {port}")
        except Exception as e:
            self.interface.show_message("Erro", f"Falha ao conectar: {e}")
        else:
            self.read_thread.start()

    def reset_serial(self):
        try:
            data = self.serial_comm.read(num_of_bits=1)
        except AttributeError:
            print('serial_comm is not open')
        else:
            print(data)

    def send_command(self, command):
        """Envia o comando para o Arduino."""
        if self.serial_comm:
            try:
                value = int(command)
                self.serial_comm.send(value)
            except ValueError:
                self.interface.show_message("Erro", "Digite um número válido.")
        else:
            self.interface.show_message("Erro", "Conecte-se a uma porta serial primeiro.")

    def read_from_serial(self):
        def __format_data(t, n=10):
            return str(t[0]).ljust(n) + str(t[1]).center(n) + str(t[2]).rjust(n) + '\n'

        while self.running:
            if self.serial_comm.waiting() >= 6:
                data = self.serial_comm.read()
                self.interface.display_response(__format_data(data))
                self.saving.save_measure(*data)
