import sys
import time

global docDict
docDict = dict()


def MyReadDataRoutine():
    # Get the file path and num of docs from terminal
    # file = sys.argv[1]
    # numDocuments = sys.argv[2]

    # get the start time
    st = time.time()

    # file to read the data
    file = open("data/DATA_1-docword.enron.txt")

    # number of documents to read
    numDocuments = 2000

    docs = 1
    previousDocID = 1

    # read the file
    data = file.read()

    # split with space
    data = data.split("\n")

    # remove the first 3 lines we don't need them here
    data.pop(0)
    data.pop(0)
    data.pop(0)

    # number of key in the dictionary (docID)
    k = 1

    # set the dictionary with keys
    for docId in range(1, numDocuments + 1):
        docDict[docId] = []

    for i in range(len(data) - 1):

        # if we pass the number of documents we want to read then stop
        if docs > numDocuments:
            break

        # split the file line to a list and get the first 2 columns (docID and wordID)
        list = data[i].split(" ")
        docID = list[0]
        wordID = list[1]

        if int(docID) > k:
            k += 1

        # check if we changed docID then increase the docs number to check it for the next
        if previousDocID < int(docID):
            docs += 1

        previousDocID = int(docID)

        if k < numDocuments + 1:
            docDict[k].append(wordID)

    # get the end time
    et = time.time()

    # get the execution time
    elapsed_time = et - st
    print('Execution time:', elapsed_time, 'seconds')


def MyJacSimWithSets(docID1, docID2):
    """ fast way
    docInDict1 = docDict.get(docID1)
    docInDict2 = docDict.get(docID2)
    return len(set(docInDict1).intersection(docInDict2)) / len(set(docInDict1).union(docInDict2))
    """
    intersectionCounter = 0
    doc1set = frozenset(docDict.get(docID1))
    doc2set = frozenset(docDict.get(docID2))

    for wordID1 in doc1set:
        for wordID2 in doc2set:
            if wordID1 == wordID2:
                intersectionCounter += 1

    unionCounter = (len(doc1set) + len(doc2set)) - intersectionCounter

    jacSim = intersectionCounter / unionCounter

    print("Intersection1= ", intersectionCounter)
    print("Union1= ", unionCounter)
    return jacSim


def MyJacSimWithOrderedLists(docID1, docID2):
    pos1 = 0
    pos2 = 0
    intersectionCounter = 0

    doc1List = list(docDict.get(docID1))
    doc2List = list(docDict.get(docID2))
    sizeOfDoc1 = len(doc1List)
    sizeOfDoc2 = len(doc2List)

    while pos1 < sizeOfDoc1 and sizeOfDoc2 < pos2:
        if doc1List[pos1] == doc2List[pos2]:
            intersectionCounter += 1
            pos1 += 1
            pos2 += 1
        else:
            if doc1List[pos1] < doc2List[pos2]:
                pos1 += 1
            else:
                pos2 += 1

    unionCounter = (sizeOfDoc1 + sizeOfDoc2) - intersectionCounter

    jacSim = intersectionCounter / unionCounter

    print("Intersection2= ", intersectionCounter)
    print("Union2= ", unionCounter)
    return jacSim


def main():
    MyReadDataRoutine()
    jac1 = MyJacSimWithSets(1000, 222)
    print("JacSim1= ", jac1)
    jac2 = MyJacSimWithOrderedLists(1000, 222)
    print("JacSim2= ", jac2)


if __name__ == "__main__":
    main()
