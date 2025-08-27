import os
import pytest
import importlib.util

def find_python_files(start_path):
    """Recursively find all Python files in a directory."""
    py_files = []
    for root, _, files in os.walk(start_path):
        for file in files:
            if file.endswith(".py"):
                py_files.append(os.path.join(root, file))
    return py_files

def get_module_name_from_path(path, root_dir):
    """Convert a file path to a Python module name."""
    rel_path = os.path.relpath(path, root_dir)
    module_path = os.path.splitext(rel_path)[0]
    return module_path.replace(os.path.sep, '.')

SERVER_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'server'))
PYTHON_FILES = find_python_files(SERVER_DIR)

@pytest.mark.parametrize("py_file", PYTHON_FILES)
def test_import_file(py_file):
    """Test that a Python file can be imported without errors."""
    module_name = get_module_name_from_path(py_file, os.path.abspath(os.path.join(SERVER_DIR, '..')))

    # Skip __init__.py files if they are empty or just contain comments
    if os.path.basename(py_file) == '__init__.py':
        with open(py_file, 'r') as f:
            content = f.read().strip()
            if not content or all(line.strip().startswith('#') for line in content.splitlines()):
                pytest.skip(f"Skipping empty or comment-only __init__.py: {module_name}")

    try:
        spec = importlib.util.spec_from_file_location(module_name, py_file)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        else:
            pytest.fail(f"Could not create module spec for {py_file}")
    except Exception as e:
        pytest.fail(f"Failed to import {module_name} from {py_file}: {e}")
