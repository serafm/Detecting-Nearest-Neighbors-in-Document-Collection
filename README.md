# Detecting-Nearest-Neighbors-in-Document-Collection

The aim is to evaluate the quality of MINHASH methods (for production
signatures) and LSH (for filtering before similarity calculation, either via Jaccard or via signatures)
when the calculation of the nearest neighbors of a document X contained in a required
collection of documents. The evaluation of proximity (as small as possible) or, equivalently, similarity (as much as possible
great done) of the other documents from document X will be done in two basic ways:
- Through the Jaccard-JSIM metric similarity (X, Y) of document X with each of the other Y documents
belong to the collection. As a solution quality, it will be our basis for comparison with other metrics.
- Through the similarity-signatures of document X with each of the other documents Y belonging to
collection.
