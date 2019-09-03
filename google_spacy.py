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


def normalize_slice(length, start, stop, step=None):
    if not (step is None or step == 1):
        raise ValueError("test")
    if start is None:
        start = 0
    elif start < 0:
        start += length
    start = min(length, max(0, start))
    if stop is None:
        stop = length
    elif stop < 0:
        stop += length
    stop = min(length, max(start, stop))
    return start, stop


# # helpers
# def to_string(txt):
#     punctRegex = re.compile('\s(?=[\.\?!,])', flags=re.IGNORECASE)
#     apostrophRegex = re.compile("(?<=(l'|s'|m'|n'|t'))\s", flags=re.IGNORECASE)
#     txt = punctRegex.sub('', txt)
#     txt = apostrophRegex.sub('', txt)
#     return txt


class GSSpan(object):
    """docstring for GSSpan"""

    def __init__(self, txt, doc, start, end):
        super(GSSpan, self).__init__()
        self.doc = doc
        self.txt = txt
        self.start = start
        self.end = end

    def __getitem__(self, index):
        if isinstance(index, slice):
            start, end = normalize_slice(len(self), index.start, index.stop, index.step)
            return GSSpan(self.txt, self.doc, start + self.start, end + self.start)
        else:
            if index < 0:
                return self.doc[self.end]
            else:
                return self.doc[self.start + index]

    def __iter__(self):
        # self._recalculate_indices()
        for i in range(self.start, self.end):
            yield self.doc[i]

    def __str__(self):
        return self.to_string()

    def __repr__(self):
        return self.to_string()

    def __len__(self):
        return self.end - self.start

    def to_string(self):
        start = self.doc[self.start].idx
        end = self.doc[self.end-1].idx + len(self.doc[self.end-1].text)
        txt = self.txt[start:end]
        return txt

    def to_json(self):
        obj = {}
        obj["text"] = self.to_string()
        obj["tokens"] = [{
            "id": tok.i,
            "text": tok.text,
            "lemma": tok.lemma_,
            "gender": tok.gender,
            "person": tok.person,
            "number": tok.number,
            "start": tok.idx,
            "end": tok.idx + len(tok.text),
            "pos": tok.pos_,
            "dep": tok.dep_,
            "head": tok.head.i
        } for tok in self.doc[self.start:self.end]]
        return obj


class GSDoc(object):
    """docstring for GSDoc."""

    def __init__(self, txt, raw, from_json=False):
        super(GSDoc, self).__init__()
        self.from_json = from_json
        self.txt = txt
        self.raw = raw  # data from google cloud nlp | from json dump

        if self.from_json is True:
            self.doc = self.process_tokens(self.raw["tokens"])
            self.sents = self.process_sentences(self.doc, self.raw["sents"])
        else:
            self.doc = self.process_tokens(self.raw.tokens)
            self.sents = self.process_sentences(self.doc, self.raw.sentences)

    def __getitem__(self, index):
        if isinstance(index, slice):
            start, stop = normalize_slice(len(self.doc), index.start, index.stop, index.step)
            return GSSpan(self.txt, self.doc, start, stop)
        if index < 0:
            index = self.length + index
        # bounds_check(i, self.length, PADDING)
        return self.doc[index]

    def __str__(self):
        return self.to_string()

    def __len__(self):
        return len(self.doc)

    def __repr__(self):
        return self.to_string()

    def to_string(self):
        start = self.doc[0].idx
        end = self.doc[-1].idx + len(self.doc[-1].text)
        txt = self.txt[start:end]
        return txt

    def to_json(self):
        obj = {}
        obj["text"] = self.txt
        obj["sents"] = [{"start":sent[0].idx, "end": sent[-1].idx + len(sent[-1].text)} for sent in self.sents]
        obj["tokens"] = [{
            "id": tok.i,
            "text": tok.text,
            "lemma": tok.lemma_,
            "gender": tok.gender,
            "person": tok.person,
            "number": tok.number,
            "start": tok.idx,
            "end": tok.idx + len(tok.text),
            "pos": tok.pos_,
            "dep": tok.dep_,
            "head": tok.head.i
        } for tok in self.doc]
        return obj

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
            self.GSTokens.append(GSToken(token, i, from_json=self.from_json))

        for token in self.GSTokens:
            token.make_references(self.GSTokens)

        for token in self.GSTokens:
            token.find_childrens(self.GSTokens)

        return self.GSTokens

    def process_sentences(self, doc, sents):
        sentences = []
        if self.from_json is True:
            offsets = [{"begin": sent["start"], "end": sent["end"]} for sent in sents]
        else:
            offsets = [{"begin": sent.text.begin_offset, "end": sent.text.begin_offset + len(sent.text.content)} for sent in sents]

        for offset in offsets:
            begin = offset["begin"]
            end = offset["end"]
            st = [tok for tok in doc if tok.idx >= begin and tok.idx <= end]
            _begin = st[0].i
            _end = st[-1].i

            sentences.append(GSSpan(self.txt, doc, _begin, _end))

        return sentences


