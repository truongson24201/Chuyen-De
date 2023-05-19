def generate_cards(doc_list):
  cards = []
  for i, doc in enumerate(doc_list, start=1):
    term_list = doc.split()
    for term in term_list:
      cards.append((term.lower(), i))
  return cards