# File: setup.py
# Path: setup.py
# Standard: AIDEV-PascalCase-1.6
# Created: March 22, 2025
# Last Modified: March 22, 2025  8:50 PM
# Description: Installation script for DocumentRenamer

"""
Installation script for the DocumentRenamer package.

This script configures package metadata and entry points for installation.
"""

from setuptools import setup, find_packages

setup(
    name="AIDEV-DocManager",
    version="0.1.0",
    description="Document management tool for Project Himalaya",
    author="Herbert J. Bowers",
    author_email="herb@bowersworld.com",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        # tkinter is part of standard Python library
    ],
    entry_points={
        "console_scripts": [
            "document-renamer=ProjectHimalaya.DocumentRenamer:Main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
