from __future__ import with_statement
from setuptools import setup, find_packages

version = {}  # will be set by exec below

with open('marcholdings/version.py', 'rb') as fp:
    exec(fp.read(), version)

setup(
    name='marcholdings',
    version=version['__version__'],
    packages=find_packages(),
    author='Health Sciences Library System, University of Pittsburgh',
    author_email='speargh@pitt.edu',
    maintainer='Geoffrey Spear',
    maintainer_email='speargh@pitt.edu',
    url='http://www.github.com/pitthsls/marcholdings',
    description='Parse NISO Z39.71 textual holdings',
    long_description='',
    keywords='library MARC holdings Z39.71',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        ],
    )
