import glob
import nltk
import spacy
import sys
from spacy.matcher import Matcher
from commonregex import CommonRegex
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import wordnet as wn
import os

nlp = spacy.load("en_core_web_sm")


# Input files
def input(input_file):
    with open(input_file, 'r') as file:
        data = file.read()
    return data


# Phone Numbers
def extract_phone_number(data):
    doc = nlp(data)
    matcher = Matcher(nlp.vocab)
    pattern1 = [{'ORTH': '('}, {'SHAPE': 'ddd'}, {'ORTH': ')'},
                {'ORTH': '-', 'OP': '?'}, {'SHAPE': 'ddd'}, {'ORTH': '-', 'OP': '?'}, {'SHAPE': 'dddd'}]
    pattern2 = [{"ORTH": {"REGEX": "^\+?[1-9][0-9]{7,14}$"}}]
    pattern3 = [{"ORTH": "+1", 'OP': '?'}, {'SHAPE': 'ddd'}, {'ORTH': '-', 'OP': '?'}, {'SHAPE': 'ddd'},
                {'ORTH': '-', 'OP': '?'}, {'SHAPE': 'dddd'}]
    #     pattern4 = [{'ORTH':{"REGEX":"^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$"}}]
    pattern5 = [{"ORTH": "+1"}, {"ORTH": "(", "OP": "?"}, {"SHAPE": "ddd"},
                {"ORTH": ")", "OP": "?"}, {'SHAPE': 'ddd'}, {'ORTH': '-', 'OP': '?'}, {"SHAPE": "dddd"}]
    pattern6 = [{"ORTH": "+1", 'OP': '?'}, {"ORTH": "(", "OP": "?"}, {"SHAPE": "ddd"},
                {"ORTH": ")", "OP": "?"}, {'POS': 'NUM'}]

    ph = []
    count = []
    for i in [pattern5, pattern3, pattern2, pattern1, pattern6]:
        matcher.add("PhoneNumber", [i])

        matches = matcher(doc)

        for match_id, start, end in matches:
            ph.append(doc[start:end].text)
    for num in ph:
        if num in data:
            data = data.replace(num, u"\u2588" * len(num))
            count.append(num)

    return data, count

# Names
def names_(data):
    
    matcher = Matcher(nlp.vocab)
    pattern = [{'POS':'PROPN'},{'ORTH':',','OP':'?'},{'POS':'PROPN','OP':'?'}]
    matcher.add('name',[pattern])
    doc=nlp(data)
    matches = matcher(doc)
    l2=[]
    count=[]
    for match_id, start, end in matches:
        span = doc[start:end]
         
        name=span.text.replace(',',' ')
        
        name=nlp(name)
        
        for i in name.ents:
            
            if i.label_ == 'PERSON':
                l2.append(i.text)
                
    redact_doc= data
    
    for word in l2:
        
        w=word.replace(" ",',')
        redact_doc= redact_doc.replace(w,u"\u2588" * len(word))
        w1=w.replace(",",' ')
        redact_doc= redact_doc.replace(w1,u"\u2588" * len(word))
        
        
    
    return redact_doc,set(l2)


# Dates
def Dates(data):
    doc = nlp(data)
    matcher = Matcher(nlp.vocab)
    pattern1 = [{'POS': 'NUM'}, {'ORTH': '-'}, {'POS': 'NUM'}, {'ORTH': '-'}, {'POS': 'NUM'}]
    pattern2 = [{'TEXT': {'REGEX': r'^\d{1,2}/\d{1,2}/\d{2}(?:\d{2})?$'}}]

    d = []
    count = []
    for i in [pattern2, pattern1]:
        matcher.add("Dates", [i])
        matches = matcher(doc)
        for match_id, start, end in matches:
            d.append(doc[start:end].text)
    for i in doc.ents:
        if i.label_ == "DATE":
            d.append(i.text)
    for num in d:
        if num in data:
            data = data.replace(num, u"\u2588" * len(num))
            count.append(num)

    return data, count


# Genders
def genders(data):
    gen = ['he', 'she', 'her', 'his', 'mr.', 'miss.',
           'mr', 'miss', 'men', 'women', 'man', 'woman', 'guy', 'ladies', 'gent',
           'they', 'himself', 'herself', 'father', 'mother', 'girl', 'boy', 'daughter',
           'son', 'male', 'female', 'wife', 'wives', 'husband', 'grandma', 'grandpa', 'grandmother',
           'grandfather', 'aunt', 'uncle', 'nephew', 'niece', 'madam', 'mister', 'mom', 'dad', 'hero', 'herione',
           'brother', 'sister', 'girlfriend', 'boyfriend', 'groom', 'bride', 'prince', 'princess', 'mummy', 'king',
           'queen',
           'lady', 'actress', 'fiance', 'gentleman', 'gentlemen', 'widow', 'spokeswoman', 'chairwoman', 'goddess',
           'priestess', 'priest',
           'empress', 'emperor']
    doc = nlp(data)
    g_count = []
    for word in doc:
        x = word.text
        if x.lower() in gen:
            g_count.append(x)
            data = data.replace(x, u"\u2588" * len(x))
        elif x[:-1].lower() in gen:
            g_count.append(x)
            data = data.replace(x, u"\u2588" * len(x))

    return data, g_count


# Adresses
def address(data):
    doc = nlp(data)
    l4 = []
    count = []
    ad_matcher = Matcher(nlp.vocab)
    pattern1 = [{'SHAPE': 'dddd'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}, {'SHAPE': '\n', 'OP': '?'}, {'POS': 'PROPN'},
                {'POS': 'PROPN'}, {'SHAPE': 'dddd'}]
    pattern2 = [{'SHAPE': 'dddd'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}]
    pattern3=[{'SHAPE': 'dddd'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'},{'POS': 'PUNCT','OP':'?'},
              {'POS': 'PROPN'}]

    for i in [pattern1, pattern2,pattern3]:
        ad_matcher.add('Address', [i])
        matches = ad_matcher(doc)

        for match_id, start, end in matches:
            span = doc[start:end]
            l4.append(span.text)
    for i in doc.ents:
        if i.label_ == "GPE":
            l4.append(i.text)
    for w in l4:
        if w in data:
            data = data.replace(w, u"\u2588" * len(w))
            count.append(w)

    return data, count


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
        error = 'file'+str(n)+': \n'
        for i in range(0, len(txt)):
            error += str(txt[i]) + '\n'
        # for i in range(0, len(l)):
        #     if l[i] == 0:
        #         err = 'There are no ' + redacted_list[i] + ' to be redacted from the file.'
        #         error.append(err)
        filepath=('./stats/%s'%(file))
        with open(filepath,'a+') as f:
            for e in error:
                f.write(e)
    else:
        txt_store = 'Stats of file'+str(n)+': \n'
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

        filepath = ('./stats/%s'%(file))
        with FileManager(filepath, 'a+') as file:
            file.write(txt_store+'\n')


# Output stored in a text file.
def output(data, file, path):
    filepath = os.path.join(os.getcwd(), path)
    try:
        os.makedirs(filepath, exist_ok=True)
        fpath = ('%s.redacted' % (file))
        with open(os.path.join(filepath, fpath), 'w+', encoding='utf-8') as f:
            f.write(data)
            f.close()
    except OSError as error:
        print(error)
