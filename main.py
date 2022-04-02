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




def main():
    MyReadDataRoutine()


if __name__ == "__main__":
    main()
