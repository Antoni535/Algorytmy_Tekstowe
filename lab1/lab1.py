#NAIWNY
def naive_string_matching(text, pattern):
    shifts=[]
    for s in range(0, len(text) - len(pattern) + 1):
        if(pattern == text[s:s+len(pattern)]):
            shifts.append(s)
            #print(f"Przesunięcie {s} jest poprawne")
    return shifts
#naive_string_matching("abaabaaaaba", "aba")


#AUTOMAT SKONCZONY
import re
def transition_table(pattern):
    alfabet=set()
    for a in pattern:
        alfabet.add(a)
    result = []
    for q in range(0, len(pattern) + 1):
        result.append({})
        for a in alfabet:
            k = min(len(pattern), q + 1)
            while True:
                if(re.search(f"{pattern[:k]}$", pattern[:q] + a)):
                    break
                k-=1
            result[q][a] = k
    return result

def fa_string_matching(text, pattern):
    shifts=[]
    q = 0
    delta=transition_table(pattern)
    print(delta)
    for s in range(0, len(text)):
        if text[s] in delta[q].keys():
            q = delta[q][text[s]]
            if(q == len(delta) - 1):
                shifts.append(s+1-q)
                #print(f"Przesunięcie {s + 1 - q} jest poprawne")
                # s + 1 - ponieważ przeczytaliśmy znak o indeksie s, więc przesunięcie jest po tym znaku
        else:
            q=0
    return shifts
print(fa_string_matching("abaabaaaaba", "aba"))


#ALGORYTM Knutha-Morrisa-Pratta
def prefix_function(pattern):
    pi = [0]
    k = 0
    for q in range(1, len(pattern)):
        while(k > 0 and pattern[k] != pattern[q]):
            k = pi[k-1]
        if(pattern[k] == pattern[q]):
            k = k + 1
        pi.append(k)
    return pi

def kmp_string_matching(text, pattern):
    shifts=[]
    pi = prefix_function(pattern)
    q = 0
    for i in range(0, len(text)):
        while(q > 0 and pattern[q] != text[i]):
            q = pi[q-1]
        if(pattern[q] == text[i]):
            q = q + 1
        if(q == len(pattern)):
            shifts.append(i+1-q)
            #print(f"Przesunięcie {i + 1 - q} jest poprawne")
            q = pi[q-1]
    return shifts
#kmp_string_matching("abaabaaaaba", "aba")

#Zad 1
import time
def tests(text,pattern):
    x=time.time()
    naive_string_matching(text,pattern)
    y=time.time()
    print(f"Naive string matching time {y-x}")
    x=time.time()
    fa_string_matching(text,pattern)
    y=time.time()
    print(f"FA string matching time {y-x}")
    x=time.time()
    kmp_string_matching(text,pattern)
    y=time.time()
    print(f"KMP string matching time {y - x}")
#tests("tekstowe"*50000, "tekst")

#Zad 2
def art_w_ustawie():
    f=open("lab1_ustawa.txt","r",encoding='utf-8')
    ustawa=f.read()
    print("Naiwny przesuniecia:")
    print(naive_string_matching(ustawa, "art"))
    print("Naiwny liczba przesuniec",len(naive_string_matching(ustawa,"art")))
    print("FA przesuniecia:")
    print(fa_string_matching(ustawa, "art"))
    print("FA liczba przesuniec", len(fa_string_matching(ustawa, "art")))
    print("KMP przesuniecia:")
    print(kmp_string_matching(ustawa, "art"))
    print("KMP liczba przesuniec", len(kmp_string_matching(ustawa, "art")))

#art_w_ustawie()

#Zad 3
def art_w_ustawie_czasy():
    f = open("lab1_ustawa.txt", "r", encoding='utf-8')
    ustawa = f.read()
    tests(ustawa,"art")

#art_w_ustawie_czasy()

#Zad 4
def fa_string_matching_zad4(text, pattern):
    shifts=[]
    q = 0
    delta=transition_table(pattern)
    x=time.time()
    for s in range(0, len(text)):
        if text[s] in delta[q].keys():
            q = delta[q][text[s]]
            if(q == len(delta) - 1):
                shifts.append(s+1-q)
                # s + 1 - ponieważ przeczytaliśmy znak o indeksie s, więc przesunięcie jest po tym znaku
        else:
            q=0
    y=time.time()
    return y-x
def kmp_string_matching_zad4(text, pattern):
    shifts=[]
    pi = prefix_function(pattern)
    q = 0
    x=time.time()
    for i in range(0, len(text)):
        while(q > 0 and pattern[q] != text[i]):
            q = pi[q-1]
        if(pattern[q] == text[i]):
            q = q + 1
        if(q == len(pattern)):
            shifts.append(i+1-q)
            q = pi[q-1]
    y=time.time()
    return y-x
def zad4():
    text="agh"*80000
    pattern="agh"*22000
    x=time.time()
    naive_string_matching(text,pattern)
    y=time.time()
    print(f"Czas algorytm naiwny: {y-x}")
    #print("Czas FA bez pre-processingu:",fa_string_matching_zad4(text,pattern))
    #obliczenie tablicy przejscia trwa bardzo dlugo gdy pattern jest dlugi
    print("Czas KMP bez pre-processingu:", kmp_string_matching_zad4(text, pattern))

#zad4()

#Zad 5
def zad5():
    pattern="agh"*150
    x = time.time()
    transition_table(pattern)
    y = time.time()
    print(f"Czas tablicy przejscia: {y - x}")
    x = time.time()
    prefix_function(pattern)
    y = time.time()
    print(f"Czas funkcji przejscia: {y-x}")

#zad5()

