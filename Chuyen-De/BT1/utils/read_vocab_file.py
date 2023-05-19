from entities.InverseIndex import InverseIndex
def read_vocabs():
  # Read vocabulary file
  vocab_file = open('datasets/term-vocab', 'r')
  vocab_dict = {}
  try:
    for line in vocab_file:
      vocab_dict[line.split()[1].lower()] = InverseIndex(0, set())
  except IndexError:
    print('end of file')
  vocab_file.close()
  return vocab_dict