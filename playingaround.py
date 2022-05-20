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


install_requires = open('requirements.txt').read().strip().split('\n')
dev_requires = open('dev-requirements.txt').read().strip().split('\n')
test_requires = open('test-requirements.txt').read().strip().split('\n')

cmdclass = {
    "verify_version": VerifyVersionCommand,
}
cmdclass.update(versioneer.get_cmdclass())

extras = {
    "dev": dev_requires + test_requires,
}

extras["all_extras"] = sum(extras.values(), [])
