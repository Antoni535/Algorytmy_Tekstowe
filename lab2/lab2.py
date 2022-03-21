class Node:
    def __init__(self, x):
        self.x=x
        self.children=[]

class Trie:
    def __init__(self, x):
        self.root=Node(x)
    def compute_initial_trie(self, text):
        x=self.root
        for i in range(len(text)):
            y=Node(text[i])
            x.children.append(y)
            x=y
    def find(self, suffix):
        tmp=self.root
        l=0
        for i in range(len(suffix)):
            end=1
            for j in range(len(tmp.children)):
                if tmp.children[j].x==suffix[i]:
                    l+=1
                    tmp=tmp.children[j]
                    end = 0
                    break
            if end==1: break
        return tmp,l
    def build_tree_schema(self, text):
        self.compute_initial_trie(text)
        for i in range(1, len(text)):
            suffix = text[i:]
            tmp,num = self.find(suffix)
            for j in range(num, len(suffix)):
                y = Node(suffix[j])
                tmp.children.append(y)
                tmp = y
    def contains_word(self, word):
        tmp=self.root
        for j in range(len(word)):
            for i in tmp.children:
                if i.x==word[j]:
                    if j==len(word)-1:
                        return True
                    tmp=i
                    break
        return False


#f = open("plik.txt", "r", encoding='utf-8')
#plik = f.read()
#trie1=Trie("root1")
#trie1.build_tree_schema(plik)
#print(trie1.contains_word("ryczałt"))

class Suffix_Tree:
    def __init__(self, x):
        self.root = Node(x)
    def compute_initial_suffix_tree(self, text):
        root=self.root
        y=Node(text)
        root.children.append(y)

    def find_head(self, root, suffix):
        r=root
        for chi in r.children:
            if chi.x[0] == suffix[0]:
                suffix=suffix[1:]
                i=1
                while i<len(chi.x):
                    if (chi.x[i]==suffix[0]):
                        suffix=suffix[1:]
                        i+=1
                    else:
                        return chi, i, suffix
                return self.find_head(chi, suffix)
        return r, -1, suffix

    def build_suffix_tree(self, text):
        self.compute_initial_suffix_tree(text)
        r=self.root
        for i in range(1, len(text)):
            suffix=text[i:]
            head, l, suff=self.find_head(r, suffix)
            x=head.x
            child=head.children
            if l==-1:
                tmp=Node(suff)
                head.children.append(tmp)
            else:
                x1=x[:l]
                x2=x[l:]
                tmp=Node(x2)
                tmp2=Node(suff)
                head.x=x1
                head.children=[]
                head.children.append(tmp)
                head.children.append(tmp2)
                tmp.children=child
    def contains_word(self, root, word):
        tmp=root
        for chi in tmp.children:
            if chi.x[0]==word[0]:
                word=word[1:]
                if len(word)==0:
                    return True
                i=1
                while i<len(chi.x):
                    if chi.x[i]==word[0]:
                        word=word[1:]
                        if len(word) == 0:
                            return True
                    else:
                        return False
                    i+=1
                return self.contains_word(chi, word)
        return False

#suffix_Tree=Suffix_Tree("suffix_tree_root")
#suffix_Tree.build_suffix_tree(plik)
#print(suffix_Tree.contains_word(suffix_Tree.root, "budżet"))
#print(suffix_Tree.contains_word(suffix_Tree.root, "Nr 137, poz. 638, Nr 147, poz. 686 i Nr 156,"))

t1="bbbd"
t2="aabbabd"
t3="ababcd"
t4="abcbccd"
f = open("plik.txt", "r", encoding='utf-8')
t5 = f.read()
import time
def tests(text):
    trie1 = Trie("trie_root")
    x1=time.time()
    trie1.build_tree_schema(text)
    y1=time.time()
    suffix_Tree = Suffix_Tree("suffix_tree_root")
    x2=time.time()
    suffix_Tree.build_suffix_tree(text)
    y2=time.time()
    return y1-x1, y2-x2

time1,time2=tests(t1)
print("TEST 1")
print("Build trie time: ")
print(time1)
print("Build suffix tree time: ")
print(time2)
print("TEST 2")
time1,time2=tests(t2)
print("Build trie time: ")
print(time1)
print("Build suffix tree time: ")
print(time2)
print("TEST 3")
time1,time2=tests(t3)
print("Build trie time: ")
print(time1)
print("Build suffix tree time: ")
print(time2)
print("TEST 4")
time1,time2=tests(t4)
print("Build trie time: ")
print(time1)
print("Build suffix tree time: ")
print(time2)
print("TEST 5")
time1,time2=tests(t5)
print("Build trie time: ")
print(time1)
print("Build suffix tree time: ")
print(time2)