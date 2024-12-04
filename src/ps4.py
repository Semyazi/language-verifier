import random
random.seed(313)

import config
import utils
import lang
from cfg import gvar,CFG,CFGLanguage
from tqdm import tqdm

""" Problem Set 4 Languages """
class L1e(lang.BaseLanguage):
    name="L1e"
    def has(self,x):
        return utils.is_pal(x)

class L1d(lang.BaseLanguage):
    name="L1d"
    def gen(self):
        for t in tqdm(range(config.LANG_TC)):
            l=random.randint(0,config.THRESHOLD)
            y=utils.rstr(l)
            if random.randint(0,1):
                x=y+utils.twice(y)[::-1]
            else:
                x=utils.twice(y)[::-1]+y
            self.sample_strings.add(x)

class L1t(lang.BaseLanguage):
    name="L1t"
    def gen(self):
        for t in tqdm(range(config.LANG_TC)):
            success=False
            while not success:
                l1=random.randint(0,config.THRESHOLD)
                l2=random.randint(0,config.THRESHOLD)
                y=utils.rstr(l1)
                z=utils.rstr(l2)
                success=utils.is_pal(y+utils.toggle(z))
            self.sample_strings.add(y+z)

class L2e(lang.BaseLanguage):
    name="L2e"
    a00=utils.PrefixAutomaton('00')
    a011=utils.PrefixAutomaton('011')
    def has(self,x):
        return self.a00.occur(x)==self.a011.occur(x)

class L2d(lang.BaseLanguage):
    name="L2d"
    a00=utils.PrefixAutomaton('00')
    a011=utils.PrefixAutomaton('011')
    def has(self,x):
        o00=self.a00.occur(x)
        o011=self.a011.occur(x)
        return o00==(2*o011) or (2*o00)==o011

class L2a(lang.BaseLanguage):
    name="L2a"
    a00=utils.PrefixAutomaton('00')
    a011=utils.PrefixAutomaton('011')
    def has(self,x):
        o00=self.a00.occur(x)
        o011=self.a011.occur(x)
        return abs(o00-o011)==1

class L3:
    def create(p,q,r,s):
        return p*'0' + q*'1' + r*'0' + s*'1'

class L3a(lang.BaseLanguage):
    name="L3a"
    def gen(self):
        for t in tqdm(range(config.LANG_TC)):
            success=False
            while not success:
                p,q,r,s=[random.randint(0,config.THRESHOLD) for _ in range(4)]
                success=((p+q)==(r+s))
            self.sample_strings.add(L3.create(p,q,r,s))

class L3b(lang.BaseLanguage):
    name="L3b"
    def gen(self):
        for t in tqdm(range(config.LANG_TC)):
            success=False
            while not success:
                p,q,r,s=[random.randint(0,config.THRESHOLD) for _ in range(4)]
                success=((p+r)==(q+s))
            self.sample_strings.add(L3.create(p,q,r,s))

class L3c(lang.BaseLanguage):
    name="L3c"
    def gen(self):        
        for t in tqdm(range(config.LANG_TC)):
            success=False
            while not success:
                p,q,r,s=[random.randint(0,config.THRESHOLD) for _ in range(4)]
                success=((p+s)==(q+r))
            self.sample_strings.add(L3.create(p,q,r,s))

""" Problem Set 4 CFGs """
# Warning: Not guaranteed to be optimal in any way!

def L1e_cfg():
    return CFGLanguage("""
    S>0S0,1S1,1,0,e
    """)

def L1d_cfg():
    return CFGLanguage("""
    S>A,B
    A>e,0A00,1A11
    B>e,00B0,11B1
    """)

def L1t_cfg():
    return CFGLanguage("""
    S>0S1,1S0,P
    P>e,0,1,0P0,1P1
    """)

def L2e_cfg():
    return CFGLanguage("""
    S>e,[A00],[A01],[A10],[A11]
    A00>0,0[A00]1[A10],01[A00],01[A10][A00]
    A01>0[A00]1[A11],01,01[A01],01[A10][A01]
    A10>1[A00],1[A10]
    A11>1[A01],1[A11],1
    """)

