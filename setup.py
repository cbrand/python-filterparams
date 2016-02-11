# -*- encoding: utf-8 -*-

from setuptools import setup, find_packages

requires = [
    'funcparserlib>=0.3.6',
    'Werkzeug',
]

VERSION = '1.0.0'

setup(
    name='filterparams',
    version=VERSION,
    description='Filterparams',
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.4",
    ],
    author='Christoph Brand',
    author_email='christoph@brand.rest',
    keywords=[],
    packages=find_packages('src'),  # include all packages under src
    package_dir={'': 'src'},  # tell distutils packages are under src
    namespace_packages=[],
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    url='https://github.com/cbrand/python-filterparams',
    download_url='https://github.com/cbrand/python-filterparams/tarball/%s' % VERSION,
    entry_points={
        'console_scripts': [
        ]
    },
)
