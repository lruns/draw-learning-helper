from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='draw-learning-helper',
    version='0.1.0',
    py_modules=['main'],
    install_reqs=required,
    entry_points={
        'console_scripts': [
            'draw-learning-helper = main:main',
        ],
    },
)
