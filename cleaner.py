import os
import shutil

DIR_TO_CLEAN = r'C:\Users\lesna\Desktop'

def load_extensions_from_file(fname):
    ext_to_dir = {}
    with open(fname, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split(':')
                dir_name = parts[0].strip()
                extensions = parts[1].strip().split()
                for ext in extensions:
                    ext_to_dir[ext] = dir_name
    return ext_to_dir

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
    print(files)
    return files

def get_extension(file):
    extension = os.path.splitext(file)[1]
    if extension:
        print(extension)
        return extension.lower()
    else:
        print("Brak rozszerzenia")
        return ""

def main():
    EXT_TO_DIR = load_extensions_from_file("extensions.txt")
    files = get_files(DIR_TO_CLEAN)
    for file in files:
        extension = get_extension(file)
        if extension in EXT_TO_DIR:
            dir_name = EXT_TO_DIR[extension]
            create_dir_if_not_exists(os.path.join(DIR_TO_CLEAN, dir_name))
            try:
                shutil.move(os.path.join(DIR_TO_CLEAN, file), os.path.join(DIR_TO_CLEAN, dir_name, file))
                print(f"Przeniesiono: {file} -> {dir_name}/")
            except OSError as e:
                print(f"Błąd przy przenoszeniu {file}: {e}")


if __name__ == '__main__':
    main()
