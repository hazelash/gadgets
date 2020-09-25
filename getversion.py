import os
import sys
import pefile
import re
import string

def list_files(path):
	files = []
	for name in os.listdir(path):
		if os.path.isfile(os.path.join(path, name)):
			files.append(name)
	return files

all_files = list_files('%s' % (sys.argv[1]))

try:
	verbose = (sys.argv[2])
	
except:
	verbose = 0

print "Sha256                                                           | CompanyName \t | ProductName \t | FileDescription \t | OriginalFilename \t | InternalName \t | " 
#\t LegalCopyright \t LegalTrademarks \ ProductVersion FileVersion"

for file in all_files:
	newpath = '%s\\%s'% (sys.argv[1], file)
	
	f = open(newpath, 'rb')
	buf = f.read()
	total_files += 1
	pe = pefile.PE(newpath, fast_load = True)
	
	rsc = pe.parse_resources_directory(  pe.OPTIONAL_HEADER.DATA_DIRECTORY[2].VirtualAddress , pe.OPTIONAL_HEADER.DATA_DIRECTORY[2].Size) 
	count = 0

	for i in  rsc.entries:
		if ( i.id == 0x10): 
			
			for xx in i.directory.entries:
				
				for yy in xx.directory.entries:
					version_struct = yy.data.struct
					start_offset = pe.get_offset_from_rva(version_struct.OffsetToData)
					
					raw_data = pe.__data__[start_offset:start_offset+version_struct.Size]
					versioninfo_struct = pe.__unpack_data__( pe.__VS_VERSIONINFO_format__, raw_data, file_offset = start_offset )
					pe.parse_version_information(yy.data.struct) 

					buf = file + ' | '

					if hasattr(pe, 'VS_VERSIONINFO'):
						if hasattr(pe, 'FileInfo'):
							for finfo in pe.FileInfo:
								for entry in finfo:
									if hasattr(entry, 'StringTable'):
										for st_entry in entry.StringTable:
											#for key, entry in list(st_entry.entries.items()):
											#print st_entry.entries
											#{'LegalCopyright': 'Copyright (c)  AllAlex, Inc.  All rights reserved.', 'InternalName': 'VideoClone.exe', 'FileVersion': '2, 3, 0, 0', 'CompanyName': 'AllAlex, Inc / Applian Technnologies, Inc', 'LegalTrademarks': 'WM Capture,VideoClone', 'ProductName': 'VideoClone', 'ProductVersion': '2, 3, 0, 0', 'FileDescription': 'VideoClone - Screen Recorder', 'OriginalFilename': 'VideoClone.exe'}
											try :
												buf += st_entry.entries['CompanyName'] + " | "
											except:
												buf += "(nil)\t | "
											try :
												buf += st_entry.entries['ProductName'] + " | "
											except:
												buf += "(nil)\t | "
											try : 
												buf += st_entry.entries['FileDescription'] + " | "
											except:
												buf += "(nil)\t | "
											try :
												buf += st_entry.entries['OriginalFilename'] + " | "
											except:
												buf += "(nil)\t | "
											try :
												buf += st_entry.entries['InternalName'] + " | "
											except:
												buf += "(nil)\t | "
											#try :
											#	buf += st_entry.entries['FileVersion'] + " | "
											#except:
											#	buf += "(nil)\t | "
											# LegalCopyright Copyright (c)  AllAlex, Inc.  All rights reserved.
											# InternalName VideoClone.exe
											# FileVersion 2, 3, 0, 0
											# CompanyName AllAlex, Inc / Applian Technnologies, Inc
											# LegalTrademarks WM Capture,VideoClone
											# ProductName VideoClone
											# ProductVersion 2, 3, 0, 0
											# FileDescription VideoClone - Screen Recorder
											# OriginalFilename VideoClone.exe
					print buf 
