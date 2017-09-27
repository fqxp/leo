#!/usr/bin/env python3

from setuptools import setup, find_packages
import os.path


here = os.path.abspath(os.path.dirname(__file__))


setup(
    name='leo',

    version='0.1',
    description='A dict.leo.org command line client',
    url='https://github.com/fqxp/leo',
    author='Frank Ploss',
    author_email='frank@fqxp.de',
    license='GPLv3',
    classifiers=[
        'Development Status :: 3 - Alpha',
    ],
    install_requires=[
        'colored',
        'requests',
        'xmltodict',
    ],
    py_modules=['leo'],
    entry_points={
        'console_scripts': [
            'leo=leo:main',
        ],
    },
)

