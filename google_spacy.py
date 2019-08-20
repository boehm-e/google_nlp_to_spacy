# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import re

pos_tag = ('UNKNOWN', 'ADJ', 'ADP', 'ADV', 'CONJ', 'DET', 'NOUN', 'NUM', 'PRON', 'PRT', 'PUNCT', 'VERB', 'X', 'AFFIX')
dep_tag = ('UNKNOWN', 'abbrev', 'acomp', 'advcl', 'advmod', 'amod', 'appos', 'attr', 'aux', 'auxpass', 'cc', 'ccomp', 'conj', 'csubj', 'csubjpass', 'dep', 'det', 'discourse', 'dobj', 'expl', 'goeswith', 'iobj', 'mark', 'mwe', 'mwv', 'neg', 'nn', 'npadvmod', 'nsubj', 'nsubjpass', 'num', 'number', 'p', 'parataxis', 'partmod', 'pcomp', 'pobj', 'poss', 'postneg', 'precomp', 'preconj', 'predet', 'pref', 'prep', 'pronl', 'prt', 'ps', 'quantmod', 'rcmod', 'rcmodrel', 'rdrop', 'ref', 'remnant', 'reparandum', 'root', 'snum', 'suff', 'tmod', 'topic', 'vmod', 'vocative', 'xcomp', 'suffix', 'title', 'advphmod', 'auxcaus', 'auxvv', 'dtmod', 'foreign', 'kw', 'list', 'nomc', 'nomcsubj', 'nomcsubjpass', 'numc', 'cop', 'dislocated', 'asp', 'gmod', 'gobj', 'infmod', 'mes', 'ncomp')
gender_tag = ('GENDER_UNKNOWN', 'FEMININE', 'MASCULINE', 'NEUTER')
person_tag = ('PERSON_UNKNOWN', 'FIRST', 'SECOND', 'THIRD', 'REFLEXIVE_PERSON')
number_tag = ('NUMBER_UNKNOWN', 'SINGULAR', 'PLURAL', 'DUAL')


# helpers
def to_string(txt):
    punctRegex = re.compile('\s(?=[\.\?!,])', flags=re.IGNORECASE)
    apostrophRegex = re.compile("(?<=(l'|s'|m'|n'|t'))\s", flags=re.IGNORECASE)
    txt = punctRegex.sub('', txt)
    txt = apostrophRegex.sub('', txt)
    return txt


class Nlp(object):
    """docstring for Nlp."""

    def __init__(self, ret):
        super(Nlp, self).__init__()

        self.ret = ret
        self.doc = self.process_tokens(self.ret.tokens)
        self.sentences = self.process_sentences(self.doc, self.ret.sentences)

    def __getitem__(self, index):
        return self.doc[index]

    def __str__(self):
        # txt = " ".join([tok.text for tok in self.doc])
        return self.to_string()

    def serialize(self):
        return self.ret.SerializeToString()

    def to_string(self):
        txt = " ".join([tok.text for tok in self.doc])
        return to_string(txt)

    def find_children_direct(self, head):
        return [tok for tok in self.doc if tok if tok.head.i == head.i]

    def find_children_tree(self, head):
        children_final = []  # liste contenant toute l'arborescence des enfants d'un token
        children_direct = self.find_children_direct(head)  # liste contenant les enfants direct d'un token
        children_final.append(children_direct)  # on ajoute au children_final, les enfants direct du token recherche
        while children_direct:  # tant qu'on decouvre de nouveaux enfants a un token
            new_children = []
            for c in children_direct:
                new_children += self.find_children_direct(c)

            if len(new_children) > 0:
                children_final.append(new_children)
            children_direct = new_children
        flatten = [item for sublist in children_final for item in sublist]  # flatten list
        flatten.sort(key=lambda x: x.i)
        return flatten

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
        self.gender = gender_tag[token.part_of_speech.gender]
        self.person = person_tag[token.part_of_speech.person]
        self.number = number_tag[token.part_of_speech.number]
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
        self.lefts = [left_token for left_token in tokens if self.i == tokens[left_token.head_].i and left_token.i < self.i]
        self.rights = [right_token for right_token in tokens if self.i == tokens[right_token.head_].i and right_token.i > self.i]
        self.head = tokens[self.head]
        # print(self.text, self.lefts, self.rights)


class GoogleSpacy(object):
    def __init__(self):
        self.lang = 'en'
        self.GSTokens = []

    def __str__(self):
        return 'Fubar'

    def set_language(self, lang):
        self.lang = lang

    def sort_by_index(self, tokList):
        lst = tokList
        lst.sort(key=lambda x: x.i)
        return lst

    def doc_to_string(self, doc):
        txt = " ".join([tok.text for tok in doc])
        return to_string(txt)

    def find_children_direct(self, doc, head):
        return [tok for tok in doc if tok if tok.head.i == head.i]

    def find_children_tree(self, doc, head):
        children_final = []  # liste contenant toute l'arborescence des enfants d'un token
        children_direct = self.find_children_direct(doc, head)  # liste contenant les enfants direct d'un token
        children_final.append(children_direct)  # on ajoute au children_final, les enfants direct du token recherche
        while children_direct:  # tant qu'on decouvre de nouveaux enfants a un token
            new_children = []
            for c in children_direct:
                new_children += self.find_children_direct(doc, c)

            if len(new_children) > 0:
                children_final.append(new_children)
            children_direct = new_children
        flatten = [item for sublist in children_final for item in sublist]  # flatten list
        flatten.sort(key=lambda x: x.i)
        return flatten

    def correct_punct(self, txt):
        return to_string(txt)

    def nlp(self, text):
        if isinstance(text, str):
            # Instantiates a client
            client = language.LanguageServiceClient()
            # Instantiates a plain text document.
            document = types.Document(
                content=text,
                language=self.lang,
                type=enums.Document.Type.PLAIN_TEXT)

            # Detects syntax in the document. You can also analyze HTML with:
            ret = client.analyze_syntax(document, enums.EncodingType.UTF32)
            return Nlp(ret)

        elif isinstance(text, bytes):
            return Nlp(types.AnalyzeSyntaxResponse().FromString(text))
