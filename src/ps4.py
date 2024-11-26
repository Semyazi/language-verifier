import random
random.seed(313)

import utils
from config import *
from cfg import verify_cfg,gvar,CFG,Var,rstr
from tqdm import tqdm

""" Problem Set 4 Languages """
class L1e:
    def has(x):
        return x==x[::-1]
    def gen():
        s=set()
        for t in tqdm(range(LANG_TC)):
            l=random.randint(0,THRESHOLD)
            x=rstr(l)
            s.add(x+random.choice(ALPHA+('',))+x[::-1])
        return s

def twice(s):
    x=''
    for c in s:
        x+=2*c
    return x

class L1d:
    def gen():
        s=set()
        for t in tqdm(range(LANG_TC)):
            l=random.randint(0,THRESHOLD)
            y=rstr(l)
            if random.randint(0,1):
                x=y+twice(y)[::-1]
            else:
                x=twice(y)[::-1]+y
            s.add(x)
        return s

def toggle(s):
    x=''
    for c in s:
        x+=str(1-int(c))
    return x

def is_pal(s):
    return s==s[::-1]

class L1t:
    def gen():
        s=set()
        for t in tqdm(range(LANG_TC)):
            success=False
            while not success:
                l1=random.randint(0,THRESHOLD)
                l2=random.randint(0,THRESHOLD)
                y=rstr(l1)
                z=rstr(l2)
                success=is_pal(y+toggle(z))
            s.add(y+z)
        return s

class L2e:
    def gen():
        s=set()
        for t in tqdm(range(LANG_TC)):
            success=False
            while not success:
                x=rstr(random.randint(0,THRESHOLD))
                success=utils.occur('00',x)==utils.occur('011',x)
            s.add(x)
        return s

class L2d:
    def gen():
        s=set()
        for t in tqdm(range(LANG_TC)):
            success=False
            while not success:
                x=rstr(random.randint(0,THRESHOLD))
                o00=utils.occur('00',x)
                o011=utils.occur('011',x)
                success=o00==(2*o011) or (2*o00)==o011
            s.add(x)
        return s

class L2a:
    def gen():
        s=set()
        for t in tqdm(range(LANG_TC)):
            success=False
            while not success:
                x=rstr(random.randint(0,THRESHOLD))
                o00=utils.occur('00',x)
                o011=utils.occur('011',x)
                success=abs(o00-o011)==1
            s.add(x)
        return s

class L3:
    def create(p,q,r,s):
        return p*'0' + q*'1' + r*'0' + s*'1'

class L3a:
    def gen():
        for t in tqdm(range(LANG_TC)):
            success=False
            while not success:
                p,q,r,s=[random.randint(0,THRESHOLD) for _ in range(4)]
                success=((p+q)==(r+s))
            yield L3.create(p,q,r,s)

class L3b:
    def gen():
        for t in tqdm(range(LANG_TC)):
            success=False
            while not success:
                p,q,r,s=[random.randint(0,THRESHOLD) for _ in range(4)]
                success=((p+r)==(q+s))
            yield L3.create(p,q,r,s)

class L3c:
    def gen():        
        for t in tqdm(range(LANG_TC)):
            success=False
            while not success:
                p,q,r,s=[random.randint(0,THRESHOLD) for _ in range(4)]
                success=((p+s)==(q+r))
            yield L3.create(p,q,r,s)

""" Problem Set 4 CFGs """
# Warning: Not guaranteed to be optimal in any way!

def L1e_cfg():
    S=Var('S')
    p={}
    p[S]=[
        ('0',S,'0'),
        ('1',S,'1'),
        ('1',),
        ('0',),
        ('',)
    ]
    return CFG(S,p)

def L1d_cfg():
    S,A,B=gvar('S','A','B')
    prod={
        S:[(A,),(B,)],
        A:[('',),('0',A,'0','0'),('1',A,'1','1')],
        B:[('',),('0','0',B,'0'),('1','1',B,'1')]
    }
    return CFG(S,prod)

def L1t_cfg():
    S,P=gvar('S','P')
    prod={
        S:[('0',S,'1'),('1',S,'0'),(P,)],
        P:[('',),('0',),('1',),('0',P,'0'),('1',P,'1')]
    }
    return CFG(S,prod)

def L2e_cfg():
    S,A00,A01,A10,A11=gvar('S','A00','A01','A10','A11')
    prod={
        S:[('',),(A00,),(A01,),(A10,),(A11,)],
        A00:[('0',),('0',A00,'1',A10),('0','1',A00),('0','1',A10,A00)],
        A01:[('0',A00,'1',A11),('0','1'),('0','1',A01),('0','1',A10,A01)],
        A10:[('1',A00),('1',A10)],
        A11:[('1',A01),('1',A11),('1',)]
    }
    return CFG(S,prod)

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
    return CFG(S,prod)

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
    return CFG(S,prod)


def L3a_cfg():
    S,A00,A01,A10,A11=gvar('S','A00','A01','A10','A11')
    prod={
        S:[('',),(A00,),(A01,),(A10,),(A11,)],
        A00:[('00',),('0',A00,'0'),('0',A10,'0')],
        A01:[('01',),('0',A00,'1'),('0',A01,'1'),('0',A10,'1'),('0',A11,'1')],
        A10:[('10',),('1',A10,'0')],
        A11:[('11',),('1',A10,'1'),('1',A11,'1')]
    }
    return CFG(S,prod)

def L3b_cfg():
    A,B,C,S=gvar('A','B','C','S')
    prod={
        A:[('',),('0',A,'1')],
        B:[('',),('1',B,'0')],
        S:[(C,),(A,B,A)],
        C:[('0',C,'1',),(A,A)]
    }
    return CFG(S,prod)

def L3c_cfg():
   A,B,C,S=gvar('A','B','C','S')
   prod={
    A:[('',),('0',A,'1')],
    B:[(A,),('0',B,'0')],
    C:[(A,),('1',C,'1')],
    S:[(B,A),(A,C)]
   }
   return CFG(S,prod)

if __name__ == '__main__':
    # Question 1
    print("Verifying L1e: Exact")
    verify_cfg(L1e,L1e_cfg())

    print("Verifying L1d: Double")
    verify_cfg(L1d,L1d_cfg())

    print("Verifying L1t: Toggle")
    verify_cfg(L1t,L1t_cfg())

    # Question 2
    print("Verifying L2e: Exact")
    verify_cfg(L2e,L2e_cfg())

    print("Verifying L2d: Double")
    verify_cfg(L2d,L2d_cfg())

    print("Verifying L2a: Almost")
    verify_cfg(L2a,L2a_cfg())

    # Question 3
    print("Verifying L3a")
    verify_cfg(L3a,L3a_cfg())

    print("Verifying L3b")
    verify_cfg(L3b,L3b_cfg())

    print("Verifying L3c")
    verify_cfg(L3c,L3c_cfg())