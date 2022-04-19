import linecache
import os
import time
import random
import collections
from termcolor import colored


global docDict, numDocuments, wordsDict, SIG, file_path, readMsg, myNeighborsDict, docDistance, K, permutationFileNames, hashLSH, numBands, rowsPerBand

# Dictionary key:docID, value:wordIDs
docDict = dict()

# Dictionary key:wordID, value:docIDs
wordsDict = dict()

# Dictionary key:docID, value:Similarity
myNeighborsDict = dict()

# Dictionary key:docID, value:distance from a docID
docDistance = dict()

# Number of documents to read
numDocuments = 20

# Number of permutation
K = 20

# List of Signatures
SIG = []


# Fonts and Colors for output terminal
class font:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Random Hash Function
def create_random_hash_function(p=2 ** 33 - 355, m=2 ** 32 - 1):
    a = random.randint(1, p - 1)
    b = random.randint(0, p - 1)
    return lambda x: 1 + (((a * x + b) % p) % m)


hashLSH = create_random_hash_function()


# Function to read the documents
def MyReadDataRoutine():
    global numDocuments, readMsg, wordsDict

    # get the start time
    st = time.time()

    # filepath
    filepath = "data/DATA_1-docword.enron.txt"

    # open file
    file = open(filepath)

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
    k = 0

    # set the dictionary with keys and value an empty list
    for docId in range(1, numDocuments + 1):
        docDict[docId] = []

    # Add documents in dictionary
    for i in range(len(data) - 1):

        # if we pass the number of documents we want to read then stop
        if docs > numDocuments:
            break

        # split the file line to a list and get the first 2 columns (docID and wordID)
        list = data[i].split(" ")
        docID = list[0]
        wordID = list[1]

        # check if we changed docID
        if int(docID) > k:
            k += 1

        # check if we changed docID then increase the docs number to check it for the next
        if previousDocID < int(docID):
            docs += 1

        previousDocID = int(docID)

        # if the docID we read now is not bigger the the number of documents then add it in the dictionary
        if k < numDocuments + 1:
            docDict[k].append(wordID)

            # add docIDs in wordIDs dictionary
            if int(wordID) in wordsDict:
                wordsDict[int(wordID)].append(int(docID))
            else:
                wordsDict[int(wordID)] = []
                wordsDict[int(wordID)].append(int(docID))

    # Sorted dictionary wordsDict
    sortedWordsDict = collections.OrderedDict(sorted(wordsDict.items()))

    # get the end time
    et = time.time()

    # get the execution time
    elapsed_time = et - st
    timeTaken = str(float(elapsed_time))

    readMsg = str('Read ' + str(numDocuments) + ' documents and added them in dictionary. Execution time: ' + str(
        timeTaken) + ' seconds for MyReadDataRoutine')
    #print("DocDict:\n", docDict)


# Jaccard Similarity of 2 Documents with double for-loop
def MyJacSimWithSets(docID1, docID2):
    intersectionCounter = 0
    # make frozensets for the 2 docs
    doc1set = frozenset(docDict.get(docID1))
    doc2set = frozenset(docDict.get(docID2))

    for wordID1 in doc1set:
        for wordID2 in doc2set:
            if wordID1 == wordID2:
                intersectionCounter += 1

    unionCounter = (len(doc1set) + len(doc2set)) - intersectionCounter

    # Jaccard Similarity
    jacSimWithSets = intersectionCounter / unionCounter

    return jacSimWithSets


# Jaccard Similarity of 2 Documents with pointers
def MyJacSimWithOrderedLists(docID1, docID2):
    pos1 = 0
    pos2 = 0
    intersectionCounter = 0

    # make lists for the 2 docs
    doc1List = list(docDict.get(docID1))
    doc2List = list(docDict.get(docID2))

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


# Random Hash Function for Permutations
def RandomHashForSignatures():
    w = len(wordsDict)
    permutationFiles = open("permutationFiles.txt", "w")

    for num in range(1, K + 1):
        h = create_random_hash_function()
        randomHash = {x: h(x) for x in range(w)}
        myHashKeysOrderedByValues = sorted(randomHash, key=randomHash.get)
        myHash = {myHashKeysOrderedByValues[x]: x for x in range(w)}

        filename = "randomHash" + str(num) + ".txt"
        if os.path.exists(filename):
            open(filename).flush()
        permutationFiles.write(filename + "\n")
        f = open(filename, "w")
        for i in myHash:
            string = str(i) + ":" + str(myHash[i]) + "\n"
            f.write(string)


# Create the Signature List
def MyMinHash(wordsDict, K):
    global numDocuments, SIG, permutationFileNames

    # get the start time
    st = time.time()

    # Open the file with the randomHash file names
    permutationFiles = open("permutationFiles.txt")

    # Add the file names in a list
    permutationFileNames = permutationFiles.read().split("\n")

    # remove the last element (is an empty string)
    permutationFileNames.pop(-1)

    randomHash = []
    randomHashList = [[]]

    for hash in range(K):
        for i in range(1, len(wordsDict)):
            randomHash.append(
                linecache.getline(str(permutationFileNames[hash]), i).replace("\n", "").replace(str(":" + str(i - 1)),
                                                                                                ""))
        randomHashList.append(randomHash)
        randomHash = []
    randomHashList.pop(0)

    positionOfList = 1

    # Arxikopoiisi tou pinaka SIG
    for col in range(numDocuments):
        SIG.append([])
        for i in range(K):
            SIG[col].append(1000000)

    for word in wordsDict:
        list = wordsDict.get(word)
        for doc in list:
            for j in range(K):
                for i in range(len(randomHashList[0])):
                    if positionOfList == int(randomHashList[j][i]):
                        if (i + 1) < SIG[doc - 1][j]:
                            SIG[doc - 1][j] = i + 1
                            break
        positionOfList += 1

    # get the end time
    et = time.time()

    # get the execution time
    elapsed_time = et - st
    print('Execution time:', '%.3f' % elapsed_time, 'seconds for MyMinHash \n')
    print(f"{font.WARNING}Signature table:{font.ENDC}\n", SIG, "\n")


