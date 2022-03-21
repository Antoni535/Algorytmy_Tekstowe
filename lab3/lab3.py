from bitarray import bitarray

class Node:
    def __init__(self,letter, w,left,right,idx=0,parent=None):
        self.letter=letter
        self.w=w
        self.left=left
        self.right=right
        self.idx=idx
        self.parent=parent
    def increment(self,arr):
        if self.parent==None:
            self.w+=1
            return
        tmpw=self.w
        tmpidx=self.idx
        i=0
        while arr[i].w!=tmpw:
            i+=1
        if arr[i].idx==tmpidx:
            arr[i].w+=1
            arr[i].parent.increment(arr)
        else:
            tmpnode1=arr[i]
            tmp_parent1=tmpnode1.parent
            tmpnode2=self
            tmp_parent2=self.parent
            if tmp_parent1.idx==tmp_parent2.idx:
                tmp_parent1.left,tmp_parent1.right=tmp_parent1.right,tmp_parent1.left
                self.w+=1
                self.idx,arr[i].idx=arr[i].idx,self.idx
                arr[tmpnode1.idx],arr[tmpnode2.idx]=arr[tmpnode2.idx],arr[tmpnode1.idx]
                self.parent.increment(arr)
                return
            if tmp_parent1.left.idx==tmpnode1.idx:
                tmp_parent1.left=self
            else:
                tmp_parent1.right=self
            self.w+=1
            self.parent = tmp_parent1
            if tmp_parent2.left.idx == tmpnode2.idx:
                tmp_parent2.left = tmpnode1
            else:
                tmp_parent2.right = tmpnode1
            tmpnode1.parent=tmp_parent2
            self.idx,arr[i].idx=arr[i].idx,self.idx
            arr[tmpnode1.idx],arr[tmpnode2.idx]=arr[tmpnode2.idx],arr[tmpnode1.idx]
            self.parent.increment(arr)

def huffman(letter_counts):
    nodes = []
    for a, weight in letter_counts.items():
        nodes.append(Node(a, weight,None,None))
    internal_nodes = []
    nodes = sorted(nodes, key=lambda n: n.w)
    if len(nodes)==0:
        return None
    if len(nodes)==1:
        return nodes[0]
    element_1, element_2 =nodes.pop(0),nodes.pop(0)
    internal_nodes.append(Node(None, element_1.w + element_2.w,element_1,element_2))
    while(len(nodes) + len(internal_nodes) > 1):
        if len(nodes)>0:
            if nodes[0].w<=internal_nodes[0].w:
                element_1=nodes.pop(0)
                if len(nodes)>0:
                    if nodes[0].w<=internal_nodes[0].w:
                        element_2=nodes.pop(0)
                    else:
                        element_2=internal_nodes.pop(0)
                else:
                    element_2 = internal_nodes.pop(0)
            else:
                element_1=internal_nodes.pop(0)
                if len(internal_nodes) > 0:
                    if nodes[0].w<=internal_nodes[0].w:
                        element_2=nodes.pop(0)
                    else:
                        element_2=internal_nodes.pop(0)
                else:
                    element_2 = nodes.pop(0)
        else:
            element_1=internal_nodes.pop(0)
            element_2=internal_nodes.pop(0)
        internal_nodes.append(Node(None,element_1.w + element_2.w,element_1,element_2))
    return internal_nodes[0]

def print_codes(node,code):
    if(node.letter!=None):
        print(node.letter +": " +code)
    else:
        print_codes(node.left,code+"0")
        print_codes(node.right,code +"1")

def hash_letter(node,code,dict):
    if(node.letter!=None):
        dict[node.letter]=code
    else:
        hash_letter(node.left,code+"0",dict)
        hash_letter(node.right,code +"1",dict)

def letter_counts(text):
    letter_c = {}
    for letter in text:
        if letter in letter_c.keys():
            letter_c[letter]=letter_c[letter]+1
        else:
            letter_c[letter] = 1
    return letter_c

def code(text,save_file,dict):
    s_f=open(save_file,"wb")
    bitarr=bitarray()
    for l in text:
        bitarr+=dict.get(l)
    bitarr.tofile(s_f)
    s_f.close()
    return len(bitarr)
