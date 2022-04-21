import time
import random
import collections


"""
1. MyReadDataRoutine(): Opens the data file and reads the number of documents you want 
   to find the Similarity-Nearest Neighbors 
2. MyJacSimWithSets(): Calculate the Jaccard Similarity of 2 Documents with a double for-loop
3. MyJacSimWithOrderedLists(): Calculate the Jaccard Similarity of 2 Documents 
   with pointers (faster method than a double for-loop) 
4. RandomHashForSignatures(): This function creates Random Hashes (Permutations) for the signatures
   and save them in a txt file
5. MyMinHash(): Create a Signature List of Lists with Rows: WordIDs and Columns: DocIDs
6. MySigSim(): Calculate the Similarity of 2 Signatures row to row
7. AverageSimilarityOfAllDocumentsWithBruteForce(): Find the Average Similarity of all documents you 
   selected from the Average Similarity of every documents from Brute Force method
8. BruteForce(): Find the Average Similarity of nearest Neighbors
9. CalculatePairsSimilarityFromLSH(): Calculate the Similarity of pairs that LSH found
10. AverageSimilarity(): Just the Average Similarity of all Documents
11. LSH(): Find similar documents using bands and buckets and extract pairs of documents that might be very similar
"""


global docDict, numDocuments, wordsDict, SIG, file_path, numPermutations, myNeighborsPairsDict
global readMsg, myNeighborsDict, docDistance, K, permutationFileNames, numNeighbors, selectedSimilarityMethod
global hashLSH, numBands, rowsPerBand, pairs, elapsed_time_for_MyMinHash, elapsed_time_bruteForce, randomHashList
global elapsed_time_for_SigSim, elapsed_time_for_jacSimWithOrderedLists, elapsed_time_for_jacSimWithSets

# Dictionary key:docID, value:wordIDs
docDict = dict()

# Dictionary key:wordID, value:docIDs
wordsDict = dict()

# Dictionary key:docID, value:Similarity
myNeighborsDict = dict()
myNeighborsPairsDict = dict()

# Dictionary key:docID, value:distance from a docID
docDistance = dict()

# Random Hash List
randomHashList = [[]]

# List of Signatures
SIG = []

# List of pairs from LSH
pairs = []


# Random Hash Function
def create_random_hash_function(p=2 ** 33 - 355, m=2 ** 32 - 1):
    a = random.randint(1, p - 1)
    b = random.randint(0, p - 1)
    return lambda x: 1 + (((a * x + b) % p) % m)


# create random hash for LSH buckets
hashLSH = create_random_hash_function()


# Function to read the documents
def MyReadDataRoutine(filepath, numDocuments):

    global readMsg, wordsDict

    # get the start time
    st = time.time()

    # open file
    file = open(filepath)

    # Counters for docs
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

    readMsg = str('Read ' + str(numDocuments) + ' documents and added them in dictionary.\nExecution time: ' + str(timeTaken) + ' seconds')
    # print("DocDict:\n", docDict)


# Jaccard Similarity of 2 Documents with double for-loop
def MyJacSimWithSets(docID1, docID2):
    global elapsed_time_for_jacSimWithSets

    # get the start time
    st = time.time()

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

    # get the end time
    et = time.time()

    # get the execution time
    elapsed_time = et - st
    elapsed_time_for_jacSimWithSets = "Execution time for Jaccard Similarity With Ordered Lists: " + str(elapsed_time)

    return jacSimWithSets


# Jaccard Similarity of 2 Documents with pointers
def MyJacSimWithOrderedLists(docID1, docID2):
    global elapsed_time_for_jacSimWithOrderedLists

    # get the start time
    st = time.time()

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

    # get the end time
    et = time.time()

    # get the execution time
    elapsed_time = et - st
    elapsed_time_for_jacSimWithOrderedLists = "Execution time for Jaccard Similarity With Ordered Lists: " + str(elapsed_time)

    return jacSimWithOrderedLists


