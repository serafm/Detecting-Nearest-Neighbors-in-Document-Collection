import random

global hashLSH, LSHdicts, sig

LSHdicts = []

lista = [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15]]

SIG = [[1, 4, 5, 3, 2, 7, 9, 10, 3, 3], [1, 4, 5, 3, 2, 4, 11, 8, 9, 1], [14, 2, 2, 1, 9, 4, 11, 8, 6, 1], [5, 2, 2, 1, 9, 4, 11, 8, 7, 1], [2, 4, 5, 3, 2, 7, 9, 10, 1, 3]]
K = 10


docID1 = [1,2,3,4,5,6,7,8,9,10]
docID2 = [2,3,4,5,6,7,1,9,8,10]


def create_random_hash_function(p=2 ** 33 - 355, m=2 ** 32 - 1):
    a = random.randint(1, p - 1)
    b = random.randint(0, p - 1)
    return lambda x: 1 + (((a * x + b) % p) % m)


def LSH(rowsPerBands):
    global SIG, LSHdicts, numBands

    numBands = int(K / rowsPerBands)
    temp = 0
    bucket = 1
    myDict = dict()
    pairs = []

    for b in range(numBands):
        for i in range(len(SIG)):
            signature = SIG[i]
            t = tuple(signature[b: b + rowsPerBands])
            myDict[i+1] = hash(t)

        randomHash = {x: hashLSH(myDict[x]) for x in myDict}
        print(randomHash)

        ordered = sorted(randomHash, key=randomHash.get)
        #print(ordered)

        # add docIDs in buckets
        for key in ordered:
            if temp == randomHash[key]:
                bucket = bucket - 1
                randomHash[key] = bucket
            temp = randomHash[key]
            randomHash[key] = bucket
            bucket += 1

        print(randomHash)

        for i in range(len(ordered) - 1):
            if randomHash[ordered[i]] == randomHash[ordered[i + 1]]:
                pairs.append((ordered[i], ordered[i+1]))

        myDict = dict()
        bucket = 1
        temp = 0

    print(pairs)


def MyJacSimWithOrderedLists(docID1, docID2):
    pos1 = 0
    pos2 = 0
    intersectionCounter = 0

    # make lists for the 2 docs
    doc1List = docID1
    doc2List = docID2

    while pos1 < len(doc1List) and pos2 < len(doc2List):
        if int(doc1List[pos1]) == int(doc2List[pos2]):
            intersectionCounter += 1
            pos1 += 1
            pos2 += 1
        else:
            if int(doc1List[pos1]) < int(doc2List[pos2]):
                pos1 += 1
            else:
                pos2 += 1

    unionCounter = (len(doc1List) + len(doc2List)) - intersectionCounter

    # Jaccard Similarity
    jacSimWithOrderedLists = intersectionCounter / unionCounter

    return jacSimWithOrderedLists


def BruteForce():

    numDocuments = 10
    calculatedDocs = []

    for docID in range(1, numDocuments+1):
        for otherDocID in range(2, numDocuments+1):
            if docID != otherDocID:
                calculatedDocs.append([docID, otherDocID])
                tempList = sorted([docID, otherDocID])
                if tempList not in calculatedDocs:
                    MyJacSimWithOrderedLists(docID, otherDocID)

def main():

    #global hashLSH
    #hashLSH = create_random_hash_function()
    #LSH(5)



    tempList = sorted([3, 1])
    print(tempList)



if __name__ == "__main__":
    main()
