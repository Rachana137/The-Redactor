import glob
import nltk
import spacy
import sys
from spacy.matcher import Matcher
from commonregex import CommonRegex
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import wordnet as wn

nlp = spacy.load("en_core_web_sm")


# Input files
def input(input_file):
    with open(input_file, 'r') as file:
        data = file.read()
    return data


# Phone Numbers
def extract_phone_number(data):
    # data = names_(data)
    matcher = Matcher(nlp.vocab)
    pattern = [{'ORTH': '('}, {'SHAPE': 'ddd'}, {'ORTH': ')'},
               {'ORTH': '-', 'OP': '?'}, {'SHAPE': 'ddd'}, {'ORTH': '-', 'OP': '?'}, {'SHAPE': 'dddd'}]
    matcher.add("PhoneNumber", [pattern])
    doc = nlp(data)
    matches = matcher(doc)
    ph = []
    for match_id, start, end in matches:
        ph.append(doc[start:end].text)
    for num in ph:
        data = data.replace(num, u"\u2588" * len(num))

    return data, ph


# Names
def names_(data):
    matcher = Matcher(nlp.vocab)
    pattern = [{'POS': 'PROPN'},{'ORTH':',','OP':'?'} ,{'POS': 'PROPN', 'OP': '?'}]
    matcher.add('name', [pattern])
    doc = nlp(data)
    matches = matcher(doc)
    l2 = []
    for match_id, start, end in matches:
        span = doc[start:end]
        for i in span.ents:
            if i.label_ == 'PERSON':
                l2.append(i.text)
    redact_doc = data
    for word in l2:
        redact_doc = redact_doc.replace(word, u"\u2588" * len(word))

    return redact_doc, l2


# Dates
def Dates(data):
    date = CommonRegex(data)
    d_count = []
    for dat in date.dates:
        d_count.append(dat)
        data = data.replace(dat, u"\u2588" * len(dat))

    return data, d_count


# Genders
def genders(data):
    gen = ['he', 'she', 'her', 'his', 'mr.', 'miss.',
           'mr', 'miss', 'men', 'women', 'man', 'woman',
           'they', 'himself', 'herself', 'father', 'mother', 'girl', 'boy']
    doc = nlp(data)
    g_count = []
    for word in doc:
        x = word.text
        if x.lower() in gen:
            g_count.append(x)
            data = data.replace(x, u"\u2588" * len(x))

    return data, g_count


# Adresses
def address(data):
    doc = nlp(data)
    ad_matcher = Matcher(nlp.vocab)
    pattern = [{'SHAPE': 'dddd'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}, {'SHAPE': '\n','OP':'?'}, {'POS': 'PROPN'},
               {'POS': 'PROPN'}, {'SHAPE': 'dddd'}]
    ad_matcher.add('Address', [pattern])
    matches = ad_matcher(doc)
    l4 = []
    for match_id, start, end in matches:
        span = doc[start:end]
        l4.append(span.text)
    for w in l4:
        data = data.replace(w, u"\u2588" * len(w))

    return data, l4


# Concept
def concept(data, concept):
    concept_list = []
    synonyms = wn.synsets(concept)

    for syn in synonyms:
        words = syn.lemma_names()
        for w in words:
            if w not in concept_list:
                concept_list.append(w)

    sentences = nltk.sent_tokenize(data)
    l5 = []
    for sentence in sentences:
        for c in concept_list:
            if c.lower() in sentence.lower():
                l5.append(sentence)
                data = data.replace(sentence, u"\u2588" * len(sentence))
    return data, l5


# Stats
def stats(data, c, file,n):
    Name = len(names_(data)[1])
    Ph_no = len(extract_phone_number(data)[1])
    Date = len(Dates(data)[1])
    Gender = len(genders(data)[1])
    Address = len(address(data)[1])
    Concept = len(concept(data, c)[1])
    l = [Name, Ph_no, Date, Gender, Address, Concept]
    redacted_list = ['Names', 'Phone Number', 'Dates', 'Gender', 'Address', 'Concept']
    txt = []
    for i in range(0, len(redacted_list)):
        x = 'The number of ' + redacted_list[i] + ' redacted from the file: ' + str(l[i])
        txt.append(x)
    total = 0
    for words in range(0, len(l)):
        total = total + l[words]
    y = 'Total number of redactions in the file is :' + str(total)
    txt.append(y)
    if file == 'stdout':
        # s=sys.stdout
        for t in txt:
            # s.write(t+'\n')
            print(t)
    elif file == 'stderr':
        error = []
        for i in range(0, len(l)):
            if l[i] == 0:
                err = 'There are no ' + redacted_list[i] + ' to be redacted from the file.'
                error.append(err)
        filepath=('./stats/file%s_stderr.txt'%(n+1))
        with open(filepath,'w+') as f:
            for e in error:
                f.write(e + '\n')
    else:
        txt_store = 'file'+ str(n)+ '\n'
        for i in range(0, len(txt)):
            txt_store += str(txt[i]) + '\n'

        class FileManager():  # defining context manager class named FileManager
            def __init__(self, filename, mode):
                self.filename = filename
                self.mode = mode

            def __enter__(self):
                self.file = open(self.filename, self.mode)
                return self.file

            def __exit__(self, exc_type, exc_value, traceback):
                self.file.close()

        filepath = ('./stats/%s%d.txt'%(file,n+1))
        with FileManager(filepath, 'w') as file:
            file.write(txt_store+'\n')


# Output stored in a text file.
def output(data, file, path):
    filepath = ('./files/ redacted_%s' % ( file))
    with open(filepath, 'w+', encoding='utf-8') as f:
        f.write(data)
        f.close()