# Random Hash Function for Permutations
def RandomHashForSignatures(K):
    w = len(wordsDict)

    for num in range(1, K + 1):
        h = create_random_hash_function()
        randomHash = {x: h(x) for x in range(w)}
        myHashKeysOrderedByValues = sorted(randomHash, key=randomHash.get)
        myHash = {myHashKeysOrderedByValues[x]: x for x in range(w)}
        keys = list(myHash.keys())
        keys.remove(0)
        randomHashList.append(keys)

    randomHashList.pop(0)


# Create the Signature List
def MyMinHash(wordsDict, K, numDocuments):
    global SIG, permutationFileNames, elapsed_time_for_MyMinHash, randomHashList

    # get the start time
    st = time.time()

    # Initialise SIG List
    for col in range(numDocuments):
        SIG.append([])
        for i in range(K):
            SIG[col].append(1000000)

    wordsDictAsListsOfValues = list(wordsDict.values())
    r = 1

    for row in range(len(wordsDictAsListsOfValues)):
        tempList = wordsDictAsListsOfValues[row]
        for col in range(len(tempList)):
            for k in range(len(randomHashList)):
                if row == len(wordsDictAsListsOfValues) - 1:
                    r = len(wordsDictAsListsOfValues) - 1
                position = randomHashList[k].index(r) + 1
                if position < SIG[tempList[col] - 1][k]:
                    SIG[tempList[col] - 1][k] = position
        r += 1

    # get the end time
    et = time.time()

    # get the execution time
    elapsed_time = et - st
    elapsed_time_for_MyMinHash = "Execution time for signatures list creation: " + str(elapsed_time)

    return SIG


# Calculate Similarity from Signatures
def MySigSim(docID1, docID2, numPermutations):

    # get the start time
    st = time.time()

    global K, elapsed_time_for_SigSim
    count = 0
    docSig1 = SIG[docID1 - 1]
    docSig2 = SIG[docID2 - 1]

    for i in range(numPermutations):
        if docSig1[i] == docSig2[i]:
            count += 1

    sigSim = count/K

    # get the end time
    et = time.time()

    # get the execution time
    elapsed_time = et - st
    elapsed_time_for_SigSim = "Execution time for 2 Signatures Similarity: " + str(elapsed_time)

    return sigSim


def BruteForce(docID):
    global myNeighborsDict, numDocuments, elapsed_time_bruteForce, numNeighbors, numPermutations, selectedSimilarityMethod

    docsDistanceDict = dict()
    jaccardSimList = []
    sigSimList = []

    # get the start time
    st = time.time()

    for otherDocID in range(1, numDocuments + 1):
        if docID != otherDocID:
            if selectedSimilarityMethod == 1:
                jaccardSimList.append(MyJacSimWithOrderedLists(docID, otherDocID))
                distance = 1 - MyJacSimWithOrderedLists(docID, otherDocID)
                docsDistanceDict[otherDocID] = distance
            elif selectedSimilarityMethod == 0:
                sigSimList.append(MySigSim(docID, otherDocID, numPermutations))
                distance = 1 - MySigSim(docID, otherDocID, numPermutations)
                docsDistanceDict[otherDocID] = distance

    orderedDocsDistanceDict = {k: v for k, v in sorted(docsDistanceDict.items(), key=lambda item: item[1])}

    n = 0

    # Get the first N Neighbors from Distance Dictionary
    for doc in orderedDocsDistanceDict:
        if selectedSimilarityMethod == 1:
            if n < numNeighbors:
                myNeighborsDict[doc] = jaccardSimList[doc - 2]
                n += 1
        elif selectedSimilarityMethod == 0:
            if n < numNeighbors:
                myNeighborsDict[doc] = sigSimList[doc - 2]
                n += 1

    AvgSimOfNeighbors = sum(myNeighborsDict.values())/len(myNeighborsDict)

    # get the end time
    et = time.time()

    # get the execution time
    elapsed_time = et - st
    elapsed_time_bruteForce = 'Execution time: ' + str(elapsed_time) + ' seconds for BruteForce'

    return AvgSimOfNeighbors


# Find the nearest neighbors from a document
def AverageSimilarityOfAllDocumentsWithBruteForce():
    global numDocuments
    AvgSim = []

    for i in range(1, numDocuments + 1):
        avg = BruteForce(i)
        AvgSim.append(avg)

    AverageSim = (1/numDocuments)*sum(AvgSim)

    return AverageSim


