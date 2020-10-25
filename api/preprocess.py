import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

import numpy as np
import pandas as pd

from num2words import num2words

nltk.download('stopwords')
nltk.download('punkt')


def preprocess(data):
    data = clean(data)
    data = no_numbers(data)
    data = stem(data)

    return data


def stem(data):
    stem = PorterStemmer()
    tokens = word_tokenize(str(data))
    res_data = ""
    for i in tokens:
        res_data = res_data + " " + stem.stem(i)
    return res_data


def clean(data):
    data = np.char.lower(data)
    punch = '!\"#$%&()*+-/:;<=>?@[\]^_`{|}~\n'

    for i in range(len(punch)):
        data = np.char.replace(data, punch[i], ' ')
        data = np.char.replace(data, " ", " ")
    data = np.char.replace(data, ',', '')
    data = np.char.replace(data, "'", "")

    stop_words = stopwords.words('english')
    words = word_tokenize(str(data))
    res_data = ""
    for i in words:
        if i not in stop_words and len(i) > 1:
            if len(res_data) == 0:
                res_data = i
            else:
                res_data = res_data + " " + i

    return res_data


def no_numbers(data):
    tokens = word_tokenize(str(data))
    res_data = ""
    for i in tokens:
        try:
            i = num2words(int(i))
        except:
            pass
        res_data = res_data + ' ' + i
    res_data = np.char.replace(res_data, '-', ' ')
    return(res_data)


def pre_process(path):
    documents = []
    reader = pd.read_csv(path)
    for row in reader["Lyrics"]:
        data = preprocess(str(row))
        documents.append(word_tokenize(data))
    print("Data Optimization Done")

    return documents
