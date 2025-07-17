import tkinter as tk
import ttkbootstrap as ttk
from ModbusRTU import ModbusRTU_Commands  # Importar los comandos Modbus
from tkinter import messagebox
import json
import time
import serial.tools.list_ports

MAX_DEVICES = 5
class HMI(ttk.Window):
    def __init__(self,on_execute_callback):
        #super().__init__(themename="darkly")
        super().__init__()
        self.title("HMI - Interfaz de Control")
        self.geometry("640x480")
        
        # Asegúrate de que handle_modbus_result existe
        print("****************\nHMI INICIALIZADO\n****************")
        # Centrar la ventana en la pantalla
        self.center_window()
        self.on_execute_callback = on_execute_callback
        # Diccionario de páginas
        self.frames = {}

        # Contenedor de páginas
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)
        

        # Inicializar las páginas y pasar el callback a ModbusPage
        for F in (InicioPage, ConfigPage, ModbusPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(InicioPage)

        #Guardar la referencia de la página de Modbus
        self.modbus_page = self.frames[ModbusPage]
        # Menú de navegación
        self.navbar = ttk.Frame(self, bootstyle="dark")
        self.navbar.pack(side="bottom", fill="x")

        ttk.Button(self.navbar, text="🏠 Inicio", command=lambda: self.show_frame(InicioPage)).pack(side="left", padx=10, pady=5)
        ttk.Button(self.navbar, text="⚙️ Configuración", command=lambda: self.show_frame(ConfigPage)).pack(side="left", padx=10, pady=5)
        ttk.Button(self.navbar, text="📡 Modbus", command=lambda: self.show_frame(ModbusPage)).pack(side="left", padx=10, pady=5)

    def show_frame(self, page):
        """Cambia de página"""
        frame = self.frames[page]
        frame.tkraise()
    
    
    def center_window(self):
        """Centrar la ventana en la pantalla"""
        # Obtener las dimensiones de la pantalla
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
   
        # Obtener las dimensiones de la ventana
        window_width = 680  # Ancho de la ventana
        window_height = 480  # Alto de la ventana

        # Calcular la posición para centrar la ventana
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)

        # Establecer la geometría (posición + tamaño de la ventana)
        self.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')     
 
    # Método para obtener los valores de ModbusPage desde el main
    def get_modbus_values(self):
        return self.modbus_page.get_values()

# 🔹 Página de Inicio
class InicioPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        #Título (fila 0)
        ttk.Label(self, text="🏠 Página de Inicio", font=("Arial", 18)).grid(row = 0, column=0, columnspan=2,pady=10)
        #Subtítulo (fila 1)
        ttk.Label(self, text="Bienvenido a la interfaz Raspberry-Modbus", font=("Arial", 14)).grid(row=1,column=0,columnspan=2,pady=5)
     
        # Obtener puertos disponibles
        puertos = [p.device for p in serial.tools.list_ports.comports()]

        ttk.Label(self, text=f"🔧 Puertos disponibles: ",font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5, sticky="w")
      
        # Combobox con los puertos activos
        self.combobox_puertos = ttk.Combobox(self, values=puertos, state="readonly", width=30)
        self.combobox_puertos.grid(row=2, column=1, padx=10, pady=5)
        if puertos:
            self.combobox_puertos.current(0)  # Selecciona el primero por defecto

        style = ttk.Style()
        style.configure("BotonRojo.TButton", background="red")
        style.configure("BotonVerde.TButton", background="green")
        # Botón de conexión (opcional)
        ttk.Button(self, text="Conectar",style="BotonVerde.TButton",command=self.conectar_puerto).grid(row=2, column=3, pady=10)
        # Botón de desconexión
        ttk.Button(self, text="Desconectar",style="BotonRojo.TButton", command=self.desconectar_puerto).grid(row=2, column=4, padx=5, pady=10)
      
        #Texto para mostrar que se está conectando/desconectando
        self.result_label = ttk.Label(self, text="")
        self.result_label.grid(row=4, column=0, columnspan=2, pady=10)

     
    def conectar_puerto(self):
        puerto = self.combobox_puertos.get()
        if puerto:
            self.result_label.config(text=f"Intentando conectar a {puerto}...")
            
    def desconectar_puerto(self):
        puerto = self.combobox_puertos.get()
        if puerto:
             self.result_label.config(text=f"Intentando desconectar de {puerto}...")

