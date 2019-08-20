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

### Usage
To use this module do as follow :

- clone the repository
    ```
    git clone git@github.com:boehm-e/google_nlp_to_spacy.git
    ```
- run the example
    ```
    python3 example.py
    ```

- use in your project
    ```python
    #setup
    gspacy = GoogleSpacy()
    gspacy.set_language('fr')
    gnlp = gspacy.nlp

    doc = gnlp("The lion is walking.")
    for token in doc:
      print( token.text, token.lemma_, token.pos_, token.dep_ )

    # The       The     DET    DET
    # lion      lion    NOUN   NSUBJ
    # is        be      VERB   AUX
    # walking   walk    VERB   ROOT


    doc = gnlp("The lion is walking. It is in the forest.")
    print(doc.sentences)
    # [ ["The", "lion", "is", "walking", "."], ["It", "is", "in", "the", "forest", "."] ]
    # each is of type GSToken, so you can access its dep, pos, lemma ...

    ```

- serialization and deserialization
    ```python
    # you can call gnlp with text or serialized bytes (from database)

    # serialize
    doc = gnlp("Avec la mer du Nord pour dernier terrain vague")

    serializedDoc = doc.serialize()
    #> b'\n2\n0\n.Avec la mer du Nord pour dernier terrain vague\x12\x18\n\x06\n\x04Avec\x12\x04\x08\x02H\x02\x1a\x02\x106"\x04Avec\x12\x1c\n\x06\n\x02la\x10\x05\x12\x08\x08\x05(\x018\x01H\x02\x1a\x04\x08\x02\x10\x10"\x02le\x12\x1c\n\x07\n\x03mer\x10\x08\x12\x08\x08\x06(\x018\x01H\x02\x1a\x02\x10$"\x03mer\x12\x1c\n\x06\n\x02du\x10\x0c\x12\x08\x08\x02(\x028\x01H\x02\x1a\x04\x08\x02\x10+"\x02du\x12 \n\x08\n\x04Nord\x10\x0f\x12\x08\x08\x06(\x028\x01H\x01\x1a\x04\x08\x03\x10$"\x04Nord\x12\x1a\n\x08\n\x04pour\x10\x14\x12\x04\x08\x02H\x02\x1a\x02\x10+"\x04pour\x12&\n\x0b\n\x07dernier\x10\x19\x12\x08\x08\x01(\x028\x01H\x02\x1a\x04\x08\x07\x10\x05"\x07dernier\x12&\n\x0b\n\x07terrain\x10!\x12\x08\x08\x06(\x028\x01H\x02\x1a\x04\x08\x05\x10$"\x07terrain\x12"\n\t\n\x05vague\x10)\x12\x08\x08\x06(\x028\x01H\x02\x1a\x04\x08\x07\x10\x1a"\x05vague\x1a\x02fr'

    deserializedDoc = gnlp(serializedDoc)

    # here doc and deserializedDoc are the same
    ```
## References

- ### GSToken

| Name          | Type     | Description                                       |
| ------------- | -------- | --------------------------------------------------|
|  text         | String   | Verbatim text content.                            |
|  pos_         | String   | Coarse-grained part-of-speech                     |
|  dep_         | String   | Syntactic dependency relation                     |
|  head         | *GSToken | The head index in the dependency tree             |
|  i            | Integer  | The index of the token within the parent document.|
|  idx          | Integer  | The begin offset of the token within the document.|
|  lemma_       | String   | Base form of the token                            |
|  lower        | String   | Lowercase form of the token                       |
|  shape        | String   | "Hello World" => "Xxxxx Xxxxx"                    |
|  is_lower     | Boolean  | Is the token in lowercase?                        |
|  is_upper     | Boolean  | Is the token in uppercase?                        |
|  is_title     | Boolean  | Is the token in titlecase?                        |
|  is_space     | Boolean  | Does the token consist of whitespace characters?  |

## Authors
* **Erwan BOEHM** - [github](https://github.com/boehm-e/)
