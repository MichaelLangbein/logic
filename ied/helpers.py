def unique(lst):
    ulst = []
    for e in lst:
        if e not in ulst:
            ulst.append(e)
    return ulst


def listUnion(list1, list2):
    uList = list1
    for entry in list2:
        if entry not in uList:
            uList.append(entry)
    return uList


def listIntersection(list1, list2):
    iList = []
    for entry in list1:
        if entry in list2:
            iList.append(entry)
    return iList
