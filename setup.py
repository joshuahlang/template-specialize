# Licensed under the MIT License
# https://github.com/craigahobbs/template-specialize/blob/master/LICENSE

import re
import os

from setuptools import setup

PACKAGE_NAME = 'template-specialize'
MODULE_NAME = 'template_specialize'

TESTS_REQUIRE = [
    'botocore >= 1.0.0'
]

def main():
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'src', MODULE_NAME, '__init__.py'), encoding='utf-8') as init_file:
        version = re.search(r"__version__ = '(.+?)'", init_file.read()).group(1)
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.md'), encoding='utf-8') as readme_file:
        long_description = readme_file.read()

    setup(
        name=PACKAGE_NAME,
        description=('Recursive template file specializer.'),
        long_description=long_description,
        long_description_content_type='text/markdown',
        version=version,
        author='Craig Hobbs',
        author_email='craigahobbs@gmail.com',
        keywords='template specialize',
        url='https://github.com/craigahobbs/template-specialize',
        license='MIT',
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Topic :: Utilities'
        ],
        package_dir={'': 'src'},
        packages=[MODULE_NAME],
        install_requires=[
            'jinja2 >= 2.10',
            'pyyaml >= 3.13'
        ],
        entry_points={
            'console_scripts': [PACKAGE_NAME + ' = ' + MODULE_NAME + '.main:main'],
        },
        test_suite='tests',
        tests_require=TESTS_REQUIRE,
        extras_require={
            'tests': TESTS_REQUIRE
        }
    )

if __name__ == '__main__':
    main()
