import os, sys
from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

def read_requirements():
    """Parse requirements from requirements.txt."""
    reqs_path = os.path.join('.', 'requirements.txt')
    with open(reqs_path, 'r') as f:
        requirements = [line.rstrip() for line in f]
    return requirements

setup(
    name='pgeotools',
    version='0.0.1',
    description='Private package for geophisical works',
    long_description=readme,
    author='Hironori Otsuka',
    author_email='hotsuka@eri.u-tokyo.ac.jp',
    install_requires=read_requirements(),
    url='https://github.com/pirotan628/pgeotools',
    license=license,
    packages=find_packages(exclude=('tests', 'docs','cmdtools'))
)