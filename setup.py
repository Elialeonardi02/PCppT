from setuptools import setup, find_packages

setup(
    name='PCppT',
    version='1.0',
    packages=find_packages(),
entry_points={
        'console_scripts': [
            'pcppt=pcppt.main:main',
        ],
    },
    extras_require={},
    author='Elia Leonardi',
    author_email='e.leonardi5@studenti.unipi.it',
    description='Python c++ transpiler',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Elialeonardi02/PCppT',
    classifiers=[
        'to do', #TODO add correct info
    ],
    python_requires='>=3.12',    #TODO add correct info
)