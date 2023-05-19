import pickle
import time
import sys
from math import log2

def memory_usage(obj):
  size = sys.getsizeof(obj)
  if isinstance(obj, dict):
      size += sum(memory_usage(v) for v in obj.values)
  elif isinstance(obj, (list, tuple, set)):
      size += sum(memory_usage(v) for v in obj)
  return size

def get_common_prefix(input_arr):
    """
    Get common prefix for a particular block for front coding
    :param input_arr:
    :return: common prefix
    """
    input_arr.sort(reverse=False)
    str1 = input_arr[0]
    str2 = input_arr[len(input_arr) - 1]
    len1 = len(str1)
    len2 = len(str2)
    prefix = ""
    i = 0
    j = 0
    while i < len1 and j < len2:
        if str1[i] != str2[j]:
            break
        prefix += str1[i]
        i += 1
        j += 1
    return prefix

with open('sorted-inverse-index-data.pkl', 'rb') as file:
    before = time.time_ns()
    my_list = pickle.load(file)
    after = time.time_ns()
    print('Thoi gian load khong nen: ',(after - before) * (10**-9))
    print('Dung luong khong nen: ', memory_usage(my_list))
    file.close()

def get_term(term_index):
    block_index = term_index // k
    block_key_str = my_list[block_index][2]
    return block_key_str


if __name__ == '__main__':
    k = int(log2(len(my_list)))
    my_str = ''
    i = 0
    for i in range(0, len(my_list) // k, k):
        tmp = [item[2] for item in my_list[i:i+k]]
        prefix = get_common_prefix(tmp)
        key_str = str(len(prefix)) + prefix + '*' + tmp[0][len(prefix):] + ''.join([str(len(term[len(prefix):])) + '|' + term[len(prefix):] for term in tmp[1:]])
        (freq, postings_list, term) = my_list[i]
        my_list[i+1:i+k] = [(item[0], item[1], None) for item in tmp[1:]]
        my_list[i] = (freq, postings_list, len(my_str))
        my_str += key_str

    with open('front-coding-data.pkl', 'wb') as file:
      pickle.dump([my_str, my_list], file)
      file.close()

    with open('front-coding-data.pkl', 'rb') as file:
      before = time.time_ns()
      [my_str, my_list] = pickle.load(file)
      after = time.time_ns()
      print('Thoi gian load nen front-coding: ',(after - before) * (10**-9))
      print('Dung luong nen front-coding: ', memory_usage(my_str) + memory_usage(my_list))
      file.close()