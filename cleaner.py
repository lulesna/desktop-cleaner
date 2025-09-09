import os
import shutil

DIR_TO_CLEAN = r'C:\Users\lesna\Desktop'
EXT_TO_DIR = {
    ".psd": "Photoshop",
    ".py": "Coding",
    ".c": "Coding",
    ".cpp": "Coding",
    ".cc": "Coding",
    ".html": "Coding",
    ".css": "Coding",
    ".js": "Coding",
    ".bat": "Coding",
    ".php": "Coding",
    ".java": "Coding",
    ".sql": "Coding",
    ".sh": "Coding",
    ".jpg": "Pictures",
    ".jpeg": "Pictures",
    ".gif": "Pictures",
    ".png": "Pictures",
    ".ico": "Pictures",
    ".bmp": "Pictures",
    ".mp3": "Music",
    ".wav": "Music",
    ".flac": "Music",
    ".mp4": "Videos",
    ".avi": "Videos",
    ".txt": "Notes",
    ".doc": "Documents",
    ".docx": "Documents",
    ".pdf": "Documents",
    ".ppt": "Presentations",
    ".pptx": "Presentations",
    ".zip": "Packages"
}

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
    files = get_files(DIR_TO_CLEAN)
    for file in files:
        extension = get_extension(file)
        if extension in EXT_TO_DIR:
            dir_name = EXT_TO_DIR[extension]
            create_dir_if_not_exists(os.path.join(DIR_TO_CLEAN, dir_name))
            try:
                shutil.move(os.path.join(DIR_TO_CLEAN, file), os.path.join(DIR_TO_CLEAN, dir_name))
                print(f"Przeniesiono: {file} -> {dir_name}/")
            except OSError as e:
                print(f"Błąd przy przenoszeniu {file}: {e}")



if __name__ == '__main__':
    main()
