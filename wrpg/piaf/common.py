from enum import IntEnum
import struct

PIAF_VERSION = 0x01000000


class FileType(IntEnum):
    UNKNOWN = 0
    MAP = 1
    EVENT_LIST = 2
    TEXT = 3
    TEXTURE = 4

class CompressionType(IntEnum):
    UNKNWOWN = 0
    RAW = 1
    ZLIB = 2
    RLE = 3

def header_check_structure():
    return (
        ">" # Big Endian
        "8s" # Magic Header
        "I" # Header Checksum
        "I" # File table Checksum
    )

def header_data_structure():
    return (
        ">" # Big Endian
        "I" # Version
        "I" # NB Files
        "I" # Data Size
        "4x" # Padding
    )

def header_structure():
    return (
        ">" # Big Endian
        +header_check_structure()[1:] # Cutting off the >
        # Offset : 24 (For checksum)
        +header_data_structure()[1:] # Cutting off the >
    )


def header_size():
    return struct.calcsize(header_structure())

def header_data_size():
    return struct.calcsize(header_data_structure())

def header_check_size():
    return struct.calcsize(header_check_structure())


def file_entry_structure():
    return (
        ">"  # Big Endian
        "8s" # Filename
        "I"  # File Type
        "I"  # Compression type
        "I"  # File Size
        "I"  # Data Offset
    )

def file_entry_size():
    return struct.calcsize(file_entry_structure())

def get_data_offset(nb_files):
    return header_size()+file_entry_size()*nb_files
