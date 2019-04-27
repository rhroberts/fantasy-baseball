from setuptools import setup, find_packages


setup(
    name='hometown_homies',
    version='0.1.0',
    description='Sabermetrics with friends',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'yahoo_oauth',
        'natsort',
        'scipy',
        'seaborn',
        'matplotlib'
    ]
)