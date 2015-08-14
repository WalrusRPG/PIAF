import struct
import zlib
from wrpg.piaf.common import (archive_structure, file_entry_structure)

def pack_filetable(archive):
    file_table = b''
    data_size = 0
    for f in archive['file_entries']:
        data_offset = data_size
        file_size = len(f["data"])
        file_table += struct.pack(file_entry_structure(), f["file_type"], f["compression_type"], file_size, data_offset)
        data_size += file_size

    return file_table

def pack_header(archive, packed_filetable):
    structure = archive_structure()
    data_size = sum([len(f["data"]) for f in archive["file_entries"]])
    # Little hack to parse only the data part of the strucutre.
    # Should evolve as the structure definition does.
    header_data = struct.pack(structure[0]+structure[5:], archive["version"], len(archive["file_entries"]), data_size)

    return struct.pack(structure,
        b"WRPGPIAF",
        zlib.crc32(header_data),
        zlib.crc32(packed_filetable),
        archive["version"],
        len(archive["file_entries"]),
        data_size
    )

def pack_data(archive):
    return b''.join([f["data"] for f in archive["file_entries"]])

def pack_archive(archive):
    file_table = pack_filetable(archive)
    header = pack_header(archive, file_table)
    data = pack_data(archive)
    return header+file_table+data
