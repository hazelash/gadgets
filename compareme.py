import sys
import os
import hashlib

BUF_SIZE = 0x4000

def get_hash(file):
	ctx = hashlib.sha256()
	with open( file , 'rb') as f:
		while True:
			data = f.read(BUF_SIZE)

			if not data:
				break
			ctx.update(data)
				
		return ctx.hexdigest()

def byte_by_byte_diff(file1, file2, offset1, offset2):
	if ( offset1 < 0 or offset2 < 0 ):
		print ("[+] Offset should be 0 or higher")
		exit(1)
	
	f1 = open(file1, 'rb')
	b1 = f1.read()
	
	f2 = open(file2, 'rb')
	b2 = f2.read()
	
	if ( offset1 >= len(b1) or offset2 >= len(b2) ):
		print ("[+] Offset should be smaller than file size")
		exit(1)
	
	if ( len(b1) == len(b2) ): limit = len(b1)
	elif ( len(b1) < len(b2) ): limit = len(b1)
	elif ( len(b1) > len(b2) ): limit = len(b2)
	
	i = 0
	
	while (offset1+i <= limit):
	
		if ( b1[offset1+i] == b2[offset2+i] ):
			i += 1
			continue
		else:
			#print ("[+] Found difference at offset %d (%d)" % (offset1+i, offset2+i ))
			printbuf1 = ''
			printbuf2 = ''
			# end buffer check, total buffer < 16
			if ( offset1+i-8 <= 0 ):
				printoffset1 = offset1+i
			else:
				printoffset1 = offset1+i-8
				
			if ( offset2+i-8 <= 0 ):
				printoffset2 = offset2+i
			else:
				printoffset2 = offset2+i-8
				
			for b in b1[printoffset1:printoffset1+16]:
				printbuf1 += "%02x " % ord (b)
			for b in b2[printoffset2:printoffset2+16]:
				printbuf2 += "%02x " % ord (b)
	
			print "+==========+=================================================+=================================================+==========+"
			print "|          |                         **                      |                         **                      |          |"
			print "| %08x | %s| %s| %08x |" % (printoffset1, printbuf1, printbuf2, printoffset2)
			print "+==========+=================================================+=================================================+==========+"
			
			input = raw_input("[+] Cancel: ( x ) | Continue to next byte: ( Enter ) | Or number of bytes to skip: ")
			if ( input == " " or input == "" ) :
				i += 1 
				continue
				
			if ( input == "x" ) :
				exit(1)
			
			try: 
				int ( input )
			except: 
				print ("[+] Wrong input, aborting diff")
				exit(1)

			i += int ( input )
			continue
	print ("[+] Reached the end of file ")			

file1 = sys.argv[1]
file2 = sys.argv[2]
option = sys.argv[3]

# take offset as input & other options
offset1 = 0
offset2 = 0

print ("[+] Compare Us!")
print ("[+] File1: %s" % file1)
print ("[+] File2: %s" % file2)

fsize1 = os.path.getsize(file1)
fsize2 = os.path.getsize(file2)

if (option):
	byte_by_byte_diff(file1, file2, offset1, offset2)
	
if ( fsize1 != fsize2 ):
	print ("[+] Different size! (%d vs %d)" % ( fsize1, fsize2 ) )
	print ("[+] If you want byte-by-byte diff, use -d option")
	exit(0)

hash1 = get_hash(file1)
hash2 = get_hash(file2)

if ( hash1 != hash2 ):
	print ("[+] Different hash! (%s vs %s)" % ( hash1, hash2 ) )
	print ("[+] If you want byte-by-byte diff, use -d option")
	exit(0)


