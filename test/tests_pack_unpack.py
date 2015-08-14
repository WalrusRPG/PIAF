import unittest
from wrpg.piaf import unpack, pack


class TestPackUnpack (unittest.TestCase):
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
