# The Redactor

### RACHANA VELLAMPALLI

 Whenever sensitive information is shared with the public, the data must go through a redaction process. That is, all sensitive names, places, and other sensitive information must be hidden. Documents such as police reports, court transcripts, and hospital records all contain sensitive information. Redacting this information is often expensive and time consuming.In this Project1, trying to redact this sensitive information from the .txt files.

## Packages Required

### Installing and Importing Packages

```bash
pipenv install nltk
pipenv install spacy
pipenv install commonregex
nltk.download('wordnet')
nltk.download('punkt')
!python -m spacy download en_core_web_sm
import glob
import nltk
import spacy
import sys
from spacy.matcher import Matcher
from commonregex import CommonRegex
from nltk.tokenize import word_tokenize,sent_tokenize
from nltk.corpus import wordnet as wn
```
# Project1/project1.py
The project1.py file contains functions to redact information like names, genders, dates, phone number and address from the given text files. And also input and output functions to read the data and store it in a new file in the given path.

The data redacted from the functions is done by replacing detected data with Unicode full block character █ (U+2588).

1. **names_(data)**

  This function takes the data and detects the names and redact it with replacing the names with Unicode full block character █ (U+2588). In this function, names are detected using Matcher from Spacy. This function returns the redacted names data and the list of names redacted.
  ```bash
   pattern = [{'POS': 'PROPN'},{'ORTH':',','OP':'?'} ,{'POS': 'PROPN', 'OP': '?'}]
  ```
  Assumed the Names are in this format {Firstname, LastName}, {FirstName LastName},{FirstName}.
  #### Bugs
  If the name is in the format {LastName, FirstName} it will only redact FirstName. And if the name is nickname (ex: Ted) it won't redact.

2. **extract_phone_number(data)**
   
  This function takes in the data and detects the phone numbers which are in the **format {(405)-536-7891} or {(405) 536  7891} or {405-536-7891} or {405 536 7891}**.
 ```bash
 pattern = [{'ORTH': '(','OP':'?'}, {'SHAPE': 'ddd'}, {'ORTH': ')','OP':'?'},
               {'ORTH': '-', 'OP': '?'}, {'SHAPE': 'ddd'}, {'ORTH': '-', 'OP': '?'}, {'SHAPE': 'dddd'}]
 ```
 It returns the redacted phones data and the list of phone numbers redacted.
 
3. **Dates(data)**

 This function takes in the data and returns the redacted Dates data and the list of redacted dates. The dates in the following format will be redacted: {'29/11/1994', '26 Mar 2021', 'Nov 29', '29/11/94', '29-11-1994' ,'29-11-94', 'April 9th'}.
 ```bash
  date = CommonRegex(data)
  for dat in date.dates:
        d_count.append(dat)
        data = data.replace(dat, u"\u2588" * len(dat))
 ```
 Here commonregex package is used to find dates. It can also be used to find phone numbers, emails, links etc.
   #### Bugs:
   If the date is in the format of 26 March 2021 it will redact like this: ██ ███ch ████.
 
4. **genders(data)**

 This function takes in the data and returns redacted genders data and list of genders redacted. The genders which can be redacted is in the below list.Even if the data is upper case (x.lower()) data is redacted.
 ```bash
 gen = ['he', 'she', 'her', 'his', 'mr.', 'miss.',
           'mr', 'miss', 'men', 'women', 'man', 'woman',
           'they', 'himself', 'herself', 'father', 'mother', 'girl', 'boy']
           
 ```
5. **address(data)**

 This function returns redacted address data and the list of addresses redacted. Considering the text files data, Assumed the address are in the format of {'1400 Smith Street\nHouston Texas 77002', '1400 Smith Street Houston Texas 77002'}.
 ```bash
 pattern = [{'SHAPE': 'dddd'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}, {'SHAPE': '\n','OP':'?'}, {'POS': 'PROPN'},
               {'POS': 'PROPN'}, {'SHAPE': 'dddd'}]
 ```
   #### Bugs
    It won't redact if given only street or location. ex: '1400 Smith Street' or 'Houston'.
    
