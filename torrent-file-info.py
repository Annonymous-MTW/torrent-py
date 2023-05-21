import os
import bencodepy
from colorama import Fore, Style, init

init(autoreset=True)

def human_readable_size(size, decimal_places=2):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f} {unit}"

def decode_torrent_file(file_path):
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
    except Exception as e:
        print(Fore.RED + f"Nu s-a putut citi fisierul {file_path}. Eroare: {e}")
        return

    try:
        torrent = bencodepy.decode(data)
    except Exception as e:
        print(Fore.RED + f"Nu s-a putut decoda fisierul {file_path}. Eroare: {e}")
        return

    info = torrent[b'info']
    file_name = info.get(b'name', b'').decode('utf-8')
    file_size = human_readable_size(info.get(b'length', 0))

    print(Fore.YELLOW + f"Numele fisierului: {file_name}, Dimensiune: {file_size}")

def scan_folder(folder_path):
    try:
        torrent_files = [f for f in os.listdir(folder_path) if f.endswith(".torrent")]
    except Exception as e:
        print(Fore.RED + f"Nu s-a putut scana folderul {folder_path}. Eroare: {e}")
        return []

    print(Fore.GREEN + f"Sunt {len(torrent_files)} fișiere .torrent în folder.")
    return torrent_files

def list_torrent_files(torrent_files):
    for i, file_name in enumerate(torrent_files, start=1):
        print(Fore.YELLOW + f"{i}. {file_name}")

def select_and_decode_torrent(torrent_files, folder_path):
    list_torrent_files(torrent_files)
    try:
        selected = int(input("Selectați un fișier .torrent: ")) - 1
    except ValueError:
        print(Fore.RED + "Selecție invalidă. Trebuie să introduceți un număr.")
        return

    if 0 <= selected < len(torrent_files):
        decode_torrent_file(os.path.join(folder_path, torrent_files[selected]))
    else:
        print(Fore.RED + "Selecție invalidă.")


def main():
    torrent_files = []
    folder_path = ''
    while True:
        print(Fore.BLUE + "1. Scanează un folder pentru fișiere .torrent")
        print(Fore.BLUE + "2. Afișează lista de fișiere .torrent")
        print(Fore.BLUE + "3. Selectează și analizează un fișier .torrent")
        print(Fore.BLUE + "4. Ieșire")
        option = input("Selectați o opțiune: ")

        if option == '1':
            folder_path = input("Introduceți calea către folder: ")
            torrent_files = scan_folder(folder_path)
        elif option == '2':
            if torrent_files:
                list_torrent_files(torrent_files)
            else:
                print(Fore.RED + "Mai întâi scanați un folder.")
        elif option == '3':
            if torrent_files and folder_path:
                select_and_decode_torrent(torrent_files, folder_path)
            else:
                print(Fore.RED + "Mai întâi scanați un folder.")
        elif option == '4':
            break
        else:
            print(Fore.RED + "Opțiune necunoscută. Vă rugăm să încercați din nou.")

if __name__ == "__main__":
    main()
