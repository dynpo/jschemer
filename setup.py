"""Setup module for dynpojschemer"""

import setuptools
import os


with open('README.md', 'r') as fh:
    long_description = fh.read()


setuptools.setup(
    name='dynpojschemer',
    version='0.0.1-alpha.0',
    author='Bruno Manesco',
    author_email='bmanesco@gmail.com',
    description='A python package that dynamically generates json sample from jschema.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/dynpo/jschemer',
    packages=setuptools.find_packages(),
    install_requires=[
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)
