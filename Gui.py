import os
import time
from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfile
import methods

global numDocuments, filepath, numNeighbors, K, jacSimCheck, sigSimCheck
global bruteForceCheck, LSHCheck, mainWindow, rowsPerBandCheck, rowsPerBand
global jaccardWindow, isClicked

isClicked = False


def GUI():
    global mainWindow, jacSimCheck, sigSimCheck, bruteForceCheck, LSHCheck, rowsPerBandCheck

    mainWindow = Tk()

    jacSimCheck = IntVar()
    sigSimCheck = IntVar()
    bruteForceCheck = IntVar()
    LSHCheck = IntVar()
    rowsPerBandCheck = IntVar()

    mainWindow.title('Detect Nearest Neighbors from Document Collection')
    mainWindow.geometry('1920x1080')

    uploadFileLabel = Label(mainWindow, text='Upload file to analyze')
    uploadFileLabel.grid(row=0, column=0, padx=10)
    uploadFileLabel.config(font=("Arial", 12, "bold"))

    uploadFileButton = Button(mainWindow, text='Choose File', command=lambda: open_file())
    uploadFileButton.grid(row=0, column=1)

    mainWindow.mainloop()


# Select the file path from a pop-up window and check if it's valid
def open_file():
    global filepath

    file_path = askopenfile(mode='r', filetypes=[("Text Files", "*.txt")])
    filepath = str(file_path).replace("<_io.TextIOWrapper name='", "").replace("' mode='r' encoding='cp1253'>", "")

    if file_path is None:
        pass

    progressBar = Progressbar(mainWindow, orient=HORIZONTAL, length=300, mode='determinate')
    progressBar.grid(row=1, columnspan=3, pady=20)

    for i in range(5):
        mainWindow.update_idletasks()
        progressBar['value'] += 20
        time.sleep(0.1)

    progressBar.destroy()
    msg = 'File with name:  ' + str(os.path.basename(filepath)) + '  uploaded successfully!'
    Label(mainWindow, text=msg, foreground='green').grid(row=1, columnspan=3, pady=10)

    Info()


# Get information from the User about the document
def Info():
    global numDocuments, numNeighbors, K, jacSimCheck, sigSimCheck, bruteForceCheck, LSHCheck


    # Label and TextBox to write the number of documents
    numDocumentsLabel = Label(mainWindow, text='Enter the number of documents:')
    numDocumentsLabel.grid(row=2, column=0)
    numDocumentsLabel.config(font=("Arial", 9, "bold"))

    numDocumentsTextBox = Text(mainWindow, height=1, width=5)
    numDocumentsTextBox.grid(row=2, column=1)

    # Label and TextBox to write the number of Neighbors to find
    numNeighborsLabel = Label(mainWindow, text='Enter the number of Neighbors to find for each Document(2,3,4 or 5):')
    numNeighborsLabel.grid(row=3, column=0)
    numNeighborsLabel.config(font=("Arial", 9, "bold"))

    numNeighborsTextBox = Text(mainWindow, height=1, width=5)
    numNeighborsTextBox.grid(row=3, column=1)

    # Label and TextBox to set number of permutations(K)
    numPermutationsLabel = Label(mainWindow, text='Set the number of permutations to build the signatures:')
    numPermutationsLabel.grid(row=4, column=0)
    numPermutationsLabel.config(font=("Arial", 9, "bold"))

    numPermutationsTextBox = Text(mainWindow, height=1, width=5)
    numPermutationsTextBox.grid(row=4, column=1)

    # Select Jaccard or Signature Similarity with check boxes
    msgSim = Label(mainWindow, text='Select one similarity method to use:')
    msgSim.grid(row=5, column=0)
    msgSim.config(font=("Arial", 9, "bold"))

    JacSimCheckBox = Checkbutton(mainWindow, text='Jaccard Similarity', variable=jacSimCheck, onvalue=1, offvalue=0)
    JacSimCheckBox.grid(row=5, column=1)

    SigSimCheckBox = Checkbutton(mainWindow, text='Signature Similarity', variable=sigSimCheck, onvalue=1, offvalue=0)
    SigSimCheckBox.grid(row=5, column=2)

    # Select Brute Force or LSH method to use with check boxes
    msgMethod = Label(mainWindow, text='Select one of the methods to calculate document similarities')
    msgMethod.config(font=("Arial", 9, "bold"))
    msgMethod.grid(row=6, column=0)

    bruteForceCheckBox = Checkbutton(mainWindow, text='Brute Force', variable=bruteForceCheck, onvalue=1, offvalue=0)
    bruteForceCheckBox.grid(row=6, column=1)

    LSHCheckBox = Checkbutton(mainWindow, text='LSH', variable=LSHCheck, onvalue=1, offvalue=0)
    LSHCheckBox.grid(row=6, column=2)


    # Submit Button
    infoButton = Button(mainWindow, text='Submit', command=lambda: ReadDocuments(numDocumentsTextBox, numNeighborsTextBox, numPermutationsTextBox))
    infoButton.grid(row=7, column=1)

    newWindow = Button(mainWindow, text='Calculate Similarity Here', command=lambda: JaccardMethodsWindow())
    newWindow.grid(row=5, column=5)



