import sys
import os
import nltk
from nltk.collocations import *
from nltk.parse.malt import MaltParser
from nltk.internals import find_jars_within_path
from nltk.tag import StanfordPOSTagger
from nltk.tag import StanfordNERTagger
# from semaphore import semaphore

'''
Run:
python extract_text_features.py <sentences.txt> <out.txt>
'''
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

# MaltParser for dependency triples
# how to get maltparser to work: http://stackoverflow.com/questions/13207394/step-by-step-to-getting-malt-parser-in-nltk-to-work
set_maltparser= "export MALT_PARSER=%s" % (os.path.abspath("maltparser-1.8.1"))
set_maltmodel = "export MALT_MODEL=%s" % (os.path.abspath("engmalt.linear-1.7.mco"))
os.system(set_maltmodel)
os.system(set_maltparser)
mp = MaltParser('maltparser-1.8.1', 'engmalt.linear-1.7.mco')

# Name entity tagger
#add the jar and model via their path:
ner_jar = os.path.abspath("stanford-ner-2016-10-31/stanford-ner-3.7.0.jar")
ner_model = os.path.abspath("stanford-ner-2016-10-31/classifiers/english.all.3class.distsim.crf.ser.gz")
ner_st = StanfordNERTagger(ner_model, ner_jar) 
pos_jar = os.path.abspath("stanford-postagger-2016-10-31/stanford-postagger.jar")
pos_model =  os.path.abspath("stanford-postagger-2016-10-31/models/english-bidirectional-distsim.tagger")
pos_st = StanfordPOSTagger(pos_model, pos_jar) 

# TODO: Figure out how the cat paper store the features



def get_bigrams(text):
	finder = BigramCollocationFinder.from_words(text)
	#TODO: check what the expected results should be for bigrams
	return 	finder.nbest(bigram_measures.pmi, 10) ## change to find all 

def pos_tag(st, tokens):
	return st.tag(tokens)

# Dependency Triples
def dependency_triples(mp, sentence):
	'''
	typed dependency triples (e.g., subj(I,are)) using the MaltParser (Nivre et al., 2007).
	http://stackoverflow.com/questions/13207394/step-by-step-to-getting-malt-parser-in-nltk-to-work
	return typed dependency triples (Tree) 
	TODO: figure out if can use other data structures other than tree
	'''
	return  mp.parse_one(sentence.split()).tree()
	
	

# Named Entity Feature
def name_entity_features(st, sentence):
	'''
	Document: http://www.nltk.org/api/nltk.tag.html#module-nltk.tag.stanford
	I'm using english.all.3class.distsim.crf.ser.gz model for now, but we can change to 4class or 7class later.
	'''	
	return st.tag(sentence.split()) 

# Frame-Semantics Features
# def frame_semantics_features(sentence):
# '''
# I'm using https://github.com/Noahs-ARK/semafor. But it is currently not working.
# '''
# 	frames=semaphore(sentence)
# 	return frames

outf = open(outputfile, 'w')
print "unigrams\tbigrams\tpostags\tdepend_triples\tname_entity"
outf.write("unigrams\tbigrams\tpostags\tdepend_triples\tname_entity\n")
with open(inputfile, 'r') as inf: # assume each line is one sentence
	for line in inf:
		text= line
		tokens = nltk.word_tokenize(text)
		tokens = [token.lower() for token in tokens if len(token) > 1] #same as unigrams
		bigrams = get_bigrams(text)
		pos_tags = pos_tag(pos_st, text.split())
		dep_trip = dependency_triples(mp, text)
		name_entity = name_entity_features(ner_st, text)
		print (text)
		print "%s\t%s\t%s\t%s\t%s" % (tokens, bigrams, pos_tags, dep_trip, name_entity)
		outf.write("%s\t%s\t%s\t%s\t%s\n" % (tokens, bigrams, pos_tags, dep_trip, name_entity))
		
		os._exit(1)
		
outf.close() # input file is already closed in 'with open' so we don't have to close it manually 
