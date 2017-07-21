#!/usr/bin/env python
import os
from setuptools import setup


def localopen(fname):
    return open(os.path.join(os.path.dirname(__file__), fname))


setup(
    name='sciunit2',
    version='0.1',
    description='sciunit command line',
    author='Zhihao Yuan',
    author_email='lichray@gmail.com',
    packages=["sciunit2"],
    zip_safe=False,
    license='ASL 2.0',
    keywords=['sciunit2'],
    url='https://github.com/lichray/moecache',
    long_description=localopen('README.md').read(),
    install_requires=localopen('requirements.txt').readlines(),
    tests_require=localopen('test-requirements.txt').readlines(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy',
    ]
)
