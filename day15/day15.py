def printgrid(grid):

    [print(''.join(row)) for row in grid]

def parsedata(data):

    grid, moves = data.strip().split('\n\n')

    grid = [list(row) for row in grid.strip().split('\n')]

    moves = list(moves.replace('\n', ''))

    return grid, moves

def parsedirection(direction):
    
    dirs = [[-1, +0], # up
            [+0, +1], # right
            [+1, +0], # down
            [+0, -1]] # left

    if direction == '^':
        return dirs[0]

    if direction == '>':
        return dirs[1]

    if direction == 'v':
        return dirs[2]

    if direction == '<':
        return dirs[3]

def findstart(grid):

    nrow = len(grid)
    ncol = len(grid[0])

    for ii in range(nrow):
        for jj in range(ncol):
            if grid[ii][jj] == '@':
                return [ii, jj]

def makemove(grid, lastloc, currdir):

    currloc  = [lastloc[0]+currdir[0], lastloc[1]+currdir[1]]
    lastcell = grid[lastloc[0]][lastloc[1]]
    currcell = grid[currloc[0]][currloc[1]]

    if currcell == '.':
        # make move
        grid[currloc[0]][currloc[1]] = lastcell
        return True
    elif currcell == 'O':
        # try next cell
        if makemove(grid, currloc, currdir):
            grid[currloc[0]][currloc[1]] = lastcell
            return True
    elif currcell == '#':
        # can't move
        return False
    
    return False

def checkmove2(grid, lastloc, currdir, movelist):
    #print('-'*50)
    currloc  = [lastloc[0]+currdir[0], lastloc[1]+currdir[1]]
    lastcell = grid[lastloc[0]][lastloc[1]]
    currcell = grid[currloc[0]][currloc[1]]
    #print('lastloc=%s' % str(lastloc))
    #print('lastcell=%s' % lastcell)
    #print('currloc=%s' % str(currloc))
    #print('currcell=%s' % currcell)
    #print('movelist:%s' % str(movelist))
    if currcell == '.':
        # make move
        if currdir[1] == 0:
            # up/down
            #print('make move up/down')
            if (lastcell == ']'):
                # check left also
                #leftcell = grid[currloc[0]][currloc[1]-1]
                #if leftcell == '.':
                updatemove(movelist, currloc, lastloc)
                return True
            elif (lastcell == '['):
                # check right also
                #rightcell = grid[currloc[0]][currloc[1]+1]
                #if rightcell == '.':
                updatemove(movelist, currloc, lastloc)
                return True
            else:
                updatemove(movelist, currloc, lastloc)
                return True
                
        else:
            # left/right
            #print('make move: left/right')
            updatemove(movelist, currloc, lastloc)
            return True
    elif currcell == '#':
        # can't move
        return False
    elif (currcell == '[') or (currcell == ']'):
        # try next cell
        #print('try next cell')
        if currdir[1] == 0:
            # up/down
            #print('up/down')
            if ((currcell == '[') and
                checkmove2(grid, currloc, currdir, movelist) and
                checkmove2(grid, [currloc[0], currloc[1]+1], currdir, movelist)):
                updatemove(movelist, currloc, lastloc)
                return True
            if ((currcell == ']') and
                checkmove2(grid, currloc, currdir, movelist) and
                checkmove2(grid, [currloc[0], currloc[1]-1], currdir, movelist)):
                updatemove(movelist, currloc, lastloc)
                return True
        else:
            # left/right
            #print('left/right')
            if checkmove2(grid, currloc, currdir, movelist):
                updatemove(movelist, currloc, lastloc)
                return True

    return False

def updatemove(movelist, currloc, lastloc):

    if not [currloc, lastloc] in movelist:
        movelist.append([currloc, lastloc])

def commitmoves(grid, movelist):

    nmove = len(movelist)
    for ii in range(nmove):
        currloc = movelist[ii][0]
        prevloc = movelist[ii][1]

        grid[currloc[0]][currloc[1]] = grid[prevloc[0]][prevloc[1]]
        grid[prevloc[0]][prevloc[1]] = '.'

    #grid[prevloc[0]][prevloc[1]] = '.'

def makemoves(grid, moves):

    nmove = len(moves)

    currloc = findstart(grid)
    
    for ii in range(nmove):
        currmove = moves[ii]
        currdir  = parsedirection(currmove)
        if makemove(grid, currloc, currdir):
            grid[currloc[0]][currloc[1]] = '.'
            currloc  = [currloc[0]+currdir[0], currloc[1]+currdir[1]]

def makemoves2(grid, moves):

    nmove = len(moves)

    currloc = findstart(grid)
    
    for ii in range(nmove):
        currmove = moves[ii]
        currdir  = parsedirection(currmove)
        movelist = []
        if checkmove2(grid, currloc, currdir, movelist):
            #print('final movelist: %s' % str(movelist))
            commitmoves(grid, movelist)
            grid[currloc[0]][currloc[1]] = '.'
            currloc  = [currloc[0]+currdir[0], currloc[1]+currdir[1]]

        #print('Move %s:' % currmove)
        #printgrid(grid)
        #input()

def calcsum(grid):

    nrow = len(grid)
    ncol = len(grid[0])

    count = 0
    for ii in range(nrow):
        for jj in range(ncol):

            if grid[ii][jj] == 'O':

                count = count + 100 * ii + jj

    return count

def calcsum2(grid):

    nrow = len(grid)
    ncol = len(grid[0])

    count = 0
    for ii in range(nrow):
        for jj in range(ncol):

            if grid[ii][jj] == '[':

                count = count + 100 * ii + jj

    return count

def doublegrid(grid):

    nrow = len(grid)
    ncol = len(grid[0])
    
    newgrid = [[0 for ii in range(ncol*2)] for jj in range(nrow)]

    for ii in range(nrow):
        for jj in range(ncol):

            if grid[ii][jj] == '#':

                newgrid[ii][2*jj]   = '#'
                newgrid[ii][2*jj+1] = '#'

            elif grid[ii][jj] == 'O':

                newgrid[ii][2*jj]   = '['
                newgrid[ii][2*jj+1] = ']'

            elif grid[ii][jj] == '.':

                newgrid[ii][2*jj]   = '.'
                newgrid[ii][2*jj+1] = '.'

            elif grid[ii][jj] == '@':

                newgrid[ii][2*jj]   = '@'
                newgrid[ii][2*jj+1] = '.'

    return newgrid
    
with open('day15.txt') as fptr:
    data = fptr.read()

grid, moves = parsedata(data)
newgrid = doublegrid(grid)
makemoves(grid, moves)
count = calcsum(grid)
print('part1: %i' % count)
makemoves2(newgrid, moves)
count = calcsum2(newgrid)
print('part2: %i' % count)
