# coding: utf-8
from setuptools import find_packages, setup


setup(
    name='idea',
    version='0.1.0',
    url='https://github.com/piratus/idea',
    license='WTFPL',
    author='Andrew Popovych',
    author_email='piratus@gmail.com',
    description='IntelliJ IDEA helper tool',
    packages=find_packages(),
    package_data={
        'idea': ['module_tpl.xml'],
    },
    install_requires=[
        'click',
        'jinja2',
        'lxml',
    ],
    entry_points={
        'console_scripts': [
            'ide = idea.__main__:cli',
        ],
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: Freeware',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development',
    ],
)
