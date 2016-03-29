#!/usr/bin/env python
from wrpg.piaf import pack
from wrpg.piaf.common import FileType, CompressionType, PIAF_VERSION

minimal_data = {"version": PIAF_VERSION,
"file_entries":[
{
	"path": "data/press.png",
	"file_name": "t_dbgfnt",
	"compression_type": CompressionType.RAW,
	"file_type": FileType.TEXTURE	
},
{
	"path": "data/press",
	"file_name": "f_dbgfnt",
	"compression_type": CompressionType.RAW,
	"file_type": FileType.UNKNOWN	
}
]
}

files_to_bundle = {"version": PIAF_VERSION,
"file_entries":[
{
	"path": "data/overworld.png",
	"file_name": "ov.png",
	"compression_type": CompressionType.RAW,
	"file_type": FileType.TEXTURE
},
{	"path": "data/l1.bin",
	"file_name": "l1.bin",
	"compression_type": CompressionType.RAW,
	"file_type": FileType.UNKNOWN
},
{	"path": "data/l2.bin",
	"file_name": "l2.bin",
	"compression_type": CompressionType.RAW,
	"file_type": FileType.UNKNOWN
},
{
	"path": "data/haeccity.png",
	"file_name": "t_haecci",
	"compression_type": CompressionType.RAW,
	"file_type": FileType.TEXTURE	
},
{
	"path": "data/haeccity",
	"file_name": "f_haecci",
	"compression_type": CompressionType.RAW,
	"file_type": FileType.UNKNOWN	
}
]};

def bundle(files, path_out):
	for f in files["file_entries"]:
		if 'path' in f:
			with open(f["path"], "rb") as o:
				f["data"] = o.read()
		f["file_name"] = f["file_name"].encode('ascii')
	out = pack.pack_archive(files)
	f = open(path_out, "wb+")
	f.write(out)

if __name__ == '__main__':
	bundle(minimal_data, "wrpg_core.wrf")
	bundle(files_to_bundle, "out.wrf")
