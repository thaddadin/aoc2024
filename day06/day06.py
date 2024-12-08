import time

def findstart(matrix):

    nrow = len(matrix)
    ncol = len(matrix[0])
    dirs = ['^', '>', 'v', '<']
    
    for ii in range(nrow):
        for jj in range(ncol):
            if matrix[ii][jj].lower() in dirs:
                return [ii, jj], dirs.index(matrix[ii][jj])

def printmatrix(matrix):
    print('\n'.join(map(''.join, matrix)))

def move(matrix, loc, direction):

    steps = [[-1, +0], # up
             [+0, +1], # right
             [+1, +0], # down
             [-0, -1]] # left

    nrow    = len(matrix)
    ncol    = len(matrix[0])
    currrow = loc[0] # initialize starting row
    currcol = loc[1] # initialize starting col
    count   = 1      # initialize count of visited space
    visits  = [[currrow, currcol]]
    vdirs   = [[direction]]
    
    nextrow = currrow + steps[direction][0] # make first step
    nextcol = currcol + steps[direction][1] # make first step

    # while in bounds, take a step
    while (nextrow >= 0) and (nextrow < nrow) and (nextcol >= 0) and (nextcol < ncol):

        #print('nextrow: %i' % nextrow)
        #print('nextcol: %i' % nextcol)
        #print('count  : %i' % count)
        #print(visits)
        #printmatrix(matrix)
        #input()
        
        stepval = matrix[nextrow][nextcol]

        if stepval == '#':
            # cannot take the step, turn 90 degrees
            direction = (direction + 1) % 4
        else:
            # take the step
            currrow = nextrow
            currcol = nextcol

            if [currrow, currcol] in visits:
                # check if it has been visited 
                vidx = visits.index([currrow, currcol])
                if direction in vdirs[vidx]:
                    return count, visits, True
                else:
                    vdirs[vidx].append(direction)
            else:
                # the cell hasn't been visited, increment count and mark as visited
                count = count + 1
                visits.append([currrow, currcol])
                vdirs.append([direction])

        nextrow = currrow + steps[direction][0]
        nextcol = currcol + steps[direction][1]

    return count, visits, False

with open('day06.txt') as fptr:
    data = fptr.read()

matrix = [list(dd) for dd in data.split('\n')[0:-1]]

loc, direction = findstart(matrix)
count, visits, looped  = move(matrix, loc, direction)
print('part1: %i' % count)
#printmatrix(matrix)
nrow = len(matrix)
ncol = len(matrix[0])
count = 0
for vv in range(len(visits)):
    ii = visits[vv][0]
    jj = visits[vv][1]
    print('-'*50)
    print('vv: %i' % vv)
    if matrix[ii][jj] == '.':
        t1 = time.time()
        matrix[ii][jj] = '#'
        lcount, tmp, looped = move(matrix, loc, direction)
        count = count + int(looped)
        t2 = time.time()
        matrix[ii][jj] = '.'

        print('row : %i' % ii)
        print('col : %i' % jj)
        print('time: %f' % (t2-t1))

print('part2: %i' % count)
