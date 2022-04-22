# CHANGES

## Output files not stored in respective folder

For this I added a code so that it can store in the given input folder.
```bash
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
```
Here, os.makedirs() helps us to create the given folder. 

## File names not re-assigned correctly

Before changes, my files stored as "redacted_file3.txt". So I made small changes in my code.
```bash
  fpath = ('%s.redacted' % (file))
```
This line of code helps in storing the redacted file in "<file>.redacted" form. (ex. file1.txt.redacted).

  
## Missing Stats 
  
Instead of "w+" I wrote "a+" so it writes in the same file.
  
 For stderr:
```bash
    filepath=('./stats/%s'%(file))
        with open(filepath,'a+') as f:
            for e in error:
                f.write(e)
```
  For any given file name:
```bash
  filepath = ('./stats/%s'%(file))
        with FileManager(filepath, 'a+') as file:
            file.write(txt_store+'\n')
```
  The stats file created will be stored in stats folder.
  
 ## Missing/No Features - Addresses
  I added few more patterns for addresses. So, it can redact it.
  ```bash
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
  ```
  This code will redact the address which are in the format of {"1400 Smith Street\nHouston Texas 77002","1400 Smith Street, Houston Texas ","1400 Smith Street","Houston"}
  
## Missing/No Features Found - Dates
  ```bash
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
```
  I included patterns for dates and used the label_ to detect the dates. It redacts the dates in the format of {04/05/22,04-05-2022,Today, April 9th, 03 January 2022}.
  Here, Today, Tommorow is also indirectly telling the date. So, it will be redacted.
  
## Missing/No Features Found- Phone Number
  I added few more patterns for the phone numbers.
  ```bash
    pattern1 = [{'ORTH': '('}, {'SHAPE': 'ddd'}, {'ORTH': ')'},
                {'ORTH': '-', 'OP': '?'}, {'SHAPE': 'ddd'}, {'ORTH': '-', 'OP': '?'}, {'SHAPE': 'dddd'}]
    pattern2 = [{"ORTH": {"REGEX": "^\+?[1-9][0-9]{7,14}$"}}]
    pattern3 = [{"ORTH": "+1", 'OP': '?'}, {'SHAPE': 'ddd'}, {'ORTH': '-', 'OP': '?'}, {'SHAPE': 'ddd'},
                {'ORTH': '-', 'OP': '?'}, {'SHAPE': 'dddd'}]
    
    pattern5 = [{"ORTH": "+1"}, {"ORTH": "(", "OP": "?"}, {"SHAPE": "ddd"},
                {"ORTH": ")", "OP": "?"}, {'SHAPE': 'ddd'}, {'ORTH': '-', 'OP': '?'}, {"SHAPE": "dddd"}]
    pattern6 = [{"ORTH": "+1", 'OP': '?'}, {"ORTH": "(", "OP": "?"}, {"SHAPE": "ddd"},
                {"ORTH": ")", "OP": "?"}, {'POS': 'NUM'}]
 ```

Now, it redacts the international numbers. Example formats of numbers can be redacted: {'+1 (450) 243-3426', '+917138531575', '(405) 346 4567','405 346 4567','405-346-4567','+1 450 2433426'}.
  
## Missing/No Features Found - Gender
  In this function, I extended the list of genders.
  ```bash
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
```
  
  I also write a code for the plurals. Example: if the given gender is girls,womens then it will be redacted.
  ```bash
      elif x[:-1].lower() in gen:
                g_count.append(x)
                data = data.replace(x, u"\u2588" * len(x))
  ```
  
  
