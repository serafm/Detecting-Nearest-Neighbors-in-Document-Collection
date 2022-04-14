
wordDict = {'50': [1, 2], '118': [3], '200': [2, 4, 5], '370': [1, 3, 4], '607': [1], '1020': [1, 2, 5]}
list = []
thesiPinaka = 1
k = 3
pos = 0

randomHash = [[2, 4, 6, 5, 1, 3], [4, 1, 2, 5, 3, 6], [1, 3, 4, 6, 2, 5]]
col = 0
row = 0

sig = [[10000, 10000, 10000], [10000, 10000, 10000], [10000, 10000, 10000], [10000, 10000, 10000], [10000, 10000, 10000]]


for word in wordDict:
    list = wordDict.get(word)

    for trys in range(len(list)):

        for j in range(k):
            for i in range(len(wordDict)):
                if thesiPinaka == randomHash[j][i]:
                    if (i + 1) < sig[int(list[col])-1][j]:
                        sig[int(list[col])-1][j] = i + 1
                        break
        col += 1
    thesiPinaka += 1
    col = 0

print(sig)