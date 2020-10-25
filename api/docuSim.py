import math
from collections import Counter
from django.db.models import query
import numpy as np
from .preprocess import *

documents = []


def term_freq(documents):
    term_freq = {}
    for i in range(len(documents)):
        words = documents[i]
        for word in words:
            try:
                term_freq[word].add(i)
            except:
                term_freq[word] = {i}
    for i in term_freq:
        term_freq[i] = len(term_freq[i])
    return term_freq


def inverse_document_frequency(documents, vocabulary):
    tfidf = {}
    i = 0
    for i in range(len(documents)):
        counter = Counter(documents[i])
        word_count = len(documents[i])
        for word in np.unique(documents[i]):
            tf = counter[word]/word_count
            contains_word = int(vocabulary[word])
            tfidf[i, word] = tf * \
                math.log((len(documents)+1)/(contains_word+1))
    i += 1
    total_vocab = [x for x in vocabulary]
    D = np.zeros((len(documents), len(vocabulary)))
    return tfidf, total_vocab, D


def doc2vec(D, tfidf, total_vocab):
    for i in tfidf:
        ind = total_vocab.index(i[1])
        D[i[0]][ind] = tfidf[i]
    return D


def gen_vector(query, vocabulary, documents):
    preprocessed_query = preprocess(query)
    tokens = word_tokenize(str(preprocessed_query))

    total_vocab = [x for x in vocabulary]
    Q = np.zeros((len(total_vocab)))

    counter = Counter(tokens)
    words_count = len(tokens)

    for token in np.unique(tokens):

        tf = counter[token] / words_count
        df = int(vocabulary[token])
        print(df)
        idf = math.log((len(documents) + 1) / (df + 1))

        try:
            ind = total_vocab.index(token)
            Q[ind] = tf * idf
        except:
            pass
    return Q


def cosine_sim(a, b):
    cos_sim = np.dot(a, b)/(np.linalg.norm(a)*np.linalg.norm(b))
    return cos_sim


def cosine_similarity(gen_vector, doc_vec):
    d_cosines = []
    for d in doc_vec:
        d_cosines.append(cosine_sim(gen_vector, d))

    out = np.array(d_cosines).argsort()[-10:][::-1]

    return out.tolist()


def tfidf(keyword, path):
    documents = pre_process(path)
    vocabulary = term_freq(documents)
    tfidf, total_vocab, D = inverse_document_frequency(documents, vocabulary)
    doc_vec = doc2vec(D=D, tfidf=tfidf, total_vocab=total_vocab)
    lyrics_ids = cosine_similarity(gen_vector(
        query=keyword, vocabulary=vocabulary, documents=documents), doc_vec=doc_vec)
    return lyrics_ids
