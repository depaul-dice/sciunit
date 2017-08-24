#!/usr/bin/env python
import os
from setuptools import setup


def localopen(fname):
    return open(os.path.join(os.path.dirname(__file__), fname))


setup(
    name='sciunit2',
    version='0.1',
    description='Sciunit command line',
    author='Zhihao Yuan',
    author_email='zhihao.yuan@depaul.edu',
    packages=["sciunit2"],
    zip_safe=False,
    license='BSD',
    keywords=['sciunit'],
    url='https://bitbucket.org/geotrust/sciunit2/src',
    long_description=localopen('README.rst').read(),
    install_requires=localopen('requirements.txt').readlines(),
    tests_require=localopen('test-requirements.txt').readlines(),
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Intended Audience :: Science/Research',
    ]
)
