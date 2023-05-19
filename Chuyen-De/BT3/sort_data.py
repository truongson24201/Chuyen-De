file = open('inverse-index-data.txt', 'r')
my_list = []
for line in file:
    [term, freq, postings_list] = line.split('::')
    postings_list = postings_list.removesuffix("\n")
    my_list.append((int(freq), sorted(eval(postings_list)), term))
file.close()

import pickle
sorted_file = open('sorted-inverse-index-data.pkl', 'wb')
my_list = sorted(my_list, key= lambda item: item[2])
pickle.dump(my_list, sorted_file, protocol=pickle.HIGHEST_PROTOCOL)
sorted_file.close()