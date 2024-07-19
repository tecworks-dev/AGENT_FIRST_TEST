import sys

def get_python_environment_directory():
    """
    Returns the directory containing the Python executable,
    which is indicative of the active Python environment.
    """
    return sys.exec_prefix

# Let's call the function and print the result
env_dir = get_python_environment_directory()
print(sys.exec_prefix)

def get_python_library_directory():
    """
    Returns the directory where the Python standard libraries are stored.
    This directory is typically included in the sys.path variable.
    """
    # sys.path contains a list of directories where Python looks for modules.
    # The first entry is typically the path to the standard library.
    for path in sys.path:
        if '\\lib' in path:
            return path
    for path in sys.path:
        if '/lib' in path:
            return path
    
    return None  # Return None if no typical lib directory is found

# Let's call the function and print the result
lib_dir = get_python_library_directory()
print("Python Library Directory:", lib_dir)
print(sys.path)