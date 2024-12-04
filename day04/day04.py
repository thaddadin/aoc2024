def printmatch(matrix, idxlist):

    nrow = len(matrix)
    ncol = len(matrix[0])

    for row in range(nrow):
        line = ''
        for col in range(ncol-1):
            if [row, col] in idxlist:
                line = line + matrix[row][col]
            else:
                line = line + '.'
        print(line)

def findxmas(matrix, row, col):

    printen = False
        
    nrows = len(matrix)
    ncols = len(matrix[0])
    
    dirs = [[-1, -1], # up and left
            [-1, +0], # up and center
            [-1, +1], # up and right
            [+0, +1], # right
            [+1, +1], # down and right
            [+1, +0], # down and center
            [+1, -1], # down and left
            [+0, -1]] # left

    letters   = ['X', 'M', 'A', 'S']
    nletters  = len(letters)
    count     = 0
    idxlist   = []
    for dd in range(len(dirs)):

        curridxlist = []
        currdir = dirs[dd]
        currrow = row
        currcol = col
        currletter = matrix[currrow][currcol]

        if printen:
            print('currrow: % i' % currrow)
            print('currcol: % i' % currcol)
            print('currletter: %s' % currletter)
        
        letteridx  = 0
        currcheck  = letters[letteridx]

        while (currletter == currcheck):

            curridxlist = curridxlist + [[currrow, currcol]]
            
            letteridx = letteridx + 1
            if (letteridx >= nletters):
                # reached end of letters
                idxlist = idxlist + curridxlist
                break
            currcheck = letters[letteridx]
            
            currrow = currrow + currdir[0]
            if (currrow < 0) or (currrow >= nrows):
                # out of bounds row
                break
            currcol = currcol + currdir[1]
            if (currcol < 0) or (currcol >= ncols):
                # out of bounds col
                break
            currletter = matrix[currrow][currcol]

            if printen:
                print('currrow: % i' % currrow)
                print('currcol: % i' % currcol)
                print('currletter: %s' % currletter)

            if printen:
                print('letteridx: %i' % letteridx)

        if letteridx == nletters:
            count = count + 1

        if printen:
            print('count:%i' % count)

    return count, idxlist

def findx_mas(matrix, row, col):

    print('-'*50)
    print('row: %i' % row)
    print('col: %i' % col)

    nrow = len(matrix)
    ncol = len(matrix[0])

    upleft    = [-1, -1]
    upright   = [-1, +1]
    downleft  = [+1, -1]
    downright = [+1, +1]

    pairs = [[upleft, downright],
             [upright, downleft]]

    currrow00 = row + pairs[0][0][0]
    currcol00 = col + pairs[0][0][1]
    currrow01 = row + pairs[0][1][0]
    currcol01 = col + pairs[0][1][1]
        
    currrow10 = row + pairs[1][0][0]
    currcol10 = col + pairs[1][0][1]
    currrow11 = row + pairs[1][1][0]
    currcol11 = col + pairs[1][1][1]

    # check row lower limit
    if (currrow00 < 0) or (currrow01 < 0):
        return 0

    # check row upper limit
    if (currrow00 >= nrow) or (currrow01 >= nrow):
        return 0

    # check col lower limit
    if (currcol00 < 0) or (currcol01 < 0):
        return 0

    # check col upper limit
    if (currcol00 >= ncol) or (currcol01 >= ncol):
        return 0

    # check row lower limit
    if (currrow10 < 0) or (currrow11 < 0):
        return 0

    # check row upper limit
    if (currrow10 >= nrow) or (currrow11 >= nrow):
        return 0

    # check col lower limit
    if (currcol10 < 0) or (currcol11 < 0):
        return 0

    # check col upper limit
    if (currcol10 >= ncol) or (currcol11 >= ncol):
        return 0

    letterpair0 = [matrix[currrow00][currcol00], matrix[currrow01][currcol01]]
    letterpair1 = [matrix[currrow10][currcol10], matrix[currrow11][currcol11]]

    print('pair0: %s' % ', '.join(letterpair0))
    print('pair1: %s' % ', '.join(letterpair1))

    if (((letterpair0 == ['M', 'S']) or (letterpair0 == ['S', 'M'])) and ((letterpair1 == ['M', 'S']) or (letterpair1 == ['S', 'M']))):
        return 1
    else:
        return 0
        

with open('day04.txt') as fptr:
    lines = fptr.readlines()
matrix = [list(ll) for ll in lines]

count = 0

# loop over rows
idxlist = []
for row in range(len(matrix)):
    # loop over cols
    for col in range(len(matrix[0])):
    
        #find 'X'
        if matrix[row][col] == 'X':
            newcount, newidxlist = findxmas(matrix, row, col)
            count = count + newcount

            idxlist = idxlist + newidxlist

print('part1: %i' % count)

count = 0
for row in range(len(matrix)):
    for col in range(len(matrix[0])):

        # find 'A':
        if matrix[row][col] == 'A':
            newcount = findx_mas(matrix, row, col)
            count = count + newcount

print('part2: %i' % count)
