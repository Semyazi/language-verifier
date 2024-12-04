import reg
import cfg
import lang

r=reg.RegexLanguage('(1+e) (01)* 00 (10)* 11 (01)* (0+e) + (0+e) (10)* 11 (01)* 00 (10)* (1+e)')
c=cfg.CFGLanguage("""
S>1A,A,0D,D
A>01A,00B
B>10B,11C
C>01C,0,e
D>10D,11E
E>01E,00F
F>10F,1,e
""")

lang.comp(r,c)