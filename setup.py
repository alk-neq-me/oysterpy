from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()


AUTHOR = 'Aung Koko Lwin'
DESCRIPTION = 'Python library providing Result and Option types inspired by Rust'
URL = 'https://github.com/alk-neq-me/oysterpy'
EMAIL = "toyko2001@gmail.com"
VERSION = "0.1.0"

# Setup configuration
setup(
    author=AUTHOR,
    version=VERSION,
    description=DESCRIPTION,
    url=URL,
    author_email=EMAIL,
    install_requires=[],
    license='MIT',
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

# python setup.py sdist bdist_wheel
