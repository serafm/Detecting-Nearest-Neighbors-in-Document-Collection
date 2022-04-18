import random

global hashLSH, LSHdicts, sig

LSHdicts = []

sig = [[1, 4, 5, 3, 2, 7, 9, 10, 3, 3], [1, 4, 5, 3, 2, 4, 11, 8, 9, 1], [14, 2, 2, 1, 9, 4, 11, 8, 6, 1], [5, 2, 2, 1, 9, 4, 11, 8, 7, 1], [2, 4, 5, 3, 2, 7, 9, 10, 1, 3]]
K = 10



def create_random_hash_function(p=2 ** 33 - 355, m=2 ** 32 - 1):
    a = random.randint(1, p - 1)
    b = random.randint(0, p - 1)
    return lambda x: 1 + (((a * x + b) % p) % m)


# Split the SIG list in b bands
def band_split(rowsPerBands):
    # r is rowsPerBand, b is numBands
    global sig
    #signature = sig[sign]
    vec = []
    numBands = K / rowsPerBands
    for s in range(len(sig)):
        signature = sig[s]
        #for i in range(0, len(signature), rowsPerBands):
        tupl = tuple(signature[0: rowsPerBands])
        vec.insert(s, tupl)

    h = dict()
    key = 1
    for x in vec:
        h[key] = hashLSH(hash(x))
        key = key + 1


    ordered = {k: v for k, v in sorted(h.items(), key=lambda item: item[1])}

    bucket = 0
    temp = 0

    for key in ordered:

        if temp == ordered[key]:
            bucket = bucket - 1
            ordered[key] = bucket

        temp = ordered[key]
        ordered[key] = bucket
        bucket += 1

    return ordered


def LSH():
    global sig, LSHdicts

    LSHdicts.append(band_split(5))

    print(LSHdicts)


def main():
    global hashLSH
    hashLSH = create_random_hash_function()
    LSH()




if __name__ == "__main__":
    main()
