import pytest
from project1 import project1 as p1

def test_names():
    data = "John father's name is Edward."
    red, li = p1.names_(data)
    assert len(li) is not None
    

def test_dates():
    data = "Marie date of birth is 29/11/1994. Today is 26 Mar 2021."
    red, li = p1.Dates(data)
    assert len(li)==3
    
    
def test_genders():
    data = ''' She should start talking 
    before long. Her age kids are already talking.  I'm sure you are teaching our girl to 
    say her first words. '''
    red, li = p1.genders(data)
    assert len(li)==4
    
def test_phone():
    data = 'My mobile number is (713) 853-1575 and my office number is (405) 346-4567.'
    red, li = p1.extract_phone_number(data)
    assert len(li)==2
    assert red=='My mobile number is ██████████████ and my office number is ██████████████.'
    
def test_address():
    data = '1400 Smith Street Houston Texas 77002'
    red, li = p1.address(data)
    assert len(li)==1
    
def test_concept():
    char=u"\u2588"
    data = 'Television has become an integral part of our daily lives. It has the power to influence our lives in many ways.'
    red, li = p1.concept(data,'television')
    assert len(li)==1
    assert char in red


