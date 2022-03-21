from bisect import bisect

import numpy as np
from spacy.language import Language
from spacy.tokenizer import Tokenizer
from spacy.vocab import Vocab
import random


def delta(a,b):
    if a==b:
        return 0
    else:
        return 1

def delta2(a,b):
    if a==b:
        return 0
    else:
        return 2

def edit_distance(x,y):
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

    print(edit_table)
    w=len(x)
    k=len(y)
    result=[]
    while w!=0 or k!=0:
        if w==0:
            k=k-1
            result.append("usuniecie literki")
        elif k==0:
            w=w-1
            result.append("dodanie literki: "+x[w] +'\n'+x[:w]+"*"+x[w]+"*"+y[k:]+"\nprawidłowy łańcuch: "+x+'\n')
        else:
            tmp=min(edit_table[w - 1, k]+1, edit_table[w, k - 1]+1, edit_table[w - 1, k - 1]+delta(x[w-1],y[k-1]))
            if tmp==edit_table[w - 1, k - 1]+delta(x[w-1],y[k-1]):
                w = w - 1
                k = k - 1
                if delta(x[w],y[k])==1:
                    result.append("zamiana znaku: " +y[k]+"->" +x[w]+":\n"+x[:w]+y[k:]+"->"+x[:w+1]+y[k+1:]+"\nprawidłowy łańcuch: "+x+'\n')
            elif tmp==edit_table[w , k - 1]+1:
                k = k - 1
                result.append("usuniecie literki: "+ y[k]+'\n'+x[:w]+y[k:]+"->"+x[:w]+y[k+1:]+"\nprawidłowy łańcuch: "+x+'\n')
            else:
                w = w - 1
                result.append("dodanie literki: "+x[w] +'\n'+x[:w]+"*"+x[w]+"*"+y[k:]+"\nprawidłowy łańcuch: "+x+'\n')


    for i in range(len(result)-1,-1,-1):
        print(result[i])
    return edit_table[(len(x),len(y))]

#print("edit distance: ",edit_distance("kloc","los"))
def lcs1(x,y):
    return (len(x)+len(y)-edit_distance2(x,y))/2

#print("lcs: ",lcs1("kloc","los"))

def edit_distance2(x,y):
    edit_table=np.empty((len(x)+1,len(y)+1))
    for i in range(len(x)+1):
        edit_table[i,0]=i
    for j in range(len(y)+1):
        edit_table[0,j]=j

    for i in range(len(x)):
        k=i+1
        for j in range(len(y)):
            l=j+1
            edit_table[k,l]= min(edit_table[k-1,l]+1,edit_table[k,l-1]+1,edit_table[k-1,l-1]+ delta2(x[i],y[j]))
    return edit_table[(len(x), len(y))]

def lcs2(x, y):
    ranges = [len(y)]
    y_letters = list(y)
    for i in range(len(x)):
        positions = [j for j, l in enumerate(y_letters) if l == x[i]]
        positions.reverse()
        for p in positions:
            k = bisect(ranges, p)
            if k == bisect(ranges, p - 1):
                if k < len(ranges) - 1:
                    ranges[k] = p
                else:
                    ranges[k:k] = [p]
    return len(ranges) - 1

def remove_tokens(tokens):
    res = []
    for t in tokens:
        if random.random() >= 0.03:
            res.append(t)
    return res

def tokenizator():
    file= open('romeo-i-julia-700.txt', "r",encoding='UTF-8')
    text = file.read()
    vocab = Language(Vocab()).vocab
    tokenizer = Tokenizer(vocab)
    tokens = tokenizer(text)
    text1 = remove_tokens(tokens)
    text2 = remove_tokens(tokens)
    with open('text1.txt', 'w') as new_file1:
        for token in text1:
            new_file1.write(token.text_with_ws)
    with open('text2.txt', 'w') as new_file2:
        for token in text2:
            new_file2.write(token.text_with_ws)
    new_file1.close()
    new_file2.close()
    f1 = open('text1.txt', "r")
    f2 = open('text2.txt', "r")
    t1=f1.read()
    t2=f2.read()
    print("dlugosc 1 tekstu: ", len(t1))
    print("dlugosc 2 tekstu: ", len(t2))
    print("długość najdłuższego podciągu wspólnych tokenów: ", lcs2(t1, t2))


tokenizator()

def diff(a, b):
    L = [[0 for _ in range(len(b) + 1)] for _ in range(len(a) + 1)]
    for i in range(len(a) + 1):
        for j in range(len(b) + 1):
            if i == 0 or j == 0:
                L[i][j] = 0
            elif a[i - 1] == b[j - 1]:
                L[i][j] = L[i - 1][j - 1] + 1
            else:
                L[i][j] = max(L[i - 1][j], L[i][j - 1])
    lines = []
    i = len(a) - 1
    j = len(b) - 1
    while i >= 0 and j >= 0:
        if a[i] == b[j]:
            i, j = i-1, j-1
        elif L[i][j-1] >= L[i-1][j]:
            lines.append(f"> [{j}] {b[j]}")
            j -= 1
        elif L[i][j-1] < L[i-1][j]:
            lines.append(f"< [{i}] {a[i]}")
            i -= 1
    while j >= 0:
        lines.append(f"> [{j}] {b[j]}")
        j -= 1
    while i >= 0:
        lines.append(f"< [{i}] {a[i]}")
        i -= 1
    lines.reverse()
    for line in lines:
        print(line)


f1 = open('text1.txt', "r")
f2 = open('text2.txt', "r")
arr_text1=[]
arr_text2=[]
for linia in f1:
    arr_text1.append(linia)
for linia in f2:
    arr_text2.append(linia)
#diff(arr_text1,arr_text2)