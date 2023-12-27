from setuptools import setup, find_packages

setup(
    name='phyloworld',
    version="1.0",
    author='Milda Milčiūtė',
    author_email='milda.milciute@yahoo.com',
    url='https://github.com/mildamarij/phyloworld/tree/main',
    description='Phyloworld is a Python package that facilitates the visualization and analysis of phylogenetic trees alongside geographic information.',
    packages=find_packages(),
    install_requires=[
        'pandas==1.3.4',
        'notebook==7.0.6',
        'plotly==5.18.0',
        'biopython==1.81',
        'requests==2.31.0',
        'chart-studio==1.1.0',
    ]
)