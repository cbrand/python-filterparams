# -*- encoding: utf-8 -*-

import sys

from setuptools import setup, find_packages
from distutils.command.build_py import build_py as _build_py


setup_requires = []

requires = [
    'funcparserlib>=0.3.6',
    'Werkzeug',
]

VERSION = '1.0.0'

cmd_class = {}


def match_patterns(path, pattern_list=[]):
    from fnmatch import fnmatch
    for pattern in pattern_list:
        if fnmatch(path, pattern):
            return True
    return False


class build_py27(_build_py):
    def __init__(self, *args, **kwargs):
        _build_py.__init__(self, *args, **kwargs)
        import logging
        import pip
        pip.main(['install', '3to2'])

        from lib2to3 import refactor
        import lib3to2.main
        rt_logger = logging.getLogger("RefactoringTool")
        rt_logger.addHandler(logging.StreamHandler())
        fixers = refactor.get_fixers_from_package('lib3to2.fixes')
        self.rtool = lib3to2.main.StdoutRefactoringTool(
            fixers,
            None,
            [],
            False,
            False
        )

    def copy_file(self, source, target, preserve_mode=True):
        if source.endswith('.py'):
            try:
                print("3to2 converting: %s => %s" % (source, target))
                with open(source, 'rt') as input:
                    # ensure file contents have trailing newline
                    source_content = input.read() + "\n"
                    nval = self.rtool.refactor_string(source_content, source)
                if nval is not None:
                    with open(target, 'wt') as output:
                        output.write('from __future__ import print_function\n')
                        output.write(str(nval))
                else:
                    raise(Exception("Failed to parse: %s" % source))
            except Exception as e:
                print("3to2 error (%s => %s): %s" % (source,target,e))


if sys.version_info[0] < 3:
    setup_requires.append('pip')
    cmd_class['build_py'] = build_py27

package_dir = {
    '': 'src',
}
packages = find_packages('src')
if 'nosetests' in sys.argv:
    packages += find_packages('test')
    packages = [
        item
        for item in packages
        if item != 'tests'
    ]
    package_dir['tests'] = 'test/tests'

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
    cmdclass=cmd_class,
    keywords=[],
    packages=packages,  # include all packages under src
    package_dir=package_dir,  # tell distutils packages are under src
    namespace_packages=[],
    include_package_data=True,
    zip_safe=False,
    setup_requires=setup_requires,
    install_requires=requires,
    url='https://github.com/cbrand/python-filterparams',
    download_url='https://github.com/cbrand/python-filterparams/tarball/%s' % VERSION,
    entry_points={
        'console_scripts': [
        ]
    },
)
