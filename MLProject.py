import requests
import time

from CorpusReader import read_corpus_from_file
from TfIdfVectorizer import TfIdfVectorizer
from KMeans import KMeans

corpus = [""]


def stemmer(doc):
    url = 'http://localhost:4027/service-trmorphology/annotate/Analyze'  # Set destination URL here
    paramaters = {'input': doc}
    r = requests.get(url, params=paramaters)
    r.encoding = "utf-8"
    return " ".join(r.text.split())  # boşluk varsa kaldır



if __name__ == '__main__':

    document_0 = "China has a strong China that is growing at a China pace. However politically it differs greatly from the US Economy."
    document_1 = "At last, China seems serious about confronting an endemic problem: domestic violence and corruption."
    document_2 = "Japan's prime minister, Shinzo Abe, is working towards healing the economic turmoil in his own country for his view on the future of his people."
    document_3 = "China Putin is working China to fix the China in Russia as the China has tumbled."
    document_4 = "What's the future of Abenomics? We asked Shinzo Abe for his views"
    document_5 = "Obama has eased sanctions on Cuba while accelerating those against the Russian Economy, even as the Ruble's value falls almost daily."
    document_6 = "Vladimir Putin was found to be riding a horse, again, without a shirt on while hunting deer. Vladimir Putin always seems so serious about things - even riding horses."

    all_documents = [document_0, document_1, document_2, document_3, document_4, document_5, document_6]
    start = time.time()

    corpus, corpus_cat = read_corpus_from_file()
    print("corpus processing time : ", time.time() - start)

    start = time.time()
    tfidf = TfIdfVectorizer(corpus=corpus)
    vector = tfidf.tf_idf()
    print("tfidf processing time : ", time.time() - start)

    start = time.time()
    kmeans = KMeans(k=6, max_iteration=20)
    clusters, centroids = kmeans.fit(vector)

    centroidSorted = []


    for center in centroids:
        sortedcenter = sorted(center, reverse=True)
        print("----------------------------")
        for ind in range(6):
            tfidfscore = center.index(sortedcenter[ind])
            print(list(tfidf.get_vocabulary())[tfidfscore])

    print("kmeans processing time : ", time.time() - start)

    print("tamamlandı.")

