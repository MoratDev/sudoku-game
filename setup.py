from setuptools import setup, find_packages

setup(
    name="sudoku-game",
    version="1.0.0",
    description="A complete Sudoku game with GUI using Pygame",
    author="Sudoku Game Developer",
    packages=find_packages(),
    install_requires=[
        "pygame>=2.6.0",
    ],
    entry_points={
        'console_scripts': [
            'sudoku-game=sudoku_pygame:main',
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Games/Entertainment :: Puzzle Games",
    ],
)