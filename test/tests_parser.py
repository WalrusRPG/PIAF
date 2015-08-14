import unittest
import os
import json
import struct

from wrpg.piaf import parser
from wrpg.piaf.parser import (
    ParserError,
    ParserMagicHeaderError,
    ParserChecksumError,
    ParserDatasizeError
)

sample_directory='test/samples/'
expected_suffix='_expected'
valid_folder='valid'



class TestParser (unittest.TestCase):
    def test_valid_samples(self):
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
                archive = parser.unpack_archive(sample.read())
                self.assertEqual(archive, json.load(expected))

    def test_invalid_samples(self):
        ### Header
        # Emtpy argument
        with self.assertRaises(struct.error):
            parser.unpack_archive(b'')

        # Header too small
        with self.assertRaises(struct.error):
            parser.unpack_archive(b'The Game')

        # Bad header
        with self.assertRaises(ParserMagicHeaderError):
            parser.unpack_archive(b'ERRHEADER\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0')

        # Bad checksum
        with self.assertRaises(ParserChecksumError):
            # Wrong header checksum
            parser.unpack_archive(b'WRPGPIAF\x0D\x0E\x0A\x0D\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0')
        with self.assertRaises(ParserChecksumError):
            # Wrong filetable checksum
            parser.unpack_archive(b'WRPGPIAF\0\0\0\0\x0D\x0E\x0A\x0D\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0')

        # Wrong data size
        with self.assertRaises(ParserDatasizeError):
            # Bad size because wrong file number
            parser.unpack_archive(b'WRPGPIAF\xc6\x0f\x16#\0\0\0\0\0\0\0\0\r\x0e\n\r\0\0\0\0\0\0\0\0')
        ### Files
