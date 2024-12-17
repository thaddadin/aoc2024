from colorama import Fore, Back, Style

def printmatrix(matrix):
    [print("".join(map(str, row))) for row in matrix]

def printregion(matrix, arealoc, perimeterloc):

    nrow = len(matrix)
    ncol = len(matrix[0])

    line = '  '
    for col in range(-1, ncol+1):
        line = line + str(abs(col)%10)
    print(line)
    for row in range(-1, nrow+1):
        print(str(abs(row)%10) + ' ', end='')
        for col in range(-1, ncol+1):
            if col == ncol:
                pend = '\n'
            else:
                pend = ''
            currloc = [row, col]
            if currloc in arealoc:
                print(matrix[row][col], end=pend)
            elif currloc in perimeterloc:
                count = perimeterloc.count(currloc)
                print(Fore.RED + '%i' % count + Style.RESET_ALL, end=pend)
            else:
                print('.', end=pend)

def findregion(matrix, checked):

    nrow = len(matrix)
    ncol = len(matrix[0])

    for row in range(nrow):
        for col in range(ncol):

            if checked[row][col] == 0:
                return [row, col]

    return [-1, -1]

def makestep(matrix, checked, currloc, arealoc, perimeterloc):
    dirs = [[-1, +0], # up
            [+0, +1], # right
            [+1, +0], # down
            [+0, -1]] # left

    nrow = len(matrix)
    ncol = len(matrix[0])
    ndir = len(dirs)
    currplant = matrix[currloc[0]][currloc[1]]
    checked[currloc[0]][currloc[1]] = 1
    area = 1
    arealoc.append(currloc)
    perimeter = 0
    
    for dd in range(ndir):

        currdir = dirs[dd]
        nextloc = [currloc[0] + currdir[0],
                   currloc[1] + currdir[1]]
        newperimeter = 0
        newarea      = 0

        if (nextloc[0] < 0) or (nextloc[0] == nrow) or (nextloc[1] < 0) or (nextloc[1] == ncol):
            # out of bounds of matrix, increment boarder and continue
            newperimeter = newperimeter + 1
            perimeterloc.append(nextloc)
        else:
        
            nextplant = matrix[nextloc[0]][nextloc[1]]
            nextcheck = checked[nextloc[0]][nextloc[1]]

            if (nextplant == currplant):
                if (nextcheck == 0):
                    newarea, newperimeter = makestep(matrix, checked, nextloc, arealoc, perimeterloc)
                else:
                    newarea = 0
                    newperimeter = 0
            else:
                newarea = 0
                newperimeter = 1
                perimeterloc.append(nextloc)

        area = area + newarea
        perimeter = perimeter + newperimeter
            
    return area, perimeter

def getfencetotal(matrix, checked):

    loc = findregion(matrix, checked)
    total1 = 0
    total2 = 0
    nregion = 0
    while (loc != [-1, -1]):
        perimeterloc = []
        arealoc = []
        currarea, currperimeter = makestep(matrix, checked, loc, arealoc, perimeterloc)
        #print('-'*50)
        #print('current plant: %s' % matrix[loc[0]][loc[1]])
        #print('currarea     : %i' % currarea)
        #print('currperimeter: %i' % currperimeter)
        #print(arealoc)
        #printregion(matrix, arealoc, perimeterloc)
        currcorner = getregioncorners(matrix, arealoc)
        #print('currarea      : %i' % currarea)
        #print('currcorner    : %i' % currcorner)
        #print('%i * %i = %i' % (currarea, currcorner, currarea*currcorner))
        total1 = total1 + currarea * currperimeter
        total2 = total2 + currarea * currcorner
        loc = findregion(matrix, checked)
        nregion = nregion + 1
        #print('nregion:%i' % nregion)
    return total1, total2

def getregioncorners(matrix, arealoc):

    narea = len(arealoc)

    totalcorner = 0
    for ii in range(narea):

        currarealoc = arealoc[ii]
        outsidecorner = outsidecornercount(matrix, currarealoc)
        insidecorner = insidecornercount(matrix, currarealoc)
        totalcorner = totalcorner + outsidecorner + insidecorner

        #print('-'*50)
        #print(currarealoc)
        #print('outside: %i' % outsidecorner)
        #print('inside : %i' % insidecorner)
        #print('total  : %i' % totalcorner)

    return totalcorner

def outsidecornercount(matrix, loc):
    dirs = [[-1, +0], # up
            [+0, +1], # right
            [+1, +0], # down
            [+0, -1]] # left
    ndir = len(dirs)
    nrow = len(matrix)
    ncol = len(matrix[0])
    currplant = matrix[loc[0]][loc[1]]

    cornercnt = 0
    for dd in range(ndir):

        dir1 = dirs[dd]
        dir2 = dirs[(dd+1) % ndir]

        loc1 = [loc[0] + dir1[0],
                loc[1] + dir1[1]]
        loc2 = [loc[0] + dir2[0],
                loc[1] + dir2[1]]

        isdiff1 = (loc1[0] < 0) or (loc1[0] == nrow) or (loc1[1] < 0) or (loc1[1] == ncol) or (matrix[loc1[0]][loc1[1]] != currplant)
        isdiff2 = (loc2[0] < 0) or (loc2[0] == nrow) or (loc2[1] < 0) or (loc2[1] == ncol) or (matrix[loc2[0]][loc2[1]] != currplant)

        if isdiff1 and isdiff2:
            cornercnt = cornercnt + 1

    return cornercnt

def insidecornercount(matrix, loc):
    dirs = [[-1, +0], # up
            [-1, +1], # up and right
            [+0, +1], # right
            [+1, +1], # down and right
            [+1, +0], # down
            [+1, -1], # down and left
            [+0, -1], # left
            [-1, -1]] # up and left
    ndir = len(dirs)
    nrow = len(matrix)
    ncol = len(matrix[0])
    currplant = matrix[loc[0]][loc[1]]

    cornercnt = 0
    for dd in range(0, ndir, 2):
        dir1 = dirs[dd]
        dir2 = dirs[dd+1]
        dir3 = dirs[(dd+2) % ndir]

        loc1 = [loc[0] + dir1[0],
                loc[1] + dir1[1]]
        loc2 = [loc[0] + dir2[0],
                loc[1] + dir2[1]]
        loc3 = [loc[0] + dir3[0],
                loc[1] + dir3[1]]
        
        isdiff1 = (loc1[0] < 0) or (loc1[0] == nrow) or (loc1[1] < 0) or (loc1[1] == ncol) or (matrix[loc1[0]][loc1[1]] != currplant)
        isdiff2 = (loc2[0] < 0) or (loc2[0] == nrow) or (loc2[1] < 0) or (loc2[1] == ncol) or (matrix[loc2[0]][loc2[1]] != currplant)
        isdiff3 = (loc3[0] < 0) or (loc3[0] == nrow) or (loc3[1] < 0) or (loc3[1] == ncol) or (matrix[loc3[0]][loc3[1]] != currplant)

        if (not isdiff1) and (isdiff2) and (not isdiff3):
            cornercnt = cornercnt + 1

    return cornercnt

with open('day12.txt') as fptr:
    data = fptr.read()

matrix  = [list(dd) for dd in data.strip().split('\n')]

nrow    = len(matrix)
ncol    = len(matrix[0])
checked = [[0] * ncol for _ in range(nrow)]
part1,part2 = getfencetotal(matrix, checked)
print('part1: %i' % part1)
print('part2: %i' % part2)
