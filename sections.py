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

try:
	verbose = (sys.argv[2])
	
except:
	verbose = 0

for file in all_files:
	newpath = '%s\\%s'% (sys.argv[1], file)
	
	logbuf = ''
	logbuf += ("%s " % file)
	
	f = open(newpath, 'rb')
	buf = f.read(0x10)
	
	num_sections_delphi = 0
	export_name_count = 0;
	random_export_name_count = 0
	
	if ord(buf[0]) != 0x4d or ord(buf[1]) != 0x5a:
		logbuf += ("not pe")
		print logbuf
		f.close()	
		continue 
		
	f.close()
	
	pe = pefile.PE(newpath, fast_load = True)
	
	chars = pe.FILE_HEADER.Characteristics
	print ( file )
	print ( "Name\t\tVirtualSize\tSizeOfRawData\tPtrToRawData\tCharacteristics" )
	print ( "--------------------------------------------------------------------------" )
	for section in pe.sections:	
		
		print ( "%s\t%08x\t%08x\t%08x\t%08x" % ( section.Name, section.Misc_VirtualSize, section.SizeOfRawData, section.PointerToRawData, section.Characteristics ))
	print ( "==========================================================================" )
		#print ( section )
