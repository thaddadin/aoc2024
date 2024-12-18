import re

def parsedata(data):

    claws = data.split('\n\n')
    nclaw = len(claws)

    clawdata = []
    for ii in range(nclaw):

        currclaw  = claws[ii]
        clawlines = currclaw.strip().split('\n')
        nclawlines = len(clawlines)
        buttondata = []
        for jj in range(nclawlines):

            currclawline = clawlines[jj]
            currbuttondata = list(map(int, re.findall(r'-?\d+', currclawline)))
            buttondata.append(currbuttondata)

        clawdata.append(buttondata)
        
    return clawdata

def solveeq(clawdata, offset=0):

    xidx  = 0
    yidx  = 1
    aidx  = 0
    bidx  = 1
    xyidx = 2
    nclaw = len(clawdata)

    buttonpress = []
    for ii in range(nclaw):

        currclaw = clawdata[ii]

        xa = currclaw[aidx][xidx]
        ya = currclaw[aidx][yidx]
        xb = currclaw[bidx][xidx]
        yb = currclaw[bidx][yidx]
        x  = currclaw[xyidx][xidx] + offset
        y  = currclaw[xyidx][yidx] + offset

        b = (xa * y - ya * x) / (yb * xa - ya * xb)
        a = (x - xb * b) / xa

        print('a: %s' % str(a))
        print('b: %s' % str(b))

        buttonpress.append([a, b])

    return buttonpress

def calctokens(buttonpress):

    acost = 3
    bcost = 1
    aidx  = 0
    bidx  = 1
    nbuttonpress = len(buttonpress)
    costs = []
    for ii in range(nbuttonpress):

        currbuttonpress = buttonpress[ii]
        
        if currbuttonpress[aidx].is_integer() and currbuttonpress[bidx].is_integer():
            costs.append(currbuttonpress[aidx]*acost + currbuttonpress[bidx]*bcost)
        else:
            costs.append(0)

    return costs

with open('day13.txt') as fptr:
    data = fptr.read()

clawdata = parsedata(data)
buttonpress = solveeq(clawdata)
costs = calctokens(buttonpress)

buttonpress2 = solveeq(clawdata, offset=10000000000000)
costs2 = calctokens(buttonpress2)

print('part1: %i' % sum(costs))
print('part2: %i' % sum(costs2))
