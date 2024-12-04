import config
import re
import lang

# Regex tools
"""
Only supports:
{0,1} - your alphabet
* - kleene star
E - empty set symbol ∅
e - ǫ epsilon
+
"""

# special characters
SPEC=('*','E','e','(',')','|','+') # these cannot be in the alphabet

for char in config.ALPHA:
    assert char not in SPEC

def comp_regex(r):
    # ignore whitespace
    r=''.join(r.split())

    # ensure everything in the regex is either a symbol in the alphabet or a special character
    # otherwise we can run into problematic behaviour with the regex module
    for c in r:
        assert c in config.ALPHA or c in SPEC
    
    # we use + for |
    r=r.replace('+','|')
    r=r.replace('e','(){1,1}') # epsilon
    r=r.replace('E','(^0$)') # empty set, it's impossible to match the end of the string, then 0, then the start of the string, so the language of this is the emptyset
    
    return re.compile(r)

class RegexLanguage(lang.BaseLanguage):
    def __init__(self,r,name=None):
        super().__init__()

        self.regex=comp_regex(r)
        if name:
            self.name=name
        else:
            self.name=f"Regex:{r}"
        
        self.lang_type="Regex"
    def has(self,s):
        return self.regex.fullmatch(s)!=None

if __name__=='__main__':
    l=RegexLanguage('1(0+E)*1*00')
    l.gen()