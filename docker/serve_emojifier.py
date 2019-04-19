from flask import Flask
from flask import request
import json
import numpy as np
from emo_utils import *
import tensorflow as tf
from keras.models import Model, model_from_json

with open("emojifier_model.json","r") as model_json_file :
    model_json = model_json_file.read()
model = model_from_json(model_json)
model.load_weights("emojifier_weights.h5")
global graph 
graph = tf.get_default_graph()

#max wordlength
maxLen = 10
#read word vector embeddings
word_to_index, index_to_word, word_to_vec_map = read_glove_vecs("data/glove.6B.50d.txt")
print("model ready")

def sentences_to_indices(X, word_to_index, max_len) :

  """
  Converts an array of sentences (strings) into an array of indices corresponding to words in the sentences.
  The output shape should be such that it can be given to `Embedding()` (described in Figure 4). 

  Arguments:
  X -- array of sentences (strings), of shape (m, 1)
  word_to_index -- a dictionary containing the each word mapped to its index
  max_len -- maximum number of words in a sentence. You can assume every sentence in X is no longer than this. 

  Returns:
  X_indices -- array of indices corresponding to words in the sentences from X, of shape (m, max_len)
  """
  m = X.shape[0]                                   # number of training examples

  # Initialize X_indices as a numpy matrix of zeros and the correct shape (≈ 1 line)
  X_indices = np.zeros((m,max_len))

  for i in range(m):                               # loop over training examples

    # Convert the ith training sentence in lower case and split is into words. You should get a list of words.
    sentence_words = X[i].lower().split()

    # Initialize j to 0
    j = 0

    # Loop over the words of sentence_words
    for w in sentence_words:
      # Set the (i,j)th entry of X_indices to the index of the correct word.
      X_indices[i, j] = word_to_index[w]
      # Increment j to j + 1
      j = j + 1
      #if j == max_len :
          #break


  return X_indices



app = Flask(__name__)

@app.route("/predict", methods=["GET"])
def predict():
    sentence = request.args.get('text')
    x_test = np.array([sentence])
    X_test_indices = sentences_to_indices(x_test,word_to_index,maxLen)
    with graph.as_default():
        prediction= np.argmax(model.predict(X_test_indices))
        print("sentence = %s prediction=%d"%(sentence,prediction))
        return "%d"%(prediction)



