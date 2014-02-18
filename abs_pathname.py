import pathname
import filename
from block import failure

def general_path_to_inode_number(path,createOnFailure=1):
	if path[0] == '/' and len(path)==1:
		return filename.rootDirectory
	if path[0]=='/':
		return pathname.name_to_inode_number(path[1:],filename.rootDirectory,createOnFailure=createOnFailure)
	else:
		return pathname.name_to_inode_number(path,createOnFailure=createOnFailure)
