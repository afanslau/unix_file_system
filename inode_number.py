import block
from FileLayer import *

#initialize 100 free inodes
inode_table = []
free_inodes = [] #0 is free 1 is occupied
num_inodes = 100
for i in range(num_inodes):
	inode_table.append(INode())
	free_inodes.append(0)




def valid_inode(inode_num):
	return (inode_num>=0) and (inode_num<num_inodes)

def get_free_inode():
	for i in range(num_inodes):
		#look for a free inode
		if free_inodes[i] == 0:
			#set it to occupied
			free_inodes[i] = 1
			#return the inode number
			return i
	raise Exception("No free inodes")

def release_inode(inode_num):
	inode_number_to_inode(inode_num).size = 0
	free_inodes[inode_num] = 0


def inode_number_to_inode(inode_num):
	if valid_inode(inode_num):
		return inode_table[inode_num]
	raise Exception("Invalid inode number")

def inode_number_to_block(offset, inode_num):
	i = inode_number_to_inode(inode_num)
	o = offset/block.block_size()
	b = i.index_to_block_number(offset)
	return block.block_number_to_block(b)

if __name__ == '__main__':
	print inode_table