def L2d_cfg():    
    S,A,B,A00,A01,A10,A11,B00,B01,B10,B11=gvar('S','A','B','A00','A01','A10','A11','B00','B01','B10','B11')
    prod={
        S:[(A,),(B,)],
        A:[('',),(A00,),(A01,),(A10,),(A11,)],
        A00:[('0',),('0',A00,A00,'1',A10),('0',A00,'1',A10,A00),('0','1',A00),('0','1',A10,A00,A00)],
        A01:[('0',A00,A00,'1',A11),('0',A00,'1',A10,A01),('0','1'),('0','1',A01),('0','1',A10,A00,A01)],
        A10:[('1',A00),('1',A10)],
        A11:[('1',),('1',A01),('1',A11)],
        B:[('',),(B00,),(B01,),(B10,),(B11,)],
        B00:[('0',),('0',B00,'1',B10,'1',B10),('0','1',B00),('0','1',B10,B00,'1',B10),('0','1',B10,'1',B10,B00)],
        B01:[('0',B00,'1',B10,'1',B11),('0','1'),('0','1',B01),('0','1',B10,'1',B10,B01),('0','1',B10,B00,'1',B11)],
        B10:[('1',B00),('1',B10)],
        B11:[('1',),('1',B01),('1',B11)]
    }
    return CFGLanguage(CFG(S,prod))

def L2a_cfg():
    S,A00,A01,A10,A11=gvar('S','A00','A01','A10','A11')
    prod={
        S:[('0',A00),('0',A01),(A00,A00),(A00,A01),(A10,A00),(A10,A01),(A00,'0'),(A10,'0'),
            ('0','1',A10),('0','1',A11),(A00,'1',A10),(A00,'1',A11),(A10,'1',A10),(A10,'1',A11),(A00,'1','1'),(A10,'1','1')],
        A00:[('0',),('0',A00,'1',A10),('0','1',A00),('0','1',A10,A00)],
        A01:[('0',A00,'1',A11),('0','1'),('0','1',A01),('0','1',A10,A01)],
        A10:[('1',A00),('1',A10)],
        A11:[('1',A01),('1',A11),('1',)]
    }
    return CFGLanguage(CFG(S,prod))


def L3a_cfg():
    S,A00,A01,A10,A11=gvar('S','A00','A01','A10','A11')
    prod={
        S:[('',),(A00,),(A01,),(A10,),(A11,)],
        A00:[('00',),('0',A00,'0'),('0',A10,'0')],
        A01:[('01',),('0',A00,'1'),('0',A01,'1'),('0',A10,'1'),('0',A11,'1')],
        A10:[('10',),('1',A10,'0')],
        A11:[('11',),('1',A10,'1'),('1',A11,'1')]
    }
    return CFGLanguage(CFG(S,prod))

def L3b_cfg():
    return CFGLanguage("""
    A>e,0A1
    B>e,1B0
    S>C,ABA
    C>0C1,AA
    """)

def L3c_cfg():
   return CFGLanguage("""
   A>e,0A1
   B>A,0B0
   C>A,1C1
   S>BA,AC
   """)

if __name__ == '__main__':
    import time
    start=time.time()
    # Question 1
    print("Verifying L1e: Exact")
    lang.comp(L1e(),L1e_cfg())

    print("Verifying L1d: Double")
    lang.comp(L1d(),L1d_cfg())

    print("Verifying L1t: Toggle")
    lang.comp(L1t(),L1t_cfg())

    # Question 2
    print("Verifying L2e: Exact")
    lang.comp(L2e(),L2e_cfg())

    print("Verifying L2d: Double")
    lang.comp(L2d(),L2d_cfg())

    print("Verifying L2a: Almost")
    lang.comp(L2a(),L2a_cfg())

    # Question 3
    print("Verifying L3a")
    lang.comp(L3a(),L3a_cfg())

    print("Verifying L3b")
    lang.comp(L3b(),L3b_cfg())

    print("Verifying L3c")
    lang.comp(L3c(),L3c_cfg())
    print(time.time()-start)