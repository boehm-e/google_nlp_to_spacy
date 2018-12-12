import sys
import munch


# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

pos_tag = ('UNKNOWN', 'ADJ', 'ADP', 'ADV', 'CONJ', 'DET', 'NOUN', 'NUM','PRON', 'PRT', 'PUNCT', 'VERB', 'X', 'AFFIX')
dep_tag = ('UNKNOWN', 'ABBREV', 'ACOMP', 'ADVCL', 'ADVMOD', 'AMOD', 'APPOS', 'ATTR', 'AUX', 'AUXPASS', 'CC', 'CCOMP', 'CONJ', 'CSUBJ', 'CSUBJPASS', 'DEP', 'DET', 'DISCOURSE', 'DOBJ', 'EXPL', 'GOESWITH', 'IOBJ', 'MARK', 'MWE', 'MWV', 'NEG', 'NN', 'NPADVMOD', 'NSUBJ', 'NSUBJPASS', 'NUM', 'NUMBER', 'P', 'PARATAXIS', 'PARTMOD', 'PCOMP', 'POBJ', 'POSS', 'POSTNEG', 'PRECOMP', 'PRECONJ', 'PREDET', 'PREF', 'PREP', 'PRONL', 'PRT', 'PS', 'QUANTMOD', 'RCMOD', 'RCMODREL', 'RDROP', 'REF','REMNANT','REPARANDUM', 'ROOT', 'SNUM', 'SUFF', 'TMOD', 'TOPIC', 'VMOD', 'VOCATIVE', 'XCOMP', 'SUFFIX', 'TITLE', 'ADVPHMOD', 'AUXCAUS', 'AUXVV', 'DTMOD', 'FOREIGN', 'KW', 'LIST', 'NOMC', 'NOMCSUBJ', 'NOMCSUBJPASS', 'NUMC', 'COP', 'DISLOCATED', 'ASP', 'GMOD', 'GOBJ', 'INFMOD', 'MES', 'NCOMP')

class GSToken(object):
    def __init__(self, token, index):
        # self.token = self.build_token(token, i)
        self.text = token.text.content
        self.lower_ = token.text.content.lower()
        self.shape = "".join(["X" if x.isupper() else "x" for x in self.text])
        self.lemma_ = token.lemma
        self.pos_ = pos_tag[token.part_of_speech.tag]
        self.dep_ = dep_tag[token.dependency_edge.label]
        self.head = token.dependency_edge.head_token_index
        self.head_ = token.dependency_edge.head_token_index
        self.is_lower = self.text.islower()
        self.is_upper = self.text.isupper()
        self.is_title = self.text.istitle()
        self.is_space = self.text.isspace()
        self.i = index

    def __repr__(self):
        return repr(self.text)

    def make_references(self, tokens):
        self.lefts  = [left_token for left_token in tokens if self.head_ == left_token.head_ and left_token.i < self.i ]
        self.rights = [right_token for right_token in tokens if self.head_ == right_token.head_ and right_token.i > self.i]
        # print(self.text, self.lefts, self.rights)
        self.head = tokens[self.head]


class GoogleSpacy(object):
    def __init__(self):
        self.GSTokens = []

    def __str__(self):
        return 'Fubar'

    def process_tokens(self, tokens):
        self.GSTokens = []
        for i, token in enumerate(tokens):
            self.GSTokens.append(GSToken(token, i))
        for token in self.GSTokens:
            token.make_references(self.GSTokens)


    def nlp(self, text):
        # Instantiates a client
        client = language.LanguageServiceClient()

        # Instantiates a plain text document.
        document = types.Document(
            content=text,
            type=enums.Document.Type.PLAIN_TEXT)

        # Detects syntax in the document. You can also analyze HTML with:
        tokens = client.analyze_syntax(document).tokens
        self.process_tokens(tokens)

        return self.GSTokens
