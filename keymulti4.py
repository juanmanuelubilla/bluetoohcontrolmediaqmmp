import evdev
from evdev import InputDevice, categorize, ecodes
from pynput.keyboard import Controller, KeyCode
import time
import subprocess
import pystray
from PIL import Image  # Necesitarás instalar el módulo 'Pillow' para trabajar con imágenes

# Ruta del dispositivo de tu teclado Bluetooth
device_path = '/dev/input/event2'  # Actualizado a 'event2'

# ID de la ventana de qmmp
qmmp_window_id = '0x02200006'  # Actualizado a '0x02200006'

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

# Diccionario para mapear los códigos de las teclas a los atajos de teclado si se mantienen presionados
long_press_keymap = {
    ecodes.KEY_PLAYPAUSE: [KeyCode.from_char('v')]  # v
}

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

# Función para escuchar eventos del dispositivo
def listen_for_events(device_path):
    try:
        device = InputDevice(device_path)
        print(f'Successfully opened device {device_path}')
        key_press_times = {}
        
        for event in device.read_loop():
            if event.type == ecodes.EV_KEY:
                key_event = categorize(event)
                keycode = key_event.scancode
                
                if key_event.keystate == key_event.key_down:
                    key_press_times[keycode] = time.time()
                elif key_event.keystate == key_event.key_up:
                    if keycode in key_press_times:
                        press_duration = time.time() - key_press_times[keycode]
                        keys = keymap.get(keycode, [])
                        
                        if press_duration >= 1.0:  # 1 segundo para detectar una pulsación larga
                            keys = long_press_keymap.get(keycode, keys)
                        
                        print(f'Pressing keys: {keys} for keycode: {keycode}')
                        if focus_qmmp():  # Poner qmmp en primer plano solo si se encuentra y se activa
                            time.sleep(0.1)  # Pequeña pausa para asegurar que la ventana tiene el foco
                            press_keys(keys)
                            # Esperar un momento para evitar múltiples activaciones
                            time.sleep(0.1)
                    key_press_times.pop(keycode, None)
    except OSError as e:
        print(f'Error reading from device: {e}')
        return False
    return True

def quit_app(icon, item):
    icon.stop()

if __name__ == '__main__':
    # Cargar el archivo de icono
    icon_image = Image.open("icon.png")
    
    # Crear el ícono en el systray
    tray_icon = pystray.Icon("My Application", icon=icon_image)
    tray_icon.menu = pystray.Menu(
        pystray.MenuItem('Quit', quit_app)
    )
    tray_icon.run()
    
    # Ejecutar el bucle principal de escucha de eventos
    while True:
        if listen_for_events(device_path):
            print(f'Device {device_path} disconnected. Waiting to reconnect...')
        time.sleep(1)

