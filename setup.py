import os

from setuptools import setup

version = {}
with open(os.path.join('adefa', '__init__.py'), 'r') as f:
    exec(f.read(), version)

with open('requirements.txt', 'r') as f:
    reqs = f.read().splitlines()

setup(
    name='adefa',
    version=version['__version__'],
    url='https://github.com/butomo1989/adefa',
    description='AWS Device Farm CLI',
    author='Budi Utomo',
    author_email='budi.ut.1989@gmail.com',
    keywords='AWS Devicefarm CLI',
    install_requires=reqs,
    py_modules=['cli', 'utils'],
    entry_points={'console_scripts': 'adefa=adefa.cli:cli'}
)
