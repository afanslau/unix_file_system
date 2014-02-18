from block import *

_num_blocks_in_file = 100 #size of inode

class FileType(object):
	regular_file = 1
	directory = 2

class INode(object):
	"""inodes here do not use indirect blocks, so the size of a file is limited to 512 bytes*100 blocks"""
	def __init__(self, type=FileType.regular_file):
		super(INode, self).__init__()
		self.block_numbers = [-1]*_num_blocks_in_file #blocks of the file, 100 blocks maximum
		self.size = 0 #size of the file in bytes
		self.type = type
		#initialize the block_numbers array by getting the right amount of free blocks 

	def valid_index(self,index):
		return self.size/block_size() >= index

	def index_to_block_number(self, index):
		if self.valid_index(index):
			return self.block_numbers[index]
		raise Exception("Index number %s out of range." % index) #for more than one value, index must be a list of values
		
	def inode_to_block(self, offset): #offset in bytes
		o = offset / block_size() #which block in the file
		b = self.index_to_block_number(o) #gets the block number
		return block_number_to_block(b) #gets the data from the block 

if __name__ == '__main__':
	inode = INode()
	print inode.block_numbers
	print inode.size
	print inode.type

	inodeDir = INode(FileType.directory)
	print inodeDir.block_numbers
	print inodeDir.size
	print inodeDir.type
