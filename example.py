from google_spacy import GoogleSpacy
gspacy = GoogleSpacy()
sentences, tokens = gspacy.nlp("The lion is walking. It is in the forest.")

print([tok.text for tok in tokens])
print([tok.shape for tok in tokens])
print([sent for sent in sentences])
