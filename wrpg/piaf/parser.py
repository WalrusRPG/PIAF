import struct
import zlib
from common import (archive_structure, file_entry_structure, get_data_offset)

class ParserError(Exception):
    pass

class ParserMagicHeaderError(ParserError):
    pass

class ParserChecksumError(ParserError):
    pass

class ParserDatasizeError(ParserError):
    pass


def check_archive(buffer, archive, checksum_header, checksum_filetable, nb_files):
    def check_header(buffer):
        return zlib.crc32(buffer[16:32], 0) & 0xffffffff

    def check_filetable(buffer, archive):
        filetable_end = get_data_offset(nb_files)
        return zlib.crc32(buffer[32:filetable_end]) & 0xffffffff

    file_checksum_header = check_header(buffer)
    if file_checksum_header != checksum_header:
        raise ParserChecksumError('Bad Header Checksum : {} != {}'.format(file_checksum_header, checksum_header))

    file_checksum_filetable = check_filetable(buffer, archive)
    if file_checksum_filetable != checksum_filetable:
        raise ParserChecksumError('Bad Filetable Checksum : {} != {}'.format(file_checksum_filetable, checksum_filetable))

def check_data_size(buffer, archive, data_size, nb_files):
    if len(buffer) != data_size + get_data_offset(nb_files):
        raise ParserDatasizeError('Bad Data Size')


def parse_header(buffer):
    header = buffer[:32]
    magic_header, header_checksum, filetable_checksum, version, nb_files, data_size = struct.unpack(archive_structure(), header)
    magic_header = magic_header.decode('utf-8')
    archive = {
        "version": version,
        }

    if magic_header != 'WRPGPIAF':
        raise ParserMagicHeaderError('Bad Magic Header')

    check_archive(buffer, archive, header_checksum, filetable_checksum, nb_files)
    check_data_size(buffer, archive, data_size, nb_files)
    return archive, nb_files

def parse_filetable(buffer, archive, nb_files):
    result = []
    for i in range(0, nb_files):
        file_type, compression_type, file_size, data_offset = struct.unpack(file_entry_structure(), buffer[32+16*i:32+16*(i+1)])
        file_entry = {
            "file_type": file_type,
            "compression_type": compression_type,
            "file_size": file_size,
            "data_offset": data_offset
            }
        result.append(file_entry)
    return result

def load_data(buffer, archive):
    for f in archive["file_entries"]:
        data_start = get_data_offset(len(archive["file_entries"]))
        f["data"] = buffer[data_start+f["data_offset"]: data_start+f["data_offset"]+f["file_size"]]

def unpack_archive(buffer):
    archive, nb_files = parse_header(buffer)
    archive["file_entries"] = parse_filetable(buffer, archive, nb_files)
    load_data(buffer, archive)
    return archive


if __name__ == '__main__':
    print(unpack_archive(b'WRPGPIAF\x92\xdd\xbf\x90\xecRC\xca\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x18\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x08The GameHa, you lost it!'
))
