# AEBS DB utils

[![Travis CI build](https://api.travis-ci.org/olavurmortensen/aebs-db-utils.svg?branch=master)](https://travis-ci.org/github/olavurmortensen/aebs-db-utils) 

This package contains utilities to deal with the Multi-Generation Register of the Genetic Biobank of the Faroe Islands (https://biobank.fo/). This register is in Faroese referred to as "Ættarbandsskráin" ("lineage-relation-register"), hence the name of the package.

The package is written in Python and reads data from a GEDCOM 5.5.1 file and writes the data to CSV. We can write simple pedigrees (individual ID, father, mother, sex), as well as supplementary information like birth year.

## Installation

Install the Python package from source via `pip`.

```
pip install git+https://github.com/olavurmortensen/aebs-db-utils.git@master#egg=aebs-db-utils
```

## Usage

Read individual ID (called `RIN` or `xref_id`), father ID, mother ID and sex (`F` or `M`) and write this to a CSV file. The header of the CSV file is `ind,father,mother,sex`.

```python
# Import the class that reads and writes the genealogy.
from aebsDButils.ged2csv import Ged2Genealogy

Ged2Genealogy([PATH TO GED], [PATH TO CSV])
```

```python
from aebsDButils.ged2csv import GetBirthYear

GetBirthYear([PATH TO GED], [PATH TO CSV])
```

```python
from aebsDButils.ged2csv import GetEncryptedID

GetEncryptedID([PATH TO GED], [PATH TO CSV])
```
