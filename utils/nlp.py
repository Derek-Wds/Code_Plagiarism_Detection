from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.metrics import BigramAssocMeasures, TrigramAssocMeasures
from nltk.collocations import BigramCollocationFinder, TrigramCollocationFinder
import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from functools import reduce
import string
import logging
import math


def punc_filter():
    """
    :return: a function which takes 1 parameter, and returns true if the para is a punctuation
    """
    return lambda w: w in string.punctuation or w == '``' or w == '\'\''


# tokenization & case-folding
def tokenize(text):
    sentences = sent_tokenize(text)
    # TODO: a more efficient way to concat lists
    words_in_sents = [word_tokenize(sent) for sent in sentences]
    words = reduce(lambda x, y: x+y, words_in_sents)
    return [w.lower() for w in words]


# stop word removal
def remove_stopword(words):
    stopset = set(stopwords.words('english'))
    return [a for a in words if a not in stopset]


# from nltk.stem.lancaster import LancasterStemmer
# from nltk.stem.wordnet import WordNetLemmatizer
# stemming
def stem_word(words):
    st = SnowballStemmer("english")
    return [st.stem(i) for i in words]

# Brief:
# For a document that includes N words, set X = log2(N). Collect number X/3 single word, X/3 bi-word-phrase, X/3 tri-word-phrase, where X = log2(N).
#
# TODO:
# 1. does it make sense to filter only noun phrase
# 2. ? keyword including ['none']
# 3. ? using markov chain to collect phrase


# Question
# 1. how to handle when target passage is part of the classified document?
# A: using only IDF will by pass the term frequency in one article.
#    or catch the signature sentence? Then how to
# 2. how to handle when part of target passage is part of the classified document?
# A: don't know yet. split the passage by subject
def one_gram(tokens):
    punc_detector = punc_filter()
    no_punc = [w for w in tokens if not punc_detector(w)]
    return nltk.FreqDist(no_punc)


def bi_gram(tokens, appearance=0):
    bcf = BigramCollocationFinder.from_words(tokens)
    bcf.apply_word_filter(punc_filter())
    if appearance != 0: bcf.apply_freq_filter(appearance)
    return bcf.ngram_fd


def tri_gram(tokens, appearance=0):
    tcf = TrigramCollocationFinder.from_words(tokens)
    tcf.apply_word_filter(punc_filter())
    if appearance != 0: tcf.apply_freq_filter(appearance)
    return tcf.ngram_fd

