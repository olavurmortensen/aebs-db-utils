import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

INSTALL_REQUIRES = ['ged4py>=0.1.11']

setuptools.setup(
    name="aebsDButils",
    version="0.0.1",
    author="Ólavur Mortensen",
    author_email="olavurmortensen@gmail.com",
    description="AEBS DB utils -- Utilities for exporting data from the Multi-Generation Registry of the Genetic Biobank of the Faroe Islands",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/olavurmortensen/aebs-db-utils",
    packages=setuptools.find_packages(),
    install_requires=INSTALL_REQUIRES,
    python_requires='>=3.6',
)
