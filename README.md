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

Read individual ID (also called `RIN`), father ID, mother ID and sex (`F` or `M`) from GED file and write this to a CSV file. The header of the CSV file is `ind,father,mother,sex`.

```python
# Import the class that reads and writes the genealogy.
from aebsDButils.ged2csv import Ged2Genealogy

Ged2Genealogy([PATH TO GED], [PATH TO CSV])
```

Read `RIN` and birth year from GED file and write to a CSV with `ind,birth_year` header.

```python
from aebsDButils.ged2csv import GetBirthYear

GetBirthYear([PATH TO GED], [PATH TO CSV])
```

This method reads `RIN` and the `REFN` ID, encrypts `REFN`, and writes this to a CSV with `ind,hash_id` header. The `REFN` ID is reformatted to match the "personal identifier" `PID` before encryption. This uses a sh256 encryption.

```python
from aebsDButils.ged2csv import GetEncryptedID

GetEncryptedID([PATH TO GED], [PATH TO CSV])
```

If we have a `PID` and want to match to a `RIN` using the CSV we created above, we can encrypt the `PID` using the following code.

```python
from aebsDButils.utils import encrypt, check_pid

# Some pretend PID.
pid = '123456789'

# Check formatting of PID.
check_pid(pid)
# Encrypt PID.
hash_id = encrypt(pid)
```

### Clean GED file

The GED file may have some issues which means the `ged4py` GED parser won't be able to read it. We can fix this quite simply:

```python
from aebsDButils.utils import clean_ged
clean_ged([DIRTY GED PATH], [CLEANED GED PATH])
```
