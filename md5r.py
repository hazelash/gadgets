import os
import sys
import hashlib

# Version 1.0	Released
# Version 1.5	Simplified Command (md5r . 2 2 => md5r . )
# Version 2.0	Added Recursive Mode + Logging Option
# Version 2.1	Solved unicode problem!!!!
# Version 2.2	Updating for python3 and some clean up 

#=================================================
def list_files(path):
	files = []
	for name in os.listdir((path)):
		if os.path.isfile(os.path.join(path, name)):
			files.append((name))

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
	md5buf = '' 
	files_in_path = list_files(path)
	
	for f in files_in_path:
		newpath = path + "\\" + f
		md5buf += hashlib.sha256(open(newpath, 'rb').read()).hexdigest() + "\t" + newpath + "\n"
	
	return md5buf

#=================================================
def recursive_dir_search(path):
	md5buf = '' 
	dirs_in_path = list_dir(path)
	
	for d in dirs_in_path:
		newpath = path + "\\" + d
		md5buf += recursive_dir_search(newpath)
	
	md5buf += get_md5_current_level(path)
	
	return md5buf

#=================================================
input_path = sys.argv[1].strip('\\')

try:
	input_mode = sys.argv[2].strip('\\')
except:
	input_mode = 'x'
	
md5buf = ''

#log_path = '.\\_md5list_'+input_mode+'.txt'
#fp = open(log_path, 'w')

print ("+================================================"  )
print ("| md5r (em-dee-fi-ver) "                            )
print ("| Version 2.2 "                                     )
print ("| 2020.01.08 by hazel"                              )
print ("+================================================"  )
print ("| Working Mode: %s " % input_mode                   )
print ("+================================================"  )

#=================================================
if input_mode == 'x':
	md5buf += get_md5_current_level(input_path)
	print (md5buf)
#=================================================	
elif input_mode == 'r':
	md5buf += recursive_dir_search(input_path)
	print ( md5buf )
	#print ("| Open Log File: %s " % log_path)
	
#=================================================		
else:
	print ("md5r [path] [mode]")

#=================================================		
#
print ("+================================================")
#print (md5buf.encode('utf8'))
#fp.write(md5buf.encode('utf8'))	
#fp.close()	

#cmd = log_path
#os.system(cmd)
