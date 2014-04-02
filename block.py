# _variable is python convention (does not enforce it) for private variables

blockSize = 512
failure = -1
success = 1

class Block(object):
	"""docstring for Block"""
	

	def __init__(self):
		super(Block, self).__init__()
		self.string = ['']*blockSize

	def write(self, buf, numBytes=-1, blockStart=0, bufferStart=0):
		'''
		blockStart - where in the block to start writing - default to 0
		buffer - string to be written
		numBytes - length of the string to be written (each char is 1 byte)
		bufferStart - place in the buffer from which to start writing - default to 0
		'''
		if (len(buf)-bufferStart < numBytes) or numBytes==-1:
			numBytes = len(buf)
		if blockStart+numBytes > blockSize:
			raise Exception('Buffer too long to write in one block')
		elif bufferStart > len(buf):
			raise Exception('Out of Bounds: bufferStart must be within the bounds of buffer')
		else:
			#go through the buffer string, start copying when i hits bufferStart
			for i in range(bufferStart,numBytes):
				self.string[i] = buf[i-bufferStart]
			return self.string

	#reads starting from blockStart up to numBytes
	#buffer must be a list at lease numBytes long
	def read(self, numBytes = blockSize, blockStart = 0, buf = -1, bufferStart = 0):
		if buf == -1:
			buf = []
			#I dont really understand why this doesnt work if I set the default to [] instead of -1. 
			#If I put buf = [] in the fn declaration, buf is carried over from the last time I call read
		if blockStart+numBytes > blockSize:
			numBytes = blockSize - blockStart
			#raise Exception('Cannot read '+numBytes+' bytes after byte '+blockStart);
			#return failure
		if bufferStart>len(buf):
			raise Exception('Out of Bounds: bufferStart must be within the bounds of buffer')
			#return failure
		for i in range(blockStart,blockStart+numBytes):
			if bufferStart+i-blockStart < len(buf):
				buf[bufferStart+i-blockStart] = self.string[i]
			else:
				buf.append(self.string[i])
		return buf


def init_blockLayer(numBlocks):
	device = []
	#NEED TO INITIALIZE EVERY BLOCK. RIGHT NOW ITS USING THE SAME BLOCK POINTER FOR EACH ELEMENT IN THE ARRAY
	for i in range(numBlocks):
		device.append(Block())
	freeList = [0]*numBlocks #0 is free, 1 is occupied
	return device,freeList

def block_size():
	return blockSize

def block_number_to_block(blockNum):
	#check if valid block number
	return device[blockNum]

def get_free_block():
	for i in range(len(freeList)):
		#find a block number that is free
		if freeList[i] == 0:
			#make it occupied
			freeList[i] = 1
			#return that block number
			return i
	raise Exception("Disk is full!!")

def release_block(blockNum):
	#check if valid block number
	freeList[blockNum] = 0
	return device[blockNum]




max_block_numbers = 100
layer = init_blockLayer(max_block_numbers)
device = layer[0]
freeList = layer[1]
# print device
# print freeList

if __name__ == '__main__':
	#do some testing code. This is excecuted when it is run from the command line NOT when imported
	b1 = block_number_to_block(get_free_block())
	b1.write('some loooooooooooooooooooooooooong text')
	#print b1.read(blockStart=5,numBytes=600)
	b1.read()

	b2 = block_number_to_block(get_free_block())
	b2.write('blah?')

	newBuf = list('hellooooooooooooo woooooooorld')
	print b2.read(buf = newBuf, numBytes = 4,bufferStart=len(newBuf))

