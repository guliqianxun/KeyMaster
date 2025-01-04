from setuptools import setup, find_packages
import os

def collect_data_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append((os.path.join(path, filename), os.path.relpath(path, '.')))
    return paths

setup(
    name='keyboard-master',
    version='0.50',
    description='Keyboard Master Application',
    author='Zhiheng Liu',
    author_email='visitorindark@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    data_files=collect_data_files('Resources'),
    entry_points={
        'console_scripts': [
            'keyboard-master=main:main',  # Assuming main.py has a main() function
        ],
    },
    install_requires=[
        # List your dependencies here
    ],
    package_data={
        '': ['Resources/keyboard.ico'],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)