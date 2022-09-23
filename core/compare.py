from difflib import get_close_matches


def find_closest(text, data):
    return get_close_matches(text, data, n = 1, cutoff = 0.8)