def ReadDocuments(numDocumentsTextBox, numNeighborsTextBox, numPermutationsTextBox):
    global numDocuments, numNeighbors, K, filepath
    onetime = True

    numDocuments = numDocumentsTextBox.get("1.0", END)
    numNeighbors = numNeighborsTextBox.get("1.0", END)
    K = numPermutationsTextBox.get("1.0", END)
    methods.K = int(K)
    methods.numDocuments = int(numDocuments)
    methods.numNeighbors = int(numNeighbors)
    methods.numPermutations = int(K)

    error = Label(mainWindow, text='Error. Number of Neighbors must be at least 5!', foreground='red')

    if int(numNeighbors) > 5:
        error.grid(row=3, column=2)
    else:
        error.grid_remove()
        numDocuments = numDocumentsTextBox.get("1.0", END)
        numNeighbors = numNeighborsTextBox.get("1.0", END)
        K = numPermutationsTextBox.get("1.0", END)

        # execute MyReadDataRoutine()
        methods.MyReadDataRoutine(filepath, int(numDocuments))
        # Time taken for read Docs
        Label(mainWindow, text=methods.readMsg, foreground='blue').grid(row=8, column=0)

        # execute RandomHashForSignatures() only one time
        methods.RandomHashForSignatures(int(K))

        if onetime:
            # execute MyMinHash() create Signatures list
            wordsDict = methods.wordsDict
            methods.MyMinHash(wordsDict, int(K), int(numDocuments))
            # Time taken for SIG creation
            Label(mainWindow, text=methods.elapsed_time_for_MyMinHash, foreground='blue').grid(row=9, column=0)
            onetime = False


        selectMethod()


def selectMethod():
    global jacSimCheck, sigSimCheck, LSHCheck, bruteForceCheck, numDocuments, numNeighbors, K, rowsPerBandCheck

    # LSH title
    lsh = Label(mainWindow, text='LSH method selected', foreground='blue')

    # Brute Force title
    bf = Label(mainWindow, text='Brute Force method selected', foreground='blue')

    if LSHCheck.get() == 1 and bruteForceCheck.get() == 0:
        bf.destroy()

        # Show LSH title
        lsh.config(font=("Arial", 12, "bold"))
        lsh.grid(row=10, column=0)

        # Space
        Label(mainWindow, text='').grid(row=11, column=0)

        # Enter rows per band
        rowsPerBandLabel = Label(mainWindow, text='Enter number of rows per band:')
        rowsPerBandLabel.config(font=("Arial", 9, "bold"))
        rowsPerBandLabel.grid(row=12, column=0)

        rowsPerBandTextBox = Text(mainWindow, height=1, width=5)
        rowsPerBandTextBox.grid(row=12, column=1)

        rowsPerBandLSHCheckBox = Checkbutton(mainWindow, text='Let LSH select number of rows for you', variable=rowsPerBandCheck, onvalue=1, offvalue=0)
        rowsPerBandLSHCheckBox.grid(row=12, column=2)

        # Submit Button
        submit = Button(mainWindow, text='Proceed', command=lambda: startLSH(rowsPerBandTextBox))
        submit.grid(row=14, column=1)

    if bruteForceCheck.get() == 1 and LSHCheck.get() == 0:
        lsh.destroy()

        # Show brute force title
        bf.config(font=("Arial", 12, "bold"))
        bf.grid(row=10, column=0)

        # Space
        Label(mainWindow, text='').grid(row=11, column=0)

        startBruteForce()


