'''
PATH NAME LAYER 
recursively goes through and does a lookup to dive down the hierarchy of directories 
'''

'''a file that represents a directory containts a table that maps file names to inode numbers
in the format: with the restriction: no filename can start with a comma  
program|10,paper|12,someOtherFile|25

'''

from FileLayer import *
from inode_number import *
import filename

def Lookup(fn,dir):
	#fn is a plain name
	#dir is an inode number
	#recursive lookup of the fn in the dir file
	#returns the inode number of the file

	#check that dir is of type FileType.directory
	if not inode_number_to_inode(dir).type == FileType.directory:
		raise Exception("Tried to parse a regular_file as a directory")
	#read in the dir file and parse into a dict
	dirStr = filename.read(dir)
	if len(dirStr) == 0:
		return failure
	fnDict = {}
	list = ''.join(dirStr).split(',')
	for entry in list:
		pair = entry.split('|')
		fnDict[pair[0]] = int(pair[1])
	if fn in fnDict:
		return fnDict[fn]
	else:
		return failure

def name_to_inode_number(path,dir=-1,createOnFailure=1):
	if dir == -1:
		dir = filename.wd
	#look for a / in path
	i = 0
	r = []
	c = ''
	while not (c=='/' or i == len(path)):
		c = path[i]
		if not c == '/':
			r.append(c)
		i += 1
	if c=='/' and i == len(path):
		#tried to parse path with format dir/dir/filename/
		raise Exception('Invalid path syntax')
	elif c == '/':
		#check if the directory exists
		inodeNum = Lookup(''.join(r),dir)
		if inodeNum == failure:
			raise Exception('Directory not found')
		else:
			return name_to_inode_number(path[i:],inodeNum)
	elif i == len(path):
		#Base Case: path is a plain name
		inodeNum = Lookup(path,dir)
		if inodeNum == failure:
			if createOnFailure ==1:
				#if the file isnt found, create it
				inodeNum = create(path,dir)
			else:
				return failure 
		return inodeNum



def create(fn,dir=-1,fileType=FileType.regular_file):
	#to create a file, read in the dir file, then append ',filename|freeINodeNum'
	#returns the new inode number
	if dir == -1:
		dir = filename.wd
	fileContents = filename.read(dir)
	newInode = get_free_inode()
	inode_number_to_inode(newInode).type = fileType 
	#build the string
	writeStr = list(fn+'|'+str(newInode))
	if not len(fileContents) == 0:
		writeStr.insert(0,',')
	fileContents += writeStr
	filename.write(dir,fileContents)
	return newInode


