from setuptools import setup, find_packages

setup(
    name='markdown2confluence',
    version='0.3.0-alpha',
    packages=find_packages(),
    install_requires=[
        # dependencies
    ],
    entry_points={
        'console_scripts': [
            'markdown2confluence = markdown2confluence.main:main_function',
        ],
    },
)
