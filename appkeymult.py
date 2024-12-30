import evdev
from evdev import InputDevice, categorize, ecodes
from pynput.keyboard import Controller, KeyCode
import time
import subprocess
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt5.QtGui import QIcon
import sys
import pystray
from PIL import Image

# Ruta del dispositivo de tu teclado Bluetooth
device_path = '/dev/input/event2'  # Actualizado a 'event2'

# ID de la ventana de qmmp
qmmp_window_id = '0x02000006'

# Crear el dispositivo de entrada
device = InputDevice(device_path)

# Crear un controlador de teclado
keyboard = Controller()

# Diccionario para mapear los códigos de las teclas a los atajos de teclado
keymap = {
    ecodes.KEY_PLAYPAUSE: [KeyCode.from_char('x')],  # x
    ecodes.KEY_NEXTSONG: [KeyCode.from_char('b')],   # b
    ecodes.KEY_PREVIOUSSONG: [KeyCode.from_char('z')],# z
    ecodes.KEY_VOLUMEUP: [KeyCode.from_char('0')],   # 0
    ecodes.KEY_VOLUMEDOWN: [KeyCode.from_char('9')]  # 9
}

print(f'Listening for events on {device_path}...')

# Función para poner qmmp en primer plano usando xdotool con el ID de ventana específico
def focus_qmmp():
    try:
        subprocess.run(['xdotool', 'windowactivate', qmmp_window_id], check=True)
        print(f'Activated qmmp window with ID: {qmmp_window_id}')
        return True
    except subprocess.CalledProcessError as e:
        print(f'Error focusing qmmp: {e}')
        return False

# Función para simular pulsaciones de teclas
def press_keys(keys):
    for key in keys:
        keyboard.press(key)
    for key in reversed(keys):
        keyboard.release(key)

# Función para mostrar la ventana principal al hacer clic en el icono de la bandeja del sistema
def show_window(icon, window):
    window.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Crear ventana principal (puede ser una instancia de QMainWindow, por ejemplo)
    # window = QMainWindow()

    # Crear icono de la bandeja del sistema
    icon = QSystemTrayIcon(QIcon('icon.png'), app)
    icon.setToolTip('Mi Aplicación')

    # Crear menú para el icono de la bandeja del sistema
    menu = QMenu()
    show_action = menu.addAction("Mostrar")
    quit_action = menu.addAction("Salir")

    # Conectar la acción de mostrar la ventana principal al menú
    show_action.triggered.connect(lambda: show_window(icon, window))
    quit_action.triggered.connect(app.quit)

    # Configurar el menú en el icono de la bandeja del sistema
    icon.setContextMenu(menu)
    icon.setVisible(True)

    # Configurar Pystray para que funcione en segundo plano
    def on_quit(icon, item):
        icon.stop()
        app.quit()

    image = Image.open('icon.png')
    icon = pystray.Icon("example", image, "Example", menu)
    icon.run(on_quit)

    # Escuchar eventos del dispositivo
    try:
        for event in device.read_loop():
            if event.type == ecodes.EV_KEY:
                key_event = categorize(event)
                if key_event.keystate == key_event.key_down:
                    if key_event.scancode in keymap:
                        keys = keymap[key_event.scancode]
                        print(f'Pressing keys: {keys}')
                        if focus_qmmp():  # Poner qmmp en primer plano solo si se encuentra y se activa
                            time.sleep(0.1)  # Pequeña pausa para asegurar que la ventana tiene el foco
                            press_keys(keys)
                            # Esperar un momento para evitar múltiples activaciones
                            time.sleep(0.1)
    except OSError as e:
        print(f'Error reading from device: {e}')
    except KeyboardInterrupt:
        print("KeyboardInterrupt: Exiting the script...")
    finally:
        device.close()
import evdev
from evdev import InputDevice, categorize, ecodes
from pynput.keyboard import Controller, KeyCode
import time
import subprocess
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt5.QtGui import QIcon
import sys
import pystray
from PIL import Image

# Ruta del dispositivo de tu teclado Bluetooth
device_path = '/dev/input/event2'  # Actualizado a 'event2'

# ID de la ventana de qmmp
qmmp_window_id = '0x02000006'

# Crear el dispositivo de entrada
device = InputDevice(device_path)

# Crear un controlador de teclado
keyboard = Controller()

# Diccionario para mapear los códigos de las teclas a los atajos de teclado
keymap = {
    ecodes.KEY_PLAYPAUSE: [KeyCode.from_char('x')],  # x
    ecodes.KEY_NEXTSONG: [KeyCode.from_char('b')],   # b
    ecodes.KEY_PREVIOUSSONG: [KeyCode.from_char('z')],# z
    ecodes.KEY_VOLUMEUP: [KeyCode.from_char('0')],   # 0
    ecodes.KEY_VOLUMEDOWN: [KeyCode.from_char('9')]  # 9
}

print(f'Listening for events on {device_path}...')

# Función para poner qmmp en primer plano usando xdotool con el ID de ventana específico
def focus_qmmp():
    try:
        subprocess.run(['xdotool', 'windowactivate', qmmp_window_id], check=True)
        print(f'Activated qmmp window with ID: {qmmp_window_id}')
        return True
    except subprocess.CalledProcessError as e:
        print(f'Error focusing qmmp: {e}')
        return False

# Función para simular pulsaciones de teclas
def press_keys(keys):
    for key in keys:
        keyboard.press(key)
    for key in reversed(keys):
        keyboard.release(key)

# Función para mostrar la ventana principal al hacer clic en el icono de la bandeja del sistema
def show_window(icon, window):
    window.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Crear ventana principal (puede ser una instancia de QMainWindow, por ejemplo)
    # window = QMainWindow()

    # Crear icono de la bandeja del sistema
    icon = QSystemTrayIcon(QIcon('icon.png'), app)
    icon.setToolTip('Mi Aplicación')

    # Crear menú para el icono de la bandeja del sistema
    menu = QMenu()
    show_action = menu.addAction("Mostrar")
    quit_action = menu.addAction("Salir")

    # Conectar la acción de mostrar la ventana principal al menú
    show_action.triggered.connect(lambda: show_window(icon, window))
    quit_action.triggered.connect(app.quit)

    # Configurar el menú en el icono de la bandeja del sistema
    icon.setContextMenu(menu)
    icon.setVisible(True)

    # Configurar Pystray para que funcione en segundo plano
    def on_quit(icon, item):
        icon.stop()
        app.quit()

    image = Image.open('icon.png')
    icon = pystray.Icon("example", image, "Example", menu)
    icon.run(on_quit)

    # Escuchar eventos del dispositivo
    try:
        for event in device.read_loop():
            if event.type == ecodes.EV_KEY:
                key_event = categorize(event)
                if key_event.keystate == key_event.key_down:
                    if key_event.scancode in keymap:
                        keys = keymap[key_event.scancode]
                        print(f'Pressing keys: {keys}')
                        if focus_qmmp():  # Poner qmmp en primer plano solo si se encuentra y se activa
                            time.sleep(0.1)  # Pequeña pausa para asegurar que la ventana tiene el foco
                            press_keys(keys)
                            # Esperar un momento para evitar múltiples activaciones
                            time.sleep(0.1)
    except OSError as e:
        print(f'Error reading from device: {e}')
    except KeyboardInterrupt:
        print("KeyboardInterrupt: Exiting the script...")
    finally:
        device.close()

