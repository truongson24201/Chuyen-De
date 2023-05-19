from utils import helper
from gensim.parsing.preprocessing import STOPWORDS
import math
from nltk.stem import WordNetLemmatizer
import pickle

terms = sorted(helper.read_terms())
lemmatizer = WordNetLemmatizer()

def create_inverted_index():
    # Đọc bộ tài liệu
    docs = helper.read_docs()
    # Xây dựng bộ chỉ mục ngược với cấu trúc {<term>: (<term_frequency>, <posting_list>)}
    indexes = dict(map(lambda term: (term, (0, [])), terms))
    for i, doc in enumerate(docs):
        words = doc.lower().split()
        for word in words:
            word = lemmatizer.lemmatize(word, "v")
            if word in indexes:
                indexes[word] = (indexes[word][0] + 1, indexes[word][1] + [i])
    pickle.dump(indexes, open("indexes.pkl", "wb"))
    return indexes

def intersect_skip(list1, list2):
  print(list1, list2)
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
    print(list1[i1], list2[i2])
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

def handle_multiple_intersect_skip(args):
    if len(args) == 0:
      return []
    elif len(args) == 1:
        return args[0]
    elif len(args) == 2:
       return sorted(set(args[0]) & set(args[1]))
        # return intersect_skip(args[0], args[1])
    return sorted(set(args[0]) & set(handle_multiple_intersect_skip(args[1:])))

def preprocessing_documents(documents):
    # Tách tài liệu thành 1 mảng các từ
    result = [set([word for word in document.split() if word not in STOPWORDS]) for document in documents]
    # Lemmatize: biến đổi tập các từ có ý nghĩa tương đương nhau nhưng khác nhau về loại từ thành 1 từ để ...
    result = [set([lemmatizer.lemmatize(word, "v") for word in document]) for document in result]
    return result

class BIM:
    def __init__(self, documents) -> None:
        self.documents = documents
        # Tạo chỉ mục ngược
        self.indexes = create_inverted_index()
        self.docs_word = preprocessing_documents(documents)

    def ranking(self, query):
        print(query.upper())
        # Tách từ câu query
        query_words = set(query.lower().split())
        # Loại bỏ stop words
        query_words = [word for word in query_words if word not in STOPWORDS]
        query_words = [lemmatizer.lemmatize(word, "v") for word in query_words]
        print(' '.join(query_words).upper())
        # Lấy danh sách docs chứa từ với mỗi từ
        # Và sắp xếp theo số lượng tài liệu chứa mỗi từ theo thứ tự tăng dần (tối ưu khi intersect)
        relevants = sorted([self.indexes[word][1] for word in query_words if word in self.indexes], key = lambda ls: len(ls))
        # Intersect để tìm ra các tài liệu phù hợp
        relevant_docs = handle_multiple_intersect_skip(relevants)
        # S là số lượng tài liệu phù hợp với câu query
        S = len(relevant_docs)
        # N là tổng số tài liệu - lấy len(documents)
        N = len(self.documents)
        # Biến result dùng để lưu và trả về kết quả
        result = {}
        # Duyệt qua bộ tài liệu
        for idx, document in enumerate(self.docs_word):
          # Khởi tạo biến score (biến thành sẽ được tính theo công thức RSV)
          # Score là giá trị để xếp hạng tài liệu
          score = 0
          # Duyệt qua các từ trong câu query
          for t in query_words:
            # Đặt điều kiện từ đó có trong tài liệu (vì xt = qt = 1 theo công thức)
            # Và để tránh trường hợp từ t không có trong bộ từ vựng thì ta đặt điều kiện "t in terms"
            if t in document and t in terms:
              # Tính s
              # s là số lượng tài liệu chứa từ t với điều kiện tài liệu phù hợp với câu query
              s = len(set(self.indexes[t][1]) & set(relevant_docs))
              # dft là tổng số tài liệu chứa từ t (giá trị này tương đương với frequency được lưu trong inverted index)
              dft = self.indexes[t][0]
              # ct là trọng số của mỗi từ trong tài liệu
              # ct được tính theo công thức
              # thêm 0.5 để làm mịn
              ct = math.log1p(((s + 0.5) / (S - s + 0.5)) / ((dft - s + 0.5) / (N - dft - S + s + 0.5)))
              # score bằng tổng các ct (với xt = qt = 1)
              score += ct
          # result là dictionary lưu trữ kết quả với key là id của tài liệu và value là RSV
          result[idx] = score
        # Sắp xếp bộ tài liệu theo RSV để xếp hạng và lấy ra 5 tài liệu có RSV cao nhất
        result = {k: v for k, v in sorted(result.items(), key= lambda item: item[1], reverse=True)[:5]}
        # Truy xuất nội dung tài liệu theo id tài liệu để trả về kết quả cuối cùng
        result = list(map(lambda item: self.documents[item[0]], result.items()))
        return result
        
import time

if __name__ == "__main__":
  bim = BIM(helper.read_docs())
  queries = helper.read_queries()
  for query in queries:
    before = time.time()
    print(bim.ranking(query))
    after = time.time()
    print("Spend:", after - before)


# Kế thừa intersect để lấy ra danh sách doc phù hợp với query (S) (1)
# N là tổng số tài liệu lấy len(docs)
# s = giao của (1) và posting list của từ -> số lượng
# dft = frequency trong inverted index