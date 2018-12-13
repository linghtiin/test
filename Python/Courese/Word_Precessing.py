# -*- coding: utf-8 -*-
"""
Created on Sat Dec  8 20:44:17 2018

@author: z
"""
import os
import pandas as pd
from collections import Counter

stats = pd.DataFrame(columns = ("Language","Author","Title","Length","Unique"))
book_dir = "./Books"
word = "We can`t do that.If we do,he will die!Are you understand?You:yes,madem."

def word_count(text):
    """  """
    text = text.lower()
    skips = ['.',',',';','?',':','!','"',"'"]
    for ch in skips:
        text = text.replace(ch," ")
    
#    word_counts = {}
#    for word in text.split(" "):
#        if word in word_counts:
#            word_counts[word] += 1
#        else:
#            word_counts[word] = 1
    word_counts = Counter(text.split(" "))
    
    return word_counts

def read_book(title_path):
    """ Read a book and return it as a string. """
    with open(title_path,"r",encoding="utf8") as current_file:
        text = current_file.read()
        text = text.replace("\n",'').replace("\r",'')
    return text

def word_stats(word_counts):
    """ Return (num_unique,counts) """
    num_unique = len(word_counts)
    counts = word_counts.values()
    return (num_unique,counts)


title_num = 1
for language in os.listdir(book_dir):
    for author in os.listdir(book_dir + "/" + language):
        for title in os.listdir(book_dir + "/" + language + "/" + author):
            inputfile = book_dir + "/" + language + "/" + author + "/" + title
            print(inputfile)
            text = read_book(inputfile)
            (num_unique,counts) = word_stats(word_count(text))
            stats.loc[title_num] = language.title(),author.title(),title.replace(".txt","").capitalize(),sum(counts),num_unique
            title_num += 1