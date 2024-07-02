import os
import subprocess
from colorama import init, Fore, Style
import threading
import socket
import time

# Inicializar colorama para soporte de colores ANSI en Windows
init(autoreset=True)

# Secuencia de Port Knocking
PORT_KNOCK_SEQUENCE = [1234, 2345, 3456]

# Función para validar comandos permitidos
def validar_comando(comando):
    comandos_permitidos = ["ls", "pwd", "cd", "exit", "mkdir", "rmdir", "cat", "echo", "touch", "rm", "FoxFoxy", "FoxHelp"]
    if comando.split()[0] in comandos_permitidos:
        return True
    return False

# Función para mostrar el banner
def mostrar_banner():
    while True:
        os.system("clear")
        banner = f"""
        {Fore.RED}╱▏┈┈┈┈┈┈▕╲▕╲┈┈┈
        {Fore.YELLOW}▏▏┈┈┈┈┈┈▕▏▔▔╲┈┈
        {Fore.GREEN}▏╲┈┈┈┈┈┈╱┈▔┈▔╲┈
        {Fore.CYAN}╲▏▔▔▔▔▔▔╯╯╰┳━━▀
        {Fore.BLUE}┈▏╯╯╯╯╯╯╯╯╱┃┈┈┈
        {Fore.MAGENTA}┈┃┏┳┳━━━┫┣┳┃┈┈┈
        {Fore.RED}┈┃┃┃┃┈┈┈┃┃┃┃┈┈┈
        {Fore.YELLOW}┈┗┛┗┛┈┈┈┗┛┗┛┈┈┈

        {Fore.CYAN}░█▀▀░█▀█░█░█░█▀▀░█▀█░█░█░█░█
        {Fore.BLUE}░█▀▀░█░█░▄▀▄░█▀▀░█░█░▄▀▄░░█░
        {Fore.MAGENTA}░▀░░░▀▀▀░▀░▀░▀░░░▀▀▀░▀░▀░░▀░

        {Fore.GREEN}Github: {Fore.YELLOW}https://github.com/Rovanof
        """
        print(banner)
        break

# Función para colorear la salida del comando ls
def colorear_salida_ls(salida):
    lines = salida.split("\n")
    for line in lines:
        parts = line.split()
        for part in parts:
            if part.endswith('/'):
                print(Fore.YELLOW + part, end=' ')
            elif part.endswith('.jpg') or part.endswith('.png'):
                print(Fore.RED + part, end=' ')
            elif part.endswith('.mp4') or part.endswith('.mkv'):
                print(Fore.BLUE + part, end=' ')
            else:
                print(Fore.GREEN + part, end=' ')
        print()

# Función para enviar la secuencia de Port Knocking
def enviar_port_knock(ip_address, sequence):
    for puerto in sequence:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.sendto(b'', (ip_address, puerto))
            sock.close()
            time.sleep(0.5)  # Esperar un poco entre los knocks
        except socket.error as e:
            print(Fore.RED + f"Error al enviar a {puerto}: {e}")

# Función para escanear puertos
def escanear_puertos(ip_address):
    puertos_abiertos = []
    puertos_a_probar = [5555, 5556, 5557]
    for puerto in puertos_a_probar:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        resultado = sock.connect_ex((ip_address, puerto))
        if resultado == 0:
            puertos_abiertos.append(puerto)
        sock.close()
    return puertos_abiertos

# Función para conectar a un dispositivo Android
def connect_device(ip_address):
    enviar_port_knock(ip_address, PORT_KNOCK_SEQUENCE)
    puertos_abiertos = escanear_puertos(ip_address)
    if not puertos_abiertos:
        print(Fore.RED + f"No se encontraron puertos abiertos en el dispositivo {ip_address}.")
        return False

    for puerto in puertos_abiertos:
        try:
            # Intentar conectar al dispositivo en el puerto encontrado
            connect_command = ["adb", "connect", f"{ip_address}:{puerto}"]
            result = subprocess.run(connect_command, capture_output=True, text=True)

            if "connected to" in result.stdout:
                print(Fore.GREEN + f"Conexión exitosa con el dispositivo {ip_address}:{puerto}.")
                return True
            else:
                print(Fore.RED + f"Error al conectar con el dispositivo {ip_address}:{puerto}: {result.stderr}")
        except subprocess.CalledProcessError as e:
            print(Fore.RED + f"Error al conectar con el dispositivo {ip_address}:{puerto}: {e}")

    print(Fore.RED + f"No se pudo conectar con el dispositivo {ip_address}.")
    return False

