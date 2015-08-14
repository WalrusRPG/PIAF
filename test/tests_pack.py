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

sample_directory='test/samples/'
expected_suffix='_expected'
valid_folder='valid'



class TestParser (unittest.TestCase):

    def test_valid_unpack(self):
        #print('Valid samples testing.\n')
        valid_folder_path = os.path.join(sample_directory, valid_folder)
        valid_expected_folder = os.path.join(sample_directory, valid_folder+expected_suffix)
        list_files = [f for f in os.listdir(valid_folder_path)
                      if os.path.isfile(os.path.join(valid_folder_path, f))
                      and f.endswith(".wrf")]

        for f in list_files:
            path_sample = os.path.join(sample_directory, valid_folder, f)
            path_expected = os.path.join(sample_directory, valid_folder+expected_suffix,
                                         f+'.json')
            #print('{} => {}'.format(path_sample, path_expected))
            with open(path_sample, 'br') as sample, open(path_expected, 'r') as expected:
                archive = unpack.unpack_archive(sample.read())
                self.assertEqual(archive, json.load(expected))

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
                }
            ]
        },
        ]
        for f in files:
            self.assertDictEqual(f, unpack.unpack_archive(pack.pack_archive(f)))
