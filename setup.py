from setuptools import setup, find_packages

setup(
    name="dustman",
    version="1.0.0",
    description="A modular CLI system cleaner with interactive TUI",
    packages=find_packages(),
    py_modules=["main"],
    install_requires=[
        "questionary",
        "prompt_toolkit",
    ],
    entry_points={
        "console_scripts": [
            "dustman=main:main",
        ],
    },
)