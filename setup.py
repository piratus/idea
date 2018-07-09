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
    include_package_data=True,
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
)