def LSH(rowsPerBand):
    global numBands, pairs, SIG

    # Number of Bands
    numBands = int(K / rowsPerBand)

    neighborsDict = dict()

    temp = 0
    bucket = 1
    tempDict = dict()
    LSHdicts = dict()

    # add docIDs in buckets using hashLSH
    for b in range(numBands):
        # Get all the docIDs signatures for every band and add it in a bucket
        for i in range(len(SIG)):
            signature = SIG[i]
            # make a docID signature from list to tuple. Now we can hash the signature
            t = tuple(signature[b: b + rowsPerBand])
            tempDict[i + 1] = hash(t)

        # hashLSH
        LSHdicts = {x: hashLSH(tempDict[x]) for x in tempDict}

        # Sort the dictionary
        ordered = sorted(LSHdicts, key=LSHdicts.get)

        # add docIDs in buckets (Sera's Algorithm)
        for key in ordered:
            if temp == LSHdicts[key]:
                bucket = bucket - 1
                LSHdicts[key] = bucket
            temp = LSHdicts[key]
            LSHdicts[key] = bucket
            bucket += 1

        # Find pairs
        for i in range(len(ordered) - 1):
            # print(randomHash[ordered[i]])
            if LSHdicts[ordered[i]] == LSHdicts[ordered[i + 1]]:
                tup = (ordered[i], ordered[i + 1])
                if tup not in pairs:
                    pairs.append(tup)

        tempDict = dict()
        bucket = 1
        temp = 0

    if len(pairs) == 0:
        print("\nNo pairs found")

    pairs = sorted(pairs)

    return pairs


def CalculatePairsDistanceFromLSH():
    global rowsPerBand, numBands, pairs, myNeighborsPairsDict, numNeighbors, selectedSimilarityMethod

    distanceDict = dict()
    jaccardSimList = []
    sigSimList = []

    # threshold
    # s = pow((1/numBands), (1/rowsPerBand))

    # Find similarity with one of the following methods
    for pair in pairs:
        p = list(pair)
        docID1 = p[0]
        docID2 = p[1]
        if selectedSimilarityMethod == 1:
            jaccard = MyJacSimWithOrderedLists(docID1, docID2)
            distance = 1 - jaccard
            jaccardSimList.append(jaccard)
            distanceDict[pair] = distance
        elif selectedSimilarityMethod == 0:
            sigSim = MySigSim(docID1, docID2, numPermutations)
            distance = 1 - sigSim
            sigSimList.append(sigSim)
            distanceDict[pair] = distance

    orderedDocsDistanceDict = {k: v for k, v in sorted(distanceDict.items(), key=lambda item: item[1])}

    n = 0
    i = 0

    # Get the first N Neighbors from Distance Dictionary
    for pair in orderedDocsDistanceDict:
        if selectedSimilarityMethod == 1:
            if n < numNeighbors:
                myNeighborsPairsDict[pair] = jaccardSimList[i]
                n += 1
                i += 1
        elif selectedSimilarityMethod == 0:
            if n < numNeighbors:
                myNeighborsPairsDict[pair] = sigSimList[i]
                n += 1
                i += 1
    i = 0

    return distanceDict


def AverageSimilarityForADocument(docID):
    global selectedSimilarityMethod

    jaccardList = []
    sigList = []

    # Find Jaccard Similarity or Signature of a docID with all the other docIDs
    for doc in range(1, numDocuments + 1):
        if docID != doc:
            if selectedSimilarityMethod == 1:
                jaccardList.append(MyJacSimWithOrderedLists(docID, doc))
            elif selectedSimilarityMethod == 0:
                sigList.append(MySigSim(docID, doc, numPermutations))

    # Find average similarity for a docID
    if selectedSimilarityMethod == 1:
        avg = sum(jaccardList)/numDocuments
    elif selectedSimilarityMethod == 0:
        avg = sum(sigList)/numDocuments

    return avg


def AverageSimilarityFromNearestNeighborsLSH():
    global myNeighborsPairsDict

    avg = sum(myNeighborsPairsDict.values())/numNeighbors

    return avg
