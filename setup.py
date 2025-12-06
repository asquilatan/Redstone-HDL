import os
import sys
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext

# Try to import pybind11, but don't fail if it's not available for C++ build
try:
    import pybind11
    PYBIND11_AVAILABLE = True
except ImportError:
    PYBIND11_AVAILABLE = False

class get_pybind11_include:
    def __str__(self):
        if PYBIND11_AVAILABLE:
            return pybind11.get_include()
        return ''

class BuildExtOptional(build_ext):
    """Allow C++ extension to fail gracefully"""
    def run(self):
        try:
            build_ext.run(self)
        except Exception:
            print("WARNING: C++ extension failed to build. Using Python fallback.")
    
    def build_extension(self, ext):
        try:
            build_ext.build_extension(self, ext)
        except Exception:
            print(f"WARNING: Failed to build {ext.name}. Using Python fallback.")

# Only include C++ extension if pybind11 is available
ext_modules = []
if PYBIND11_AVAILABLE and os.environ.get('REDSCRIPT_BUILD_CPP', '0') == '1':
    ext_modules = [
        Extension(
            'redscript.solver._solver',
            [
                'src/cpp/bindings.cpp',
                'src/cpp/solver.cpp',
                'src/cpp/constraints/qc.cpp',
            ],
            include_dirs=[get_pybind11_include()],
            language='c++',
            extra_compile_args=['-std=c++17'] if sys.platform != 'win32' else ['/std:c++17'],
        ),
    ]

setup(
    name='redscript',
    version='0.1.0a1',
    author='Redstone HDL Contributors',
    description='A Minecraft Redstone HDL compiler',
    packages=['redscript', 'redscript.compiler', 'redscript.solver', 'redscript.viewer', 'redscript.cli', 'redscript.utils'],
    package_dir={'': 'src'},
    ext_modules=ext_modules,
    cmdclass={'build_ext': BuildExtOptional},
    install_requires=[
        'lark>=1.1.0',
        'ursina>=5.0.0',
        'litemapy>=0.4.0',
        'numpy>=1.24.0',
    ],
    entry_points={
        'console_scripts': [
            'redscript=redscript.cli.main:main',
        ],
    },
    python_requires='>=3.11',
)
