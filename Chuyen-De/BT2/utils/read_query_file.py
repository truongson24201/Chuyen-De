def read_queries():
  # Read doc file
  query_file = open('datasets/query-text', 'r')
  query_list = []
  tmp = ''
  try:
    for line in query_file:
      strip_line = line.strip('\n')
      if strip_line.isdigit():
        continue
      elif strip_line.endswith('/'):
        query_list.append(tmp.strip())
        tmp = ''
      else:
        tmp += " {}".format(strip_line.lower())
  except IndexError:
    print('end of file')
  query_file.close()
  return query_list