def decode(file,decode_file,root,len_bitarr):
    f=open(file,"rb")
    d_f=open(decode_file,"w")
    bitarr=bitarray()
    bitarr.fromfile(f)
    bitarr=bitarr[:len_bitarr]
    i=0
    while i<len(bitarr):
        r=root
        while r.letter==None:
            if bitarr[i]==0:
                r=r.left
            else: r=r.right
            i+=1
        d_f.write(r.letter)
    f.close()
    d_f.close()

def make_alfphabet(text):
    al=[]
    for l in text:
        if l not in al:
            al.append(l)
    return al

def start_adaptiv_Huffman(alphabet):
    arr = []
    nodes = {}
    root = Node('#', 0, None, None)
    arr.append(root)
    nodes['#'] = root
    for letter in list(alphabet):
            tmp = arr[len(arr) - 1]
            node1 = Node(letter, 1, None, None, tmp.idx + 1, tmp)
            node2 = Node('#', 0, None, None, tmp.idx + 2, tmp)
            arr.append(node1)
            arr.append(node2)
            tmp.letter = None
            tmp.left = node2
            tmp.right = node1
            tmp.w = 1
            nodes[letter] = node1
            if tmp.parent != None:
                tmp.parent.increment(arr)
    return root, nodes, arr

def adaptive_huffman_code(text,save_file,alphabet):
    root, nodes, arr=start_adaptiv_Huffman(alphabet)
    s_f = open(save_file, "wb")
    s_f.truncate()
    bitarr=bitarray()
    for letter in list(text):
        actual_dict = {}
        hash_letter(root, "", actual_dict)
        bitarr+=actual_dict.get(letter)
        node = nodes.get(letter)
        node.increment(arr)
    bitarr.tofile(s_f)
    s_f.close()
    return len(bitarr)

def adaptive_huffman_decode(file,decode_file,len_bitarr,alphabet):
    f = open(file, "rb")
    d_f = open(decode_file, "w")
    bitarr = bitarray()
    bitarr.fromfile(f)
    bitarr=bitarr[:len_bitarr]
    root, nodes, arr = start_adaptiv_Huffman(alphabet)
    tmp=""
    actual_dict={}
    hash_letter(root, "", actual_dict)
    i=0
    while i < len(bitarr):
        r = root
        while r.letter == None:
            if bitarr[i] == 0:
                r = r.left
            else:
                r = r.right
            i += 1
        node = nodes.get(r.letter)
        node.increment(arr)
        d_f.write(r.letter)
        hash_letter(root, "", actual_dict)
    f.close()
    d_f.close()

import time
import os
def test(file):
    f=open(file, "r",encoding='UTF-8')
    t=f.read()
    x1=time.time()
    l_c=letter_counts(t)
    x=huffman(l_c)
    dictionary_Huffman = {}
    hash_letter(x, "", dictionary_Huffman)
    len1 = code(t, "code_file.txt", dictionary_Huffman)
    y1=time.time()
    decode("code_file.txt", "decode_file.txt", x, len1)
    z1=time.time()
    s1=os.path.getsize("code_file.txt")
    s2=os.path.getsize("decode_file.txt")
    print("Statyczny algorytm Huffmana wspolczynnik kompresji:",1-s1/s2)
    print("Statyczny algorytm Huffmana czas kompresji:",y1-x1)
    print("Statyczny algorytm Huffmana czas dekompresji:",z1-y1)
    alphabet = make_alfphabet(t)
    x2=time.time()
    len2 = adaptive_huffman_code(t, "adaptive_code_file.txt", alphabet)
    y2=time.time()
    adaptive_huffman_decode("adaptive_code_file.txt", "adaptive_decode_file.txt", len2, alphabet)
    z2=time.time()
    s3 = os.path.getsize("adaptive_code_file.txt")
    s4 = os.path.getsize("adaptive_decode_file.txt")
    print("Dynamiczny algorytm Huffmana wspolczynnik kompresji:", 1 - s3 / s4)
    print("Dynamiczny algorytm Huffmana czas kompresji:", y2 - x2)
    print("Dynamiczny algorytm Huffmana czas dekompresji:", z2 - y2)

test("plikGithub.txt")