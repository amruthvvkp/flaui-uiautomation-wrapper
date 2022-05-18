from pydantic import BaseSettings
from setuptools import find_packages

class Settings(BaseSettings):
    name = 'flaui-uiautomation-wrapper'
    version = '0.0.1'
    author ='Amruth VVKP'
    author_email = 'amruthvvkp@gmail.com'
    url = 'https://github.com/amruthvvkp/flaui-uiautomation-wrapper'
    description = 'Tool to perform UI Automation on Windows desktop applications using an underlying FlaUI wrapper.'
    python_requires = '>=3.7'
    packages = find_packages(include=('src', 'tests'))
    

settings = Settings()