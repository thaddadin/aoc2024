import time

def getop(oplist):

    for ii in range(len(oplist)):
        oplist[ii] = oplist[ii] + 1
        if oplist[ii] < 3:
            return
        else:
            oplist[ii] = 0

def concatenate(a, b):

    ndigits = len(str(b))
    return 10**ndigits*a+b

with open('day07.txt') as fptr:
    data = fptr.read()

result = {
    int(line.split(':')[0]) : list(map(int, line.split(':')[1].split())) for line in data.strip().split('\n')}

passing = []
for key in result.keys():
    
    currlist = result[key]
    nlist    = len(currlist)
    
    # loop over each operator location
    for ii in range(2**(nlist-1)):

        # loop over each bit and perform the operation
        value = currlist[0]
        for jj in range(nlist-1):

            operation = (ii >> jj) & 0x1

            if operation:
                # perform multiply
                value = value * currlist[jj+1]
            else:
                # perform addiction
                value = value + currlist[jj+1]

        if value == key:
            passing.append(key)
            break

count = sum(passing)
print('part1: %i' % count)

passing = []
for key in result.keys():
    print('-'*50)
    print(key)
    print('-'*50)
    t1 = time.time()
    currlist = result[key]
    nlist    = len(currlist)
        
    oplist = [2] * (nlist-1)

    # loop over each operator location
    for ii in range(3**(nlist-1)):
        
        getop(oplist)
        
        # loop over each bit and perform the operation
        value = currlist[0]
        for jj in range(nlist-1):

            operation = oplist[jj]

            if operation == 0:
                # perform multiply
                value = value * currlist[jj+1]
            elif operation == 1:
                # perform addition
                value = value + currlist[jj+1]
            else:
                # perform concatenation
                value = concatenate(value, currlist[jj+1])

        if value == key:
            passing.append(key)
            break
    t2 = time.time()
    print('%f' % (t2-t1))

count = sum(passing)
print('part2: %i' % count)
