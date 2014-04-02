from fileSystemAPI import *
import filename as FileNameLayer
import inode_number as InodeNumberLayer
from abs_pathname import general_path_to_inode_number
'''
Example Usage

rm(name)  
ls() 
mkdir(name)
rmdir(name)
cd(name)
cat(name) print file
append(name,buf) write to end
'''
prevDir = FileNameLayer.rootDirectory

def append(name,buf):
	f = OPEN(name)
	contents = READ(f)
	contents += list(buf)
	WRITE(f,contents)

def cat(name):
	f = OPEN(name)
	print ''.join(READ(f))

def cd(name):
	CHDIR(name)

def mkdir(name):
	MKDIR(name)

def ls(name=''):
	if name == '':
		dir = FileNameLayer.wd
	else:
		dir = general_path_to_inode_number(name,createOnFailure=0)
		if dir == failure:
			raise Exception("Directory not found")
	#read in the dir
	contents = FileNameLayer.read(dir)
	#parse it to a list
	if not len(contents) == 0:
		list = ''.join(contents).split(',')
		printList = []
		for entry in list:
			pair = entry.split('|')
			printList.append(pair[0])
		print printList
		return printList
	else:
		print []
		return []

def rm(name,rmdir=False):
	#get the directory which contains the file by parsing the path
	#find the last slash in the path
	slashPos = []
	for i in range(len(name)):
		if name[i] == '/':
			slashPos.append(i)
	#if no slashes are found, use wd
	if len(slashPos) == 0:
		dir = FileNameLayer.wd
		matchName = name 
	elif slashPos[-1]==0:
		#if the last slash is the first char, use root dir
		dir = FileNameLayer.rootDirectory
		matchName = name[1:]
	else:
		#get the inode number for the path up to the last slash, which is the directory that contains the file
		dir = general_path_to_inode_number(name[:slashPos[-1]],createOnFailure=0)
		matchName = name[(slashPos[-1]+1):]
	#free the file's inode
	fd = OPEN(name)
	InodeNumberLayer.release_inode(fd.inodeNum)
	#remove the reference from wd
	contents = FileNameLayer.read(dir)
	list = ''.join(contents).split(',')
	i = 0

	while i < len(list):
		pair = list[i].split('|')
		#if the file is in the dir, remove it
		if pair[0] == matchName:
			list.pop(i)
			FileNameLayer.write(dir,','.join(list))
			return success 
		else:
			i += 1
	if rmdir:
		raise Exception("Directory not found")
	else:
		raise Exception("File not found")

def rmdir(name):
	#first, remove every file inside the directory recursively diving down as far as possible
	#open the directory
	#recursively call rmdir until not directory
	#repeat for all files in directory
	dirInodeNum = general_path_to_inode_number(name,createOnFailure=0)
	if dirInodeNum == failure:
		raise Exception("Directory not found")

	#parse to dict
	fnDict = FileNameLayer.parseDirectory(dirInodeNum)
	#go through all the files in the directory
	for fn in fnDict:
		if InodeNumberLayer.inode_number_to_inode(fnDict[fn]).type == FileNameLayer.FileType.directory:
			rmdir(name+'/'+fn)
		else:
			#base case: delete the file
			# print 'filename:',fn
			rm(name+'/'+fn)
	# print 'name:',name
	rm(name,rmdir=True)


if __name__ == '__main__':
	print 'Test: ls()'
	ls()
	print "Test: create new file append('newFile','hello this is some text') and cat('newFile')"
	append('newFile','hello this is some text')
	print ''.join(FileNameLayer.read(FileNameLayer.wd))
	cat('newFile')
	print "Test: append to the end append('newFile','MORE TEXT!')"
	append('newFile','MORE TEXT!')
	cat('newFile')

	#create a long string
	longStr = []
	for i in range(100):
		longStr.append('This is a really long string used for testing. ')
	longStr = ''.join(longStr)

	print 'Test create a long (multi-block) file'
	append('longer file',longStr)
	cat('longer file')
	print ''.join(FileNameLayer.read(FileNameLayer.wd))
	print 'Test append with a long file'
	append('longer file','-Bart Simpson')
	cat('longer file')

	ls()
	print "Test: rm('newFile')"
	rm('newFile')
	ls()
	
	#reading or writing to a non-existent file both create a new file with that filename
	cat('randomFile')
	cat('newFile')
	ls()

	print 'Test:abs_path'
	mkdir('newDir')	
	ls()
	cd('newDir')
	ls()
	append('/fileInRoot',"I've created this by using an absolute path name")
	ls()
#	print 'wd:',''.join(FileNameLayer.read(FileNameLayer.wd))
	append('testFile','blah blah blah')
	append('/newDir/fileWithPathName','testing')

	ls()
	mkdir('subDir')
	ls()
	cd('subDir')
	append('fileInSubDir','text in the file')
	mkdir('subDir2')
	cd('subDir2')
	append('deepestFile','jfkdlsjafkldjsaflkjdal;fj')
	ls()

	rm('/newDir/testFile')

	cd('/newDir')
	ls()

	cd('/')
	ls('/newDir/subDir')

	print 'Testing: rmdir()'

	rmdir('/newDir')
	ls()





