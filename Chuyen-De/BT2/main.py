from utils.read_doc_file import *
from utils.read_query_file import *
from read_inverse_index import read_inverse_index
import numpy as np
from math import *
import pickle

doc_dict = read_docs()
vocab_dict = read_inverse_index()

def tf_weight(term, doc_id):
    # tf = doc_dict[doc_id].split().count(term) if doc_id in vocab_dict[term].s else 0
    tf = doc_dict[doc_id].split().count(term)
    return 1+log10(tf) if tf > 0 else 0

def tf_weight_query(term, query):
    tf = query.split().count(term)
    return 1+log10(tf) if tf > 0 else 0

def idf(term):
    try:
        return log10(len(doc_dict) / len(vocab_dict[term].s))
    except:
        return 0

def remove_stop_words(query):
  words = query.split()
  words = [word for word in words if word in vocab_dict]
  return ' '.join(words)

def create_vector_space():
    # doc is column and term is row
    matrix = np.zeros((len(vocab_dict), len(doc_dict)), dtype=np.float64)
    # vindex: index, vkey: term (vocab), vvalue: (freq, set_of_docs)
    for vindex, (vkey, vvalue) in enumerate(vocab_dict.items()):
        # dindex start with 0
        for dindex, (dkey, dvalue) in enumerate(doc_dict.items()):
            if dkey not in vvalue.s:
                continue
            matrix[vindex][dindex] = tf_weight(vkey, dkey) * idf(vkey)
            print(vindex, dindex, matrix[vindex][dindex])
    with open('vector-space.pkl', 'wb') as f:
        pickle.dump(matrix, f)
        f.close()

if __name__ == "__main__":
    f = open('vector-space.pkl', 'rb')
    matrix = pickle.load(f)
    f.close()

    queries = read_queries()
    for query in queries[:10]:
        query = remove_stop_words(query)
        print("QUERY", query)
        query_tfidf_weight = np.array([tf_weight_query(term, query) * idf(term) for term in vocab_dict.keys()], dtype=np.float64)


        result = np.array([np.sum(np.dot(query_tfidf_weight, column)) / np.sqrt(np.sum(np.square(column)) * np.sum(np.square(query_tfidf_weight))) for column in matrix.T], dtype=np.float64)
        result = dict(enumerate(result, 1))
        result = dict(sorted(result.items(),reverse=True, key= lambda item: item[1]))
        result = dict(list(result.items())[:2])


        for index in result.keys():
            print(doc_dict[index],'\n\n')
    
