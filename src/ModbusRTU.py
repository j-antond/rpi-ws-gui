import logging
import pycrc

logging.basicConfig(level=logging.INFO)

class ModbusRTU_Commands:
    """
    Clase para manejar la simplificar el envio de comandos con los módulos Waveshare
    """
    
    COMMANDS = {
        "READ COILS": 1,                 # Leer salidas digitales 0x01
        "READ DISCRETE INPUTS": 2,       # Leer entradas digitales 0x02
        "READ HOLDING REGISTERS": 3,     # Leer registros de almacenamiento 0x03
        "READ INPUT REGISTERS": 4,       # Leer registros de entrada 0x04
        "WRITE SINGLE COIL": 5,          # Escribir en una sola salida digital 0x05
        "WRITE SINGLE REGISTER": 6,      # Escribir en un solo registro 0x06
        "WRITE MULTIPLE COILS": 7,       # Escribir en múltiples salidas digitales 0x0F
        "WRITE MULTIPLE REGISTERS": 8 ,  # Escribir en múltiples registros 0x10
        "SET BAUDRATE": 9 ,              # Cambiar velocidad de transmisión 0x06
        "READ ADDRESS": 10,              # Leer dirección del dispositivo 0x03
        "SET ADDRESS" : 11               # Asignar dirección al dispositivo 0x06
    }
    
    BAUDRATE = {
        4800 : 0X00 ,
        9600 : 0x01 ,
        19200: 0x02 ,
        38400: 0x03 ,
        57600: 0x04,
        115200: 0x05,
        128000: 0x06 ,
        256000: 0x07 ,
        
    }
    
    
    PARITY = {
        "NONE" : 0X00 ,
        "EVEN" : 0x01 ,
        "ODD"  : 0x02 ,
    }
    
    def __init__(self):
        self.broadcast_address = 0x00
        
        
    @classmethod
    def get_command_code(cls, command_name):
        """ Devuelve el código de función Modbus correspondiente a un nombre de comando. """
        return cls.COMMANDS.get(command_name.upper(), None)

    def command_exists(self,function_code,array_commands):
        if function_code not in array_commands.values():  # Buscar en los valores
            logging.error(f"Código de función inválido: {function_code}")
            return False
        # Encontrar la clave asociada al código
        command_name = next((key for key, value in array_commands.items() if value == function_code), "DESCONOCIDO")
        
        return True,command_name
    
    def select_option(options_dict,prompt_message):
        """
        Permite al usuario seleccionar una opción de un diccionario y devuelve la clave seleccionada.
        
        :param options_dict: Diccionario con las opciones a elegir.
        :param prompt_message: Mensaje a mostrar antes de la selección.
        :return: Clave seleccionada del diccionario.
        """
        options_list = list(options_dict.keys()) # Obtener las claves (opciones disponibles)
        
        while True:
            print(prompt_message)
            for i, option in enumerate(options_list, start=1):
                print(f"{i}. {option}")  # Mostrar opciones numeradas

            try:
                choice = int(input("\nSelecciona un número: "))
                if 1 <= choice <= len(options_list):
                    selected_key = options_list[choice - 1]
                    print(f"\n✅ Has seleccionado: {selected_key}")
                    return selected_key  # Devuelve la clave correspondiente
                else:
                    print("⚠ Número fuera de rango. Inténtalo de nuevo.")
            except ValueError:
                print("⚠ Entrada inválida. Ingresa un número válido.")

    def send_command(self,function_code, device_address,count,baudrate_value=9600,parity_method="NONE"):
        #device_address = hex(device_address) #pasar a hexadecimal (el usuario la introducirá como un entero)
        #print(f"El dispositivo está configurado con la dirección {1}, una velocidad de transmisión de {baudrate_value} y una paridad {parity_method}.\n")
        baudrate_value = self.BAUDRATE.get(baudrate_value) 
        parity_method  = self.PARITY.get(parity_method)
        
        """Genera y envía un comando Modbus"""
        try:
            cmd = None  # Asegurar que siempre existe
            if function_code == 1:  # Read Coil Status
                cmd = [device_address, 0x01, count, 2, 0xFF, 0, 0, 0]
            elif function_code == 2:  # Read Discrete Inputs
                cmd = [device_address, 0x02, 0, 0, 0, 8, 0, 0]
                exit
            elif function_code == 3: #Read Holding Registers
                cmd = [device_address, 0x03, 0, 0, 0, 8, 0, 0] #waveshare                                        
                cmd = [device_address, 0x03, 0, 0x02, 0, 0x02, 0, 0]  #Sonda T/HR THM
                #cmd = [device_address, 0x03, 0, register_initial_address, 0, register_numbers, 0, 0]
                """
                Read channel 1-8 data type: 01 03 00 00 00 08 44 0C
                Read channel 1 data type: 01 03 00 00 00 01 84 0A
                Read channel 3-5 data type: 01 03 00 02 00 03 A4 0B 
                """
            elif function_code == 4:
                hola = 0
            elif function_code == 5:
                cmd = [device_address, 0x05, 0, count, 0xFF, 0, 0, 0]
            elif function_code == 6:
                cmd = [device_address, 0x06, 0, count, 0x03, 0xE8, 0, 0]
            elif function_code == 7:
                cmd = [device_address, 0x0F, 0, 0, 0x00, 0x08, 0x01, 0xFF, 0, 0]
            elif function_code == 8:
                cmd = []
            elif function_code == 9: #Set baudrate
                cmd = [device_address, 0x06 , 0x20 , 0 , parity_method, baudrate_value, 0,0]
                exit
            elif function_code == 10: #Read address
                cmd = [self.broadcast_address, 0x03 , 0x40 , 0 , 0, 0x01, 0,0] 
                exit
            elif function_code == 11: #Set Address
                cmd = [self.broadcast_address, 0x06 , 0x40 , 0 , 0, device_address, 0,0]
                exit
            else:
                logging.error(f"Código de función inválido: {hex(function_code)}")
                return None
            
            crc = pycrc.ModbusCRC(cmd[:-2]) #coger los primeros bytes para calcular el CRC
            cmd[-2] = crc & 0xFF
            cmd[-1] = crc >> 8
            
            print(f"Comando generado: {cmd}")
         
            return cmd  # Aquí iría la lógica de envío
        except Exception as e:
            logging.error(f"Error al enviar comando: {e}")
            return None
        


    @staticmethod
    def get_baudrate_options():
        """Obtiene las opciones de baudrate"""
        return list(ModbusRTU_Commands.BAUDRATE.keys())

    @staticmethod
    def get_parity_options():
        """Obtiene las opciones de paridad"""
        return list(ModbusRTU_Commands.PARITY.keys())