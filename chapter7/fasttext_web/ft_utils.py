"""
This module contains the fasttext related code to load the module, get some
words from the module, compute the vectors for the code and then keep them in
memory. Functions to compute the nearest neighbor words based on the question
word are also defined here.

Usage
-----
    $ python ft_utils.py
    loading the model
    model is loaded
    words similar to hungry:
    grownups
    angry
    dachshunds
    tired
    hunger

"""
import fastText
from fastText.util.util import find_nearest_neighbor
from fastText import load_model
import numpy as np
import os


print('loading the model')
FT_MODEL = os.environ.get('FT_MODEL')
if not FT_MODEL:
    raise ValueError('No fasttext model has been linked.')
FT_MODEL = fastText.load_model(FT_MODEL)
print('model is loaded')
threshold = 100000

# Gets words with associated frequency sorted by default by descending order
words, freq = FT_MODEL.get_words(include_freq=True)
words = words[:threshold]
vectors = np.zeros((len(words), FT_MODEL.get_dimension()), dtype=float)
for i in range(len(words)):
    wv = FT_MODEL.get_word_vector(words[i])
    wv = wv / np.linalg.norm(wv)
    vectors[i] = wv

# For efficiency preallocate the memory to calculate cosine similarities
cossims = np.zeros(len(words), dtype=float)


def get_nn_words(question, cossims, model, words, vectors, k=1):
    question = question.lower().strip()
    if question not in words:
        print(question, ' not in vocabulary')
    query = question
    query = model.get_word_vector(query)
    query = query / np.linalg.norm(query)
    seen_words = [question]
    for _ in range(k):
        ban_set = list(map(lambda x: words.index(x), seen_words))
        nn = words[find_nearest_neighbor(query, vectors, ban_set, cossims=cossims)]
        seen_words.append(nn)
        yield nn

def nn(model, question, k):
    print('words similar to {}:'.format(question))
    yield from get_nn_words(question, cossims, model, words, vectors, k)


if __name__ == "__main__":
    for i in nn(FT_MODEL, 'hungry', k=5):
        print(i)
