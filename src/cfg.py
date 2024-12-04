import random
random.seed(313)

import config
import lang
from tqdm import tqdm

class Var:
    def __init__(self,name):
        self.name=name
    def __repr__(self):
        return f'<{self.name}>'

def gvar(*args):
    return [Var(x) for x in args]

class CFG:
    def __init__(self,sv,prod):
        self.sv=sv # starting variable
        self.prod=prod # var to prods associated with the var
    
    def apply_prod(self,partial,idx,prod):
        # TODO: add compression so that when two strings are next to each other they get combined, only needs to be done around idx
        x=partial[:idx]+prod+partial[idx+1:]
        return x
    
    def get_var_indices(self,partial):
        for i,x in enumerate(partial):
            if type(x)==Var:yield i
    
    def randomly_apply_prod(self,partial):
        ind=list(self.get_var_indices(partial))
        if len(ind)==0:return ''.join(partial),True # we're done, there are no more vars
        idx=random.choice(ind)
        v=partial[idx]
        prod=random.choice(self.prod[v])
        x=self.apply_prod(partial,idx,prod)
        return x,False # we're done, we applied a production to a var

    def generate_strs(self,tc=config.CFG_TC,depth=config.CFG_DEPTH):
        strs=set()

        for t in tqdm(range(tc)):
            part=(self.sv,)
            for i in range(depth):
                part,done=self.randomly_apply_prod(part)
                if done:
                    strs.add(part)
                    break
        return strs

class CFGLanguage(lang.BaseLanguage):
    def __init__(self,cfg,name=None):
        super().__init__()
        if name:
            self.name=name
        else:
            self.name="CFG"
        
        self.lang_type="CFG"

        if type(cfg)==CFG:
            self.cfg=cfg
            return

        # parse the cfg syntax:::
        # language rules:
        """
        RULES:
        each line has two parts, S is always the starting variable, we need S always.
        we ignore all whitespace in each line.
        variables consisting of more than one character must be enclosed in <> UNLESS they are at the start of the line (so, only for productions),
        they please dont enclose them in <>.
        productions in each line are separated by commas
        also, e is the empty character

        for ex:
        S>X,Y
        X>0X,1X,00A
        A>0A,1A,11B
        B>0B,1B,e
        Y>0Y,1Y,11C
        C>0C,1C,00B
        """

        vs={}
        prods={}

        assert type(cfg)==str
        for line in cfg.split("\n"):
            if '>' not in line:continue
            line=''.join(line.split()) # no whitespace

            var,prod=line.split('>')
            assert var not in config.ALPHA

            if var not in vs:vs[var]=Var(var)
            var=vs[var]

            for prod in prod.split(','):
                p=[]
                reading_var=False
                buf=''
                while len(prod)>0:
                    char=prod[0]
                    prod=prod[1:]

                    buf+=char

                    if char=='[':
                        reading_var=True
                        continue

                    if char==']':
                        reading_var=False
                        
                        v=buf[1:-1]
                        buf=''
                        if v not in vs:vs[v]=Var(v)
                        v=vs[v]

                        p.append(v)
                        continue
                    
                    if reading_var:continue

                    # otherwise, the buf is just the current character
                    # please NOBODY EVER use e as a variable :(
                    if buf=='e':
                        buf=''
                    if buf!='' and buf not in config.ALPHA:
                        # it must be a variable
                        if buf not in vs:vs[buf]=Var(buf)
                        buf=vs[buf]
                    p.append(buf)
                    
                    buf=''

                if var not in prods:prods[var]=[]
                prods[var].append(tuple(p))
        
        assert 'S' in vs # need a starting var...
        self.cfg=CFG(vs['S'],prods)
    
    def gen(self):
        print(f"Generating strings for {self.name}")
        self.sample_strings=self.cfg.generate_strs()

if __name__ == '__main__':
    cfg=CFGLanguage("""
    S>X,Y
    X>0X,1X,00A
    A>0A,1A,11B
    B>0B,1B,e
    Y>0Y,1Y,11[C00]
    C00>0[C00],1[C00],00B
    """)
    cfg.gen()
    print(list(cfg.sample_strings)[:10])