# This file use to save reverse index data
# Import utils and needed class
from utils.read_vocab_file import read_vocabs
from utils.read_doc_file import read_docs
from utils.generate_locator_cards import generate_cards
from entities.InverseIndex import InverseIndex

# Read vocabs from file
vocab_dict = read_vocabs()
# Read docs from file
doc_dict = read_docs()
print(doc_dict)

# Generate locator cards (tạo danh sách thẻ định vị)
cards = generate_cards(list(doc_dict.values()))

# Sort cards
cards.sort()

# Tổng hợp danh sách thẻ định vị
for card in cards:
  # Nếu term có trong bộ từ vựng và doc_id chưa có trong postings list của term
  if card[0] in vocab_dict and card[1] not in vocab_dict[card[0]].s:
    # Doc chưa có trong postings set -> frequency + 1
    vocab_dict[card[0]].freq += 1
    # Thêm doc_id vào postings set
    vocab_dict[card[0]].s.add(card[1])
file = open('inverse-index-data.txt', 'w')
# Save to file
for key, value in vocab_dict.items():
  file.write('{0}::{1}::{2}\n'.format(key, value.freq, value.s))
file.close()
