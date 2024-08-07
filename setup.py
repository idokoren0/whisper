from setuptools import setup, find_packages

setup(
    name='whisper',
    version='0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'PyYAML',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'whisper=src.server:main',
        ],
    },
)