import os
import sys
import pefile
import re

def list_files(path):
	files = []
	for name in os.listdir(path):
		if os.path.isfile(os.path.join(path, name)):
			files.append(name)
	return files

all_files = list_files('%s' % (sys.argv[1]))

for file in all_files:
	newpath = '%s\\%s'% (sys.argv[1], file)
	
	logbuf = ''
	logbuf += ("%s " % file)
	
	f = open(newpath, 'rb')
	buf = f.read(0x10)
	
	if ord(buf[0]) != 0x4d or ord(buf[1]) != 0x5a:
		logbuf += ("not pe")
		print logbuf
		f.close()	
		continue 
		
	pe = pefile.PE(newpath, fast_load = True)
	
	aep = pe.OPTIONAL_HEADER.AddressOfEntryPoint
	print "%s\t%x" % (file, aep)
	print pe.get_section_by_rva(aep)
	ep_offset = pe.get_offset_from_rva(aep)
	print "%x" % ep_offset
	
	f.seek(ep_offset)
	buf2 = f.read(0x30)
	nn = ''
	for b in buf2:
		nn+= "%0x "%ord(b)
	print nn
	f.close()