def startLSH(rowsPerBandTextBox):
    global rowsPerBand, rowsPerBandCheck

    # IF user checks the box to let LSH choose rows per band ELSE get the input rows from user
    if rowsPerBandCheck.get() == 1:
        rowsPerBand = int(K)/4
        methods.rowsPerBand = rowsPerBand
    elif rowsPerBandTextBox.get("1.0", END) is not None:
        rowsPerBand = rowsPerBandTextBox.get("1.0", END)
        methods.rowsPerBand = int(rowsPerBand)

    # LSH method with Jaccard Similarity OR Signatures Similarity (Question: 4a.)
    if jacSimCheck.get() == 1:

        methods.selectedSimilarityMethod = 1

        # get the start time
        st = time.time()

        methods.LSH(int(rowsPerBand))

        if methods.pairs == []:
            Label(mainWindow, text='No Pairs Found').grid(row=15, column=1)
        else:

            # Calculate Distance for pairs (Question 4a.)
            methods.CalculatePairsDistanceFromLSH()

            # Calculate AvgSim for nearest neighbors (Question 4b.)
            avgSim = methods.AverageSimilarityFromNearestNeighborsLSH()

            # get the end time
            et = time.time()

            # get the execution time
            elapsed_time_lsh = et - st


            # Show AvgSim and ExecTime (Question 5)
            avgLabel = Label(mainWindow, text='Average Similarity: ' + str(avgSim))
            avgLabel.grid(row=15, column=1)
            timeLabel = Label(mainWindow, text='Execution Time: ' + str(elapsed_time_lsh))
            timeLabel.grid(row=16, column=1)

    elif sigSimCheck.get() == 1:

        methods.selectedSimilarityMethod = 0

        # get the start time
        st = time.time()

        methods.LSH(int(rowsPerBand))

        if methods.pairs == []:
            Label(mainWindow, text='No Pairs Found').grid(row=15, column=1)
        else:

            # Calculate Distance for pairs (Question 4a.)
            methods.CalculatePairsDistanceFromLSH()

            # Calculate AvgSim for nearest neighbors (Question 4b.)
            avgSim = methods.AverageSimilarityFromNearestNeighborsLSH()

            # get the end time
            et = time.time()

            # get the execution time
            elapsed_time_lsh = et - st


            # Show AvgSim and ExecTime (Question 5)
            avgLabel = Label(mainWindow, text='Average Similarity: ' + str(avgSim))
            avgLabel.grid(row=15, column=1)
            timeLabel = Label(mainWindow, text='Execution Time: ' + str(elapsed_time_lsh))
            timeLabel.grid(row=16, column=1)


def startBruteForce():
    global numDocuments

    # Use Brute Force Jaccard Sim method (Question 4a.)
    if jacSimCheck.get() == 1:

        methods.selectedSimilarityMethod = 1

        # get the start time
        st = time.time()

        for i in range(1, int(numDocuments)+1):
            methods.BruteForce(i)
            # nearest neighbors
            methods.myNeighborsDict

        # Calculate AvgSim (Question 4b.)
        avgSim = methods.AverageSimilarityOfAllDocumentsWithBruteForce()

        # get the end time
        et = time.time()

        # get the execution time
        elapsed_time_brute_force = et - st

        # Show AvgSim and ExecTime (Question 5)
        avgLabel = Label(mainWindow, text='Average Similarity: ' + str(avgSim))
        avgLabel.grid(row=11, column=1)
        timeLabel = Label(mainWindow, text='Execution Time: ' + str(elapsed_time_brute_force))
        timeLabel.grid(row=12, column=1)

    # Use Brute Force SigSim method (Question 4a.)
    elif sigSimCheck.get() == 1:

        methods.selectedSimilarityMethod = 0

        # get the start time
        st = time.time()

        for i in range(1, int(numDocuments)+1):
            methods.BruteForce(i)
            # nearest neighbors
            methods.myNeighborsDict

        # Calculate AvgSim (Question 4b.)
        avgSim = methods.AverageSimilarityOfAllDocumentsWithBruteForce()

        # get the end time
        et = time.time()

        # get the execution time
        elapsed_time_brute_force = et - st

        # Show AvgSim and ExecTime (Question 5)
        avgLabel = Label(mainWindow, text='Average Similarity: ' + str(avgSim))
        avgLabel.grid(row=11, column=1)
        timeLabel = Label(mainWindow, text='Execution Time: ' + str(elapsed_time_brute_force))
        timeLabel.grid(row=12, column=1)


