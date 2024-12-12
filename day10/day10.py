def printmatrix(matrix):
    [print(" ".join(map(str, row))) for row in matrix]

def findstarts(matrix):

    starts = []
    nrow   = len(matrix)
    ncol   = len(matrix[0])
    for row in range(nrow):
        for col in range(ncol):
            if matrix[row][col] == 0:
                starts.append([row, col])

    return starts

def makestep(matrix, currloc, peaks):
    dirs = [[-1, +0], # up
            [+0, +1], # right
            [+1, +0], # down
            [+0, -1]] # left

    nrow = len(matrix)
    ncol = len(matrix[0])
    ndir = len(dirs)
    currlevel = matrix[currloc[0]][currloc[1]]

    if currlevel == 9:
        peakidx = getpeakidx(peaks, currloc)
        if peakidx > -1:
            # peak is already in list, increment count
            peaks[peakidx][1] = peaks[peakidx][1] + 1
        else:
            # peak isn't already in list, add peak and set count to 1
            peaks.append([currloc, 1])

    for dd in range(ndir):

        currdir = dirs[dd]
        nextloc = [currloc[0] + currdir[0],
                   currloc[1] + currdir[1]]

        if (nextloc[0] < 0) or (nextloc[0] == nrow) or (nextloc[1] < 0) or (nextloc[1] == ncol):
            # out of bounds of matrix
            continue

        nextlevel = matrix[nextloc[0]][nextloc[1]]
        leveldiff = nextlevel - currlevel
        
        if (leveldiff == 1):
            # go to next location
            makestep(matrix, nextloc, peaks)

def findscore(matrix):

    starts = findstarts(matrix)
    nstart = len(starts)

    count = 0
    rating = 0
    for ii in range(nstart):
        peaks   = []
        currloc = starts[ii]
        makestep(matrix, currloc, peaks)
        count = count + len(peaks)

        npeaks = len(peaks)
        for jj in range(npeaks):
            rating = rating + peaks[jj][1]
    return count, rating

def getpeakidx(peaks, currloc):

    idx = -1
    npeaks = len(peaks)
    for ii in range(npeaks):
        if peaks[ii][0] == currloc:
            idx = ii

    return idx

with open('day10.txt') as fptr:
    data = fptr.read()

matrix = [list(map(int, dd)) for dd in data.strip().split('\n')]
starts = findstarts(matrix)
count, rating = findscore(matrix)

print('part1: %i' % count)
print('part2: %i' % rating)
