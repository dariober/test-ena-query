[![test status](https://github.com/dariober/test-ena-query/actions/workflows/main.yml/badge.svg)](https://github.com/dariober/test-ena-query/actions?query=branch%3Amaster+workflow%3Amain)
[![Language](http://img.shields.io/badge/language-python-blue.svg)](https://www.python.com/)
[![License](http://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/dariober/test-ena-query/blob/master/LICENSE.md)

<!-- vim-markdown-toc GFM -->

* [Description](#description)
* [Usage:](#usage)
* [Set up](#set-up)
* [Developer](#developer)

<!-- vim-markdown-toc -->

# Description

This Python module implements a simple interface to query the European
Nucleotide Archive ([ENA](https://www.ebi.ac.uk/ena/browser/home))

The code is functional and tested but it is only meant for demonstration
purposes.

# Usage:

Query ENA for the given accession id:

```
import enaquery

ena = enaquery.EnaQuery("PRJNA636949")
```

Get table of libraries in this project:

```
ena.table
# ...

ena.table[['run_accession', 'scientific_name', 'read_count']]

#    run_accession scientific_name  read_count
# 0    SRR11914509    Homo sapiens    12364309
# 1    SRR11914510    Homo sapiens     7855677
# 2    SRR11914511    Homo sapiens     2752375
# 3    SRR11914512    Homo sapiens     3964899
# 4    SRR11914513    Homo sapiens     7278733
# ...
```

Download some files in dry-run mode and show download command:

```
ena.download(dryrun=True, library_layout=['SINGLE'])
['curl -L ftp.sra.ebi.ac.uk/vol1/fastq/SRR119/009/SRR11914509/SRR11914509.fastq.gz > ./SRR11914509.fastq.gz',
 'curl -L ftp.sra.ebi.ac.uk/vol1/fastq/SRR119/010/SRR11914510/SRR11914510.fastq.gz > ./SRR11914510.fastq.gz',
 'curl -L ftp.sra.ebi.ac.uk/vol1/fastq/SRR119/011/SRR11914511/SRR11914511.fastq.gz > ./SRR11914511.fastq.gz'
 ...]
```

# Set up

Using [conda](https://docs.conda.io/projects/conda/en/latest/index.html) and
[mamba](https://github.com/mamba-org/mamba) configured for working with [bioconda](https://bioconda.github.io/):

```
mamba create -n test-chipseq --yes
mamba activate test-chipseq
mamba install -n test-chipseq --file requirements.txt --yes
```

# Developer

Run tests:

```
./test/test.py
```

Format code:

```
black enaquery.py test/test.py
```
