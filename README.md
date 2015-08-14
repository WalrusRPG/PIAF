# PIAF
## PIAF Is an Archive Format

Python library to read/write WRPG archive files. PIAF is a custom archive format thought to pack data files for WRPG-based projects, it's thus not thought a general use.

## File Specifications.

A PIAF file (`.wrf` for W-Rpg File) is in three parts : the header, the file table and the data part. All the values are stored in **big endian**.

### The Header
The header has a fixed size : 24 bytes. Here's its content:

- A magic cookie : "WRPGPIAF" (not-null terminated, taking 8 bytes)
- The header's checksum (CRC32 value, taking 4 bytes)
- The filetable's checksum (CRC32 value, taking 4 bytes)
- The version, stored in a uint32 in this form : `0xAABBCCCC` (A = major version, B = minor version, C=fix) (4 bytes)
- The number of files (taking 4 bytes)
- The data section's size (taking 4 bytes)


More to come.
