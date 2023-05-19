def read_docs():
  # Read doc file
  doc_file = open('datasets/doc-text', 'r')
  docs = []
  tmp = ''
  try:
    for row in doc_file:
      row = row.strip('\n')
      if row.isdigit():
        pass
      elif row.endswith('/'):
        docs.append(tmp.strip())
        tmp = ''
      else:
        tmp += " {}".format(row)
  except IndexError:
    pass
  doc_file.close()
  return docs

  



def read_queries():
  # Read doc file
  query_file = open('datasets/query-text', 'r')
  queries = []
  tmp = ''
  try:
    for row in query_file:
      row = row.strip('\n')
      if row.isdigit():
        continue
      elif row.endswith('/'):
        queries.append(tmp.strip())
        tmp = ''
      else:
        tmp += " {}".format(row.lower())
  except IndexError:
    pass
  query_file.close()
  return queries





def read_terms():
  # Read vocabulary file
  term_file = open('datasets/term-vocab', 'r')
  terms = []
  try:
    for row in term_file:
      terms.append(row.split()[1].lower())
  except IndexError:
    pass
  term_file.close()
  return terms

def create_inverted_index():
  terms = read_terms()
