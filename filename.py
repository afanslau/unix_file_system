'''
File Name Layer

file names are mapped to inode numbers

need to maintain the working directory

to create a file:
	allocates an inode (get a free one)
	init its metadata (size, ...? )
	maps the proposed file name to the new inode

'''


from inode_number import *
from block import *
from FileLayer import *


def write(inodeNum, buf, numBytes = -1, fileStart = 0, bufferStart = 0):
	#get the inode
	if numBytes == -1:
		numBytes = len(buf)
	inode = inode_number_to_inode(inodeNum)
	if numBytes > block_size()*len(device):
		raise Exception("Not enough bytes on disk")
	if numBytes > len(buf)-bufferStart:
		numBytes = len(buf)-bufferStart
	inode.size = numBytes
	numFullBlocks = numBytes/block_size()
	extraBytes = numBytes%block_size()
	block_index = 0
	while block_index < numFullBlocks:
		newBlockNum = get_free_block()
		inode.block_numbers[block_index] = newBlockNum
		block_index += 1
	if extraBytes > 0:
		newBlockNum = get_free_block()
		inode.block_numbers[block_index] = newBlockNum
	#write the full blocks
	bufCursor = bufferStart
	block_index = 0
	while bufCursor < bufferStart+numBytes:
		#prepare the string to write - get the next 512 bytes
		blockWrite = buf[bufCursor:bufCursor+block_size()]
		#get the block number
		thisBlockNum = inode.block_numbers[block_index]
		thisBlock = block_number_to_block(thisBlockNum)
		thisBlock.write(blockWrite,len(blockWrite))
		bufCursor += block_size() #if the string is 2.5 blocks long, bufCursor will get incremented to 3 after the 2nd block is written
		block_index += 1

	#write the extra bytes
	blockWrite = buf[-extraBytes:]
	thisBlockNum = inode.block_numbers[block_index]
	thisBlock = block_number_to_block(thisBlockNum)
	thisBlock.write(blockWrite,len(blockWrite))
	return success

def read(inodeNum, buf=-1, numBytes=-1, fileStart=0, bufferStart=0):
	if buf == -1:
		buf = []
	#get the inode
	inode = inode_number_to_inode(inodeNum)
	#if numBytes is not specified, read the whole file
	if numBytes == -1:
		numBytes = inode.size - fileStart
	#first, read in the first block
	bufCursor = bufferStart
	first_block_index = fileStart/block_size()
	first_block_start = fileStart%block_size()
	firstBlockNum = inode.block_numbers[first_block_index]
	firstBlock = block_number_to_block(firstBlockNum)
	#read up to numBytes. If it spills over, the block layer handles the error and only reads one block
	firstBlock.read(buf=buf,numBytes=numBytes,blockStart=first_block_start,bufferStart=bufCursor)	
	bufCursor += block_size()-first_block_start
	#if attempting to read from only one block, the read operation is finished. Return buf
	if numBytes <= block_size()-first_block_start:
		return buf 
	#otherwise, decrement numBytes by the number of bytes already read
	numBytes -= block_size()-first_block_start
	#read the rest of the file starting from the beginning of the first full block
	numFullBlocks = numBytes/block_size()
	extraBytes = numBytes%block_size()		
	#go through each full block and write it to the buffer
	block_index = first_block_index+1
	while block_index<numFullBlocks+1:
		#get the block
		thisBlockNum = inode.block_numbers[block_index]
		thisBlock = block_number_to_block(thisBlockNum)
		#read to buf
		thisBlock.read(buf=buf,bufferStart=bufCursor)
		bufCursor += block_size()
		block_index += 1
	#read the extra bytes
	thisBlockNum = inode.block_numbers[block_index]
	thisBlock = block_number_to_block(thisBlockNum)
	thisBlock.read(buf=buf,numBytes=extraBytes,bufferStart=bufCursor)
	return buf 


rootDirectory = get_free_inode()
inode_number_to_inode(rootDirectory).type = FileType.directory
wd = rootDirectory
#used to implement the .. alias
lastDir = rootDirectory

if __name__ == '__main__':
	writeStr = []
	for i in range(100):
		writeStr.append('This is a really long string used for testing. ')
	writeStr.append('-Bart Simpson')
	writeStr = ''.join(writeStr)



	newFile = get_free_inode()
	write(newFile,'second file, does this become buf? and more bytes!')
	print read(newFile)

	write(wd,'blah blah blah blah blah blah blah')
	print read(wd)