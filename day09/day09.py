def createdisk(data):
    disk = []
    fileid = 0
    for ii in range(len(data)):
        if (ii % 2) == 0:
            # add file
            disk = disk + [fileid] * int(data[ii])
            fileid = fileid + 1
        else:
            disk = disk + [-1] * int(data[ii])

    return disk

def findlastfile(disk, lastidx):

    while((lastidx>-1) and (disk[lastidx]) == -1):
        lastidx = lastidx -1
    return lastidx

def packdisk(disk):

    lastidx = len(disk)-1
    for ii in range(len(disk)):
        
        if disk[ii] < 0:
            # empty disk block
            lastidx = findlastfile(disk, lastidx)

            if ii >= lastidx:
                #print('ii=%i' % ii)
                #print('lastidx=%i' % lastidx)
                return

            disk[ii] = disk[lastidx] # move file
            disk[lastidx] = -1       # clear disk

def findspace(disk, filesize, maxidx):
    #print('findspace()')

    spacestart = 0
    spacesize  = 0
    while True:
        spaceidx = spacestart + spacesize

        if spaceidx == maxidx:
            # reached max index
            spacesize = 0
            break
        elif disk[spaceidx] == -1:
            # in an empty space
            spacesize = spacesize + 1
        elif disk[spaceidx] > -1:
            # in a file
            spacestart = spacestart + 1
            spacesize  = 0

        if spacesize == filesize:
            break

    return spacestart, spacesize

def findfile(disk, fileid):
    #print('findfile()')

    ndisk    = len(disk)
    fileend  = ndisk-1
    filesize = 0
    while True:
        fileidx = fileend - filesize

        if fileidx < 0:
            # reach start of disk
            break
        elif disk[fileidx] == fileid:
            # in the file that matches fileid
            filesize = filesize + 1
        else:
            # not in file
            if filesize == 0:
                fileend = fileend - 1
            else:
                # just reached end of file
                fileend = fileend
                filesize  = filesize
                break
    filestart = fileend - filesize + 1
    
    return filestart, filesize

def packdisk2(disk, nfile):
    #print('packdisk2()')

    for ii in range(nfile, -1, -1):
        fileid = ii
        filestart, filesize = findfile(disk, fileid)
        spacestart, spacesize = findspace(disk, filesize, filestart)
        #print('fileid    =%i' % fileid)
        #print('filestart =%i' % filestart)
        #print('filesize  =%i' % filesize)
        #print('spacestart=%i' % spacestart)
        #print('spacesize =%i' % spacesize)
        if spacesize > 0:
            # move file
            movefile(disk, filestart, filesize, spacestart)

        #print(disk)
        #input()
    
def movefile(disk, filestart, filesize, spacestart):
    #print('movefile()')
    for ii in range(filesize):
        disk[spacestart+ii] = disk[filestart+ii]
        disk[filestart+ii] = -1
            
def calcchecksum(disk):

    checksum = 0
    for ii in range(len(disk)):

        if disk[ii] > -1:
            checksum = checksum + ii * disk[ii]

    return checksum

with open('day09.txt') as fptr:
    data = fptr.read().strip()

disk = createdisk(data)
#packdisk(disk)
#checksum = calcchecksum(disk)
#print('part1: %i' % checksum)
disk  = createdisk(data)
nfile = int(len(data)/2)
packdisk2(disk, nfile)
checksum = calcchecksum(disk)
print('part2: %i' % checksum)
