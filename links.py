import os
import sys

def ensure_pypim_links():
    """Create necessary symbolic links for PyPIM"""
    project_root = os.path.dirname(os.path.abspath(__file__))
    pypim_dir = os.path.join(project_root, 'pypim')
    if not os.path.exists(pypim_dir):
        os.makedirs(pypim_dir)
    source_lib = os.path.join(project_root, 'PyPIM', 'pypim', 'libsimulator.so')
    target_lib = os.path.join(pypim_dir, 'libsimulator.so')
    source_driver = os.path.join(project_root, 'PyPIM', 'pypim', 'driver.cpython-310-x86_64-linux-gnu.so')
    target_driver = os.path.join(pypim_dir, 'driver.cpython-310-x86_64-linux-gnu.so')
    if not os.path.exists(source_lib):
        print(f"Error: Source library {source_lib} does not exist")
        return False
        
    if not os.path.exists(source_driver):
        print(f"Warning: Source driver {source_driver} does not exist")
    if not os.path.exists(target_lib):
        os.symlink(source_lib, target_lib)
        print(f"Created symbolic link: {target_lib} -> {source_lib}")
        
    if os.path.exists(source_driver) and not os.path.exists(target_driver):
        os.symlink(source_driver, target_driver)
        print(f"Created symbolic link: {target_driver} -> {source_driver}")
    
    return True

if __name__ == "__main__":
    ensure_pypim_links()