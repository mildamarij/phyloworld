from setuptools import setup, find_packages

def read_requirements(file):
    with open(file) as f:
        return f.read().splitlines()
requirements = read_requirements("requirements.txt")

setup(
    name = 'phylowordl',
    version = "1.0",
    author = 'Milda Milčiūtė',
    author_email = 'milda.milciute@yahoo.com',
    url = 'https://github.com/mildamarij/phyloworld/tree/main',
    description = 'Phyloworld is a Python package that facilitates the visualization and analysis of phylogenetic trees alongside geographic information.',
    packages = find_packages(exclude=["test"]),  
    install_requires = requirements
)