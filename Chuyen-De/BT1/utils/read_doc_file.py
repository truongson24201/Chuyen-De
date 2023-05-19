def read_docs():
  # Read doc file
  doc_file = open('datasets/doc-text', 'r')
  doc_dict = {}
  i = None
  tmp = ''
  try:
    for line in doc_file:
      strip_line = line.strip('\n')
      if strip_line.isdigit():
        i = int(strip_line)
      elif strip_line.endswith('/'):
        doc_dict[i] = tmp.strip()
        tmp = ''
      else:
        tmp += " {}".format(strip_line)
  except IndexError:
    print('end of file')
  doc_file.close()
  return doc_dict