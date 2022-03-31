import sys

import numpy as np


def MyReadDataRoutine():

    # Get the file path and num of docs from terminal
    #dataFilePath = sys.argv[1]
    #numDocuments = sys.argv[2]

    file = open("data/DATA_1-docword.enron.txt")
    numDocuments = 100

    data = file.read()
    data = data.split("\n")

    # remove the first 3 lines
    data.pop(0)
    data.pop(0)
    data.pop(0)

    frozenData = []

    for i in range(len(data)-1):
        list = data[i].split(" ")
        docID = list[0]
        wordID = list[1]
        frozenData = frozenData + [docID, wordID]

    frozeSet = frozenset(frozenData)
    print(frozeSet)









def main():
    MyReadDataRoutine()

if __name__ == "__main__":
    main()