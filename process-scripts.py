import pickle
import os
from scraper import *

## Markov Chain Generation ----------------------------------------------------
def generate_trigram(words):
    if len(words) < 3:
        return
    for i in xrange(len(words) - 2):
        yield (words[i], words[i+1], words[i+2])

def generate_chain(sentences):
	chain = {}

	for sentence in sentences:
		words = sentence.split()
		for word1, word2, word3 in generate_trigram(words):
		    key = (word1, word2)
		    if key in chain:
		        chain[key].append(word3)
		    else:
		        chain[key] = [word3]

	return chain

## Main -----------------------------------------------------------------------
weighted_characters = []
character_dialogue = {}

# make a list of all characters
for filename in os.listdir('scripts'):

	# open and read the file
	script_file = open('scripts/' + filename, 'r')

	script_html = script_file.read()
	script_file.close()

	# scrape episode for data
	info, utterances = scrape_episode(script_html)
	
	# get a unique list of all the characters
	for _, (speaker, sentences) in enumerate(utterances):
		
		weighted_characters.append(speaker)

		# store sentences for each speaker
		character_dialogue[speaker] = character_dialogue.get(speaker, [])
		sentence_list = []
		for _, sentence in enumerate(sentences):
			sentence_list.append(sentence)
		character_dialogue[speaker].append("BEGIN NOW " + " ".join(sentence_list) + " END")

# generate markov chain data for all speaker sentences
for speaker, sentences in character_dialogue.iteritems():
	chain = generate_chain(sentences)
	pickle.dump(chain, open('data/'+speaker+'.p', 'wb'))

# save to file
pickle.dump(weighted_characters, open('data/_characters.p', 'wb'))