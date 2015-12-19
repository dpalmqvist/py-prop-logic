from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import io
import os
import sys

import prop_logic

here = os.path.abspath(os.path.dirname(__file__))

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.md')

setup(
    name='prop_logic',
    version=prop_logic.__version__,
    url='http://github.com/dpalmqvist/prop_logic/',
    license='GPL',
    author='Daniel Palmqvist',
    author_email='daniel.u.palmqvist@gmail.com',
    description='Propositional logic engine implemented in Python',
    long_description=long_description,
    packages=['prop_logic'],
    include_package_data=True,
    platforms='any',
    test_suite='prop_logic.test.test',
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Environment :: Logic programming',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ]
)