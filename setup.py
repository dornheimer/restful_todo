from setuptools import setup, find_packages

setup(
    version=0.1,
    name='todo',
    packages=find_packages(),
    install_requires=[
        'setuptools',
        'Flask',
        'flask_httpauth',
        'flask_migrate',
        'flask_sqlalchemy'
    ],
)
