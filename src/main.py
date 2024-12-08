from pyfiglet import Figlet
import string
import random
import zxcvbn
from os import path
from datetime import datetime
from colorama import Fore, Style, init

"""
PasswdG - Password Generator and Analyzer

Copyright (c) 2024 [Enes Can Adil]

This project is licensed under the MIT License.
See the LICENSE file in the project root for more information.
"""

init(autoreset=True)

figlet = Figlet(font='slant')

def menu():
    print(Fore.CYAN + figlet.renderText('PasswdG'))
    print(Fore.GREEN + "Welcome to the Password Generator!")
    print(Fore.YELLOW + "1. Generate a password")
    print(Fore.YELLOW + "2. Analyze your password")
    print(Fore.RED + "3. Exit")

def user_input(prompt, valid_options=None):
    while True:
        response = input(Fore.BLUE + prompt).strip().upper()
        if valid_options and response not in valid_options:
            print(Fore.RED + "Please enter a valid option.")
        else:
            return response

def generate_password(length, lowercase, uppercase, digits, special_chars):
    char_set = ""

    if lowercase == "Y":
        char_set += string.ascii_lowercase
    if uppercase == "Y":
        char_set += string.ascii_uppercase
    if digits == "Y":
        char_set += string.digits
    if special_chars == "Y":
        char_set += string.punctuation

    if not char_set:
        return None

    return ''.join(random.choice(char_set) for _ in range(length))

def analyze_password(password):
    print(Fore.MAGENTA + "\nDetailed Password Analysis:")
    analysis = zxcvbn.zxcvbn(password)
    score = analysis['score']
    crack_time_online = analysis['crack_times_display']['online_no_throttling_10_per_second']
    crack_time_offline = analysis['crack_times_display']['offline_fast_hashing_1e10_per_second']

    levels = ["Very Weak", "Weak", "Medium", "Strong", "Very Strong"]
    colors = [Fore.RED, Fore.YELLOW, Fore.LIGHTYELLOW_EX, Fore.GREEN, Fore.LIGHTGREEN_EX]

    print(Fore.CYAN + f"Password: {Fore.LIGHTWHITE_EX}{password}")
    print(f"Score: {colors[score]}{score} ({levels[score]})")
    print(Fore.LIGHTBLUE_EX + f"Online cracking time (10 guesses/sec): {crack_time_online}")
    print(Fore.LIGHTBLUE_EX + f"Offline cracking time (fast hardware): {crack_time_offline}")

    if analysis['feedback']['warning']:
        print(Fore.RED + f"Warning: {analysis['feedback']['warning']}")
    if analysis['feedback']['suggestions']:
        print(Fore.LIGHTYELLOW_EX + "Suggestions:")
        for suggestion in analysis['feedback']['suggestions']:
            print(Fore.LIGHTMAGENTA_EX + f"- {suggestion}")

def save_password(password):
    if not path.exists("passwords.txt"):
        with open("passwords.txt", "w") as file:
            pass

    with open("passwords.txt", "r+") as file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        saved_passwords = file.read().splitlines()
        if password in saved_passwords:
            print(Fore.RED + "This password is already saved.")
            return
        file.write(f"{password} - {timestamp}\n")
        print(Fore.GREEN + "Password saved to 'passwords.txt'.")

def analyze_existing_password():
    password = input(Fore.BLUE + "Please enter the password you want to analyze: ").strip()
    if not password:
        print(Fore.RED + "Please enter a valid password!")
        return
    analyze_password(password)

def main():
    while True:
        menu()
        choice = user_input("Choose an option: ", ["1", "2", "3"])

        if choice == "1":
            while True:
                try:
                    length = int(input(Fore.CYAN + "Enter the password length (min. 4): "))
                    if length >= 4:
                        break
                    else:
                        print(Fore.RED + "The password length must be at least 4.")
                except ValueError:
                    print(Fore.RED + "Please enter a valid number.")

            lowercase = user_input("Include lowercase letters? (Y/N): ", ["Y", "N"])
            uppercase = user_input("Include uppercase letters? (Y/N): ", ["Y", "N"])
            digits = user_input("Include numbers? (Y/N): ", ["Y", "N"])
            special_chars = user_input("Include special characters? (Y/N): ", ["Y", "N"])

            password = generate_password(length, lowercase, uppercase, digits, special_chars)

            if not password:
                print(Fore.RED + "You must select at least one type of character!")
                continue

            analyze_password(password)

            save = user_input("\nDo you want to save the generated password? (Y/N): ", ["Y", "N"])
            if save == "Y":
                save_password(password)

            cont = user_input("\nWould you like to generate another password? (Y/N): ", ["Y", "N"])
            if cont != "Y":
                print(Fore.LIGHTBLUE_EX + "Exiting the program...")
                break

        elif choice == "2":
            analyze_existing_password()

        elif choice == "3":
            print(Fore.LIGHTBLUE_EX + "Exiting the program...")
            break

if __name__ == "__main__":
    main()
