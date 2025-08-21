# Interfaz gráfica para Raspberry Pi con comunicación Modbus RTU vía dispositivo Waveshare

Este proyecto tiene como objetivo el desarrollo de una interfaz gráfica de usuario (GUI) que permita la comunicación y el control de dispositivos industriales a través del protocolo Modbus RTU, utilizando una Raspberry Pi conectada a los módulos Modbus RTU de Waveshare. La interfaz permite visualizar datos en tiempo real y enviar comandos, todo ello con una experiencia visual amigable.

## Objetivos principales

- Establecer comunicación Modbus RTU entre la Raspberry Pi y dispositivos esclavos (sensores, actuadores, PLCs) mediante el módulo RS485 de Waveshare.

- Desarrollar una interfaz gráfica en Python para leer y escribir registros Modbus (holding registers, input registers, coils, etc.).

- Monitorizar datos en tiempo real y registrar eventos o variables seleccionadas.

- Diseñar una arquitectura de software robusta, modular y fácilmente escalable.

## Características del sistema

- Interfaz gráfica táctil o mediante ratón/teclado.

- Soporte para múltiples esclavos Modbus.

- Lectura periódica y escritura de registros Modbus (funciones 03, 04, 06, 16...).

- Gestión de errores y control de estados de comunicación.

## Tecnologías utilizadas

### Hardware

- Raspberry Pi 5

- Módulo RS485 USB o UART de Waveshare

- Dispositivos Modbus RTU Waveshare

### Software

- Python 3

- Librería pymodbus o minimalmodbus

- GUI con Tkinter

- Sistema operativo: Raspberry Pi OS

## Aplicaciones posibles

- Monitorización de sensores industriales (temperatura, humedad, presión, etc.)

- Automatización de procesos sencillos

- Estaciones de pruebas o bancadas de laboratorio

- Sistemas SCADA ligeros

## 🚀 Instalación del entorno

### 1. Clonar el repositorio

```bash
git clone https://github.com/j-antond/rpi-ws-gui.git 
cd rpi-ws-gui
```

---

### 2. Crear un entorno virtual

- En Windows:

```bash
pyhon -m venv venv 
venv\Scripts\activate
```

- En macOS/Linux:

```bash
pyhon3 -m venv venv 
source venv/bin/activate
```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

Esto instalará todos los paquetes necesarios como `numpy`, `pyserial` y `ttkbootstrap`. 

## ✅ Verificar instalación
Puedes probar ejecutando Python e importando los módulos principales

```python 
import numpy 
import serial
import ttkbootstrap
```


## 🖥 Ejecutar la interfaz gráfica (GUI)

Para iniciar la interfaz gráfica del proyecto, simplemente ejecuta el archivo `main.py` desde la raíz del proyecto:

```bash
python -m src.main
```

> ⚠️ Asegúrate de tener un archivo `__init__.py` dentro de la carpeta `src/` para que Python la reconozca como un paquete.


## 🧪 Ejecutar tests

```bash
python -m unittest test.test_main
```

---

## 🛠 Estructura del proyecto

```text
mi_proyecto/
├── src/
│   ├── __init__.py
│   ├── gui.py
│   ├── main.py
│   ├── ModbusRTU.py
│   └── pycrc.py
├── test/
│   ├── __init__.py
│   └── test_main.py
├── .gitignore
├── requirements.txt
└── README.md
```
