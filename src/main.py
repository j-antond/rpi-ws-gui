#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import serial
from . import pycrc
import time
import numpy as np
from .ModbusRTU import ModbusRTU_Commands
from .gui import HMI, ModbusPage


#s = serial.Serial("/dev/ttyUSB0",9600) 


def active_outputs(array_hex,array_dec):
    """Función que convierte las listas que devuelve el dispositivo 
        en lista binaria para saber que salidas están activas.

    Args:
        array_hex (list): lista en hexadecimal que leemos del dispositivo cuando le enviamos el comando de lectura de las entradas digitales
        array_dec (list): lista en decimal

    Returns:
        string: mensaje que indica que salidas están activas
    """

    # Elegimos un número decimal para convertir a binario, en este caso tiene que ser el 4 elemento
    num = array_dec[3]
    # Convertimos a binario asegurándonos de que tenga 8 bits (08b)
    array_dec2bin = format(num, '08b')  # Esto devuelve una cadena como '01000001'
    # Convertimos la cadena en una lista de enteros (0 y 1)
    array_dec2bin = np.array([int(bit) for bit in array_dec2bin], dtype=np.int32)
    print(f"{num} en binario: {array_dec2bin}")

    hex_num = array_hex[3]
    bin_str = bin(int(hex_num, 16))[2:].zfill(8)  # Convertimos a binario y aseguramos 8 bits
    array_hex2bin = np.array([int(bit) for bit in bin_str], dtype=np.int32)

    print(f"{hex_num} en binario: {array_hex2bin}")

    #Comparar si son iguales para continuar con el proceso
    if np.array_equal(array_hex2bin,array_dec2bin) == True:
        # Obtenemos los índices donde hay un 1
        indices_activos = sorted([8 - i for i in np.where(array_dec2bin == 1)[0]])
        # Generamos el mensaje
        if len(indices_activos) > 0:
            mensaje = f"Salidas activas: {','.join(map(str, indices_activos))}"
        else:
            mensaje = "No hay salidas activas."

    return mensaje

def return_hex_cmd(cmd):
    """
    Convertir array en decimal a hexadecimal
    Args:
        cmd (list): array of command generated in decimal

    Returns:
        list: array of command converted to hexadecimal
    """
    cmd_hex = []
    for i in cmd:
        cmd_hex.append(hex(i))

    return cmd_hex


#Función que llama a la clase HMI para que se ejecute en tiempo real en la GUI
#En esta función solo habrá llamadas a otras funciones

def check_values(address,command,baudrate,parity):
    address = int(address)
    command = int(command)
    if command== 9:
        baudrate = int(baudrate)
        parity = str(parity)
    
    return address, command, baudrate,parity

def main(address,command,baudrate,parity):
    address, command, baudrate, parity = check_values(address,command,baudrate,parity)
 
    modbus_page = ModbusPage(app,app)
    modbus_op = ModbusRTU_Commands()
    
    exists,command_name = modbus_op.command_exists(command,ModbusRTU_Commands.COMMANDS)
    
    
    if exists:
        if command == 9:
        
            cmd= modbus_op.send_command(command,address,0,baudrate,parity)
        else:
            cmd= modbus_op.send_command(command,address,0)
    
    modbus_page.f_data_send(cmd)  # Pasamos cmd a la función f_data_send de la clase ModbusPage


app = HMI(main)  
def start_gui():
    app.mainloop()
    
    
# # Si el archivo se ejecuta como script principal
# if __name__ == "__main__":
#     app.mainloop()
         
        # for i in range(8):
        #     cmd = modbus_op.send_command(2,1,i)
        #     #s.write(cmd)
        #     time.sleep(0.2)
        #     #print(list(s.read_all()))
            
        #     cmd_hex = return_hex_cmd(cmd)
        #     print(f"Comando generado (hex): {cmd_hex}")
        
        
        #mensaje = active_outputs(cmd_hex_read,cmd_read)
        
 