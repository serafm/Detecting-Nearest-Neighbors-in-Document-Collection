import linecache
import time
import random
import collections
from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfile

global docDict, numDocuments, wordDict, SIG, file_path, readMsg
docDict = dict()
wordDict = dict()
numDocuments = 10
SIG = []


def create_random_hash_function(p=2 ** 33 - 355, m=2 ** 32 - 1):
    a = random.randint(1, p - 1)
    b = random.randint(0, p - 1)
    return lambda x: 1 + (((a * x + b) % p) % m)


def MyReadDataRoutine(filepath):
    global numDocuments, readMsg, wordDict

    # get the start time
    st = time.time()

    # file to read the data
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

            # add docIDs in wordIDs dictionary
            if int(wordID) in wordDict:
                wordDict[int(wordID)].append(int(docID))
            else:
                wordDict[int(wordID)] = []
                wordDict[int(wordID)].append(int(docID))

    sortedWordDict = collections.OrderedDict(sorted(wordDict.items()))

    # get the end time
    et = time.time()

    # get the execution time
    elapsed_time = et - st
    timeTaken = str(float(elapsed_time))

    readMsg = str('Read ' + str(numDocuments) + ' documents and added them in dictionary. Execution time: ' + str(
        timeTaken) + ' seconds for MyReadDataRoutine')


def MyJacSimWithSets(docID1, docID2):
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
    jacSim = intersectionCounter / unionCounter

    print("MyJacSimWithSets")
    print("Intersection=", intersectionCounter)
    print("Union=", unionCounter)

    # get the end time
    et = time.time()

    # get the execution time
    elapsed_time = et - st
    print('Execution time:', '%.3f' % elapsed_time, 'seconds for MyJacSimWithSets')

    return jacSim


def MyJacSimWithOrderedLists(docID1, docID2):
    # get the start time
    st = time.time()

    pos1 = 0
    pos2 = 0
    intersectionCounter2 = 0

    # make lists for the 2 docs
    doc1List = list(docDict.get(docID1))
    doc2List = list(docDict.get(docID2))
    sizeOfDoc1 = len(doc1List)
    sizeOfDoc2 = len(doc2List)

    while pos1 < sizeOfDoc1 and pos2 < sizeOfDoc2:
        if int(doc1List[pos1]) == int(doc2List[pos2]):
            intersectionCounter2 += 1
            pos1 += 1
            pos2 += 1
        else:
            if int(doc1List[pos1]) < int(doc2List[pos2]):
                pos1 += 1
            else:
                pos2 += 1

    unionCounter2 = (sizeOfDoc1 + sizeOfDoc2) - intersectionCounter2

    # Jaccard Similarity
    jacSim2 = intersectionCounter2 / unionCounter2

    print("MyJacSimWithOrderedLists")
    print("Intersection=", intersectionCounter2)
    print("Union=", unionCounter2)

    # get the end time
    et = time.time()

    # get the execution time
    elapsed_time = et - st
    print('Execution time:', '%.3f' % elapsed_time, 'seconds for MyJacSimWithOrderedLists')

    return jacSim2


