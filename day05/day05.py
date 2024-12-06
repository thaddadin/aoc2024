def checkrule(currupdates, currrule):

    if (currrule[0] in currupdates) and (currrule[1] in currupdates):
        # both items from rule are in update list, perform check
        idx0 = currupdates.index(currrule[0])
        idx1 = currupdates.index(currrule[1])

        return idx0 < idx1
    else:
        # both items are not in the update list, rule pass
        return True

def needswap(pages, rules):

    nrules = len(rules)

    for ii in range(nrules):

        currrule = rules[ii]
        
        if (pages[0] in currrule) and (pages[1] in currrule):
            # check if they are in the correct order
            if pages == currrule:
                # don't need to swap
                return False
            else:
                return True
        else:
            # go to next rule
            pass

    return False

with open('day05.txt') as fptr:
    data = fptr.read()[0:-1]

data0, data1 = data.split('\n\n')

rules   = [[int(ll) for ll in line.split('|')] for line in data0.split('\n')]
updates = [[int(ll) for ll in line.split(',')] for line in data1.split('\n')]

nrules   = len(rules)
nupdates = len(updates)

# list of passing updates
passedupdates = []
failedupdates = []
for ii in range(nupdates):

    currupdates = updates[ii]
    npages      = len(currupdates)
    updatepass  = True
    
    for jj in range(npages):

        currpage = currupdates[jj]

        for kk in range(nrules):

            currrule = rules[kk]

            if currpage in currrule:
                # check if rule passes
                updatepass = checkrule(currupdates, currrule)

            if not updatepass:
                # if failed dont check remaining rules
                break

        if not updatepass:
            # if failed dont check ramining pages
            break

    if updatepass:
        # add currupdates to passing list
        passedupdates.append(currupdates)
    else:
        # add currupdates to failing list
        failedupdates.append(currupdates)

npassed = len(passedupdates)
count   = 0
for ii in range(npassed):
    currpassed = passedupdates[ii]
    count = count + currpassed[int(len(currpassed)/2)]

print('part1: %i' % count)

nfailed = len(failedupdates)
for ii in range(nfailed):

    currupdates = failedupdates[ii]
    toswap      = True
    
    while toswap:

        toswap = False
        npages = len(currupdates)
        
        for jj in range(npages-1):
            
            if needswap(currupdates[jj:jj+2], rules):
                temp = currupdates[jj]
                currupdates[jj]   = currupdates[jj+1]
                currupdates[jj+1] = temp
                toswap = True

    failedupdates[ii] = currupdates

count = 0
for ii in range(nfailed):

    currfailed = failedupdates[ii]
    count = count + currfailed[int(len(currfailed)/2)]

print('part2: %i' % count)
