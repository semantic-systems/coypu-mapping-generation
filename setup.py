from setuptools import setup

setup(
    name='coypu-mapping-generation',
    version='0.0.1',
    packages=[
        'semanticlabeling',
        'semanticmodeling',
        'util',
        'tests'
    ],
    scripts=[
        'bin/infermapping'
    ],
    url='',
    license='',
    author='Patrick Westphal',
    author_email='',
    description='',
    install_requires=[
        'rdflib==7.0.0',
        'pandas==2.2.0',
        'matplotlib',
        'steiner-tree==1.1.3',
    ]
)
