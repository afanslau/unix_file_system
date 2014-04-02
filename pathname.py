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

def Lookup(fn,dirInodeNum):
	#fn is a plain name
	#dir is an inode number
	#recursive lookup of the fn in the dir file
	#returns the inode number of the file

	#check that dir is of type FileType.directory
	if not inode_number_to_inode(dirInodeNum).type == FileType.directory:
		raise Exception("Tried to parse a regular_file as a directory")

	
	fnDict = filename.parseDirectory(dirInodeNum)
	if fn in fnDict:
		return fnDict[fn]
	else:
		return failure

def name_to_inode_number(path,currDir=-1,createOnFailure=1):
	# Default value
	if currDir == -1:
		currDir = filename.wd

	splitPath = path.split('/',1)
	pathLen = len(splitPath)
	firstName = splitPath[0]

	if path[-1]=='/':
		#tried to parse path with format dir/dir/filename/
		raise Exception('Invalid path syntax')
	#check if the directory exists
	inodeNum = Lookup(firstName,currDir)
	if pathLen==2:
		#valid path format dir/dir/filename
		if inodeNum == failure:
			raise Exception("Directory '"+firstName+"' not found")
		else:
			#recursive traversal to file
			return name_to_inode_number(splitPath[1],inodeNum)
	elif pathLen==1:
		#Base Case: path is a plain name
		if inodeNum == failure and createOnFailure:
			#if the file isnt found, create it
			inodeNum = create(firstName,currDir)
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


