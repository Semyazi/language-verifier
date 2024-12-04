import random
random.seed(313)

import config

# prefix function - KMP
def Pf(s):
    n=len(s)
    pi=[0]*n
    for i in range(1,n):
        cur=pi[i-1]
        while cur>0 and s[cur]!=s[i]:
            cur=pi[cur-1]
        if cur==0:cur=s[0]==s[i]
        else:cur+=1
        pi[i]=cur
    return pi

# build a prefix automaton w/ kmp
class PrefixAutomaton:
    def __init__(self,pattern):
        self.patlen=len(pattern)
        self.pi=Pf(pattern)

        # for each value prefix can take and for each char, figure out the transition with DP
        self.delta=[{} for _ in range(self.patlen+1)]
        for l in range(self.patlen+1):
            for c in config.ALPHA:
                # assume the prefix function is l and we read c, find the new value of the pfx fcn
                if l<self.patlen and pattern[l]==c:
                    self.delta[l][c]=l+1
                    continue
                if l==0:
                    self.delta[l][c]=pattern[0]==c
                    continue

                self.delta[l][c]=self.delta[self.pi[l-1]][c]
    
    def occur(self,s):
        cur=0
        cnt=cur==self.patlen
        for char in s:
            cur=self.delta[cur][char]
            cnt+=cur==self.patlen
        return cnt

# generate random string of length l with characters from our alphabet
def rstr(l):
    return ''.join(random.choice(config.ALPHA) for _ in range(l))

def twice(s):
    x=''
    for c in s:
        x+=2*c
    return x

def toggle(s):
    x=''
    for c in s:
        x+=str(1-int(c))
    return x

def is_pal(s):
    return s==s[::-1]