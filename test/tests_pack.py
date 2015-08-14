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

sample_directory=os.path.join("test","samples")
expected_suffix='_expected'
valid_folder='valid'

def get_files_ending_with(folder, ending):
    return [os.path.join(folder,f) for f in os.listdir(folder)
                  if os.path.isfile(os.path.join(folder, f))
                  and f.endswith(ending)]


def get_sample_files_and_expected(root_folder, base_folder_name):
    sample_folder = os.path.join(root_folder, base_folder_name)
    expected_folder = os.path.join(root_folder, base_folder_name+expected_suffix)
    list_samples = get_files_ending_with(sample_folder, ".wrf")
    list_expected = get_files_ending_with(expected_folder, ".wrf.json")
    return list_samples, list_expected

class TestParser (unittest.TestCase):

    def test_valid_unpack(self):
        list_samples, list_expected = get_sample_files_and_expected(os.path.join(sample_directory, "unpack"), "valid")
        for sample_path, expected_path in zip(list_samples, list_expected):
            with open(sample_path, "rb") as sample, open(expected_path, "r") as expected:
                    self.assertEqual(unpack.unpack_archive(sample.read()), json.load(expected))

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

    def test_pack_unpack(self):
        files = [
        {
            "version": 0,
            "file_entries": []
        },
        {
            "version": 0,
            "file_entries": [{
                "file_type":1,
                "compression_type": 0,
                "data": b"The Game"
                },
                {
                "file_type":1,
                "compression_type": 0,
                "data": b"Ha, you lost it!"
                },
                {
                "file_type": 0,
                "compression_type": 1,
                "data": b"\0Test test test \0"
                }
            ]
        },
        ]
        for f in files:
            self.assertDictEqual(f, unpack.unpack_archive(pack.pack_archive(f)))
