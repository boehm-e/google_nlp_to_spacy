# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

pos_tag = ('UNKNOWN', 'ADJ', 'ADP', 'ADV', 'CONJ', 'DET', 'NOUN',
           'NUM', 'PRON', 'PRT', 'PUNCT', 'VERB', 'X', 'AFFIX')
dep_tag = ('UNKNOWN', 'abbrev', 'acomp', 'advcl', 'advmod', 'amod', 'appos', 'attr', 'aux', 'auxpass', 'cc', 'ccomp', 'conj', 'csubj', 'csubjpass', 'dep', 'det', 'discourse', 'dobj', 'expl', 'goeswith', 'iobj', 'mark', 'mwe', 'mwv', 'neg', 'nn', 'npadvmod', 'nsubj', 'nsubjpass', 'num', 'number', 'p', 'parataxis', 'partmod', 'pcomp', 'pobj', 'poss', 'postneg', 'precomp', 'preconj', 'predet',
           'pref', 'prep', 'pronl', 'prt', 'ps', 'quantmod', 'rcmod', 'rcmodrel', 'rdrop', 'ref', 'remnant', 'reparandum', 'root', 'snum', 'suff', 'tmod', 'topic', 'vmod', 'vocative', 'xcomp', 'suffix', 'title', 'advphmod', 'auxcaus', 'auxvv', 'dtmod', 'foreign', 'kw', 'list', 'nomc', 'nomcsubj', 'nomcsubjpass', 'numc', 'cop', 'dislocated', 'asp', 'gmod', 'gobj', 'infmod', 'mes', 'ncomp')


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
        self.idx = token.text.begin_offset  # pos of first letter of token

    def __repr__(self):
        return repr(self.text)

    def make_references(self, tokens):
        self.lefts = [left_token for left_token in tokens if self.head_
                      == left_token.head_ and left_token.i < self.i]
        self.rights = [right_token for right_token in tokens if self.head_
                       == right_token.head_ and right_token.i > self.i]
        # print(self.text, self.lefts, self.rights)
        self.head = tokens[self.head]


class GoogleSpacy(object):
    def __init__(self):
        self.lang = 'en'
        self.GSTokens = []

    def __str__(self):
        return 'Fubar'

    def set_language(self, lang):
        self.lang = lang

    def process_tokens(self, tokens):
        self.GSTokens = []
        for i, token in enumerate(tokens):
            self.GSTokens.append(GSToken(token, i))

        for token in self.GSTokens:
            token.make_references(self.GSTokens)

        return self.GSTokens

    def process_sentences(self, doc, sents):
        sentences = []
        offsets = [{"begin": sent.text.begin_offset, "end": sent.text.begin_offset + len(sent.text.content)} for sent in sents]

        for offset in offsets:
            begin = offset["begin"]
            end = offset["end"]
            sentences.append([tok for tok in doc if tok.idx >= begin and tok.idx <= end])

        return sentences

    def nlp(self, text):
        # Instantiates a client
        client = language.LanguageServiceClient()

        # Instantiates a plain text document.
        document = types.Document(
            content=text,
            language=self.lang,
            type=enums.Document.Type.PLAIN_TEXT)

        # Detects syntax in the document. You can also analyze HTML with:
        ret = client.analyze_syntax(document, enums.EncodingType.UTF32)
        doc = self.process_tokens(ret.tokens)
        sentences = self.process_sentences(doc, ret.sentences)
        return [sentences, doc]