def JaccardMethodsWindow():
    global jaccardWindow

    jaccardWindow = Tk()
    jaccardWindow.title('Calculate Jaccard Similarity')
    jaccardWindow.geometry('600x600')

    jacLabel = Label(jaccardWindow, text='Enter 2 Documents to calculate Jaccard Similarity:')

    docID1Text = Text(jaccardWindow, height=1, width=5)
    docID2Text = Text(jaccardWindow, height=1, width=5)

    jacLabel.grid(row=1, column=0)
    docID1Text.grid(row=1, column=1)
    docID2Text.grid(row=1, column=2)

    sigLabel = Label(jaccardWindow, text='Enter number of Permutations Documents for Signature Similarity:')
    sigLabel.grid(row=2, column=0)
    numPermutationsText = Text(jaccardWindow, height=1, width=5)
    numPermutationsText.grid(row=2, column=1)

    jacButton = Button(jaccardWindow, text='Calculate', command=lambda: calculateJaccardSimilaritiesOrSigSim(docID1Text, docID2Text, numPermutationsText))
    jacButton.grid(row=3, column=1)

    jaccardWindow.mainloop()


def calculateJaccardSimilaritiesOrSigSim(docID1Text, docID2Text, numPermutationsText):
    global isClicked


    docID1 = int(docID1Text.get("1.0", END))
    docID2 = int(docID2Text.get("1.0", END))
    numPermutations = int(numPermutationsText.get("1.0", END))

    jac1 = methods.MyJacSimWithOrderedLists(docID1, docID2)
    jac2 = methods.MyJacSimWithSets(docID1, docID2)
    sigSim = methods.MySigSim(docID1, docID2, numPermutations)

    jacLabel1 = Label(jaccardWindow, text='Jaccard Similarity with Ordered Lists: ' + str(jac1))
    jacLabel2 = Label(jaccardWindow, text='Jaccard Similarity with Sets:' + str(jac2))
    sigSimLabel = Label(jaccardWindow, text='Signature Similarity: ' + str(sigSim))

    if isClicked:
        jacLabel1.destroy()
        jacLabel2.destroy()
        sigSimLabel.destroy()

    isClicked = True

    jacLabel1 = Label(jaccardWindow, text='Jaccard Similarity with Ordered Lists: ' + str(jac1))
    Label(jaccardWindow, text=methods.elapsed_time_for_jacSimWithOrderedLists).grid(row=5, column=0)
    jacLabel2 = Label(jaccardWindow, text='Jaccard Similarity with Sets:' + str(jac2))
    Label(jaccardWindow, text=methods.elapsed_time_for_jacSimWithSets).grid(row=7, column=0)
    sigSimLabel = Label(jaccardWindow, text='Signature Similarity: ' + str(sigSim))
    Label(jaccardWindow, text=methods.elapsed_time_for_SigSim).grid(row=9, column=0)


    jacLabel1.config(font=("Arial", 8, "bold"))
    jacLabel2.config(font=("Arial", 8, "bold"))
    sigSimLabel.config(font=("Arial", 8, "bold"))
    jacLabel1.grid(row=4, column=0)
    jacLabel2.grid(row=6, column=0)
    sigSimLabel.grid(row=8, column=0)




def main():
    GUI()


if __name__ == "__main__":
    main()
