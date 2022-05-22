'''Project Setup'''

import os
import sys
from setuptools import setup, find_packages, Distribution
import versioneer
from setuptools.command.install import install

with open('README.md', 'r') as f:
    long_description = f.read()

with open('LICENSE') as f:
    license = f.read()


class BinaryDistribution(Distribution):

    def has_ext_modules(self):
        '''Forces binary package with platform name

        Distribution which always forces a binary package with platform name

        :return: bool
        '''

        return True


class VerifyVersionCommand(install):
    '''Verify GIT tag against the version

    Verify that the git tag matches our package version

    :param install: setuptools install
    '''

    description = 'verify that the git tag matches our package version'

    def run(self):
        version = versioneer.get_version()
        tag = os.getenv('CIRCLE_TAG')

        if tag != version:
            sys.exit(
                f'Failed version verification: "{tag}" does not match the version of this app: "{version}"'
            )


install_requires = ["wheel", "pythonnet==2.5.2", "pydantic>=1.9.0", "loguru>=0.6.0", "pillow>=9.1.0", "versioneer"]

cmdclass = {
    "verify_version": VerifyVersionCommand,
}
cmdclass.update(versioneer.get_cmdclass())

setup(
    name='flaui-uiautomation-wrapper',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author='Amruth VVKP',
    author_email='amruthvvkp@gmail.com',
    url='https://github.com/amruthvvkp/flaui-uiautomation-wrapper',
    description=
    'Tool to perform UI Automation on Windows desktop applications using an underlying FlaUI wrapper.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.7, !=3.9, != 3.10',
    packages=find_packages("src"),
    package_dir={"": "src"},   # tell distutils packages are under src
    package_data={
        # If any package contains *.dll files, include them:
        "": ["*.dll"],
    },
    include_package_data=True,
    install_requires=install_requires,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: Microsoft',
        'Topic :: Software Development :: Testing',
        'Intended Audience :: Developers'
    ],
    distclass=BinaryDistribution,
    platforms=['Windows'],
    license='LGPLv3')