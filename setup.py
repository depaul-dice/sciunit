#!/usr/bin/env python
import version
import os
import subprocess
import gzip
from setuptools import setup, find_packages
from setuptools.command.build_py import build_py


def localopen(fname):
    return open(os.path.join(os.path.dirname(__file__), fname))


class BuildCommand(build_py):
    def run(self):
        subprocess.check_call(['cmake', '-DCMAKE_BUILD_TYPE=Release'])
        subprocess.check_call(['make', '-j4'])
        build_py.run(self)
        _build_manpage('docs/sciunit.1.rst', 'sciunit.1.gz')


def _build_manpage(src, target):
    from docutils.core import publish_file
    from docutils.writers import manpage

    with gzip.open(target, 'wb') as f:
        publish_file(source_path=src,
                     destination=f,
                     writer=manpage.Writer())

setup(
    name='sciunit2',
    version=version.get_version(),
    description='Sciunit command line',
    author='Zhihao Yuan',
    author_email='zhihao.yuan@depaul.edu',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    license='BSD',
    keywords=['sciunit'],
    url='https://bitbucket.org/geotrust/sciunit2/src',
    long_description=localopen('README.rst').read(),
    setup_requires=['docutils'],
    install_requires=localopen('requirements.txt').readlines(),
    tests_require=localopen('test-requirements.txt').readlines(),
    cmdclass={'build_py': BuildCommand},
    entry_points={'console_scripts': ['sciunit=sciunit2.cli:main']},
    data_files=[('man/man1', ['sciunit.1.gz'])],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Intended Audience :: Science/Research',
    ]
)
