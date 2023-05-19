from vb_code import *
from read_inverse_index import read_inverse_index
from entities.InverseIndex import InverseIndex
import pickle

def to_delta_list(ids):
    delta = 0
    res_ls = []
    for id in ids:
        delta = id - delta
        res_ls.append(delta)
    return res_ls

def to_id_list(delta_list):
    if delta_list:
        id = 0
        res_ls = []
        for delta in delta_list:
            res_ls.append(id + delta)
            id = delta
        return res_ls
    else:
        return []

def compress():
    d = read_inverse_index()
    # Sort doc_id list
    d = {k: InverseIndex(v.freq, sorted(v.s)) for k, v in d.items()}
    # Convert doc_id list to delta list
    d = {k: InverseIndex(v.freq, to_delta_list(v.s)) for k, v in d.items()}
    # Encode
    d = {k: InverseIndex(v.freq, list(map(lambda i: vb_encode(i), v.s))) for k, v in d.items()}
    return d

def extract():
    d = read_compress()
    # Decode
    d = {k: InverseIndex(v.freq, list(map(lambda i: int(''.join([str(i) for i in vb_decode(i)])), v.s))) for k, v in d.items()}
    # Convert delta list to doc_id list
    d = {k: InverseIndex(v.freq, to_id_list(v.s)) for k, v in d.items()}
    return d


def write_compress():
    with open('vb-compress-data.pkl', 'wb') as f:
        pickle.dump(compress(), f, protocol=pickle.HIGHEST_PROTOCOL)

def read_compress():
    with open('vb-compress-data.pkl', 'rb') as f:
        return pickle.load(f)

if __name__ == '__main__':
    write_compress()
    d = extract()
    print(d["use"])
