import logging
import random
import spacy
import sys

sys.path.append('./')
from src.utils import TwoWayDict

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class Substitutor:

    def __init__(self, base_pairs, name_pairs=None, his_him=True, spacy_model='en_core_web_lg'):

        logging.info("Loading spaCy model...")
        self.nlp = spacy.load(spacy_model)
        logging.info("Done.")

        # This flag tells it whether or not to apply the special case intervention to him/his/her/hers
        self.his_him = his_him

        self.base_pairs = TwoWayDict()
        for (male, female) in base_pairs:
            self.base_pairs[male.lower()] = female.lower()

        self.name_pairs = TwoWayDict()
        for (male, female) in name_pairs:
            self.name_pairs[male.lower()] = female.lower()

    def probablistic_substitute(self, input_texts):
        for text in input_texts:
            if bool(random.getrandbits(1)):
                yield self.invert_document(text)
            else:
                yield text

    def invert_document(self, input_text):
        # Parse the doc
        doc = self.nlp(input_text)

        output = input_text

        # Walk through in reverse order making substitutions
        for word in reversed(doc):

            # Calculate inversion
            flipped = self.invert_word(word)

            if flipped is not None:
                # Splice it into output
                start_index = word.idx
                end_index = start_index + len(word.text)
                output = output[:start_index] + flipped + output[end_index:]

        return output

    def invert_word(self, spacy_word):

        flipped = None
        text = spacy_word.text.lower()

        # Handle base case
        if text in self.base_pairs.keys():
            flipped = self.base_pairs[text]

        # Handle name case
        elif text in self.name_pairs.keys() and spacy_word.ent_type_ == "PERSON":
            flipped = self.name_pairs[text]

        # Handle special case (his/his/her/hers)
        elif self.his_him:
            pos = spacy_word.tag_
            if text == "him":
                flipped = "her"
            elif text == "his":
                if pos == "NNS":
                    flipped = "hers"
                else:  # PRP/PRP$
                    flipped = "her"
            elif text == "her":
                if pos == "PRP$":
                    flipped = "his"
                else:  # PRP
                    flipped = "him"
            elif text == "hers":
                flipped = "his"

        if flipped is not None:
            # Attempt to approximate case-matching
            return self.match_case(flipped, spacy_word.text)
        return None

    @staticmethod
    def match_case(input_string, target_string):
        # Matches the case of a target string to an input string
        # This is a very naive approach, but for most purposes it should be okay.
        if target_string.islower():
            return input_string.lower()
        elif target_string.isupper():
            return input_string.upper()
        elif target_string[0].isupper() and target_string[1:].islower():
            return input_string[0].upper() + input_string[1:].lower()
        else:
            logging.warning("Unable to match case of {}".format(target_string))
            return input_string
