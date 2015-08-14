import unittest
import os
import json
import struct

from wrpg.piaf import unpack, pack
from wrpg.piaf.unpack import (
    ParserError,
    ParserMagicHeaderError,
    ParserChecksumError,
    ParserDatasizeError
)

from test.common_util import *

class TestUnpack (unittest.TestCase):
    def test_valid_unpack(self):
        list_samples, list_expected = get_sample_files_and_expected(os.path.join(sample_directory, "unpack"), "valid")
        for sample_path, expected_path in zip(list_samples, list_expected):
            with open(sample_path, "rb") as sample, open(expected_path, "r") as expected:
                    # Little hack to support JSON's non-byte strings.
                    expected_data = json.load(expected)
                    for f in expected_data["file_entries"]:
                        if "data" in f:
                            f["data"] = bytes(f["data"], "ascii")
                    self.assertEqual(unpack.unpack_archive(sample.read()), expected_data)

    def test_invalid_unpack(self):
        ### Header
        # Emtpy argument
        with self.assertRaises(struct.error):
            unpack.unpack_archive(b'')

        # Header too small
        with self.assertRaises(struct.error):
            unpack.unpack_archive(b'The Game')

        # Bad header
        with self.assertRaises(ParserMagicHeaderError):
            unpack.unpack_archive(b'ERRHEADER\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0')

        # Bad checksum
        with self.assertRaises(ParserChecksumError):
            # Wrong header checksum
            unpack.unpack_archive(b'WRPGPIAF\x0D\x0E\x0A\x0D\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0')
        with self.assertRaises(ParserChecksumError):
            # Wrong filetable checksum
            unpack.unpack_archive(b'WRPGPIAF\0\0\0\0\x0D\x0E\x0A\x0D\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0')

        # Wrong data size
        with self.assertRaises(ParserDatasizeError):
            # Bad size because wrong file number
            unpack.unpack_archive(b'WRPGPIAF\xc6\x0f\x16#\0\0\0\0\0\0\0\0\r\x0e\n\r\0\0\0\0\0\0\0\0')
        ### Files
