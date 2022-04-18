import random

global hashLSH, LSHdicts, sig

LSHdicts = []

SIG = [[1, 4, 5, 3, 2, 7, 9, 10, 3, 3], [1, 4, 5, 3, 2, 4, 11, 8, 9, 1], [14, 2, 2, 1, 9, 4, 11, 8, 6, 1], [5, 2, 2, 1, 9, 4, 11, 8, 7, 1], [2, 4, 5, 3, 2, 7, 9, 10, 1, 3]]
K = 10



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


def main():
    global hashLSH
    hashLSH = create_random_hash_function()
    LSH(5)


if __name__ == "__main__":
    main()
