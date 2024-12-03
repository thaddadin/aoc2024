with open('day01.txt') as fptr:
    datalines = fptr.readlines()

# map data to 2d matrix
data = [[int(dd) for dd in ll.split()] for ll in datalines]

# transpose list
data = list(map(list, zip(*data)))

# sort each column
data[0].sort()
data[1].sort()

nlines = len(data[0])

answer = 0
for ii in range(nlines):
    diff = abs(data[0][ii] - data[1][ii])
    answer = answer + diff

print('part1: %i' % answer)

answer = 0
for ii in range(nlines):
    num0  = data[0][ii]
    count = 0
    jj    = 0
    while ((jj < nlines) and (data[1][jj] <= num0)):
        if (data[1][jj] == num0):
            count = count + 1
        jj = jj + 1
    answer = answer + num0 * count

print('part2: %i' % answer)
