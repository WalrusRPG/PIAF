import struct
import zlib
from wrpg.piaf.common import (
    header_structure,
    file_entry_structure,
    file_entry_size,
    get_data_offset,
    header_size,
    header_check_size,
    header_data_size)

class ParserError(Exception):
    pass

class ParserMagicHeaderError(ParserError):
    pass

class ParserChecksumError(ParserError):
    pass

class ParserDatasizeError(ParserError):
    pass


def load_data(buffer, archive, file_sizes):
    data_offset = 0
    for f, file_size in zip(archive["file_entries"], file_sizes):
        data_start = get_data_offset(len(archive["file_entries"]))
        data_start_position = data_start+data_offset
        f["data"] = buffer[data_start_position: data_start_position+file_size]
        data_offset += file_size

def unpack_archive(buffer):
    def parse_header():
        header = buffer[:header_size()]
        (   magic_header,
            header_checksum,
            filetable_checksum,
            version,
            nb_files,
            data_size ) = struct.unpack(header_structure(), header)

        magic_header = magic_header.decode('utf-8')
        archive = {
            "version": version }

        if magic_header != 'WRPGPIAF':
            raise ParserMagicHeaderError('Bad Magic Header')

        calculated_header_checksum = zlib.crc32(buffer[
            header_check_size()
            :header_check_size()+header_data_size() ]) & 0xffffffff

        if calculated_header_checksum != header_checksum:
            raise ParserChecksumError('Bad Header Checksum : {} != {}'
                .format(calculated_header_checksum, header_checksum))

        calculated_file_table_checksum = zlib.crc32(buffer[
            header_size()
            :header_size()+nb_files*file_entry_size()]
        ) & 0xffffffff

        if calculated_file_table_checksum != filetable_checksum:
            raise ParserChecksumError('Bad Filetable Checksum : {} != {}'
                .format(calculated_file_table_checksum, filetable_checksum))

        if len(buffer) != data_size + get_data_offset(nb_files):
            raise ParserDatasizeError('Bad Data Size')

        return archive, nb_files

    def parse_filetable():
        result = []
        file_sizes = []
        for i in range(nb_files):
            file_entry_offset = header_size()+file_entry_size()*i
            file_name, file_type, compression_type, file_size, data_offset =\
		struct.unpack(
	                file_entry_structure(),
                	buffer[ file_entry_offset: file_entry_offset+file_entry_size()]
                )

            file_entry = { "file_type": file_type,
                           "compression_type": compression_type }

            result.append(file_entry)
            file_sizes.append(file_size)
        return result, file_sizes

    archive, nb_files = parse_header()
    archive["file_entries"], file_sizes = parse_filetable()
    load_data(buffer, archive, file_sizes)
    return archive
