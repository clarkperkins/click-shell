
from setuptools import setup, find_packages

# Set version
__version__ = '0.0.0'  # Explicit default
with open('click_shell/version.py') as f:
    exec(f.read())


SHORT_DESCRIPTION = 'An extension to click that easily turns your click app into a shell utility'

# Use the README.md as the long description
with open('README.rst') as f:
    LONG_DESCRIPTION = f.read()

requirements = [
    'click>=6.0',
]


setup(
    name='click-shell',
    version=__version__,
    url='https://github.com/clarkperkins/click-shell',
    author='Clark Perkins',
    author_email='r.clark.perkins@gmail.com',
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
        'Development Status :: 3 - Alpha',
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
