from entities.InverseIndex import InverseIndex
# This file use to read reverse index data
def read_inverse_index():
  file = open('inverse-index-data.txt', 'r')
  my_dict = {}
  for line in file:
    arr = line.split('::')
    my_dict[arr[0]] = InverseIndex(arr[1], eval(arr[2]))
  return my_dict