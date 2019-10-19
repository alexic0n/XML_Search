import os
import sys
import re
from nltk.stem import PorterStemmer

known_stems = {}
regex = re.compile('[^a-zA-Z ]')

def make_stop():
    stop_list_file = open("files/englishST.txt","r")
    stop_list = []
    for line in stop_list_file:
        line = regex.sub('',line.lower())
        stop_list.append(line)
    stop_list_file.close
    return stop_list

def stem(token):
    if token in known_stems:
        return known_stems[token]
    ps = PorterStemmer()
    stemmed_token = ps.stem(token)
    known_stems[token] = stemmed_token
    return stemmed_token

def process_line(line, stop_list, applystopandstem):
    line = line.lower()
    line = regex.sub(' ',line)
    tokens = line.split()
    if applystopandstem:
        return [stem(token) for token in tokens if token not in stop_list]
    return tokens

def full_suite(in_file,out_file):
    k = 0
    stop_list = make_stop()
    with open(in_file,"r") as fin, open(out_file,"w+") as fout:
        for line in fin:
            k = k + 1
            if(line != "\n"):
                processed_lined = process_line(line, stop_list, True)
                for a in processed_lined:
                    fout.write(a + "\n")
            if k % 100000 == 0:
                print(k)
