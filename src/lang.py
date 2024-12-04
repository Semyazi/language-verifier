import random
random.seed(313)

import config
from tqdm import tqdm

# Common language functionality
class BaseLanguage:
    name="Base Language"
    lang_type="Base"
    def __init__(self):
        self.sample_strings=set()
    def has(self,s):
        return s in self.sample_strings
    def gen(self):
        # Populate self.sample_strings
        # Either override this *or* the has method
        # TODO: Try to figure out how to use the logging module lol, seems like a good use for it idk
        print(f"Generating strings for {self.name}")
        for t in tqdm(range(config.LANG_TC)):
            sat=False
            while not sat:
                s=self.rand_gen()
                sat=self.has(s)
            self.sample_strings.add(s)
    @property            
    def is_gen(self):
        return len(self.sample_strings)>0
    def rand_gen(self):
        # TODO: Try to find a way to generate all strings in the language of length 0,1,2,... so we don't waste time.
        length=random.randint(0,config.THRESHOLD)
        return ''.join(random.choice(config.ALPHA) for _ in range(length))

# Language comparisons
def comp(l1,l2):
    if not l1.is_gen:l1.gen()
    if not l2.is_gen:l2.gen()

    print(f"Comparing: {l1.name} and {l2.name}")

    l1_errors=[]
    l2_errors=[]

    for s in l1.sample_strings:
        if len(s)>config.THRESHOLD:continue
        if not l2.has(s):l1_errors.append(s)
    
    for s in l2.sample_strings:
        if len(s)>config.THRESHOLD:continue
        if not l1.has(s):l2_errors.append(s)
    
    if len(l1_errors):
        print(f"Error: {l1.lang_type} language had {len(l1_errors)} strings not in the {l2.lang_type} language.")
        print("Some examples are:",l1_errors[:10])
    
    if len(l2_errors):
        print(f"Error: {l2.lang_type} language had {len(l2_errors)} strings not in the {l1.lang_type} language.")
        print("Some examples are:",l2_errors[:10])
    
    if len(l1_errors)+len(l2_errors)==0:
        print("The languages match!")