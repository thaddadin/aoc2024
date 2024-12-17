import time

def check1(stone):
    return stone == 0

def rule1():
    return 1

def check2(stone):
    return (len(str(stone)) % 2) == 0

def rule2(stone):
    stonestr = str(stone)
    ndigits  = len(stonestr)
    stone0   = int(stonestr[0:int(ndigits/2)])
    stone1   = int(stonestr[int(ndigits/2)::])
    return [stone0, stone1]

def rule3(stone):
    return stone * 2024

def blinkN(stones, blinks):
    
    counts = [1] * len(stones)
    
    for ii in range(blinks):
        
        t1 = time.time()
        
        nextstones = []
        nextcounts = []
        for jj in range(len(stones)):
            currstone = stones[jj]
            currcount = counts[jj]

            if check1(currstone):
                nextstones.append(rule1())
                nextcounts.append(currcount)
            elif check2(currstone):
                nextstones.extend(rule2(currstone))
                nextcounts.extend([currcount]*2)
            else:
                nextstones.append(rule3(currstone))
                nextcounts.append(currcount)

        stones, counts = consolidate(nextstones, nextcounts)
        
        t2 = time.time()
        print('nstones      = %i' % (len(stones)))
        print('blink%i time = %f' % (ii, t2-t1))

    return sum(counts)

def blink25(stones):
    blinks = 25
    return blinkN(stones, blinks)

def blink75(stones):
    blinks = 75
    return blinkN(stones, blinks)

def consolidate(stones, counts):

    nstone    = len(stones)
    newstones = [] # list of consolidated stones
    newcounts = [] # count of stone instances
    for ii in range(nstone):
        currstone = stones[ii]
        currcount = counts[ii]
        if not (currstone in newstones):
            newstones.append(currstone)
            newcounts.append(currcount)
        else:
            stoneidx = newstones.index(currstone)
            newcounts[stoneidx] = newcounts[stoneidx] + currcount

    return newstones, newcounts

with open('day11.txt') as fptr:
    data = fptr.read()

stones = [int(stone) for stone in data.split()]
counts1 = blink25(stones)
print('part1: %i' % counts1)
counts2 = blink75(stones)
print('part2: %i' % counts2)
