from queue import Queue
import time
class Node:
    def __init__(self):
        self.stan = 0
        self.children = {}
        self.faillink =None


def kmp_string_matching(text,pattern,pi,idx,l):
    shifts = []
    q = 0
    for i in range(0, len(text)):
        while (q > 0 and pattern[q] != text[i]):
            q = pi[q - 1]
        if (pattern[q] == text[i]):
            q = q + 1
        if (q == len(pattern)):
            shifts.append((i + 1 - q, idx+1-l))
            q = pi[q - 1]
    return shifts


def prefix_function(pattern):
    pi = [0]
    k = 0
    for q in range(1, len(pattern)):
        while (k > 0 and pattern[k] != pattern[q]):
            k = pi[k - 1]
        if (pattern[k] == pattern[q]):
            k = k + 1
        pi.append(k)

    return pi

class Tree:
    def __init__(self,pattern):
        self.root= Node()
        self.stany_koncowe = []
        self.pattern=pattern

        aktualny_stan = 0
        alfabet = set()
        n = len(pattern)
        for i in range(n):
            tmp= self.root
            for j in range(len(pattern[i])):
                if pattern[i][j] not in tmp.children.keys():
                    alfabet.add(pattern[i][j])
                    tmp_child= Node()
                    aktualny_stan += 1
                    tmp_child.stan = aktualny_stan
                    tmp.children[pattern[i][j]]=tmp_child
                tmp=tmp.children[pattern[i][j]]

        q = Queue()
        for c in self.root.children.keys():
            self.root.children[c].faillink = self.root
            q.put(self.root.children[c])


        for l in alfabet:
            if l not in self.root.children:
                self.root.children[l] =self.root

        while not q.empty():
            node = q.get()
            for l in alfabet:
                if l in node.children.keys():
                    next_node = node.children[l]
                    q.put(next_node)
                    tmp = node.faillink
                    while l not in tmp.children.keys():
                        tmp = tmp.faillink
                    next_node.faillink = tmp.children[l]


        for i in range(n):
            tmp = self.root
            for l in pattern[i]:
                tmp=tmp.children[l]
            self.stany_koncowe.append(tmp.stan)

    def znajdz_stan_powrotu(self,letter,tmp_node):
        while letter not in tmp_node.children.keys():
            tmp_node = tmp_node.faillink
            if tmp_node is None:
                tmp_node= self.root
                return tmp_node
        tmp_node = tmp_node.children[letter]
        return tmp_node

    def find(self,text):
        l = len(text[0])
        arr = []
        for line in text:
            l=max(l, len(line))
            arr.append([])
        for i in range(len(text)):
            tmp_node = self.root
            for j in range(l):
                if(j<len(text[i])):
                    tmp_node = self.znajdz_stan_powrotu(text[i][j],tmp_node)
                    arr[i].append(tmp_node.stan)
                else:
                    arr[i].append(0)
        result = []
        pi = prefix_function(self.stany_koncowe)
        x=[0 for i in range(len(text))]
        for i in range(l):
            for j in range(len(text)):
                x[j]=arr[j][i]
            shifts=kmp_string_matching(x, self.stany_koncowe, pi, i,len(self.pattern[0]))
            for shift in shifts:
                result.append(shift)
        return result

def zad2():
    file=open('haystack.txt','r')
    text = file.readlines()
    alfabet = set()
    for line in text:
        for c in line:
            alfabet.add(c)

    for l in alfabet:
        tree = Tree([l, l])
        result = tree.find(text)
        if len(result)>0:
            print(l)
            print(result)
#zad2()

def zad3():
    file = open('haystack.txt', 'r')
    text= file.readlines()

    tree1= Tree(["th", "th"])
    result1 = tree1.find(text)
    print("th:")
    print(result1)
    tree2 = Tree(["t h", "t h"])
    result2 = tree2.find(text)
    print("t h:")
    print(result2)

#zad3()

def zad6():
    file = open('haystack.txt', 'r')
    text = file.readlines()
    pattern1 = ["reader",
                     "ted to"]
    pattern2 = ["The theoretical approach to the representation",
                      "of trees or finite state automata. It appears ",
                      "efficient. This shows the practical importance",
                      "approach to text problems. At LITP (Paris) and"]

    pattern3 =["An image scanner is a kind of photocopier. It is used to give a digitiz",
               "version of a n image. W h e n the image is a page of text, the n a t u ",
               "scanner must be in a digital form available to a text editor. T h e tra",
               "of a digitized image of a text into a usual computer representation of ",
               "is realized by a n Optical Character Recognition ( O C R ) . Scanning a",
               "an O C R can be 50 times faster t h a n retyping the text on a keyboard",
               "O C R softwares are likely to become more common. B u t they still suff",
               "a high degree of imprecision. T h e average rate of error in the recogn",
               "characters is approximately one percent. Even if this may h a p p e n t",
               "small, this means t h a t scanning a book produces approximately one er",
               "line. This is compared with the usually very high quality of texts chec",
               "by specialists. Technical improvements on the hardware can help elimina",
               "certain kinds of errors occurring on scanned texts in printed forms. Bu",
               "cannot alleviate the problem associated with recognizing texts in print",
               "Reduction of the number of errors can thus only be achieved by consider",
               "context of the characters, which assumes some understanding of the stru",
               "of the text. Image processing is related to the problem of two-dimensio",
               "pattern matching. Another related problem is the data structure for all",
               "subimages, which is discussed in this book in the context of the dictio"]
    t1 = time.time()
    tree1=Tree(pattern1)
    t1_2=time.time()
    tree1.find(text)
    t1_3=time.time()
    print("czas budowania automatu dla malego wzorca: ", t1_2 - t1)
    print("czas wyszukiwania dla malego wzorca: ", t1_3 - t1_2)

    t2 = time.time()
    tree2=Tree(pattern2)
    t2_2=time.time()
    tree2.find(text)
    t2_3=time.time()
    print("czas budowania automatu dla sredniego wzorca: ", t2_2 - t2)
    print("czas wyszukiwania dla sredniego wzorca: ", t2_3 - t2_2)

    t3 = time.time()
    tree3=Tree(pattern3)
    t3_2=time.time()
    tree3.find(text)
    t3_3=time.time()
    print("czas budowania automatu dla duzego wzorca: ", t3_2 - t3)
    print("czas wyszukiwania dla duzego wzorca: ", t3_3 - t3_2)

#zad6()
