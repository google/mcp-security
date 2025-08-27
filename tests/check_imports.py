#!/usr/bin/env python3
"""
Import validation script for CI/CD pipeline.

This script tests all Python files in server directories to catch import errors
and syntax issues that could break production deployments.
"""

import os
import sys
import importlib.util


def test_python_file(filepath):
    """
    Test if a Python file can be imported without errors.
    
    Args:
        filepath: Path to the Python file to test
        
    Returns:
        bool: True if import succeeds, False otherwise
    """
    try:
        spec = importlib.util.spec_from_file_location('temp_module', filepath)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return True
    except Exception as e:
        print(f'✗ {filepath}: {e}')
        return False
    return True


def find_python_files(directory):
    """
    Recursively find all Python files in a directory.
    
    Args:
        directory: Directory to search
        
    Returns:
        list: List of Python file paths
    """
    python_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    return python_files


def main():
    """Main function to test all Python files in server directories."""
    # Test all Python files in server directories
    server_dirs = ['server/gti', 'server/scc', 'server/secops', 'server/secops-soar']
    failed_files = []
    total_files = 0

    for server_dir in server_dirs:
        if os.path.exists(server_dir):
            python_files = find_python_files(server_dir)
            total_files += len(python_files)
            print(f'Testing {len(python_files)} Python files in {server_dir}...')
            
            for py_file in python_files:
                if not test_python_file(py_file):
                    failed_files.append(py_file)

    print(f'\nTested {total_files} Python files total')
    if failed_files:
        print(f'\n{len(failed_files)} files failed import tests:')
        for failed_file in failed_files:
            print(f'  - {failed_file}')
        return 1
    else:
        print('✓ All Python files import successfully')
        return 0


if __name__ == "__main__":
    sys.exit(main())