#!/usr/bin/env python3

import unittest
import sys
import shutil
import os
import pandas

from importlib.machinery import SourceFileLoader

enaquery = SourceFileLoader("enaquery", "enaquery.py").load_module()


class EnaQuery(unittest.TestCase):
    def setUp(self):
        sys.stderr.write("\n" + self.id().split(".")[-1] + " ")  # Print test name
        if os.path.exists("test_out"):
            shutil.rmtree("test_out")
        os.mkdir("test_out")

    def tearDown(self):
        if os.path.exists("test_out"):
            shutil.rmtree("test_out")

    def testCanGetTableAsDataFrame(self):
        ena = enaquery.EnaQuery("PRJNA636949")
        df = ena.table
        self.assertTrue(isinstance(ena.table, pandas.core.frame.DataFrame))
        self.assertEqual(len(df), 53)

    def testCanSelectDryRunDownload(self):
        ena = enaquery.EnaQuery("PRJNA636949")
        cmd_list = ena.download(
            dryrun=True,
            library_layout=["SINGLE"],
            library_strategy=["OTHER", "AMPLICON"],
        )
        self.assertEqual(len(cmd_list), 32)
        self.assertTrue(cmd_list[0][0:4], "curl")

        cmd_list = ena.download(
            dryrun=True, run_accession=["SRR11914513", "SRR11914514"]
        )
        self.assertEqual(len(cmd_list), 4)

    def testCanDownloadRunAccession(self):
        ena = enaquery.EnaQuery("PRJNA636949")
        cmd_list = ena.download(
            dryrun=False, run_accession=["SRR11914511"], outdir="test_out"
        )
        self.assertTrue(os.path.isfile("test_out/SRR11914511.fastq.gz"))

    def testCanDownloadRunAccession(self):
        ena = enaquery.EnaQuery("PRJNA636949")
        cmd_list = ena.download(
            dryrun=False, run_accession=["SRR11914511"], outdir="test_out"
        )
        self.assertTrue(os.path.isfile("test_out/SRR11914511.fastq.gz"))

    def testAccessionNotFound(self):
        ena = enaquery.EnaQuery("PRJNA636949")
        cmd_list = ena.download(run_accession=["FOOBAR"])
        self.assertEqual(len(cmd_list), 0)

        ena = enaquery.EnaQuery("FOO")
        self.assertEqual(len(ena.table), 0)


if __name__ == "__main__":
    unittest.main()
