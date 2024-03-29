import math
import string


class TfIdfVectorizer:

    corpus = []
    vocabulary = []
    tfidf_vector = {}
    idf_vector = {}
    corpus_size = 0
    sublinear_tf = True

    def __init__(self, _corpus=None, _vocabulary=None, _sublinear_tf=True):
        self.corpus = [self.remove_punctuation(doc) for doc in _corpus]
        self.corpus_size = len(_corpus)
        self.sublinear_tf = _sublinear_tf

        if _vocabulary is None:                          # vocabulary verilmezse oluştur
            self.vocabulary = self.create_vocabulary()
        else:                                           # vocabulary verildiyse eşitle
            self.vocabulary = [term.lower() for term in _vocabulary]

    def get_vocabulary(self):
        return self.vocabulary

    def remove_punctuation(self, doc):
        delete_chars = string.digits + string.punctuation
        doc = doc.lower()
        doc = str(doc).replace("\r", " ").replace("\n", " ").replace("“", " ").replace("’", " ").replace("", " ") \
            .translate(str.maketrans('', '', delete_chars)).replace("", " ").replace("", " ").replace("", " ")

        doc = " ".join(doc.split())
        return doc

    def create_vocabulary(self):
        vocabulary = []
        for doc in self.corpus:
            for term in doc.split():
                vocabulary.append(term)
        return set(vocabulary)

    # dokumandaki terim / dokumandaki toplam terim
    def term_frequency(self, term, doc):
        doc_term_count = doc.count(term)
        total_term = len(doc.split())
        if total_term == 0:
            return 0
        return doc_term_count / total_term

    # log normalizasyon
    def sublinear_term_frequency(self, term, doc):
        term = " "+term+" "                           #içinde aranan terim geçen kelimeleri saydırmamalıyız
        doc = " "+doc+" "
        count = doc.count(term)

        if count == 0:
            return 0
        return 1 + math.log10(count)

    # kelimelerin idf'lerini hesapla
    def calc_inverse_doc_frequency(self):
        for term in self.vocabulary:
            idf_count = 1                           # division by zero hatası almamak için 1'den başlat
            term = " "+term+" "
            for doc in self.corpus:
                doc = " "+doc+" "
                if doc.count(term) > 0:
                    idf_count += 1

            self.idf_vector[term.strip()] = math.log10(1 + (self.corpus_size / idf_count))

    def tf_idf(self):
        doc_count = 0
        self.calc_inverse_doc_frequency()                           # her terimin idf ini hesapla

        for doc in self.corpus:
            doc_key = "D" + str(doc_count)
            term_count = 0
            self.tfidf_vector[doc_key] = {}                         # doc için yeni dictionary oluştur

            for term in self.vocabulary:
                term_key = 'T' + str(term_count)+"_"+term

                if self.sublinear_tf:                               # log normalization
                    tf = self.sublinear_term_frequency(term, doc)   # tf hesapla
                else:
                    tf = self.term_frequency(term, doc)

                idf = self.idf_vector[term]                         # terimin idf'ini al
                tf_idf = tf * idf                                   # tf*idf hesapla

                term_dict = {'tf': tf, 'idf': idf, 'tfidf': tf_idf}

                self.tfidf_vector[doc_key][term_key] = term_dict     #doc için hesaplanan tf-idf'i vectore ekle
                term_count += 1
            doc_count += 1
        return self.tfidf_vector
