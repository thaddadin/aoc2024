from colorama import Fore, Back, Style
def printdirs(dirsgrid, path):

    for currpath in path:

        print('[%i, %i] = %s'  % (currpath[0], currpath[1], dirsgrid[currpath[0]][currpath[1]]))
        
def printdirscount(dirsgrid):

    nrow = len(dirsgrid)
    ncol = len(dirsgrid[0])

    for row in range(nrow):
        for col in range(ncol):
            if (col == ncol-1):
                pend = '\n'
            else:
                pend = ''
                
            count = len(dirsgrid[row][col])

            print('%i' % count, end=pend)
            
def printcost(grid):

    nrow = len(grid)
    ncol = len(grid[0])
    maxcost = nrow * ncol * 2000
    lmax = 5#len(str(maxcost))
    for ii in range(nrow):
        for jj in range(ncol):
            if (jj == ncol-1):
                pend = '\n'
            else:
                pend = ''

            if grid[ii][jj] == maxcost:
                #print(Fore.RED + f"{grid[ii][jj]:0{lmax}d} " + Style.RESET_ALL, end=pend)
                print(Fore.RED + "*"*lmax + Style.RESET_ALL + " ", end=pend)
            else:
                print(f"{grid[ii][jj]:0{lmax}d} ", end=pend)
                
def printgrid(grid):

    [print(''.join(map(str, row))) for row in grid]

def printpath(grid, path):

    nrow = len(grid)
    ncol = len(grid[0])

    for ii in range(nrow):
        for jj in range(ncol):
            if (jj == ncol-1):
                pend = '\n'
            else:
                pend = ''

            if [ii, jj] in path:
                print(Fore.RED + grid[ii][jj] + Style.RESET_ALL, end=pend)
            else:
                print(grid[ii][jj], end=pend)

def parsedata(data):

    grid = [list(row) for row in data.strip().split('\n')]

    return grid

def findstart(grid):

    nrow = len(grid)
    ncol = len(grid[0])

    for ii in range(nrow):
        for jj in range(ncol):
            if grid[ii][jj] == 'S':
                return [ii, jj]

def findend(grid):

    nrow = len(grid)
    ncol = len(grid[0])

    for ii in range(nrow):
        for jj in range(ncol):
            if grid[ii][jj] == 'E':
                return [ii, jj]

def createcosts(grid, endloc):
    nrow = len(grid)
    ncol = len(grid[0])
    # 2 rotations at each cell, this value should never be reached 
    maxcost = nrow*ncol*2000
    costgrid = [[maxcost for _ in range(ncol)] for _ in range(nrow)]
    costgrid[endloc[0]][endloc[1]] = 0
    return costgrid

def createdirs(grid, startloc, endloc):
    nrow = len(grid)
    ncol = len(grid[0])
    lastgrid = [[[] for _ in range(ncol)] for _ in range(nrow)]

    # any direction on end cell
    lastgrid[endloc[0]][endloc[1]] = [[-1, +0], # up
                                      [+0, +1], # right
                                      [+1, +0], # down
                                      [+0, -1]] # left
    return lastgrid

def createcount(grid):
    nrow = len(grid)
    ncol = len(grid[0])
    countgrid = [[0 for _ in range(ncol)] for _ in range(nrow)]
    return countgrid

def calcrotation(indir, outdirs):
    
    dirs = [[-1, +0], # up
            [+0, +1], # right
            [+1, +0], # down
            [+0, -1]] # left

    inoutlut = [[0, 1, 2, 1], #in=0, out=[0, 1, 2, 3]
                [1, 0, 1, 2], #in=1, out=[0, 1, 2, 3]
                [2, 1, 0, 1], #in=2, out=[0, 1, 2, 3]
                [1, 2, 1, 0]] #in=3, out=[0, 1, 2, 3]

    inidx    = dirs.index(indir)
    outidxs  = [dirs.index(outdir) for outdir in outdirs]
    rotation = [inoutlut[inidx][outidx] for outidx in outidxs]

    minrot = min(rotation)

    return minrot