# 🔹 Página de Configuración
class ConfigPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
       # Limpiar la ventana
        self.device_address = []
        self.device_name = []
     # Título de la página de configuración
        ttk.Label(self, text="⚙️ Configuración del Sistema", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=20)

        # Dirección del dispositivo (columna 1)
        ttk.Label(self, text="📍 Dirección del dispositivo").grid(row=1, column=1, pady=5, sticky="w", padx=10)

        # Nombre del dispositivo (columna 2)
        ttk.Label(self, text="🖥️ Nombre del dispositivo").grid(row=1, column=3, pady=5, sticky="w", padx=10)

        for i in range(1,MAX_DEVICES+1):
            # Dirección dispositivos
            ttk.Label(self, text=f"🔧 Dirección disp. {i}:").grid(row=1+i, column=0, pady=5, sticky="w", padx=10)
            self.combox_1 = ttk.Combobox(self, values=[i for i in range(20)])
            self.combox_1.grid(row=1+i, column=1, pady=5, sticky="e", padx=10)
            self.device_address.append(self.combox_1)

            # Nombre dispositivos 
            ttk.Label(self, text=f"🔧 Nombre disp. {i}:").grid(row=1+i, column=2, pady=5, sticky="w", padx=10)
            self.combox_2 = ttk.Combobox(self, values=["Waveshare 8CH DI/DO", "Waveshare 8CH AO", "Waveshare 8CH DO"])
            self.combox_2.grid(row=1+i, column=3, pady=5, sticky="e", padx=10)
            self.device_name.append(self.combox_2)

        # Botón para guardar la configuración
        self.save_button = ttk.Button(self, text="Guardar Configuración", command=self.save_config, bootstyle="primary")
        self.save_button.grid(row=10, column=1, columnspan=3, pady=10,padx=10,sticky="nsew")
        
    
        # Cargar la configuración guardada si existe
        self.load_config()

        
    def save_config(self):
        """Guardar la configuración del dispositivo en un archivo JSON"""
        device_address_array = [combobox.get() for combobox in self.device_address if combobox.get()]
        device_name_array = [combobox.get() for combobox in self.device_name if combobox.get()]

        #Crear un diccionario con los valores de configuración
        config_data = {
            "device_address": device_address_array,
            "device_name": device_name_array           
        }
        
        print(config_data)
        # Guardar los datos en un archivo JSON
        try:
            with open("config.json", "w") as json_file:
                json.dump(config_data, json_file, indent=4)
            messagebox.showinfo("Configuración guardada", "La configuración del dispositivo se ha guardado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la configuración: {str(e)}")

    def load_config(self):
        """Cargar la configuración desde el archivo JSON"""
        try:
            with open("config.json", "r") as json_file:
                config_data = json.load(json_file)
                device_address = config_data.get("device_address", [])
                device_name = config_data.get("device_name", [])

                # Asignar los valores cargados a los combobox
                for i in range(len(device_address)):
                    if i < len(self.device_address):
                        self.device_address[i].set(device_address[i])

                for i in range(len(device_name)):
                    if i < len(self.device_name):
                        self.device_name[i].set(device_name[i])

        except FileNotFoundError:
            print("El archivo de configuración no existe. No se puede cargar.")
        except json.JSONDecodeError:
            print("Error al leer el archivo de configuración.")
            
class ModbusPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.hola = None  # Inicializamos la variable `hola`
        self.data_send = None  # Inicializamos `data_send`, debe ser un widget de tkinter (ej. Label)
        # Variables de control 
        self.device_address_var = tk.StringVar()  # Dirección Modbus
        self.command_var = tk.StringVar()  # Comando seleccionado
        self.baudrate_var = tk.StringVar()  # Baudrate
        self.parity_var = tk.StringVar()  # Paridad

        #Asignar valor por defecto para que cada vez que abra la página aparezcan estos
        self.device_address_var.set("1")
        self.command_var.set("READ COILS")
        self.baudrate_var.set("9600")
        self.parity_var.set("NONE")
        
        # Crear widgets de la página
        self.create_widgets()

    def create_widgets(self):
        # Título de la página
        ttk.Label(self, text="📡 Control Modbus", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        # Selección de comando
        ttk.Label(self, text="🔧 Selecciona un comando:").grid(row=1, column=0, pady=5, sticky="e")
        self.command_menu = ttk.Combobox(self, textvariable=self.command_var, values=list(ModbusRTU_Commands.COMMANDS.keys()))
        self.command_menu.grid(row=1, column=1, pady=5)
        self.command_menu.bind("<<ComboboxSelected>>", self.check_command)

        # Campo de dirección del dispositivo
        ttk.Label(self, text="📍 Dirección del dispositivo:").grid(row=2, column=0, pady=5, sticky="e")
        self.device_address_entry = ttk.Entry(self, textvariable=self.device_address_var)
        self.device_address_entry.grid(row=2, column=1, pady=5)

        # Botón de ejecución
        self.execute_button = ttk.Button(self, text="Ejecutar", command=self.execute_and_store)
        self.execute_button.grid(row=3, column=1, pady=10, sticky="e")

        # Etiqueta para mostrar resultado
        self.result_label = ttk.Label(self, text="")
        self.result_label.grid(row=4, column=0, columnspan=2, pady=10)

        # Etiqueta para mostrar datos que enviamos (cmd send)
        self.data_send = ttk.Label(self, text="Esperando datos...")
        self.data_send.grid(row=5, column=0, columnspan=2, pady=10)
  
        
        # Etiqueta para mostrar datos que recibimos (cmd received)
        self.data_receive = ttk.Label(self, text="")
        self.data_receive.grid(row=6, column=0, columnspan=2, pady=10)
        
        # Campos de baudrate y paridad (se mostrarán solo si comando = 9)
        self.baudrate_label = ttk.Label(self, text="⏳ Selecciona Baudrate:")
        self.baudrate_menu = ttk.Combobox(self, textvariable=self.baudrate_var)

        self.parity_label = ttk.Label(self, text="🔢 Selecciona Paridad:")
        self.parity_menu = ttk.Combobox(self, textvariable=self.parity_var)

    def check_command(self, event=None):
        """Muestra la selección de baudrate y paridad si el comando es 9"""
        selected_command = self.command_var.get()
        command_code = ModbusRTU_Commands.COMMANDS.get(selected_command, None)

        if command_code == 9:
            baud_options = ModbusRTU_Commands.get_baudrate_options()
            self.baudrate_menu['values'] = baud_options

            parity_options = ModbusRTU_Commands.get_parity_options()
            self.parity_menu['values'] = parity_options

            self.baudrate_label.grid(row=1, column=2, padx=5, pady=5, sticky="e")
            self.baudrate_menu.grid(row=1, column=3, padx=5, pady=5)

            self.parity_label.grid(row=2, column=2, padx=5, pady=5, sticky="e")
            self.parity_menu.grid(row=2, column=3, padx=5, pady=5)
        else:
            self.baudrate_label.grid_forget()
            self.baudrate_menu.grid_forget()
            self.parity_label.grid_forget()
            self.parity_menu.grid_forget()

    def execute_command(self):
        """Ejecuta un comando Modbus"""
        selected_command = self.command_var.get()
        device_address = self.device_address_var.get()

        if not selected_command and not device_address.isdigit():
            self.result_label.config(text="⚠️ Error: Selecciona un comando y una dirección válida", foreground="red")
            return None, None, None, None
        if not selected_command:
            self.result_label.config(text="⚠️ Error: Selecciona un comando válido", foreground="red")
            return None, None, None, None
        if not device_address.isdigit():
            self.result_label.config(text="⚠️ Error: Selecciona una dirección válida", foreground="red")
            return None, None, None, None

        command_code = ModbusRTU_Commands.COMMANDS[selected_command]

        message = f"✅ {selected_command} | Dirección: {device_address}"

        if command_code == 9:
            baudrate = self.baudrate_var.get()
            parity = self.parity_var.get()

            if not baudrate or not parity:
                self.result_label.config(text="⚠️ Error: Selecciona una velocidad de baudrate y paridad", foreground="red")
                return None, None, None, None

            message += f" | Baudrate: {baudrate} | Paridad: {parity}"
            self.result_label.config(text=message, foreground="green")

            return (device_address, command_code, baudrate, parity)

        self.result_label.config(text=message, foreground="green")
        return (device_address, command_code, None, None)
    
    def execute_and_store(self):
        address, command , baudrate , parity = self.execute_command()
      
        if address is None:
            return
        
        # Al llamar al callback proporcionado por main.py, pasamos los valores
        self.controller.on_execute_callback(address, command, baudrate, parity)
        
        # modbus_op = ModbusRTU_Commands()
        # address = int(address)
        # modbus_op.send_command(command,address,0,baudrate,parity)
   
       
        

    def f_data_send(self, cmd):
        

        # Asegúrate de que self.data_send esté correctamente inicializado
        if hasattr(self, 'data_send') and self.data_send is not None:
            message = f"✅ {cmd}"
            self.data_send.config(text=message, foreground="green")
            self.data_send.update_idletasks()  # Forzar la actualización de la interfaz
            print(f"Texto actualizado en GUI: {message}")
        else:
            print("❌ Error: self.data_send no está definido")

    def get_cmd(self):
        # Si el cmd viene de main.py, solo lo retornamos
        return self.hola
     
   
        
    def f_data_receive(self,cmd):
        message = f"✅ {cmd}"
        
        self.data_receive.config(text=message, foreground="green")
    # def save_modbus_config(self, address, command, baudrate, parity):
    #     """Guardar la configuración Modbus en un archivo JSON"""
    #     modbus_config = {
    #         "device_address": address,
    #         "command": command,
    #         "baudrate": baudrate,
    #         "parity": parity
    #     }

    #     try:
    #         # Intentar abrir el archivo JSON y leer el contenido existente
    #         try:
    #             with open("config.json", "r") as json_file:
    #                 config_data = json.load(json_file)
    #         except (FileNotFoundError, json.JSONDecodeError):
    #             config_data = {}

    #         # Agregar la configuración de Modbus al archivo JSON
    #         config_data["modbus_config"] = modbus_config

    #         # Guardar los datos en el archivo JSON
    #         with open("config.json", "w") as json_file:
    #             json.dump(config_data, json_file, indent=4)

    #         messagebox.showinfo("Configuración Modbus guardada", "La configuración Modbus se ha guardado correctamente.")
    #     except Exception as e:
    #         messagebox.showerror("Error", f"No se pudo guardar la configuración Modbus: {str(e)}")
            

    # def load_modbus_config(self):
    #     """Cargar la configuración Modbus desde el archivo JSON"""
    #     try:
    #         with open("configuracion.json", "r") as json_file:
    #             config_data = json.load(json_file)
    #             modbus_config = config_data.get("modbus_config", {})

    #             # Asignar los valores cargados a los widgets
    #             if modbus_config:
    #                 self.device_address_var.set(modbus_config.get("device_address", ""))
    #                 self.command_var.set(modbus_config.get("command", ""))
    #                 self.baudrate_var.set(modbus_config.get("baudrate", ""))
    #                 self.parity_var.set(modbus_config.get("parity", ""))

    #     except FileNotFoundError:
    #         print("El archivo de configuración Modbus no existe. No se puede cargar.")
    #     except json.JSONDecodeError:
    #         print("Error al leer el archivo de configuración Modbus.")
