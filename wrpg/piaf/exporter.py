import struct
import zlib
from common import (archive_structure, file_entry_structure)

def pack_filetable(archive):
    file_table = b''
    data_size = 0
    for f in archive['file_entries']:
        data_offset = data_size
        file_size = len(f["data"])
        file_table += struct.pack(file_entry_structure(), f["file_type"], f["compression_type"], file_size, data_offset)
        data_size += file_size

    return file_table, data_size

def pack_header(archive, packed_filetable, data_size):
    structure = archive_structure()
    nb_files = len(archive["file_entries"])
    header_data = struct.pack(structure[0]+structure[5:], archive["version"], nb_files, data_size)
    checksum_header = zlib.crc32(header_data)
    checksum_filetable = zlib.crc32(packed_filetable)
    print(checksum_filetable)

    return struct.pack(structure,
        b"WRPGPIAF",
        checksum_header,
        checksum_filetable,
        archive["version"],
        nb_files,
        data_size
    )

def pack_data(archive):
    return b''.join([f["data"] for f in archive["file_entries"]])

def pack_archive(archive):
    file_table, data_size = pack_filetable(archive)
    header = pack_header(archive, file_table, data_size)
    data = pack_data(archive)
    return header+file_table+data


if __name__ == '__main__':
    result = pack_archive({
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
    })
    print(result)
