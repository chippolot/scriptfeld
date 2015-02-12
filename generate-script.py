#!/usr/bin/env python -tt
  
import cPickle as pickle
import random
from settings import *
from markov import *

weighted_speakers = pickle.load(open('data/_characters.p', 'rb'))
dialogue_chains = {}

def generate_script():
	while True:

		# pick a number of characters to be in the scene
		num_speakers = random.randint(MIN_SPEAKERS, MAX_SPEAKERS)

		# pick characters from weighted list
		cast = []
		while len(cast) < num_speakers:
			cast_member = random.choice(weighted_speakers)
			if cast_member in cast:
				continue
			cast.append(cast_member)

		# load cast dialogue chains
		for cast_member in cast:
			if not cast_member in dialogue_chains:
				dialogue_chains[cast_member] = pickle.load(open('data/'+cast_member+'.p', 'rb'))

		# create script
		script = ""
		last_speaker = ""
		num_utterances = random.randint(MIN_UTTERANCES, MAX_UTTERANCES)
		for i in range(num_utterances):

			# choose speaker
			speaker = last_speaker
			while speaker == last_speaker:
				speaker = random.choice(cast)
			last_speaker = speaker
			script += speaker + "\n"

			# say something
			sentence = markov(dialogue_chains[speaker])

			script += sentence + "\n"

			# seperator
			script += "\n"

		# remove the final two line breaks
		script = script[:-2]

		if len(script) > MAX_CHARACTERS:
			continue

		return script

if __name__ == '__main__':
	while True:
		print "---------------------------------------"
		print generate_script()
		print "---------------------------------------"
		choice = raw_input("Another (y/n): ")
		if choice == "n":
			break