def calcstep(grid, costgrid, countgrid, dirsgrid, currloc, updatedloc, ddoffset=0):
    
    dirs = [[-1, +0], # up
            [+0, +1], # right
            [+1, +0], # down
            [+0, -1]] # left

    ndir = len(dirs)

    stepcost = 1
    rotcost  = 1000
    currcost = costgrid[currloc[0]][currloc[1]]
    currdirs = dirsgrid[currloc[0]][currloc[1]]

    for dd in range(ndir):
        loopdir  = dirs[(dd+ddoffset) % ndir]
        backdir  = [loopdir[0]*(-1), loopdir[1]*(-1)]
        prevloc  = [currloc[0]+backdir[0], currloc[1]+backdir[1]]
        prevcell = grid[prevloc[0]][prevloc[1]]
        
        if (prevcell == '.') or (prevcell == 'S'):
            rotation = calcrotation(loopdir, currdirs)
            newcost = currcost + rotation * rotcost
            prevcost = newcost + stepcost
            
            if prevcost < costgrid[prevloc[0]][prevloc[1]]:
                costgrid[prevloc[0]][prevloc[1]] = prevcost
                #costgrid[currloc[0]][currloc[1]] = newcost
                dirsgrid[prevloc[0]][prevloc[1]] = [loopdir]
                countgrid[prevloc[0]][prevloc[1]] = 1
                if (not (prevloc in updatedloc)) and (prevcell != 'S'):
                    updatedloc.append(prevloc)
            elif prevcost == costgrid[prevloc[0]][prevloc[1]]:
                #costgrid[currloc[0]][currloc[1]] = newcost
                dirsgrid[prevloc[0]][prevloc[1]].append(loopdir)
                countgrid[prevloc[0]][prevloc[1]] += 1
                if (not (prevloc in updatedloc)) and (prevcell != 'S'):
                    updatedloc.append(prevloc)

    return updatedloc

def backstep(grid):

    endloc    = findend(grid)
    startloc  = findstart(grid)
    costgrid  = createcosts(grid, endloc)
    dirsgrid  = createdirs(grid, startloc, endloc)
    countgrid = createcount(grid)
    
    updatedloc = [endloc]
    while (updatedloc):

        currloc = updatedloc.pop(0)
        calcstep(grid, costgrid, countgrid, dirsgrid, currloc, updatedloc, 3)

    # because you start the puzzle pointing right)
    lastrot = calcrotation([0, 1], dirsgrid[startloc[0]][startloc[1]])
    cost    = costgrid[startloc[0]][startloc[1]] + lastrot * 1000

    path = findpath(costgrid, startloc, endloc)

    #printcost(costgrid)
    #printgrid(countgrid)
    #printdirscount(dirsgrid)
    printpath(grid, path)
    #printdirs(dirsgrid, path)

    return cost

def findpath(costgrid, startloc, endloc):
    
    dirs = [[-1, +0], # up
            [+0, +1], # right
            [+1, +0], # down
            [+0, -1]] # left
    ndir = len(dirs)

    nrow = len(grid)
    ncol = len(grid[0])

    path = [startloc]
    while path[-1] != endloc:
        #print(path[-1])
        currloc = path[-1]

        mincost = nrow*ncol*2000
        minloc  = None

        for dd in range(ndir):

            currdir  = dirs[dd]
            testloc  = [currloc[0]+currdir[0], currloc[1]+currdir[1]]
            testcost = costgrid[testloc[0]][testloc[1]]

            if testcost < mincost:
                mincost = testcost
                minloc  = testloc

        path.append(minloc)
        #print('path=%s' % str(path))

    return path

with open('test16.txt') as fptr:
    data = fptr.read()

grid = parsedata(data)
cost = backstep(grid)

print('part1: %i' % cost)
