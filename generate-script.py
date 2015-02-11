#!/usr/bin/env python -tt
  
import pickle
import random
from settings import *
from markov import *

def generate_script():
	# pick a number of characters to be in the scene
	num_characters = random.randint(MIN_CHARACTERS, MAX_CHARACTERS)
	weighted_characters = pickle.load(open('data/_characters.p', 'rb'))

	# pick characters from weighted list
	cast = []
	while len(cast) < num_characters:
		cast_member = random.choice(weighted_characters)
		if cast_member in cast:
			continue
		cast.append(cast_member)

	# load cast dialogue chains
	dialogue_chains = {}
	for cast_member in cast:
		dialogue_chains[cast_member] = pickle.load(open('data/'+cast_member+'.p', 'rb'))

	# create script
	script = []
	last_speaker = ""
	num_utterances = random.randint(MIN_UTTERANCES, MAX_UTTERANCES)
	for i in range(num_utterances):

		# choose speaker
		speaker = last_speaker
		while speaker == last_speaker:
			speaker = random.choice(cast)
		last_speaker = speaker
		print speaker

		# choose num sentences
		num_sentences = random.randint(MIN_SENTENCES_PER_UTTERANCE, MAX_SENTENCES_PER_UTTERANCE)
		for j in range(num_sentences):
			sentence = markov(dialogue_chains[speaker])
			print sentence

		# seperator
		print ""

	print "\n".join(script)

if __name__ == '__main__':
	generate_script()