# Calculate Similarity from Signatures
def MySigSim(docID1, docID2, numPermutations):
    global K
    count = 0
    docSig1 = SIG[docID1 - 1]
    docSig2 = SIG[docID2 - 1]

    for i in range(numPermutations):
        if docSig1[i] == docSig2[i]:
            count += 1

    sigSim = count/(len(docSig1)+len(docSig2))

    return sigSim


# Find the nearest neighbors from a document
def NearestNeighbors(docID):
    global docDistance
    numNeighbors = 5
    i = 0
    SigSimList = []
    JacSimList = []

    for d in range(1, numDocuments + 1):
        if d != docID:
            SigSimList.append(MySigSim(docID, d, K))
            JacSimList.append(MyJacSimWithOrderedLists(docID, d))
            distance = 1 - MyJacSimWithOrderedLists(docID, d)
            if d not in docDistance:
                docDistance[d] = distance

    orderedDistanceDict = {k: v for k, v in sorted(docDistance.items(), key=lambda item: item[1])}

    for doc in orderedDistanceDict:
        if i < numNeighbors:
            myNeighborsDict[doc] = JacSimList[doc - 2]
            i += 1

    return myNeighborsDict


def BruteForce():
    AvgSimList = []
    tempDict = dict()
    numNeighbors = 5
    sum = 0
    allDocAvg = 0

    for i in range(1, numDocuments + 1):
        tempDict = NearestNeighbors(i)
        for doc in tempDict:
            sum = sum + tempDict.get(doc)
        tempAvg = sum / numNeighbors
        allDocAvg += tempAvg
        AvgSimList.append(tempAvg)
        sum = 0

    AvgSim = allDocAvg / numDocuments

    return "Average= " + str(AvgSim) + "\n"


def LSH(rowsPerBands):
    global SIG, numBands

    # Number of Bands
    numBands = int(K / rowsPerBands)

    temp = 0
    bucket = 1
    myDict = dict()
    pairs = []

    # add docIDs in buckets using hashLSH
    for b in range(numBands):
        # Get all the docIDs signatures for every band and add it in a bucket
        for i in range(len(SIG)):
            signature = SIG[i]
            # make a docID signature from list to tuple. Now we can hash the signature
            t = tuple(signature[b: b + rowsPerBands])
            myDict[i + 1] = hash(t)

        # hashLSH
        randomHash = {x: hashLSH(myDict[x]) for x in myDict}
        # print(randomHash)

        # Sort the dictionary
        ordered = sorted(randomHash, key=randomHash.get)
        # print(ordered)

        # add docIDs in buckets
        for key in ordered:
            if temp == randomHash[key]:
                bucket = bucket - 1
                randomHash[key] = bucket
            temp = randomHash[key]
            randomHash[key] = bucket
            bucket += 1

        print(colored("DocIDs:Bucket for Band:" + str(b+1), 'green') + "\n", randomHash)


        # Find pairs
        for i in range(len(ordered) - 1):
            # print(randomHash[ordered[i]])
            if randomHash[ordered[i]] == randomHash[ordered[i + 1]]:
                tup = (ordered[i], ordered[i + 1])
                if tup not in pairs:
                    pairs.append(tup)

        myDict = dict()
        bucket = 1
        temp = 0

    checked = []
    doc = 1
    numNeighbors = 5
    sum = 0
    allDocAvg = 0

    for pair in pairs:
        p = list(pair)
        if doc == p[0]:
            if p[0] not in checked:
                n = NearestNeighbors(p[0])
                for doc in n:
                    sum = sum + n.get(doc)

                tempAvg = sum / numNeighbors
                allDocAvg += tempAvg
                sum = 0
                AvgSim = allDocAvg / numDocuments
                print("AVG=", AvgSim)

            """if p[1] not in checked:
                n2 = NearestNeighbors(p[1])
                for doc in n:
                    sum = sum + n.get(doc)

                tempAvg = sum / numNeighbors
                allDocAvg += tempAvg
                sum = 0
                AvgSim = allDocAvg / numDocuments
                print("AVG=", AvgSim)"""


    if len(pairs) == 0:
        print("\nNo pairs found")
    else:
        print(f"{font.WARNING}\nPairs:{font.ENDC}", pairs)



def main():

    MyReadDataRoutine()
    print(f"{font.WARNING}MyReadDataRoutine:{font.ENDC}")
    print(readMsg, "\n")

    print(f"{font.WARNING}MyJacSimWithSets for docs 1,2:{font.ENDC}")
    print("Jaccard: ", MyJacSimWithSets(1, 2), "\n")
    # print("Jaccard: ", MyJacSimWithOrderedLists(1, 2))

    # RandomHashForSignatures()

    print(f"{font.WARNING}MyMinHash:{font.ENDC}")
    MyMinHash(wordsDict,K)

    print(f"{font.WARNING}MySigSim for docs 1,2:{font.ENDC}")
    print("Sig: ", MySigSim(1, 2, 20))

    print(f"{font.WARNING}\nBruteForce:{font.ENDC}")
    print(BruteForce())

    print(f"{font.WARNING}LSH:{font.ENDC}")
    LSH(1)


if __name__ == "__main__":
    main()
