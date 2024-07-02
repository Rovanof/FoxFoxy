import os
import subprocess
import random
import time
from faker import Faker
from colorama import init, Fore, Style

init(autoreset=True)

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

fake = Faker()

def generate_fake_credit_card(first_six_digits, last_four_digits):
    # Generar 6 dígitos aleatorios para el medio de la tarjeta
    middle_digits = ''.join(random.choice('0123456789') for _ in range(6))

    # Generar una fecha aleatoria (mes/año)
    expiration_date = f"{random.randint(1, 12):02d}/{random.randint(24, 30)}"

    # Generar un CCV aleatorio de 3 dígitos
    ccv = ''.join(random.choice('0123456789') for _ in range(3))

    # Generar dirección aleatoria
    address = fake.address()

    # Combinar todos los componentes para formar el número completo de la tarjeta
    credit_card_number = first_six_digits + middle_digits + last_four_digits

    return credit_card_number, expiration_date, ccv, address

def luhn_checksum(card_number):
    digits = list(map(int, card_number))
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = sum(odd_digits)
    for digit in even_digits:
        checksum += sum(divmod(2 * digit, 10))
    return checksum % 10

def is_valid_credit_card(card_number):
    return luhn_checksum(card_number) == 0

def get_card_type(card_number):
    if card_number.startswith("4"):
        return "Visa"
    elif card_number.startswith("5"):
        return "MasterCard"
    else:
        return "Desconocida"

def validate_card_length(card_number):
    return len(card_number) in [16, 19]

def validate_expiration_date(expiration_date):
    month, year = map(int, expiration_date.split('/'))
    return 1 <= month <= 12 and 22 <= year <= 30

def validate_ccv(ccv):
    return len(ccv) == 3 and ccv.isdigit()

def validate_address(address):
    return len(address) > 10

def additional_verifications(card):
    numero_tarjeta, fecha_expiracion, ccv, direccion = card
    return (validate_card_length(numero_tarjeta) and
            validate_expiration_date(fecha_expiracion) and
            validate_ccv(ccv) and
            validate_address(direccion))

def generate_and_save_valid_cards(quantity):
    valid_cards = []
    with open("tarjetas_validas.txt", "w") as file:
        for i in range(quantity):
            print(f"Generando tarjeta {i+1}...")
            time.sleep(1)  # Espera de 1 segundo por generación de tarjeta

            credit_card = generate_fake_credit_card("477053", "2606")  # Usar los dígitos de la Visa proporcionada
            numero_tarjeta, fecha_expiracion, ccv, direccion = credit_card

            if is_valid_credit_card(numero_tarjeta) and additional_verifications(credit_card):
                card_type = get_card_type(numero_tarjeta)
                file.write(f"Número de tarjeta: {numero_tarjeta}\n")
                file.write(f"Tipo: {card_type}\n")
                file.write(f"Fecha de expiración: {fecha_expiracion}\n")
                file.write(f"CCV: {ccv}\n")
                file.write(f"Dirección: {direccion}\n\n")
                valid_cards.append(credit_card)
                print(Fore.GREEN + f"Tarjeta {i+1} generada y validada correctamente.")
            else:
                print(Fore.RED + f"Error: Tarjeta {i+1} generada no válida.")

    return valid_cards

# Mostrar el banner al inicio
mostrar_banner()

# Pedir al usuario la cantidad de tarjetas de crédito a generar
try:
    cantidad = int(input("Ingrese la cantidad de tarjetas de crédito a generar: "))
    if cantidad <= 0:
        raise ValueError("La cantidad debe ser mayor a cero.")

    # Generar y guardar las tarjetas de crédito válidas
    tarjetas_validas = generate_and_save_valid_cards(cantidad)

    # Mostrar las tarjetas de crédito válidas generadas
    print("\nTarjetas de crédito válidas generadas y guardadas en 'tarjetas_validas.txt':")
    for i, tarjeta in enumerate(tarjetas_validas, start=1):
        numero_tarjeta, fecha_expiracion, ccv, direccion = tarjeta
        card_type = get_card_type(numero_tarjeta)
        print(f"\nTarjeta {i}:")
        print("Número de tarjeta de crédito:", numero_tarjeta)
        print("Tipo:", card_type)
        print("Fecha de expiración:", fecha_expiracion)
        print("CCV:", ccv)
        print("Dirección:", direccion)

except ValueError as e:
    print(Fore.RED + "Error:", e)
except Exception as e:
    print(Fore.RED + "Ocurrió un error:", e)
