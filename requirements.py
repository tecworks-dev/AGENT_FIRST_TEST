import os
import ast
import requests
from collections import defaultdict
import shutil


from stdlib_list import stdlib_list

def get_imports(file_path):
    """
    Extracts all unique external import statements from a Python file.
    
    Args:
    file_path (str): The path to the Python file to scan.
    
    Returns:
    set: A set of unique imports from the file.
    """
    encodings = ['utf-8', 'latin-1', 'ascii']
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                tree = ast.parse(file.read())
            
            imports = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.add(alias.name.split('.')[0])
                elif isinstance(node, ast.ImportFrom):
                    if node.module and node.level == 0:
                        imports.add(node.module.split('.')[0])
            
            return imports
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"Error processing file {file_path}: {str(e)}")
            return set()
    
    print(f"Warning: Unable to read file {file_path} with any of the attempted encodings.")
    return set()

def check_pypi(package):
    """
    Checks if a package exists on PyPI.
    
    Args:
    package (str): The package name to check.
    
    Returns:
    bool: True if the package exists, False otherwise.
    """
    try:
        response = requests.get(f"https://pypi.org/pypi/{package}/json")
        return response.status_code == 200
    except requests.RequestException:
        print(f"Warning: Unable to check PyPI for package {package}. Assuming it exists.")
        return True

def scan_folder(folder_path, FOLDERS_TO_EXCLUDE=None):
    """
    Scans a folder for Python files and extracts all unique imports.
    
    Args:
    folder_path (str): The path to the folder to scan.
    FOLDERS_TO_EXCLUDE (list, optional): A list of directory names to exclude from the scan.
    
    Returns:
    defaultdict(set): A dictionary with keys as package names and values as sets of file paths.
    """
    all_imports = defaultdict(set)
    python_std_lib = set(stdlib_list('3.8'))  # Change '3.8' to your Python version as necessary
    
    for root, dirs, files in os.walk(folder_path):
        if FOLDERS_TO_EXCLUDE is not None:
            dirs[:] = [d for d in dirs if d not in FOLDERS_TO_EXCLUDE]
            
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                imports = get_imports(file_path)
                filtered_imports = {imp for imp in imports if imp not in python_std_lib}
                for imp in filtered_imports:
                    all_imports[imp].add(file_path)
    
    return all_imports

def create_requirements(imports):
    """
    Creates a list of requirements from a set of imports, checking against PyPI.
    
    Args:
    imports (defaultdict(set)): A dictionary with keys as package names and values as sets of file paths.
    
    Returns:
    list: A sorted list of packages that exist on PyPI.
    """
    requirements = []
    manual_conversions = { ... }  # Keep existing mappings as is
    
    for imp, files in imports.items():
        package = manual_conversions.get(imp, imp)
        if check_pypi(package):
            requirements.append(package)
    
    return sorted(set(requirements))

def create_requirements(imports):
    requirements = []
    manual_conversions = {
        'cv2': 'opencv-python',
        'PIL': 'pillow',
        'sklearn': 'scikit-learn',
        'yaml': 'PyYAML',
        'np': 'numpy',
        'pd': 'pandas',
        'plt': 'matplotlib',
        'scipy': 'scipy',
        'tf': 'tensorflow',
        'torch': 'torch',
        'keras': 'keras',
        'sklearn': 'scikit-learn',
        'skimage': 'scikit-image',
        'bs4': 'beautifulsoup4',
        'nx': 'networkx',
        'sns': 'seaborn',
        'nltk': 'nltk',
        'gensim': 'gensim',
        'sympy': 'sympy',
        'pypdf2': 'PyPDF2',
        'openpyxl': 'openpyxl',
        'xlrd': 'xlrd',
        'xlwt': 'xlwt',
        'lxml': 'lxml',
        'scrapy': 'Scrapy',
        'flask': 'Flask',
        'django': 'Django',
        'sqlalchemy': 'SQLAlchemy',
        'psycopg2': 'psycopg2-binary',
        'pymongo': 'pymongo',
        'redis': 'redis',
        'pika': 'pika',
        'celery': 'celery',
        'pytest': 'pytest',
        'unittest': 'unittest2',
        'selenium': 'selenium',
        'requests_html': 'requests-html',
        'dash': 'dash',
        'plotly': 'plotly',
        'bokeh': 'bokeh',
        'pydot': 'pydot',
        'graphviz': 'graphviz',
        'pyyaml': 'PyYAML',
        'ujson': 'ujson',
        'fastapi': 'fastapi',
        'pydantic': 'pydantic',
        'uvicorn': 'uvicorn',
        'gunicorn': 'gunicorn',
        'aiohttp': 'aiohttp',
        'asyncio': 'asyncio',
        'cython': 'Cython',
        'numba': 'numba',
        'joblib': 'joblib',
        'dask': 'dask',
        'xgboost': 'xgboost',
        'lightgbm': 'lightgbm',
        'catboost': 'catboost',
        'spacy': 'spacy',
        'gym': 'gym',
        'pyqt5': 'PyQt5',
        'pyspark': 'pyspark',
        'boto3': 'boto3',
        'paramiko': 'paramiko',
        'cryptography': 'cryptography',
        'pycrypto': 'pycrypto',
        'bcrypt': 'bcrypt',
        'jwt': 'PyJWT',
        'faker': 'Faker',
        'tqdm': 'tqdm',
        'ipython': 'ipython',
        'jupyter': 'jupyter',
        'click': 'click',
        'typer': 'typer',
        'streamlit': 'streamlit',
        'pynput': 'pynput',
        'pyautogui': 'PyAutoGUI',
        'pendulum': 'pendulum',
        'arrow': 'arrow',
        'loguru': 'loguru',
    }
    
    for imp, files in imports.items():
        package = manual_conversions.get(imp, imp)
        if check_pypi(package):
            requirements.append(package)
        # else:
        #     print(f"Warning: {package} not found on PyPI. Used in: {', '.join(files)}")
    
    return requirements

def do_requirements(folder_path, FOLDERS_TO_EXCLUDE=None):
    if os.path.exists(os.path.join(folder_path, '.venv')):
        shutil.rmtree(os.path.join(folder_path, '.venv'))
    # folder_path = input("Enter the folder path to scan: ")
    imports = scan_folder(folder_path, FOLDERS_TO_EXCLUDE)
    requirements = create_requirements(imports)
    
    with open(folder_path + '/requirements.txt', 'w') as f:
        for req in sorted(requirements):
            f.write(f"{req}\n")
            print(req)
    
    print("requirements.txt has been created.")
    

def main():
    FOLDERS_TO_EXCLUDE = ['node_modules', 'venv', '.venv', 'env', '.env', 'build', '.system']
    folder_path = input("Enter the folder path to scan: ")
    imports = scan_folder(folder_path, FOLDERS_TO_EXCLUDE)
    requirements = create_requirements(imports)
    
    with open(f"{folder_path}/requirements.txt", 'w') as f:
        for req in sorted(requirements):
            f.write(f"{req}\n")
    
    print("requirements.txt has been created.")


if __name__ == "__main__":
    main()