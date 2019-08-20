from google_spacy import GoogleSpacy, Nlp

gspacy = GoogleSpacy()
gspacy.set_language('fr')
gnlp = gspacy.nlp

# create a document
doc = gnlp("Avec la mer du Nord pour dernier terrain vague")

print([tok.text for tok in doc])
print([tok.shape for tok in doc])
print([sent for sent in doc.sentences])
# ['Avec', 'la', 'mer', 'du', 'Nord', 'pour', 'dernier', 'terrain', 'vague']
# ['Xxxx', 'xx', 'xxx', 'xx', 'Xxxx', 'xxxx', 'xxxxxxx', 'xxxxxxx', 'xxxxx']
# [['Avec', 'la', 'mer', 'du', 'Nord', 'pour', 'dernier', 'terrain', 'vague']]


# serialize the document:
serializedDoc = doc.serialize()
#> b'\n2\n0\n.Avec la mer du Nord pour dernier terrain vague\x12\x18\n\x06\n\x04Avec\x12\x04\x08\x02H\x02\x1a\x02\x106"\x04Avec\x12\x1c\n\x06\n\x02la\x10\x05\x12\x08\x08\x05(\x018\x01H\x02\x1a\x04\x08\x02\x10\x10"\x02le\x12\x1c\n\x07\n\x03mer\x10\x08\x12\x08\x08\x06(\x018\x01H\x02\x1a\x02\x10$"\x03mer\x12\x1c\n\x06\n\x02du\x10\x0c\x12\x08\x08\x02(\x028\x01H\x02\x1a\x04\x08\x02\x10+"\x02du\x12 \n\x08\n\x04Nord\x10\x0f\x12\x08\x08\x06(\x028\x01H\x01\x1a\x04\x08\x03\x10$"\x04Nord\x12\x1a\n\x08\n\x04pour\x10\x14\x12\x04\x08\x02H\x02\x1a\x02\x10+"\x04pour\x12&\n\x0b\n\x07dernier\x10\x19\x12\x08\x08\x01(\x028\x01H\x02\x1a\x04\x08\x07\x10\x05"\x07dernier\x12&\n\x0b\n\x07terrain\x10!\x12\x08\x08\x06(\x028\x01H\x02\x1a\x04\x08\x05\x10$"\x07terrain\x12"\n\t\n\x05vague\x10)\x12\x08\x08\x06(\x028\x01H\x02\x1a\x04\x08\x07\x10\x1a"\x05vague\x1a\x02fr'


docFromSerialized = gnlp(serializedDoc)

print([tok.text for tok in docFromSerialized])
print([tok.shape for tok in docFromSerialized])
print([sent for sent in docFromSerialized.sentences])
# ['Avec', 'la', 'mer', 'du', 'Nord', 'pour', 'dernier', 'terrain', 'vague']
# ['Xxxx', 'xx', 'xxx', 'xx', 'Xxxx', 'xxxx', 'xxxxxxx', 'xxxxxxx', 'xxxxx']
# [['Avec', 'la', 'mer', 'du', 'Nord', 'pour', 'dernier', 'terrain', 'vague']]
