# https://cp-algorithms.com/string/z-function.html
def Zf(s):
    n=len(s)
    z=[0]*n
    l,r=0,0
    for i in range(1,n):
        if i<r:
            z[i]=min(r-i,z[i-l])
        while (i+z[i]<n)and(s[z[i]]==s[i+z[i]]):
            z[i]+=1
        if i+z[i]>r:
            l=i
            r=i+z[i]
    return z

# num of occurs of x in s
# str.count doesn't work properly with overlap :(
def occur(x,s):
    return Zf(x+'*'+s).count(len(x))