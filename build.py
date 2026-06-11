#!/usr/bin/env python3
"""
Build script to run all CadQuery scripts and export 3D-printable files.
"""

import os
import sys
import subprocess
import time

# ANSI color codes for rich console formatting
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
BOLD = "\033[1m"
RESET = "\033[0m"

SCRIPTS = [
    "glass-focusing-screen.py",
    "paper-focusing-screen.py"
]

def print_header():
    print(f"{BLUE}{BOLD}====================================================")
    print("      Mamiya Press Focusing Screen CAD Builder")
    print(f"===================================================={RESET}\n")

def check_dependencies():
    print(f"{BLUE}Checking environment...{RESET}")
    try:
        import cadquery
        print(f"  {GREEN}✓{RESET} CadQuery version: {cadquery.__version__}")
        return True
    except ImportError:
        print(f"  {RED}✗{RESET} CadQuery is not installed in this Python environment.")
        print(f"\n{YELLOW}To install CadQuery, run:{RESET}")
        print("  pip install -r requirements.txt")
        print(f"  or configure a conda environment.")
        return False

def clean_exports():
    import shutil
    export_dir = "exports"
    if os.path.exists(export_dir):
        print(f"{BLUE}Cleaning existing exports in '{export_dir}/'...{RESET}")
        try:
            shutil.rmtree(export_dir)
        except Exception as e:
            print(f"  {RED}Error cleaning directory: {e}{RESET}")
    os.makedirs(export_dir, exist_ok=True)

def run_script(script):
    print(f"\n{BOLD}{BLUE}Running script: {script}...{RESET}")
    if not os.path.exists(script):
        print(f"  {RED}Error: File '{script}' not found.{RESET}")
        return False
        
    start_time = time.time()
    result = subprocess.run([sys.executable, script], capture_output=True, text=True)
    elapsed = time.time() - start_time
    
    if result.returncode == 0:
        print(f"  {GREEN}✓{RESET} Successfully completed in {elapsed:.2f}s")
        if result.stdout:
            for line in result.stdout.strip().split("\n"):
                print(f"    {line}")
        return True
    else:
        print(f"  {RED}✗{RESET} Failed with exit code {result.returncode} in {elapsed:.2f}s")
        if result.stderr:
            print(f"    {RED}Error details:{RESET}")
            for line in result.stderr.strip().split("\n"):
                print(f"      {line}")
        return False

def report_exports():
    export_dir = "exports"
    if not os.path.exists(export_dir):
        print(f"\n{RED}No files exported.{RESET}")
        return
        
    files_found = []
    for root, dirs, files in os.walk(export_dir):
        for file in files:
            path = os.path.join(root, file)
            rel_path = os.path.relpath(path, export_dir)
            files_found.append((rel_path, path))
            
    if not files_found:
        print(f"\n{RED}No files exported.{RESET}")
        return
        
    print(f"\n{BOLD}{GREEN}Generated Assets in '{export_dir}/':{RESET}")
    print(f"{'-'*55}")
    print(f"{'Relative Filename':<35} | {'Size':<15}")
    print(f"{'-'*55}")
    for rel_path, path in sorted(files_found):
        size_bytes = os.path.getsize(path)
        if size_bytes > 1024 * 1024:
            size_str = f"{size_bytes / (1024 * 1024):.2f} MB"
        else:
            size_str = f"{size_bytes / 1024:.2f} KB"
        print(f"{rel_path:<35} | {size_str:<15}")
    print(f"{'-'*55}\n")

def main():
    print_header()
    
    # We allow the build to proceed even if verification fails, as the user might be building in another env
    cq_available = check_dependencies()
    if not cq_available:
        print(f"\n{YELLOW}Proceeding anyway, but script runs will likely fail unless CadQuery is installed.{RESET}")
        
    clean_exports()
    
    success_count = 0
    for script in SCRIPTS:
        if run_script(script):
            success_count += 1
            
    print(f"\n{BOLD}====================================================")
    if success_count == len(SCRIPTS):
        print(f"      {GREEN}Build Completed Successfully! ({success_count}/{len(SCRIPTS)}){RESET}")
    else:
        print(f"      {RED}Build Failed! ({success_count}/{len(SCRIPTS)} Succeeded){RESET}")
    print(f"{BOLD}===================================================={RESET}")
    
    if success_count > 0:
        report_exports()

if __name__ == "__main__":
    main()
