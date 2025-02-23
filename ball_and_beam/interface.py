import tkinter as tk
from tkinter import ttk, messagebox


class SerialInterface:
    def __init__(self, master, connect_callback, send_callback, disconnect_callback):
        self.master = master
        self.master.title("Arduino Serial Communication")
        self.master.geometry("400x800")

        self.connect_callback = connect_callback
        self.send_callback = send_callback
        self.disconnect_callback = disconnect_callback
        self.messages = []

        # Cria os elementos da interface
        self.create_widgets()

    def create_widgets(self):
        # Dropdown para seleção da porta
        self.port_label = ttk.Label(self.master, text="Porta Serial:")
        self.port_label.pack(pady=5)

        self.port_combobox = ttk.Combobox(self.master, values=[], state="readonly")
        self.port_combobox.pack(pady=5)

        # Frame para os botões
        button_frame = tk.Frame(self.master)
        button_frame.pack(pady=10)

        # Botão de conexão
        self.connect_button = ttk.Button(button_frame, text="Conectar", command=self.connect_serial)
        self.connect_button.pack(side="left", padx=5)

        # Botão de desconexão
        self.connect_button = ttk.Button(button_frame, text="Read buffer", command=self.disconnect_serial)
        self.connect_button.pack(side="left", padx=5)

        # Área de envio de comandos
        self.command_entry = ttk.Entry(self.master, width=30)
        self.command_entry.pack(pady=5)

        self.send_button = ttk.Button(self.master, text="Enviar", command=self.send_command)
        self.send_button.pack(pady=10)

        # Área de resposta
        self.response_label = ttk.Label(self.master, text="Resposta do Arduino:")
        self.response_label.pack(pady=5)

        # Frame para a resposta
        output_frame = tk.Frame(self.master)
        output_frame.pack(pady=10)

        self.response_text = tk.Text(output_frame, height=30, width=40)
        self.response_text.pack(side="left", padx=5)

        # Criar a Scrollbar e associá-la ao widget Text
        scrollbar = tk.Scrollbar(output_frame, command=self.response_text.yview)
        scrollbar.pack(padx=5, side="right", fill="y")

        # Configurar o widget Text para usar a Scrollbar
        self.response_text.config(yscrollcommand=scrollbar.set)

    def update_ports(self, ports):
        """Atualiza a lista de portas no dropdown."""
        self.port_combobox['values'] = ports
        if ports:
            self.port_combobox.current(0)

    def connect_serial(self):
        """Chama a função de conexão do callback."""
        port = self.port_combobox.get()
        if port:
            self.connect_callback(port)
        else:
            messagebox.showwarning("Atenção", "Selecione uma porta serial.")

    def disconnect_serial(self):
        self.disconnect_callback()

    def send_command(self):
        """Chama a função de envio do callback."""
        command = self.command_entry.get()
        self.send_callback(command)

    def display_response(self, response):
        """Exibe a resposta recebida na interface."""
        self.response_text.insert(tk.END, response)
        self.response_text.see(tk.END)

    @staticmethod
    def show_message(title, message):
        """Exibe uma mensagem de aviso."""
        messagebox.showinfo(title, message)
