import numpy as np

def delta(a,b):
    if a==b:
        return 0
    else:
        return 1

def lcs(x,y):
    edit_table=np.empty((len(x)+1,len(y)+1))
    for i in range(len(x)+1):
        edit_table[i,0]=i
    for j in range(len(y)+1):
        edit_table[0,j]=j

    for i in range(len(x)):
        k=i+1
        for j in range(len(y)):
            l=j+1
            edit_table[k,l]= min(edit_table[k-1,l]+1,edit_table[k,l-1]+1,edit_table[k-1,l-1]+ delta(x[i],y[j]))

    #print(edit_table)
    tmp=[[0 for i in range(len(y)+1)]for j in range(len(x)+1)]
    lcs=0
    for i in range(len(x)):
        for j in range(len(y)):
            if edit_table[i+1][j+1]==edit_table[i][j]:
                tmp[i+1][j+1]=tmp[i][j]+1
                if tmp[i+1][j+1]>lcs:
                    lcs=tmp[i+1][j+1]
    #print(lcs)
    le=max(len(x),len(y))
    metryka_lcs=1-lcs/le
    return metryka_lcs

print(lcs("ababaasadfdsfafsd","caasadfdsc"))

def dice(a,b,n):
    s1=set()
    s2=set()
    for i in range(len(a)-n+1):
        s=a[i:i+n]
        if not s in s1:
            s1.add(s)
    for i in range(len(b)-n+1):
        s=b[i:i+n]
        if not s in s2:
            s2.add(s)

    return 1 - (2*len(s1.intersection(s2))/(len(s1)+len(s2)))

print(dice("kloc","los",2))

def cosinusowa(x,y,n):
    A={}
    B={}
    for i in range(len(x)-n+1):
        t=x[i:i+n]
        if t not in A:
            A[t]=1
        else:
            A[t]+=1

    for i in range(len(y)-n+1):
        t=y[i:i+n]
        if t not in B:
            B[t]=1
        else:
            B[t]=B[t]+1

    keys = set(A.keys()) | set(B.keys())
    vec1= np.zeros(len(keys))
    vec2=np.zeros(len(keys))
    for idx,key in enumerate(keys):
        vec1[idx] = A.get(key,0)
        vec2[idx]=B.get(key,0)

    return 1 - np.dot(vec1,vec2)/(np.linalg.norm(vec1) * np.linalg.norm(vec2))

print(cosinusowa("kloc","los",2))