def MyMinHash(wordDict):
    """
    w = len(wordDict)
    f = open("MyHash10.txt", "w")

    h = create_random_hash_function()
    randomHash = {x: h(x) for x in range(w)}

    myHashKeysOrderedByValues = sorted(randomHash, key=randomHash.get)
    myHash = {myHashKeysOrderedByValues[x]: x for x in range(w)}

    for i in myHash:
        string = str(i) + ":" + str(myHash[i]) + "\n"
        f.write(string)
        string = ""
    """

    # get the start time
    st = time.time()

    global numDocuments, SIG
    k = 7
    hashFile = ["MyHash1.txt", "MyHash2.txt", "MyHash3.txt", "MyHash4.txt", "MyHash5.txt", "MyHash6.txt", "MyHash7.txt",
                "MyHash8.txt", "MyHash9.txt", "MyHash10.txt"]

    randomHash = []
    randomHashList = [[]]

    for hash in range(k):
        for i in range(1, len(wordDict)):
            randomHash.append(
                linecache.getline(str(hashFile[hash]), i).replace("\n", "").replace(str(":" + str(i - 1)), ""))
        randomHashList.append(randomHash)
        randomHash = []
    randomHashList.pop(0)

    thesiPinaka = 1
    pos = 0

    for col in range(numDocuments):
        SIG.append([])
        for i in range(k):
            SIG[col].append(1000000)

    for word in wordDict:
        list = wordDict.get(word)
        for doc in range(len(list)):
            for j in range(k):
                for i in range(len(randomHashList[0])):
                    if thesiPinaka == int(randomHashList[j][i]):
                        if (i + 1) < SIG[int(list[pos]) - 1][j]:
                            SIG[int(list[pos]) - 1][j] = i + 1
                            break
            pos += 1
        thesiPinaka += 1
        pos = 0

    # get the end time
    et = time.time()

    # get the execution time
    elapsed_time = et - st
    print('Execution time:', '%.3f' % elapsed_time, 'seconds for MyMinHash')

    print(SIG)


def MySigSim(docID1, docID2, numPermutations):
    # get the start time
    st = time.time()

    count = 0
    docSig1 = SIG[docID1 - 1]
    docSig2 = SIG[docID2 - 1]

    for i in range(numPermutations):
        if docSig1[i] == docSig2[i]:
            count += 1

    sigSim = count / numPermutations

    # get the end time
    et = time.time()

    # get the execution time
    elapsed_time = et - st
    print('\nExecution time:', '%.3f' % elapsed_time, 'seconds for MySigSim')
    print("\nSigSim= ", sigSim)


def GUI():
    mainWindow = Tk()
    mainWindow.title('Detect Nearest Neighbors from Document Collection')
    mainWindow.geometry('600x600')

    def open_file():
        global file_path
        file_path = askopenfile(mode='r', filetypes=[("Text Files", "*.txt")])
        filepath = str(file_path).replace("<_io.TextIOWrapper name='", "").replace("' mode='r' encoding='cp1253'>", "")

        if file_path is None:
            pass

        progressBar = Progressbar(mainWindow, orient=HORIZONTAL, length=300, mode='determinate')
        progressBar.grid(row=1, columnspan=3, pady=20)

        for i in range(5):
            mainWindow.update_idletasks()
            progressBar['value'] += 20
            time.sleep(0.2)

        progressBar.destroy()
        Label(mainWindow, text='File Uploaded Successfully!', foreground='green').grid(row=1, columnspan=3, pady=10)

        MyReadDataRoutine(filepath)
        readMsgLabel = Label(mainWindow, text=readMsg)
        readMsgLabel.grid(row=2, column=0)

        jac1 = MyJacSimWithSets(1, 2)
        jaccardSimWithSetsLabel1 = Label(mainWindow, text="Jaccard Similarity with sets:")
        jaccardSimWithSetsLabel1.grid(row=3, column=0)
        jaccardSimWithSetsLabel2 = Label(mainWindow, text=jac1)
        jaccardSimWithSetsLabel2.grid(row=3, column=1)

        jac2 = MyJacSimWithOrderedLists(1, 2)
        jaccardSimWithOrderedListsLabel1 = Label(mainWindow, text="Jaccard Similarity with ordered lists:")
        jaccardSimWithOrderedListsLabel1.grid(row=4, column=0)
        jaccardSimWithOrderedListsLabel2 = Label(mainWindow, text=jac2)
        jaccardSimWithOrderedListsLabel2.grid(row=4, column=1)

        MyMinHash(wordDict)
        MySigSim(2, 5, 7)

    uploadFileLabel = Label(mainWindow, text='Upload file to analyze')
    uploadFileLabel.grid(row=0, column=0, padx=10)
    uploadFileLabel.config(font=("Arial", 12, "bold"))

    uploadFileButton = Button(mainWindow, text='Choose File', command=lambda: open_file())
    uploadFileButton.grid(row=0, column=1)

    mainWindow.mainloop()


def main():
    GUI()


if __name__ == "__main__":
    main()
