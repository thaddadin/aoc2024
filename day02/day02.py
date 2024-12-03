def checkrow(row):
    sign0    = int(row[0] < row[1])*2-1
    fail     = False
    jj       = 0
    while (jj < (len(row)-1)):

        diff = abs(row[jj] - row[jj+1])
        sign = int(row[jj] < row[jj+1])*2-1

        if (diff < 1) or (diff > 3) or (sign != sign0):
            fail = True

        if fail:
            return 0
        else:
            jj = jj + 1

    if fail:
        return 0
    else:
        return 1

with open('day02.txt') as fptr:
    datalines = fptr.readlines()

data = [[int(dd) for dd in ll.split()] for ll in datalines]
fail = []
nlines = len(data)
answer1 = 0
answer2 = 0
for ii in range(nlines):
    currline = [dd for dd in data[ii]]
    if checkrow(currline):
        answer1 = answer1 + 1
        answer2 = answer2 + 1
    else:
        # if you fail try deleting a signle index and see if you pass after
        # removing one index
        for jj in range(len(currline)):
            editedline = [dd for dd in currline]
            del editedline[jj]
            if checkrow(editedline):
                answer2 = answer2 + 1
                break
print('part1: %i' % answer1)
print('part2: %i' % answer2)
            
