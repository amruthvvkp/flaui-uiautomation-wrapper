from pydantic import BaseSettings
from setuptools import setup, find_packages


class APISettings(BaseSettings):
    version = '0.0.1'
    title = 'Aladdin API'
    description = 'API model for Aladdin'


class Settings(BaseSettings):
    name = 'aladdin'
    version = '0.0.1'
    url = 'https://github.com/amruthvvkp/flaui-uiautomation-wrapper'
    description = 'Tool to perform UI Automation on Windows desktop applications using an underlying Fla-UI wrapper.'
    python_requires = '>=3.8'
    packages = find_packages(include=('src', 'tests'))
    api_settings: APISettings = APISettings()


settings = Settings()