import os
import subprocess

def convert_to_exe(file_path, output_folder):
    file_name = os.path.basename(file_path)
    exe_name = file_name.split('.')[0] + ".exe"
    output_path = os.path.join(output_folder, exe_name)
    subprocess.run(["pyinstaller", "--onefile", "--distpath", output_folder, file_path])
    print(f"Converted {file_name} to {exe_name}")

def main():
    current_folder = os.getcwd()
    output_folder = os.path.join(current_folder, "Executables")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file_name in os.listdir(current_folder):
        if file_name.endswith(".py") and file_name != "setup.py":
            file_path = os.path.join(current_folder, file_name)
            convert_to_exe(file_path, output_folder)

if __name__ == "__main__":
    main()
