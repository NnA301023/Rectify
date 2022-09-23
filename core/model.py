"""
import numpy as np
from numpy.linalg import norm
from transformers import BertTokenizer 


TOKENIZER = BertTokenizer.from_pretrained("bert-base-cased")


def cosine(matrix_a, matrix_b):
    return np.dot(matrix_a, matrix_b) / (norm(matrix_a) * norm(matrix_b))

def tokenize(text):
    return np.array(TOKENIZER.convert_token_to_ids(TOKENIZER.tokenize(text)))
"""