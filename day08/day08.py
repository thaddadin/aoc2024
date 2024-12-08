def printmatrix(matrix):
    print('\n'.join(map(''.join, matrix)))

def printantinodes(matrix, antinodelocs):

    nrow = len(matrix)
    ncol = len(matrix[0])

    for row in range(nrow):
        line = ''
        for col in range(ncol):

            if [row, col] in antinodelocs:
                line = line + '#'
            else:
                line = line + matrix[row][col]

        print(line)

def getantennas(matrix):

    # get list of antennas

    nrow = len(matrix)
    ncol = len(matrix[0])

    antennas = []
    for row in range(nrow):
        for col in range(ncol):
            if matrix[row][col] != '.':
                if not matrix[row][col] in antennas:
                    antennas.append(matrix[row][col])

    return antennas

def getantennalocs(matrix, antenna):

    # get list of antenna locations for a given antenna type

    nrow = len(matrix)
    ncol = len(matrix[0])
    
    antennalocs = []
    for row in range(nrow):
        for col in range(ncol):
            if matrix[row][col] == antenna:
                antennalocs.append([row, col])

    return antennalocs

def isdoubledist(loc, antennalocs):

    dist0 = (loc[0] - antennalocs[0][0])**2 + (loc[1] - antennalocs[0][1])**2
    dist1 = (loc[0] - antennalocs[1][0])**2 + (loc[1] - antennalocs[1][1])**2

    if (dist0 == 0) or (dist1 == 0):
        return False
    
    ratio = dist0/dist1
    
    if (ratio==4) or (ratio==0.25):
        # then one antenna is double the distance of the other
        return True
    else:
        return False

def isinline(loc, antennalocs):
    # equation for a line: y=mx+b
    # find m and b for line created with loc and each antennaloc
    # if m and b are equal then the points are inline

    if loc in antennalocs:
        # for part1 this case shouldn't occur because isdoubledist criteria
        # for part2 this should return true
        return True

    rowdelta0 = loc[0] - antennalocs[0][0]
    rowdelta1 = loc[0] - antennalocs[1][0]
    coldelta0 = loc[1] - antennalocs[0][1]
    coldelta1 = loc[1] - antennalocs[1][1]

    if (coldelta0 != 0) and (coldelta1 != 0):
        m0 = rowdelta0 / coldelta0
        m1 = rowdelta1 / coldelta1
        b0 = loc[0] - m0*loc[1]
        b1 = loc[0] - m1*loc[1]
    elif (rowdelta0 != 0) and (rowdelta1 != 0):
        m0 = coldelta0 / rowdelta0
        m1 = coldelta1 / rowdelta1
        b0 = loc[1] - m0*loc[0]
        b1 = loc[1] - m1*loc[0]
    elif ((rowdelta0 == 0) and (coldelta1 == 0)) or ((rowdelta1 == 0) and (coldelta0 == 0)):
        return False
    else:
        pass

    if (m0 == m1) and (b0 == b1):
        return True
    else:
        return False
    
def isantinode(loc, antennalocs):
    
    nantennalocs = len(antennalocs)
    
    # loop over each pair of antennas
    for ii in range(nantennalocs):
        for jj in range(nantennalocs):
            if ii != jj:
                antennapair = [antennalocs[ii], antennalocs[jj]]
                if isdoubledist(loc, antennapair):
                    if isinline(loc, antennapair):
                        return True

    return False

def isantinode2(loc, antennalocs):

    nantennalocs = len(antennalocs)

    # loop over each pair of antennas
    for ii in range(nantennalocs):
        for jj in range(nantennalocs):
            if ii != jj:
                antennapair = [antennalocs[ii], antennalocs[jj]]
                if isinline(loc, antennapair):
                    return True

    return False

def findantinodes(matrix, antennas):

    nantennas = len(antennas)
    nrow      = len(matrix)
    ncol      = len(matrix[0])
    count     = 0
    count2    = 0
    antinodelocs = []
    antinodelocs2 = []
    for antenna in range(nantennas):
        
        currantenna = antennas[antenna]
        antennalocs = getantennalocs(matrix, currantenna)

        print(currantenna)
        
        for row in range(nrow):
            for col in range(ncol):
                loc = [row, col]

                # part1
                if isantinode(loc, antennalocs):
                    if not loc in antinodelocs:
                        antinodelocs.append(loc)
                        count = count + 1

                # part2
                if isantinode2(loc, antennalocs):
                    if not loc in antinodelocs2:
                        antinodelocs2.append(loc)
                        count2 = count2 + 1

    return count, antinodelocs, count2, antinodelocs2

with open('test08.txt') as fptr:
    data = fptr.read()

matrix = [list(dd) for dd in data.strip().split('\n')]
antennas = getantennas(matrix)

count1, antinodelocs1, count2, antinodelocs2 = findantinodes(matrix, antennas)

#printantinodes(matrix, antinodelocs1)
#printmatrix(matrix)
print('part1: %i' % count1)
print('part2: %i' % count2)

