import sys
sys.path.append('./')

from src.substitutor import Substitutor
from src.utils import load_json_pairs

# Run me from the base directory.

# Example text which requires NER and POS information to properly invert
text = "Amber grabbed her pick-axe and began chipping away at the last of the amber."

base_pairs = load_json_pairs('data/cda_default_pairs.json')
name_pairs = load_json_pairs('data/names_pairs_1000_scaled.json')

# Initialise a substitutor with a list of pairs of gendered words (and optionally names)
substitutor = Substitutor(base_pairs, name_pairs=name_pairs)

flipped = substitutor.invert_document(text)

print("Before: {}".format(text))
print("After: {}".format(flipped))
# It correctly doesn't flip the sentence ending noun "amber", and properly converts "her" to "his" not "him"

# If you want to apply an intervention probablistically, use the method
flipped = substitutor.probablistic_substitute([text, text, text, text])
# which takes a list and returns a generator which flips 50% of documents

print("50% chance flipped: {}".format(next(flipped)))
print("50% chance flipped: {}".format(next(flipped)))
print("50% chance flipped: {}".format(next(flipped)))
print("50% chance flipped: {}".format(next(flipped)))

