"""Project Setup"""

from setuptools import setup
import config

with open("README.md", 'r') as f:
    long_description = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name=config.settings.name,
    version=config.settings.version,
    packages=config.settings.packages,
    url=config.settings.url,
    description=config.settings.description,
    long_description=long_description,
    python_requires=config.settings.python_requires,
    license=license,
)