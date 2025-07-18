# PRUEBA USO GIT
Esto es una prueba para ver como funcionan los comandos de Git. Ha sido creada a partir de un directorio local y se ha cargado en el directorio remoto o en la nube.
Con este repositorio se probarán los diferentes comandos que existen y como se hace uso de ellos.

# PROYECTO PYTHON
Proyecyo base en Python. Contiene una estructura inicial con 'src/' y 'tests/'

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



