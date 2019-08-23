# GOOGLE NLP TO SPACY

A wrapper to make google cloud natural language API return elements structured like spacy

### Context
I was working on a NLP project and began to create algorithmes with spacy classes.
For some reason (mostly scalability, and performances) I decided to switch to google cloud language, which achieve the current state of the art results on 11 NLP tasks ([google blog](https://ai.googleblog.com/2018/11/open-sourcing-bert-state-of-art-pre.html))

### Goal
The goal of this project is to provide a simple transition from Spacy to Google Cloud NLP by providing wrappers to Google NLP that matches Spacy's documentation.
So (ideally) we only have to change a few line to our code and all is working.

### Prerequisites

in order to run this, you will need the google cloud language package :
```
pip install google-cloud-language
```

# Usage
## To use this module do as follow :

### clone the repository
```
git clone git@github.com:boehm-e/google_nlp_to_spacy.git
```
### try it
```
python3 example.py
```

### use in your project
```python
#setup
gspacy = GoogleSpacy()
gnlp = gspacy.load('fr')

doc = gnlp("Le lion marche dans la foret.")
for token in doc:
    print( token.text, token.lemma_, token.pos_, token.dep_ )

  # | lion   | lion    | NOUN  | nsubj   |
  # |--------|---------|-------|---------|
  # | marche | marcher | VERB  | root    |
  # |--------|---------|-------|---------|
  # | dans   | dans    | ADP   | prep    |
  # |--------|---------|-------|---------|
  # | la     | le      | DET   | det     |
  # |--------|---------|-------|---------|
  # | foret  | foret   | NOUN  | pobj    |
  # |--------|---------|-------|---------|
  # | .      | .       | PUNCT | p       |


doc = gnlp("Le lion marche. Il est dans la foret.")
print(doc.sents)
# [Le lion marche., Il est dans la foret.]
```

### export and import
you can export and import document (for example, to store it in a database)

#### export to json
```python

# export
doc = gnlp("Avec la mer du Nord pour dernier terrain vague")
jsonDoc = doc.to_json()

#>{'text': 'Avec la mer du Nord pour dernier terrain vague',
#  'sents': [{'start': 0, 'end': 40}],
#  'tokens': [{'id': 0,
#    'text': 'Avec',
#    'lemma': 'Avec',
#    'gender': 'GENDER_UNKNOWN',
#    'person': 'PERSON_UNKNOWN',
#    'number': 'NUMBER_UNKNOWN',
#    'start': 0,
#    'end': 4,
#    'pos': 'ADP',
#    'dep': 'root',
#    'head': 0},
#   ... ... ...
#   {'id': 8,
#    'text': 'vague',
#    'lemma': 'vague',
#    'gender': 'MASCULINE',
#    'person': 'PERSON_UNKNOWN',
#    'number': 'SINGULAR',
#    'start': 41,
#    'end': 46,
#    'pos': 'NOUN',
#    'dep': 'nn',
#    'head': 7}]
#   }
```

#### import from json

```python
doc = gnlp(jsonDoc, from_json=True) # we take the json export from previous example

print(doc[2])
#> mer
```

### References

- ### GSDoc

| Name          | Type     | Description                                       |
| ------------- | -------- | --------------------------------------------------|
|  \_\_getitem\_\_ (position)          | GSToken   | The token at doc[i].                            |
|  \_\_getitem\_\_ (range)          | GSSpan   | The span at doc[start:end].                            |
|  to_json()          | json   | A json representation of the document who can be stored and used to construct the same Doc |

- ## GSSpan

| Name          | Type     | Description                                       |
| ------------- | -------- | --------------------------------------------------|
|  doc         | GSDoc   | The parent document.                            |
|  start         | int   | The index of the first token of the span. |
|  end         | int   |  The index of the first token after the span. |
|  to_json()          | json   | A json representation of the document who can be stored and used to construct the same Doc |

- ### GSToken

| Name          | Type     | Description                                       |
| ------------- | -------- | --------------------------------------------------|
|  text         | String   | Verbatim text content.                            |
|  pos_         | String   | Coarse-grained part-of-speech                     |
|  dep_         | String   | Syntactic dependency relation                     |
|  head         | *GSToken | The head index in the dependency tree             |
|  lefts        | *GSToken | The leftward immediate children of the word, in the syntactic dependency parse. |
|  rights         | *GSToken | The rightward immediate children of the word, in the syntactic dependency parse.|
|  children         | *GSToken | A sequence of the token’s immediate syntactic children. |
|  i            | Integer  | The index of the token within the parent document.|
|  idx          | Integer  | The begin offset of the token within the document.|
|  lemma_       | String   | Base form of the token                            |
|  lower        | String   | Lowercase form of the token                       |
|  shape        | String   | "Hello World" => "Xxxxx Xxxxx"                    |
|  gender       | String   | GENDER_UNKNOWN \| FEMININE \| MASCULINE \| NEUTER    |
|  person       | String   | PERSON_UNKNOWN \| FIRST \| SECOND \| THIRD \| REFLEXIVE_PERSON |
|  number       | String   | NUMBER_UNKNOWN \| SINGULAR \| PLURAL \| DUAL  |
|  is_lower     | Boolean  | Is the token in lowercase?                        |
|  is_upper     | Boolean  | Is the token in uppercase?                        |
|  is_title     | Boolean  | Is the token in titlecase?                        |
|  is_space     | Boolean  | Does the token consist of whitespace characters?  |

## Authors
* **Erwan BOEHM** - [github](https://github.com/boehm-e/)
