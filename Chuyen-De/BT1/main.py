from read_inverse_index import read_inverse_index
from utils.read_doc_file import read_docs
from utils.read_query_file import read_queries
import math
def intersect(p1, p2):
  answer = []
  i1 = i2 = 0
  while i1 < len(p1) and i2 < len(p2):
    if p1[i1] == p2[i2]:
      answer.append(p1[i1])
      i1 += 1
      i2 += 1
    elif p1[i1] < p2[i2]:
      i1 += 1
    else:
      i2 += 1
  return answer

def intersect_skip(list1, list2):
  i1 = i2 = 0
  len1, len2 = len(list1), len(list2)
  skip1 = int(math.sqrt(len1))
  skip2 = int(math.sqrt(len2))

  skip_dict_1 = {}
  skip_dict_2 = {}

  while i1 + skip1 < len1:
    skip_dict_1[i1] = list1[i1 + skip1]
    i1 += skip1
  while i2 + skip2 < len2:
    skip_dict_2[i2] = list2[i2 + skip2]
    i2 += skip2

  answer = []

  i1 = i2 = 0
  while i1 < len1 and i2 < len2:
    if list1[i1] == list2[i2]:
      answer.append(list1[i1])
      i1 += 1
      i2 += 1
    elif list1[i1] < list2[i2]:
      if i1 in skip_dict_1 and skip_dict_1[i1] <= list2[i2]:
        while i1 in skip_dict_1 and skip_dict_1[i1] <= list2[i2]:
          i1 += skip1
      else:
        i1 += 1
    else:
      if i2 in skip_dict_2 and skip_dict_2[i2] <= list1[i1]:
        while i2 in skip_dict_2 and skip_dict_2[i2] <= list1[i1]:
          i2 += skip2
      else:
        i2 += 1
  return answer

def remove_stop_words(s, vocab_dict):
  words = s.split()
  words = [word for word in words if word in vocab_dict]
  return ' '.join(words)

if __name__ == '__main__':
  doc_dict = read_docs()
  vocab_dict = read_inverse_index()
  query_list = read_queries()
  query_list = list(map(lambda s: remove_stop_words(s, vocab_dict), query_list))
  # Sort query list by length
  query_list = sorted(query_list, key = lambda query: len(query))
  print(query_list)
  for query in query_list:
    # Separate words
    words = query.split()
    if len(words) == 0:
      print([])
      continue
    result = sorted(vocab_dict[words[0]].s)
    if len(words) == 1:
      print(result)
    else:
      for remain_word in words[1:]:
        result = intersect_skip(result, sorted(vocab_dict[remain_word].s))
      print(result)