from setuptools import setup, find_packages, Command
import os
import sys
import subprocess
import shutil
from distutils.command.build import build
from setuptools.command.install import install
from setuptools.command.develop import develop

def check_dependencies():
    nvcc_present = shutil.which('nvcc') is not None
    if not nvcc_present:
        print("ERROR: NVIDIA CUDA compiler (nvcc) not found. Please install CUDA Toolkit.")
        return False
    gcc10_present = shutil.which('gcc-10') is not None
    if not gcc10_present:
        print("ERROR: GCC 10 not found. Please install gcc-10.")
        return False
    
    return True

class InstallPyPIM(Command):
    description = "Install PyPIM submodule"
    user_options = []
    
    def initialize_options(self):
        pass
        
    def finalize_options(self):
        pass
        
    def run(self):
        if not check_dependencies():
            sys.exit(1)
            
        project_root = os.path.dirname(os.path.abspath(__file__))
        pypim_dir = os.path.join(project_root, 'PyPIM')
        
        if not os.path.exists(pypim_dir):
            print(f"ERROR: PyPIM directory not found at {pypim_dir}")
            sys.exit(1)
        
        print("Building and installing PyPIM...")
        try:
            env = os.environ.copy()
            env["CC"] = "gcc-10"
            env["CXX"] = "g++-10"
            subprocess.run(
                ["pip", "install", "-e", "."], 
                cwd=pypim_dir, 
                check=True,
                env=env
            )
            self.create_symlinks()
            
            print("PyPIM installation successful.")
        except subprocess.CalledProcessError as e:
            print(f"ERROR: Failed to install PyPIM: {e}")
            sys.exit(1)
    
    def create_symlinks(self):
        """Create necessary symbolic links for PyPIM libraries"""
        project_root = os.path.dirname(os.path.abspath(__file__))
        pypim_dir = os.path.join(project_root, 'PyPIM', 'pypim')
        target_dir = os.path.join(project_root, 'pypim')
        os.makedirs(target_dir, exist_ok=True)
        libraries = [
            'libsimulator.so',
            *[f for f in os.listdir(pypim_dir) if f.startswith('driver.') and f.endswith('.so')]
        ]
        
        for lib in libraries:
            source = os.path.join(pypim_dir, lib)
            target = os.path.join(target_dir, lib)
            if os.path.exists(source) and not os.path.exists(target):
                print(f"Creating symbolic link: {target} -> {source}")
                os.symlink(source, target)

class BuildWithPyPIM(build):
    def run(self):
        self.run_command('install_pypim')
        build.run(self)

class InstallWithPyPIM(install):
    def run(self):
        self.run_command('install_pypim')
        install.run(self)

class DevelopWithPyPIM(develop):
    def run(self):
        self.run_command('install_pypim')
        develop.run(self)

setup(
    name="nocktensors",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["numpy"],
    python_requires=">=3.6",
    description="Emulated processing-in-memory stack-based CUDA Nock interpreter using PyPIM",
    author="~sitful-hatred",
    author_email="reid@nativeplanet.io",
    cmdclass={
        'install_pypim': InstallPyPIM,
        'build': BuildWithPyPIM,
        'install': InstallWithPyPIM,
        'develop': DevelopWithPyPIM,
    },
)