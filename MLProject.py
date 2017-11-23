import time

from CorpusReader import read_corpus_from_file
from TfIdfVectorizer import TfIdfVectorizer
from KMeans import KMeans
from SilhouetteCoefficient import SilhouetteCoefficient

corpus = [""]


if __name__ == '__main__':

    start = time.time()

    corpus, corpus_cat = read_corpus_from_file()
    print("corpus processing time : ", time.time() - start)

    start = time.time()
    tfidf = TfIdfVectorizer(_corpus=corpus, _sublinear_tf=True)
    vector = tfidf.tf_idf()
    print("tfidf processing time : ", time.time() - start)

    start = time.time()
    kmeans = KMeans(k=6, max_iteration=20)
    clusters, centroids = kmeans.fit(vector)

    print("kmeans processing time : ", time.time() - start)


    '''  
    centroidSorted = []
    for center in centroids:
        sortedcenter = sorted(center, reverse=True)
        print("----------------------------")
        for ind in range(6):
            tfidfscore = center.index(sortedcenter[ind])
            print(list(tfidf.get_vocabulary())[tfidfscore])
   '''

    silhouette = SilhouetteCoefficient(_clusters=clusters, _centers=centroids)
    sil_coef = silhouette.compute()

    print("silhouette coefficient : ", sil_coef)


    print("tamamlandı.")

