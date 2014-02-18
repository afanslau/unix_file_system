from FileLayer import *
import block as BlockLayer
from inode_number import *
import filename as FileNameLayer
from pathname import *
from abs_pathname import *


class FileDescriptor(object):
	"""docstring for FileDescriptor"""
	def __init__(self, filename, inodeNum):
		super(FileDescriptor, self).__init__()
		self.filename = filename
		self.inodeNum = inodeNum
		self.size = inode_number_to_inode(inodeNum).size
		self.cursor = 0
	def updateSize(self):
		self.size = inode_number_to_inode(self.inodeNum).size

#returns a FileDescriptor Object
def OPEN(filename, createOnFailure=1):
	inodeNum = general_path_to_inode_number(filename,createOnFailure)
	#SHOULD I RESTRICT SOMEONE FROM OPENING A DIRECTORY AS A FILE?
	if inodeNum == failure:
			raise Exception('No file exists named '+filename)
	return FileDescriptor(filename,inodeNum)

def READ(fd,buf=-1,numBytes=-1,bufferStart=0):
	if buf == -1:
		buf = []
	return FileNameLayer.read(fd.inodeNum,buf,numBytes,fd.cursor,bufferStart)

def WRITE(fd,buf,numBytes=-1,bufferStart=0):
	FileNameLayer.write(fd.inodeNum,buf,numBytes,fd.cursor,bufferStart)
	fd.updateSize()
	#return what was written

def SEEK(fd,offset,whence='beg'):
	#whence can be either beg, end, or curr
	if whence == 'beg':
		fd.cursor = offset
	elif whence == 'end':
		fd.cursor = fd.size-offset
	elif whence == 'curr':
		fd.cursor += offset
	else:
		raise Exception("Invalid usage: whence parameter must be either 'beg', 'end', or 'curr'")

def MKDIR(dirName):
	create(dirName,fileType=FileType.directory)

def CHDIR(dirName):
	inodeNum = general_path_to_inode_number(dirName)
	if inodeNum == failure:
		raise Exception("No directory by that name exists. To create one, use MKDIR(dirName)")
	FileNameLayer.wd = inodeNum

def CLOSE(fd):
	fd = None
			

if __name__ == '__main__':
	#test to create new files
	#print 'TESTING FOR OPEN(), READ(), AND WRITE()'
	firstFile = OPEN('myFirstFile')
	WRITE(firstFile,'this is some texting')
	#print ''.join(READ(firstFile))
	file2 = OPEN('secondFile')
	longStr = []
	for i in range(100):
		longStr.append('This is a really long string used for testing. ')
	longStr.append('-Bart Simpson')
	longStr = ''.join(longStr)
	WRITE(file2,longStr)

	#print read(wd)
	#print ''.join(READ(firstFile))
	#print read(wd)
	#print ''.join(READ(file2))
	#print read(wd)

	third = OPEN('third')
	#print read(wd)

	#print ' ------------------------- \n TESTING FOR SEEK()'
	SEEK(file2,15,'end')
	#print READ(file2)
	SEEK(file2,10,'curr')
	#print READ(file2)

	
	f = OPEN('new file')

	print '-------------------\n TESTING FOR MKDIR() AND CHDIR()'
	MKDIR('directory1')
	print 'wd before CHDIR',FileNameLayer.wd,filename.read(FileNameLayer.wd)
	CHDIR('directory1')
	print 'wd after CHDIR',FileNameLayer.wd,filename.read(FileNameLayer.wd)

	test=OPEN('another file')
