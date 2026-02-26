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
    import importlib
    
    # Special handling for tools directories - import as modules not files
    if "/tools/" in filepath and filepath.endswith(".py"):
        try:
            # Convert file path to module path
            # e.g., server/gti/gti_mcp/tools/files.py -> gti_mcp.tools.files
            parts = filepath.replace(".py", "").split("/")
            
            # Find the package name (gti_mcp, secops_mcp, etc)
            module_parts = []
            found_package = False
            for part in parts:
                if part in ["gti_mcp", "secops_mcp", "secops_soar_mcp", "scc_mcp"]:
                    found_package = True
                if found_package:
                    module_parts.append(part)
            
            if module_parts:
                # Add parent to sys.path temporarily
                server_dir = filepath.split("/" + module_parts[0])[0]
                if server_dir not in sys.path:
                    sys.path.insert(0, server_dir)
                
                module_name = ".".join(module_parts)
                importlib.import_module(module_name)
                return True
        except Exception as e:
            print(f"✗ {filepath}: {e}")
            return False
    
    # Default behavior for non-tools files
    try:
        spec = importlib.util.spec_from_file_location("temp_module", filepath)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return True
    except Exception as e:
        print(f"✗ {filepath}: {e}")
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
    # Files to skip
    skip_files = {"setup.py", "example.py", "conftest.py", "__init__.py"}
    
    python_files = []
    for root, dirs, files in os.walk(directory):
        # Skip test directories
        if "tests" in root or "__pycache__" in root:
            continue
            
        for file in files:
            if file.endswith(".py") and file not in skip_files:
                python_files.append(os.path.join(root, file))
    return python_files


def main():
    """Main function to test all Python files in server directories."""
    # Test all Python files in server directories
    server_dirs = ["server/gti", "server/scc", "server/secops", "server/secops-soar"]
    failed_files = []
    total_files = 0

    for server_dir in server_dirs:
        if os.path.exists(server_dir):
            python_files = find_python_files(server_dir)
            total_files += len(python_files)
            print(f"Testing {len(python_files)} Python files in {server_dir}...")
            
            for py_file in python_files:
                if not test_python_file(py_file):
                    failed_files.append(py_file)

    print(f"\nTested {total_files} Python files total")
    if failed_files:
        print(f"\n{len(failed_files)} files failed import tests:")
        for failed_file in failed_files:
            print(f"  - {failed_file}")
        return 1
    else:
        print("✓ All Python files import successfully")
        return 0


if __name__ == "__main__":
    sys.exit(main())