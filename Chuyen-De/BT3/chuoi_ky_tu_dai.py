# Chuỗi ký tự dài (Huỳnh)
import sys
import pickle
import time

def memory_usage(obj):
  size = sys.getsizeof(obj)
  if isinstance(obj, dict):
      size += sum(memory_usage(v) for v in obj.values)
  elif isinstance(obj, (list, tuple, set)):
      size += sum(memory_usage(v) for v in obj)
  return size

with open('sorted-inverse-index-data.pkl', 'rb') as file:
    before = time.time_ns()
    my_list = pickle.load(file)
    after = time.time_ns()
    print("Thoi gian load khong nen: ", (after - before) * (10**-9))
    print("Dung luong khong nen: ", memory_usage(my_list))
    file.close()
    chuoi_ky_tu_dai = ''
    miss_like = []
    for line in my_list:
        # [freq, postings_list, term] = line.split(',')
        # miss_like.append((freq,postings_list, len(chuoi_ky_tu_dai)))
        # chuoi_ky_tu_dai += term
        thistuple = (line[0], line[1], len(chuoi_ky_tu_dai))
        chuoi_ky_tu_dai += line[2]
        miss_like.append(thistuple)

    with open('chuoi-ky-tu-dai-data.pkl', 'wb') as file:
        pickle.dump([chuoi_ky_tu_dai, miss_like], file)
        file.close()
    
    with open('chuoi-ky-tu-dai-data.pkl', 'rb') as file:
        before = time.time_ns()
        [chuoi_ky_tu_dai, miss_like] = pickle.load(file)
        after = time.time_ns()
        print("Thoi gian load nen: ", (after - before) * 10**-9)
        print("Duong luong nen: ", memory_usage(chuoi_ky_tu_dai) + memory_usage(miss_like))
        file.close()
    