Title:  Bag of Words Data Set

Abstract: 
=========
This collection contains three text collections in the form of bags-of-words.


Data Set Information:
=====================
For each text dataset in the collection: 
* D is the number of documents, 
* W is the number of words in the vocabulary, and 
* N is the total number of words

Moreover, NNZ (see below) is the number of nonzero counts in the
bag-of-words). After tokenization and removal of stopwords, the
vocabulary of unique words was truncated by only keeping words that
occurred more than ten times. Individual document names (i.e. an
identifier for each docID) are not provided for copyright reasons.

These data sets have no class labels, and for copyright reasons no
filenames or other document-level metadata.  These data sets are ideal
for clustering and topic modeling experiments.

For each text collection we provide docword.*.txt (the bag-of-words
file, in sparse format) and vocab.*.txt (the vocabulary file).

==================================
DATA_1-docword.enron.txt
==================================
Enron Emails:
orig source: www.cs.cmu.edu/~enron
D=39861
W=28102
N=6,400,000 (approx)

==================================
DATA_2-docword.nips.txt
==================================
NIPS full papers:
orig source: books.nips.cc
D=1500
W=12419
N=1,900,000 (approx)

==================================

Attribute Information:

The format of the docword.*.txt file is 3 header lines, followed by
NNZ triples:
---
D
W
NNZ
docID wordID count
docID wordID count
docID wordID count
docID wordID count
...
docID wordID count
docID wordID count
docID wordID count
---

The format of the vocab.*.txt file is line contains wordID=n.