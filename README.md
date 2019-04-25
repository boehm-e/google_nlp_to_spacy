# google_nlp_to_spacy

A wrapper to make google cloud natural language API return elements structured like spacy

### Context
I was working on a NLP project and began to create algorithmes with spacy classes (mostly the Token class).
For some reason (mostly scalability, and performances) I decided to switch to google cloud language, which acchieve the current state of the art results on 11 NLP tasks ([google blog](https://ai.googleblog.com/2018/11/open-sourcing-bert-state-of-art-pre.html))

### Goal
The goal of this project is to provide a simple transition Spacy to Google Cloud NLP by providing wrappers to Google NLP that matches Spacy documentation.
So (ideally) we only have to change a few line to our code and all would be working.

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
    python example.py
    ```

- use in your project
    ```python
    from google_spacy import GoogleSpacy
    gspacy = GoogleSpacy()
    sentences, tokens = gspacy.nlp("The lion is walking.")


    for token in tokens:
      print( token.text, token.lemma_, token.pos_, token.dep_ )

    # The       The     DET    DET
    # lion      lion    NOUN   NSUBJ
    # is        be      VERB   AUX
    # walking   walk    VERB   ROOT

    sentences, tokens = gspacy.nlp("The lion is walking. It is in the forest.")
    print(sentences)
    # each is of type GSToken, so you can access its dep, pos, lemma ...
    # [ ["The", "lion", "is", "walking", "."], ["It", "is", "in", "the", "forest."] ]

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
