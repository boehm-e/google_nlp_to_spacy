from google_spacy import GoogleSpacy

gspacy = GoogleSpacy()
gnlp = gspacy.load('fr')

# create a document
doc = gnlp("Avec la mer du Nord pour dernier terrain vague")

print([tok.text for tok in doc])
print([tok.shape for tok in doc])
print([sent for sent in doc.sents])
# [Avec, la, mer, du, Nord, pour, dernier, terrain, vague]
# ['Xxxx', 'xx', 'xxx', 'xx', 'Xxxx', 'xxxx', 'xxxxxxx', 'xxxxxxx', 'xxxxx']
# [['Avec', 'la', 'mer', 'du', 'Nord', 'pour', 'dernier', 'terrain', 'vague']]


# export the document to json:
jsonDoc = doc.to_json()


docFromJson = gnlp(jsonDoc, from_json=True)

print([tok.text for tok in docFromJson])
print([tok.shape for tok in docFromJson])
print([sent for sent in docFromJson.sents])
# ['Avec', 'la', 'mer', 'du', 'Nord', 'pour', 'dernier', 'terrain', 'vague']
# ['Xxxx', 'xx', 'xxx', 'xx', 'Xxxx', 'xxxx', 'xxxxxxx', 'xxxxxxx', 'xxxxx']
# [['Avec', 'la', 'mer', 'du', 'Nord', 'pour', 'dernier', 'terrain', 'vague']]
