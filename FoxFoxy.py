import os
import subprocess
import time
from colorama import init, Fore

# Initialize colorama
init(autoreset=True)

# Paths to scripts
FOXYWEB_SCRIPT = "/data/data/com.termux/files/home/FoxFoxy/files/FoxWeb.sh"
FOXYDROID_SCRIPT = "/data/data/com.termux/files/home/FoxFoxy/files/FoxDroid.py"
FOXCARD_SCRIPT = "/data/data/com.termux/files/home/FoxFoxy/files/FoxCard.py"

# Dependencies dictionary (you can populate this as per your actual dependencies)
DEPENDENCIES = {
    FOXYWEB_SCRIPT: [],  # List of dependencies for FoxWeb.sh
    FOXYDROID_SCRIPT: [],  # List of dependencies for FoxDroid.py
    FOXCARD_SCRIPT: []  # List of dependencies for FoxCard.py
}

# Function to execute scripts in their directories
def open_in_new_session(script_path):
    script_name = os.path.basename(script_path)
    script_directory = os.path.dirname(script_path)
    os.chdir(script_directory)  # Change current directory to script's directory

    if script_name.endswith(".sh"):
        subprocess.Popen(['./' + script_name], shell=True)  # Execute shell script
    elif script_name.endswith(".py"):
        subprocess.Popen(['python3', script_name])  # Execute Python script

# Function to check and install missing dependencies
def check_and_install_dependencies(script_path):
    dependencies = DEPENDENCIES.get(script_path, [])
    missing_dependencies = []

    for dependency in dependencies:
        if dependency.startswith("pip"):
            result = subprocess.run(['pip', 'show', dependency], capture_output=True, text=True)
        elif dependency.startswith("pkg"):
            result = subprocess.run(['pkg', 'list-installed', dependency], capture_output=True, text=True)
        else:
            continue
        
        if dependency not in result.stdout:
            missing_dependencies.append(dependency)

    if missing_dependencies:
        print(f"{Fore.RED}Missing dependencies for {script_path}:")
        for dep in missing_dependencies:
            print(f"- {dep}")
        print(f"{Fore.GREEN}Installing dependencies...")
        for dep in missing_dependencies:
            if dep.startswith("pip"):
                subprocess.run(['pip', 'install', dep])
            elif dep.startswith("pkg"):
                subprocess.run(['pkg', 'install', dep])
        print(f"{Fore.GREEN}Dependencies installed!")
    else:
        print(f"{Fore.GREEN}All dependencies for {script_path} are already installed.")

# Main menu function
def main_menu():
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
        {Fore.RED}No me hago responsable de su mal uso
        {Fore.RED}el uso indebido de esta herramienta 
        {Fore.RED}puedd considerarse Inlegal.
        {Fore.YELLOW}desarrolado con fines educativos
        {Fore.BLUE}Version:0.0.0
        {Fore.GREEN}Github: {Fore.YELLOW}https://github.com/Rovanof
        """
        print(banner)
        print(Fore.CYAN + "        Menu:")
        print("        1. FoxyWeb")
        print("        2. FoxyDroid")
        print("        3. FoxCard")
        print("        4. Install Dependencies")
        print("        5. Say Fox")

        option = input("      \033[1;30m FoxFoxy > ")

        if option == "1":
            open_in_new_session(FOXYWEB_SCRIPT)
            input("Press Enter to continue...")
        elif option == "2":
            open_in_new_session(FOXYDROID_SCRIPT)
            input("Press Enter to continue...")
        elif option == "3":
            open_in_new_session(FOXCARD_SCRIPT)
            input("Press Enter to continue...")
        elif option == "4":
            install_dependencies()
            input("Press Enter to continue...")
        elif option == "5":
            say_fox()
            break
        else:
            print(Fore.RED + "Invalid option. Please select a valid option from the menu.")
            time.sleep(2)

# Function to install dependencies for all scripts
def install_dependencies():
    print("Checking and installing dependencies for FoxyWeb, FoxyDroid, and FoxCard...")
    check_and_install_dependencies(FOXYWEB_SCRIPT)
    check_and_install_dependencies(FOXYDROID_SCRIPT)
    check_and_install_dependencies(FOXCARD_SCRIPT)
    print("Dependency installation complete.")

# Function to exit the program
def say_fox():
    print("Exiting the program. Goodbye!")
    exit()

if __name__ == "__main__":
    main_menu()