class GSToken(object):
    def __init__(self, token, index, from_json=False):
        # self.token = self.build_token(token, i)
        if from_json is True:
            self.text = token["text"]
            self.lower_ = self.text.lower()
            self.shape = "".join(["X" if x.isupper() else "x" for x in self.text])
            self.lemma_ = token["lemma"]
            self.pos_ = token["pos"]
            self.dep_ = token["dep"]
            self.head = token["head"]
            self.head_ = token["head"]
            self.gender = token["gender"]
            self.person = token["person"]
            self.number = token["number"]
            self.is_lower = self.text.islower()
            self.is_upper = self.text.isupper()
            self.is_title = self.text.istitle()
            self.is_space = self.text.isspace()
            self.i = index
            self.idx = token["start"]  # pos of first letter of token
        else:
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

    def __str__(self):
        return self.text

    def __repr__(self):
        return self.text

    def make_references(self, tokens):
        self.lefts = [left_token for left_token in tokens if self.i == tokens[left_token.head_].i and left_token.i < self.i]
        self.rights = [right_token for right_token in tokens if self.i == tokens[right_token.head_].i and right_token.i > self.i]
        self.head = tokens[self.head]

    def find_childrens(self, doc):
        self.doc = doc
        self.children = [tok for tok in self.doc if tok.head.i == self.i]


class GoogleSpacy(object):
    def __init__(self):
        self.lang = 'en'
        self.GSTokens = []

    def __str__(self):
        return 'Fubar'

    def load(self, lang):
        self.lang = lang
        return self.nlp

    def sort_by_index(self, tokList):
        lst = tokList
        lst.sort(key=lambda x: x.i)
        return lst

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

    def doc_to_string(self, doc):
        txt = " ".join([tok.text for tok in doc])
        return to_string(txt)

    def nlp(self, raw, from_json=False):
        if from_json is False:
            text = raw

            # Instantiates a client
            client = language.LanguageServiceClient()
            # Instantiates a plain text document.
            document = types.Document(
                content=text,
                language=self.lang,
                type=enums.Document.Type.PLAIN_TEXT)

            # Detects syntax in the document. You can also analyze HTML with:
            ret = client.analyze_syntax(document, enums.EncodingType.UTF32)
            data = ret
            return GSDoc(text, data, from_json=from_json)
        else:
            json = raw
            text = json["text"]
            return GSDoc(text, json, from_json=from_json)


# helpers
def to_string(txt):
    punctRegex = re.compile('\s(?=[\.\?!,])', flags=re.IGNORECASE)
    apostrophRegex = re.compile("(?<=(l'|s'|m'|n'|t'))\s", flags=re.IGNORECASE)
    txt = punctRegex.sub('', txt)
    txt = apostrophRegex.sub('', txt)
    return txt
