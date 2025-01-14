from setuptools import setup, find_packages

setup(
    name='PCppT',
    version='1.p',
    packages=find_packages(),
    install_requires=[
        'ast','sys','subprocess', 'inspect', 'types','enum'
    ],
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
    python_requires='>=3.0',    #TODO add correct info
)