from __future__ import print_function
import sys
import os
import nltk
from nltk.collocations import * # http://www.nltk.org/howto/collocations.html
from nltk.internals import find_jars_within_path
#from nltk.tag import StanfordPOSTagger, StanfordNERTagger #http://www.nltk.org/api/nltk.tag.html
from nltk.tag.perceptron import PerceptronTagger
from nltk import word_tokenize




'''
Make sure you did module load java
Run:
python extract_text_features_reduced.py <sentences.txt> <out.txt>
python extract_text_features_reduced.py data/memegenerator_algonquin_21000000_22000000_bottom.tsv results/memegenerator_algonquin_21000000_22000000_bottom_features_reduced.tsv
'''

inputfile = sys.argv[1]
outputfile = sys.argv[2]
bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()

pos_tagger = PerceptronTagger() # this is fater than stanford-postagger, according to http://stackoverflow.com/questions/11610076/slow-performance-of-pos-tagging-can-i-do-some-kind-of-pre-warming



# '''
# for each line in file
# a sentence is cat(top, bottom)
# extract features* for each line 
# The features being 
# 1) unigrams/ bigrams
# 2) POS features

# Features
# 1. unigrams
# 2. bigrams
# 3. pos-tags
# '''




def get_bigrams(tokens):
	finder = BigramCollocationFinder.from_words(tokens)
	scored = finder.score_ngrams(bigram_measures.raw_freq)
	#TODO: check what the expected results should be for bigrams
	return 	sorted(bigram for bigram, score in scored) ## change to find all 

def get_trigrams(tokens):
	finder = TrigramCollocationFinder.from_words(tokens)
	scored = finder.score_ngrams(bigram_measures.raw_freq)
	#TODO: check what the expected results should be for bigrams
	return 	sorted(bigram for bigram, score in scored) ## change to find all 



def my_pos_tag(st, tokens):
	'''
	Here is a list of part-of-speech tags: https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
	'''
	tagset = None
	tags = nltk.tag._pos_tag(tokens, tagset, st)
	return tags



outf = open(outputfile, 'w')
inf = open(inputfile, 'r')
print ("unigrams\tbigrams\ttrigrams\tpostags")
outf.write("unigrams\tbigrams\ttrigrams\tpostags\n")

for line in inf:
	text= line
	print(text)
	if line=="NA" or line=="(no top text)" or line=="(no bottom text":
		# print("------NA------")
		outf.write("%s\t%s\t%s\t%s\n" % ("NA", "NA","NA", "NA"))
	else:
		# print("enter tokenizing")
		tokens = nltk.word_tokenize(text)
		tokens = [token.lower() for token in tokens if len(token) > 0] #same as unigrams
		if len(tokens)<=0:
			# print("------NA------")
			outf.write("%s\t%s\t%s\t%s\n" % ("NA", "NA", "NA", "NA"))
		else:
			# print("------NOT NA----")
			bigrams = get_bigrams(tokens)
			trigrams = get_trigrams(tokens)
			pos_tags = my_pos_tag(pos_tagger, tokens)			
			print("%s\t%s\t%s\t%s" % (tokens, bigrams, trigrams, pos_tags))
			outf.write("%s\t%s\t%s\t%s\n" % (tokens, bigrams, trigrams,pos_tags))
			
			
inf.close()
outf.close() # input file is already closed in 'with open' so we don't have to close it manually 


