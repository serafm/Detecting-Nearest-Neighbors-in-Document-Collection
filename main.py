import sys


def listToString(s):
    # initialize an empty string
    str1 = ""

    # traverse in the string
    for ele in s:
        str1 += ele

        # return string
    return str1

def MyReadDataRoutine():

    # Get the file path and num of docs from terminal
    #dataFilePath = sys.argv[1]
    #numDocuments = sys.argv[2]

    # file to read the data
    file = open("data/DATA_1-docword.enron.txt")

    # new file to write later
    newFile = open("FrozenDataSet.txt", "w")

    # number of documents to read
    numDocuments = 10

    docs = 1
    previousDocID = 1

    data = file.read()
    data = data.split("\n")

    # remove the first 3 lines we don't need them here
    data.pop(0)
    data.pop(0)
    data.pop(0)

    frozenData = []
    string = []

    for i in range(len(data)-1):

        # if we pass the number of documents we want to read then stop
        if docs > numDocuments:
            break

        # split the file line to a list and get the first 2 columns (docID and wordID)
        list = data[i].split(" ")
        docID = list[0]
        wordID = list[1]

        # we need it to write after in file
        string = string + [docID + " : " + wordID + "\n"]

        # add tuple of docID and wordID in list
        frozenData = frozenData + [(docID, wordID)]

        # check if we changed docID then increase the docs number to check it for the next
        if previousDocID < int(docID):
            docs += 1

        previousDocID = int(docID)


    # remove the last tuple from list because its not in range of the number of documents
    frozenData.pop(-1)

    # convert list of tuples to frozenset
    frozenSet = frozenset(frozenData)

    # no need we remove the last element
    string.pop(-1)

    # convert list to string to save it in file
    fstring = listToString(string)

    # write the string in file
    newFile.write(fstring)



def main():
    MyReadDataRoutine()

if __name__ == "__main__":
    main()