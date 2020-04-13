# Counterfactual Data Substitution

This repository contains an implementation of 
the name-based Counterfactual Data Substitution (CDS) method presented in the paper https://www.aclweb.org/anthology/D19-1530.pdf

### Background

Counterfactual Data Substitution (CDS) is a gender mitigation method that works at the corpus level. 
It works by probablistically applying an intervention to half the documents in a corpus at random.
This intervention attempts to invert all of the gendered language in a document, whilst maintaining its grammatical coherence.

### Usage

To run, you will need a virtual environment with spaCy installed. Simply run `pip install spacy`, 
then `python -m spacy download en_core_web_lg` to download the default model used in this repo.

Look at `example.py` for example usage.
You will want to initialise a `Substitutor` using a list of gender-word pairs (e.g. he and she) and (optionally) a set of name pairs (e.g. John and Sally). These pairs need not be case sensative.
A substitutor will use these pairs when applying an intervention, along with a special case which handles the words 'him', 'his', 'her', and 'hers' (using POS tag data). 
These four words should not be in the lists of pairs you provide unless you 
want to override its special case behaviour.

The `invert_document` method in `Substitutor` takes a piece of text
and applies a counterfactual intervention to the whole piece of text. I emphasise: all language which it determines is gendered will be 'flipped'.
To apply an intervention probablistically to a series of pieces of text, pass a list of strings to the `probablistic_substitute` method. 
Exactly what constitutes a single unit of text will depend on your corpus---it might be an individual tweet, a Wikipedia article, or a whole a chapter of a book. Where possible, 
avoid splitting contiguous segments of text into smaller fractions, since then coherence might be damaged (e.g. 'Sally' might become 'John' halfway through a paragraph). 

This implementation won't currently work well with social media data, like tweets. I'll look in to adding an implementation for that later.

### Data

I include two sets of pairs. First, the pairs described in Lu et al., 2019 (https://arxiv.org/pdf/1807.11714.pdf), and second, a set of 1000 name pairs 
derived using the method described in Hall Maudslay et al., 2019.

### Implementation Details

The original implementation of CDS worked in two phases:
first, entire corpora were annotated (using a slow but comparatively accurate model in CoreNLP),
then various interventions were applied quickly using that annotation. For ease-of-use (at the cost of efficiency and sometimes accuracy), this
implementation works in one step using spaCy. In my experience the spaCy NER system can sometimes be a little overzealous, tagging names which are also common nouns or verbs (e.g. 'rob' or 'rose') as people when they aren't.
If this matters to you, it may be worth exploring the use of a more complex processing pipeline.
