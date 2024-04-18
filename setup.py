from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='draw-learning-helper',
    version='1.0.0',
    package_dir={"": "src"},
    install_requires=required,
    entry_points={
        'console_scripts': [
            'draw-learning-helper = main:main',
        ],
    },
)
