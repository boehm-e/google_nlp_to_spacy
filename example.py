from google_spacy import GoogleSpacy
gspacy = GoogleSpacy()
tokens = gspacy.nlp("The lion is walking")

print([tok.text for tok in tokens])
print([tok.shape for tok in tokens])
