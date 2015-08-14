import struct


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
        ">" # Big Endian
        "I" # File Type
        "I" # Compression type
        "I" # File Size
        "I" # Data Offset
    )

def file_entry_size():
    return struct.calcsize(file_entry_structure())

def get_data_offset(nb_files):
    return header_size()+file_entry_size()*nb_files
