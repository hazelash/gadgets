import os
import sys
import hashlib

# Version 1.0	Released

#=================================================
def list_files(path):
	files = []
	for name in os.listdir(path):
		if os.path.isfile(os.path.join(path, name)):
			files.append(name)
	
	return files

#=================================================
def list_dir(path):
	dirs = []
	
	for name in os.listdir(path):
		if os.path.isdir(os.path.join(path, name)):
			dirs.append(name)
	
	return dirs

#=================================================
def get_md5_current_level(path):	
	#md5buf = '' 
	files_in_path = list_files(path)
	
	for f in files_in_path:
		newpath = path + "\\" + f
		#md5buf += hashlib.md5(open(newpath, 'rb').read()).hexdigest() + "\t" + newpath + "\n"
		cmd = "move \"%s\" %s" % ( newpath, path + "\\" + hashlib.md5(open(newpath, 'rb').read()).hexdigest() )
		print cmd 
		os.system( cmd )

#=================================================
def recursive_dir_search(path):
	dirs_in_path = list_dir(path)
	
	for d in dirs_in_path:
		newpath = path + "\\" + d
		recursive_dir_search(newpath)
	
	get_md5_current_level(path)

#=================================================
input_path = sys.argv[1].strip('\\')

try:
	input_mode = sys.argv[2].strip('\\')
except:
	input_mode = 'x'
	
md5buf = ''

log_path = 'd:\\temp\\_md5list_'+input_mode+'.txt'
fp = open(log_path, 'w')

print "+================================================"
print "| rename to md5 "
print "| Version 1.0 "
print "| 2016 September by hazel"
print "+================================================"
print "| Working Mode: %s " % input_mode
print "+================================================"

#=================================================
if input_mode == 'x':
	get_md5_current_level(input_path)
#=================================================	
elif input_mode == 'r':
	recursive_dir_search(input_path)
	
#=================================================		
else:
	print "md5r [path] [mode]"

#=================================================		
#
print "+================================================"
#fp.write(md5buf)	
#fp.close()	
