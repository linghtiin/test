# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 23:27:27 2018

@author: z
"""
import re

def read_seq(inportfile):
    with open(inportfile,"r") as f:
        seq = f.read()
    seq = seq.replace("\n","")
    seq = seq.replace("\r","")
    return seq

def translate(mRNA):
    """ this funtion is translate mRNA to protein. """
    TranList = {
    'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M',
    'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
    'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K',
    'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',
    'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
    'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
    'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q',
    'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
    'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',
    'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
    'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
    'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
    'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
    'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
    'TAC':'Y', 'TAT':'Y', 'TAA':'_', 'TAG':'_',
    'TGC':'C', 'TGT':'C', 'TGA':'_', 'TGG':'W',
    }
    
    protein = ""
    if len(mRNA) % 3 == 0:
        for i in range(0,len(mRNA),3):
            codon = mRNA[i:i+3]
            protein += TranList[codon]
    return protein


inportfile = "NM_207618.2.txt"
seq = read_seq(inportfile)
mRNA = re.search(r'mRNA(\w+)',seq).group(0)[4:]
translation = re.search(r'translation="(.+?)"',seq).group(0)[13:-1]
if translation in translate(mRNA[20:938]):
    print(True)