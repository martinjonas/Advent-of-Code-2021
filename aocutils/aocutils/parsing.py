import re

non_word_re = re.compile(r"\W+")


def break_words(s: str):
    return non_word_re.split(s)
