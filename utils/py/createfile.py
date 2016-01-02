#import pdb
def make_file(path, size):
    chunksize = 10485760 #10MB
    chunk = "A" * chunksize
    fh = open(path, 'w')
    left=size
    lastchunksize = size - (chunksize * int(size/chunksize))
    #pdb.set_trace()
    while left > lastchunksize:
        fh.write(chunk)
        left -= chunksize
        
    #pdb.set_trace()
    if left > 0 :
        fh.write("A" * left)
        
    fh.close
    
if __name__ == "__main__":
    print("creating the file ...")
    size = 2 # write the size in bytes
    make_file(str(size),size)
    
    print("file creation completed.")