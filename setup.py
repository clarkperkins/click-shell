import io
import os

from setuptools import setup, find_packages


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with io.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            # __version__ = "0.9"
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


SHORT_DESCRIPTION = "An extension to click that easily turns your click app into a shell utility"

# Use the README.md as the long description
LONG_DESCRIPTION = read('README.rst')

requirements = [
    'click>=6.0',
]

setup(
    name='click-shell',
    version=get_version('click_shell/__init__.py'),
    url="https://github.com/clarkperkins/click-shell",
    author="Clark Perkins",
    author_email="r.clark.perkins@gmail.com",
    description=SHORT_DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    license='BSD',
    include_package_data=True,
    packages=find_packages(),
    zip_safe=False,
    install_requires=requirements,
    dependency_links=[],
    extras_require={
        'readline': ['gnureadline'],
        'windows': ['pyreadline'],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: User Interfaces',
        'Topic :: System :: Shells',
        'Topic :: Utilities',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ]
)
