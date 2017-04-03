import sys
import nltk
from nltk.collocations import *


inputfile = sys.argv[1]
outputfile = sys.argv[2]
bigram_measures = nltk.collocations.BigramAssocMeasures()
_POS_TAGGER = 'taggers/maxent_treebank_pos_tagger/english.pickle'

'''
for each line in file
a sentence is cat(top, bottom)
extract features* for each line 
The features being 
1) unigrams/ bigrams
2) POS features
3) Dependency Triples

Features
1. unigrams
2. bigrams
3. 
'''

# TODO: Figure out how the cat paper store the features

outf = open(outputfile, 'w')
with open(inputfile, 'r') as inf:
	for line in inf:
		text=line
		tokens = nltk.word_tokenize(text)
		tokens = [token.lower() for token in tokens if len(token) > 1] #same as unigrams

		
outf.close()



def get_bigrams(text):
	finder = BigramCollocationFinder.from_words(text)
	### MUST CHANGE THIS
	return 	finder.nbest(bigram_measures.pmi, 10) ## change to find all 

def pos_tag(tokens):
	tagger = load(_POS_TAGGER)
    return tagger.tag(tokens)

# Dependency Triples

# Named Entity Features

# Frame-Semantics Features



