import os
import shutil
from pprint import pprint

FILE_NAME = "extensions.txt"

def load_extensions_from_file(fname):
    ext_to_dir = {}
    path = None
    with open(fname, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                if line.startswith('PATH:'):
                    path = line.split(':', 1)[1].strip()
                else:
                    parts = line.split(':')
                    dir_name = parts[0].strip()
                    extensions = parts[1].strip().split()
                    for ext in extensions:
                        ext_to_dir[ext] = dir_name
    return ext_to_dir, path

def create_dir_if_not_exists(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"Stworzono folder: {path}")
    except OSError:
        print("Błąd")

def get_files(path):
    files_and_dirs = os.listdir(path)
    files = []
    for file_or_dir in files_and_dirs:
        if os.path.isfile(os.path.join(path, file_or_dir)):
            files.append(file_or_dir)
    return files

def get_extension(file):
    extension = os.path.splitext(file)[1]
    if extension:
        return extension.lower()
    else:
        print("Brak rozszerzenia")
        return ""

def clean_files():
    ext_to_dir, dir_path = load_extensions_from_file(FILE_NAME)
    if not dir_path:
        print("Nie znaleziono ścieżki w pliku konfiguracyjnym.")
        return
    files = get_files(dir_path)
    for file in files:
        extension = get_extension(file)
        if extension in ext_to_dir:
            dir_name = ext_to_dir[extension]
            create_dir_if_not_exists(os.path.join(dir_path, dir_name))
            try:
                shutil.move(os.path.join(dir_path, file), os.path.join(dir_path, dir_name, file))
                print(f"Przeniesiono: {file} -> {dir_name}/")
            except OSError as e:
                print(f"Błąd przy przenoszeniu {file}: {e}")


def preview_clean_files():
    ext_to_dir, dir_path = load_extensions_from_file(FILE_NAME)
    if not dir_path:
        print("Nie znaleziono ścieżki w pliku konfiguracyjnym.")
        return
    files = get_files(dir_path)
    print("\n!PODGLĄD SPRZĄTANIA!")
    to_move = {}
    ignored = []
    for file in files:
        extension = get_extension(file)
        if extension in ext_to_dir:
            dir_name = ext_to_dir[extension]
            if dir_name not in to_move:
                to_move[dir_name] = []
            to_move[dir_name].append(file)
        else:
            ignored.append(file)
    print("\nPrzeniesione pliki:")
    pprint(to_move)
    print("\nZignorowane pliki:")
    pprint(ignored)
    total_to_move = sum(len(files) for files in to_move.values())
    print(f"\nPodsumowanie: {total_to_move} plików do przeniesienia, {len(ignored)} zignorowanych")


def show_current_settings(fname):
    with open(fname, "r") as f:
        print(f.read())


def add_new_dir(fname):
    dir_name = input("Podaj nazwę dla nowego folderu: ").strip()
    with open(fname, "a") as f:
        f.write(f"\n{dir_name}:")


def add_new_extension(fname):
    ext_name = input("Podaj nazwę rozszerzenia, które chcesz dodać, np. .txt: ").strip()
    if not ext_name.startswith("."):
        ext_name = f".{ext_name}"

    ext_to_dir, _ = load_extensions_from_file(fname)
    if ext_name in ext_to_dir:
        current_dir = ext_to_dir[ext_name]
        print(f"Rozszerzenie {ext_name} już zostało dodane wcześniej do {current_dir}")
        return

    dir_name = input("Podaj nazwę folderu, do którego ma zostać dodane rozszerzenie: ").strip()

    with open(fname, "r") as f:
        lines = f.readlines()

    found = False
    for i, line in enumerate(lines):
        if line.strip().startswith(dir_name + ":"):
            lines[i] = f"{line.strip()} {ext_name}\n"
            found = True
            break
    if found:
        with open(fname, "w") as f:
            f.writelines(lines)
            print(f"Dodano rozszerzenie {ext_name} do folderu {dir_name}.")
    else:
        print(f"Folder {dir_name} nie znaleziony, czy dodać ten folder?")
        answer = input("T/N: ")
        if answer.upper() == "T":
            add_new_dir(fname)
            print(f"Folder {dir_name} został dodany. Spróbuj ponownie dodać rozszerzenie.")
        elif answer.upper() == "N":
            print("Nie dodano rozszerzenia z powodu braku podanego folderu.")
        else:
            print("Podano błędną odpowiedź.")

def save_path_to_file(fname, path):
    with open(fname, 'r') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if line.strip().startswith('PATH:'):
            lines[i] = f"PATH: {path}\n"
            break

    with open(fname, 'w') as f:
        f.writelines(lines)


def main():
    try:
        while True:
            print("""
    1. Uruchom sprzątanie
    2. Symulacja sprzątania
    3. Pokaż obecne ustawienia  
    4. Zarządzaj folderami i rozszerzeniami
    5. Wyjdź
                """)
            choice = input("Wybór: ")

            if choice == "1":
                clean_files()
            elif choice == "2":
                preview_clean_files()
            elif choice == "3":
                show_current_settings(FILE_NAME)
            elif choice == "4":
                while True:
                    print("""
        Co chcesz zmodyfikować?
        1. Dodaj nowy folder
        2. Dodaj rozszerzenie do istniejącego folderu
        3. Zmień ścieżkę folderu do posprzątania
        4. Powrót do menu głównego
                    """)
                    choice_2 = input("Wybór: ")
                    if choice_2 == "1":
                        add_new_dir(FILE_NAME)
                    elif choice_2 == "2":
                        add_new_extension(FILE_NAME)
                    elif choice_2 == "3":
                        current_path = None
                        with open(FILE_NAME, 'r') as f:
                            first_line = f.readline()
                            if first_line.startswith('PATH:'):
                                current_path = first_line.split(':', 1)[1].strip()
                            else:
                                print(f"Ścieżka jest błędnie zapisana w pliku {FILE_NAME}.")
                        print(f"Aktualna ścieżka folderu: {current_path}")
                        new_path = input("Podaj nową ścieżkę (w takim formacie jak ta powyżej): ")
                        new_path = os.path.normpath(new_path.strip())
                        if os.path.isdir(new_path):
                            save_path_to_file(FILE_NAME, new_path)
                            print(f"Zmieniono ścieżkę na: {new_path}")
                        else:
                            print("Ścieżka nie istnieje lub nie jest katalogiem.")
                    elif choice_2 == "4":
                        print("Wyjście z menu modyfikacji")
                        break
                    else:
                        print("Nieprawidłowy wybór. Wybierz 1-4.")
            elif choice == "5":
                print("Wyjście z programu")
                break
            else:
                print("Nieprawidłowy wybór. Wybierz 1-4.")
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