# Función para leer la salida del dispositivo de forma asíncrona
def leer_salida(adb_process):
    while True:
        output = adb_process.stdout.readline().strip()
        if output:
            if 'ls' in output:
                colorear_salida_ls(output)
            else:
                print(output)
        else:
            break

# Función para ejecutar comandos repetidos en el dispositivo
def execute_repeated_commands(adb_process, ip_address):
    while True:
        comando = input(Fore.RED + "FoxFoxy > " + Style.RESET_ALL)
        
        if comando.strip().lower() == "exit":
            break
        
        if comando.strip().lower() == "FoxHelp":
            print("Comandos disponibles:")
            print("ls, pwd, cd, exit, mkdir, rmdir, cat, echo, touch, rm, FoxFoxy, FoxHelp")
            continue
        
        if not validar_comando(comando):
            print(Fore.RED + "Comando no permitido.")
            continue
        
        if comando.strip().lower() == "FoxFoxy":
            # Comando especial para reproducir video
            video_command = f"adb -s {ip_address} shell am start -a android.intent.action.VIEW -d file:///data/data/com.termux/files/home/FoxFoxy/files/FoxFoxy.mp4 -t video/mp4"
            subprocess.run(video_command, shell=True)
            continue
        
        try:
            adb_process.stdin.write(comando + "\n")
            adb_process.stdin.flush()
            threading.Thread(target=leer_salida, args=(adb_process,)).start()
        except BrokenPipeError as e:
            print(Fore.RED + f"Error de comunicación con el dispositivo: {e}")
            break

# Función para abrir una shell en el dispositivo
def open_shell(ip_address):
    try:
        adb_command = ["adb", "-s", ip_address, "shell"]
        adb_process = subprocess.Popen(adb_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        print(Fore.GREEN + f"Shell abierta en el dispositivo {ip_address}. Ingrese 'exit' para salir.")
        execute_repeated_commands(adb_process, ip_address)

        adb_process.terminate()
        adb_process.communicate()

        print(Fore.GREEN + f"Desconectado del dispositivo {ip_address}")

    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"Error al abrir la shell en el dispositivo {ip_address}: {e}")
    except Exception as e:
        print(Fore.RED + f"Ha ocurrido un error: {e}")



# Función principal para gestionar las conexiones a dispositivos
def main():
    mostrar_banner()
    ip_addresses = input("Ingrese las direcciones IP de los dispositivos Android separadas por comas: ").split(',')
    connected_devices = [] 
    for ip in ip_addresses:
        ip = ip.strip()
        if connect_device(ip):
            connected_devices.append(ip)
        else:
            print(Fore.YELLOW + f"Reintentando conexión con {ip}...")
            if connect_device(ip):
                connected_devices.append(ip)
            else:
                print(Fore.RED + f"No se pudo conectar con el dispositivo {ip}")

    if not connected_devices:
        print(Fore.RED + "No se pudo conectar a ningún dispositivo.")
        return

    print("Dispositivos conectados:")
    for idx, ip in enumerate(connected_devices):
        print(f"{idx + 1}. {ip}")

    try:
        selected_index = int(input("Seleccione el número del dispositivo al que desea acceder: ")) -1
    except ValueError:
        print(Fore.RED + "Selección inválida.")
        return

    if 0 <= selected_index < len(connected_devices):
        open_shell(connected_devices[selected_index])
    else:
        print(Fore.RED + "Selección inválida.")

if __name__ == "__main__":
    main()
