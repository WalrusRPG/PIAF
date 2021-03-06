#!/usr/bin/env python
from wrpg.piaf import pack
from wrpg.piaf.common import FileType, CompressionType, PIAF_VERSION

minimal_data = {"version": PIAF_VERSION,
                "file_entries": [
                    {
                        "path": "data/core/press.png",
                        "file_name": "t_dbgfnt",
                        "compression_type": CompressionType.RAW,
                        "file_type": FileType.TEXTURE
                    },
                    {
                        "path": "data/core/press",
                        "file_name": "f_dbgfnt",
                        "compression_type": CompressionType.RAW,
                        "file_type": FileType.UNKNOWN
                    }
                ]
                }

wip_wrpg_data = {"version": PIAF_VERSION,
                 "file_entries": [
                     {
                         "path": "data/wip_data/overworld.png",
                         "file_name": "ov.png",
                         "compression_type": CompressionType.RAW,
                         "file_type": FileType.TEXTURE
                     },
                     {
                         "path": "data/wip_data/complete_spritesheet.png",
                         "file_name": "castle.png",
                         "compression_type": CompressionType.RAW,
                         "file_type": FileType.TEXTURE
                     },
                     {
                         "path": "data/wip_data/map.wrm",
                         "file_name": "map.wrm",
                         "compression_type": CompressionType.RAW,
                         "file_type": FileType.MAP
                     },
                     {
                         "path": "data/wip_data/set.wts",
                         "file_name": "set.wts",
                         "compression_type": CompressionType.RAW,
                         "file_type": FileType.MAP
                     },
                     {
                         "path": "data/wip_data/haeccity.png",
                         "file_name": "t_haecci",
                         "compression_type": CompressionType.RAW,
                         "file_type": FileType.TEXTURE
                     },
                     {
                         "path": "data/wip_data/haeccity",
                         "file_name": "f_haecci",
                         "compression_type": CompressionType.RAW,
                         "file_type": FileType.UNKNOWN
                     }
                 ]}


def bundle(files, path_out):
    for f in files["file_entries"]:
        if 'path' in f:
            with open(f["path"], "rb") as o:
                f["data"] = o.read()
                print(f['file_name'])
        f["file_name"] = f["file_name"].encode('ascii')
    out = pack.pack_archive(files)
    f = open(path_out, "wb+")
    f.write(out)


if __name__ == '__main__':
    bundle(minimal_data, "wrpg_core.wrf")
    bundle(wip_wrpg_data, "wip_data.wrf")
