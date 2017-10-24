import codecs
import os

root_path = "C:\\Users\\birkan\\PycharmProjects\\TextLearning\\"

#news_category = os.listdir(root_path+"news")  #news içindeki klasörleri al
news_category = ["ekonomi", "kultur-sanat", "saglik", "siyaset", "spor", "teknoloji"]




def read_corpus_from_file():
    count = 0
    corpus = []
    corpus_category = []

    for dir in news_category:
        docs = os.listdir(root_path + "news/" + dir + "/processed/") #kategori içinden dosyaları al
        #print(dir +" kategorisi: ")
        for doc in docs[:100]:
            doc_path = root_path + "news/" + dir + "/processed/" + doc
            news = ""
            with codecs.open(doc_path, 'r', encoding='utf8') as file:
                news = file.read()  # dosya oku
            if(news == ""):
                continue
            else:
                corpus.append(news)
                corpus_category.append(dir)
        count += 1
    return corpus, corpus_category