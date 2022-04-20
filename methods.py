import linecache
import os
import time
import random
import collections
import Gui as user


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

# Number of permutation
# K = 20

# List of Signatures
SIG = []

# List of pairs from LSH
pairs = []


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
def MyReadDataRoutine(filepath, numDocuments):

    global readMsg, wordsDict

    # get the start time
    st = time.time()

    # filepath
    # filepath = "data/DATA_1-docword.enron.txt"

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
    # permutationFiles = open("permutationFiles.txt", "w")

    for num in range(1, K + 1):
        h = create_random_hash_function()
        randomHash = {x: h(x) for x in range(w)}
        myHashKeysOrderedByValues = sorted(randomHash, key=randomHash.get)
        myHash = {myHashKeysOrderedByValues[x]: x for x in range(w)}
        randomHashList.append(myHash)

        """
        filename = "randomHash" + str(num) + ".txt"
        if os.path.exists(filename):
            open(filename).flush()
        permutationFiles.write(filename + "\n")
        f = open(filename, "w")
        for i in myHash:
            string = str(i) + ":" + str(myHash[i]) + "\n"
            f.write(string)
        """
    randomHashList.pop(0)


# Create the Signature List
def MyMinHash(wordsDict, K, numDocuments):
    global SIG, permutationFileNames, elapsed_time_for_MyMinHash

    # get the start time
    st = time.time()

    # Open the file with the randomHash file names
    # permutationFiles = open("permutationFiles.txt")

    # Add the file names in a list
    # permutationFileNames = permutationFiles.read().split("\n")

    # remove the last element (is an empty string)
    # permutationFileNames.pop(-1)

    # randomHash = []
    # randomHashList = [[]]

    """
    for hash in range(K):
        for i in range(1, len(wordsDict)):
            randomHash.append(
                linecache.getline(str(permutationFileNames[hash]), i).replace("\n", "").replace(str(":" + str(i - 1)), ""))
        randomHashList.append(randomHash)
        randomHash = []
    """

    # randomHashList.pop(0)

    positionOfList = 1

    # Initialise SIG List
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
    elapsed_time_for_MyMinHash = "Execution time for signatures list creation: " + str(elapsed_time)
    # print('Execution time:', '%.3f' % elapsed_time, 'seconds for MyMinHash \n')
    # print(f"{font.WARNING}Signature table:{font.ENDC}\n", SIG, "\n")

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


# Find the nearest neighbors from a document
def AverageSimilarityOfAllDocumentsWithBruteForce():
    global numDocuments
    AvgSim = []

    for i in range(1, numDocuments + 1):
        avg = BruteForce(i)
        AvgSim.append(avg)

    AverageSim = (1/numDocuments)*sum(AvgSim)

    return AverageSim


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

    for doc in range(1, numDocuments + 1):
        if docID != doc:
            if selectedSimilarityMethod == 1:
                jaccardList.append(MyJacSimWithOrderedLists(docID, doc))
            elif selectedSimilarityMethod == 0:
                sigList.append(MySigSim(docID, doc, numPermutations))

    if selectedSimilarityMethod == 1:
        avg = sum(jaccardList)/numDocuments
    elif selectedSimilarityMethod == 0:
        avg = sum(sigList)/numDocuments

    return avg


def AverageSimilarityFromNearestNeighborsLSH():
    global myNeighborsPairsDict

    avg = sum(myNeighborsPairsDict.values())/numNeighbors

    return avg


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
        # print(randomHash)

        # Sort the dictionary
        ordered = sorted(LSHdicts, key=LSHdicts.get)
        # print(ordered)

        # add docIDs in buckets (Sera's Algorithm)
        for key in ordered:
            if temp == LSHdicts[key]:
                bucket = bucket - 1
                LSHdicts[key] = bucket
            temp = LSHdicts[key]
            LSHdicts[key] = bucket
            bucket += 1

        # print(colored("DocIDs:Bucket for Band:" + str(b+1), 'green') + "\n", LSHdicts)

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


"""
def main():
    MyReadDataRoutine()
    print(f"{font.WARNING}MyReadDataRoutine:{font.ENDC}")
    print(readMsg, "\n")

    print(f"{font.WARNING}MyJacSimWithSets for docs 1,2:{font.ENDC}")
    print("Jaccard: ", MyJacSimWithSets(1, 2), "\n")
    # print("Jaccard: ", MyJacSimWithOrderedLists(1, 2))

    # RandomHashForSignatures()

    print(f"{font.WARNING}MyMinHash:{font.ENDC}")
    MyMinHash(wordsDict, K)

    print(f"{font.WARNING}MySigSim for docs 1,2:{font.ENDC}")
    print("Sig: ", MySigSim(1, 2, 20))

    print(f"{font.WARNING}\nBruteForce DocID=1 :{font.ENDC}")
    print(f"{font.WARNING}Average Similarity:{font.ENDC}", BruteForce(1), "\n")

    print(f"{font.WARNING}Average Similarity for all documents:{font.ENDC}",
          AverageSimilarityOfAllDocumentsWithBruteForce())

    print(f"{font.WARNING}\nLSH:{font.ENDC}")
    print(f"{font.WARNING}\nPairs:{font.ENDC}", LSH(SIG, 1), "\n")

    print(CalculatePairsSimilarityFromLSH())


if __name__ == "__main__":
    main()
"""