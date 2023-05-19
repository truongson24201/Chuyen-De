from gamma_code import gamma_encode, gamma_decode
from read_inverse_index import read_inverse_index
from vb_implement import to_delta_list, to_id_list
from entities.InverseIndex import InverseIndex
import pickle

def compress():
    d = read_inverse_index()
    # Sort id list
    d = {k: InverseIndex(v.freq, sorted(v.s)) for k, v in d.items()}
    # To delta list
    d = {k: InverseIndex(v.freq, to_delta_list(v.s)) for k, v in d.items()}
    # Encode
    d = {k: InverseIndex(v.freq, list(map(lambda i: gamma_encode(i), v.s))) for k, v in d.items()}
    return d

def extract():
    d = read_compress()
    # Decode
    d = {k: InverseIndex(v.freq, list(map(lambda i: gamma_decode(i), v.s))) for k, v in d.items()}
    # Convert delta list to doc_id list
    d = {k: InverseIndex(v.freq, to_id_list(v.s)) for k, v in d.items()}
    return d


def write_compress():
    with open('gamma-compress-data.pkl', 'wb') as f:
        pickle.dump(compress(), f, protocol=pickle.HIGHEST_PROTOCOL)

def read_compress():
    with open('gamma-compress-data.pkl', 'rb') as f:
        return pickle.load(f)

if __name__ == '__main__':
    write_compress()
    d = extract()
    print(d["use"])
