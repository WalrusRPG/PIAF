
def archive_structure():
    return (
        ">" # Big Endian
        "8s" # Magic Header
        "I" # Header Checksum
        "I" # File table Checksum
        # Offset : 24 (For checksum)
        "I" # Version
        "I" # NB Files
        "I" # Data Size
        "4x" # Padding
    )

def file_entry_structure():
    return (
        ">" # Big Endian
        "I" # File Type
        "I" # Compression type
        "I" # File Size
        "I" # Data Offset
    )

def get_data_offset(nb_files):
    return 32+16*nb_files
