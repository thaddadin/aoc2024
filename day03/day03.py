import re

with open('day03.txt') as fptr:
    data = fptr.read()

search1 = r'mul\((\d{1,3}),(\d{1,3})\)'
matches = re.findall(search1, data)

answer1 = 0
for ii in range(len(matches)):
    answer1 = answer1 + int(matches[ii][0]) * int(matches[ii][1])

print('part1: %i' % answer1)

search2 = r"(?:mul\((\d{1,3}),(\d{1,3})\))|(don't\(\))|(do\(\))"
matches = re.findall(search2, data)

enable  = 1
answer2 = 0
for ii in range(len(matches)):

    # check if enabled
    if matches[ii][3] != "":
        enable = 1
    # check if disable
    elif matches[ii][2] != "":
        enable = 0
    else:
        val0 = int(matches[ii][0])
        val1 = int(matches[ii][1])
        answer2 = answer2 + val0*val1*enable

print('part2: %i' % answer2)
