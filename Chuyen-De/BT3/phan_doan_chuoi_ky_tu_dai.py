import pickle
import sys
import time

k = 4
with open('sorted-inverse-index-data.pkl', 'rb') as file:
    before = time.time_ns()
    my_list = pickle.load(file)
    after = time.time_ns()
    print('Thoi gian load khong nen: ',(after - before) * (10**-9))
    my_str = ''
    file.close()

def get_term(term_index):
  first_term_index = term_index // k
  i = my_list[first_term_index][2]
  num_str = ''
  while my_str[i].isdigit():
     num_str += my_str[i]
     i+= 1
  num = int(num_str)
  term = my_str[i: i+num]
  return term

def memory_usage(obj):
  size = sys.getsizeof(obj)
  if isinstance(obj, dict):
      size += sum(memory_usage(v) for v in obj.values)
  elif isinstance(obj, (list, tuple, set)):
      size += sum(memory_usage(v) for v in obj)
  return size

if __name__ == '__main__':
    print("Dung luong khong nen: ", memory_usage(my_list))
    count = 0
    for item in my_list:
        (freq, postings_list, term) = item
        if count % k == 0:
          my_list[count] = (freq, postings_list, len(my_str))
          count += 1
          continue
        my_str += str(len(item[2])) + item[2]
        my_list[count] = (freq, postings_list, None)
        count += 1
    after = memory_usage(my_list)

    with open('phan-doan-data.pkl', 'wb') as file:
      pickle.dump([my_str, my_list], file, protocol=pickle.HIGHEST_PROTOCOL)
      file.close()

    before = time.time_ns()
    with open('phan-doan-data.pkl', 'rb') as file:
      [my_str, my_list] = pickle.load(file)
      file.close()

    after = time.time_ns()
    print('Thoi gian load nen phan doan: ',(after - before) * (10**-9))
    print("Dung luong nen phan doan: ", memory_usage(my_list) + memory_usage(my_str))

        