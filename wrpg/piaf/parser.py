import struct
import string
import unittest
import zlib
from .common import (archive_structure, file_entry_structure)

class ParserError(Exception):
    pass

class ParserMagicHeaderError(ParserError):
    pass

class ParserChecksumError(ParserError):
    pass

class ParserDatasizeError(ParserError):
    pass


def check_archive(buffer, archive, checksum_header, checksum_filetable):
    def check_header(buffer):
        return zlib.crc32(buffer[16:32], 0) & 0xffffffff

    def check_filetable(buffer, archive):
        filetable_end = 32+24*archive["nb_files"]
        return zlib.crc32(buffer[32:filetable_end]) & 0xffffffff

    file_checksum_header = check_header(buffer)
    if file_checksum_header != checksum_header:
        raise ParserChecksumError('Bad Header Checksum : {} != {}'.format(file_checksum_header, checksum_header))

    file_checksum_filetable = check_filetable(buffer, archive)

    if file_checksum_filetable != checksum_filetable:
        raise ParserChecksumError('Bad Filetable Checksum : {} != {}'.format(file_checksum_filetable, check_filetable))

def check_data_size(buffer, archive):
    if len(buffer) != archive["data_size"] + 32 + 24*archive["nb_files"]:
        raise ParserDatasizeError('Bad Data Size')

def parse_header(buffer):
    header = buffer[:32]
    parsed_header = struct.unpack(archive_structure(), header)
    magic_header = parsed_header[0].decode('utf-8')
    archive = {
    "version": parsed_header[3],
    "nb_files": parsed_header[4],
    "data_size": parsed_header[5]
    }

    if magic_header != 'WRPGPIAF':
        raise ParserMagicHeaderError('Bad Magic Header')

    check_archive(buffer, archive, parsed_header[1], parsed_header[2])
    check_data_size(buffer, archive)
    return archive

def parse_filetable(buffer, archive):
    result = []
    for i in range(0, archive["nb_files"]):
        result.append(struct.unpack(file_entry_structure(), archive[32+24*i:32+24*(i+1)]))
    return result

def parse_archive(buffer):
    archive = parse_header(buffer)
    archive["file_entries"] = parse_filetable(buffer, archive)
    return archive
