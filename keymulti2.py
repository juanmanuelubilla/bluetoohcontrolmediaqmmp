import evdev
from evdev import InputDevice, categorize, ecodes
from pynput.keyboard import Controller, KeyCode
import time
import subprocess

# Ruta del dispositivo de tu teclado Bluetooth
device_path = '/dev/input/event2'  # Actualizado a 'event2'

# ID de la ventana de qmmp
qmmp_window_id = '0x02200006'

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
        subprocess.run(['xdotool', 'windowactivate', qmmp_window_id])
        print(f'Activated qmmp window with ID: {qmmp_window_id}')
        return True
    except Exception as e:
        print(f'Error focusing qmmp: {e}')
        return False

# Función para simular pulsaciones de teclas
def press_keys(keys):
    for key in keys:
        keyboard.press(key)
    for key in reversed(keys):
        keyboard.release(key)

# Escuchar eventos del dispositivo
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