6. **concept(data, concept)**

 This function takes in the data and the concept. Here, The concept taken is 'insurance'. Whenever the concept word or similar word is detected the sentence related to the word should be redacted.
 Here, the similar words for insurance are 'insurance', 'policy', 'insurance_policy', 'indemnity'.
 Nltk package is used to built the concept function. Returns the redacted concept data and list of sentences redacted.
 
7. **stats(data, c, file,n)**

 This function takes either the name of the file or special files (stdout,stderr) and writes the summary of the redaction process.
 If the file is stdout then it prints the stats of the redact process in the console. The stats included are number of names, dates, phone numbers, genders, address and concept redacted and total number of redacted in each file.
 ```bash
 if file == 'stdout':
        for t in txt:
            print(t)
 ```
 If the file is stderr then it checks if the data does not contain any list of flags mentioned above and then it stores the result in the given file.
 ```bash
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
 ```
 If the text file doesnot have any names or genders flags then the stored file will be in this format:
 ```bash
 There are no Names to be redacted from the file.
There are no Gender to be redacted from the file.
```
If stats takes any name of the file then the stats of the redacted process is stored in the name of that file at given location.
The output is similar to like this:
```bash
file0
The number of Names redacted from the file: 9
The number of Phone Number redacted from the file: 0
The number of Dates redacted from the file: 1
The number of Gender redacted from the file: 17
The number of Address redacted from the file: 0
The number of Concept redacted from the file: 0
Total number of redactions in the file is :27
```
Refer this folder [stats](https://github.com/Rachana137/cs5293sp22-project1/tree/main/stats) to know the redact process of  texts file taken.

8. **input(input_file)**

 This function takes the path of the text file and returns the data in that file.
 
9. **output(data, file, path)**

 This function takes the redacted data, file name and the location where the file need be stored.
 ```bash
 filepath = ('./files/ redacted_%s' % ( file))
    with open(filepath, 'w+', encoding='utf-8') as f:
        f.write(data)
        f.close()
 ```
 To refer the redacted files, go this folder [files](https://github.com/Rachana137/cs5293sp22-project1/tree/main/files)
 ## redactor.py

In this file, the main is written. All the functions saved in project1.py are imported. Next, Multiple arguments are passed from the command line in to related lists conditions.
To take each file path from the input an argument parser with type=glob.glob is created.
```bash
 parser.add_argument("--input", type=glob.glob, required=True, help="Source File location", nargs='*',
                        action='store')
```
Next, Each file is taken from the input paths and redact the data from the file. Each function to redact the data is called as per the given flags and concept.The redacted data is written into .redacted file as per given output path.

The program is runned by the following command.
```bash
pipenv run python redactor.py --input '*.txt' \
                    --names --dates --phones --genders --address\
                    --concept 'insurance' \
                    --output 'files/' \
                    --stats stderr
                    
```
If the file name is given for stats then:
```bash
pipenv run python redactor.py --input '*.txt' \
                    --names --dates --phones --genders --address\
                    --concept 'insurance' \
                    --output 'files/' \
                    --stats <filename>
```
## tests/test_all.py
This test_all.py contains the test cases to test functions in project1.py. The test functions are created for names,dates,genders, phone number, address and concept flags.
>  Test functions are created in such a way that the length of list of flag is same as number of flag values in data then the test is passed.
Example for names_() the test case code is:
```bash
def test_names():
    data = "John father's name is Edward."
    red, li = p1.names_(data)
    assert len(li)==2
    assert red == "████ father's name is ██████."
```
To test the testcases run:
```bash
pipenv run pytest
```
This will fetch results from test_all.py and return if the tests passed or not.
## References
https://towardsdatascience.com/how-to-extract-structured-information-from-a-text-through-python-spacy-749b311161e
https://github.com/madisonmay/CommonRegex
