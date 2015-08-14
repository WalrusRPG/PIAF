import unittest
from wrpg.piaf import unpack, pack


class TestUnpackPack (unittest.TestCase):
    def test_pack_unpack(self):
        files = [
            b'WRPGPIAF\xec\xbbKU\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        ]
        for f in files:
            self.assertEqual(f, pack.pack_archive(unpack.unpack_archive(f)))
