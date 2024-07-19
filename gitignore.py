import os
import shutil

def find_venv_folders(start_path='.',name=""):
    venv_folders = []
    
    for root, dirs, files in os.walk(start_path):
        for dir in dirs:
            if name in dir.lower():
                relative_path = os.path.relpath(os.path.join(root, dir), start_path)
                venv_folders.append(relative_path)
        
    return venv_folders

# Example usage
start_directory = '.'  # Current directory
venv_paths = find_venv_folders(start_directory,'venv')

print("Folders containing 'venv':")
for path in venv_paths:
    print(path)
# Example usage
start_directory = '.'  # Current directory
venv_paths = find_venv_folders(start_directory,'__pycache__')

for path in venv_paths:
    print(path)
    shutil.rmtree(path, ignore_errors=True)