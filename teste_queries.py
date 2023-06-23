import nltk
# nltk.help.upenn_tagset() get all tags


def is_noun(pos: list) -> bool:
    nltk.download('averaged_perceptron_tagger')
    nltk.download('tagsets')
    # function to test if something is a noun
    return pos[:2] == 'NN' or pos[:2] == 'NNP'


def get_nouns(sentence: str) -> list:
    # pega os substantivos de acordo com a gramática implementada no nltk
    tokenized = nltk.word_tokenize(sentence)
    print(nltk.pos_tag(tokenized))
    nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)]
    return nouns
