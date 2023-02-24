#!/usr/bin/env python3

import os
import subprocess
import requests
import io
import pandas


class QueryException(Exception):
    pass


class EnaQuery:
    ENA_API = "https://www.ebi.ac.uk/ena/portal/api"

    def __init__(self, accession):
        """Query ena for the given accession"""
        self.columns = self._get_available_columns()
        self.table = self._query(accession, list(self.columns["columnId"]))

    def download(self, dryrun=False, outdir=".", **kwargs):
        """Download fastq. kwargs are columns to filter results.
        E.g. download(run_accession=['SRR123', 'SRR456'], taxid=[5821])"""
        keep = pandas.DataFrame.copy(self.table, deep=True)
        for column in kwargs:
            value = kwargs[column]
            keep = keep[keep[column].isin(value)]
        cmd_list = []
        for fastq_pair in keep.fastq_ftp:
            mates = fastq_pair.split(";")
            for fastq_ftp in mates:
                outfile = os.path.join(outdir, os.path.basename(fastq_ftp))
                cmd = f"curl -L {fastq_ftp} > {outfile}"
                cmd_list.append(cmd)
                if not dryrun:
                    p = subprocess.Popen(
                        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
                    )
                    stdout, stderr = p.communicate()
                    if p.returncode != 0:
                        try:
                            os.remove(outfile)
                        except:
                            pass
                        raise QueryException(
                            f"Exit code {p.returncode} while executing:\n{cmd}\n{stderr.decode()}"
                        )
        return cmd_list

    def _get_available_columns(self, for_type="read_run"):
        """Return a table of columns and descriptions for this data type"""
        url = f"{self.ENA_API}/returnFields?dataPortal=ena&result={for_type}"
        r = requests.get(url)
        if r.status_code != 200:
            raise QueryException("Return code %s" % r.status_code)

        txt = io.StringIO(r.text)
        table = pandas.read_csv(txt, sep="\t", low_memory=False)
        return table

    def _query(self, accession, columns):
        """Get results for this accession and returns all the given columns"""
        fields = ",".join(columns)
        url = f"{self.ENA_API}/filereport?accession={accession}&fields={fields}&result=read_run&limit=0"
        r = requests.get(url)
        if r.status_code == 200:
            txt = io.StringIO(r.text)
            table = pandas.read_csv(txt, sep="\t", usecols=columns, low_memory=False)
        else:
            table = pandas.DataFrame(columns=columns)
        return table
