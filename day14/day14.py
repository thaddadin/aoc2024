import time
import re

xgrid = 101 # 11
ygrid = 103 # 7

def printgrid(posxy):

    xpos  = 0
    ypos  = 1

    for yy in range(ygrid):
        for xx in range(xgrid):
            if xx == (xgrid-1):
                pend='\n'
            else:
                pend=''
                
            if [xx, yy] in posxy:
                print(posxy.count([xx, yy]), end=pend)
            else:
                print('.', end=pend)

def printgrid2(posxy):

    grid = makegrid(posxy)
    [print(''.join(map(str, row))) for row in grid]

def printgrid3(grid):
    [print(''.join(map(str, row))) for row in grid]

def makemove(robots, nmove):

    xpos  = 0
    ypos  = 1
    xvel  = 2
    yvel  = 3
    nrobots = len(robots)
    posxy = [[rr[xpos], rr[ypos]] for rr in robots]
    velxy = [[rr[xvel], rr[yvel]] for rr in robots]
    neighborcnt = [0] * nmove

    jj = 0
    while jj < nmove:
        print('jj=%i' % jj)
        for ii in range(nrobots):
            
            currxpos = posxy[ii][xpos]
            currypos = posxy[ii][ypos]
            currxvel = velxy[ii][xvel%2]
            curryvel = velxy[ii][yvel%2]

            nextxpos = (currxpos + currxvel) % xgrid
            nextypos = (currypos + curryvel) % ygrid

            posxy[ii][xpos] = nextxpos
            posxy[ii][ypos] = nextypos

        #neighborcnt[jj] = countneighbors(posxy)
        if (jj==6869):
            printgrid(posxy)
            input()
        #printgrid(posxy)
        #input()

        jj = jj + 1

    for ii in range(nrobots):
        robots[ii][xpos] = posxy[ii][xpos]
        robots[ii][ypos] = posxy[ii][ypos]

    return neighborcnt

def countquads(robots):

    xpos  = 0
    ypos  = 1
    quads = [0, 0, 0, 0] # top left, top right, bottom left, bottom right
    nrobot = len(robots)

    for ii in range(nrobot):

        currxpos = robots[ii][xpos]
        currypos = robots[ii][ypos]

        if (currxpos < int(xgrid/2)):
            # left
            if (currypos < int(ygrid/2)):
                # top
                quads[0] = quads[0] + 1
            elif (currypos > int(ygrid/2)):
                # bottom
                quads[2] = quads[2] + 1
        elif (currxpos > int(xgrid/2)):
            # right
            if (currypos < int(ygrid/2)):
                # top
                quads[1] = quads[1] + 1
            elif (currypos > int(ygrid/2)):
                # bottom
                quads[3] = quads[3] + 1

    return quads

def prod(quads):

    prod = 1
    nquad = len(quads)
    for ii in range(nquad):
        prod = prod * quads[ii]

    return prod

def findloop(robots):

    xpos  = 0
    ypos  = 1
    xvel  = 2
    yvel  = 3
    nrobots = len(robots)
    start = [[rr[xpos], rr[ypos]] for rr in robots]
    posxy = [[rr[xpos], rr[ypos]] for rr in robots]
    velxy = [[rr[xvel], rr[yvel]] for rr in robots]
    loops = [0] * nrobots

    for ii in range(nrobots):
        jj = 0
        while (posxy[ii] != start[ii]) or (jj==0):
            
            currxpos = posxy[ii][xpos]
            currypos = posxy[ii][ypos]
            currxvel = velxy[ii][xvel%2]
            curryvel = velxy[ii][yvel%2]

            nextxpos = (currxpos + currxvel) % xgrid
            nextypos = (currypos + curryvel) % ygrid
        
            posxy[ii][xpos] = nextxpos
            posxy[ii][ypos] = nextypos

            jj = jj + 1

        loops[ii] = jj

    return loops

def mapmove(robot, nmove):

    xpos  = 0
    ypos  = 1
    xvel  = 2
    yvel  = 3
    velxy = [robot[xvel], robot[yvel]]
    locs  = [[0, 0] for ii in range(nmove)]
    locs[0] = [robot[xpos], robot[ypos]]

    for ii in range(1, nmove):
        
        currxpos = locs[ii-1][xpos]
        currypos = locs[ii-1][ypos]

        nextxpos = (currxpos + velxy[xpos]) % xgrid
        nextypos = (currypos + velxy[ypos]) % ygrid

        locs[ii] = [nextxpos, nextypos]

    return locs

def makegrid(posxy):

    grid = [[0 for ii in range(xgrid)] for jj in range(ygrid)]

    for xx in range(xgrid):
        for yy in range(ygrid):

            if [xx, yy] in posxy:

                grid[yy][xx] = posxy.count([xx, yy])

    return grid

def findtri(posxy):

    grid = makegrid(posxy)

    tri = [[0, 0, 1, 0, 0],
           [0, 1, 1, 1, 0],
           [1, 1, 1, 1, 1]]
    ntrix = len(tri[0])
    ntriy = len(tri)
    
    for xx in range(xgrid-ntrix):
        for yy in range(ygrid-ntriy):
            ismatch = True
            for ii in range(ntriy):
                currgrid = grid[yy+ii][xx:xx+ntrix]
                currtri  = tri[ii]
                ismatch = ismatch and (currgrid == currtri)
                if not ismatch:
                    break

            if ismatch:
                printgrid3(grid)
                print('xx=%i, yy=%i' % (xx, yy))
                input()

def countneighbors(posxy):
    
    dirs = [[-1, +0], # up
            [-1, +1], # up and right
            [+0, +1], # right
            [+1, +1], # down and right
            [+1, +0], # down
            [+1, -1], # down and left
            [+0, -1], # left
            [-1, -1]] # up and left

    ndir   = len(dirs)
    nposxy = len(posxy)

    neighbors = 0
    for ii in range(nposxy):

        currposxy = posxy[ii]
        
        for jj in range(ndir):

            currdir     = dirs[jj]
            
            neighborloc = [currposxy[0]+currdir[0],
                           currposxy[1]+currdir[1]]

            if neighborloc in posxy:

                neighbors = neighbors + 1

    return neighbors
                
with open('day14.txt') as fptr:
    data = fptr.read()

robots = [list(map(int, re.findall(r'-?\d+', dd))) for dd in data.strip().split('\n')]
nloop = xgrid * ygrid
neighborcnt = makemove(robots, nloop)
quads = countquads(robots)
part1 = prod(quads)

print('part1: %i' % part1)
